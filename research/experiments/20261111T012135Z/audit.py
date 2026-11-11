"""Independent Fraction signals, new native LOT/cash/funding/impact and aligned-parent audit."""
import gzip,json,math,statistics
from decimal import Decimal as D,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
from common import *
import market
from audit_native import native
from audit_helpers_complete import near,metrics,verify_recent

plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ms,cm=market.load(plan);vectors,source_scenes,old,arcs,diagnostics=market.recover(plan,ms,cm);counts={k:0 for k in ['funding','fills','rejects','metric_checks','margin_checks']};newnative=oldnative=parents=decisions=0
proxy={'ts':cm['start_ns']+cm['keys']//16,'daily_indices':cm['daily_indices'],'fold_indices':cm['fold_indices']}
def policy(leg,spec,m):
 global decisions
 p=spec['parameters'];entryN=D(str(p['fixed_entry_notional_usdt']));C=D(str(p['initial_capital_usdt']));assert D(leg['state_segments'][0]['cash'])==C and len(leg['decisions'])==370
 for d in leg['decisions']:
  i=d['decision_index'];st=d['state_before'];q=D(st['signed_units']);actual=(q>0)-(q<0);audit=d['policy_audit']
  if p.get('signal_mode')=='constant_long_reference':wanted=1;assert audit=={'kind':'constant_long_reference'}
  elif m['asset']=='BTC':
   ll=int(p['lookback_days']);r=F(m['closes'][i-1])/F(m['closes'][i-1-ll])-1;h=F(str(p['return_hurdle']));e=F(str(p['exit_buffer_fraction']));assert p['lookback_days']==29 and e in [F('.0075'),F('.01'),F('.0125')];wanted=1 if r>h else -1 if r<-h else 1 if actual==1 and r>-e else -1 if actual==-1 and r<e else 0;assert audit=={'kind':'BTC_momentum','return_exact':str(r)}
  else:
   L=int(p['lookback_days']);S=int(p['trend_lookback_days']);lag=int(p['trend_slope_lag_days']);h=F(str(p['return_hurdle']));e=F(str(p['exit_buffer_fraction']));assert L in [4,5,6] and S in [12,16,20] and p['trend_slope_hurdle_fraction'] in [.00625,.0075,.00875] and lag in [1,2,3,4,5] and h in [F('.0175'),F('.02'),F('.0225')] and e in [F('.00625'),F('.0075'),F('.00875')] and e<h and p['trend_estimator']=='finite_normalized_exponentially_weighted_mean_slope' and p['trend_decay_numerator']==S-1 and p['trend_decay_denominator']==S+1 and p['trend_window_days']==S and i-S-lag>=0 and p['trend_gate_scope']=='new_or_reversed_position_only'
   rr=F(m['closes'][i-1])/F(m['closes'][i-1-L])-1;total=F(0);mass=F(0);past=F(0);beta=F(S-1,S+1)
   # Independent oldest-to-newest Horner recursion for both completed windows.
   for j in range(i-S,i):total=F(m['closes'][j])+beta*total;mass=1+beta*mass
   for j in range(i-S-lag,i-lag):past=F(m['closes'][j])+beta*past
   meanclose=total/mass;reference=past/mass;slow=total/past-1
   base=-1 if rr>h else 1 if rr<-h else actual if actual==1 and rr<e or actual==-1 and rr>-e else 0;strength=F(str(p['trend_slope_hurdle_fraction']));gate=1 if slow>strength else -1 if slow<-strength else 0;raw=base if base==actual or base==gate else 0;V=int(p['entry_volatility_window_days']);cap=float(p['entry_volatility_ceiling']);assert V in [6,7,8,10,12] and cap in [.045,.05,.055]
   xs=[math.log(float(m['closes'][j])/float(m['closes'][j-1])) for j in range(i-V,i)];mean=math.fsum(xs)/V;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/(V-1));wanted=0 if raw and raw!=actual and sigma>cap else raw
   pre_funding=wanted;sn=int(m['frame']['available_ts'][i*1440-1]);count=int(p['entry_funding_settlement_count']);assert count in [2,3,4];eligible=[e for e in m['signal_funds'] if sn-36*HOUR<=e['settlement_ts']<=sn-HOUR and e['available_ts']<=sn];selected=list(reversed(sorted(eligible,key=lambda e:e['settlement_ts'])))[:count];assert len(selected)==count;rates=sorted(F(e['realized_rate']) for e in selected);median=rates[count//2] if count%2 else (rates[count//2-1]+rates[count//2])/2;fa=audit['funding_filter'];hours=D(selected[0]['settlement_ts']-m['signal_funds'][selected[0]['source_index']-1]['settlement_ts'])/D(HOUR);assert selected[0]['source_index']>0 and selected[0]['entry_interval_hours']==hours;VW=int(p['entry_funding_budget_volatility_window_days']);assert VW in [8,10,12] and count==4;bx=[math.log(float(m['closes'][j])/float(m['closes'][j-1])) for j in range(i-VW,i)];bm=math.fsum(bx)/VW;independent_sigma=math.sqrt(math.fsum((z-bm)**2 for z in bx)/(VW-1));near(float(fa['budget_sigma_daily']),independent_sigma,1e-12);budget=min(D('.0002'),D(str(p['entry_funding_volatility_ratio']))*D(str(statistics.stdev(bx)))*hours/D(24));fc=F(budget);assert fa['budget_volatility_window_days']==VW and fa['budget_ratio']==str(p['entry_funding_volatility_ratio']) and D(fa['latest_past_interval_hours'])==hours and D(fa['budget_sigma_daily'])==D(str(statistics.stdev(bx)));out=max(F(wanted)*median,F(0));ap=bool(wanted and wanted!=actual);block=ap and out>fc;wanted=0 if block else wanted
   expected_fields=[{'settlement_ts_ns':e['settlement_ts'],'available_ts_ns':e['available_ts'],'realized_rate':str(e['realized_rate']),'source_index':e['source_index']} for e in selected]
   assert audit['raw_desired_before_funding_filter']==pre_funding and fa['applied']==ap and fa['blocked']==block and F(fa['cap_fraction_per_settlement'])==fc and fa['signal_available_ts_ns']==sn and fa['selected_settlements']==expected_fields and fa['settlement_count']==count and F(fa['median_realized_rate'])==median and F(fa['expected_outflow_fraction'])==out and fa['minimum_age_ns']==HOUR and fa['maximum_age_ns']==36*HOUR
   assert audit['ungated_desired']==base and audit['slowgate_direction']==gate and audit['trend_gate_applied']==bool(base and base!=actual) and audit['trend_gate_scope']=='new_or_reversed_position_only'
   assert audit['fast_lookback_days']==L and audit['kind']=='ETH_finite_EWMslope_entry_gate_reversal_entry_vol' and audit['slope_lag_days']==lag and audit['slope_hurdle_fraction']==float(strength) and audit['slow_distance_basis']=='finite_EWM_slope_ratio' and audit['slow_reference_mean_exact']==str(reference) and audit['long_entry_return_hurdle']==float(h) and audit['short_entry_return_hurdle']==float(h) and audit['exit_buffer_fraction']==float(e) and audit['return_exact']==str(rr) and audit['slow_mean_exact']==str(meanclose) and audit['slow_distance_exact']==str(slow) and audit['slow_lookback_days']==S and audit['raw_desired_before_entry_filter']==raw and audit['entry_filter_applied']==bool(raw and raw!=actual) and audit['volatility_window_days']==V and audit['entry_volatility_ceiling']==cap;near(audit['observed_sample_logvol'],sigma,1e-12)

  assert d['desired_direction']==wanted and d['signal_available_ts_ns']<=d['execution_ts_ns']-MIN and D(str(d['fixed_entry_notional_usdt']))==entryN
  trades=[t for t in leg['trades'] if t['decision_index']==i and not t['terminal']];close=[t for t in trades if not t['opening']];op=[t for t in trades if t['opening']];assert len(close)==int(actual!=0 and actual!=wanted)
  if close:assert D(close[0]['change_signed_units'])==-q
  expected=bool(wanted and (not q or actual!=wanted));assert len(op)==int(expected)
  if op:
   lot=D(m['meta']['lot_size']);quantity=(entryN/m['closes'][i-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;assert D(op[0]['change_signed_units'])==quantity*wanted
   if close:assert close[0]['axis_index']<op[0]['axis_index']
  if actual==wanted and actual:assert D(d['state_after']['signed_units'])==q
  assert d['state_after']==(trades[-1]['state_after'] if trades else st);decisions+=1
for fp,arc in arcs.items():
 ref=plan['read_only_references'][fp];m=ms[ref['asset']];spec=json.loads((ROOT/ref['spec']).read_text())
 for k,z in arc['scenes'].items():
  v=native(z,m,m,int(k),None,spec,counts);assert np.array_equal(v[cm['projections'][ref['asset']]],vectors[fp,k]);verify_recent(v,m,source_scenes[fp,k]);oldnative+=1
for c in report['configs'].values():
 arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));spec=arc['spec'];assert reg.fingerprint(spec)==c['fingerprint'] and sha(ROOT/c['archive'])==c['archive_sha256']
 for k,z in arc['scenes'].items():
  if c['scope']=='native':
   m=ms[c['asset']];policy(z,spec,m);v=native(z,m,m,int(k),None,spec,counts);verify_recent(v,m,z['summary']);vectors[c['fingerprint'],k]=v[cm['projections'][c['asset']]];source_scenes[c['fingerprint'],k]=z['summary'];newnative+=1
  else:
   fps=c['source_fingerprints'];assert [x['weight'] for x in spec['components']]==[1,1];v=vectors[fps[0],k]+vectors[fps[1],k];s=z['summary'];assert core.navhash(v)==s['NAV_sha256_f64le'] and v[0]==c['capital_usdt']==sum(source_scenes[fp,k]['initial_capital_usdt'] for fp in fps) and s['daily_equity_usdt']==v[cm['daily_indices']].tolist();metrics(v,s['daily_equity_usdt'],370,s);counts['metric_checks']+=1
   for j,(a,b) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):metrics(v[a:b+1],s['daily_equity_usdt'][j*30:min(j*30+30,370)+1],min(30,370-j*30),s['folds'][j]);counts['metric_checks']+=1
   verify_recent(v,proxy,s)
   for field in ['cost_usdt','funding_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements']:near(s[field],sum(source_scenes[fp,k][field] for fp in fps),1e-12)
   for field in ['fee','half_spread','slippage','impact','tick_rounding']:near(s['cost_parts_usdt'][field],sum(source_scenes[fp,k]['cost_parts_usdt'][field] for fp in fps),1e-12)
   near(v[-1]-v[0],s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],1e-10);assert s['parent_executions']==0 and s['margin']['independent_sleeve_violations']==sum(source_scenes[fp,k]['margin']['violations'] for fp in fps);assert z['source_full_NAV_sha256']==[source_scenes[fp,k]['NAV_sha256_f64le'] for fp in fps] and z['source_common_axis_sha256']==cm['sha256'];vectors[c['fingerprint'],k]=v;parents+=1
  assert c['scenes'][k]==z['summary']
