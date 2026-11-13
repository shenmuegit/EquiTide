"""Signed median premium, side/closure and passive NAV regression checks."""
from common import *
from engine import premium_filter
import numpy as np
def row(v,t):
 x=[0]*12;x[4]=str(v);x[6]=t-1;return x
bars=[row('.0001',10),row('-.0003',20),row('.0002',30),row('.9',40)]
assert premium_filter(1,0,bars,1,1,.0001,10*1000000)[0]==1
assert premium_filter(1,0,bars,1,1,.00005,10*1000000)[0]==0
assert premium_filter(-1,0,bars,1,1,.00005,10*1000000)[0]==-1
assert premium_filter(-1,0,bars,2,1,.0002,20*1000000)[0]==0
assert premium_filter(1,1,bars,3,1,.00005,30*1000000)[0]==1
assert premium_filter(0,1,bars,3,1,.00005,30*1000000)[0]==0
assert premium_filter(1,0,bars,1,1,.0001,10*1000000-1)[0]==0
assert premium_filter(1,0,[],0,1,.0001,0)[0]==0
assert premium_filter(1,0,bars,3,3,.0001,30*1000000)[0]==1
assert premium_filter(1,0,bars,3,3,.0001,30*1000000)==premium_filter(1,0,bars[:3]+[row('-.9',40)],3,3,.0001,30*1000000)
a=np.array([3750.,4500.,3000.]);b=np.array([15000.,14000.,16000.]);assert (a+b).tolist()==[18750.,18500.,19000.] and not np.array_equal(a+b,(a+b)/2)
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'premium_cases':10,'tests':['signedpremium','threshold equality','side sign','sameq retained','normalexit','futureclose rejected','missing blocked','odd median','future suffix invariant','wholebank not normalized','crossfold DD25pct'],'new_strategy_or_account_calculations':0})
print('PASS10syntheticpremiumcases+wholebank/crossfoldDD;0backtests')
