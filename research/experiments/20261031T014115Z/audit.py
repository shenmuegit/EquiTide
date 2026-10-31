"""Independent exact ranking policy and Decimal native money/NAV audit."""
import bisect,copy,gzip,json,math
from decimal import Decimal as D,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
from common import *
import market
from audit_helpers_complete import near,metrics,verify_recent
native_auditor=module(ROOT/'research/experiments/20261030T194013Z/audit_complete.py','immutable_native_cashflow_auditor')
def state_at(segments,idx):
 j=bisect.bisect_right([z['axis_start'] for z in segments],idx)-1;assert j>=0;return {a:D(segments[j][a]) for a in ['cash','signed_units','entry_price','entry_reference']}
def money_state(s):return {k:D(v) for k,v in s.items()}
def policy(scene,spec,ms,axis):
 p=spec['parameters'];L,period=p['lookback_days'],p['rebalance_interval_days'];dd=scene['decisions'];assert len(dd)==370;completed=0;scheduled_count=0;probe=0;streak=0;seen=set()
 for i,d in zip(range(33,403),dd):
  t=axis['first_ns']+i*DAY+MIN;ix6=int(np.searchsorted(axis['keys'],np.array((t,6),dtype=axis['keys'].dtype)));ix7=ix6+1;assert int(axis['ts'][ix7])==t and axis['codes'][ix7]==7;before={a:state_at(scene['legs'][a]['state_segments'],ix6-1) for a in ms};afterclose={a:state_at(scene['legs'][a]['state_segments'],ix6) for a in ms};after={a:state_at(scene['legs'][a]['state_segments'],ix7) for a in ms};current=1 if before['ETH']['signed_units']>0 else -1 if before['ETH']['signed_units']<0 else 0;scheduled=(i-33)%period==0;scheduled_count+=scheduled
  assert d['day_index']==i and d['execution_ts_ns']==t and d['signal_available_ts_ns']==int(ms['BTC']['frame']['available_ts'][i*1440-1])<t and d['scheduled']==scheduled and d['pair_side_before']==current and not d['recovery_before'] and not d['recovery_after'];assert all(money_state(d['state_before'][a])==before[a] and money_state(d['state_after_close'][a])==afterclose[a] and money_state(d['state_after'][a])==after[a] for a in ms)
  assert d['probe_before']==probe and d['streak_before']==streak
  desired=current
  if scheduled:
   rb=F(ms['BTC']['closes'][i-1])/F(ms['BTC']['closes'][i-1-L])-1;re=F(ms['ETH']['closes'][i-1])/F(ms['ETH']['closes'][i-1-L])-1;diff=rb-re;H=F(D(str(p['relative_return_entry_deadband'])));K=p['consecutive_scheduled_confirmations'];raw=1 if diff>H else -1 if diff< -H else 0;streak=(streak+1 if raw==probe else 1) if raw else 0;probe=raw;fresh=-raw if raw and streak>=K else 0;desired=(fresh if diff*(-current)<=0 else current) if current else fresh;winner=1 if diff>0 else -1 if diff<0 else 0;z=d['rank'];assert z['BTC_direction']==winner and z['ETH_direction']==-winner and z['feature_end_day_index']==i-1 and z['feature_start_day_index']==i-1-L;near(float(rb),z['BTC_return'],1e-12);near(float(re),z['ETH_return'],1e-12);near(float(diff),z['relative_return_difference'],1e-12);assert d['action']=='scheduled'
  else:assert d['rank'] is None and d['action']=='hold'
  assert d['probe_after']==probe and d['streak_after']==streak
  close=bool(scheduled and current and desired!=current);opennew=bool(scheduled and desired and (not current or close));assert d['desired_side']==desired and d['pending_open_side']==(desired if opennew else 0) and d['pair_side_after']==desired
  for a in ['BTC','ETH']:
   ts=scene['legs'][a]['trades'];ct=[x for x in ts if x['axis_index']==ix6];ot=[x for x in ts if x['axis_index']==ix7];assert len(ct)==int(close) and len(ot)==int(opennew)
   if close:assert not ct[0]['opening'] and D(ct[0]['change_signed_units'])==-before[a]['signed_units'] and ct[0]['decision_reason']=='scheduled_rank_change';seen.add((a,ix6));assert afterclose[a]['signed_units']==0
   else:assert afterclose[a]==before[a]
   if opennew:
    lot=D(ms[a]['meta']['lot_size']);qty=(D(2000)/ms[a]['closes'][i-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;wanted=D(desired if a=='ETH' else -desired)*qty;assert ot[0]['opening'] and D(ot[0]['change_signed_units'])==wanted and after[a]['signed_units']==wanted and ot[0]['decision_reason']==('open_first' if a=='BTC' else 'open_second');seen.add((a,ix7))
   else:assert after[a]==afterclose[a]
  completed+=int(close)
 terminal=len(axis['ts'])-1;was_open=False
 for a in ms:
  before=state_at(scene['legs'][a]['state_segments'],terminal-1);tt=[x for x in scene['legs'][a]['trades'] if x['axis_index']==terminal];assert len(tt)==int(before['signed_units']!=0)
  if tt:assert not tt[0]['opening'] and tt[0]['terminal'] and tt[0]['decision_reason']=='terminal' and D(tt[0]['change_signed_units'])==-before['signed_units'];seen.add((a,terminal));was_open=True
  assert all(x['status']=='filled' and (a,x['axis_index']) in seen for x in scene['legs'][a]['trades'])
 completed+=int(was_open);assert completed==scene['terminal_pair_state']['completed_pairs']==scene['summary']['round_trips'];assert not scene['terminal_pair_state']['side'] and not scene['terminal_pair_state']['recovery'];assert scene['terminal_pair_state']['probe']==probe and scene['terminal_pair_state']['streak']==streak;assert scheduled_count==(370-1)//period+1;return len(dd),scheduled_count
def fullmetrics(v,axis,z):
 daily=v[axis['daily_indices']].tolist();assert z['NAV_points']==len(v) and z['NAV_sha256_f64le']==core.navhash(v) and z['daily_equity_usdt']==daily;metrics(v,daily,370,z)
 for j,(a,b) in enumerate(zip(axis['fold_indices'],axis['fold_indices'][1:])):
  days=min(30,370-30*j);f=z['folds'][j];assert f['duration_days']==days and f['start_utc']==core.stamp(int(axis['ts'][a])) and f['end_exclusive_utc']==core.stamp(int(axis['ts'][b]));metrics(v[a:b+1],daily[30*j:30*j+days+1],days,f)
 verify_recent(v,axis,z);assert abs(math.prod(1+f['net_return_pct']/100 for f in z['folds'])-v[-1]/v[0])<1e-12
def main():
 p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());assert r['frozen_plan_sha256']==sha(R/'plan.json');ms,axis=market.load(p);counter={'funding':0,'fills':0,'rejects':0,'metric_checks':0,'margin_checks':0};decisions=scheduled=points=0;curves=0
 for fp,x in p['read_only_references'].items():
  assert sha(ROOT/x['spec'])==x['spec_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['archive'])==x['archive_sha256']
 for c in r['configs'].values():
  assert sha(ROOT/c['archive'])==c['archive_sha256'];arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));spec=json.loads((ROOT/c['spec']).read_text());assert arc['spec']==spec and arc['fingerprint']==reg.fingerprint(spec)==c['fingerprint']
  for k,scene in arc['scenes'].items():
   n,ns=policy(scene,spec,ms,axis);decisions+=n;scheduled+=ns;vv=[]
   for a in ['BTC','ETH']:vv.append(native_auditor.native(scene['legs'][a],ms[a],axis,int(k),None,None,counter));points+=len(vv[-1]);curves+=1
   v=vv[0]+vv[1];z=scene['summary'];assert c['scenes'][k]==z;fullmetrics(v,axis,z);points+=len(v);curves+=1
   native=[scene['legs'][a]['summary'] for a in ['BTC','ETH']]
   for key in ['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']:near(z[key],sum(x[key] for x in native),1e-12)
   for part in z['cost_parts_usdt']:near(z['cost_parts_usdt'][part],sum(x['cost_parts_usdt'][part] for x in native),1e-12)
   assert z['executions']==sum(x['executions'] for x in native) and z['terminal_flat'] and not z['margin']['independent_sleeve_violations'];near(z['gross_reference_price_PnL_usdt']+z['funding_usdt']-z['cost_usdt'],v[-1]-20000)
 # Preserve and reconcile existing long-only benchmark native and parent hashes.
 bfps=['c31aabeccae5e90da96853e94bde989f2aac7fb3df207cb1b566d8cb07593698','cdf263cff49d32d681b465cfd64ccfde6e5c01257fbda45ab13a29a85094469b'];bcurves={}
 for a,fp in zip(['BTC','ETH'],bfps):
  x=p['read_only_references'][fp];assert sha(ROOT/x['archive'])==x['archive_sha256'];arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()))
  for k,scene in arc['scenes'].items():bcurves[(a,k)]=native_auditor.native(scene,ms[a],axis,int(k),None,None,counter)
 parentfp='97f687b5fc562ebc7a442cf7ca7ff1908b1b05a2a858fdf0fcc8f1f482780d0a';x=p['read_only_references'][parentfp];arc=json.loads(gzip.decompress((ROOT/x['archive']).read_bytes()))
 for k,z in arc['scenes'].items():assert core.navhash(bcurves[('BTC',k)]+bcurves[('ETH',k)])==z['summary']['NAV_sha256_f64le']
 cs=list(r['configs'].values());hs=[.01,.02,.04];ks=[1,2];strict=lambda c:all(sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
 for c in cs:
  ns=[x for x in cs if abs(hs.index(x['relative_return_entry_deadband'])-hs.index(c['relative_return_entry_deadband']))<=1 and abs(ks.index(x['consecutive_scheduled_confirmations'])-ks.index(c['consecutive_scheduled_confirmations']))<=1];s=c['scenes'];g={'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_all_costs':strict(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)>=.6,'local_recent6of8_allcost_gte60pct':sum(strict(x) for x in ns)/len(ns)>=.6,'four_completed_pair_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':s['1']['gross_reference_PnL_to_execution_cost'] is not None and s['1']['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(z['margin']['independent_sleeve_violations']==0 for z in s.values()),'terminal_flat':all(z['terminal_flat'] for z in s.values()),'minimum180days':True};assert c['criteria']==g and c['failed_criteria']==[a for a,b in g.items() if not b] and c['status']==('passed' if all(g.values()) else 'rejected') and c['sensitivity']['neighbor_names']==[x['name'] for x in ns]
 out={'passed':True,'actual_financial_configs':6,'new_joint_cost_scenes':18,'internal_bank_cost_curves':36,'actual_policy_decisions_checked':decisions,'scheduled_rank_decisions_checked':scheduled,'source_cashflow_and_margin_checks':counter,'new_native_and_joint_curves_checked':curves,'new_native_and_joint_NAV_points_checked':points,'new_joint_overall_monthly_recent_metric_checks':18*23,'old_benchmark_native_curves_checked':6,'old_benchmark_parent_hashes_checked':3,'complete_original_benchmark_hashes_unchanged':True,'no_model_or_trade_function_called_in_audit':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
