"""Independent signed ledger, funding, causal sizing, sampled curves and risk verification."""
import bisect,copy,gzip,hashlib,json,math,statistics
from decimal import Decimal as D,ROUND_CEILING,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
import engine
from run import ROOT,R,LOOKS,HURDLES,EXITS,sha,put,reg,grid_configs,neighbors

def near(a,b,tol=1e-9):assert abs(float(a)-float(b))<=tol*max(1,abs(float(a)),abs(float(b))),(a,b)

def metrics(curve,daily,days,saved):
 values=np.asarray(curve);d=np.asarray(daily);rr=d[1:]/d[:-1]-1;sd=np.std(rr,ddof=1);cagr=100*((values[-1]/values[0])**(365/days)-1);dd=float(max(100*(1-values/np.maximum.accumulate(values))));near(saved['net_return_pct'],100*(values[-1]/values[0]-1),1e-12);near(saved['max_drawdown_pct'],dd,1e-12);near(saved['cagr_pct'],cagr,1e-12);near(saved['daily_mark_drawdown_pct'],max(100*(1-d/np.maximum.accumulate(d))),1e-12)
 if sd:near(saved['sharpe_365'],np.mean(rr)/sd*math.sqrt(365),1e-10)
 else:assert saved['sharpe_365'] is None
 if dd:near(saved['calmar'],cagr/dd,1e-10)
 else:assert saved['calmar'] is None

def verify_axis(m):
 f,h=m['frame'],m['hour'];codes=m['codes'];ts=m['ts'];S,E=m['start_ns'],m['end_ns'];assert len(ts)==58923 and np.all(np.diff(ts)>=0) and np.array_equal(np.lexsort((codes,ts)),np.arange(len(ts)))
 for code in range(10):assert np.all(m['axis_prices'][codes==code]>0)
 ix=np.flatnonzero(codes==1);assert len(ix)==57600 and ts[ix].tolist()==f['available_ts'][engine.START*1440+1:engine.END*1440+1].to_list();assert np.array_equal(m['axis_prices'][ix],np.asarray([float(x) for x in f['close'][engine.START*1440+1:engine.END*1440+1]]))
 for code in [5,6,7]:
  ix=np.flatnonzero(codes==code);assert len(ix)==40 and ts[ix].tolist()==[S+i*engine.DAY for i in range(40)]
  assert m['axis_prices'][ix].tolist()==[float(f['open'][i*1440+1]) for i in range(engine.START,engine.END)]
 for code in [3,4]:
  ix=np.flatnonzero(codes==code);assert len(ix)==120 and ts[ix].tolist()==[e['settlement_ts'] for e in m['funds']]
  assert m['axis_prices'][ix].tolist()==[float(e['mark_price_at_settlement']) for e in m['funds']]
 ix=np.flatnonzero(codes==2);expected=[j for j,z in enumerate(h['available_ts']) if S<int(z)<=E];assert len(ix)==960 and ts[ix].tolist()==[int(h['available_ts'][j]) for j in expected];assert len(m['controls'])==201 and len(m['daily_indices'])==41 and len(m['fold_indices'])==9
 assert ts[0]==S and ts[-1]==E and codes[0]==0 and codes[-1]==9

def independent_margin(m,segments):
 ta=[int(m['ts'][s['axis_start']]) for s in segments];tb=[int(m['ts'][s['axis_end_exclusive']-1]) for s in segments];minimum=None;count=viol=0
 for hour in m['hour'].to_dicts():
  if hour['open_ts']<m['start_ns'] or hour['available_ts']>m['end_ns']:continue
  lo=bisect.bisect_left(tb,hour['open_ts']);hi=bisect.bisect_left(ta,hour['available_ts'])
  for s in segments[lo:hi]:
   q=D(s['signed_units'])
   if not q:continue
   adverse=hour['low'] if q>0 else hour['high'];cushion=D(s['cash'])+q*(adverse-D(s['entry_price']))-D('.01')*abs(q)*adverse;minimum=cushion if minimum is None else min(minimum,cushion);count+=1;viol+=int(cushion<=0)
 return minimum,count,viol

