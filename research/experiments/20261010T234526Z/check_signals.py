"""Hand-checked disjoint volume threshold equality and future-input fixtures, not returns."""
from decimal import Decimal as D
from volume_signals import volume_channel
from signals import filtered_channel
from design import AXES
import json
for n in AXES['BTC_volume_lookback_days']:
 for ratio in AXES['BTC_minimum_volume_ratio']:
  rows=[{'close':'100','quote_volume':'100'}for _ in range(186)];rows[182].update(close='120',quote_volume=str(D(100)*D(str(ratio))))
  a=volume_channel(rows,15,30,n,ratio,start=183,end=184);assert a[0]['long']and a[0]['quote_volume_reference_mean']=='100'and a[0]['volume_eligible']
  rows[183].update(close='99999',quote_volume='99999');assert a==volume_channel(rows,15,30,n,ratio,start=183,end=184)
  rows[182]['quote_volume']=str(D(100)*D(str(ratio))-D('.01'));assert not volume_channel(rows,15,30,n,ratio,start=183,end=184)[0]['long']
  rows[182]['quote_volume']=str(D(100)*D(str(ratio)));rows[183].update(close='80',quote_volume='0');assert [x['long']for x in volume_channel(rows,15,30,n,ratio,start=183,end=185)]==[True,False]
values=['100']*182+['120','80','9999'];a=filtered_channel(values,15,30,30,.0125,start=183,end=185);assert [x['long']for x in a]==[True,False]and a==filtered_channel(values[:-1]+['.001'],15,30,30,.0125,start=183,end=185)
print(json.dumps({'synthetic_fixture_checks':'PASS','joint_grid_cells':9,'BTC_disjoint_volume_windows':[20,30,40],'minimum_ratios':[.9,1,1.1],'ETH_frozen_span':30,'threshold_equality_and_exit_priority':True,'no_future_bar_input':True,'not_performance_evidence':True}))
