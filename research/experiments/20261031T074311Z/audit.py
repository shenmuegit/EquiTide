"""Read-only independent native money replay and funded-interest composite verification."""
import gzip,json,math
from decimal import Decimal as D
import numpy as np
from common import *
import market
from audit_native import native
from audit_helpers_complete import near,metrics,verify_recent

plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ms,cm=market.load(plan);oldv,oldss,old=market.recover(plan,ms,cm);vectors={};counts={k:0 for k in ['funding','fills','rejects','metric_checks','margin_checks']};native_curves=0;parent_curves=0
proxy={'ts':cm['start_ns']+cm['keys']//16,'daily_indices':cm['daily_indices'],'fold_indices':cm['fold_indices']}
for fp,ref in plan['read_only_references'].items():
 if ref['scope']!='native':continue
 arc=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));m=ms[ref['asset']]
 for k,z in arc['scenes'].items():
  v=native(z,m,m,int(k),None,None,counts);v=v[cm['projections'][ref['asset']]];assert np.array_equal(v,oldv[fp,k]);vectors[fp,k]=v;native_curves+=1

for c in report['configs'].values():
 arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));spec=json.loads((ROOT/c['spec']).read_text());assert spec==arc['spec'] and reg.fingerprint(spec)==c['fingerprint'] and sha(ROOT/c['archive'])==c['archive_sha256'];weights=spec['parameters']['raw_component_multipliers'];fps=[x['fingerprint'] for x in spec['components']];assert fps==c['source_fingerprints'] and weights==[c['raw_BTC_weight'],c['raw_ETH_weight']]==[x['weight'] for x in spec['components']]
 for k,z in arc['scenes'].items():
  v=np.add(np.multiply(vectors[fps[0],k],weights[0]),np.multiply(vectors[fps[1],k],weights[1]));s=z['summary'];assert s==c['scenes'][k] and s['initial_capital_usdt']==v[0]==10000*sum(weights)==c['capital_usdt'];assert core.navhash(v)==s['NAV_sha256_f64le'] and s['NAV_points']==len(v);daily=v[cm['daily_indices']].tolist();assert daily==s['daily_equity_usdt'];metrics(v,daily,370,s);counts['metric_checks']+=1
  for j,(a,b) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):metrics(v[a:b+1],daily[j*30:min(j*30+30,370)+1],min(30,370-j*30),s['folds'][j]);counts['metric_checks']+=1
  verify_recent(v,proxy,s)
  source=[oldss[fp,k] for fp in fps]
  for field in ['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']:
   expected=sum(D(str(w))*D(str(x[field])) for w,x in zip(weights,source));near(s[field],expected,1e-12)
  for field in ['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']:assert s[field]==sum(x[field] for x in source)
  for field in ['fee','half_spread','slippage','impact','tick_rounding']:near(s['cost_parts_usdt'][field],sum(D(str(w))*D(str(x['cost_parts_usdt'][field])) for w,x in zip(weights,source)),1e-12)
  near(s['cost_usdt'],sum(s['cost_parts_usdt'].values()),1e-12);near(v[-1]-v[0],s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],1e-10);near(s['gross_reference_PnL_to_execution_cost'],(s['gross_reference_price_PnL_usdt']+s['funding_usdt'])/s['cost_usdt']);assert s['parent_executions']==0 and s['margin']['independent_sleeve_violations']==sum(x['margin']['violations'] for x in source)==0 and D(s['terminal_units'])==0
  assert arc['scenes'][k]['source_full_NAV_sha256']==[x['NAV_sha256_f64le'] for x in source];parent_curves+=1

full={**old,**{c['fingerprint']:c for c in report['configs'].values()}}
recentpass=lambda c:all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
for c in report['configs'].values():
 wb,we=c['raw_BTC_weight'],c['raw_ETH_weight'];axis=[.5,1,1.5];ns=[full[g['fingerprint']] for g in plan['grid'] if g['role']==c['role'] and abs(axis.index(g['wB'])-axis.index(wb))<=1 and abs(axis.index(g['wE'])-axis.index(we))<=1];p=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);q=sum(recentpass(x) for x in ns)/len(ns);assert c['sensitivity']['neighbor_count']==len(ns) and c['sensitivity']['neighbor_names']==[x['name'] for x in ns];near(c['sensitivity']['local_3x_neighbor_positive_fraction'],p);near(c['sensitivity']['local_recent_allcost_qualifying_fraction'],q)
 gates=c['criteria'];assert gates['positive_all_costs']==all(z['net_return_pct']>0 for z in c['scenes'].values()) and gates['nine_of_twelve_positive_complete30d_1x_folds']==(sum(f['net_return_pct']>0 for f in c['scenes']['1']['folds'][:12])>=9) and gates['recent40_six_of_eight_positive5d_all_costs']==recentpass(c) and gates['local_positive3_gte60pct']==(p>=.6) and gates['local_recent6of8_allcost_gte60pct']==(q>=.6);assert c['status']==('passed' if all(gates.values()) else 'rejected')
homothetic=[]
for role in ['candidate','benchmark']:
 center=old[plan['old_center_fingerprints'][role]]
 for w in [.5,1.5]:
  row=next(c for c in report['configs'].values() if c['role']==role and c['raw_BTC_weight']==c['raw_ETH_weight']==w)
  for k,z in row['scenes'].items():
   near(z['net_return_pct'],center['scenes'][k]['net_return_pct'],1e-12);near(z['max_drawdown_pct'],center['scenes'][k]['max_drawdown_pct'],1e-12);assert np.allclose(np.array(z['daily_equity_usdt'])/z['initial_capital_usdt'],np.array(center['scenes'][k]['daily_equity_usdt'])/20000,atol=1e-15,rtol=1e-15)
  homothetic.append(row['name'])
assert native_curves==12 and parent_curves==36 and counts['rejects']==0
put(R/'verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'independent_native_source_curves':native_curves,'new_parent_curves':parent_curves,'new_parent_NAV_points':parent_curves*len(cm['keys']),'old_parent_NAV_hashes':18,'counts':counts,'new_native_source_signals_or_orders':0,'parent_fills':0,'homothetic_new_configs_checked':homothetic,'independent_normalized_weight_ratios_per_role':7,'policy':'Independent native Decimal money/funding/impact/margin replay, aligned source SHA, raw-capital and cost contribution checks, every whole/month/recent curve metric and frozen sensitivity gates. No source target/simulate/trade called; not scaled-native-order execution proof.'});print(json.dumps({'passed':True,'native_curves':native_curves,'new_parent_curves':parent_curves,**counts}),flush=True)
