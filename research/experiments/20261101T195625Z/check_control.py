"""Synthetic behavior checks: common-return removal, exact boundaries, no future data."""
import copy,json
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.025,'btc_return_control_weight':1}}
e=[D(60)]*25+[D(100)]*19+[D(96)];b=[D(100)]*44+[D(96)]
w,a=engine.decide(base,{'asset':'ETH','closes':e,'benchmark_closes':b},45,0)
assert w==0,'common BTC/ETH move must cancel at control A1'
checks=[]
for L in [3,4,5]:
 for A in [0,.5,1]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,btc_return_control_weight=A)
  e=[D(60)]*25+[D(100)]*19+[D(94)];b=[D(100)]*44+[D(98)]
  w,a=engine.decide(sp,{'asset':'ETH','closes':e,'benchmark_closes':b},45,0);assert w==1 and F(a['return_exact'])==-F(6,100)+F(str(A))*F(2,100)
  assert a['btc_return_control_weight']==A and F(a['ETH_return_exact'])==-F(6,100)
  assert engine.decide(sp,{'asset':'ETH','closes':e+[D(999999)],'benchmark_closes':b+[D(1)]},45,0)==(w,a)
  e=[D(200)]*25+[D(100)]*19+[D(106)];b[-1]=D(102)
  w,a=engine.decide(sp,{'asset':'ETH','closes':e,'benchmark_closes':b},45,0);assert w==-1
  e=[D(60)]*25+[D(100)]*19+[D('100.1')];b[-1]=D(100)
  assert engine.decide(sp,{'asset':'ETH','closes':e,'benchmark_closes':b},45,1)[0]==1
  e[-1]=D('100.25');assert engine.decide(sp,{'asset':'ETH','closes':e,'benchmark_closes':b},45,1)[0]==0
  e[-1]=D('97.5');assert engine.decide(sp,{'asset':'ETH','closes':e,'benchmark_closes':b},45,0)[0]==0
  e=[D(200)]*25+[D(100)]*19+[D(94)]
  assert engine.decide(sp,{'asset':'ETH','closes':e,'benchmark_closes':b},45,0)[0]==0
  checks.append([L,A,'relative-long/short/boundary/future/retention/absolute-slow-gate'])
# No BTC source dependence at A0; .5 is a signal coefficient, not normalization.
sp=copy.deepcopy(base);sp['parameters']['btc_return_control_weight']=0;e=[D(60)]*25+[D(100)]*19+[D(96)]
assert engine.decide(sp,{'asset':'ETH','closes':e},45,0)[0]==1
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.045001,.045)==0
assert engine.entry_filter(1,1,1,.045)==1 and engine.entry_filter(0,1,1,.045)==0
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':checks+['A0baselineidentity','entryvolboundary']})
print('PASS L3/4/5 x A0/.5/1, exact residual, causality and gate/exit/retention')
