"""Synthetic capital, D/E neighborhoods, exactexitboundaries and causality."""
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
if '--negative-control-fixed-L5' in sys.argv:
 original_decide=engine.decide
 def incorrect_fixed_L5(spec,m,i,actual):
  wrong=copy.deepcopy(spec);wrong['parameters']['lookback_days']=5;return original_decide(wrong,m,i,actual)
 engine.decide=incorrect_fixed_L5
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted axis accepted')
k=F('.015')
for slope,w in [(-k-F('.000001'),-1),(-k,0),(F(0),0),(k,0),(k+F('.000001'),1)]:assert engine.slope_gate(slope,k)==w
for raw,actual,vol,w in [(1,1,.09,1),(1,0,.045,1),(1,0,.045001,0),(-1,1,.045001,0),(0,1,.09,0)]:assert engine.entry_filter(raw,actual,vol,.045)==w
p={'slope_lags':[6,7,8],'fast_lookbacks':[3,5,7]};g=lambda d,l,scope:{'L':l,'H':.02,'E':.01,'S':24,'K':.015,'D':d,'N':1000 if scope=='parent' else 4500,'fingerprint':f'{scope}/{d}/{l}','readonly':False}
p['grid']=[g(d,l,'parent') for d in p['slope_lags'] for l in p['fast_lookbacks']];p['native_grid']=[g(d,l,'native') for d in p['slope_lags'] for l in p['fast_lookbacks']];full={x['fingerprint']:{'name':x['fingerprint']} for x in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for x in grid:
  original={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(original);c=run.current_grid_row(original,x,scope);assert original==saved and c['D']==x['D'] and c['L']==x['L'];neighbors=run.neighborhood(c,p,full);n=(2 if x['D'] in[6,8] else 3)*(2 if x['L'] in[3,7] else 3);assert len(neighbors)==n;cases.append({'scope':scope,'D':x['D'],'L':x['L'],'neighbors':len(neighbors)})
sp={'parameters':{'lookback_days':5,'trend_lookback_days':24,'trend_slope_lag_days':6,'trend_slope_hurdle_fraction':.015,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.01,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':23,'trend_decay_denominator':25,'trend_window_days':24,'trend_gate_scope':'new_or_reversed_position_only'}};causal=0;boundary=0;lagcases=0
for d in [6,7,8]:
 sp['parameters']['trend_slope_lag_days']=d
 for l in [3,5,7]:
  sp['parameters']['lookback_days']=l
  for actual in [-1,0,1]:
   m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)]};x=engine.decide(sp,m,33,actual);assert x[1]['return_exact']==str(F(m['closes'][32])/F(m['closes'][32-l])-1) and x[1]['fast_lookback_days']==l,'Incorrectfastlookbackmustbedetected';m['closes'] += [D(1),D(999999)];assert engine.decide(sp,m,33,actual)==x;causal+=1
sp['parameters']['trend_slope_lag_days']=6
for l in [3,5,7]:
 sp['parameters']['lookback_days']=l;m={'asset':'ETH','closes':[D(100)]*33};m['closes'][25]=D(107);m['closes'][27]=D(105);m['closes'][29]=D(103);x=engine.decide(sp,m,33,0);assert x[1]['return_exact']==str(F(100)/F(m['closes'][32-l])-1);lagcases+=1
 exact=F('.01');eps=F('.000001')
 for actual,roc,wanted in [(1,exact-eps,1),(1,exact,0),(1,exact+eps,0),(-1,-exact-eps,0),(-1,-exact,0),(-1,-exact+eps,-1)]:
  m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(D(roc.numerator)/D(roc.denominator)+1);got=engine.decide(sp,m,33,actual);assert got[0]==wanted,(l,actual,str(roc),got);boundary+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_D_L_neighborhoods':cases,'causal_cases':causal,'distinct_fast_lag_cases':lagcases,'strict_exit_boundary_cases':boundary,'slope_threshold_cases':5,'volatility_retention_cases':5,'native_and_parent_two_axes':True,'maximum_required_context_days':32,'source_context_days':33});print('PASS18D/Lneighborhoods,27causality,3distinctpastLindices,18strictE1boundaries,5fixedK/vol andcapital/axis;0marketvaluations')
