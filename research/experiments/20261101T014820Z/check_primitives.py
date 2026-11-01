from decimal import Decimal as D
from common import *
import engine
spec={'parameters':{'lookback_days':4,'trend_lookback_days':28,'return_hurdle':.02,'exit_buffer_fraction':0,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045}}
v=[D(100)]*45;v[4]=D(110);v[32]=D(102);m={'asset':'ETH','closes':v}
assert engine.decide(spec,m,33,0)[0]==0 and engine.decide(spec,m,33,-1)[0]==-1
v[32]=D('102.01');wanted,a=engine.decide(spec,m,33,0);assert wanted==-1;v[33]=D(999999);assert engine.decide(spec,m,33,0)==(wanted,a)
v[25]=D(300);assert engine.decide(spec,m,33,0)[0]==0 and engine.decide(spec,m,33,-1)[0]==-1
v[32]=D(100);assert engine.decide(spec,m,33,-1)[0]==0
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.045001,.045)==0 and engine.entry_filter(1,1,.99,.045)==1 and engine.entry_filter(0,1,.99,.045)==0
state={'cash':'15000','signed_units':'0','entry_price':'0','entry_reference':'0'};meta={'lot_size':'.001','tick_size':'.01','min_notional':'20'};after,z=core.trade(state,D('1.5'),D(3000),D(100000000),D('.03'),meta,3,True);assert z['status']=='filled' and D(after['cash'])<15000 and D(after['signed_units'])==D('1.5')
base,flow=core.funding_amount(D('-1.5'),D(3000),D('.0001'),3);assert flow==base==D('.45')
print('PASS synthetic signal boundary/causality/volfilter/native accounting')

spec["parameters"]["exit_buffer_fraction"]=.0025
v=[D(100)]*45;v[4]=D(90);v[32]=D("100.10");m={"asset":"ETH","closes":v};assert engine.decide(spec,m,33,1)[0]==1 and engine.decide(spec,m,33,0)[0]==0
v[32]=D("100.25");assert engine.decide(spec,m,33,1)[0]==0
v[4]=D(110);v[32]=D("99.90");assert engine.decide(spec,m,33,-1)[0]==-1
v[32]=D("99.75");assert engine.decide(spec,m,33,-1)[0]==0
print("PASS nonzero exitbuffer holds crossingzero, exitsstrictboundary, does notcreatefreshentry")

put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':['nonzeroexitbuffer symmetric retention and strict boundary exits without fresh entries','exact H equality no fresh short, crossed H opens and retains actual short','future close perturbation cannot affect priorclosed signal','entry-only fixed volatility cap, same-direction actual retention and zero exit','native actual15000 collateral/4500 quantity/nonlinear execution','positive funding income unamplified']})
