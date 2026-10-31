import math,statistics,json
from decimal import Decimal as D
from common import *
import engine
assert engine.entry_filter(1,0,.03,.03)==1 and engine.entry_filter(1,0,.03001,.03)==0
assert engine.entry_filter(1,1,.99,.03)==1 and engine.entry_filter(0,1,.99,.03)==0 and engine.entry_filter(-1,1,.99,.03)==0
spec={'parameters':{'lookback_days':4,'trend_lookback_days':28,'return_hurdle':.02,'exit_buffer_fraction':0,'entry_volatility_window_days':15,'entry_volatility_ceiling':.035}}
v=[D(100)]*45;v[4]=D(104);v[28]=D(100);v[32]=D(103);m={'asset':'ETH','closes':v};wanted,a=engine.decide(spec,m,33,0);assert wanted==-1;v[33]=D(999999);assert engine.decide(spec,m,33,0)==(wanted,a)
v[25]=D(200);assert engine.decide(spec,m,33,0)[0]==0 and engine.decide(spec,m,33,-1)[0]==-1
v[4]=D(90);assert engine.decide(spec,m,33,-1)[0]==0
state={'cash':'15000','signed_units':'0','entry_price':'0','entry_reference':'0'};meta={'lot_size':'.001','tick_size':'.01','min_notional':'20'};after,z=core.trade(state,D('1.5'),D(3000),D(100000000),D('.03'),meta,3,True);assert z['status']=='filled' and D(after['cash'])<15000 and D(after['signed_units'])==D('1.5')
base,flow=core.funding_amount(D('-1.5'),D(3000),D('.0001'),3);assert flow==base==D('.45')
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':['strictvolcap equalityallowed/exceedblocks','filteronlyfreshentry/orflipentry, sameactualretentionandbaseexitunaffected','causalV15onlypriorclosesandfutureperturbation','slowgatealwaysclosesincompatibleactualposition','native15000collateral/4500sizenonlinearcost','positivefundingincomeunamplified']});print('PASS syntheticnewentryvolcap/causality/execution')