full={**old,**{c['fingerprint']:c for c in report['configs'].values()}}
recentpass=lambda c:all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
for c in report['configs'].values():
 if c['role'].startswith('benchmark'):
  assert c['criteria']=={'benchmark_control_not_strategy_candidate':False} and c['status']=='rejected';continue
 grid=plan['native_grid'] if c['scope']=='native' else plan['grid'];ng=[g for g in grid if abs(plan['slope_lags'].index(g['D'])-plan['slope_lags'].index(c['D']))<=1 and abs(plan['slope_strengths'].index(g['K'])-plan['slope_strengths'].index(c['K']))<=1]
 ns=[full[g['fingerprint']] for g in ng];p=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);q=sum(recentpass(x) for x in ns)/len(ns);near(c['sensitivity']['local_3x_neighbor_positive_fraction'],p);near(c['sensitivity']['local_recent_allcost_qualifying_fraction'],q);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['status']==('passed' if all(c['criteria'].values()) else 'rejected')
for x in report['matched_hold_comparisons']:
 a=full[x['fingerprint']]['scenes'][str(x['cost_multiplier'])];b=report['benchmark_grid'][str(x['N'])]['scenes'][str(x['cost_multiplier'])];near(x['excess_to_hold_pp'],a['net_return_pct']-b['net_return_pct']);assert a['initial_capital_usdt']==b['initial_capital_usdt']
assert newnative==24 and parents==24 and oldnative==18 and decisions==8880
put(R/'verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_native_curves':newnative,'new_parent_curves':parents,'new_NAV_points':sum(s['NAV_points'] for c in report['configs'].values() for s in c['scenes'].values()),'read_only_native_curves':oldnative,'read_only_parent_hashes':3*sum(x['scope']=='parent' for x in plan['read_only_references'].values()),'independent_new_policy_decisions':decisions,'counts':counts,'new_native_size_LOT_impact_capital_verified':True,'parent_no_linear_NAV_scaling':True,'matched_hold_comparisons_checked':len(report['matched_hold_comparisons']),'old_statuses_and_report_bytes_unchanged':True,'scope':'Independent Fraction originaloldledger/newparentVW/R; Decimal nativecash/fee/volumeimpact/fund/hourrisk replay; aligned whole/month/recent parent metrics and frozen sensitivity. Auditusesno source/new simulate,decideortrade calls.'});print(json.dumps({'passed':True,'new_native_curves':newnative,'new_parent_curves':parents,'old_native_curves':oldnative,'policy_decisions':decisions,**counts}),flush=True)
