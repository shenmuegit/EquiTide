"""Independent recorded-order/funding replay and structured-clock ownership audit."""
import ast,gzip,hashlib,json,math
from decimal import Decimal as D
import numpy as np
import engine
from run import ROOT,R,reg,sha,put,module
base=module(R/'audit_helpers.py','recorded_ledger_independent_audit')
near,metrics,verify_axis,verify_recent,replay=base.near,base.metrics,base.verify_axis,base.verify_recent,base.recover_from_recorded_events

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');assert len(batch)==40 and report['summary']['cost_scenarios']==120 and report['frozen_plan_sha256']==sha(R/'plan.json') and sha(R/'engine.py')==sha(ROOT/plan['source_engine']['path']);markets={a:engine.load_market(a,fs) for a,fs in plan['data']['assets'].items()}
 for m in markets.values():verify_axis(m)
 dt=np.dtype([('t','<i8'),('k','<i8')]);structured={}
 for a,m in markets.items():
  q=np.empty(len(m['ts']),dtype=dt);q['t']=m['ts'];q['k']=m['codes'];structured[a]=q
 union=np.union1d(structured['BTC'],structured['ETH']);packed=(union['t']-markets['BTC']['start_ns'])*16+union['k'];assert hashlib.sha256(packed.astype('<i8').tobytes()).hexdigest()==report['parent_axis']['union_axis_sha256'];projections={}
 for a,old in structured.items():
  j=np.searchsorted(old,union,side='right')-1;assert (j>=0).all() and ((old[j]['t']<union['t'])|((old[j]['t']==union['t'])&(old[j]['k']<=union['k']))).all() and np.array_equal(j[np.searchsorted(union,old)],np.arange(len(old)));projections[a]=j
 pre=np.flatnonzero(union['k']==5);assert len(pre)==370;days=np.asarray([0,*pre[1:],len(union)-1]);folds=np.asarray([0,*pre[np.arange(30,370,30)],len(union)-1]);common={'daily_indices':days,'ts':union['t']};vectors={};ss={};counters={'source_recorded_trades_checked':0,'source_recorded_funding_checked':0}
 for fp,x in plan['component_sources'].items():
  assert sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256'] and records[fp]['status']==x['original_status'] and records[fp]['report_sha256']==x['report_sha256'];arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()));assert reg.fingerprint(arc['spec'])==fp and arc['spec']['parameters']['initial_capital_usdt']==10000 and arc['spec']['parameters']['fixed_entry_notional_usdt']==x['fixed_entry_notional_usdt']
  for k,z in arc['scenes'].items():
   v=replay(markets[x['asset']],z,counters,int(k));assert hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==x['NAV_sha256_by_cost'][k];vectors[fp,k]=v[projections[x['asset']]];ss[fp,k]=z['summary']
 assert len(vectors)==36 and counters==plan['recorded_source_events'];grid={}
 for name,x in plan['read_only_anchor_references'].items():
  c=json.loads((ROOT/x['report']).read_text())['configs'][name];p=json.loads((ROOT/x['spec']).read_text())['parameters'];assert records[x['fingerprint']]['status']==x['original_status'] and records[x['fingerprint']]['report_sha256']==x['report_sha256'];grid[name]={**c,'BTC_bank_units':p.get('BTC_bank_units',1),'ETH_exit_buffer_fraction':p['ETH_exit_buffer_fraction'],'ETH_trend_lookback_days':p['ETH_trend_lookback_days']}
 grid.update({n:c for n,c in report['configs'].items() if c['role']=='candidate'});assert len(grid)==63
 axes={'BTC_bank_units':[.25,.375,.5,.625,.75,.875,1],'ETH_exit_buffer_fraction':[-.015,-.01,-.005],'ETH_trend_lookback_days':[27,28,29]};checks=recentchecks=scenes=0
 for row in batch:
  c=report['configs'][row['name']];sp=json.loads((ROOT/row['spec']).read_text());arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));assert sha(ROOT/c['archive'])==c['archive_sha256'] and arc['spec']==sp and arc['fingerprint']==row['fingerprint']==reg.fingerprint(sp);p=sp['parameters'];w=row['BTC_bank_units'];ww=[w,2-w];fps=row['source_fingerprints'];capital=20000
  assert p['raw_component_multipliers']==row['raw_component_multipliers']==ww and [x['weight'] for x in sp['components']]==ww and [x['fingerprint'] for x in sp['components']]==fps and p['initial_capital_usdt']==c['capital_usdt']==capital and p['source_component_parameters']==[records[fp]['spec']['parameters'] for fp in fps]
  assert p['owned_component_capitals_usdt']==[10000*w,10000*(2-w)] and p['effective_owned_entry_budgets_usdt']==[1000*w,3000*(2-w)] and sum(p['owned_component_capitals_usdt'])==capital and [plan['component_sources'][fp]['asset'] for fp in fps]==['BTC','ETH']
  if row['role']=='candidate':
   a,b=p['source_component_parameters'];S=c['ETH_trend_lookback_days'];E=c['ETH_exit_buffer_fraction'];assert a['lookback_days']==31 and a['return_hurdle']==.04 and a['exit_buffer_fraction']==.01 and a['fixed_entry_notional_usdt']==1000 and b['lookback_days']==3 and b['return_hurdle']==.025 and b['exit_buffer_fraction']==E and b['trend_lookback_days']==S and b['trend_gate_lookbacks_days']==[S-1,S,S+1] and b['trend_gate_application']=='entries_only' and b['fixed_entry_notional_usdt']==3000
  rv=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(rv)==1 and rv[0]['recorded_at_utc']<report['evaluation_started_utc']
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,z in arc['scenes'].items():
   v=np.zeros(len(union))
   for fp,a in zip(fps,ww):v+=vectors[fp,k]*a
   s=z['summary'];parts=[ss[fp,k] for fp in fps];assert s==c['scenes'][k] and v[0]==capital and s['initial_capital_usdt']==capital and s['NAV_points']==len(v)==545013 and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==s['NAV_sha256_f64le'] and z['source_fingerprints']==fps and z['source_full_NAV_sha256']==[x['NAV_sha256_f64le'] for x in parts];daily=v[days].tolist();assert daily==s['daily_equity_usdt'];metrics(v,daily,370,s);checks+=1
   for j,(a,b) in enumerate(zip(folds,folds[1:])):
    lo,hi=j*30,min((j+1)*30,370);f=s['folds'][j];assert f['duration_days']==hi-lo and f['start_utc']==engine.stamp(int(union['t'][a])) and f['end_exclusive_utc']==engine.stamp(int(union['t'][b]));metrics(v[a:b+1],daily[lo:hi+1],hi-lo,f);checks+=1
   assert len(s['folds'])==13 and abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/capital)<1e-12;verify_recent(v,common,s);recentchecks+=9
   money=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt'];counts=['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']
   for f in money:near(s[f],sum(a*x[f] for a,x in zip(ww,parts)))
   for f in counts:assert s[f]==sum(x[f] for x in parts)
   for f,val in s['cost_parts_usdt'].items():near(val,sum(a*x['cost_parts_usdt'][f] for a,x in zip(ww,parts)))
   near(s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],v[-1]-capital);near(s['cost_pct_initial'],s['cost_usdt']/capital*100);assert all(D(x['terminal_units'])==0 for x in parts) and D(s['terminal_units'])==0
   assert s['margin']=={'independent_sleeve_violations':sum(x['margin']['violations'] for x in parts),'minimum_individual_sleeve_cushion_usdt':min((a*x['margin']['minimum_equity_minus_maintenance_usdt'] for a,x in zip(ww,parts) if x['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True};scenes+=1
  if row['role']=='benchmark':assert c['status']=='rejected' and c['criteria']=={'reference_only_no_alpha_qualification':False};continue
  ns=[x for x in grid.values() if all(abs(vals.index(x[p])-vals.index(c[p]))<=1 for p,vals in axes.items())];frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)
  def strong(x):return all(sum(f['net_return_pct']>0 for f in x['scenes'][k]['recent40']['folds'])>=6 for k in ['1','2','3'])
  rf=sum(strong(x) for x in ns)/len(ns);assert c['sensitivity']=={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'dimension_count':3,'local_3x_neighbor_positive_fraction':frac,'local_recent6of8_allcost_fraction':rf};s=c['scenes'];pos=sum(f['net_return_pct']>0 for f in s['1']['folds'][:12]);recentpos=sum(f['net_return_pct']>0 for f in s['1']['recent40']['folds']);assert c['positive_complete_30d_folds_1x']==pos and c['recent40_positive_5d_folds_1x']==recentpos and c['positive_folds_1x']==sum(f['net_return_pct']>0 for f in s['1']['folds']);ratio=s['1']['gross_reference_PnL_to_execution_cost']
  expected={'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':pos>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_1x_folds':recentpos>=6,'recent40_six_of_eight_positive5d_all_costs':strong(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':frac>=.6,'local_recent6of8_allcost_gte60pct':rf>=.6,'four_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(z['margin']['independent_sleeve_violations']==0 for z in s.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in s.values()),'minimum180days':True};assert c['criteria']==expected and c['failed_criteria']==[k for k,v in expected.items() if not v] and (c['status']=='passed')==all(expected.values())
 assert scenes==120 and checks==1680 and recentchecks==1080 and all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items())
 for path in ['run.py','audit.py']:
  tree=ast.parse((R/path).read_text());assert not any(isinstance(x,ast.Call) and ((isinstance(x.func,ast.Attribute) and x.func.attr in ['simulate','target','trade','funding_amount']) or (isinstance(x.func,ast.Name) and x.func.id in ['simulate','target','trade','funding_amount'])) for x in ast.walk(tree))
 out={'passed':True,'actual_financial_configs':40,'actual_candidates':36,'actual_benchmarks':4,'new_native_components':0,'new_passive_parents':40,'source_native_components_reused_readonly':12,'source_native_cost_NAVs_recovered':36,**counters,'cost_scenes_audited':scenes,'full_NAV_points_per_scene':len(union),'full_NAV_points_audited':len(union)*scenes,'independent_overall_and_fold_metric_checks':checks,'independent_recent40_and_fold_metric_checks':recentchecks,'structured_clock_raw_units_capital20000_verified':True,'strict_new_eachcost_and_neighborhood_gates_verified':True,'old27_qualifications_unchanged':True,'source_models_not_rerun':True,'protected_inputs_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
