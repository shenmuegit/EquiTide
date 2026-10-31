"""Independent exact ROC policy, cashflow, costs, funding, margin and complete curve audit."""
import copy,gzip,json,math
from decimal import Decimal as D,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
from common import *
from run import load,recover,grid_axes,recent_ok
from audit_native import native
from audit_helpers_complete import metrics,near,verify_recent

plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ms,cm=load(plan);vectors,_,old=recover(plan,ms,cm);counts={k:0 for k in ['funding','fills','rejects','metric_checks','margin_checks']};decisions=0;curves=0
def policy(leg,spec,m):
 global decisions
 p=spec['parameters'];S=p['trend_lookback_days'];H=F(str(p['return_hurdle']));values=m['signal_closes'];assert len(leg['decisions'])==370
 for d in leg['decisions']:
  i=d['decision_index'];st=d['state_before'];q=D(st['signed_units']);actual=(q>0)-(q<0);r=F(values[i-1])/F(values[i-4])-1;slow=F(values[i-1])/F(values[i-1-S])-1;fresh=-1 if r>H else 1 if r<-H else actual if actual==1 and r<0 or actual==-1 and r>0 else 0;gate=(slow>0)-(slow<0);wanted=fresh if fresh==gate else 0
  assert d['lookback_return_exact']==str(r) and d['trend_return_exact']==str(slow) and d['desired_direction']==wanted and d['signal_available_ts_ns']<=d['execution_ts_ns']-MIN
  trades=[t for t in leg['trades'] if not t['terminal'] and t['decision_index']==i];close=[t for t in trades if not t['opening']];op=[t for t in trades if t['opening']]
  assert len(close)==int(actual!=0 and actual!=wanted)
  if close:assert D(close[0]['change_signed_units'])==-q and close[0]['axis_index']<next((x['axis_index'] for x in op),10**9)
  expectedopen=bool(wanted and (not q or actual!=wanted));assert len(op)==int(expectedopen)
  if op:
   lot=D(m['meta']['lot_size']);quantity=(D(3000)/m['closes'][i-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;assert D(op[0]['change_signed_units'])==quantity*wanted
  if actual==wanted and actual:assert D(d['state_after']['signed_units'])==q
  assert d['state_after']==(trades[-1]['state_after'] if trades else st);decisions+=1

for fp,ref in plan['read_only_references'].items():
 if ref['scope']!='native':continue
 arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));m=ms[ref['asset']]
 for k,z in arc['scenes'].items():
  v=native(z,m,m,int(k),None,None,counts);assert np.array_equal(v[cm['projections'][ref['asset']]],vectors[fp,k]);curves+=1
for c in report['configs'].values():
 arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));spec=arc['spec'];assert sha(ROOT/c['archive'])==c['archive_sha256'] and reg.fingerprint(spec)==c['fingerprint']
 for k,z in arc['scenes'].items():
  if c['scope']=='native':
   m=ms['ETH'];policy(z,spec,m);v=native(z,m,m,int(k),None,None,counts);verify_recent(v,m,z['summary']);vectors[c['fingerprint'],k]=v[cm['projections']['ETH']]
  else:
   aa,bb=c['source_fingerprints'];v=vectors[aa,k]+vectors[bb,k];assert core.navhash(v)==z['summary']['NAV_sha256_f64le'];vectors[c['fingerprint'],k]=v
   s=z['summary'];daily=v[cm['daily_indices']].tolist();assert s['daily_equity_usdt']==daily;metrics(v,daily,370,s);counts['metric_checks']+=1
   for j,(a,b) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):metrics(v[a:b+1],daily[j*30:min(j*30+30,370)+1],min(30,370-j*30),s['folds'][j]);counts['metric_checks']+=1
   # Recent slices must be inherited full-curve values, never reset account NAV.
   proxy={'daily_indices':cm['daily_indices'],'ts':ms['BTC']['ts']};assert len(v)==len(proxy['ts']);verify_recent(v,proxy,s)
  assert c['scenes'][k]==z['summary'];curves+=1
full={**old,**{c['fingerprint']:c for c in report['configs'].values()}}
for c in report['configs'].values():
 S,H=grid_axes(c);ns=[full[g['fingerprint']] for g in plan['grid'] if g['scope']==c['scope'] and abs([21,28,35].index(g['S'])-[21,28,35].index(S))<=1 and abs([.01,.02,.03].index(g['H'])-[.01,.02,.03].index(H))<=1];near(c['sensitivity']['local_3x_neighbor_positive_fraction'],sum(z['scenes']['3']['net_return_pct']>0 for z in ns)/len(ns));near(c['sensitivity']['local_recent_allcost_qualifying_fraction'],sum(recent_ok(z) for z in ns)/len(ns));assert c['status']==('passed' if all(c['criteria'].values()) else 'rejected')
assert decisions==5550 and curves==45 and counts['rejects']==0
put(R/'verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'independent_policy_decisions':decisions,'new_and_readonly_curves_checked':curves,'new_curves':30,'readonly_native_curves':15,'readonly_parent_hashes':12,'new_NAV_points':30*545013,'counts':counts,'policy':'Independent Fraction ROC/state and Decimal native cost/fund/book/margin replay; no call to new target/simulate/trade; exact old source NAV SHA recovery; continuous parent sum and every fold/recent metrics checked.'});print(json.dumps({'passed':True,'policy_decisions':decisions,'curves':curves,**counts}),flush=True)
