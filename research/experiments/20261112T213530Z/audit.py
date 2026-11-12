"""Independent saved native cash/LOT/cost/funding/signals, aligned parent and fixed gates audit."""
import gzip,json,math,statistics,copy
from decimal import Decimal as D,ROUND_FLOOR
from fractions import Fraction as F
import numpy as np
from common import *
import market
from audit_native import native
from audit_helpers_complete import near,metrics,verify_recent
plan=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());ms,cm=market.load(plan);vectors,source_scenes,old,arcs,diagnostics=market.recover(plan,ms,cm);counts={k:0 for k in ['funding','fills','rejects','metric_checks','margin_checks']};newnative=oldnative=parents=decisions=0
proxy={'ts':cm['start_ns']+cm['keys']//16,'daily_indices':cm['daily_indices'],'fold_indices':cm['fold_indices']}
for fp,arc in arcs.items():
 ref=plan['read_only_references'][fp];m=ms[ref['asset']];sp=json.loads((ROOT/ref['spec']).read_text())
 for k,z in arc['scenes'].items():
  v=native(z,m,m,int(k),None,sp,counts);assert np.array_equal(v[cm['projections'][ref['asset']]],vectors[fp,k]);verify_recent(v,m,source_scenes[fp,k]);oldnative+=1
for c in report['configs'].values():
 arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));sp=arc['spec'];assert reg.fingerprint(sp)==c['fingerprint'] and sha(ROOT/c['archive'])==c['archive_sha256']
 for k,z in arc['scenes'].items():
  fps=c['source_fingerprints'];assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['component_initial_entry_notionals_usdt']==[c['NB'],c['NE']];v=vectors[fps[0],k]+vectors[fps[1],k];s=z['summary'];assert core.navhash(v)==s['NAV_sha256_f64le'] and v[0]==18750 and s['daily_equity_usdt']==v[cm['daily_indices']].tolist();metrics(v,s['daily_equity_usdt'],370,s);counts['metric_checks']+=1
  for j,(a,b) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):metrics(v[a:b+1],s['daily_equity_usdt'][j*30:min(j*30+30,370)+1],min(30,370-j*30),s['folds'][j]);counts['metric_checks']+=1
  verify_recent(v,proxy,s)
  for f in ['cost_usdt','funding_usdt','gross_reference_price_PnL_usdt','executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements']:near(s[f],sum(source_scenes[x,k][f] for x in fps),1e-12)
  for f in ['fee','half_spread','slippage','impact','tick_rounding']:near(s['cost_parts_usdt'][f],sum(source_scenes[x,k]['cost_parts_usdt'][f] for x in fps),1e-12)
  near(v[-1]-v[0],s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt']);assert s['parent_executions']==0 and s['margin']['independent_sleeve_violations']==sum(source_scenes[x,k]['margin']['violations'] for x in fps);assert z['source_full_NAV_sha256']==[source_scenes[x,k]['NAV_sha256_f64le'] for x in fps] and z['source_common_axis_sha256']==cm['sha256'];parents+=1
  assert c['scenes'][k]==z['summary']
 if c['scope']=='parent':
  source_specs=[json.loads((ROOT/plan['read_only_references'][f]['spec']).read_text()) for f in c['source_fingerprints']];qb,qe=[z['parameters'] for z in source_specs];assert qb['return_hurdle']==c['H']==.03 and qb['exit_buffer_fraction']==c['E_BTC']==.01 and qb['entry_volatility_window_days']==10 and qb['entry_volatility_ceiling']==c['BVC'] and qb['entry_volatility_gate_scope']=='new_or_reversed_position_only';assert qe['entry_funding_volatility_ratio']==c['R'] and qe['entry_funding_budget_volatility_window_days']==c['VW']==8 and qe['entry_funding_settlement_count']==4 and qe['entry_volatility_window_days']==6 and qe['entry_volatility_ceiling']==.05625 and not qe.get('entry_close_location_filter') and not qe.get('entry_path_efficiency_filter')

def safety_ratio(scene):
 cost=scene['cost_usdt']
 if cost==0:
  assert scene['executions']==scene['round_trips']==0 and scene['gross_reference_price_PnL_usdt']==scene['funding_usdt']==0 and scene['gross_reference_PnL_to_execution_cost'] is None,'Zero execution cost must represent the verified flat bank'
  return None
 assert cost>0
 ratio=(scene['gross_reference_price_PnL_usdt']+scene['funding_usdt'])/cost;near(scene['gross_reference_PnL_to_execution_cost'],ratio);return ratio

full={**old,**{c['fingerprint']:c for c in report['configs'].values()}}
recentpass=lambda c:all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in c['scenes'].values())
for c in report['configs'].values():
 ng=[g for g in plan['grid'] if abs(plan['axes']['BTC_VOL_CAP'].index(g['BVC'])-plan['axes']['BTC_VOL_CAP'].index(c['BVC']))<=1 and abs(plan['axes']['ETH_FUND_R'].index(g['R'])-plan['axes']['ETH_FUND_R'].index(c['R']))<=1];dimensions=2
 ns=[full[g['fingerprint']] for g in ng];pos=sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns);rob=sum(recentpass(x) for x in ns)/len(ns);near(c['sensitivity']['local_3x_neighbor_positive_fraction'],pos);near(c['sensitivity']['local_recent_allcost_qualifying_fraction'],rob);assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns] and c['sensitivity']['dimension_count']==dimensions
 ss=list(c['scenes'].values());one,three=c['scenes']['1'],c['scenes']['3'];ratio=safety_ratio(one)
 expected={'positive_all_costs':all(z['net_return_pct']>0 for z in ss),'nine_of_twelve_positive_complete30d_1x_folds':sum(z['net_return_pct']>0 for z in one['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in ss),'recent40_six_of_eight_positive5d_all_costs':recentpass(c),'composite_DD3_lte25pct':three['max_drawdown_pct']<=25,'local_positive3_gte60pct':pos>=.6,'local_recent6of8_allcost_gte60pct':rob>=.6,'four_underlying_native_closes1':one['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_negative_native_collateral':all(z['cash_or_units_violations']==0 for z in ss),'no_native_order_rejections':all(z['rejected_orders']==0 for z in ss),'no_native_margin_proxy_violations':all(z['margin'].get('independent_sleeve_violations',z['margin'].get('violations'))==0 for z in ss),'native_terminal_flat':all(D(z['terminal_units'])==0 for z in ss),'minimum180days':True}
 assert c['criteria']==expected and c['status']==('passed' if all(expected.values()) else 'rejected') and c['failed_criteria']==[k for k,v in expected.items() if not v]
assert (newnative,oldnative,parents,decisions)==(0,27,12,0)
for x in report['matched_hold_comparisons']:
 c=report['all_current_grid'][x['fingerprint']];h=old[plan['benchmark_parent_fingerprint']];k=str(x['cost_multiplier']);near(x['excess_to_matched_hold_pp'],c['scenes'][k]['net_return_pct']-h['scenes'][k]['net_return_pct']);assert x['matched_notional'] and x['H']==c['H'] and x['R']==c['R'] and x['E_BTC']==c['E_BTC'] and x['VW']==c['VW'] and [c['NB'],c['NE']]==[1000,4000]
for fp,ref in plan['read_only_references'].items():
 z=reg.read_records(ROOT/'research/automation/registry.jsonl')[fp];assert z['status']==ref['status'] and z['report_sha256']==ref['report_sha256']
put(R/'verification.json',{'passed':True,'report_sha256':sha(R/'report.json'),'plan_sha256':sha(R/'plan.json'),'new_native_curves':newnative,'new_parent_curves':parents,'read_only_native_curves':oldnative,'independent_new_policy_decisions':decisions,'counts':counts,'old_statuses_and_reports_unchanged':True,'reused_actual_native_quantity_LOT_and_volume_impact_independently_verified':True,'reused_BTC_N_values':[1000],'reused_ETH_N_values':[4000],'BTC_pricevol_caps':[.03,.04,.05],'ETH_funding_ratios':[.00875,.01,.01125],'ETH_fixed_budget_VW':8,'new_BTC_policies':0,'new_ETH_policies':0,'existing_BTC_and_controls_readonly':True,'parent_two_rule_axes':True,'new_native_policy_runs':0,'parent_raw_weights':[1,1],'no_source_NAV_scaling':True,'scope':'Independently replay saved Decimalcash/fund/LOT/adversetick/volumeimpact, complete native saved q/cash/cost/funding/hourrisk/NAV and both component rule axes; all policies previously executed and hashed, no new policy decisions;no simulate/decide/trade functions invoked by audit.'});print(json.dumps({'passed':True,'new_native':newnative,'old_native':oldnative,'new_parent':parents,'new_decisions':decisions,**counts}),flush=True)
