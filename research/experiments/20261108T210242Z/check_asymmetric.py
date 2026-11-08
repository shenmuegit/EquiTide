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
if '--negative-control-fixed-D4' in sys.argv:
 original_decide=engine.decide
 def incorrect_fixed_D4(spec,m,i,actual):
  wrong=copy.deepcopy(spec);wrong['parameters']['trend_slope_lag_days']=4;return original_decide(wrong,m,i,actual)
 engine.decide=incorrect_fixed_D4
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted axis accepted')
k=F('.015')
for slope,w in [(-k-F('.000001'),-1),(-k,0),(F(0),0),(k,0),(k+F('.000001'),1)]:assert engine.slope_gate(slope,k)==w
for raw,actual,vol,w in [(1,1,.09,1),(1,0,.045,1),(1,0,.045001,0),(-1,1,.045001,0),(0,1,.09,0)]:assert engine.entry_filter(raw,actual,vol,.045)==w
p={'slope_lags':[2,3,4],'slow_windows':[12,14,16]};g=lambda d,slow,scope:{'L':5,'H':.02,'E':.01,'S':slow,'K':.015,'D':d,'N':1000 if scope=='parent' else 4500,'fingerprint':f'{scope}/{d}/{slow}','readonly':False}
p['grid']=[g(d,slow,'parent') for d in p['slope_lags'] for slow in p['slow_windows']];p['native_grid']=[g(d,slow,'native') for d in p['slope_lags'] for slow in p['slow_windows']];full={x['fingerprint']:{'name':x['fingerprint']} for x in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for x in grid:
  original={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(original);c=run.current_grid_row(original,x,scope);assert original==saved and c['D']==x['D'] and c['S']==x['S'];neighbors=run.neighborhood(c,p,full);n=(2 if x['D'] in[2,4] else 3)*(2 if x['S'] in[12,16] else 3);assert len(neighbors)==n;cases.append({'scope':scope,'D':x['D'],'S':x['S'],'neighbors':len(neighbors)})
sp={'parameters':{'lookback_days':5,'trend_lookback_days':16,'trend_slope_lag_days':4,'trend_slope_hurdle_fraction':.015,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.01,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':15,'trend_decay_denominator':17,'trend_window_days':16,'trend_gate_scope':'new_or_reversed_position_only'}};causal=0;boundary=0;lagcases=0
for d in [2,3,4]:
 sp['parameters']['trend_slope_lag_days']=d
 for slow in [12,14,16]:
  l=5;h=.02;sp['parameters'].update(lookback_days=l,trend_lookback_days=slow,trend_window_days=slow,trend_decay_numerator=slow-1,trend_decay_denominator=slow+1)
  for actual in [-1,0,1]:
   m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)]};x=engine.decide(sp,m,33,actual);assert x[1]['return_exact']==str(F(m['closes'][32])/F(m['closes'][32-l])-1) and x[1]['fast_lookback_days']==l and x[1]['long_entry_return_hurdle']==x[1]['short_entry_return_hurdle']==h and x[1]['slow_lookback_days']==slow and x[1]['slope_lag_days']==d,'IncorrectslopeDmustbedetected';m['closes'] += [D(1),D(999999)];assert engine.decide(sp,m,33,actual)==x;causal+=1
sp['parameters']['trend_slope_lag_days']=4
entrybound=0
for slow in [12,14,16]:
 l=5;h=.02;sp['parameters'].update(lookback_days=l,trend_lookback_days=slow,trend_window_days=slow,trend_decay_numerator=slow-1,trend_decay_denominator=slow+1);lagcases+=1
 exact=F('.01');eps=F('.000001')
 for actual,roc,wanted in [(1,exact-eps,1),(1,exact,0),(1,exact+eps,0),(-1,-exact-eps,0),(-1,-exact,0),(-1,-exact+eps,-1)]:
  m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(D(roc.numerator)/D(roc.denominator)+1);got=engine.decide(sp,m,33,actual);assert got[0]==wanted,(h,actual,str(roc),got);boundary+=1
 for roc,base in [(F(str(h))-eps,0),(F(str(h)),0),(F(str(h))+eps,-1),(-F(str(h))-eps,1),(-F(str(h)),0),(-F(str(h))+eps,0)]:
  m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(D(roc.numerator)/D(roc.denominator)+1);got=engine.decide(sp,m,33,0);assert got[1]['ungated_desired']==base and got[1]['long_entry_return_hurdle']==got[1]['short_entry_return_hurdle']==h;entrybound+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_D_S_neighborhoods':cases,'causal_cases':causal,'distinct_slow_S_cases':lagcases,'strict_entry_boundary_cases':entrybound,'strict_exit_boundary_cases':boundary,'slope_threshold_cases':5,'volatility_retention_cases':5,'native_and_parent_two_axes':True,'maximum_required_context_days':30,'ETH_required_context_days':21,'ETH_signal_context_days':20,'ETH_cost_context_days':21,'source_context_days':33});print('PASS18D/Sneighborhoods,27causality,3distinctS,18strictentryH/18exitE1boundaries,5fixedK/vol andcapital/axis;0marketvaluations')
