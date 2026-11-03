"""Synthetic quantity discontinuity, prior-price causality, costs and L/N neighborhoods."""
import copy,sys
from decimal import Decimal as D,ROUND_FLOOR
from common import *
import engine
if '--legacy-slow-range' in sys.argv:engine=module(ROOT/'research/experiments/20261103T020232Z/engine.py','old_without_explicit_sizing_guard')
try:q=engine.entry_quantity(D(250),D(80000),D('.001'))
except AttributeError as e:raise AssertionError('Explicit prior-close LOT sizing guard required for new BTC entry-size direction') from e
assert q==D('.003')
checks=[];costs={}
for N,expected in [(250,'.003'),(375,'.004'),(500,'.006')]:
 q=engine.entry_quantity(D(N),D(80000),D('.001'));assert q==D(expected)
 assert q*D(80000)<=N<(q+D('.001'))*D(80000)
 for future_open in [D(60000),D(120000)]:assert engine.entry_quantity(D(N),D(80000),D('.001'))==q
 for k in [1,2,3]:
  state={'cash':'3750','signed_units':'0','entry_price':'0','entry_reference':'0'};meta={'lot_size':'.001','tick_size':'.1','min_notional':'50'}
  after,receipt=core.trade(state,q,D(80000),D(20000000),D('.03'),meta,k,True);assert receipt['status']=='filled' and D(after['signed_units'])==q and D(receipt['quantity'])==q and D(receipt['participation'])==q*D(80000)/D(20000000)
  assert abs(D(receipt['cost_parts']['impact'])-q*D(80000)*D('.5')*D('.03')*(q*D(80000)/D(20000000)).sqrt()*k)<D('1e-24')
  costs[N,k]=D(receipt['cost_usdt']);checks.append({'N':N,'cost_multiplier':k,'expected_quantity':str(q),'actual_cost':str(costs[N,k]),'actual_participation':receipt['participation']})
assert engine.entry_quantity(D(250),D(80000),D('.001'))!=engine.entry_quantity(D(375),D(80000),D('.001'))*D(250)/D(375)
assert engine.entry_quantity(D(500),D(80000),D('.001'))!=engine.entry_quantity(D(375),D(80000),D('.001'))*D(500)/D(375)
assert costs[500,1]!=costs[375,1]*D(500)/D(375)
policy=[]
for N in [250,375,500]:
 sp={'parameters':{'lookback_days':31,'return_hurdle':.04,'exit_buffer_fraction':.01,'fixed_entry_notional_usdt':N}}
 for rr,actual,wanted in [(D('.04'),0,0),(D('.040001'),0,1),(-D('.04'),0,0),(-D('.040001'),0,-1),(-D('.01'),1,0),(-D('.009999'),1,1),(D('.01'),-1,0),(D('.009999'),-1,-1)]:
  m={'asset':'BTC','closes':[D(100)]*32+[100*(1+rr)]};want,a=engine.decide(sp,m,33,actual);assert want==wanted;(m['closes']).extend([D(1),D(99999)]);assert engine.decide(sp,m,33,actual)==(want,a);policy.append({'N':N,'return':str(rr),'actual':actual,'expected':wanted,'future_prices_ignored':True})
import run
p={'lookbacks':[3,4,5],'entry_notionals':[250,375,500]};p['grid']=[{'L':L,'N':N,'readonly':N==375,'fingerprint':f'{L}/{N}'} for L in p['lookbacks'] for N in p['entry_notionals']];p['native_grid']=[{'L':31,'N':N,'readonly':N==375,'fingerprint':f'BTC/{N}'} for N in p['entry_notionals']];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']+p['native_grid']};ng=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for g in grid:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);row=run.current_grid_row(old,g,scope);assert old==saved and row['N']==g['N'] and row['L']==g['L'];ne=run.neighborhood(row,p,full);expected=(2 if g['N'] in [250,500] else 3)*(1 if scope=='native' else 2 if g['L'] in [3,5] else 3);assert len(ne)==expected;ng.append({'scope':scope,'L':g['L'],'N':g['N'],'neighbors':len(ne),'canonical_status_unchanged':True})
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'quantity_and_nonlinear_cost_fixtures':checks,'strict_original_BTC_policy_fixtures':policy,'grid_metadata_neighborhood_fixtures':ng,'old_NAV_linear_scaling_explicitly_falsified':True,'native_1axis_parent_2axes_disclosed':True});print('PASS9LOT/cost fixtures,24BTC causal boundary fixtures,12native/parent metadata-neighborhood fixtures;no real-market evaluation')
