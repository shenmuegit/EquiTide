import math
from common import *
MONEY=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']
COUNTS=['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']
def summary(v,parts,weights,cm):
 daily=v[cm['daily_indices']].tolist();s=core.stats(v,daily,370);s['folds']=[];stamp=lambda d:core.stamp(cm['start_ns']+d*DAY)
 for j,(a,b) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):
  lo,hi=j*30,min(j*30+30,370);s['folds'].append({'fold':j+1,'start_utc':stamp(lo),'end_exclusive_utc':stamp(hi),'duration_days':hi-lo,**core.stats(v[a:b+1],daily[lo:hi+1],hi-lo)})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/v[0])<1e-12
 s.update({f:sum(w*p[f] for w,p in zip(weights,parts)) for f in MONEY});s.update({f:sum(p[f] for p in parts) for f in COUNTS});capital=sum(w*p['initial_capital_usdt'] for w,p in zip(weights,parts));assert v[0]==capital and abs(s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt']-(v[-1]-capital))<2e-8
 costs={k:sum(w*p['cost_parts_usdt'][k] for w,p in zip(weights,parts)) for k in ['fee','half_spread','slippage','impact','tick_rounding']}
 s.update(initial_capital_usdt=capital,final_NAV_usdt=float(v[-1]),cost_pct_initial=s['cost_usdt']/capital*100,cost_parts_usdt=costs,gross_reference_PnL_to_execution_cost=(s['gross_reference_price_PnL_usdt']+s['funding_usdt'])/s['cost_usdt'] if s['cost_usdt'] else None,terminal_units='0',daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=core.navhash(v),axis_sha256=cm['sha256'],parent_executions=0,source_operation_count_policy='Counts and monetary fields sum actual native bank operations at childweights1/1; no fractional ledger scaling.',weighted_source_execution_units=sum(w*p['executions'] for w,p in zip(weights,parts)),weighted_source_closing_units=sum(w*p['round_trips'] for w,p in zip(weights,parts)),margin={'independent_sleeve_violations':sum(p['margin']['violations'] for p in parts),'underlying_native_hour_checks':sum(p['margin']['state_hour_extreme_bounding_checks'] for p in parts),'minimum_individual_sleeve_cushion_usdt':min(p['margin']['minimum_equity_minus_maintenance_usdt'] for p in parts if p['margin']['minimum_equity_minus_maintenance_usdt'] is not None),'no_cross_margin_netting':True,'scope':'Actual current-capital native bank maintenance proxies; no cross-margin netting.'})
 assert all(core.D(p['terminal_units'])==0 for p in parts)
 a=cm['daily_indices'][330];tail=v[a:];t={**core.stats(tail,daily[330:],40),'start_utc':stamp(330),'end_exclusive_utc':stamp(370),'initial_NAV_usdt':float(tail[0]),'final_NAV_usdt':float(tail[-1]),'NAV_points':len(tail),'NAV_sha256_f64le':core.navhash(tail),'daily_equity_usdt':daily[330:],'state_policy':'Inherited day330 actual native bank states, no reset or diagnostic orders.','folds':[]}
 for j in range(8):
  lo,hi=330+5*j,335+5*j;aa,bb=cm['daily_indices'][[lo,hi]];t['folds'].append({'fold':j+1,'start_utc':stamp(lo),'end_exclusive_utc':stamp(hi),'duration_days':5,**core.stats(v[aa:bb+1],daily[lo:hi+1],5)})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in t['folds'])-tail[-1]/tail[0])<1e-12;s['recent40']=t;return s
