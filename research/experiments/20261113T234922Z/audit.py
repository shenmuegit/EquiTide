"""Independent saved native cash/LOT/cost/funding/signals, aligned parent and fixed gates audit."""
import gzip,json,math,statistics,copy
from decimal import Decimal as D,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
from common import *
import market
from audit_native import native
from audit_helpers_complete import near,metrics,verify_recent
plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ms,cm=market.load(plan);vectors={};source_scenes={};counts={k:0 for k in ['funding','fills','rejects','metric_checks','margin_checks']};newnative=parents=decisions=0
proxy={'ts':cm['start_ns']+cm['keys']//16,'daily_indices':cm['daily_indices'],'fold_indices':cm['fold_indices']}
def policy(leg,spec,m):
 global decisions
 p=spec['parameters'];entryN=D(str(p['fixed_entry_notional_usdt']));C=D(str(p['initial_capital_usdt']));assert D(leg['state_segments'][0]['cash'])==C and len(leg['decisions'])==390
 for d in leg['decisions']:
  i=d['decision_index'];st=d['state_before'];q=D(st['signed_units']);actual=(q>0)-(q<0);audit=d['policy_audit']
  if p.get('signal_mode')=='constant_long_reference':wanted=1;assert audit=={'kind':'constant_long_reference'}
  elif m['asset']=='BTC':
   L=int(p['lookback_days']);h=F(str(p['return_hurdle']));r=F(m['closes'][i-1])/F(m['closes'][i-1-L])-1;assert L in [28,29,30] and h in [F('.025'),F('.03'),F('.035')] and p['exit_buffer_fraction'] in [.005,.01,.015];e=F(str(p['exit_buffer_fraction']));raw=1 if r>h else -1 if r<-h else 1 if actual==1 and r>-e else -1 if actual==-1 and r<e else 0
   V=int(p['entry_volatility_window_days']);cap=float(p['entry_volatility_ceiling']);assert V in [6,10,14] and cap in [.03,.04,.05] and p['entry_volatility_gate_scope']=='new_or_reversed_position_only';xs=[math.log(float(m['closes'][j])/float(m['closes'][j-1])) for j in range(i-V,i)];mean=math.fsum(xs)/V;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));wanted=0 if raw and raw!=actual and sigma>cap else raw
   assert audit['kind']=='BTC_momentum_entry_vol' and audit['return_exact']==str(r) and audit['raw_desired_before_entry_filter']==raw and audit['entry_filter_applied']==bool(raw and raw!=actual) and audit['volatility_window_days']==V and audit['entry_volatility_ceiling']==cap and audit['entry_volatility_gate_scope']=='new_or_reversed_position_only';near(audit['observed_sample_logvol'],sigma,1e-12)

  else:
   L=int(p['lookback_days']);S=int(p['trend_lookback_days']);lag=int(p['trend_slope_lag_days']);h=F(str(p['return_hurdle']));e=F(str(p['exit_buffer_fraction']));assert L in [4,5,6] and S in [12,16,20] and p['trend_slope_hurdle_fraction'] in [.00625,.0075,.00875] and lag in [1,2,3,4,5] and h in [F('.0175'),F('.019'),F('.02'),F('.021'),F('.0225')] and e in [F('.00625'),F('.0075'),F('.00875')] and e<h and p['trend_estimator']=='finite_normalized_exponentially_weighted_mean_slope' and p['trend_decay_numerator']==S-1 and p['trend_decay_denominator']==S+1 and p['trend_window_days']==S and i-S-lag>=0 and p['trend_gate_scope']=='new_or_reversed_position_only'
   rr=F(m['closes'][i-1])/F(m['closes'][i-1-L])-1;total=F(0);mass=F(0);past=F(0);beta=F(S-1,S+1)
   # Independent oldest-to-newest Horner recursion for both completed windows.
   for j in range(i-S,i):total=F(m['closes'][j])+beta*total;mass=1+beta*mass
   for j in range(i-S-lag,i-lag):past=F(m['closes'][j])+beta*past
   meanclose=total/mass;reference=past/mass;slow=total/past-1
   base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;strength=F(str(p['trend_slope_hurdle_fraction']));gate=1 if slow>strength else -1 if slow<-strength else 0;raw=base if base==actual or base==gate else 0;V=int(p['entry_volatility_window_days']);cap=float(p['entry_volatility_ceiling']);assert V in [5,6,7,8,10,12] and cap in [.045,.05,.0525,.055,.05625,.0575,.06]
   xs=[math.log(float(m['closes'][j])/float(m['closes'][j-1])) for j in range(i-V,i)];mean=math.fsum(xs)/V;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));wanted=0 if raw and raw!=actual and sigma>cap else raw
   pre_funding=wanted;sn=int(m['frame']['available_ts'][i*1440-1]);count=int(p['entry_funding_settlement_count']);assert count in [2,3,4];eligible=[e for e in m['signal_funds'] if sn-36*HOUR<=e['settlement_ts']<=sn-HOUR and e['available_ts']<=sn];selected=list(reversed(sorted(eligible,key=lambda e:e['settlement_ts'])))[:count];assert len(selected)==count;rates=sorted(F(e['realized_rate']) for e in selected);median=rates[count//2] if count%2 else (rates[count//2-1]+rates[count//2])/2;fa=audit['funding_filter'];hours=D(selected[0]['settlement_ts']-m['signal_funds'][selected[0]['source_index']-1]['settlement_ts'])/D(HOUR);assert selected[0]['source_index']>0 and selected[0]['entry_interval_hours']==hours;VW=int(p['entry_funding_budget_volatility_window_days']);assert VW in [8,10,12] and count in [2,3,4];bx=[math.log(float(m['closes'][j])/float(m['closes'][j-1])) for j in range(i-VW,i)];bm=math.fsum(bx)/VW;independent_sigma=math.sqrt(math.fsum((z-bm)**2 for z in bx)/(VW-1));near(float(fa['budget_sigma_daily']),independent_sigma,1e-12);budget=min(D('.0002'),D(str(p['entry_funding_volatility_ratio']))*D(str(statistics.stdev(bx)))*hours/D(24));fc=F(budget);assert fa['budget_volatility_window_days']==VW and fa['budget_ratio']==str(p['entry_funding_volatility_ratio']) and D(fa['latest_past_interval_hours'])==hours and D(fa['budget_sigma_daily'])==D(str(statistics.stdev(bx)));out=max(F(wanted)*median,F(0));ap=bool(wanted and wanted!=actual);block=ap and out>fc;wanted=0 if block else wanted
   expected_fields=[{'settlement_ts_ns':e['settlement_ts'],'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'source_index':e['source_index']} for e in selected]
   assert audit['raw_desired_before_funding_filter']==pre_funding and fa['applied']==ap and fa['blocked']==block and F(fa['cap_fraction_per_settlement'])==fc and fa['signal_available_ts_ns']==sn and fa['selected_settlements']==expected_fields and fa['settlement_count']==count and F(fa['median_realized_rate'])==median and F(fa['expected_outflow_fraction'])==out and fa['minimum_age_ns']==HOUR and fa['maximum_age_ns']==36*HOUR
   assert audit['ungated_desired']==base and audit['slowgate_direction']==gate and audit['trend_gate_applied']==bool(base and base!=actual) and audit['trend_gate_scope']=='new_or_reversed_position_only'
   assert audit['fast_lookback_days']==L and audit['kind']=='ETH_finite_EWMslope_entry_gate_reversal_entry_vol' and audit['slope_lag_days']==lag and audit['slope_hurdle_fraction']==float(strength) and audit['slow_distance_basis']=='finite_EWM_slope_ratio' and audit['slow_reference_mean_exact']==str(reference) and audit['long_entry_return_hurdle']==float(h) and audit['short_entry_return_hurdle']==float(h) and audit['exit_buffer_fraction']==float(e) and audit['return_exact']==str(rr) and audit['slow_mean_exact']==str(meanclose) and audit['slow_distance_exact']==str(slow) and audit['slow_lookback_days']==S and audit['raw_desired_before_entry_filter']==raw and audit['entry_filter_applied']==bool(raw and raw!=actual) and audit['volatility_window_days']==V and audit['entry_volatility_ceiling']==cap;near(audit['observed_sample_logvol'],sigma,1e-12)

  if p.get('entry_direction_mode')=='long_only':
   assert audit['raw_desired_before_side_filter']==wanted and audit['allowed_direction']=='long_only';wanted=wanted if wanted>0 else 0
  if 'entry_premium_window_days' in p:
   W=int(p['entry_premium_window_days']);cap=F(str(p['entry_premium_maximum_directional_fraction']));rows=m['premium_rows'][i-W:i];assert len(rows)==W and all((z[6]+1)*1000000<=d['signal_available_ts_ns'] for z in rows);values=sorted(F(z[4]) for z in reversed(rows));median=values[(len(values)-1)//2];richness=F(0) if wanted*median<=0 else wanted*median;applied=bool(wanted and wanted!=actual);blocked=applied and richness>cap;fa=audit['premium_filter'];assert audit['raw_desired_before_premium_filter']==wanted and fa['applied']==applied and fa['blocked']==blocked and F(fa['median_premium_exact'])==median and F(fa['directional_richness_exact'])==richness and fa['source_close_values']==[z[4] for z in rows] and fa['source_close_available_ns']==[(z[6]+1)*1000000 for z in rows] and fa['row_range']==[i-W,i] and fa['window_days']==W and F(fa['maximum_directional_premium'])==cap;wanted=0 if blocked else wanted
  assert d['desired_direction']==wanted and d['signal_available_ts_ns']<=d['execution_ts_ns']-MIN and D(str(d['fixed_entry_notional_usdt']))==entryN
  trades=[t for t in leg['trades'] if t['decision_index']==i and not t['terminal']];close=[t for t in trades if not t['opening']];op=[t for t in trades if t['opening']];assert len(close)==int(actual!=0 and actual!=wanted)
  if close:assert D(close[0]['change_signed_units'])==-q
  expected=bool(wanted and (not q or actual!=wanted));assert len(op)==int(expected)
  if op:
   lot=D(m['meta']['lot_size']);quantity=(entryN/m['closes'][i-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;assert D(op[0]['change_signed_units'])==quantity*wanted
   if close:assert close[0]['axis_index']<op[0]['axis_index']
  if actual==wanted and actual:assert D(d['state_after']['signed_units'])==q
  assert d['state_after']==(trades[-1]['state_after'] if trades else st);decisions+=1

def verify_extension(v,m,z):
 ix=m['daily_indices'];daily=v[ix].tolist();s=z['extension20'];a=int(ix[370]);assert len(daily)==391 and s['daily_equity_usdt']==daily[370:] and s['NAV_sha256_f64le']==core.navhash(v[a:]) and s['initial_NAV_usdt']==v[a] and s['final_NAV_usdt']==v[-1];metrics(v[a:],daily[370:],20,s)
 for f,lo,hi in zip(s['folds'],[370,375,380,385],[375,380,385,390]):
  aa,bb=ix[[lo,hi]];assert f['duration_days']==hi-lo and f['start_utc']==core.stamp(int(m['ts'][aa])) and f['end_exclusive_utc']==core.stamp(int(m['ts'][bb]));metrics(v[aa:bb+1],daily[lo:hi+1],hi-lo,f)
 assert len(s['folds'])==4 and abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/v[a])<1e-12

readonly_curves=0
for fp,ref in plan['read_only_references'].items():
 if ref['scope']!='native':continue
 arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));m=ms[ref['asset']]
 for k,z in arc['scenes'].items():
  policy(z,arc['spec'],m);v=native(z,m,m,int(k),None,arc['spec'],counts);verify_recent(v,m,z['summary']);verify_extension(v,m,z['summary']);vectors[fp,k]=v[cm['projections'][ref['asset']]];source_scenes[fp,k]=z['summary'];readonly_curves+=1
readonly_decisions=decisions;decisions=0
for c in report['configs'].values():
 arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));sp=arc['spec'];assert reg.fingerprint(sp)==c['fingerprint'] and sha(ROOT/c['archive'])==c['archive_sha256']
 for k,z in arc['scenes'].items():
  if c['scope']=='native':
   m=ms[c['asset']];policy(z,sp,m);v=native(z,m,m,int(k),None,sp,counts);verify_recent(v,m,z['summary']);verify_extension(v,m,z['summary']);vectors[c['fingerprint'],k]=v[cm['projections'][c['asset']]];source_scenes[c['fingerprint'],k]=z['summary'];newnative+=1
  else:
   fps=c['source_fingerprints'];v=vectors[fps[0],k]+vectors[fps[1],k];s=z['summary'];assert v[0]==18750 and s['NAV_sha256_f64le']==core.navhash(v) and s['daily_equity_usdt']==v[cm['daily_indices']].tolist();metrics(v,s['daily_equity_usdt'],390,s);counts['metric_checks']+=1
   for j,(aa,bb) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):metrics(v[aa:bb+1],s['daily_equity_usdt'][j*30:min(j*30+30,390)+1],min(30,390-j*30),s['folds'][j]);counts['metric_checks']+=1
   verify_recent(v,proxy,s);verify_extension(v,proxy,s)
   for field in ['cost_usdt','funding_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','funding_settlements']:near(s[field],sum(source_scenes[f,k][field] for f in fps),1e-12)
   for field in ['fee','half_spread','slippage','impact','tick_rounding']:near(s['cost_parts_usdt'][field],sum(source_scenes[f,k]['cost_parts_usdt'][field] for f in fps),1e-12)
   assert [x['weight'] for x in sp['components']]==[1,1] and z['source_full_NAV_sha256']==[source_scenes[f,k]['NAV_sha256_f64le'] for f in fps] and z['source_common_axis_sha256']==cm['sha256'] and s['parent_executions']==0;near(v[-1]-v[0],s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt']);parents+=1
  assert c['scenes'][k]==z['summary']
full={c['fingerprint']:c for c in report['configs'].values()}
for rows in [plan['grid'],plan['native_grid']]:
 for g in rows:
  if g['readonly']:
   d=plan['read_only_references'][g['fingerprint']];c=copy.deepcopy(next(c for c in json.loads((ROOT/d['report']).read_text())['configs'].values() if c['fingerprint']==g['fingerprint']));c.update(W=g['W'],K=g['K'],readonly=True);full[g['fingerprint']]=c
recent_ok=lambda c:all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
for c in report['configs'].values():
 if c['role']=='benchmark':ns=[c];dims=0
 else:
  rows=plan['grid'] if c['scope']=='parent' else plan['native_grid'];ns=[full[g['fingerprint']] for g in rows if abs(plan['axes']['BTC_VOL_CAP'].index(g['W'])-plan['axes']['BTC_VOL_CAP'].index(c['W']))<=1 and abs(plan['axes']['ETH_FUND_R'].index(g['K'])-plan['axes']['ETH_FUND_R'].index(c['K']))<=1];dims=2
  if c['scope']=='native':ns=[full[g['fingerprint']] for g in rows if g['asset']==c['asset']];dims=1

 pos=sum(z['scenes']['3']['net_return_pct']>0 for z in ns)/len(ns);rob=sum(recent_ok(z) for z in ns)/len(ns);assert c['sensitivity']['dimension_count']==dims and c['sensitivity']['neighbor_names']==[z['name'] for z in ns];near(c['sensitivity']['local_3x_neighbor_positive_fraction'],pos);near(c['sensitivity']['local_recent_allcost_qualifying_fraction'],rob)
 ss=list(c['scenes'].values());one,three=c['scenes']['1'],c['scenes']['3'];ratio=(one['gross_reference_price_PnL_usdt']+one['funding_usdt'])/one['cost_usdt'] if one['cost_usdt'] else None
 if ratio is not None:near(one['gross_reference_PnL_to_execution_cost'],ratio)
 else:assert one['gross_reference_PnL_to_execution_cost'] is None and one['executions']==0
 expected={'positive_all_costs':all(z['net_return_pct']>0 for z in ss),'ten_of_thirteen_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in one['folds'])>=10,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss),'recent40_six_of_eight_positive5d_all_costs':recent_ok(c),'composite_DD3_lte25pct':three['max_drawdown_pct']<=25,'local_positive3_gte60pct':pos>=.6,'local_recent6of8_allcost_gte60pct':rob>=.6,'four_underlying_native_closes1':one['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_native_collateral':all(z['cash_or_units_violations']==0 for z in ss),'no_native_order_rejections':all(z['rejected_orders']==0 for z in ss),'no_native_margin_proxy_violations':all(z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'))==0 for z in ss),'native_terminal_flat':all(D(z['terminal_units'])==0 for z in ss),'minimum180days':True,'extension20_positive_all_costs':all(z['extension20']['net_return_pct']>0 for z in ss),'extension20_three_of_four_positive_folds_all_costs':all(sum(f['net_return_pct']>0 for f in z['extension20']['folds'])>=3 for z in ss)}
 assert c['criteria']==expected and c['status']==('passed' if all(expected.values()) else 'rejected') and c['failed_criteria']==[k for k,v in expected.items() if not v]
assert (newnative,parents,decisions,readonly_curves)==(18,15,7020,0)
rs=reg.read_records(ROOT/'research/automation/registry.jsonl')
for fp,z in plan['read_only_references'].items():assert rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
put(R/'verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_native_curves':newnative,'new_parent_curves':parents,'read_only_native_curves':readonly_curves,'independent_new_policy_decisions':decisions,'readonly_policy_decisions':readonly_decisions,'counts':counts,'all389days_cash_quantity_funding_costs_hourrisk_fullNAV_checked':True,'extension20_inherited_not_reset':True,'all_old_statuses_and_reports_unchanged':True,'two_axis_sensitivity_and_all_gates_independently_recomputed':True});print(json.dumps({'passed':True,'native':newnative,'parents':parents,'policy_decisions':decisions,'readonlycurves':readonly_curves,**counts}),flush=True)
