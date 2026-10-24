"""Independent stored-ledger recovery,structured-time alignment and full portfolio checks."""
import copy,gzip,hashlib,json,math
from decimal import Decimal as D
import numpy as np
from run import ROOT,R,HURDLES,BUFFERS,sha,put,reg,module,grid_configs

def near(a,b,tol=1e-9):assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)
def stats(v,d,days,s):
 d=np.asarray(d);r=d[1:]/d[:-1]-1;sd=np.std(r,ddof=1);dd=100*float(np.max(1-v/np.maximum.accumulate(v)));cagr=100*((v[-1]/v[0])**(365/days)-1);near(s['net_return_pct'],100*(v[-1]/v[0]-1),1e-12);near(s['max_drawdown_pct'],dd,1e-12);near(s['daily_mark_drawdown_pct'],100*np.max(1-d/np.maximum.accumulate(d)),1e-12);near(s['cagr_pct'],cagr,1e-12)
 if sd:near(s['sharpe_365'],np.mean(r)/sd*math.sqrt(365),1e-10)
 else:assert s['sharpe_365'] is None
 if dd:near(s['calmar'],cagr/dd,1e-10)
 else:assert s['calmar'] is None

def recover_from_recorded_events(m,scene,counters,multiplier):
 state={'cash':D(10000),'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)};v=np.empty(len(m['ts']));events=sorted([(int(t['axis_index']),'trade',t) for t in scene['trades']]+[(int(f['axis_index']),'fund',f) for f in scene['funding_events']]);assert len({i for i,_,_ in events})==len(events);start=0
 for idx,kind,e in events:
  v[start:idx]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:idx]-float(state['entry_price']))
  if kind=='trade':
   assert e['status']=='filled' and {k:D(x) for k,x in e['state_before'].items()}==state and e['trade_ts_ns']==int(m['ts'][idx]);q=state['signed_units'];cash=state['cash'];change=D(e['change_signed_units']);ref=D(e['reference']);px=D(e['execution']);fee=D(e['cost_parts']['fee']);cost=sum(D(x) for x in e['cost_parts'].values());assert abs(change)==D(e['quantity'])
   if e['opening']:
    assert q==0;new={'cash':cash-fee,'signed_units':change,'entry_price':px,'entry_reference':ref};assert abs(change)*px<=new['cash']
   else:
    assert change==-q;near(D(e['reference_price_PnL_usdt']),q*(ref-state['entry_reference']),1e-13);new={'cash':cash+q*(px-state['entry_price'])-fee,'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)}
   assert abs(cash+q*(ref-state['entry_price'])-(new['cash']+new['signed_units']*(ref-new['entry_price']))-cost)<D('1e-18');assert {k:D(x) for k,x in e['state_after'].items()}==new;state=new;counters['source_recorded_trades_checked']+=1
  else:
   assert int(m['codes'][idx])==4 and e['settlement_ts_ns']==int(m['ts'][idx]) and D(e['signed_units'])==state['signed_units'] and D(e['cash_before'])==state['cash'];base=-state['signed_units']*D(e['mark_price'])*D(e['realized_rate']);assert base==D(e['base_amount_usdt']);amount=D(e['amount_usdt']);assert amount==(base if base>=0 else base*multiplier)
   if amount:state['cash']+=amount
   assert state['cash']==D(e['cash_after']);counters['source_recorded_funding_checked']+=1
  start=idx
 v[start:]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:]-float(state['entry_price']));assert state['signed_units']==0 and {k:D(x) for k,x in scene['terminal_state'].items()}==state
 # The actual event ledger and independent saved-state encoding must produce every same point.
 n=0
 for s in scene['state_segments']:
  a,b=s['axis_start'],s['axis_end_exclusive'];assert a==n;other=float(s['cash'])+float(s['signed_units'])*(m['axis_prices'][a:b]-float(s['entry_price']));assert np.array_equal(v[a:b],other);n=b
 assert n==len(v) and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==scene['summary']['NAV_sha256_f64le'];return v

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');sourceengine=module(ROOT/plan['source_engine']['path'],'parent_independent_axis');assert sha(ROOT/plan['source_engine']['path'])==plan['source_engine']['sha256'];markets={a:sourceengine.load_market(a,x) for a,x in plan['data']['assets'].items()};dtype=np.dtype([('t','<i8'),('k','<i8')]);structured={}
 for a,m in markets.items():
  keys=np.empty(len(m['ts']),dtype=dtype);keys['t']=m['ts'];keys['k']=m['codes'];structured[a]=keys
 union=np.union1d(structured['BTC'],structured['ETH']);start=markets['BTC']['start_ns'];packed=(union['t']-start)*16+union['k'];axis_hash=hashlib.sha256(packed.astype('<i8').tobytes()).hexdigest();assert axis_hash==report['axis']['union_axis_sha256'] and len(union)==report['axis']['union_points'];ix={}
 for a,old in structured.items():
  j=np.searchsorted(old,union,side='right')-1;past=(old[j]['t']<union['t'])|((old[j]['t']==union['t'])&(old[j]['k']<=union['k']));assert (j>=0).all() and past.all() and np.array_equal(j[np.searchsorted(union,old)],np.arange(len(old)));ix[a]=j
 pre=np.flatnonzero(union['k']==5);assert len(pre)==330;daily_idx=np.asarray([0,*pre[1:],len(union)-1]);fold_idx=np.asarray([0,*pre[np.arange(30,330,30)],len(union)-1]);assert len(daily_idx)==331 and len(fold_idx)==12
 counters={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0};vectors={};source_scenes={};source_arcs={}
 for fp,ref in plan['component_sources'].items():
  assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and records[fp]['report_sha256']==ref['report_sha256'] and records[fp]['status']==ref['original_status'];arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));assert reg.fingerprint(arc['spec'])==fp and arc['spec']['parameters']['initial_capital_usdt']==10000;source_scenes[fp]={};source_arcs[fp]=arc
  for k,s in arc['scenes'].items():
   v=recover_from_recorded_events(markets[ref['asset']],s,counters,int(k));assert hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==ref['NAV_sha256_by_cost'][k];vectors[fp,k]=v[ix[ref['asset']]];source_scenes[fp][k]=s['summary']
 assert len(vectors)==36 and counters['source_recorded_funding_checked']==35640 and counters['source_recorded_trades_checked']==sum(len(s['trades']) for arc in source_arcs.values() for s in arc['scenes'].values());scenes=checks=0
 for row in batch:
  cfg=report['configs'][row['name']];arc=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()));spec=json.loads((ROOT/row['spec']).read_text());assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'] and arc['spec']==spec and reg.fingerprint(spec)==row['fingerprint']==arc['fingerprint'];assert [x['weight'] for x in spec['components']]==[1,1] and spec['parameters']['component_capitals_usdt']==[10000,10000] and spec['parameters']['initial_capital_usdt']==20000
  reserves=[x for x in events if x['fingerprint']==row['fingerprint'] and x['status']=='reserved'];assert len(reserves)==1 and reserves[0]['recorded_at_utc']<report['evaluation_started_utc']
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  fps=row['source_fingerprints'];assert [plan['component_sources'][fp]['asset'] for fp in fps]==['BTC','ETH'] and fps==arc['source_fingerprints']
  for k,s in arc['scenes'].items():
   v=vectors[fps[0],k]+vectors[fps[1],k];z=s['summary'];parts=[source_scenes[fp][k] for fp in fps];assert z==cfg['scenes'][k] and v[0]==20000 and len(v)==z['NAV_points']==len(union) and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'];assert s['source_full_NAV_sha256']==[plan['component_sources'][fp]['NAV_sha256_by_cost'][k] for fp in fps];daily=v[daily_idx].tolist();assert daily==z['daily_equity_usdt'];stats(v,daily,330,z);checks+=1
   for j,(a,b) in enumerate(zip(fold_idx,fold_idx[1:])):stats(v[a:b+1],daily[j*30:(j+1)*30+1],30,z['folds'][j]);checks+=1
   assert len(z['folds'])==11 and abs(math.prod(1+f['net_return_pct']/100 for f in z['folds'])-v[-1]/v[0])<1e-12
   trades=[t for fp in fps for t in source_arcs[fp]['scenes'][k]['trades']];funding=[t for fp in fps for t in source_arcs[fp]['scenes'][k]['funding_events']];cost=sum(sum(D(x) for x in t['cost_parts'].values()) for t in trades);gross=sum(D(t['reference_price_PnL_usdt']) for t in trades);fund=sum(D(t['amount_usdt']) for t in funding);near(cost,z['cost_usdt']);near(gross,z['gross_reference_price_PnL_usdt']);near(fund,z['funding_usdt']);near(gross+fund-cost,D(str(v[-1]))-20000);assert z['executions']==sum(x['executions'] for x in parts) and z['round_trips']==sum(x['round_trips'] for x in parts) and z['funding_settlements']==1980 and z['rejected_orders']==z['cash_or_units_violations']==0
   assert z['margin']=={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min(x['margin']['minimum_equity_minus_maintenance_usdt'] for x in parts),'no_cross_margin_netting':True} and D(z['terminal_units'])==0;scenes+=1
  if row['role']=='benchmark':assert cfg['status']=='rejected' and cfg['criteria']=={'reference_only_no_alpha_qualification':False};continue
  axes={'BTC_return_hurdle':HURDLES,'BTC_exit_buffer_fraction':BUFFERS,'ETH_return_hurdle':HURDLES};ns=[x for x in grid_configs(report['configs']).values() if x['role']=='candidate' and all(abs(vals.index(x[p])-vals.index(cfg[p]))<=1 for p,vals in axes.items())];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);assert cfg['sensitivity']=={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'three_dimensional_local_3x_positive_fraction':frac};ss=cfg['scenes'];pos=sum(x['net_return_pct']>0 for x in ss['1']['folds']);assert pos==cfg['positive_folds_1x'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];expected={'positive_all_costs':all(x['net_return_pct']>0 for x in ss.values()),'eight_positive_1x_folds':pos>=8,'composite_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'full3D_neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_sleeve_collateral':all(x['cash_or_units_violations']==0 for x in ss.values()),'no_source_order_rejections':all(x['rejected_orders']==0 for x in ss.values()),'no_either_sleeve_margin_violations':all(x['margin']['independent_sleeve_violations']==0 for x in ss.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in ss.values())};assert cfg['criteria']==expected and (cfg['status']=='passed')==all(expected.values())
 assert len(batch)==27 and scenes==81 and checks==972;assert all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items());out={'passed':True,'parent_financial_configs':27,'candidate_parents':27,'benchmark_parents':0,'source_configs_reused_read_only':12,'source_cost_scenes_rebuilt_and_original_SHA_verified':36,**counters,'new_parent_cost_scenes_audited':scenes,'common_axis_points_per_scene':len(union),'new_parent_NAV_points_audited':len(union)*scenes,'independent_overall_and_fold_metric_checks':checks,'structured_key_alignment_independently_verified':True,'raw_1_1_means_20000_collateral_not_normalized':True,'source_signals_orders_and_funding_models_not_rerun':True,'protected_inputs_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)

if __name__=='__main__':main()
