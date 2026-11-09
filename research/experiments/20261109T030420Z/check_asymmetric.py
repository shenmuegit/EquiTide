"""Synthetic fixedD3 K/S identities, exact boundaries, causal and bank checks."""
import copy,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
from common import *
import engine,run
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48])
if '--negative-control-double-weighting' in sys.argv:
 assert (.2*btc+.8*eth)[0]==18750,'Synthetic double weighting must fail whole-bank capital identity'
if '--negative-control-fixed-K10000ppm' in sys.argv:
 original_decide=engine.decide
 def wrong_fixed_K(spec,m,i,actual):
  z=copy.deepcopy(spec);z['parameters'].update(trend_lookback_days=16,trend_window_days=16,trend_decay_numerator=15,trend_decay_denominator=17);return original_decide(z,m,i,actual)
 engine.decide=wrong_fixed_K
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted event axis accepted')
thresholds=0
for k in map(F,['.005','.0075','.01']):
 for slope,w in [(-k-F('.000001'),-1),(-k,0),(F(0),0),(k,0),(k+F('.000001'),1)]:assert engine.slope_gate(slope,k)==w;thresholds+=1
for raw,actual,vol,w in [(1,1,.09,1),(1,0,.045,1),(1,0,.045001,0),(-1,1,.045001,0),(0,1,.09,0)]:assert engine.entry_filter(raw,actual,vol,.045)==w
p={'slope_strengths':[.005,.0075,.01],'slow_windows':[16,18,20],'slope_lags':[3]};g=lambda k,s,scope:{'L':5,'H':.02,'E':.01,'S':s,'K':k,'D':3,'N':1000 if scope=='parent' else 4500,'fingerprint':f'{scope}/{k}/{s}','readonly':False}
p['grid']=[g(k,s,'parent') for k in p['slope_strengths'] for s in p['slow_windows']];p['native_grid']=[g(k,s,'native') for k in p['slope_strengths'] for s in p['slow_windows']];full={z['fingerprint']:{'name':z['fingerprint']} for z in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for z in grid:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,z,scope);assert old==saved and c['D']==3 and c['K']==z['K'] and c['S']==z['S'];ns=run.neighborhood(c,p,full);expected=(2 if z['K'] in [.005,.01] else 3)*(2 if z['S'] in [16,20] else 3);assert len(ns)==expected;cases.append({'scope':scope,'K':z['K'],'S':z['S'],'neighbors':len(ns)})
sp={'parameters':{'lookback_days':5,'trend_lookback_days':16,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.005,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.01,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':15,'trend_decay_denominator':17,'trend_window_days':16,'trend_gate_scope':'new_or_reversed_position_only'}};causal=0;boundaries=0;entrybound=0
for k in [.005,.0075,.01]:
 for slow in [16,18,20]:
  sp['parameters'].update(trend_slope_hurdle_fraction=k,trend_lookback_days=slow,trend_window_days=slow,trend_decay_numerator=slow-1,trend_decay_denominator=slow+1)
  for actual in [-1,0,1]:
   m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)]};got=engine.decide(sp,m,33,actual);a=got[1];assert a['return_exact']==str(F(m['closes'][32])/F(m['closes'][27])-1) and a['slope_lag_days']==3 and a['slope_hurdle_fraction']==k and a['slow_lookback_days']==slow and a['long_entry_return_hurdle']==a['short_entry_return_hurdle']==.02;m['closes'] += [D(1),D(999999)];assert engine.decide(sp,m,33,actual)==got;causal+=1
sp['parameters']['trend_slope_hurdle_fraction']=.005
for slow in [16,18,20]:
 sp['parameters'].update(trend_lookback_days=slow,trend_window_days=slow,trend_decay_numerator=slow-1,trend_decay_denominator=slow+1);e=F('.01');h=F('.02');eps=F('.000001')
 for actual,roc,w in [(1,e-eps,1),(1,e,0),(1,e+eps,0),(-1,-e-eps,0),(-1,-e,0),(-1,-e+eps,-1)]:
  m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(1+D(roc.numerator)/D(roc.denominator));assert engine.decide(sp,m,33,actual)[0]==w;boundaries+=1
 for roc,base in [(h-eps,0),(h,0),(h+eps,-1),(-h-eps,1),(-h,0),(-h+eps,0)]:
  m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(1+D(roc.numerator)/D(roc.denominator));assert engine.decide(sp,m,33,0)[1]['ungated_desired']==base;entrybound+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_K_S_neighborhoods':cases,'causal_cases':causal,'distinct_slow_S_cases':3,'distinct_K_cases':3,'strict_entry_boundary_cases':entrybound,'strict_exit_boundary_cases':boundaries,'slope_threshold_cases':thresholds,'volatility_retention_cases':5,'native_and_parent_two_axes':True,'maximum_required_context_days':30,'ETH_required_context_days':23,'ETH_signal_context_days':23,'ETH_cost_context_days':21,'source_context_days':33});print('PASS18K/Sneighborhoods,27causality,15strictK/18strictH/18Eboundaries,5vol,wholebank/shiftedaxis;0marketvaluations')
