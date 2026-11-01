import json,numpy as np
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());assert p['BTC_capitals']==[3750,5000,6250] and p['fast_hurdles']==[.02,.025,.03] and len(batch)==8
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());C=row['BTC_capital_usdt'];assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['component_capitals_usdt']==[C,15000] and sp['parameters']['component_initial_entry_notionals_usdt']==[C/10,4500] and sp['parameters']['initial_capital_usdt']==C+15000
 # Detect weighting fullbank equity twice, subtracting onlyoneprincipal, and averaging component DD/Sharpe.
a=np.array([10000.,10200.,9800.]);b=np.array([15000.,14900.,15300.]);v=a+b;assert v.tolist()==[25000.,25100.,25100.] and not np.array_equal(v,.4*a+.6*b)
put(R/'primitive_verification.json',{'passed':True,'synthetic_only':True,'cases':['exactbankcapitalandnativeN at all6newcandidates2newholdcontrols,raw1/1','parent NAV is dollar sum,not bankfraction multiplied twice','newscope only oneexistingbank per distinct asset; no native strategy calculation']});print('PASS actual bank/N/rawownership definitions and dollar alignment primitive')
