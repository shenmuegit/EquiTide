"""Syntheticcausality fordeclared N/span axes only;notperformance."""
from signals import filtered_channel
from volume_signals import volume_channel
from design import AXES
import json
for n in AXES['BTC_volume_lookback_days']:
 rows=[{'close':'100','quote_volume':'100'}for _ in range(185)];rows[182]['close']='120';a=volume_channel(rows,15,30,n,1,start=183,end=184);assert a[0]['long']and a[0]['quote_volume_reference_mean']=='100'
 rows[183].update(close='99999',quote_volume='99999');assert a==volume_channel(rows,15,30,n,1,start=183,end=184)
for span in AXES['EMA_span_days']:
 values=['100']*182+['120','80','9999'];a=filtered_channel(values,15,30,span,.0125,start=183,end=185);assert [x['long']for x in a]==[True,False]and a==filtered_channel(values[:-1]+['.001'],15,30,span,.0125,start=183,end=185)
print(json.dumps({'synthetic_fixture_checks':'PASS','joint_grid_cells':9,'BTC_disjoint_volume_windows':[20,30,40],'ETH_spans':[30,33,35],'no_future_bar_input':True,'not_performance_evidence':True}))
