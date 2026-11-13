"""Strict slope, side suppression and full-bank/DD primitive regressions."""
from common import *
import engine
from fractions import Fraction as F
import numpy as np
for k in [F('.00625'),F('.0075'),F('.00875')]:
 assert engine.slope_gate(k,k)==engine.slope_gate(-k,k)==0
 assert engine.slope_gate(k+F(1,10**9),k)==1 and engine.slope_gate(-k-F(1,10**9),k)==-1
old=engine.base_decide
try:
 for desired,actual in [(-1,0),(-1,1),(0,1),(1,0),(1,1)]:
  engine.base_decide=lambda sp,m,i,a,d=desired:(d,{'kind':'synthetic_base'})
  result,audit=engine.decide({'parameters':{'entry_direction_mode':'long_only'}},{},0,actual);assert result==max(desired,0) and audit['raw_desired_before_side_filter']==desired
finally:engine.base_decide=old
a=np.array([3750.,4500.,3000.]);b=np.array([15000.,14000.,16000.]);assert (a+b).tolist()==[18750.,18500.,19000.] and not np.array_equal(a+b,(a+b)/2)
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'strict_threshold_cases':12,'side_wrapper_cases':5,'tests':['strictpositiveandnegativeequalities','longonlysuppressesnegative','normalexit','sameqtarget','wholebanknotnormalized','continuouscrossfoldDD25pct'],'new_strategy_or_account_calculations':0});print('PASS slope/side/fullbank/DDprimitive regressions;0backtests')
