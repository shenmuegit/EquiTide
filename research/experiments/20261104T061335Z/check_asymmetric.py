"""Synthetic S/E causality/equality, exact independent EWM kernel and axis/capital guards."""
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
p={'trend_windows':[16,24,32],'exit_buffers':[.00375,.005,.00625]};p['grid']=[{'L':5,'H':.02,'S':S,'E':E,'fingerprint':f'{S}/{E}','readonly':S==32 and E==.005} for S in p['trend_windows'] for E in p['exit_buffers']];p['native_grid']=p['grid'];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']};cases=[]
for scope in ['native','parent']:
 for g in p['grid']:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,g,scope);assert old==saved and c['S']==g['S'] and c['E']==g['E'];ns=run.neighborhood(c,p,full);expected=(2 if g['S'] in [16,32] else 3)*(2 if g['E'] in [.00375,.00625] else 3);assert len(ns)==expected;cases.append({'scope':scope,'S':g['S'],'E':g['E'],'neighbors':len(ns),'old_metadata_unchanged':True})
def expected(prices,S,E,actual):
 i=33;weights=[(S-1)**j*(S+1)**(S-1-j) for j in range(S)];mass=sum(weights);level=sum((F(prices[i-1-j])*weights[j] for j in range(S)),F(0))/mass;slow=F(prices[i-1])/level-1;r=F(prices[i-1])/F(prices[i-6])-1;h=F('.02');e=F(str(E));base=-1 if r>h else 1 if r<-h else actual if actual==1 and r<e or actual==-1 and r>-e else 0;gate=(slow>0)-(slow<0);raw=base if base==gate else 0;xs=[math.log(float(prices[j])/float(prices[j-1])) for j in range(23,33)];mean=math.fsum(xs)/10;sigma=math.sqrt(math.fsum((x-mean)**2 for x in xs)/9);return (0 if raw and raw!=actual and sigma>.045 else raw),level,r,slow,sigma
series=[[D(100)]*36,[D(90)+D(j)/2 for j in range(36)],[D(110)-D(j)/2 for j in range(36)]]
for direction in [1,-1]:
 q=[D(90 if direction==1 else 110)]*36;q[21:33]=[D(100)]*12;q[32]=D(100)*(1-D('.03')*direction);series.append(q)
toy=[D(100)]*36;toy[32]=D(200);series.append(toy);checks=0;window_checks=0
for S in [16,24,32]:
 for E in [.00375,.005,.00625]:
  sp={'parameters':{'lookback_days':5,'trend_lookback_days':S,'trend_window_days':S,'trend_decay_numerator':S-1,'trend_decay_denominator':S+1,'trend_estimator':'finite_normalized_exponentially_weighted_mean_level','entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':E,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02}}
  for prices in series:
   for actual in [-1,0,1]:
    want,level,r,slow,sigma=expected(prices,S,E,actual);w,a=run.engine.decide(sp,{'asset':'ETH','closes':prices},33,actual);assert w==want and F(a['slow_mean_exact'])==level and F(a['return_exact'])==r and F(a['slow_distance_exact'])==slow and abs(a['observed_sample_logvol']-sigma)<1e-12
    future=prices[:];future[33:]=[D(1000000)]*3;assert run.engine.decide(sp,{'asset':'ETH','closes':future},33,actual)==(w,a)
    past=prices[:];past[0]=D(1);assert run.engine.decide(sp,{'asset':'ETH','closes':past},33,actual)==(w,a);checks+=1
  for direction in [1,-1]:
   q=[D(90 if direction==1 else 110)]*36;q[21:33]=[D(100)]*12;q[32]=D(100)*(1-D('.02')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':q},33,0)[0]==0
   q[32]=D(100)*(1+D(str(E))*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':q},33,direction)[0]==0
   q[32]=D(100)*(1+(D(str(E))-D('.00001'))*direction);w,a=run.engine.decide(sp,{'asset':'ETH','closes':q},33,direction);assert w==expected(q,S,E,direction)[0]
  assert run.engine.decide(sp,{'asset':'ETH','closes':[D(100)]*36},33,1)[0]==0
  assert expected(toy,S,E,0)[1]!=sum(F(z) for z in toy[33-S:33])/S;window_checks+=1
assert run.engine.entry_filter(1,0,.046,.045)==0 and run.engine.entry_filter(1,0,.045,.045)==1 and run.engine.entry_filter(1,1,.06,.045)==1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'correct_parent_DD_pct':float(correctdd),'incorrect_mean_DD_pct':float(mean_dd),'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'grid_cases':cases,'independent_integer_weight_signal_cases':checks,'S_E_window_cases':window_checks,'future_and_outside_window_closes_ignored':True,'finite_EWM_distinguished_from_SMA':True,'actualstate_and_entry_exit_equalities_checked':True,'old_metadata_immutable':True});print('PASS syntheticS16/24/32,E3values,integerEWMkernel/causality/equalities,18neighborhoods andcapital/axisguards;0marketvaluations')
