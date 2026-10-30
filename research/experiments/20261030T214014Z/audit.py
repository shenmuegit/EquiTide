"""Independent original cashflow replay, causal revaluation, portfolio metrics."""
import gzip,json,math
import numpy as np
from common import *
import market
from audit_helpers_complete import near,metrics,verify_recent
old_audit=module(ROOT/'research/experiments/20261030T194013Z/audit_complete.py','readonly_original_native_audit')

def fullmetrics(v,axis,z):
 daily=v[axis['daily_indices']].tolist();assert core.navhash(v)==z['NAV_sha256_f64le'] and len(v)==z['NAV_points'] and daily==z['daily_equity_usdt'];metrics(v,daily,370,z)
 for j,(a,b) in enumerate(zip(axis['fold_indices'],axis['fold_indices'][1:])):
  days=min(30,370-30*j);f=z['folds'][j];assert f['duration_days']==days and f['start_utc']==core.stamp(int(axis['ts'][a])) and f['end_exclusive_utc']==core.stamp(int(axis['ts'][b]));metrics(v[a:b+1],daily[30*j:30*j+days+1],days,f)
 assert len(z['folds'])==13 and abs(math.prod(1+f['net_return_pct']/100 for f in z['folds'])-v[-1]/v[0])<1e-12;verify_recent(v,axis,z)

