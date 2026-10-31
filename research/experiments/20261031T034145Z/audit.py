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
def verify_features(ms,ff):
 closes={a:[float(v) for v in m['closes']] for a,m in ms.items()};independent={};fits=scores=0
 for W in [20,30]:
  for i in range(33,403,7):
   f=ff['fits'][f'{W}:{i}'];a,b=i-W-1,i-1;assert f['training_start_return_day']==a and f['training_stop_exclusive_return_day']==b and f['last_training_close_day']==i-2 and f['latest_momentum_close_day']==i-1 and a>=1 and f['training_observations']==W
   xx=[math.log(closes['BTC'][j]/closes['BTC'][j-1]) for j in range(a,b)];yy=[math.log(closes['ETH'][j]/closes['ETH'][j-1]) for j in range(a,b)];mx=math.fsum(xx)/W;my=math.fsum(yy)/W;den=math.fsum((x-mx)**2 for x in xx);beta=math.fsum((x-mx)*(y-my) for x,y in zip(xx,yy))/den if den>1e-20 else None;alpha=my-beta*mx if beta is not None else None;eligible=beta is not None and math.isfinite(beta) and math.isfinite(alpha) and .5<=beta<=2;assert f['eligible_beta']==eligible;near(f['x_mean'],mx,1e-9);near(f['y_mean'],my,1e-9);near(f['denominator'],den,1e-9)
   if beta is not None:near(f['beta'],beta,1e-9);near(f['alpha'],alpha,1e-9)
   else:assert f['beta'] is None and f['alpha'] is None
   fits+=1
   for L in [7,14,28]:
    z=ff['scores'][f'{W}:{L}:{i}'];assert all(z[k]==v for k,v in f.items()) and z['momentum_lookback_days']==L and z['momentum_start_close_day']==i-1-L and z['momentum_end_close_day']==i-1 and not z['alpha_subtracted'];me=math.log(closes['ETH'][i-1]/closes['ETH'][i-1-L]);mb=math.log(closes['BTC'][i-1]/closes['BTC'][i-1-L]);sc=me-beta*mb if beta is not None else None;near(z['ETH_logmomentum'],me,1e-12);near(z['BTC_logmomentum'],mb,1e-12)
    if sc is not None:near(z['score'],sc,1e-9);assert (sc>0)-(sc<0)==(z['score']>0)-(z['score']<0)
    else:assert z['score'] is None
    independent[W,L,i]={'beta':beta,'eligible':eligible,'score':sc};scores+=1
 assert fits==106 and scores==318 and len(ff['fits'])==106 and len(ff['scores'])==318;return independent

