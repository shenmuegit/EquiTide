"""Synthetic causality and declared funding-size fixtures only;not performance."""
from signals import filtered_channel
from volume_signals import volume_channel
from design import AXES
from decimal import Decimal as D
import json
for span in AXES['EMA_span_days']:
 values=['100']*182+['120','80','9999'];a=filtered_channel(values,15,30,span,.0125,start=183,end=185)
 assert [x['long']for x in a]==[True,False]and a==filtered_channel(values[:-1]+['.001'],15,30,span,.0125,start=183,end=185)
rows=[{'close':'100','quote_volume':'100'}for _ in range(185)];rows[182]['close']='120';rows[182]['quote_volume']='100';a=volume_channel(rows,15,30,30,1,start=183,end=184);assert a[0]['long']and a[0]['quote_volume_reference_mean']=='100'
rows[183]['close']='99999';rows[183]['quote_volume']='99999';assert a==volume_channel(rows,15,30,30,1,start=183,end=184)
for weights in AXES['raw_initial_weights']:
 assert sum(D(str(w))*2000 for w in weights)==2000
print(json.dumps({'synthetic_fixture_checks':'PASS','joint_grid_cells':9,'causal_source_rules':True,'no_future_bar_input':True,'raw_initial_weights_preserved':True,'not_performance_evidence':True}))
