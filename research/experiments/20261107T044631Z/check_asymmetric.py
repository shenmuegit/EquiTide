"""Synthetic complete-bank and causal-axis checks, no market strategy evaluation."""
import copy,itertools,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
from common import *
import engine,run
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48])
if '--negative-control-double-weighting' in sys.argv:
 wrong=.2*btc+.8*eth;assert wrong[0]==18750,'Synthetic double-weighting raw full banks must fail capital identity'
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted axis accepted')
for slope,w in [(-F('.020001'),-1),(-F('.02'),0),(F(0),0),(F('.02'),0),(F('.020001'),1)]:assert engine.slope_gate(slope,F('.02'))==w
p={'BTC_lookbacks':[27,29,31],'slope_lags':[6,7,8],'volatility_ceilings':[.04,.045,.05]};base=lambda d,v:{'L':5,'H':.02,'E':.005,'S':24,'K':.02,'D':d,'VC':v,'readonly':False};p['grid']=[{**base(d,v),'BTC_L':h,'N':1000,'fingerprint':f'parent/{h}/{d}/{v}'} for h,d,v in itertools.product(p['BTC_lookbacks'],p['slope_lags'],p['volatility_ceilings'])];p['native_grid']=[{**base(d,v),'N':4500,'fingerprint':f'native/{d}/{v}'} for d,v in itertools.product(p['slope_lags'],p['volatility_ceilings'])];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for g in grid:
  original={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};before=copy.deepcopy(original);c=run.current_grid_row(original,g,scope);assert original==before;ns=run.neighborhood(c,p,full);expected=(2 if g['D'] in [6,8] else 3)*(2 if g['VC'] in [.04,.05] else 3)*(2 if g.get('BTC_L') in [27,31] else 3) if scope=='parent' else (2 if g['D'] in [6,8] else 3)*(2 if g['VC'] in [.04,.05] else 3);assert len(ns)==expected;cases.append({'scope':scope,'BTC_L':g.get('BTC_L'),'D':g['D'],'VC':g['VC'],'neighbors':expected})
sp={'parameters':{'lookback_days':5,'trend_lookback_days':24,'trend_slope_lag_days':7,'trend_slope_hurdle_fraction':.02,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.005,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':23,'trend_decay_denominator':25,'trend_window_days':24,'trend_gate_scope':'new_or_reversed_position_only'}};causal=0
for d,v,actual in itertools.product([6,7,8],[.04,.045,.05],[-1,0,1]):
 sp['parameters'].update(trend_slope_lag_days=d,entry_volatility_ceiling=v);m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)]};a=engine.decide(sp,m,33,actual);m['closes'] += [D(1),D(999999)];assert engine.decide(sp,m,33,actual)==a;causal+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_parent_L_D_VC_and_readonly_native_D_VC_neighborhoods':cases,'causal_cases':causal,'maximum_required_context_days':32,'source_context_days':33,'new_native_market_evaluations':0});print('PASS27jointL/D/VCparent+9readonlyD/VC neighborhoods,27syntheticcausality,capital/axisguards;0marketvaluations')
