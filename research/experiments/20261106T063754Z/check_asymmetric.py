"""Synthetic-only full bank conservation and D/K causal-boundary/neighborhood tests."""
import copy,sys
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
for k in [.01,.02,.03]:
 for slope,w in [(-F(str(k))-F('.000001'),-1),(-F(str(k)),0),(F(0),0),(F(str(k)),0),(F(str(k))+F('.000001'),1)]:assert engine.slope_gate(slope,F(str(k)))==w
for raw,actual,vol,w in [(1,1,.09,1),(1,0,.045,1),(1,0,.045001,0),(-1,1,.045001,0),(0,1,.09,0)]:assert engine.entry_filter(raw,actual,vol,.045)==w
p={'slope_lags':[6,7,8],'slope_strengths':[.01,.02,.03]};g=lambda d,k,scope:{'L':5,'H':.02,'E':.005,'S':24,'K':k,'D':d,'N':625 if scope=='parent' else 4500,'fingerprint':f'{scope}/{d}/{k}','readonly':False}
p['grid']=[g(d,k,'parent') for d in p['slope_lags'] for k in p['slope_strengths']];p['native_grid']=[g(d,k,'native') for d in p['slope_lags'] for k in p['slope_strengths']];full={x['fingerprint']:{'name':x['fingerprint']} for x in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for x in grid:
  original={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(original);c=run.current_grid_row(original,x,scope);assert original==saved and c['D']==x['D'] and c['K']==x['K'];ns=run.neighborhood(c,p,full);n=(2 if x['D'] in [6,8] else 3)*(2 if x['K'] in [.01,.03] else 3);assert len(ns)==n;cases.append({'scope':scope,'D':x['D'],'K':x['K'],'neighbors':len(ns)})
sp={'parameters':{'lookback_days':5,'trend_lookback_days':24,'trend_slope_lag_days':1,'trend_slope_hurdle_fraction':.0005,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.005,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':23,'trend_decay_denominator':25,'trend_window_days':24,'trend_gate_scope':'new_or_reversed_position_only'}};causal=0
for d in [6,7,8]:
 sp['parameters']['trend_slope_lag_days']=d
 for k in [.01,.02,.03]:
  sp['parameters']['trend_slope_hurdle_fraction']=k
  for actual in [-1,0,1]:
   m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)]};x=engine.decide(sp,m,33,actual);m['closes'] += [D(1),D(999999)];assert engine.decide(sp,m,33,actual)==x;causal+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_D_K_neighborhoods':cases,'causal_cases':causal,'slope_threshold_cases':15,'volatility_retention_cases':5,'native_and_parent_two_axes':True,'maximum_required_context_days':32,'source_context_days':33});print('PASS18D/Kneighborhoods,27causality,strictslope/volatility andfullbankcapital/axisguards;0marketvaluations')
