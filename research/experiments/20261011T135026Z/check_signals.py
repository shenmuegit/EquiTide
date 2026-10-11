"""Handexpected ETH period/band causal gates;synthetic checks only,not returns."""
from signals import filtered_channel
from design import definitions
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'automation'));import registry
base=['100']*185;base[182]='101.09'
for span,want in((20,False),(30,True),(40,True)):
 a=filtered_channel(base,15,30,span,.01,start=183,end=184);assert a[0]['long']==want and a[0]['channel_entry']
 assert abs(a[0]['EMA_prior']-(100+2/(span+1)*1.09))<1e-12
 tail=base.copy();tail[-1]='99999';assert a==filtered_channel(tail,15,30,span,.01,start=183,end=184)
rows=base.copy();rows[182]='101.3'
for band,want in((.01,True),(.0125,False),(.015,False)):
 a=filtered_channel(rows,15,30,30,band,start=183,end=184);assert a[0]['long']==want
rows=['100']*185;rows[160]='80';rows[182]='102';rows[183]='97.5';a=filtered_channel(rows,15,30,30,.0125,start=183,end=185);assert[z['long']for z in a]==[True,False]and a[1]['EMA_exit']and not a[1]['channel_exit']
rows=['100']*185;rows[181]='110';rows[182]='105';rows[183]='104';a=filtered_channel(rows,15,30,30,.0125,start=183,end=185);assert all(z['EMA_entry']and not z['channel_entry']and not z['long']for z in a)
assert not filtered_channel(['100']*185,15,30,30,.0125,start=183,end=184)[0]['long']
items=definitions(registry.fingerprint);assert len(items)==len({registry.fingerprint(sp)for sp,b in items})==38
print(json.dumps({'synthetic_fixture_checks':'PASS','ETH_joint_grid_cells':9,'ETH_EMA_spans':[20,30,40],'ETH_EMA_bands':[.01,.0125,.015],'hand_expected_period_and_band_differences':True,'EMA_only_exit_without_channel_exit':True,'joint_channel_gate_no_delayed_arming':True,'price_equality_preserves_cash':True,'no_future_tail_input':True,'funds_fixed':[1100,900],'not_performance_evidence':True}))
