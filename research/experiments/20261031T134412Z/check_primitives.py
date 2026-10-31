"""Synthetic causality, native LOT, impact and collateral boundary checks only."""
from decimal import Decimal as D,ROUND_FLOOR
from common import *
import engine
lot=D('.001');ref=D('90000');q1=(D(1000)/ref/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;qhalf=(D(500)/ref/lot).to_integral_value(rounding=ROUND_FLOOR)*lot;q15=(D(1500)/ref/lot).to_integral_value(rounding=ROUND_FLOOR)*lot
assert q1==D('.011') and qhalf==D('.005') and q1*D('.5')%lot and q15==D('.016') and q1*D('1.5')%lot
meta={'lot_size':'.001','tick_size':'.1','min_notional':'50'};state={'cash':'5000','signed_units':'0','entry_price':'0','entry_reference':'0'}
_,a=core.trade(state,q1,ref,D('100000000'),D('.03'),meta,1,True);s,b=core.trade(state,q15,ref,D('100000000'),D('.03'),meta,1,True);assert D(s['cash'])<D(5000) and D(b['impact_rate'])>D(a['impact_rate']) and D(b['cost_parts']['impact'])/D(a['cost_parts']['impact'])>q15/q1
st,r=core.trade(state,D('.1'),ref,D('100000000'),D('.03'),meta,1,True);assert r['status']=='rejected' and r['reason']=='fully_collateralized_1x_entry_cap' and st==state
spec={'parameters':{'lookback_days':31,'return_hurdle':.04,'exit_buffer_fraction':.01}};values=[D(100)]*40;values[32]=D(104);m={'asset':'BTC','closes':values};assert engine.decide(spec,m,33,0)[0]==0;values[32]=D(105);z=engine.decide(spec,m,33,0);assert z[0]==1;values[33]=D(999999);assert engine.decide(spec,m,33,0)==z
es={'parameters':{'lookback_days':3,'return_hurdle':.02,'exit_buffer_fraction':0,'trend_lookback_days':28}};v=[D(100)]*40;v[29]=D(104);v[4]=D(90);mm={'asset':'ETH','closes':v};assert engine.decide(es,mm,33,0)[0]==1;v[4]=D(110);assert engine.decide(es,mm,33,1)[0]==0
base,flow=core.funding_amount(D('-.005'),ref,D('.0001'),3);assert flow==base==D('.045');base,flow=core.funding_amount(D('.005'),ref,D('.0001'),3);assert base==D('-.045') and flow==D('-.135')
# Exact L5 boundary, future-day mutation and zero exit after incompatible slow gate.
es['parameters']['lookback_days']=5;es['parameters']['return_hurdle']=.03;v=[D(100)]*40;v[4]=D(110);v[27]=D(100);v[32]=D('103');mm={'asset':'ETH','closes':v};assert engine.decide(es,mm,33,0)[0]==0
v[32]=D('103.0001');z=engine.decide(es,mm,33,0);assert z[0]==-1;v[33]=D(999999);assert engine.decide(es,mm,33,0)==z
v[32]=D(100);assert engine.decide(es,mm,33,-1)[0]==0
put(R/'primitive_verification.json' ,{'passed':True,'synthetic_only':True,'cases':['native LOT half/1.5 differs from scaled old quantity','size-dependent impact not linear source cost','actual5000 collateral entry cap rejects oversized order','BTC strict hurdle and future-close perturbation','ETH true slow-gate closes incompatible actual position','funding income unscaled/outflow stressed','genericL5 strict3percent equality and future-close causality','zero-exit equality closes actualshort']});print('PASS6 synthetic native-execution/capital/policy boundary groups')
