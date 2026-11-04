"""Independent old-ledger replay and new portfolio whole/fold/recent metrics; no native sim."""
import gzip,json
import numpy as np
from common import *
import market
from audit_native import native
from audit_helpers_complete import near,metrics,verify_recent
p=json.loads((R/'plan.json').read_text());rep=json.loads((R/'report.json').read_text());ms,cm=market.load(p);vectors,ss,old,arcs,diag=market.recover(p,ms,cm);counts={k:0 for k in ['funding','fills','rejects','metric_checks','margin_checks']};oldnative=parents=0;proxy={'ts':cm['start_ns']+cm['keys']//16,'daily_indices':cm['daily_indices'],'fold_indices':cm['fold_indices']}
for fp,arc in arcs.items():
 ref=p['read_only_references'][fp];m=ms[ref['asset']];sp=json.loads((ROOT/ref['spec']).read_text())
 for k,z in arc['scenes'].items():
  v=native(z,m,m,int(k),None,sp,counts);assert np.array_equal(v[cm['projections'][ref['asset']]],vectors[fp,k]);verify_recent(v,m,ss[fp,k]);oldnative+=1
for c in rep['configs'].values():
 arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));sp=arc['spec'];assert reg.fingerprint(sp)==c['fingerprint'] and sha(ROOT/c['archive'])==c['archive_sha256'] and c['scope']=='parent' and [x['weight'] for x in sp['components']]==[1,1]
 for k,z in arc['scenes'].items():
  fps=c['source_fingerprints'];assert len(fps)==2 and [p['read_only_references'][fp]['capital_usdt'] for fp in fps]==[15000,15000];v=vectors[fps[0],k]+vectors[fps[1],k];s=z['summary'];assert core.navhash(v)==s['NAV_sha256_f64le'] and v[0]==c['capital_usdt']==30000 and s['daily_equity_usdt']==v[cm['daily_indices']].tolist();metrics(v,s['daily_equity_usdt'],370,s);counts['metric_checks']+=1
  for j,(a,b) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):metrics(v[a:b+1],s['daily_equity_usdt'][j*30:min(j*30+30,370)+1],min(30,370-j*30),s['folds'][j]);counts['metric_checks']+=1
  verify_recent(v,proxy,s)
  for field in ['cost_usdt','funding_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements']:near(s[field],sum(ss[fp,k][field] for fp in fps),1e-12)
  for field in ['fee','half_spread','slippage','impact','tick_rounding']:near(s['cost_parts_usdt'][field],sum(ss[fp,k]['cost_parts_usdt'][field] for fp in fps),1e-12)
  near(v[-1]-v[0],s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],1e-10);assert s['parent_executions']==0 and s['margin']['independent_sleeve_violations']==sum(ss[fp,k]['margin']['violations'] for fp in fps);assert z['source_full_NAV_sha256']==[ss[fp,k]['NAV_sha256_f64le'] for fp in fps] and z['source_common_axis_sha256']==cm['sha256'] and c['scenes'][k]==s;parents+=1
full={c['fingerprint']:c for c in rep['configs'].values()};recent=lambda c:all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
for c in full.values():
 ng=[g for g in p['grid'] if abs(p['lookbacks'].index(g['L'])-p['lookbacks'].index(c['L']))<=1 and abs(p['hurdles'].index(g['H'])-p['hurdles'].index(c['H']))<=1];ns=[full[g['fingerprint']] for g in ng];near(c['sensitivity']['local_3x_neighbor_positive_fraction'],sum(z['scenes']['3']['net_return_pct']>0 for z in ns)/len(ns));near(c['sensitivity']['local_recent_allcost_qualifying_fraction'],sum(recent(z) for z in ns)/len(ns));assert c['sensitivity']['neighbor_names']==[z['name'] for z in ns]
for x in rep['matched_hold_comparisons']:
 a=full[x['fingerprint']]['scenes'][str(x['cost_multiplier'])];b=rep['benchmark_grid']['matched']['scenes'][str(x['cost_multiplier'])];assert a['initial_capital_usdt']==b['initial_capital_usdt']==30000;near(x['excess_to_hold_pp'],a['net_return_pct']-b['net_return_pct'])
assert oldnative==39 and parents==27 and counts['rejects']==0
put(R/'verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_native_curves':0,'new_parent_curves':27,'new_NAV_points':sum(z['NAV_points'] for c in rep['configs'].values() for z in c['scenes'].values()),'read_only_native_curves':oldnative,'read_only_parent_hashes':30,'independent_new_policy_decisions':0,'counts':counts,'new_native_size_LOT_impact_capital_verified':False,'actual_source_native_size_cost_funding_risk_replayed':True,'parent_no_linear_NAV_scaling':True,'matched_hold_comparisons_checked':27,'old_statuses_and_report_bytes_unchanged':True,'scope':'Thirtynine existingnativecostcurves independentlyreplayed fromactualledgers;new27wholebankportfolio curves/wholeDD/13folds/recent8folds checked. Zero newnative decisions/simulations/orders;oldoperationcounts not newtrades. Differentcapital/exposurefromoldallocation disclosed.'});print(json.dumps({'passed':True,'new_native_curves':0,'new_parent_curves':27,'old_native_curves':oldnative,'policy_decisions':0,**counts}),flush=True)
