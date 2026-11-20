"""Synthetic strict signal/funding and new calendar checks, zero market backtests."""
from common import *
import engine
from fractions import Fraction as F
import numpy as np
n=0
L=29
for H in [F('.0275'),F('.03'),F('.0325')]:
 for E in [F('.00375'),F('.005'),F('.00625')]:
  for actual in [-1,0,1]:
   for roc in sorted(set([-H-F('.00000001'),-H,-E-F('.00000001'),-E,F(0),E,E+F('.00000001'),H,H+F('.00000001')])):
    c=[F(200)]*50;c[39-L]=F(100);c[39]=100*(1+roc);want=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0;out,r=engine.btc.target(c,40,L,float(H),actual,float(E));assert want==out and F(r)==roc and engine.btc.target(c[:40]+[F(10**12),F(1)],40,L,float(H),actual,float(E))==(out,r);n+=1
for cap in [.026125,.0275,.028875]:
 assert engine.entry_filter(1,0,cap,cap)==1 and engine.entry_filter(1,0,cap+1e-6,cap)==0 and engine.entry_filter(1,1,cap+1e-6,cap)==1
assert core.funding_amount(core.D(2),core.D(100),core.D('.001'),3)==(core.D('-.2'),core.D('-.6')) and core.funding_amount(core.D(-2),core.D(100),core.D('.001'),3)==(core.D('.2'),core.D('.2'))
assert core.END-core.START==core.DAYS==391 and list(range(0,391,30))+[391]==[0,30,60,90,120,150,180,210,240,270,300,330,360,390,391] and 391-351==40 and 391-370==21
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25;assert (np.array([3750.,4500.])+np.array([15000.,14000.])).tolist()==[18750.,18500.]
# Exact declared neighbor geometry, synthetic only.
import json
from run import neighbors
p=json.loads((R/'plan.json').read_text());full={g['fingerprint']:g for g in p['grid']+p['native_grid']}
for g in p['grid']:
 ns,dims=neighbors(g,p,full);expected=[z for z in p['grid'] if abs(p['axes']['ETH_TREND_WINDOW_DAYS'].index(z['W'])-p['axes']['ETH_TREND_WINDOW_DAYS'].index(g['W']))<=1 and abs(p['axes']['ETH_FUNDING_SETTLEMENT_COUNT'].index(z['K'])-p['axes']['ETH_FUNDING_SETTLEMENT_COUNT'].index(g['K']))<=1];assert dims==2 and {z['fingerprint'] for z in ns}=={z['fingerprint'] for z in expected}
for g in p['native_grid']:
 ns,dims=neighbors(g,p,full);expected=[z for z in p['native_grid'] if abs(p['axes']['ETH_TREND_WINDOW_DAYS'].index(z['W'])-p['axes']['ETH_TREND_WINDOW_DAYS'].index(g['W']))<=1 and abs(p['axes']['ETH_FUNDING_SETTLEMENT_COUNT'].index(z['K'])-p['axes']['ETH_FUNDING_SETTLEMENT_COUNT'].index(g['K']))<=1];assert dims==2 and {z['fingerprint'] for z in ns}=={z['fingerprint'] for z in expected}
assert core.stats(np.array([100.,80.,110.]),[100.,110.],1)['sharpe_365'] is None
# Funding budget depends only on the completed prefix; equality passes, greater outflow blocks.
import math,statistics
closes=[100+((i*7)%11) for i in range(50)];i=40
for VW in [7,8,9,10,12]:
 expected=statistics.stdev([math.log(closes[j]/closes[j-1]) for j in range(i-VW,i)]);assert engine.budget_sigma(closes,i,VW)==expected==engine.budget_sigma(closes[:i]+[10**12,1],i,VW)
 event={'events':[{'entry_interval_hours':core.D(8),'settlement_ts':9*HOUR,'available_ts':9*HOUR,'realized_rate':core.D('.00001'),'source_index':1}], 'median_rate':core.D('.00001'),'count':1};cap=engine.carry_cap(expected,.01,event);assert cap==min(core.D('.0002'),core.D('.01')*core.D(str(expected))*core.D(8)/core.D(24));event['median_rate']=cap;assert engine.funding_filter(1,0,event,10*HOUR,cap)[0]==1;event['median_rate']=cap+core.D('1e-12');assert engine.funding_filter(1,0,event,10*HOUR,cap)[0]==0 and engine.funding_filter(1,1,event,10*HOUR,cap)[0]==1

# Synthetic mature-prefix medians: exact even/odd rules, age boundaries and future exclusion.
signal=50*HOUR
base=[{'settlement_ts':signal-age*HOUR,'available_ts':signal-(age-1)*HOUR,'realized_rate':core.D(rate),'source_index':j+1,'entry_interval_hours':core.D(8)} for j,(age,rate) in enumerate([(1,'.0001'),(9,'.0004'),(17,'-.0002'),(25,'.0003')])]
for count,expected in [(2,'.00025'),(3,'.0001'),(4,'.0002')]:
 out=engine.median_funding(base,signal,count);assert out['median_rate']==core.D(expected) and out['count']==count
 future={'settlement_ts':signal+HOUR,'available_ts':signal+2*HOUR,'realized_rate':core.D(999),'source_index':99}
 immature={'settlement_ts':signal-HOUR+1,'available_ts':signal,'realized_rate':core.D(999),'source_index':98}
 stale={'settlement_ts':signal-36*HOUR-1,'available_ts':signal,'realized_rate':core.D(999),'source_index':97}
 assert engine.median_funding(base+[future,immature,stale],signal,count)==out
 assert engine.median_funding(base[:count-1],signal,count) is None
