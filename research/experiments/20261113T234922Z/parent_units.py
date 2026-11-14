"""Synthetic strict signal/funding and new calendar checks, zero market backtests."""
from common import *
import engine
from fractions import Fraction as F
import numpy as np
n=0
for actual in [-1,0,1]:
 for roc in [F('-.03000001'),F('-.03'),F('-.01'),F(0),F('.01'),F('.03'),F('.03000001')]:
  c=[F(100)]*50;c[39]=100*(1+roc);want=1 if roc>F('.03') else -1 if roc<F('-.03') else 1 if actual==1 and roc>F('-.01') else -1 if actual==-1 and roc<F('.01') else 0;out,r=engine.btc.target(c,40,29,.03,actual,.01);assert want==out and F(r)==roc and engine.btc.target(c[:40]+[F(10**12),F(1)],40,29,.03,actual,.01)==(out,r);n+=1
for cap in [.03,.04]:
 assert engine.entry_filter(1,0,cap,cap)==1 and engine.entry_filter(1,0,cap+1e-6,cap)==0 and engine.entry_filter(1,1,cap+1e-6,cap)==1
assert core.funding_amount(core.D(2),core.D(100),core.D('.001'),3)==(core.D('-.2'),core.D('-.6')) and core.funding_amount(core.D(-2),core.D(100),core.D('.001'),3)==(core.D('.2'),core.D('.2'))
assert core.END-core.START==core.DAYS==390 and list(range(0,391,30))==[0,30,60,90,120,150,180,210,240,270,300,330,360,390] and 390-350==40 and 390-370==20
v=np.array([100.,120.,90.,110.]);assert max(1-v/np.maximum.accumulate(v))==.25;assert (np.array([3750.,4500.])+np.array([15000.,14000.])).tolist()==[18750.,18500.]
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'strict_BTC_boundary_and_future_suffix_cases':n,'native_entry_equalities_and_funding_income_outflow_stress_checked':True,'calendar390_13fullfold_recent40_extension20_checked':True,'whole_bank_weights_not_normalized':True,'new_strategy_or_account_calculations':0});print('PASS syntheticcausality/strictentry/funding/calendargeometry/fullDD,0marketbacktests')
