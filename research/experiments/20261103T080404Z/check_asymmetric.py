"""Synthetic axis mismatch, raw fullbank aggregation and non-average drawdown guards."""
import copy,sys
import numpy as np
from common import *
from portfolio import sum_aligned_full_banks
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48]);weights=[1,1]
if '--legacy-slow-range' in sys.argv:
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
p={'lookbacks':[3,4,5],'slow_windows':[27,28,29]};p['grid']=[{'L':L,'S':S,'readonly':S==28,'fingerprint':f'{L}/{S}'} for L in p['lookbacks'] for S in p['slow_windows']];p['native_grid']=p['grid'];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']};cases=[]
for scope in ['native','parent']:
 for g in p['grid']:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);c=run.current_grid_row(old,g,scope);assert old==saved and c['S']==g['S'];ns=run.neighborhood(c,p,full);expected=(2 if g['L'] in [3,5] else 3)*(2 if g['S'] in [27,29] else 3);assert len(ns)==expected;cases.append({'scope':scope,'L':g['L'],'S':g['S'],'neighbors':len(ns),'old_metadata_unchanged':True})
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'correct_toy_return_pct':expected_return,'incorrect_mean_return_pct':mean_return,'correct_parent_DD_pct':float(correctdd),'incorrect_mean_DD_pct':float(mean_dd),'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'grid_cases':cases});print('PASS rawbank capital/return/DD,misaligned-axis rejection,18L/Sneighborhood cases;no actual source simulation')
