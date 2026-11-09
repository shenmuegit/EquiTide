"""Synthetic H/E boundaries/causality and complete independent-bank capital checks."""
import copy,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
from common import *
import engine,run
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48])
if '--negative-control-double-weighting' in sys.argv:assert (.2*btc+.8*eth)[0]==18750,'Double weighting must fail actual whole-bank capital'
if '--negative-control-fixed-H200bp' in sys.argv:
 original=engine.decide
 def wrong(spec,m,i,actual):
  sp=copy.deepcopy(spec);sp['parameters'].update(return_hurdle=.02,long_entry_return_hurdle=.02,short_entry_return_hurdle=.02);return original(sp,m,i,actual)
 engine.decide=wrong
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted event axis accepted')
p={'entry_hurdles':[.0175,.02,.0225],'exit_buffers':[.00625,.0075,.00875]};g=lambda h,e,scope:{'L':5,'H':h,'E':e,'S':16,'K':.0075,'VC':.05,'D':3,'N':1000 if scope=='parent' else 4500,'fingerprint':f'{scope}/{h}/{e}','readonly':h==.02}
p['grid']=[g(h,e,'parent') for h in p['entry_hurdles'] for e in p['exit_buffers']];p['native_grid']=[g(h,e,'native') for h in p['entry_hurdles'] for e in p['exit_buffers']];full={z['fingerprint']:{'name':z['fingerprint']} for z in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for z in grid:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,z,scope);assert old==saved and c['K']==.0075 and c['L']==5 and c['H']==z['H'] and c['E']==z['E'];ns=run.neighborhood(c,p,full);expected=(2 if z['H'] in [.0175,.0225] else 3)*(2 if z['E'] in [.00625,.00875] else 3);assert len(ns)==expected;cases.append({'scope':scope,'H':z['H'],'E':z['E'],'neighbors':len(ns)})
sp={'parameters':{'lookback_days':5,'trend_lookback_days':16,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'entry_volatility_window_days':10,'entry_volatility_ceiling':.05,'exit_buffer_fraction':.0075,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':15,'trend_decay_denominator':17,'trend_window_days':16,'trend_gate_scope':'new_or_reversed_position_only'}};causal=exits=entries=thresholds=0
for h0 in ['.0175','.02','.0225']:
 for e0 in ['.00625','.0075','.00875']:
  sp['parameters'].update(return_hurdle=float(h0),long_entry_return_hurdle=float(h0),short_entry_return_hurdle=float(h0),exit_buffer_fraction=float(e0));e=F(e0);h=F(h0);eps=F('.000001')
  for actual in [-1,0,1]:
   m={'asset':'ETH','closes':[D(100)+D(j%8)*D('.2') for j in range(33)]};got=engine.decide(sp,m,33,actual);a=got[1];assert a['fast_lookback_days']==5 and a['return_exact']==str(F(m['closes'][32])/F(m['closes'][27])-1) and a['exit_buffer_fraction']==float(e0) and a['long_entry_return_hurdle']==a['short_entry_return_hurdle']==float(h0) and a['slope_hurdle_fraction']==.0075 and a['slow_lookback_days']==16;m['closes'] += [D(1),D(999999)];assert engine.decide(sp,m,33,actual)==got;causal+=1
  for actual,roc,w in [(1,e-eps,1),(1,e,0),(1,e+eps,0),(-1,-e-eps,0),(-1,-e,0),(-1,-e+eps,-1)]:
   m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(1+D(roc.numerator)/D(roc.denominator));assert engine.decide(sp,m,33,actual)[0]==w;exits+=1
  for roc,w in [(h-eps,0),(h,0),(h+eps,-1),(-h-eps,1),(-h,0),(-h+eps,0)]:
   m={'asset':'ETH','closes':[D(100)]*33};m['closes'][-1]=D(100)*(1+D(roc.numerator)/D(roc.denominator));assert engine.decide(sp,m,33,0)[1]['ungated_desired']==w;entries+=1
for slope,w in [(-F('.007501'),-1),(-F('.0075'),0),(F(0),0),(F('.0075'),0),(F('.007501'),1)]:assert engine.slope_gate(slope,F('.0075'))==w;thresholds+=1
for raw,actual,vol,w in [(1,1,.09,1),(1,0,.05,1),(1,0,.050001,0),(-1,1,.050001,0),(0,1,.09,0)]:assert engine.entry_filter(raw,actual,vol,.05)==w
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_H_E_neighborhoods':cases,'causal_cases':causal,'distinct_H_cases':3,'distinct_E_cases':3,'strict_entry_boundary_cases':entries,'strict_exit_boundary_cases':exits,'fixed_K_strict_threshold_cases':thresholds,'volatility_retention_cases':5,'native_and_parent_two_axes':True,'maximum_required_context_days':30,'ETH_required_context_days':21,'ETH_signal_context_days':19,'ETH_cost_context_days':21,'source_context_days':33})
print('PASS18H/Eneighborhoods,27causality,54strictH/54strictEboundaries,5fixedK/5vol,wholebank/shiftedaxis;0marketvaluations')
