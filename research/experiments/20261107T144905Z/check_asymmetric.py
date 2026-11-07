"""Synthetic hysteresis boundaries, future invariance, grid and full-bank checks."""
import copy,itertools,sys
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
p={'BTC_lookbacks':[28,29,30],'BTC_exit_buffers':[.01],'BTC_hurdles':[.0275,.03,.0325]};cases=[];boundary=0;future=0
for scope in ['native','parent']:
 p['native_grid']=[{'L':l,'H':h,'E':.01,'S':None,'K':None,'D':None,'N':1000,'readonly':False,'fingerprint':f'{scope}/{l}/{h}'} for l,h in itertools.product(p['BTC_lookbacks'],p['BTC_hurdles'])];p['grid']=p['native_grid'];full={g['fingerprint']:g for g in p['grid']}
 for g in p['grid']:
  original={'criteria':{'old':False},'sensitivity':{'old':7}};before=copy.deepcopy(original);c=run.current_grid_row(original,g,scope);assert original==before;ns=run.neighborhood(c,p,full);expected=(2 if g['L'] in [28,30] else 3)*(2 if g['H'] in [.0275,.0325] else 3);assert len(ns)==expected;cases.append({'scope':scope,'L':g['L'],'H':g['H'],'E':g['E'],'neighbors':len(ns)})
for l,h in itertools.product(p['BTC_lookbacks'],p['BTC_hurdles']):
 e=.01;ee,hh,eps=F(str(e)),F(str(h)),F('.000001')
 for ret in [-hh-eps,-hh,-hh+eps,-ee-eps,-ee,-ee+eps,F(0),ee-eps,ee,ee+eps,hh-eps,hh,hh+eps]:
  for actual in [-1,0,1]:
   sp={'parameters':{'lookback_days':l,'return_hurdle':h,'exit_buffer_fraction':e}};cls=[D(100)]*33;cls[-1]=D(100)*(D(1)+D(ret.numerator)/D(ret.denominator));m={'asset':'BTC','closes':cls};wanted,audit=engine.decide(sp,m,33,actual);rr=F(cls[-1])/F(cls[32-l])-1;expected=1 if rr>hh else -1 if rr<-hh else 1 if actual==1 and rr>-ee else -1 if actual==-1 and rr<ee else 0;assert wanted==expected and audit=={'kind':'BTC_momentum','return_exact':str(rr)};boundary+=1;m['closes']+=[D(1),D(999999)];assert engine.decide(sp,m,33,actual)==(wanted,audit);future+=1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'joint_L_H_neighborhoods':cases,'strict_entry_exit_hysteresis_boundary_cases':boundary,'future_append_invariance_cases':future,'maximum_required_context_days':31,'source_context_days':33});print(f'PASS{len(cases)}L/Hneighborhoods,{boundary}strictboundaries/{future}futureinvariance,capital+axisguards;0marketvaluations')
