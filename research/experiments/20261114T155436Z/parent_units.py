"""Synthetic strict signal/funding and new calendar checks, zero market backtests."""
from common import *
import engine
from fractions import Fraction as F
import numpy as np
n=0
H=F('.03')
for E in [F('.005'),F('.01'),F('.015')]:
 for L in [29]:
  for actual in [-1,0,1]:
   for roc in sorted(set([-H-F('.00000001'),-H,-E-F('.00000001'),-E,F(0),E,E+F('.00000001'),H,H+F('.00000001')])):
    c=[F(200)]*50;c[39-L]=F(100);c[39]=100*(1+roc);want=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>-E else -1 if actual==-1 and roc<E else 0;out,r=engine.btc.target(c,40,L,float(H),actual,float(E));assert want==out and F(r)==roc and engine.btc.target(c[:40]+[F(10**12),F(1)],40,L,float(H),actual,float(E))==(out,r);n+=1
for cap in [.03,.04]:
 assert engine.entry_filter(1,0,cap,cap)==1 and engine.entry_filter(1,0,cap+1e-6,cap)==0 and engine.entry_filter(1,1,cap+1e-6,cap)==1
assert core.funding_amount(core.D(2),core.D(100),core.D('.001'),3)==(core.D('-.2'),core.D('-.6')) and core.funding_amount(core.D(-2),core.D(100),core.D('.001'),3)==(core.D('.2'),core.D('.2'))
assert core.END-core.START==core.DAYS==391 and list(range(0,391,30))+[391]==[0,30,60,90,120,150,180,210,240,270,300,330,360,390,391] and 391-351==40 and 391-370==21
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25;assert (np.array([3750.,4500.])+np.array([15000.,14000.])).tolist()==[18750.,18500.]
# Validate the actual preregistered neighbor graph without any market return calculation.
import json
from run import neighbors
p=json.loads((R/'plan.json').read_text());full={g['fingerprint']:g for g in p['grid']+p['native_grid']}
for g in p['grid']:
 ns,dims=neighbors(g,p,full);assert dims==2 and len(ns)==(6 if g['W']==.01 else 4)
for g in p['native_grid']:
 ns,dims=neighbors(g,p,full);assert dims==1 and all(z['asset']==g['asset'] for z in ns) and len(ns)==(3 if g['asset']=='BTC' and g['W']==.01 else 2)
assert core.stats(np.array([100.,80.,110.]),[100.,110.],1)['sharpe_365'] is None
# Funding budget depends only on the completed prefix; equality passes, greater outflow blocks.
import math,statistics
closes=[100+((i*7)%11) for i in range(50)];i=40
for VW in [8,10,12]:
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
