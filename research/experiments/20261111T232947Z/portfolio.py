import math
import numpy as np
from common import *
MONEY=['cost_usdt','funding_usdt','base_funding_same_exposure_usdt','funding_stress_increment_usdt','funding_income_usdt','funding_outflow_usdt','gross_reference_price_PnL_usdt']
COUNTS=['executions','round_trips','rejected_orders','cash_or_units_violations','funding_settlements','nonzero_funding_settlements']
def summary(v,parts,weights,cm):
 daily=v[cm['daily_indices']].tolist();s=core.stats(v,daily,18);s['folds']=[];stamp=lambda d:core.stamp(cm['start_ns']+d*DAY)
 for j,(a,b) in enumerate(zip(cm['fold_indices'],cm['fold_indices'][1:])):
  lo,hi=j*3,min(j*3+3,18);s['folds'].append({'fold':j+1,'start_utc':stamp(lo),'end_exclusive_utc':stamp(hi),'duration_days':hi-lo,**core.stats(v[a:b+1],daily[lo:hi+1],hi-lo)})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-v[-1]/v[0])<1e-12
 s.update({f:sum(w*p[f] for w,p in zip(weights,parts)) for f in MONEY});s.update({f:sum(p[f] for p in parts) for f in COUNTS});capital=sum(w*p['initial_capital_usdt'] for w,p in zip(weights,parts));assert v[0]==capital and abs(s['gross_reference_price_PnL_usdt']+s['funding_usdt']-s['cost_usdt']-(v[-1]-capital))<2e-8
 costs={k:sum(w*p['cost_parts_usdt'][k] for w,p in zip(weights,parts)) for k in ['fee','half_spread','slippage','impact','tick_rounding']}
 s.update(initial_capital_usdt=capital,final_NAV_usdt=float(v[-1]),cost_pct_initial=s['cost_usdt']/capital*100,cost_parts_usdt=costs,gross_reference_PnL_to_execution_cost=(s['gross_reference_price_PnL_usdt']+s['funding_usdt'])/s['cost_usdt'] if s['cost_usdt'] else None,terminal_units='0',daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=core.navhash(v),axis_sha256=cm['sha256'],parent_executions=0,source_operation_count_policy='Counts and monetary fields sum actual native bank operations at childweights1/1; no fractional ledger scaling.',weighted_source_execution_units=sum(w*p['executions'] for w,p in zip(weights,parts)),weighted_source_closing_units=sum(w*p['round_trips'] for w,p in zip(weights,parts)),margin={'independent_sleeve_violations':sum(p['margin']['violations'] for p in parts),'underlying_native_hour_checks':sum(p['margin']['state_hour_extreme_bounding_checks'] for p in parts),'minimum_individual_sleeve_cushion_usdt':min((p['margin']['minimum_equity_minus_maintenance_usdt'] for p in parts if p['margin']['minimum_equity_minus_maintenance_usdt'] is not None),default=None),'no_cross_margin_netting':True,'scope':'Actual current-capital native bank maintenance proxies; no cross-margin netting.'})
 assert all(core.D(p['terminal_units'])==0 for p in parts)
 return s


def sum_aligned_full_banks(vectors,axes):
 assert len(vectors)==len(axes)==2
 assert all(np.asarray(v).ndim==1 and len(v)==len(a) and np.isfinite(v).all() for v,a in zip(vectors,axes))
 assert np.array_equal(axes[0],axes[1]),'Source event axes must be aligned before summing dollar NAV'
 return np.asarray(vectors[0])+np.asarray(vectors[1])
