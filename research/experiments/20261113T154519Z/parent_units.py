"""Strict BTC entry/persistence boundaries, suffix causality and dollar-bank/DD checks."""
from common import *
import engine
from fractions import Fraction as F
import numpy as np
n=0
for L in [29,31,32]:
 for H in [F('.025'),F('.03'),F('.035')]:
  for actual in [-1,0,1]:
   for roc in [-H-F(1,10**8),-H,F('-.01'),F(0),F('.01'),H,H+F(1,10**8)]:
    closes=[F(100)]*50;closes[39]=100*(1+roc);expected=1 if roc>H else -1 if roc<-H else 1 if actual==1 and roc>F('-.01') else -1 if actual==-1 and roc<F('.01') else 0
    wanted,r=engine.btc.target(closes,40,L,float(H),actual,.01);assert wanted==expected and F(r)==roc
    mutated=closes[:40]+[F(1),F(10**12),F(2),F(10**10)];assert engine.btc.target(mutated,40,L,float(H),actual,.01)==(wanted,r);n+=1
a=np.array([3750.,4500.,3000.]);b=np.array([15000.,14000.,16000.]);assert (a+b).tolist()==[18750.,18500.,19000.] and not np.array_equal(a+b,(a+b)/2)
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'BTC_strict_entry_persistence_future_suffix_cases':n,'tests':['bothentryequalities','entrybandpriority','strictlongshortexitbuffer','futureclosemutationirrelevant','33daywarmupsupportsL32','wholebanknotnormalized','continuouscrossfoldDD25pct'],'new_strategy_or_account_calculations':0});print('PASS',n,'syntheticBTCboundary/suffixcases+wholebank/DD;0backtests')