def main():
 p=json.loads((R/'plan.json').read_text());report=json.loads((R/'report.json').read_text());assert report['frozen_plan_sha256']==sha(R/'plan.json');ms,axis=market.load(p);oldms={a:core.load_market(a,fs) for a,fs in p['data']['assets'].items()};curves={};summaries={};counters={'funding':0,'fills':0,'rejects':0,'metric_checks':0,'margin_checks':0};sourceproof=json.loads((R/'source_revaluation.json').read_text());source_original_points=0;revalued_extra=0
 for asset,m in oldms.items():m.update(first_ns=int(m['frame']['open_ts'][0]),fund_lookup={x['settlement_ts']:x for x in m['funds']},terminal_reference_decimal=m['frame']['open'][403*1440+1])
 arcs={fp:json.loads(gzip.decompress((ROOT/x['archive']).read_bytes())) for fp,x in p['source_results'].items()}
 for fp,x in p['source_results'].items():
  assert sha(ROOT/x['archive'])==x['archive_sha256'] and sha(ROOT/x['report'])==x['report_sha256'] and sha(ROOT/x['spec'])==x['spec_sha256'] and arcs[fp]['fingerprint']==fp
 for k in ['1','2','3']:
  vals=[];originals=[]
  for asset,x in zip(['BTC','ETH'],p['trend_native']):
   fp=x['fingerprint'];scene=arcs[fp]['scenes'][k];m=oldms[asset];original=old_audit.native(scene,m,m,int(k),None,None,counters);originals.append(original);source_original_points+=len(original)
   oldkeys=np.empty(len(m['ts']),dtype=axis['keys'].dtype);oldkeys['t']=m['ts'];oldkeys['k']=m['codes'];j=np.searchsorted(oldkeys,axis['keys'],side='right')-1;assert (j>=0).all();seg=scene['state_segments'];si=np.searchsorted(np.array([s['axis_start'] for s in seg]),j,side='right')-1;cash=np.array([float(s['cash']) for s in seg])[si];q=np.array([float(s['signed_units']) for s in seg])[si];entry=np.array([float(s['entry_price']) for s in seg])[si];v=cash+q*(ms[asset]['axis_prices']-entry);origix=np.searchsorted(axis['keys'],oldkeys);assert np.array_equal(v[origix],original);assert core.navhash(v)==sourceproof[fp+':'+k]['expanded_NAV_sha256_f64le'];vals.append(v);revalued_extra+=len(v)-len(original)
  tfp=p['trend_parent']['fingerprint'];z=arcs[tfp]['scenes'][k]['summary'];assert core.navhash(originals[0]+originals[1])==z['NAV_sha256_f64le'];curves[(tfp,k)]=vals[0]+vals[1];summaries[(tfp,k)]=z
  for x in p['paired_parents'].values():
   fp=x['fingerprint'];scene=arcs[fp]['scenes'][k];vv=[]
   for asset in ['BTC','ETH']:vv.append(old_audit.native(scene['legs'][asset],ms[asset],axis,int(k),None,None,counters));source_original_points+=len(vv[-1])
   v=vv[0]+vv[1];assert core.navhash(v)==scene['summary']['NAV_sha256_f64le'];curves[(fp,k)]=v;summaries[(fp,k)]=scene['summary']
 portfolio_points=0;metric_count=0
 for c in report['configs'].values():
  arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));assert sha(ROOT/c['archive'])==c['archive_sha256'] and arc['fingerprint']==c['fingerprint'];rr=reg.read_records(ROOT/'research/automation/registry.jsonl')[c['fingerprint']];assert rr['recorded_at_utc']>report['evaluation_started_utc'] if rr['status']!='reserved' else rr['recorded_at_utc']<report['evaluation_started_utc']
  for k,z in c['scenes'].items():
   assert arc['scenes'][k]['summary']==z;v=curves[(c['trend_fp'],k)].copy();xs=[summaries[(c['trend_fp'],k)]];ws=[1]
   if c['pair_fp']:v+=c['raw_pair_units']*curves[(c['pair_fp'],k)];xs.append(summaries[(c['pair_fp'],k)]);ws.append(c['raw_pair_units'])
   else:v+=c['cash_usdt']
   assert v[0]==c['capital_usdt'];fullmetrics(v,axis,z);portfolio_points+=len(v);metric_count+=23
   for key in ['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']:near(z[key],sum(w*x[key] for w,x in zip(ws,xs)),1e-12)
   for part in z['cost_parts_usdt']:near(z['cost_parts_usdt'][part],sum(w*x['cost_parts_usdt'][part] for w,x in zip(ws,xs)),1e-12)
   for key in ['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']:assert z[key]==sum(x[key] for x in xs)
   near(z['gross_reference_price_PnL_usdt']+z['funding_usdt']-z['cost_usdt'],v[-1]-c['capital_usdt']);near(z['gross_reference_PnL_to_execution_cost'],(z['gross_reference_price_PnL_usdt']+z['funding_usdt'])/z['cost_usdt']);assert z['terminal_flat'] and not z['margin']['independent_sleeve_violations']
 # Independent gate calculation, including all-cost recent consistency and 2D neighbors.
 candidates=[c for c in report['configs'].values() if c['role']=='candidate'];controls=[c for c in report['configs'].values() if c['role']=='benchmark'];es=[2,2.5,3];ws=[.25,.5,.75]
 strict=lambda c:all(sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values())
 for c in report['configs'].values():
  ns=[x for x in candidates if abs(es.index(x['entry_z'])-es.index(c['entry_z']))<=1 and abs(ws.index(x['raw_pair_units'])-ws.index(c['raw_pair_units']))<=1] if c['role']=='candidate' else controls;s=c['scenes'];g={'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'nine_of_twelve_positive_complete30d_1x_folds':sum(f['net_return_pct']>0 for f in s['1']['folds'][:12])>=9,'recent40_positive_all_costs':all(z['recent40']['net_return_pct']>0 for z in s.values()),'recent40_six_of_eight_positive5d_all_costs':strict(c),'composite_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'local_positive3_gte60pct':sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns)>=.6,'local_recent6of8_allcost_gte60pct':sum(strict(x) for x in ns)/len(ns)>=.6,'four_source_completed_round_trips1':s['1']['round_trips']>=4,'gross_plus_funding_to_cost1_gte2_5':s['1']['gross_reference_PnL_to_execution_cost']>=2.5,'no_negative_collateral':all(z['cash_or_units_violations']==0 for z in s.values()),'no_order_rejections':all(z['rejected_orders']==0 for z in s.values()),'no_margin_proxy_violations':all(z['margin']['independent_sleeve_violations']==0 for z in s.values()),'terminal_flat':all(z['terminal_flat'] for z in s.values()),'minimum180days':True};assert c['criteria']==g and c['status']==('passed' if all(g.values()) else 'rejected') and c['failed_criteria']==[a for a,b in g.items() if not b];assert c['sensitivity']['neighbor_names']==[x['name'] for x in ns]
 out={'passed':True,'source_native_curves_independently_replayed':24,'source_original_NAV_points':source_original_points,'extra_trend_revaluation_points':revalued_extra,'new_portfolio_curves':36,'new_portfolio_NAV_points':portfolio_points,'portfolio_overall_monthly_recent_metric_checks':metric_count,'source_cashflow_and_margin_checks':counters,'source_orders_or_signals_resimulated':0,'all_original_native_and_parent_NAV_hashes_exact':True,'sourcepoint_preservation_and_causal_extra_OPEN_valuation':True,'raw_ownership_and_independent_cost_gates_verified':True,'report_sha256':sha(R/'report.json')};put(R/'verification.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':main()
