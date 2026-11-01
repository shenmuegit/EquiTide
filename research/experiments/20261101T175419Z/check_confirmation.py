"""Synthetic-only behavior tests; financial strategy removal must break the spike case."""
import copy,json
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.025,'entry_confirmation_days':2}}
cl=[D(60)]*25+[D(100)]*19+[D(96)]
w,a=engine.decide(base,{'asset':'ETH','closes':cl},45,0)
assert w==0, 'single spike must wait for two completed extremes'
checks=[]
for L in [3,4,5]:
 for K in [1,2,3]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,entry_confirmation_days=K)
  cl=[D(60)]*25+[D(100)]*17+[D(96),D(95),D(94)]
  w,a=engine.decide(sp,{'asset':'ETH','closes':cl},45,0);assert w==1
  assert a['entry_confirmation_days']==K and a['entry_confirmation_passed']
  future=cl+[D(999999),D(1)];assert engine.decide(sp,{'asset':'ETH','closes':future},45,0)==(w,a)
  cl=[D(200)]*25+[D(100)]*17+[D(104),D(105),D(106)]
  w,a=engine.decide(sp,{'asset':'ETH','closes':cl},45,0);assert w==-1 and a['entry_confirmation_passed']
  cl=[D(60)]*25+[D(100)]*19+[D('100.1')]
  assert engine.decide(sp,{'asset':'ETH','closes':cl},45,1)[0]==1
  cl[-1]=D('100.25');assert engine.decide(sp,{'asset':'ETH','closes':cl},45,1)[0]==0
  cl[-1]=D(96)
  assert engine.decide(sp,{'asset':'ETH','closes':cl},45,-1)[0]==(1 if K==1 else 0)
  cl[-1]=D('97.5');assert engine.decide(sp,{'asset':'ETH','closes':cl},45,0)[0]==0
  checks.append([L,K,'long/short/history/future/retention/equality/failed-flip'])
# Previous-day exact hurdle fails strict confirmation; t+0 value never rescues it.
sp=copy.deepcopy(base);cl=[D(60)]*25+[D(100)]*18+[D('97.5'),D(96)]
assert engine.decide(sp,{'asset':'ETH','closes':cl},45,0)[0]==0
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.045001,.045)==0
assert engine.entry_filter(1,1,1,.045)==1 and engine.entry_filter(0,1,1,.045)==0
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':checks+['priorhurdleequality','entryvolboundary']})
print('PASS causal K1/2/3 confirmation, equality, exit/retention/flip, nofuture')
