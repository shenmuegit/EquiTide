"""Synthetic quantity discontinuity, prior-price causality, costs and L/N neighborhoods."""
import copy,sys
from decimal import Decimal as D,ROUND_FLOOR
from common import *
import engine
sizing=engine.entry_quantity
if '--legacy-slow-range' in sys.argv:
 # Intentional synthetic negative control: resizing oldN500 units is mathematically wrong at new LOT boundaries.
 sizing=lambda n,price,lot:engine.entry_quantity(D(500),price,lot)*n/D(500)
assert sizing(D(625),D(100000),D('.001'))==D('.006'),'Synthetic linear resizing must fail exact prior-close LOT sizing'
checks=[];costs={}
for N,expected in [(500,'.005'),(625,'.006'),(750,'.007')]:
 q=engine.entry_quantity(D(N),D(100000),D('.001'));assert q==D(expected)
 assert q*D(100000)<=N<(q+D('.001'))*D(100000)
 for future_open in [D(60000),D(120000)]:assert engine.entry_quantity(D(N),D(100000),D('.001'))==q
 for k in [1,2,3]:
  state={'cash':'3750','signed_units':'0','entry_price':'0','entry_reference':'0'};meta={'lot_size':'.001','tick_size':'.1','min_notional':'50'}
  after,receipt=core.trade(state,q,D(100000),D(20000000),D('.03'),meta,k,True);assert receipt['status']=='filled' and D(after['signed_units'])==q and D(receipt['quantity'])==q and D(receipt['participation'])==q*D(100000)/D(20000000)
  assert abs(D(receipt['cost_parts']['impact'])-q*D(100000)*D('.5')*D('.03')*(q*D(100000)/D(20000000)).sqrt()*k)<D('1e-24')
  costs[N,k]=D(receipt['cost_usdt']);checks.append({'N':N,'cost_multiplier':k,'expected_quantity':str(q),'actual_cost':str(costs[N,k]),'actual_participation':receipt['participation']})
assert engine.entry_quantity(D(625),D(100000),D('.001'))!=engine.entry_quantity(D(500),D(100000),D('.001'))*D(625)/D(500)
assert engine.entry_quantity(D(750),D(100000),D('.001'))!=engine.entry_quantity(D(500),D(100000),D('.001'))*D(750)/D(500)
assert costs[750,1]!=costs[500,1]*D(750)/D(500)
policy=[]
for N in [500,625,750]:
 sp={'parameters':{'lookback_days':31,'return_hurdle':.04,'exit_buffer_fraction':.01,'fixed_entry_notional_usdt':N}}
 for rr,actual,wanted in [(D('.04'),0,0),(D('.040001'),0,1),(-D('.04'),0,0),(-D('.040001'),0,-1),(-D('.01'),1,0),(-D('.009999'),1,1),(D('.01'),-1,0),(D('.009999'),-1,-1)]:
  m={'asset':'BTC','closes':[D(100)]*32+[100*(1+rr)]};want,a=engine.decide(sp,m,33,actual);assert want==wanted;(m['closes']).extend([D(1),D(99999)]);assert engine.decide(sp,m,33,actual)==(want,a);policy.append({'N':N,'return':str(rr),'actual':actual,'expected':wanted,'future_prices_ignored':True})
import run
p={'lookbacks':[3,4,5],'entry_notionals':[500,625,750]};p['grid']=[{'L':L,'N':N,'readonly':N==500,'fingerprint':f'{L}/{N}'} for L in p['lookbacks'] for N in p['entry_notionals']];p['native_grid']=[{'L':31,'N':N,'readonly':N==500,'fingerprint':f'BTC/{N}'} for N in p['entry_notionals']];full={g['fingerprint']:{'name':g['fingerprint']} for g in p['grid']+p['native_grid']};ng=[]
for scope,grid in [('parent',p['grid']),('native',p['native_grid'])]:
 for g in grid:
  old={'criteria':{'sentinel':False},'sensitivity':{'sentinel':17}};saved=copy.deepcopy(old);row=run.current_grid_row(old,g,scope);assert old==saved and row['N']==g['N'] and row['L']==g['L'];ne=run.neighborhood(row,p,full);expected=(2 if g['N'] in [500,750] else 3)*(1 if scope=='native' else 2 if g['L'] in [3,5] else 3);assert len(ne)==expected;ng.append({'scope':scope,'L':g['L'],'N':g['N'],'neighbors':len(ne),'canonical_status_unchanged':True})
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'quantity_and_nonlinear_cost_fixtures':checks,'strict_original_BTC_policy_fixtures':policy,'grid_metadata_neighborhood_fixtures':ng,'old_NAV_linear_scaling_explicitly_falsified':True,'native_1axis_parent_2axes_disclosed':True});print('PASS9LOT/cost fixtures,24BTC causal boundary fixtures,12native/parent metadata-neighborhood fixtures;no real-market evaluation')
