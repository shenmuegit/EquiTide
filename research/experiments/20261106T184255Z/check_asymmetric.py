"""Synthetic D/VC causality, threshold boundaries, complete-bank capital and index guards."""
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
for slope,w in [(-F('.020001'),-1),(-F('.02'),0),(F(0),0),(F('.02'),0),(F('.020001'),1)]:assert engine.slope_gate(slope,F('.02'))==w
for cap in [.04,.045,.05]:
 for raw,actual,vol,w in [(1,1,cap+.01,1),(1,0,cap,1),(1,0,cap+.000001,0),(-1,1,cap+.000001,0),(0,1,cap+.01,0)]:assert engine.entry_filter(raw,actual,vol,cap)==w
p={'slope_lags':[6,7,8],'volatility_ceilings':[.04,.045,.05]};g=lambda d,v,scope:{'L':5,'H':.02,'E':.005,'S':24,'K':.02,'D':d,'VC':v,'N':1000 if scope=='parent' else 4500,'fingerprint':f'{scope}/{d}/{v}','readonly':False};p['grid']=[g(d,v,'parent') for d in p['slope_lags'] for v in p['volatility_ceilings']];p['native_grid']=[g(d,v,'native') for d in p['slope_lags'] for v in p['volatility_ceilings']];full={x['fingerprint']:{'name':x['fingerprint']} for x in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for x in grid:
  orig={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(orig);c=run.current_grid_row(orig,x,scope);assert orig==saved and c['VC']==x['VC'];ns=run.neighborhood(c,p,full);n=(2 if x['D'] in [6,8] else 3)*(2 if x['VC'] in [.04,.05] else 3);assert len(ns)==n;cases.append({'scope':scope,'D':x['D'],'VC':x['VC'],'neighbors':n})
sp={'parameters':{'lookback_days':5,'trend_lookback_days':24,'trend_slope_lag_days':7,'trend_slope_hurdle_fraction':.02,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.005,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':23,'trend_decay_denominator':25,'trend_window_days':24,'trend_gate_scope':'new_or_reversed_position_only'}};causal=0
for d in [6,7,8]:
 for cap in [.04,.045,.05]:
  sp['parameters'].update(trend_slope_lag_days=d,entry_volatility_ceiling=cap)
  for actual in [-1,0,1]:
   m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)]};x=engine.decide(sp,m,33,actual);m['closes'] += [D(1),D(999999)];assert engine.decide(sp,m,33,actual)==x;causal+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_D_VC_neighborhoods':cases,'causal_cases':causal,'strict_slope_threshold_cases':5,'volatility_boundary_and_retention_cases':15,'maximum_required_context_days':32,'source_context_days':33});print('PASS18D/VCneighborhoods,27causality,strictslope/15volboundaryretention,capital/axisguards;0marketvaluations')
