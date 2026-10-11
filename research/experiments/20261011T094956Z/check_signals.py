"""Literal asymmetric-band gates,independent exitwidth,no delayedarming/futuretail;not returns."""
from volume_ema_signals import volume_ema_channel
from design import definitions
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'automation'));import registry
base=[{'close':'100','quote_volume':'100'}for _ in range(185)];base[182].update(close='101.06',quote_volume='110')
for entry,want in[(.005,True),(.01,False),(.015,False)]:
 a=volume_ema_channel(base,15,30,40,1.1,20,entry,.03,start=183,end=184);assert a[0]['long']==want and a[0]['volume_eligible']and a[0]['quote_volume_reference_mean']=='100'and a[0]['relative_quote_volume']=='1.1'
 assert abs(a[0]['EMA_prior']-(100+2/21*1.06))<1e-12
 future=[dict(z)for z in base];future[-1].update(close='.001',quote_volume='99999');assert a==volume_ema_channel(future,15,30,40,1.1,20,entry,.03,start=183,end=184)
rows=[dict(z)for z in base];rows[182]['close']='102';assert volume_ema_channel(rows,15,30,40,1.1,20,.015,.03,start=183,end=184)[0]['long']
rows[160]['close']='80';rows[183].update(close='97.5',quote_volume='0')
for exit,want in[(.02,[True,False]),(.03,[True,True]),(.04,[True,True])]:
 a=volume_ema_channel(rows,15,30,40,1.1,20,.005,exit,start=183,end=185);assert[z['long']for z in a]==want and not a[1]['channel_exit']and not a[1]['volume_eligible'];assert a[1]['EMA_exit']==(exit==.02)
rows[183]['close']='101.07';a=volume_ema_channel(rows,15,30,40,1.1,20,.005,.02,start=183,end=185);assert[z['long']for z in a]==[True,True]and not a[1]['volume_eligible']
rows=[dict(z)for z in base];rows[182]['quote_volume']='109.99';rows[183].update(close='101.06',quote_volume='111');a=volume_ema_channel(rows,15,30,40,1.1,20,.005,.03,start=183,end=185);assert[z['long']for z in a]==[False,False]and a[0]['EMA_entry']and not a[0]['volume_eligible']and a[1]['volume_eligible']and not a[1]['price_breakout']
future=[dict(z)for z in rows];future[-1].update(close='99999',quote_volume='0');assert a==volume_ema_channel(future,15,30,40,1.1,20,.005,.03,start=183,end=185)
zero=[dict(z,quote_volume='0')for z in base];assert not volume_ema_channel(zero,15,30,40,1.1,20,.005,.03,start=183,end=184)[0]['long']
items=definitions(registry.fingerprint);assert len(items)==42 and len({registry.fingerprint(sp)for sp,b in items})==42
print(json.dumps({'synthetic_fixture_checks':'PASS','BTC_joint_grid_cells':9,'BTC_EMA_span':20,'BTC_EMA_entry_bands':[.005,.01,.015],'BTC_EMA_exit_bands':[.02,.03,.04],'hand_expected_entry_differences':True,'hand_expected_independent_exitwidth_differences':True,'EMA_only_exit_without_channel_exit':True,'low_volume_alone_preserves_position':True,'no_delayed_arming':True,'disjoint_volume_threshold_equality':True,'no_future_tail_input':True,'funds_fixed':[1100,900],'not_performance_evidence':True}))
