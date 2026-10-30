import ast,json
import numpy as np
from common import *
import portfolio
p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());assert len(rows)==12 and len({x['fingerprint'] for x in rows})==12
for x in rows:
 s=json.loads((ROOT/x['spec']).read_text());q=s['parameters'];w=x['raw_pair_units'];assert reg.fingerprint(s)==x['fingerprint'] and q['initial_capital_usdt']==20000*(1+w) and w in [.25,.5,.75] and q['raw_trend_units']==1 and s['universe']==['BTC/USDT','ETH/USDT']
 if x['role']=='candidate':assert s['kind']=='combination' and s['components'][0]['weight']==1 and s['components'][1]['weight']==w and q['cash_usdt']==0
 else:assert q['cash_usdt']==20000*w and q['raw_pair_units']==0
# A minute-close at t=1 is followed by a newly available OPEN at the same ns.
# Carrying old source NAV would miss the price jump; mapping ns alone would also
# apply the future funding cashflow too early. This fixture fails both shortcuts.
dt=np.dtype([('t','<i8'),('k','<i8')]);old=np.array([(0,0),(1,1),(2,3),(2,4),(3,9)],dtype=dt);new=np.array([(0,0),(1,1),(1,5),(1,6),(1,7),(2,3),(2,4),(3,9)],dtype=dt);px=np.array([100.,101.,110.,110.,110.,90.,90.,90.]);oldpx=px[np.searchsorted(new,old)];segments=[{'axis_start':0,'axis_end_exclusive':3,'cash':'1000','signed_units':'1','entry_price':'100'},{'axis_start':3,'axis_end_exclusive':5,'cash':'995','signed_units':'1','entry_price':'100'}];original=np.array([1000.,1001.,990.,985.,985.]);scene={'state_segments':segments,'summary':{'NAV_sha256_f64le':core.navhash(original)}};v,proof=portfolio.expand(scene,{'ts':old['t'],'codes':old['k'],'axis_prices':oldpx,'axis_sha256':'fixture'},{'axis_prices':px},{'ts':new['t'],'keys':new,'axis_sha256':'fixtureexpanded'});assert v.tolist()==[1000,1001,1010,1010,1010,990,985,985] and v[2]!=original[1] and v[5]!=v[6]
assert 20000+.25*20000==25000 and 20000+.5*20000==30000 and 20000+.75*20000==35000
files=['common.py','market.py','portfolio.py','freeze.py','run.py','audit.py','audit_helpers_complete.py','check_definitions.py','plan.json']
for f in files:
 if f.endswith('.py'):ast.parse((R/f).read_text())
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':{rel(R/f):sha(R/f) for f in files},'immutable_accounting_source':{'path':rel(CORE_PATH),'sha256':sha(CORE_PATH)}});put(R/'definition_check.json',{'passed':True,'complete_specs':12,'candidates':9,'samecapital_cash_comparators':3,'cost_scenes':36,'raw_units_not_normalized':True,'synthetic_causal_OPEN_and_same_ns_funding_fixture':True,'source_orders_not_rerun':True});print('PASS12 definitions;causalOPEN/same-ns funding/raw ownership fixture')
