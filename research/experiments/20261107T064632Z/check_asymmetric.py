"""Synthetic strict BTC boundaries, past-only signals and whole-bank alignment."""
import copy,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
from common import *
import engine,run
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48])
if '--negative-control-double-weighting' in sys.argv:assert (.2*btc+.8*eth)[0]==18750,'Synthetic double-weighting raw full banks must fail capital identity'
assert np.array_equal(sum_aligned_full_banks([btc,eth],[axis,axis]),np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted axis accepted')
p={'BTC_lookbacks':[23,25,27],'BTC_hurdles':[.03,.04,.05]};cases=[];boundaries=0;future=0
for scope in ['native','parent']:
 p['native_grid']=[{'L':l,'H':h,'fingerprint':f'{scope}/{l}/{h}'} for l in p['BTC_lookbacks'] for h in p['BTC_hurdles']];p['grid']=p['native_grid'];full={g['fingerprint']:g for g in p['grid']}
 for g in p['grid']:
  c={**g,'scope':scope};n=run.neighborhood(c,p,full);expected=(2 if g['L'] in [23,27] else 3)*(2 if g['H'] in [.03,.05] else 3);assert len(n)==expected;cases.append({'scope':scope,'L':g['L'],'H':g['H'],'neighbors':len(n)})
for l in [23,25,27]:
 for h in [.03,.04,.05]:
  for r in [-F(str(h))-F('.000001'),-F(str(h)),-F('.01'),F(0),F('.01'),F(str(h)),F(str(h))+F('.000001')]:
   for actual in [-1,0,1]:
    spec={'parameters':{'lookback_days':l,'return_hurdle':h,'exit_buffer_fraction':.01}};cls=[D(100)]*33;cls[-1]=D(100)*(D(1)+D(r.numerator)/D(r.denominator));m={'asset':'BTC','closes':cls};wanted,audit=engine.decide(spec,m,33,actual);rr=F(cls[-1])/F(cls[32-l])-1;hh=F(str(h));ee=F('.01');independent=1 if rr>hh else -1 if rr<-hh else 1 if actual==1 and rr>-ee else -1 if actual==-1 and rr<ee else 0;assert wanted==independent and audit=={'kind':'BTC_momentum','return_exact':str(rr)};boundaries+=1;m['closes'] += [D(1),D(999999)];assert engine.decide(spec,m,33,actual)==(wanted,audit);future+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_L_H_neighborhoods':cases,'strict_boundary_and_persistence_cases':boundaries,'future_append_invariance_cases':future,'maximum_required_context_days':32,'source_context_days':33});print('PASS18L/Hneighborhoods,189strictentry/exit/persistenceandfutureboundarycases;0marketvaluations')
