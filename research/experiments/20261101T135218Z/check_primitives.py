import json,copy
import numpy as np
from decimal import Decimal as D
from fractions import Fraction as F
from common import *
import engine
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());assert p['lookbacks']==[3,4,5] and p['fast_hurdles']==[.02,.025,.03] and len(batch)==12
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text())
 if row['scope']=='parent':assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['component_capitals_usdt']==[3750,15000] and sp['parameters']['component_initial_entry_notionals_usdt']==[375,4500] and row['capital_usdt']==18750
 else:assert sp['parameters']['lookback_days'] in [3,5] and sp['parameters']['initial_capital_usdt']==15000 and sp['parameters']['fixed_entry_notional_usdt']==4500
base=json.loads((ROOT/next(x['spec'] for x in batch if x['scope']=='native')).read_text());checks=[]
for L in [3,5]:
 sp=copy.deepcopy(base);sp['parameters'].update(lookback_days=L,return_hurdle=.02);closes=[D(60)]*17+[D(100)]*27+[D(88)];wanted,a=engine.decide(sp,{'asset':'ETH','closes':closes},45,0);assert wanted==1 and F(a['return_exact'])==-F(3,25) and a['raw_desired_before_entry_filter']==1;checks.append([L,'fastnegative-slowpositivecausallong'])
 closes[-1]=D('100.25');wanted,a=engine.decide(sp,{'asset':'ETH','closes':closes},45,1);assert wanted==0 and F(a['return_exact'])==F(1,400) and a['raw_desired_before_entry_filter']==0;checks.append([L,'longexit-equality-.0025'])
assert engine.entry_filter(1,0,.045,.045)==1 and engine.entry_filter(1,0,.0450001,.045)==0 and engine.entry_filter(0,1,1,.045)==0 and engine.entry_filter(1,1,1,.045)==1
a=np.array([3750.,3800.,3700.]);b=np.array([15000.,14900.,15100.]);assert (a+b).tolist()==[18750.,18700.,18800.] and not np.array_equal(a+b,.2*a+.8*b)
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':checks+['entryfilterequality/retainedq/exit','raw1/1dollarsumnotdoublecapitalweight'],'actual_market_backtests':0});print('PASS newL3/L5signal/exit-boundary/entryfilter andnativebank/dollarsumprimitives')
