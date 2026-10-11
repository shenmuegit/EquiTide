"""Handexpected independentETHentry/exit bands;synthetic only,not performance."""
from signals import asymmetric_filtered_channel as signal,filtered_channel
from design import definitions
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'automation'));import registry
base=['100']*185;base[182]='101.3'
for entry,want in((.01,True),(.0125,False),(.015,False)):
 a=signal(base,15,30,30,entry,.03,start=183,end=184);assert a[0]['long']==want and a[0]['channel_entry']
 assert abs(a[0]['EMA_prior']-(100+2/31*1.3))<1e-12
 tail=base.copy();tail[-1]='99999';assert a==signal(tail,15,30,30,entry,.03,start=183,end=184)
rows=['100']*185;rows[160]='80';rows[182]='102';rows[183]='97.5'
for exit,want in((.02,[True,False]),(.03,[True,True]),(.04,[True,True])):
 a=signal(rows,15,30,30,.0125,exit,start=183,end=185);assert[z['long']for z in a]==want and not a[1]['channel_exit'];assert a[1]['EMA_exit']==(exit==.02)
rows=['100']*185;rows[181]='110';rows[182]='105';rows[183]='104';a=signal(rows,15,30,30,.0125,.03,start=183,end=185);assert all(z['EMA_entry']and not z['channel_entry']and not z['long']for z in a)
assert signal(rows,15,30,30,.0125,.0125,start=183,end=185)==filtered_channel(rows,15,30,30,.0125,start=183,end=185)
assert not signal(['100']*185,15,30,30,.0125,.03,start=183,end=184)[0]['long']
items=definitions(registry.fingerprint);assert len(items)==len({registry.fingerprint(sp)for sp,b in items})==38
print(json.dumps({'synthetic_fixture_checks':'PASS','ETH_joint_grid_cells':9,'ETH_EMA_span_fixed':30,'ETH_entry_bands':[.01,.0125,.015],'ETH_exit_bands':[.02,.03,.04],'hand_expected_independent_entry_exit_differences':True,'EMA_only_exit_without_channel_exit':True,'joint_channel_gate_no_delayed_arming':True,'symmetric_rule_equivalence_in_synthetic_fixture_only':True,'no_future_tail_input':True,'funds_fixed':[1100,900],'not_performance_evidence':True}))
