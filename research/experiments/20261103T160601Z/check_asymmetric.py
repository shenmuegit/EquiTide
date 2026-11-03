"""Synthetic axis mismatch, raw fullbank aggregation and non-average drawdown guards."""
import copy,sys
import numpy as np
from common import *
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48]);weights=[1,1]
if '--negative-control-double-weighting' in sys.argv:
 wrong=.2*btc+.8*eth
 assert wrong[0]==18750,'Synthetic double-weighting raw full banks must fail capital identity'
v=sum_aligned_full_banks([btc,eth],[axis,axis]);assert np.array_equal(v,np.array([18750.,18700.,19400.,19300.])) and v[0]==18750
expected_return=100*(19300/18750-1);assert abs(100*(v[-1]/v[0]-1)-expected_return)<1e-12
mean_return=(100*(btc[-1]/btc[0]-1)+100*(eth[-1]/eth[0]-1))/2;assert abs(expected_return-mean_return)>.1
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('One shifted source event must be rejected,not silently summed')
correctdd=max(100*(1-v/np.maximum.accumulate(v)));mean_dd=(max(100*(1-btc/np.maximum.accumulate(btc)))+max(100*(1-eth/np.maximum.accumulate(eth))))/2;assert abs(correctdd-mean_dd)>1
import run
p={'lookbacks':[7,14,21],'hurdles':[.01,.02,.03]};p['grid']=[{'L':L,'H':H,'S':28,'E':.005,'readonly':False,'fingerprint':f'{L}/{H}'} for L in p['lookbacks'] for H in p['hurdles']];p['native_grid']=p['grid'];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']};cases=[]
for scope in ['native','parent']:
 for g in p['grid']:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,g,scope);assert old==saved and c['L']==g['L'] and c['H']==g['H'];ns=run.neighborhood(c,p,full);expected=(2 if g['L'] in [7,21] else 3)*(2 if g['H'] in [.01,.03] else 3);assert len(ns)==expected;cases.append({'scope':scope,'L':g['L'],'H':g['H'],'neighbors':len(ns),'old_metadata_unchanged':True})
from decimal import Decimal as D
for L in [7,14,21]:
 for H in [.01,.02,.03]:
  sp={'parameters':{'lookback_days':L,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.005,'return_hurdle':H,'long_entry_return_hurdle':H}}
  prices=[D(100)]*36;prices[4]=D(99);prices[25]=D(100);prices[18]=D(105);prices[11]=D(106);prices[32]=D(104);w,audit=run.engine.decide(sp,{'asset':'ETH','closes':prices},33,0);assert w==(1 if L==7 else 0)
  future=prices.copy();future[33:]=[D(1000000)]*3;assert run.engine.decide(sp,{'asset':'ETH','closes':future},33,0)==(w,audit)
  for direction in [1,-1]:
   prices=[D(100)]*36;prices[4]=D(98 if direction==1 else 102);prices[32]=D(100)*(D(1)+D('.04')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':prices},33,0)[0]==direction
   prices[32]=D(100)*(D(1)+D(str(H))*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':prices},33,0)[0]==0
   prices[32]=D(100)*(D(1)-D('.005')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':prices},33,direction)[0]==0
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'correct_toy_return_pct':expected_return,'incorrect_mean_return_pct':mean_return,'correct_parent_DD_pct':float(correctdd),'incorrect_mean_DD_pct':float(mean_dd),'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'grid_cases':cases,'synthetic_future_closes_ignored':True,'synthetic_L7_vs_L14_L21_distinguished':True,'strict_symmetric_entry_equality_stays_flat':True,'both_momentum_directions_checked':True,'strict_exit_equality_exits':True});print('PASS rawbank capital/return/DD,misaligned-axis rejection,18L/Hneighborhood cases;no actual source simulation')
