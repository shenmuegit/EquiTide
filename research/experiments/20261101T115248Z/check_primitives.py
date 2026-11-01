import json,numpy as np
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());assert p['BTC_capitals']==[3125,3750,4375] and p['fast_hurdles']==[.02,.025,.03] and len(batch)==12
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());C=row['BTC_capital_usdt']
 if row['scope']=='parent':assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['component_capitals_usdt']==[C,15000] and sp['parameters']['component_initial_entry_notionals_usdt']==[C/10,4500] and row['capital_usdt']==C+15000
 else:assert row['capital_usdt'] in [3125,4375] and sp['parameters']['fixed_entry_notional_usdt']==row['capital_usdt']/10
a=np.array([10000.,10200.,9800.]);b=np.array([15000.,14900.,15300.]);v=a+b;assert v.tolist()==[25000.,25100.,25100.] and not np.array_equal(v,.4*a+.6*b)
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':['native3125/N312.5 and4375/N437.5 fixedbeforeevaluation','parentraw1/1 dollar sum','no doubleweighting,capitaltransfer orsameasset clones']});print('PASS native budget and dollar alignment primitives')
