"""Synthetic expiry regression: exact day ages, closing priority, no same-decision re-entry."""
import copy
from decimal import Decimal as D
from common import *
import engine
base={'parameters':{'lookback_days':3,'trend_lookback_days':28,'entry_volatility_window_days':10,'entry_volatility_ceiling':.045,'exit_buffer_fraction':.0025,'return_hurdle':.025,'max_holding_days':3}}
m={'asset':'ETH','closes':[D(60)]*25+[D(100)]*19+[D(96)]}
assert engine.decide(base,m,45,1,held_age_days=3)[0]==0,'Existing long must expire on age3 despite unchanged long signal'
cases=[]
for L in [3,4,5]:
 for cap in [3,7,None]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,max_holding_days=cap)
  assert engine.decide(sp,m,45,0,held_age_days=None)[0]==1
  ages=[0,2,3,6,7,8]
  for age in ages:
   wanted,a=engine.decide(sp,m,45,1,held_age_days=age);expired=cap is not None and age>=cap
   assert wanted==(0 if expired else 1) and a['held_age_days']==age and a['max_holding_days']==cap and a['holding_limit_applied']==expired and a['desired_before_holding_limit']==1
   future=copy.deepcopy(m);future['closes'].extend([D('999999'),D('.001')]);assert engine.decide(sp,future,45,1,held_age_days=age)==(wanted,a)
   short={'asset':'ETH','closes':[D(200)]*25+[D(100)]*19+[D(104)]};assert engine.decide(sp,short,45,-1,held_age_days=age)[0]==(0 if expired else -1)
   assert engine.decide(sp,m,45,-1,held_age_days=age)[0]==(0 if expired else 1),'Expiry must suppress same-decision reversal re-entry'
  exitm=copy.deepcopy(m);exitm['closes'][-1]=D('100.25');assert engine.decide(sp,exitm,45,1,held_age_days=0)[0]==0
  cases.append({'L':L,'max_holding_days':cap,'ages':ages,'expiry_priority_and_no_same_decision_reentry':True,'future_invariance':True,'earlier_original_exit_unchanged':True})
for age in [None,-1,1.5]:
 try:engine.decide(base,m,45,1,held_age_days=age)
 except AssertionError:pass
 else:raise AssertionError('Open position requires valid actual integer age')
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.045001,.045)==0
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':cases,'extra_checks':['exact expiry boundary','flat ageNone enters normally','expiry prevents reversal entry','open age required/integer/nonnegative','vol boundary']})
print('PASS L3/4/5 x holding3/7/OFF, exact expiry, same-day flat, valid ages, original exits and future-invariance')
