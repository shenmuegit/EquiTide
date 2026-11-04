"""Synthetic native LOT/nonlinear-impact, original signal and joint N/D conservation guards."""
import ast,copy,sys
from decimal import Decimal as D,ROUND_FLOOR
from common import *
import engine,run
from portfolio import sum_aligned_full_banks
import numpy as np
btc=np.array([3750.,4000.,3800.,3900.]);eth=np.array([15000.,14700.,15600.,15400.]);axis=np.array([0,16,32,48])
if '--negative-control-double-weighting' in sys.argv:
 wrong=.2*btc+.8*eth;assert wrong[0]==18750,'Synthetic double-weighting raw full banks must fail capital identity'
v=sum_aligned_full_banks([btc,eth],[axis,axis]);assert np.array_equal(v,np.array([18750.,18700.,19400.,19300.]))
try:sum_aligned_full_banks([btc,eth],[axis,np.array([0,16,33,48])])
except AssertionError:pass
else:raise AssertionError('Shifted source events must be rejected')
q=lambda N:(D(N)/D(70000)/D('.001')).to_integral_value(rounding=ROUND_FLOOR)*D('.001');checks=[];costs={}
for N,w in [(500,'.007'),(625,'.008'),(750,'.010')]:
 qty=q(N);assert qty==D(w) and qty*70000<=N<(qty+D('.001'))*70000
 for k in [1,2,3]:
  state={'cash':'3750','signed_units':'0','entry_price':'0','entry_reference':'0'};meta={'lot_size':'.001','tick_size':'.1','min_notional':'50'};after,t=engine.trade(state,qty,D(70000),D(20000000),D('.03'),meta,k,True);assert t['status']=='filled' and D(after['signed_units'])==qty and D(t['quantity'])==qty and D(t['participation'])==qty*70000/D(20000000)
  assert abs(D(t['cost_parts']['impact'])-qty*D(70000)*D('.5')*D('.03')*(qty*70000/D(20000000)).sqrt()*k)<D('1e-24');costs[N,k]=D(t['cost_usdt']);checks.append({'N':N,'cost_multiplier':k,'expected_quantity':str(qty),'actual_cost_usdt':str(costs[N,k]),'actual_participation':t['participation']})
assert q(750)!=q(625)*D(750)/D(625) and costs[750,1]!=costs[625,1]*D(750)/D(625)
# Actual inline sizing operation unchanged byte-for-byte; independently replayed for every real fill in audit.py.
assert 'quantity=(notional/m[\'closes\'][ref-1]/lot).to_integral_value(rounding=ROUND_FLOOR)*lot' in (R/'engine.py').read_text()
policy=[]
for N in [500,625,750]:
 sp={'parameters':{'lookback_days':31,'return_hurdle':.04,'exit_buffer_fraction':.01,'fixed_entry_notional_usdt':N}}
 for rr,actual,w in [(D('.04'),0,0),(D('.040001'),0,1),(-D('.04'),0,0),(-D('.040001'),0,-1),(-D('.01'),1,0),(-D('.009999'),1,1),(D('.01'),-1,0),(D('.009999'),-1,-1)]:
  m={'asset':'BTC','closes':[D(100)]*32+[100*(1+rr)]};wanted,a=engine.decide(sp,m,33,actual);assert wanted==w;m['closes'].extend([D(1),D(99999)]);assert engine.decide(sp,m,33,actual)==(wanted,a);policy.append({'N':N,'return':str(rr),'actual':actual,'expected':w,'future_prices_ignored':True})
p={'entry_notionals':[500,625,750],'slope_strengths':[.00025,.0005,.00075]};p['grid']=[{'L':5,'H':.02,'E':.005,'S':24,'K':kk,'D':1,'N':n,'readonly':False,'fingerprint':f'{n}/{kk}'} for n in p['entry_notionals'] for kk in p['slope_strengths']];p['native_grid']=[{'L':31,'H':.04,'E':.01,'S':None,'K':None,'D':None,'N':n,'readonly':False,'fingerprint':f'BTC/{n}'} for n in p['entry_notionals']];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']+p['native_grid']};cases=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for g in grid:
  original={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(original);c=run.current_grid_row(original,g,scope);assert original==saved and c['N']==g['N'];ns=run.neighborhood(c,p,full);expected=(2 if g['N'] in [500,750] else 3)*(1 if scope=='native' else 2 if g['K'] in [.00025,.00075] else 3);assert len(ns)==expected;cases.append({'scope':scope,'N':g['N'],'K':g['K'],'neighbors':len(ns)})
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'raw_weights':[1,1],'fixed_capital':18750,'shifted_event_axis_rejected':True,'double_weighted_capital_rejected':True,'quantity_and_nonlinear_cost_fixtures':checks,'strict_original_BTC_policy_fixtures':policy,'grid_cases':cases,'old_NAV_linear_scaling_explicitly_falsified':True,'native_1axis_parent_2axes_disclosed':True,'maximum_required_context_days':32,'source_context_days':33});print('PASS9 LOT/cost,24 BTC causal boundary,12 N/K neighborhoods plus fullbank capital/axis guards;0 market valuation')
