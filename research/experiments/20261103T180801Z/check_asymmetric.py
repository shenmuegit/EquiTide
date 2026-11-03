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
p={'slow_windows':[24,28,32],'exit_buffers':[.00375,.005,.00625]};p['grid']=[{'L':4,'H':.02,'S':S,'E':E,'readonly':False,'fingerprint':f'{S}/{E}'} for S in p['slow_windows'] for E in p['exit_buffers']];p['native_grid']=p['grid'];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']};cases=[]
for scope in ['native','parent']:
 for g in p['grid']:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,g,scope);assert old==saved and c['S']==g['S'] and c['E']==g['E'] and c['L']==4 and c['H']==.02;ns=run.neighborhood(c,p,full);expected=(2 if g['S'] in [24,32] else 3)*(2 if g['E'] in [.00375,.00625] else 3);assert len(ns)==expected;cases.append({'scope':scope,'S':g['S'],'E':g['E'],'neighbors':len(ns),'old_metadata_unchanged':True})
from decimal import Decimal as D
from fractions import Fraction as F
for S in [24,28,32]:
 for E in [.00375,.005,.00625]:
  sp={'parameters':{'lookback_days':4,'trend_lookback_days':S,'trend_estimator':'simple_moving_average_level','entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':E,'return_hurdle':.02,'long_entry_return_hurdle':.02,'short_entry_return_hurdle':.02}}
  prices=[D(100)]*36;prices[1:9]=[D(80)]*8;prices[28]=D(102);prices[32]=D(98);w,audit=run.engine.decide(sp,{'asset':'ETH','closes':prices},33,0);assert w==(0 if S==24 else 1)
  mean=sum((F(z) for z in prices[33-S:33]),F(0))/S;assert audit['slow_mean_exact']==str(mean) and audit['slow_distance_exact']==str(F(prices[32])/mean-1)
  future=prices.copy();future[33:]=[D(1000000)]*3;assert run.engine.decide(sp,{'asset':'ETH','closes':future},33,0)==(w,audit)
  for direction in [1,-1]:
   prices=[D(90 if direction==1 else 110)]*36;prices[21:33]=[D(100)]*12;prices[32]=D(100)*(D(1)-D('.03')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':prices},33,0)[0]==direction
   prices[32]=D(100)*(D(1)-D('.02')*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':prices},33,0)[0]==0
   prices[32]=D(100)*(D(1)+D(str(E))*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':prices},33,direction)[0]==0
   prices[32]=D(100)*(D(1)+(D(str(E))-D('.00001'))*direction);assert run.engine.decide(sp,{'asset':'ETH','closes':prices},33,direction)[0]==direction
  flat=[D(100)]*36;assert run.engine.decide(sp,{'asset':'ETH','closes':flat},33,1)[0]==0
  # Fast long signal and ROCslow gate conflict, while SMAlevel agrees: rules are observably distinct.
  prices=[D(90)]*36;prices[21:33]=[D(100)]*12;prices[32]=D(97);prices[32-S]=D(99)
  wanted,audit=run.engine.decide(sp,{'asset':'ETH','closes':prices},33,0);assert wanted==1 and F(prices[32])/F(prices[32-S])-1<0 and F(audit['slow_distance_exact'])>0
assert run.engine.entry_filter(1,0,.046,.045)==0 and run.engine.entry_filter(1,0,.045,.045)==1 and run.engine.entry_filter(1,1,.06,.045)==1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'correct_toy_return_pct':expected_return,'incorrect_mean_return_pct':mean_return,'correct_parent_DD_pct':float(correctdd),'incorrect_mean_DD_pct':float(mean_dd),'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'grid_cases':cases,'synthetic_future_closes_ignored':True,'SMA24_vs_SMA28_SMA32_distinguished':True,'SMAlevel_distinguished_from_ROC_endpoint':True,'SMA_uses_exact_last_S_completed_closes_including_latest':True,'strict_symmetric_entry_equality_stays_flat':True,'both_reversal_directions_checked':True,'strict_exit_equality_exits_and_inside_retains':True,'flat_SMA_gate_closes':True,'entry_only_volatility_filter_equality_checked':True});print('PASS rawbank capital/return/DD,misalignedaxis rejection,18S/E neighborhoods,SMAspan/equality/causality/reversal logic;no actual market valuation')
