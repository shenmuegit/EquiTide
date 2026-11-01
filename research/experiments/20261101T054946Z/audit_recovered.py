"""Independent native-size/accounting recovery and whole-parent metrics, no strategy calls."""
import gzip,json,math
from decimal import Decimal as D,ROUND_FLOOR
import numpy as np
from common import *
import market
from audit_native import native
from audit_helpers_complete import near,metrics,verify_recent
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());ms,cm=market.load(p);vec,ss,old,arcs,diag=market.recover(p,ms,cm);counts={k:0 for k in ['funding','fills','rejects','metric_checks','margin_checks']};oldnative=newparents=quantitychecks=0
for fp,arc in arcs.items():
 ref=p['read_only_references'][fp];m=ms[ref['asset']];sp=json.loads((ROOT/ref['spec']).read_text());C=D(str(sp['parameters']['initial_capital_usdt']));N=D(str(sp['parameters']['fixed_entry_notional_usdt']));assert C==ref['capital_usdt'] and N==(C/10 if ref['asset']=='BTC' else D(4500))
 for k,z in arc['scenes'].items():
  v=native(z,m,m,int(k),None,sp,counts);assert np.array_equal(v[cm['projections'][ref['asset']]],vec[fp,k]);verify_recent(v,m,ss[fp,k]);oldnative+=1
  for t in z['trades']:
   if t['opening']:
    day=(t['trade_ts_ns']-m['first_ns']-MIN)//DAY;lot=D(m['meta']['lot_size']);qty=(N/m['closes'][day-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;assert D(t['quantity'])==qty and D(t['state_before']['cash'])>0;assert int(m['frame']['available_ts'][day*1440-1])+MIN<=t['trade_ts_ns'];quantitychecks+=1
proxy={'ts':cm['start_ns']+cm['keys']//16,'daily_indices':cm['daily_indices'],'fold_indices':cm['fold_indices']};curves={};source_reports={fp:sha(ROOT/x['report']) for fp,x in p['read_only_references'].items()}
for c in r['configs'].values():
 arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));sp=arc['spec'];assert reg.fingerprint(sp)==c['fingerprint'] and sha(ROOT/c['archive'])==c['archive_sha256'];fps=c['source_fingerprints'];assert [x['weight'] for x in sp['components']]==[1,1] and len(set(p['read_only_references'][fp]['asset'] for fp in fps))==2
 for k,z in arc['scenes'].items():
  v=vec[fps[0],k]+vec[fps[1],k];s=z['summary'];assert v[0]==c['capital_usdt']==sum(ss[fp,k]['initial_capital_usdt'] for fp in fps) and core.navhash(v)==s['NAV_sha256_f64le'] and s['daily_equity_usdt']==v[cm['daily_indices']].tolist() and c['scenes'][k]==s;metrics(v,s['daily_equity_usdt'],370,s);counts['metric_checks']+=1
  for j,(a,b) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):metrics(v[a:b+1],s['daily_equity_usdt'][j*30:min(j*30+30,370)+1],min(30,370-j*30),s['folds'][j]);counts['metric_checks']+=1
  verify_recent(v,proxy,s)
  for field in ['cost_usdt','funding_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements']:near(s[field],sum(ss[fp,k][field] for fp in fps),1e-12)
  for field in ['fee','half_spread','slippage','impact','tick_rounding']:near(s['cost_parts_usdt'][field],sum(ss[fp,k]['cost_parts_usdt'][field] for fp in fps),1e-12)
  near(v[-1]-v[0],s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt'],1e-10);assert s['parent_executions']==0 and s['margin']['independent_sleeve_violations']==sum(ss[fp,k]['margin']['violations'] for fp in fps) and z['source_full_NAV_sha256']==[ss[fp,k]['NAV_sha256_f64le'] for fp in fps];curves[c['fingerprint'],k]=v;newparents+=1
full={**old,**{c['fingerprint']:c for c in r['configs'].values()}};recent=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values())
for c in r['configs'].values():
 if c['role']=='benchmark':assert c['criteria']=={'benchmark_control_not_strategy_candidate':False} and c['status']=='rejected';continue
 ng=[g for g in p['grid'] if abs(p['BTC_capitals'].index(g['BTC_capital_usdt'])-p['BTC_capitals'].index(c['BTC_capital_usdt']))<=1 and abs(p['fast_hurdles'].index(g['H'])-p['fast_hurdles'].index(c['H']))<=1];ns=[full[g['fingerprint']] for g in ng];near(c['sensitivity']['local_3x_neighbor_positive_fraction'],sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns));near(c['sensitivity']['local_recent_allcost_qualifying_fraction'],sum(recent(x) for x in ns)/len(ns));assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns]
for x in r['matched_hold_comparisons']:
 a=full[x['fingerprint']]['scenes'][str(x['cost_multiplier'])];b=r['benchmark_grid'][str(x['BTC_capital_usdt'])]['scenes'][str(x['cost_multiplier'])];assert a['initial_capital_usdt']==b['initial_capital_usdt'];near(x['excess_to_hold_pp'],a['net_return_pct']-b['net_return_pct'])
assert oldnative==30 and newparents==18 and all(sha(ROOT/x['report'])==source_reports[fp] for fp,x in p['read_only_references'].items())
put(R/'verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_native_curves':0,'new_parent_curves':newparents,'new_NAV_points':newparents*len(cm['keys']),'read_only_native_curves':oldnative,'read_only_parent_hashes':18,'independent_new_policy_decisions':0,'native_open_quantity_and_lag_checks':quantitychecks,'counts':counts,'new_native_size_LOT_impact_capital_verified':True,'parent_no_linear_NAV_scaling':True,'matched_hold_comparisons_checked':len(r['matched_hold_comparisons']),'old_statuses_and_report_bytes_unchanged':True,'scope':'Independently recover30oldnativecurves with Decimal LOT/cash/fund/impact/hourrisk and originalactualN; sum exactonebankperasset/raw1/1, whole/fold/recent metrics. No native signal/trade/simulate calls or regrading. Newparentcombination evaluation only.'});print(json.dumps({'passed':True,'old_native_curves':oldnative,'new_parent_curves':newparents,'native_quantity_checks':quantitychecks,**counts}),flush=True)
