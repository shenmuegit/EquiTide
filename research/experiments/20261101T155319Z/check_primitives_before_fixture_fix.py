import copy,json
import numpy as np
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());assert p['lookbacks']==[3,4,5] and p['slow_windows']==[24,28,32] and p['fixed_entry_hurdle']==.025 and len(batch)==12
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text())
 if row['scope']=='parent':assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['component_capitals_usdt']==[3750,15000] and sp['parameters']['component_initial_entry_notionals_usdt']==[375,4500] and row['capital_usdt']==18750
 else:assert sp['parameters']['trend_lookback_days'] in [24,32] and sp['parameters']['lookback_days'] in [3,4,5] and sp['parameters']['initial_capital_usdt']==15000 and sp['parameters']['fixed_entry_notional_usdt']==4500
base=json.loads((ROOT/next(x['spec'] for x in batch if x['scope']=='native')).read_text());checks=[]
for L in [3,4,5]:
 for S in [24,28,32]:
  sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,trend_lookback_days=S);cl=[D(60)]*17+[D(100)]*27+[D(88)];want,a=engine.decide(sp,{'asset':'ETH','closes':cl},45,0);assert want==1 and F(a['return_exact'])==-F(3,25) and F(a['slow_return_exact'])==F(88,60)-1
  cl[-1]=D('100.25');want,a=engine.decide(sp,{'asset':'ETH','closes':cl},45,1);assert want==0 and F(a['return_exact'])==F(1,400) and a['raw_desired_before_entry_filter']==0;checks.append([L,S,'causallong-and-exit-equality'])
  cl=[D(200)]*25+[D(100)]*19+[D(112)];want,a=engine.decide(sp,{'asset':'ETH','closes':cl},45,0);assert want==-1 and F(a['slow_return_exact'])==F(112,200)-1
sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=5,trend_lookback_days=32);cl=[D(60)]+[D(100)]*31+[D(88)];want,a=engine.decide(sp,{'asset':'ETH','closes':cl},33,0);assert want==1 and F(a['slow_return_exact'])==F(88,60)-1;checks.append(['i33','S32','oldestclosedwarmupindex0,no negativeindex'])
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.0450001,.045)==0 and engine.entry_filter(0,1,1,.045)==0 and engine.entry_filter(1,1,1,.045)==1
a=np.array([3750.,3800.,3700.]);b=np.array([15000.,14900.,15100.]);assert (a+b).tolist()==[18750.,18700.,18800.] and not np.array_equal(a+b,.2*a+.8*b)
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_market_backtests':0,'cases':checks+['entryfilterequality/retainedq/exit','raw1/1dollarsum']});print('PASS L/Sdirection/exit/oldestS32warmup/entryfilter andrawbankownership primitives')
