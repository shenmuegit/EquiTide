"""Synthetic capital, joint H/F, causal price/funding, and strict threshold checks."""
import copy,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
from common import *
import engine,run
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48]);negative=any(x.startswith('--negative-control') for x in sys.argv)
if '--negative-control-double-weighting' in sys.argv:assert (.2*btc+.8*eth)[0]==18750,'Double weighting must fail actual whole-bank capital'
if '--negative-control-fixed-H200bp' in sys.argv:
 orig=engine.decide
 def wrong(sp,m,i,actual):
  s=copy.deepcopy(sp);s['parameters'].update(return_hurdle=.02,long_entry_return_hurdle=.02,short_entry_return_hurdle=.02);return orig(s,m,i,actual)
 engine.decide=wrong
if '--negative-control-future-funding' in sys.argv:engine.latest_funding=lambda events,sn:max(events,key=lambda e:e['settlement_ts']) if events else None
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,axis+1])
except AssertionError:pass
else:raise AssertionError('Shifted event axis accepted')
p={'entry_hurdles':[.0175,.02,.0225],'funding_caps':[0,.00005,None]};g=lambda h,f,sc:{'L':5,'H':h,'E':.0075,'F':f,'S':16,'K':.0075,'VC':.05,'D':3,'N':1000 if sc=='parent' else 4500,'fingerprint':f'{sc}/{h}/{f}','readonly':f is None}
p['grid']=[g(h,f,'parent') for h in p['entry_hurdles'] for f in p['funding_caps']];p['native_grid']=[g(h,f,'native') for h in p['entry_hurdles'] for f in p['funding_caps']];full={z['fingerprint']:{'name':z['fingerprint']} for z in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for z in grid:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,z,scope);assert old==saved and c['F']==z['F'] and c['E']==.0075;ns=run.neighborhood(c,p,full);expected=(2 if z['H']!=.02 else 3)*(3 if z['F']==.00005 else 2);assert len(ns)==expected;cases.append({'scope':scope,'H':z['H'],'F':z['F'],'neighbors':len(ns)})
sn=33*DAY;good={'settlement_ts':sn-8*HOUR,'available_ts':sn-7*HOUR,'realized_rate':D('-.00002'),'source_index':2};events=[good,{'settlement_ts':sn,'available_ts':sn+HOUR,'realized_rate':D('.9'),'source_index':3},{'settlement_ts':sn-13*HOUR,'available_ts':sn-12*HOUR,'realized_rate':D('.7'),'source_index':1}];assert engine.latest_funding(events,sn)==good
boundaries=0
for age,delay,w in [(HOUR,HOUR,True),(HOUR-1,0,False),(12*HOUR,HOUR,True),(12*HOUR+1,HOUR,False),(8*HOUR,9*HOUR,False),(8*HOUR,8*HOUR,True)]:
 e={**good,'settlement_ts':sn-age,'available_ts':sn-age+delay};assert (engine.latest_funding([e],sn) is not None)==w;boundaries+=1
fundcases=[]
for cap in [D('0'),D('.00005')]:
 for raw in [-1,0,1]:
  for actual in [-1,0,1]:
   for rate in [D('-.00005001'),D('-.00005'),D(0),D('.00005'),D('.00005001')]:
    ev={**good,'realized_rate':rate};want=0 if raw and raw!=actual and max(D(raw)*rate,D(0))>cap else raw;v,a=engine.funding_filter(raw,actual,ev,sn,cap);assert v==want and a['blocked']==bool(raw and raw!=actual and max(D(raw)*rate,D(0))>cap);fundcases.append((str(cap),raw,actual,str(rate),v))
   v,a=engine.funding_filter(raw,actual,None,sn,cap);assert v==(0 if raw and raw!=actual else raw)
sp={'parameters':{'lookback_days':5,'trend_lookback_days':16,'trend_slope_lag_days':3,'trend_slope_hurdle_fraction':.0075,'entry_volatility_window_days':10,'entry_volatility_ceiling':.05,'exit_buffer_fraction':.0075,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','trend_decay_numerator':15,'trend_decay_denominator':17,'trend_window_days':16,'trend_gate_scope':'new_or_reversed_position_only','entry_funding_outflow_cap':.00005}};causal=exits=entries=0
for h0 in ['.0175','.02','.0225']:
 sp['parameters'].update(return_hurdle=float(h0),long_entry_return_hurdle=float(h0),short_entry_return_hurdle=float(h0));e=F('.0075');h=F(h0);eps=F('.000001')
 def market(roc=None):
  closes=[D(100)+D(j%8)*D('.2') for j in range(33)] if roc is None else [D(100)]*33
  if roc is not None:closes[-1]=D(100)*(1+D(roc.numerator)/D(roc.denominator))
  return {'asset':'ETH','closes':closes,'frame':{'available_ts':{33*1440-1:sn}},'signal_funds':copy.deepcopy(events)}
 for actual in [-1,0,1]:
  m=market();got=engine.decide(sp,m,33,actual);assert got[1]['long_entry_return_hurdle']==float(h0);m['closes'] += [D(1),D(999999)];m['signal_funds'].append({'settlement_ts':sn+HOUR,'available_ts':sn+2*HOUR,'realized_rate':D('9999'),'source_index':4});assert engine.decide(sp,m,33,actual)==got;causal+=1
 for actual,roc,w in [(1,e-eps,1),(1,e,0),(1,e+eps,0),(-1,-e-eps,0),(-1,-e,0),(-1,-e+eps,-1)]:assert engine.decide(sp,market(roc),33,actual)[0]==w;exits+=1
 for roc,w in [(h-eps,0),(h,0),(h+eps,-1),(-h-eps,1),(-h,0),(-h+eps,0)]:assert engine.decide(sp,market(roc),33,0)[1]['ungated_desired']==w;entries+=1
for slope,w in [(-F('.007501'),-1),(-F('.0075'),0),(F(0),0),(F('.0075'),0),(F('.007501'),1)]:assert engine.slope_gate(slope,F('.0075'))==w
for raw,actual,vol,w in [(1,1,.09,1),(1,0,.05,1),(1,0,.050001,0),(-1,1,.050001,0),(0,1,.09,0)]:assert engine.entry_filter(raw,actual,vol,.05)==w
if not negative:put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'joint_H_F_neighborhoods':cases,'causal_cases':causal,'strict_entry_boundary_cases':entries,'strict_exit_boundary_cases':exits,'funding_age_and_availability_boundary_cases':boundaries,'funding_entry_retention_threshold_cases':len(fundcases),'missing_funding_cases':18,'future_price_and_funding_invariance':True,'native_and_parent_two_axes':True,'maximum_required_context_days':30,'ETH_required_context_days':21,'ETH_signal_context_days':19,'ETH_cost_context_days':21,'source_context_days':33})
print('PASS H/F18neighborhoods,strictH/E,causality/fundingage/availability/strictoutflow/samedirection/missing;0marketvaluations')
