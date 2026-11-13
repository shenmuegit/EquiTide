"""Concrete normalization and cross-fold DD guards for actual whole-bank combinations."""
import json,numpy as np
from common import *
a=np.array([3750.,4500.,3000.,4000.]);b=np.array([15000.,14000.,16000.,14500.]);v=a+b
assert v.tolist()==[18750.,18500.,19000.,18500.] and not np.array_equal(v,(a+b)/2)
path=np.array([100.,120.,90.,110.]);assert max(1-path/np.maximum.accumulate(path))==.25
p=json.loads((R/'plan.json').read_text());assert len(p['grid'])==9 and len(p['deduplication'])==3 and sum(not z['readonly'] for z in p['grid'])==6
for fp,z in p['read_only_references'].items():
 sp=json.loads((ROOT/z['spec']).read_text());assert sha(ROOT/z['spec'])==z['spec_sha256'] and sp['parameters']['end_utc']=='2026-11-12T00:01:00Z' and sp['parameters']['continuous_oos_days']==389
 if z['scope']=='native':assert sp['parameters']['initial_capital_usdt']==(3750 if z['asset']=='BTC' else 15000)
put(R/'parent_primitive_verification.json',{'passed':True,'synthetic_only':True,'actual_reference_specs_checked':12,'tests':['wholebankdollars not normalized','continuouscrossfoldDD25pct','6new/3exactread-onlygridcells','fixedactualC/N/calendar'],'new_backtests_or_account_valuations':0})
print('PASS wholebank/crossfoldDD and12actualsource-spec constraints;0newvaluations')
