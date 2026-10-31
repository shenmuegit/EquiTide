"""Independent Fraction signals, new native LOT/cash/funding/impact and aligned-parent audit."""
import gzip,json,math
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
 p=spec['parameters'];N=D(str(p['fixed_entry_notional_usdt']));C=D(str(p['initial_capital_usdt']));assert D(leg['state_segments'][0]['cash'])==C and len(leg['decisions'])==370
 for d in leg['decisions']:
  i=d['decision_index'];st=d['state_before'];q=D(st['signed_units']);actual=(q>0)-(q<0);audit=d['policy_audit']
  if p.get('signal_mode')=='constant_long_reference':wanted=1;assert audit=={'kind':'constant_long_reference'}
  elif m['asset']=='BTC':
   r=F(m['closes'][i-1])/F(m['closes'][i-32])-1;h=F('.04');e=F('.01');wanted=1 if r>h else -1 if r<-h else 1 if actual==1 and r>-e else -1 if actual==-1 and r<e else 0;assert audit=={'kind':'BTC_momentum','return_exact':str(r)}
  else:
   r=F(m['closes'][i-1])/F(m['closes'][i-1-int(p['lookback_days'])])-1;slow=F(m['closes'][i-1])/F(m['closes'][i-29])-1;h=F(str(p['return_hurdle']));base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<0 or actual==-1 and r>0 else 0;gate=(slow>0)-(slow<0);wanted=base if base==gate else 0;assert audit=={'kind':'ETH_gated_reversal','return_exact':str(r),'slow_return_exact':str(slow)}
  assert d['desired_direction']==wanted and d['signal_available_ts_ns']<=d['execution_ts_ns']-MIN and D(str(d['fixed_entry_notional_usdt']))==N
  trades=[t for t in leg['trades'] if t['decision_index']==i and not t['terminal']];close=[t for t in trades if not t['opening']];op=[t for t in trades if t['opening']];assert len(close)==int(actual!=0 and actual!=wanted)
  if close:assert D(close[0]['change_signed_units'])==-q
  expected=bool(wanted and (not q or actual!=wanted));assert len(op)==int(expected)
  if op:
   lot=D(m['meta']['lot_size']);quantity=(N/m['closes'][i-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;assert D(op[0]['change_signed_units'])==quantity*wanted
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
   near(v[-1]-v[0],s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],1e-10);assert s['parent_executions']==0 and s['margin']['independent_sleeve_violations']==sum(source_scenes[fp,k]['margin']['violations'] for fp in fps);assert z['source_full_NAV_sha256']==[source_scenes[fp,k]['NAV_sha256_f64le'] for fp in fps];vectors[c['fingerprint'],k]=v;parents+=1
  assert c['scenes'][k]==z['summary']
full={**old,**{c['fingerprint']:c for c in report['configs'].values()}}
recentpass=lambda c:all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
for c in report['configs'].values():
 grid=plan['native_grid'] if c['scope']=='native' else plan['grid'];ng=[g for g in grid if abs(plan['lookbacks'].index(g['L'])-plan['lookbacks'].index(c['L']))<=1 and abs(plan['hurdles'].index(g['H'])-plan['hurdles'].index(c['H']))<=1]
 ns=[full[g['fingerprint']] for g in ng];p=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);q=sum(recentpass(x) for x in ns)/len(ns);near(c['sensitivity']['local_3x_neighbor_positive_fraction'],p);near(c['sensitivity']['local_recent_allcost_qualifying_fraction'],q);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['status']==('passed' if all(c['criteria'].values()) else 'rejected')
for x in report['matched_hold_comparisons']:
 a=full[x['fingerprint']]['scenes'][str(x['cost_multiplier'])];b=old[plan['benchmark_parent_fingerprint']]['scenes'][str(x['cost_multiplier'])];near(x['excess_to_hold_pp'],a['net_return_pct']-b['net_return_pct']);assert a['initial_capital_usdt']==b['initial_capital_usdt']==20000
assert newnative==6 and parents==6 and oldnative==51 and decisions==2220
put(R/'verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_native_curves':newnative,'new_parent_curves':parents,'new_NAV_points':(newnative+parents)*len(cm['keys']),'read_only_native_curves':oldnative,'read_only_parent_hashes':3*sum(x['scope']=='parent' for x in plan['read_only_references'].values()),'independent_new_policy_decisions':decisions,'counts':counts,'new_native_size_LOT_impact_capital_verified':True,'parent_no_linear_NAV_scaling':True,'matched_hold_comparisons_checked':len(report['matched_hold_comparisons']),'old_statuses_and_report_bytes_unchanged':True,'scope':'Independent Fraction originalpolicies/actualnewN LOT sizing; Decimal nativecash/fee/volumeimpact/fund/hourrisk replay; aligned whole/month/recent parent metrics and frozen sensitivity. No source/new simulate, decide or trade calls.'});print(json.dumps({'passed':True,'new_native_curves':newnative,'new_parent_curves':parents,'old_native_curves':oldnative,'policy_decisions':decisions,**counts}),flush=True)
