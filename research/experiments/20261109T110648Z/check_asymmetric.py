"""Synthetic K/VC identities, strict cap/entry/exit boundaries, causality and whole-bank checks."""
import copy,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
from common import *
import engine,run
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48])
if '--negative-control-double-weighting' in sys.argv:assert (.2*btc+.8*eth)[0]==18750,'Synthetic double weighting must fail whole-bank capital identity'
if '--negative-control-fixed-VC45000ppm' in sys.argv:
 original_decide=engine.decide
 def wrong_fixed_cap(spec,m,i,actual):
  z=copy.deepcopy(spec);z['parameters']['entry_volatility_ceiling']=.045;return original_decide(z,m,i,actual)
 engine.decide=wrong_fixed_cap
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted event axis accepted')
thresholds=volcases=0
for k in map(F,['.005','.0075','.01']):
 for slope,w in [(-k-F('.000001'),-1),(-k,0),(F(0),0),(k,0),(k+F('.000001'),1)]:assert engine.slope_gate(slope,k)==w;thresholds+=1
for cap in [.045,.05,.055]:
 for raw,actual,vol,w in [(1,1,.09,1),(1,0,cap,1),(1,0,cap+.000001,0),(-1,1,cap+.000001,0),(0,1,.09,0)]:assert engine.entry_filter(raw,actual,vol,cap)==w;volcases+=1
p={'slope_strengths':[.005,.0075,.01],'volatility_ceilings':[.045,.05,.055],'exit_buffers':[.01],'slow_windows':[16],'slope_lags':[3]};g=lambda k,cap,scope:{'L':5,'H':.02,'E':.01,'S':16,'K':k,'VC':cap,'D':3,'N':1000 if scope=='parent' else 4500,'fingerprint':f'{scope}/{k}/{cap}','readonly':False}
p['grid']=[g(k,cap,'parent') for k in p['slope_strengths'] for cap in p['volatility_ceilings']];p['native_grid']=[g(k,cap,'native') for k in p['slope_strengths'] for cap in p['volatility_ceilings']];full={z['fingerprint']:{'name':z['fingerprint']} for z in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for z in grid:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,z,scope);assert old==saved and c['K']==z['K'] and c['VC']==z['VC'] and c['E']==.01 and c['S']==16;ns=run.neighborhood(c,p,full);expected=(2 if z['K'] in [.005,.01] else 3)*(2 if z['VC'] in [.045,.055] else 3);assert len(ns)==expected;cases.append({'scope':scope,'K':z['K'],'VC':z['VC'],'neighbors':len(ns)})
sp={'parameters':{'lookback_days':5,'trend_lookback_days':16,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.005,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.01,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':15,'trend_decay_denominator':17,'trend_window_days':16,'trend_gate_scope':'new_or_reversed_position_only'}};causal=boundaries=entrybound=0
for k in [.005,.0075,.01]:
 for cap in [.045,.05,.055]:
  sp['parameters'].update(trend_slope_hurdle_fraction=k,entry_volatility_ceiling=cap)
  for actual in [-1,0,1]:
   m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)]};got=engine.decide(sp,m,33,actual);a=got[1];assert a['return_exact']==str(F(m['closes'][32])/F(m['closes'][27])-1) and a['slope_lag_days']==3 and a['slope_hurdle_fraction']==k and a['slow_lookback_days']==16 and a['exit_buffer_fraction']==.01 and a['entry_volatility_ceiling']==cap and a['long_entry_return_hurdle']==a['short_entry_return_hurdle']==.02;m['closes'] += [D(1),D(999999)];assert engine.decide(sp,m,33,actual)==got;causal+=1
sp['parameters']['trend_slope_hurdle_fraction']=.005
for cap in [.045,.05,.055]:
 sp['parameters']['entry_volatility_ceiling']=cap;e=F('.01');h=F('.02');eps=F('.000001')
 for actual,roc,w in [(1,e-eps,1),(1,e,0),(1,e+eps,0),(-1,-e-eps,0),(-1,-e,0),(-1,-e+eps,-1)]:
  m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(1+D(roc.numerator)/D(roc.denominator));assert engine.decide(sp,m,33,actual)[0]==w;boundaries+=1
 for roc,base in [(h-eps,0),(h,0),(h+eps,-1),(-h-eps,1),(-h,0),(-h+eps,0)]:
  m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(1+D(roc.numerator)/D(roc.denominator));assert engine.decide(sp,m,33,0)[1]['ungated_desired']==base;entrybound+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_K_VC_neighborhoods':cases,'causal_cases':causal,'distinct_VC_cases':3,'distinct_K_cases':3,'strict_entry_boundary_cases':entrybound,'strict_exit_boundary_cases':boundaries,'slope_threshold_cases':thresholds,'volatility_retention_cases':volcases,'native_and_parent_two_axes':True,'maximum_required_context_days':30,'ETH_required_context_days':21,'ETH_signal_context_days':19,'ETH_cost_context_days':21,'source_context_days':33});print('PASS18K/VCneighborhoods,27causality,15strictK/18H/18Eboundaries,15volcap/retention/reversalchecks,wholebank/shiftedaxis;0marketvaluations')