def main():
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');markets={a:engine.load_market(a,x) for a,x in plan['data']['assets'].items()};assert len(batch)==42 and report['frozen_plan_sha256']==sha(R/'plan.json') and report['anchor_sources']==plan['anchor_sources'] and report['summary']['cost_scenarios']==3*len(batch)==126
 for m in markets.values():verify_axis(m)
 scenes=fills=funding_checks=decision_checks=metric_checks=margin_checks=0
 for row in batch:
  cfg=report['configs'][row['name']];arc=json.loads(gzip.decompress((ROOT/cfg['archive']).read_bytes()));spec=json.loads((ROOT/row['spec']).read_text());assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'] and arc['spec']==spec and arc['fingerprint']==row['fingerprint']==reg.fingerprint(spec);reserved=[e for e in events if e['fingerprint']==row['fingerprint'] and e['status']=='reserved'];assert len(reserved)==1 and reserved[0]['recorded_at_utc']<report['evaluation_started_utc'];m=markets[row['asset']];p=spec['parameters'];f=m['frame'];native=m['closes'];prices=[int(x*D(10)**18) for x in native];meta=m['meta'];lot=D(meta['lot_size']);tick=D(meta['tick_size'])
  if records[row['fingerprint']]['status']!='reserved':assert records[row['fingerprint']]['report_sha256']==sha(R/'report.json')
  for k,s in arc['scenes'].items():
   mult=int(k);state={x:D(v) for x,v in {'cash':'10000','signed_units':'0','entry_price':'0','entry_reference':'0'}.items()};v=np.empty(len(m['ts']));start=0;ti=fi=di=0;expected_segments=[];segstart=0;segstate=copy.deepcopy(state);wanted=0
   def fill(idx,i,change,opening,terminal=False):
    nonlocal state,ti,fills
    t=s['trades'][ti];assert t['status']=='filled' and t['axis_index']==idx and t['decision_index']==i and t['trade_ts_ns']==int(m['ts'][idx]) and t['terminal']==terminal and t['opening']==opening and t['asset']==row['asset'];assert {x:D(y) for x,y in t['state_before'].items()}==state
    cash,q,entry,er=[state[x] for x in ['cash','signed_units','entry_price','entry_reference']];ref=f['open'][i*1440+1];qty=abs(change);adv=D(t['lagged_ADV']);sig=D(t['lagged_sigma']);part=qty*ref/adv;near(adv,statistics.mean(float(x['quote_volume']) for x in m['rows'][i-20:i]),1e-13);rr=[math.log(float(native[j])/float(native[j-1])) for j in range(i-20,i)];near(sig,statistics.stdev(rr),1e-13)
    assert D(t['change_signed_units'])==change and D(t['quantity'])==qty and D(t['reference'])==ref and D(t['participation'])==part<=D('.001') and qty%lot==0
    fee,spread,slip=D('.0005')*mult,D('.0001')*mult,D('.0002')*mult;impact=D('.5')*sig*part.sqrt()*mult;theory=ref*(1+(spread+slip+impact)*(1 if change>0 else -1));px=(theory/tick).to_integral_value(rounding=ROUND_CEILING if change>0 else ROUND_FLOOR)*tick;assert D(t['execution'])==px and px%tick==0 and qty*px>=D(meta['min_notional']);parts={'fee':qty*px*fee,'half_spread':qty*ref*spread,'slippage':qty*ref*slip,'impact':qty*ref*impact,'tick_rounding':qty*abs(px-theory)};assert all(D(t['cost_parts'][a])==b for a,b in parts.items()) and D(t['cost_usdt'])==sum(parts.values())
    if opening:assert q==0;new={'cash':cash-parts['fee'],'signed_units':change,'entry_price':px,'entry_reference':ref};realized=refpnl=D(0);assert qty*px<=new['cash']
    else:assert change==-q;realized=q*(px-entry);refpnl=q*(ref-er);new={'cash':cash+realized-parts['fee'],'signed_units':D(0),'entry_price':D(0),'entry_reference':D(0)}
    assert D(t['realized_price_PnL_usdt'])==realized and D(t['reference_price_PnL_usdt'])==refpnl and {x:D(y) for x,y in t['state_after'].items()}==new;assert abs(cash+q*(ref-entry)-(new['cash']+new['signed_units']*(ref-new['entry_price']))-sum(parts.values()))<D('1e-18');state=new;ti+=1;fills+=1
   for idx0 in m['controls']:
    idx=int(idx0);before=copy.deepcopy(state);v[start:idx]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:idx]-float(state['entry_price']));code=int(m['codes'][idx]);ref=int(m['refs'][idx])
    if code==4:
     e=m['funds'][ref];t=s['funding_events'][fi];q=state['signed_units'];raw=-q*e['mark_price_at_settlement']*e['realized_rate'];amount=raw*mult if raw<0 else raw;assert t['axis_index']==idx and t['settlement_ts_ns']==e['settlement_ts'] and t['available_ts_ns']==e['available_ts'] and t['source_index']==e['source_index'] and D(t['signed_units'])==q and D(t['realized_rate'])==e['realized_rate'] and D(t['mark_price'])==e['mark_price_at_settlement'];assert D(t['cash_before'])==state['cash'] and D(t['base_amount_usdt'])==raw and D(t['amount_usdt'])==amount
     if amount:state['cash']+=amount
     assert D(t['cash_after'])==state['cash'];fi+=1;funding_checks+=1
    elif code==6:
     if p.get('signal_mode')=='constant_long_reference':wanted=1;roc=None
     else:
      j=ref-1;L=p['lookback_days'];assert j-L>=0;n,d=prices[j]-prices[j-L],prices[j-L];hurdle=F(str(p['return_hurdle']));desired=1 if n*hurdle.denominator>hurdle.numerator*d else -1 if n*hurdle.denominator < -hurdle.numerator*d else 0
      buffer=F(str(p['exit_buffer_fraction']))
      if desired==0:
       if state['signed_units']>0 and n*buffer.denominator>-buffer.numerator*d:desired=1
       elif state['signed_units']<0 and n*buffer.denominator<buffer.numerator*d:desired=-1
      wanted=desired;roc=F(n,d)
     dec=s['decisions'][di];assert dec['decision_index']==ref and dec['execution_ts_ns']==int(m['ts'][idx]) and dec['signal_available_ts_ns']+engine.MIN==dec['execution_ts_ns'] and dec['desired_direction']==wanted and dec['fixed_entry_notional_usdt']==p['fixed_entry_notional_usdt'] and {x:D(y) for x,y in dec['state_before'].items()}==state
     assert dec['lookback_return_exact'] is None if roc is None else F(dec['lookback_return_exact'])==roc
     q=state['signed_units']
     if q and (1 if q>0 else -1)!=wanted:fill(idx,ref,-q,False)
     decision_checks+=1
    elif code==7:
     if wanted and state['signed_units']==0:
      steps=F(str(p['fixed_entry_notional_usdt']))/(F(native[ref-1])*F(lot));qty=D(steps.numerator//steps.denominator)*lot;fill(idx,ref,D(wanted)*qty,True)
     assert {x:D(y) for x,y in s['decisions'][di]['state_after'].items()}==state;di+=1
    elif code==9:
     if state['signed_units']:fill(idx,engine.END,-state['signed_units'],False,True)
    if state!=before:
     if idx>segstart:expected_segments.append({'axis_start':segstart,'axis_end_exclusive':idx,**segstate})
     segstart=idx;segstate=copy.deepcopy(state)
    start=idx
   v[start:]=float(state['cash'])+float(state['signed_units'])*(m['axis_prices'][start:]-float(state['entry_price']));expected_segments.append({'axis_start':segstart,'axis_end_exclusive':len(v),**segstate});saved_segments=[{a:(D(b) if a not in ['axis_start','axis_end_exclusive'] else b) for a,b in x.items()} for x in s['state_segments']];assert expected_segments==saved_segments and di==40 and fi==120 and ti==len(s['trades']) and state['signed_units']==0 and {x:D(y) for x,y in s['terminal_state'].items()}==state
   z=s['summary'];assert z==cfg['scenes'][k] and hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==z['NAV_sha256_f64le'] and z['NAV_points']==len(v)==58923 and (v>0).all();daily=v[m['daily_indices']].tolist();assert daily==z['daily_equity_usdt'];metrics(v,daily,40,z);metric_checks+=1
   for j,(a,b) in enumerate(zip(m['fold_indices'],m['fold_indices'][1:])):metrics(v[a:b+1],daily[j*5:(j+1)*5+1],5,z['folds'][j]);metric_checks+=1
   assert len(z['folds'])==8 and abs(math.prod(1+x['net_return_pct']/100 for x in z['folds'])-v[-1]/10000)<1e-12
   gross=sum(D(t['reference_price_PnL_usdt']) for t in s['trades']);fund=sum(D(t['amount_usdt']) for t in s['funding_events']);basefund=sum(D(t['base_amount_usdt']) for t in s['funding_events']);cost=sum(sum(D(x) for x in t['cost_parts'].values()) for t in s['trades']);near(gross,z['gross_reference_price_PnL_usdt']);near(fund,z['funding_usdt']);near(basefund,z['base_funding_same_exposure_usdt']);near(fund-basefund,z['funding_stress_increment_usdt']);near(sum(D(t['amount_usdt']) for t in s['funding_events'] if D(t['amount_usdt'])>0),z['funding_income_usdt']);near(-sum(D(t['amount_usdt']) for t in s['funding_events'] if D(t['amount_usdt'])<0),z['funding_outflow_usdt']);near(cost,z['cost_usdt']);near(gross+fund-cost,D(str(v[-1]))-10000);assert z['executions']==len(s['trades']) and z['round_trips']==sum(not t['opening'] for t in s['trades']) and z['rejected_orders']==z['cash_or_units_violations']==0
   for mask,field in [(np.isin(m['codes'],[0,2,3,4,9]),'mark_observation_drawdown_pct'),(np.isin(m['codes'],[0,1,3,4,5,6,7,8,9]),'trade_proxy_drawdown_pct')]:
    vv=v[mask];near(100*np.max(1-vv/np.maximum.accumulate(vv)),z[field]);assert z[field]<=z['max_drawdown_pct']+1e-10
   minimum,count,viol=independent_margin(m,s['state_segments']);assert count==z['margin']['state_hour_extreme_bounding_checks'] and viol==z['margin']['violations']
   if count:near(minimum,z['margin']['minimum_equity_minus_maintenance_usdt'],1e-10)
   margin_checks+=count;scenes+=1
  if cfg.get('role')=='benchmark':assert cfg['status']=='rejected' and cfg['criteria']=={'reference_only_no_alpha_qualification':False};continue
  ns=neighbors(cfg,grid_configs(report['configs']));frac=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);assert cfg['sensitivity']=={'neighbor_names':[x['name'] for x in ns],'neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':frac};ss=cfg['scenes'];positive=sum(x['net_return_pct']>0 for x in ss['1']['folds']);ratio=ss['1']['gross_reference_PnL_to_execution_cost'];expected={'positive_all_costs':all(x['net_return_pct']>0 for x in ss.values()),'six_positive_of_eight_1x_folds':positive>=6,'minimum180days_evidence':False,'composite_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_collateral':all(x['cash_or_units_violations']==0 for x in ss.values()),'no_order_rejections':all(x['rejected_orders']==0 for x in ss.values()),'no_margin_proxy_violations':all(x['margin']['violations']==0 for x in ss.values()),'terminal_flat':all(float(x['terminal_units'])==0 for x in ss.values())};assert cfg['criteria']==expected and cfg['positive_folds_1x']==positive and (cfg['status']=='passed')==all(expected.values())
 refs=json.loads((R/'anchors.json').read_text());assert report['read_only_anchor_references']==refs and len(refs)==0;docs={}
 for name,ref in refs.items():
  path=ref['source_report'];assert sha(ROOT/path)==ref['source_report_sha256']
  if path not in docs:docs[path]=json.loads((ROOT/path).read_text())
  c=docs[path]['configs'][name];rec=records[ref['fingerprint']];assert c['fingerprint']==ref['fingerprint'] and rec['status']==c['status']==ref['original_status'] and rec['report_sha256']==ref['source_report_sha256'];assert sha(ROOT/ref['source_archive'])==ref['source_archive_sha256'];assert all(c['scenes'][k]['NAV_sha256_f64le']==h for k,h in ref['NAV_sha256_by_cost'].items())
 assert len(grid_configs(report['configs']))==36 and {c['exit_buffer_fraction'] for c in grid_configs(report['configs']).values()}=={.005,.01,.02}
 assert scenes==126 and funding_checks==15120 and decision_checks==5040 and metric_checks==1134;assert all(sha(ROOT/p)==h for p,h in json.loads((R/'context.json').read_text())['account_hashes_before'].items());out={'passed':True,'actual_financial_configs':42,'candidate_configs':36,'benchmark_configs':6,'cost_scenes_audited':scenes,'full_NAV_points_per_scene':58923,'full_NAV_points_audited':scenes*58923,'independent_overall_and_fold_metric_checks':metric_checks,'causal_daily_decisions_checked':decision_checks,'actual_fills_independently_verified':fills,'actual_funding_settlements_verified_including_flat':funding_checks,'independent_state_hour_margin_checks':margin_checks,'buffer_exit_hysteresis_integer_signal_verified':True,'read_only_anchor_configs_verified':0,'old_anchor_NAV_or_status_not_recomputed':True,'signed_cash_funding_and_price_PnL_identity_verified':True,'funding_rates_not_used_for_signal_or_quantity':True,'protected_source_accounts_unchanged':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)

if __name__=='__main__':main()
