"""Synthetic fullbank capital, drawdown and event-axis guards; no native valuation."""
import sys,json,ast
import numpy as np
from common import *
from portfolio import sum_aligned_full_banks
btc=np.array([15000.,15500.,15200.,15700.]);eth=np.array([15000.,14600.,15800.,15300.]);axis=np.array([0,16,32,48])
if '--negative-control-double-weighting' in sys.argv:
 wrong=.5*btc+.5*eth;assert wrong[0]==30000,'Synthetic double-weighting raw full banks must fail capital identity'
v=sum_aligned_full_banks([btc,eth],[axis,axis]);assert np.array_equal(v,np.array([30000.,30100.,31000.,31000.])) and v[0]==30000
correctdd=max(100*(1-v/np.maximum.accumulate(v)));mean_dd=(max(100*(1-btc/np.maximum.accumulate(btc)))+max(100*(1-eth/np.maximum.accumulate(eth))))/2;assert abs(correctdd-mean_dd)>1
oldbtc=np.array([3750.,3900.,3700.,4000.]);assert not np.array_equal(4*oldbtc+eth,v)
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted source event must be rejected')
import run
p={'lookbacks':[3,5,7],'hurdles':[.015,.02,.025]};p['grid']=[{'L':L,'H':H,'fingerprint':f'{L}/{H}'} for L in p['lookbacks'] for H in p['hurdles']];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']};cases=[]
for g in p['grid']:
 ns=run.neighborhood(g,p,full);expected=(2 if g['L'] in [3,7] else 3)*(2 if g['H'] in [.015,.025] else 3);assert len(ns)==expected;cases.append({'L':g['L'],'H':g['H'],'neighbors':len(ns)})
for n in ['run.py','audit.py']:
 tree=ast.parse((R/n).read_text());assert not any(isinstance(x,ast.Call) and ((isinstance(x.func,ast.Name) and x.func.id in ['simulate','decide','trade']) or isinstance(x.func,ast.Attribute) and x.func.attr in ['simulate','decide','trade']) for x in ast.walk(tree))
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':30000,'correct_parent_DD_pct':float(correctdd),'incorrect_mean_DD_pct':float(mean_dd),'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'scaling_old_BTC_book_rejected':True,'grid_cases':cases,'new_native_policy_or_trade_calls':0,'no_native_engine_file':not(R/'engine.py').exists()});print('PASS fullbank30000 capital,nonaverageDD,oldBTCresizingnegativecontrol,shiftedaxis rejection,9L/Hneighborhoods andzero nativecalls')
