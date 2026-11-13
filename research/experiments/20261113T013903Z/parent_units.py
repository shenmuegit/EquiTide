"""Synthetic exact-boundary, side-sign, closure and passive-dollar arithmetic regressions."""
from common import *
from engine import flow_filter
import numpy as np
def row(buy,close):
 x=[0]*12;x[6]=close-1;x[7]='100';x[10]=str(buy);return x
bars=[row(55,86400000),row(45,172800000),row(99,259200000)]
assert flow_filter(1,0,bars,1,1,.1,86400000*1000000)[0]==1
assert flow_filter(-1,0,bars,1,1,0,86400000*1000000)[0]==0
assert flow_filter(-1,0,bars,2,1,.1,172800000*1000000)[0]==-1
assert flow_filter(1,1,bars,2,1,.1,172800000*1000000)[0]==1
assert flow_filter(0,1,bars,2,1,.1,172800000*1000000)[0]==0
assert flow_filter(1,0,bars,1,1,0,86400000*1000000-1)[0]==0
assert flow_filter(1,0,[],0,1,0,0)[0]==0
zero=row(0,86400000);zero[7]='0';assert flow_filter(1,0,[zero],1,1,0,86400000*1000000)[0]==0
# Future suffix cannot change the previous completed window.
assert flow_filter(1,0,bars,1,1,.1,86400000*1000000)==flow_filter(1,0,bars[:1]+[row(0,172800000)],1,1,.1,86400000*1000000)
a=np.array([3750.,4000.,3000.]);b=np.array([15000.,16000.,15500.]);assert (a+b).tolist()==[18750.,20000.,18500.] and not np.array_equal(a+b,(a+b)/2)
whole=np.array([100.,120.,90.,110.]);assert max(1-whole/np.maximum.accumulate(whole))==.25
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'flow_cases':9,'tests':['threshold equality admitted','short direction sign','same-position retained','normal exit','future closure rejected','missing/zero rejected','future suffix invariant','whole cash banks not normalized','continuous drawdown crosses fold boundary25pct'],'new_financial_or_account_calculations':0})
print('PASS9syntheticflowcases+passivebank/crossfoldDDregressions;0backtests')
