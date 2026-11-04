"""Synthetic exact K/D gates, finite history, equality and full-bank axis checks."""
import copy,json,math,sys
from decimal import Decimal as DD
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
else:raise AssertionError('Shifted source events must be rejected')
import run
p={'slope_strengths':[.001,.002,.003],'slope_lags':[1,3,5]}
p['grid']=[{'L':5,'H':.02,'S':24,'K':K,'D':lag,'E':.005,'fingerprint':f'{K}/{lag}','readonly':False} for K in p['slope_strengths'] for lag in p['slope_lags']]
p['native_grid']=p['grid'];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']};cases=[]
for scope in ['native','parent']:
 for g in p['grid']:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,g,scope)
  assert old==saved and c['K']==g['K'] and c['D']==g['D'] and c['S']==24
  ns=run.neighborhood(c,p,full);expected=(2 if g['K'] in [.001,.003] else 3)*(2 if g['D'] in [1,5] else 3);assert len(ns)==expected
  cases.append({'scope':scope,'K':g['K'],'D':g['D'],'neighbors':len(ns)})
def expected(prices,lag,K,actual):
 i=33;S=24;weights=[23**j*25**(23-j) for j in range(24)];mass=sum(weights)
 level=sum((F(prices[i-1-j])*weights[j] for j in range(S)),F(0))/mass
 past=sum((F(prices[i-1-lag-j])*weights[j] for j in range(S)),F(0))/mass
 slope=level/past-1;r=F(prices[i-1])/F(prices[i-6])-1;h=F('.02');e=F('.005');k=F(str(K))
 base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<e or actual==-1 and r>-e else 0
 gate=1 if slope>k else -1 if slope<-k else 0;raw=base if base==gate else 0
 xs=[math.log(float(prices[j])/float(prices[j-1])) for j in range(23,33)];mean=math.fsum(xs)/10;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/9)
 return (0 if raw and raw!=actual and sigma>.045 else raw),level,past,r,slope,sigma
series=[[DD(100)]*36,[DD(80)+DD(j)/2 for j in range(36)],[DD(120)-DD(j)/2 for j in range(36)]]
for direction in [1,-1]:
 z=[DD(90 if direction==1 else 110)]*36;z[21:33]=[DD(100)]*12;z[32]=DD(100)*(1-DD('.03')*direction);series.append(z)
for step in ['.01','.02','.05','.10','.2']:
 z=[DD(100)+DD(j)*DD(step) for j in range(36)];series.append(z)
checks=distinct=equality=0
for K in [.001,.002,.003]:
 for lag in [1,3,5]:
  sp={'parameters':{'lookback_days':5,'trend_lookback_days':24,'trend_window_days':24,'trend_decay_numerator':23,'trend_decay_denominator':25,'trend_slope_lag_days':lag,'trend_slope_hurdle_fraction':K,'trend_estimator':'finite_normalized_exponentially_weighted_mean_slope','entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.005,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02}}
  for prices in series:
   for actual in [-1,0,1]:
    want,level,past,r,slope,sigma=expected(prices,lag,K,actual);w,a=run.engine.decide(sp,{'asset':'ETH','closes':prices},33,actual)
    assert w==want and F(a['slow_mean_exact'])==level and F(a['slow_reference_mean_exact'])==past and F(a['return_exact'])==r and F(a['slow_distance_exact'])==slope and a['slope_lag_days']==lag and a['slope_hurdle_fraction']==K and a['slow_distance_basis']=='finite_EWM_slope_ratio' and abs(a['observed_sample_logvol']-sigma)<1e-12
    future=prices[:];future[33:]=[DD(1000000)]*3;assert run.engine.decide(sp,{'asset':'ETH','closes':future},33,actual)==(w,a)
    first=33-24-lag;assert first>=4;older=prices[:];older[first-1]=DD(1);assert run.engine.decide(sp,{'asset':'ETH','closes':older},33,actual)==(w,a)
    distinct+=int(run.engine.slope_gate(slope,F(str(K)))!=((slope>0)-(slope<0)));checks+=1
  k=F(str(K));eps=F(1,10**12)
  for s,w in [(k,0),(-k,0),(k+eps,1),(-k-eps,-1),(k-eps,0),(-k+eps,0),(F(0),0)]:
   assert run.engine.slope_gate(s,k)==w;equality+=1
  for direction in [1,-1]:
   z=[DD(90 if direction==1 else 110)]*36;z[21:33]=[DD(100)]*12;z[32]=DD(100)*(1-DD('.02')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':z},33,0)[0]==0
   z[32]=DD(100)*(1+DD('.005')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':z},33,direction)[0]==0
   z[32]=DD(100)*(1+DD('.00499')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':z},33,direction)[0]==expected(z,lag,K,direction)[0]
assert distinct>0 and checks==270 and equality==63
assert run.engine.entry_filter(1,0,.046,.045)==0 and run.engine.entry_filter(1,0,.045,.045)==1 and run.engine.entry_filter(1,1,.06,.045)==1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'correct_parent_DD_pct':float(correctdd),'incorrect_mean_DD_pct':float(mean_dd),'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'grid_cases':cases,'independent_integer_weight_signal_cases':checks,'strength_vs_zero_strength_gate_distinct_cases':distinct,'strict_slope_equality_and_epsilon_cases':equality,'maximum_required_context_days':29,'source_context_days':33,'future_and_outside_required_window_closes_ignored':True,'strict_entry_exit_equalities_checked':True,'entry_volatility_filter_equality_checked':True})
print('PASS270 exact synthetic K/D cases,63 strength equality/epsilon cases,causal finite windows,18 neighborhoods and capital/axis guards;0 market valuation')