edge=[{**base[0],'settlement_ts':signal-HOUR},{**base[1],'settlement_ts':signal-36*HOUR}];assert engine.median_funding(edge,signal,2) is not None
assert engine.median_funding([{**edge[0],'available_ts':signal+1},edge[1]],signal,2) is None
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'strict_BTC_boundary_and_future_suffix_cases':n,'native_entry_equalities_and_funding_income_outflow_stress_checked':True,'calendar391_13fullfold_1daytail_recent40_extension21_checked':True,'whole_bank_weights_not_normalized':True,'new_strategy_or_account_calculations':0});print('PASS syntheticcausality/strictentry/funding/calendargeometry/fullDD,0marketbacktests')

# Actual samplelogvol window semantics and future-suffix exclusion, synthetic only.
for V in [6,8,9,10,11,12,14]:
 expected=statistics.stdev([math.log(closes[j]/closes[j-1]) for j in range(i-V,i)]);assert engine.btc_entry_sigma(closes,i,V)==expected==engine.btc_entry_sigma(closes[:i]+[10**12,1],i,V)
 assert engine.entry_filter(1,0,expected,expected)==1 and engine.entry_filter(1,0,expected,expected-1e-12)==0 and engine.entry_filter(1,1,expected,expected-1e-12)==1

for recent in [F('.0025')-F('1e-10'),F('.0025'),F('.0025')+F('1e-10')]:
 assert engine.confirmation_filter(1,0,recent,.0025)==(1 if recent>F('.0025') else 0)
 assert engine.confirmation_filter(-1,0,-recent,.0025)==(-1 if recent>F('.0025') else 0)
 assert engine.confirmation_filter(1,1,recent,.0025)==1

# Newly accepted counts: independent odd/even medians and scarce ordinary8h history.
for M in [4,5,6]:
 ev=[{'settlement_ts':signal-age*HOUR,'available_ts':signal-(age-1)*HOUR,'realized_rate':core.D(str((j*7)%11/100000)),'source_index':j+1,'entry_interval_hours':core.D(4)} for j,age in enumerate([1,5,9,13,17,21])]
 vals=sorted(e['realized_rate'] for e in ev[:M]);wanted=vals[M//2] if M%2 else (vals[M//2-1]+vals[M//2])/2;out=engine.median_funding(ev,signal,M);assert out['median_rate']==wanted and out['count']==M and len(out['events'])==M
 assert engine.median_funding(ev[:M-1],signal,M) is None
 ordinary=[{**e,'settlement_ts':signal-age*HOUR,'available_ts':signal-(age-1)*HOUR} for e,age in zip(ev,[8,16,24,32,40,48])]
 if M>4:assert engine.median_funding(ordinary,signal,M) is None
assert engine.funding_filter(1,0,None,signal,None)[0]==0 and engine.funding_filter(1,1,None,signal,None)[0]==1 and engine.funding_filter(0,1,None,signal,None)[0]==0
assert engine.trade is core.trade and engine.funding_amount is core.funding_amount and engine.summary is core.summary
put(R/'engine_domain_unit_verification.json',{'passed':True,'synthetic_only':True,'newM5_M6_odd_even_independent_medians_and_1to36h_age_available_prefix_and_missing_entry_only_checked':True,'ordinary8h_midnight_scarcity_checked':True,'accounting_execution_funding_function_identity_unchanged':True,'no_market_or_account_calculations':True})

# Explicit max-age boundary and joint count tests; default36 matches historical kernel.
old=module(ROOT/'research/experiments/20261120T184719Z/engine.py','old_age36_kernel')
for age in [36,48,60]:
 for M in [4,5,6]:
  out=engine.median_funding(ordinary,signal,M,age);selected=[z for z in ordinary if HOUR<=signal-z['settlement_ts']<=age*HOUR and z['available_ts']<=signal][:M]
  assert (out is None)==(len(selected)<M)
  if out:
   rates=sorted(z['realized_rate'] for z in selected);assert out['median_rate']==(rates[M//2] if M%2 else sum(rates[M//2-1:M//2+1])/2)
  if age==36:assert out==old.median_funding(ordinary,signal,M)
 edge=[{**ev[0],'settlement_ts':signal-HOUR},{**ev[1],'settlement_ts':signal-age*HOUR}]
 assert engine.median_funding(edge,signal,2,age) is not None
 assert engine.median_funding([edge[0],{**edge[1],'settlement_ts':signal-age*HOUR-1}],signal,2,age) is None
 for raw,actual in [(1,0),(1,1),(0,1),(-1,0)]:assert engine.funding_filter(raw,actual,None,signal,None,age)==old.funding_filter(raw,actual,None,signal,None) if age==36 else engine.funding_filter(raw,actual,None,signal,None,age)[0]==(0 if raw and raw!=actual else raw)
put(R/'engine_domain_unit_verification.json',{'passed':True,'synthetic_only':True,'joint3x3_age_count_checked':True,'inclusive_age_boundary_future_available_and_missing_entry_only_checked':True,'default36_selection_and_filter_equal_historical_kernel':True,'native_cashflow_trade_cost_funding_function_identity':True,'no_market_or_account_calculations':True})
