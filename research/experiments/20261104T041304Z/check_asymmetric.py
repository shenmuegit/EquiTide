"""Synthetic exact finite EWM, causal/equality/entry-only-filter and capital/axis guards."""
import copy,json,math,sys
from decimal import Decimal as D
from fractions import Fraction as F
import numpy as np
from common import *
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48])
if '--negative-control-double-weighting' in sys.argv:
 wrong=.2*btc+.8*eth;assert wrong[0]==18750,'Synthetic double-weighting raw full banks must fail capital identity'
v=sum_aligned_full_banks([btc,eth],[axis,axis]);assert np.array_equal(v,np.array([18750.,18700.,19400.,19300.]))
correctdd=max(100*(1-v/np.maximum.accumulate(v)));mean_dd=(max(100*(1-btc/np.maximum.accumulate(btc)))+max(100*(1-eth/np.maximum.accumulate(eth))))/2;assert abs(correctdd-mean_dd)>1
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted source events must not be silently added')
import run
p={'lookbacks':[3,5,7],'hurdles':[.015,.02,.025]};p['grid']=[{'L':L,'H':H,'S':32,'E':.005,'fingerprint':f'{L}/{H}','readonly':False} for L in p['lookbacks'] for H in p['hurdles']];p['native_grid']=p['grid'];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']};cases=[]
for scope in ['native','parent']:
 for g in p['grid']:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,g,scope);assert old==saved;ng=run.neighborhood(c,p,full);expected=(2 if g['L'] in [3,7] else 3)*(2 if g['H'] in [.015,.025] else 3);assert len(ng)==expected;cases.append({'scope':scope,'L':g['L'],'H':g['H'],'neighbors':len(ng)})
# Independent integer kernel: no powers of Fraction and no call to engine's mean implementation.
def expected(prices,L,H,actual):
 i=33;weights=[31**j*33**(31-j) for j in range(32)];mass=sum(weights);num=sum((F(prices[i-1-j])*weights[j] for j in range(32)),F(0));level=num/mass;slow=F(prices[i-1])/level-1;r=F(prices[i-1])/F(prices[i-1-L])-1;h=F(str(H));e=F('.005');base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<e or actual==-1 and r>-e else 0;gate=(slow>0)-(slow<0);raw=base if base==gate else 0;xs=[math.log(float(prices[j])/float(prices[j-1])) for j in range(23,33)];mean=math.fsum(xs)/10;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/9);return (0 if raw and raw!=actual and sigma>.045 else raw),level,r,slow,sigma
series=[[D(100)]*36,[D(90)+D(j)/2 for j in range(36)],[D(110)-D(j)/2 for j in range(36)]]
for direction in [1,-1]:
 q=[D(90 if direction==1 else 110)]*36;q[21:33]=[D(100)]*12;q[32]=D(100)*(1-D('.03')*direction);series.append(q)
toy=[D(100)]*36;toy[32]=D(200);series.append(toy);checks=0
for L in [3,5,7]:
 for H in [.015,.02,.025]:
  sp={'parameters':{'lookback_days':L,'trend_lookback_days':32,'trend_window_days':32,'trend_decay_numerator':31,'trend_decay_denominator':33,'trend_estimator':'finite_normalized_exponentially_weighted_mean_level','entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.005,'return_hurdle':H,'long_entry_return_hurdle':H,'short_entry_return_hurdle':H}}
  for prices in series:
   for actual in [-1,0,1]:
    want,level,r,slow,sigma=expected(prices,L,H,actual);w,a=run.engine.decide(sp,{'asset':'ETH','closes':prices},33,actual);assert w==want and F(a['slow_mean_exact'])==level and F(a['return_exact'])==r and F(a['slow_distance_exact'])==slow and abs(a['observed_sample_logvol']-sigma)<1e-12
    future=prices[:];future[33:]=[D(1000000)]*3;assert run.engine.decide(sp,{'asset':'ETH','closes':future},33,actual)==(w,a);checks+=1
  for direction in [1,-1]:
   q=[D(90 if direction==1 else 110)]*36;q[21:33]=[D(100)]*12;q[32]=D(100)*(1-D(str(H))*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':q},33,0)[0]==0
   q[32]=D(100)*(1+D('.005')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':q},33,direction)[0]==0
   q[32]=D(100)*(1+D('.00499')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':q},33,direction)[0]==direction
  assert run.engine.decide(sp,{'asset':'ETH','closes':[D(100)]*36},33,1)[0]==0
assert expected(toy,3,.02,0)[1]!=sum(F(x) for x in toy[1:33])/32
assert run.engine.entry_filter(1,0,.046,.045)==0 and run.engine.entry_filter(1,0,.045,.045)==1 and run.engine.entry_filter(1,1,.06,.045)==1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'correct_parent_DD_pct':float(correctdd),'incorrect_mean_DD_pct':float(mean_dd),'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'grid_cases':cases,'independent_integer_weight_signal_cases':checks,'finite_EWM32_exact_last32_complete_closes':True,'finite_EWM_distinguished_from_SMA':True,'future_closes_ignored':True,'both_directions_actualstate_and_entry_exit_equalities_checked':True,'entry_only_volatility_filter_equality_checked':True});print('PASS synthetic finiteEWM integerkernel,causality/equalities/nativeentryfilter,18neighborhoods andrawcapital/DD/axisguards;0marketvaluations')
