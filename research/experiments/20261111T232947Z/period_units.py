"""Synthetic18-day calendar, sixfold compound return and cross-fold global drawdown test."""
import copy,json,math,sys
import numpy as np
from common import *
import engine,period_summary
from audit_helpers_complete import metrics
assert (core.START,core.END,core.DAYS,engine.START,engine.END,engine.DAYS)==(33,51,18,33,51,18)
original=period_summary.stats
if '--fold-reset' in sys.argv:
 def bad(v,daily,days):
  s=original(v,daily,days)
  if days==18:s['max_drawdown_pct']=max(original(v[j:j+4],daily[j:j+4],3)['max_drawdown_pct'] for j in range(0,18,3))
  return s
 period_summary.stats=bad
if '--wrong-days' in sys.argv:period_summary.DAYS=370
v=np.array([100.,110.,120.,115.,100.,90.,95.,96.,97.,98.,99.,100.,101.,102.,103.,104.,105.,106.,107.]);codes=np.zeros(19,dtype=np.int8);codes[-1]=9;m={'daily_indices':np.arange(19),'fold_indices':np.arange(0,19,3),'start_ns':1792800060000000000,'codes':codes,'axis_sha256':'synthetic','axis_price_sha256_f64le':'synthetic'};parts={k:'0' for k in ['fee','half_spread','slippage','impact','tick_rounding']};trades=[{'status':'filled','opening':False,'cost_parts':parts,'reference_price_PnL_usdt':'7'}];segments=[{'cash':'107','signed_units':'0'}];period_summary.margin_audit=lambda *args:{'violations':0,'state_hour_extreme_bounding_checks':0,'minimum_equity_minus_maintenance_usdt':None};s=period_summary.native_summary(m,v,trades,[],segments);assert abs(s['max_drawdown_pct']-25)<1e-12 and s['net_return_pct']==100*(107/100-1) and len(s['folds'])==6 and all(f['duration_days']==3 for f in s['folds']);metrics(v,v.tolist(),18,s)
for j,f in enumerate(s['folds']):metrics(v[3*j:3*j+4],v[3*j:3*j+4],3,f)
assert abs(math.prod(1+f['net_return_pct']/100 for f in s['folds'])-1.07)<1e-12 and s['folds'][-1]['end_exclusive_utc']=='2026-11-11T00:01:00Z'
if len(sys.argv)==1:put(R/'period_primitive_verification.json',{'passed':True,'synthetic_only':True,'period_days':18,'folds':6,'fold_days':3,'global_cross_fold_drawdown25pct_not_max_or_mean_of_fold_drawdowns':True,'native_summary_exact_calendar_and_compounded_return':True,'independent_metrics_checks':7,'summary_margin_stubbed_synthetic_only':True,'real_market_or_account_calculations':0})
print('PASS synthetic18day/six3dayfold/wholeDD25% and compound/annualization guards;0realmarket/accountcalculations')
