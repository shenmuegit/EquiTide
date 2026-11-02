"""Synthetic first: prevent fresh entries in weak trends while retaining valid old positions."""
import copy
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.025,'minimum_absolute_slow_return_for_fresh_entry':.025}}
cl=[D(95)]*25+[D(100)]*19+[D(96)];m={'asset':'ETH','closes':cl}
assert engine.decide(base,m,45,0)[0]==0,'Fresh long in 1.05% slow trend must be blocked by2.5% strength minimum'
cases=[]
for L in [3,4,5]:
 for T in [0,.025,.05]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,minimum_absolute_slow_return_for_fresh_entry=T)
  weak=copy.deepcopy(m);w,a=engine.decide(sp,weak,45,0);assert w==(1 if T==0 else 0)
  assert a['minimum_absolute_slow_return_for_fresh_entry']==T and a['observed_slow_absolute_return_exact']==str(abs(F(96)/F(95)-1)) and a['strength_filter_applied'] is True
  strong=copy.deepcopy(weak);strong['closes'][16]=D(60);assert engine.decide(sp,strong,45,0)[0]==1
  future=copy.deepcopy(strong);future['closes'].extend([D('999999'),D('.001')]);assert engine.decide(sp,future,45,0)==engine.decide(sp,strong,45,0)
  assert engine.decide(sp,weak,45,1)[0]==1
  weak['closes'][-1]=D('100.25');assert engine.decide(sp,weak,45,1)[0]==0
  short=copy.deepcopy(m);short['closes']=[D(105)]*25+[D(100)]*19+[D(104)];assert engine.decide(sp,short,45,0)[0]==(-1 if T==0 else 0)
  short['closes'][16]=D(150);assert engine.decide(sp,short,45,0)[0]==-1
  assert engine.decide(sp,m,45,-1)[0]==(1 if T==0 else 0)
  opposite=copy.deepcopy(m);opposite['closes'][16]=D(150);assert engine.decide(sp,opposite,45,1)[0]==0
  cases.append({'L':L,'strength_minimum':T,'weak_fresh_long':w,'future_append_invariant':True,'retention_exit_flip_and_short_checked':True})
for T,px,fast in [(.025,'102.5','106'),(.05,'105','109')]:
 sp=copy.deepcopy(base);sp['parameters']['minimum_absolute_slow_return_for_fresh_entry']=T;mm={'asset':'ETH','closes':[D(100)]*25+[D(fast)]*19+[D(px)]};assert engine.decide(sp,mm,45,0)[0]==1
 sp['parameters']['minimum_absolute_slow_return_for_fresh_entry']=T+1e-10;assert engine.decide(sp,mm,45,0)[0]==0
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.045001,.045)==0
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':cases,'extra_checks':['exact threshold equality and+1e-10','vol ceiling equality','mandatory slow-direction exit','weak same-side retention','fresh failed flip leaves flat','no funding signal required']})
print('PASS slow-strength thresholds0/2.5/5%, past-only exact ratios, retention/exit/reversal and vol boundary')