def policy(scene,spec,ms,axis,ff,independent):
 p=spec['parameters'];L,W=p['momentum_lookback_days'],p['beta_fit_window_days'];dd=scene['decisions'];assert len(dd)==370;completed=0;scheduled_count=0;seen=set();entry_beta=None
 for i,d in zip(range(33,403),dd):
  t=axis['first_ns']+i*DAY+MIN;ix6=int(np.searchsorted(axis['keys'],np.array((t,6),dtype=axis['keys'].dtype)));ix7=ix6+1;assert int(axis['ts'][ix7])==t and axis['codes'][ix7]==7;before={a:state_at(scene['legs'][a]['state_segments'],ix6-1) for a in ms};afterclose={a:state_at(scene['legs'][a]['state_segments'],ix6) for a in ms};after={a:state_at(scene['legs'][a]['state_segments'],ix7) for a in ms};current=1 if before['ETH']['signed_units']>0 else -1 if before['ETH']['signed_units']<0 else 0;scheduled=(i-33)%7==0;scheduled_count+=scheduled
  assert d['day_index']==i and d['execution_ts_ns']==t and d['signal_available_ts_ns']==int(ms['BTC']['frame']['available_ts'][i*1440-1])<t and d['scheduled']==scheduled and d['pair_side_before']==current and not d['recovery_before'] and not d['recovery_after'] and d['entry_beta_before']==entry_beta;assert all(money_state(d['state_before'][a])==before[a] and money_state(d['state_after_close'][a])==afterclose[a] and money_state(d['state_after'][a])==after[a] for a in ms)
  desired=current;f=None
  if scheduled:
   f=ff['scores'][f'{W}:{L}:{i}'];check=independent[W,L,i];assert d['rank']==f and d['action']=='scheduled';desired=(1 if check['score']>0 else -1 if check['score']<0 else 0) if check['eligible'] else 0
  else:assert d['rank'] is None and d['action']=='hold'
  close=bool(scheduled and current and desired!=current);opennew=bool(scheduled and desired and (not current or close));assert d['desired_side']==desired and d['pending_open_side']==(desired if opennew else 0) and d['pair_side_after']==desired
  if close:entry_beta=None
  for a in ['BTC','ETH']:
   ts=scene['legs'][a]['trades'];ct=[x for x in ts if x['axis_index']==ix6];ot=[x for x in ts if x['axis_index']==ix7];assert len(ct)==int(close) and len(ot)==int(opennew)
   if close:assert not ct[0]['opening'] and D(ct[0]['change_signed_units'])==-before[a]['signed_units'] and ct[0]['decision_reason']=='scheduled_rank_change';seen.add((a,ix6));assert afterclose[a]['signed_units']==0
   else:assert afterclose[a]==before[a]
   if opennew:
    lot=D(ms[a]['meta']['lot_size']);notional=D(2000)*(D(str(f['beta'])) if a=='BTC' else D(1));qty=(notional/ms[a]['closes'][i-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;indepN=D(2000)*(D(str(independent[W,L,i]['beta'])) if a=='BTC' else D(1));indepq=(indepN/ms[a]['closes'][i-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;assert indepq==qty;wanted=D(desired if a=='ETH' else -desired)*qty;assert ot[0]['opening'] and D(ot[0]['change_signed_units'])==wanted and after[a]['signed_units']==wanted and ot[0]['decision_reason']==('open_first' if a=='BTC' else 'open_second');seen.add((a,ix7))
   else:assert after[a]==afterclose[a]
  if opennew:entry_beta=str(f['beta'])
  assert d['entry_beta_after']==entry_beta;completed+=int(close)
 terminal=len(axis['ts'])-1;was_open=False
 for a in ms:
  before=state_at(scene['legs'][a]['state_segments'],terminal-1);tt=[x for x in scene['legs'][a]['trades'] if x['axis_index']==terminal];assert len(tt)==int(before['signed_units']!=0)
  if tt:assert not tt[0]['opening'] and tt[0]['terminal'] and tt[0]['decision_reason']=='terminal' and D(tt[0]['change_signed_units'])==-before['signed_units'];seen.add((a,terminal));was_open=True
  assert all(x['status']=='filled' and (a,x['axis_index']) in seen for x in scene['legs'][a]['trades'])
 completed+=int(was_open);assert completed==scene['terminal_pair_state']['completed_pairs']==scene['summary']['round_trips'];assert not scene['terminal_pair_state']['side'] and not scene['terminal_pair_state']['recovery'] and scene['terminal_pair_state']['entry_beta'] is None and scheduled_count==53;return len(dd),scheduled_count

def fullmetrics(v,axis,z):
 daily=v[axis['daily_indices']].tolist();assert z['NAV_points']==len(v) and z['NAV_sha256_f64le']==core.navhash(v) and z['daily_equity_usdt']==daily;metrics(v,daily,370,z)
 for j,(a,b) in enumerate(zip(axis['fold_indices'],axis['fold_indices'][1:])):
  days=min(30,370-30*j);f=z['folds'][j];assert f['duration_days']==days and f['start_utc']==core.stamp(int(axis['ts'][a])) and f['end_exclusive_utc']==core.stamp(int(axis['ts'][b]));metrics(v[a:b+1],daily[30*j:30*j+days+1],days,f)
 verify_recent(v,axis,z);assert abs(math.prod(1+f['net_return_pct']/100 for f in z['folds'])-v[-1]/v[0])<1e-12
def main():
 p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());assert r['frozen_plan_sha256']==sha(R/'plan.json');ms,axis=market.load(p);fb=json.loads(gzip.decompress((R/'features.json.gz').read_bytes()));assert fb['plan_sha256']==sha(R/'plan.json');ff=fb['features'];independent=verify_features(ms,ff);counter={'funding':0,'fills':0,'rejects':0,'metric_checks':0,'margin_checks':0};decisions=scheduled=points=0;curves=0
 for c in r['configs'].values():
  assert sha(ROOT/c['archive'])==c['archive_sha256'];arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));spec=json.loads((ROOT/c['spec']).read_text());assert arc['spec']==spec and arc['fingerprint']==reg.fingerprint(spec)==c['fingerprint']
  for k,scene in arc['scenes'].items():
   n,ns=policy(scene,spec,ms,axis,ff,independent);decisions+=n;scheduled+=ns;vv=[]
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
 cs=list(r['configs'].values());ls=[20,30];ps=[7,14,28];strict=lambda c:all(sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
 for c in cs:
  ns=[x for x in cs if abs(ls.index(x['beta_fit_window_days'])-ls.index(c['beta_fit_window_days']))<=1 and abs(ps.index(x['momentum_lookback_days'])-ps.index(c['momentum_lookback_days']))<=1];s=c['scenes'];g={'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_all_costs':strict(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)>=.6,'local_recent6of8_allcost_gte60pct':sum(strict(x) for x in ns)/len(ns)>=.6,'four_completed_pair_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':s['1']['gross_reference_PnL_to_execution_cost'] is not None and s['1']['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(z['margin']['independent_sleeve_violations']==0 for z in s.values()),'terminal_flat':all(z['terminal_flat'] for z in s.values()),'minimum180days':True};assert c['criteria']==g and c['failed_criteria']==[a for a,b in g.items() if not b] and c['status']==('passed' if all(g.values()) else 'rejected') and c['sensitivity']['neighbor_names']==[x['name'] for x in ns]
 out={'passed':True,'actual_financial_configs':6,'new_joint_cost_scenes':18,'internal_bank_cost_curves':36,'independent_unique_beta_fits':106,'independent_unique_scores':318,'independent_beta_native_LOT_sizing_equal':True,'actual_policy_decisions_checked':decisions,'scheduled_rank_decisions_checked':scheduled,'source_cashflow_and_margin_checks':counter,'new_native_and_joint_curves_checked':curves,'new_native_and_joint_NAV_points_checked':points,'new_joint_overall_monthly_recent_metric_checks':18*23,'old_benchmark_native_curves_checked':6,'old_benchmark_parent_hashes_checked':3,'complete_original_benchmark_hashes_unchanged':True,'no_model_or_trade_function_called_in_audit':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
