"""Synthetic short-hurdle independence and strict causal boundaries; no market valuations."""
import copy,sys
from decimal import Decimal as D
from common import *
import engine
if '--legacy-fixed-short' in sys.argv:
 original=engine.decide
 def fixed_short(spec,m,i,actual):
  sp=copy.deepcopy(spec);sp['parameters']['return_hurdle']=.025;return original(sp,m,i,actual)
 engine.decide=fixed_short
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.02,'long_entry_return_hurdle':.015}}
short={'asset':'ETH','closes':[D(200)]*25+[D(100)]*19+[D('102.2')]}
assert engine.decide(base,short,45,0)[0]==-1,'2.2% rally must enter short at HS2%, independent of old fixed HS2.5%'
cases=[]
for L in [3,4,5]:
 for HS in [.02,.025,.03]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,return_hurdle=HS);w,a=engine.decide(sp,short,45,0);assert w==(-1 if HS==.02 else 0)
  assert a['long_entry_return_hurdle']==.015 and a['short_entry_return_hurdle']==HS
  edge=copy.deepcopy(short);edge['closes'][-1]=D(100)*(1+D(str(HS)));assert engine.decide(sp,edge,45,0)[0]==0;edge['closes'][-1]+=D('.0000001');assert engine.decide(sp,edge,45,0)[0]==-1
  long={'asset':'ETH','closes':[D(60)]*25+[D(100)]*19+[D('98.5')]};assert engine.decide(sp,long,45,0)[0]==0;long['closes'][-1]-=D('.0000001');assert engine.decide(sp,long,45,0)[0]==1
  assert engine.decide(sp,long,45,-1)[0]==1 and engine.decide(sp,short,45,1)[0]==w
  retlong=copy.deepcopy(long);retlong['closes'][-1]=D('100.1');assert engine.decide(sp,retlong,45,1)[0]==1;retlong['closes'][-1]=D('100.25');assert engine.decide(sp,retlong,45,1)[0]==0
  retshort=copy.deepcopy(short);retshort['closes'][-1]=D('99.9');assert engine.decide(sp,retshort,45,-1)[0]==-1;retshort['closes'][-1]=D('99.75');assert engine.decide(sp,retshort,45,-1)[0]==0
  future=copy.deepcopy(short);future['closes'].extend([D('999999'),D('.001')]);assert engine.decide(sp,future,45,0)==(w,a)
  wrongslow=copy.deepcopy(edge);wrongslow['closes'][16]=D(60);assert engine.decide(sp,wrongslow,45,0)[0]==0
  cases.append({'L':L,'short_HS':HS,'fixed_long_HL':.015,'strict_boundaries_retention_exit_flip_future_slowgate':True})
assert engine.entry_filter(-1,0,.045,.045)==-1 and engine.entry_filter(-1,0,.045001,.045)==0 and engine.entry_filter(-1,-1,.045001,.045)==-1
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':cases,'extra_checks':['fixedshortmutant is detected at2.2%rally','long1.5boundary independent fromvariedshortHS','volentryboundary vsactualpositionretention']})
print('PASS shortHS2/2.5/3% xL3/4/5, fixedlong1.5%, strict boundaries/retention/exits/flip/future-invariance')
