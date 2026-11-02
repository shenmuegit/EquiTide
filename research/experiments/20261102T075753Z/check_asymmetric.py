"""Synthetic regression: long hurdle varies independently while short threshold stays2.5%."""
import copy,sys
from decimal import Decimal as D
from common import *
import engine
if "--legacy-symmetric" in sys.argv:engine=module(ROOT/"research/experiments/20261101T135218Z/engine.py","legacy_symmetric_for_regression")
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.025,'long_entry_return_hurdle':.01}}
m={'asset':'ETH','closes':[D(60)]*25+[D(100)]*19+[D('98.8')]}
assert engine.decide(base,m,45,0)[0]==1,'1.2% pullback should enter with1%long hurdle even though short hurdle is2.5%'
cases=[]
for L in [3,4,5]:
 for HL in [.01,.015,.02]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,long_entry_return_hurdle=HL)
  w,a=engine.decide(sp,m,45,0);assert w==(1 if HL==.01 else 0)
  assert a['long_entry_return_hurdle']==HL and a['short_entry_return_hurdle']==.025
  # Independent long equality vs strict crossing.
  long=copy.deepcopy(m);long['closes'][-1]=D(100)*(1-D(str(HL)));assert engine.decide(sp,long,45,0)[0]==0
  long['closes'][-1]-=D('.0000001');assert engine.decide(sp,long,45,0)[0]==1
  # Short threshold must not change when the long parameter moves.
  short={'asset':'ETH','closes':[D(200)]*25+[D(100)]*19+[D('102.2')]};assert engine.decide(sp,short,45,0)[0]==0
  short['closes'][-1]=D('102.5');assert engine.decide(sp,short,45,0)[0]==0
  short['closes'][-1]+=D('.0000001');assert engine.decide(sp,short,45,0)[0]==-1
  retain=copy.deepcopy(m);retain['closes'][-1]=D('100.1');assert engine.decide(sp,retain,45,1)[0]==1
  retain['closes'][-1]=D('100.25');assert engine.decide(sp,retain,45,1)[0]==0
  retain['closes'][-1]=D('99.75');assert engine.decide(sp,retain,45,-1)[0]==0
  assert engine.decide(sp,m,45,-1)[0]==(1 if HL==.01 else 0)
  future=copy.deepcopy(m);future['closes'].extend([D('999999'),D('.001')]);assert engine.decide(sp,future,45,0)==(w,a)
  wrongslow=copy.deepcopy(long);wrongslow['closes'][16]=D(200);assert engine.decide(sp,wrongslow,45,0)[0]==0
  if HL==.02:
   implicit=copy.deepcopy(sp);implicit['parameters'].pop('long_entry_return_hurdle');implicit['parameters']['return_hurdle']=HL;explicit=copy.deepcopy(implicit);explicit['parameters']['long_entry_return_hurdle']=HL;assert engine.decide(implicit,m,45,0)==engine.decide(explicit,m,45,0)
  cases.append({'L':L,'long_H':HL,'short_H':.025,'strict_long_and_short_boundaries':True,'retention_exit_flip_future_and_slowgate':True})
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.045001,.045)==0
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':cases,'extra_checks':['long1.2%pullback independent fromshortH','implicit symmetric2 identity','volboundary']})
print('PASS asymmetric long1/1.5/2% xL3/4/5 with fixedshort2.5%, strict boundaries, original exits and future-invariance')
