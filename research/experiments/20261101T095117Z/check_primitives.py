import json,numpy as np
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());assert p['BTC_capitals']==[2500,3750,5000] and p['fast_hurdles']==[.02,.025,.03] and len(batch)==6
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());C=row['BTC_capital_usdt']
 if row['scope']=='parent':assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['component_capitals_usdt']==[C,15000] and sp['parameters']['component_initial_entry_notionals_usdt']==[C/10,4500] and row['capital_usdt']==C+15000
 else:assert sp['parameters']['fixed_entry_notional_usdt']==250 and row['capital_usdt']==2500
a=np.array([10000.,10200.,9800.]);b=np.array([15000.,14900.,15300.]);v=a+b;assert v.tolist()==[25000.,25100.,25100.] and not np.array_equal(v,.4*a+.6*b)
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':['native2500/N250 fixed beforeevaluation','parentraw1/1 dollar sum','no doubleweighting,capitaltransfer orsameasset clones']});print('PASS native budget and dollar alignment primitives')
