"""Literal hand-checked exit-window differences and future-tail causality,not performance."""
from signals import filtered_channel
from volume_signals import volume_channel
from design import definitions
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'automation'));import registry
for low_days,expected in [(162,{20:[True,False],30:[True,True],40:[True,True]}),(151,{20:[True,False],30:[True,False],40:[True,True]})]:
 closes=['50']*low_days+['100']*(182-low_days)+['120','97','9999']
 rows=[{'close':c,'quote_volume':'100'}for c in closes];rows[182]['quote_volume']='110';rows[183]['quote_volume']='0'
 for x,want in expected.items():
  a=volume_channel(rows,15,x,40,1.1,start=183,end=185);b=filtered_channel(closes,15,x,30,.0125,start=183,end=185)
  assert [z['long']for z in a]==want and [z['long']for z in b]==want
  future=[dict(z)for z in rows];future[-1].update(close='.001',quote_volume='99999');assert a==volume_channel(future,15,x,40,1.1,start=183,end=185)
  assert b==filtered_channel(closes[:-1]+['.001'],15,x,30,.0125,start=183,end=185)
items=definitions(registry.fingerprint);assert len(items)==30 and len({registry.fingerprint(sp)for sp,b in items})==30
print(json.dumps({'synthetic_fixture_checks':'PASS','joint_grid_cells':9,'BTC_exit_windows':[20,30,40],'ETH_exit_windows':[20,30,40],'literal_20_vs30_vs40_exit_differences_checked':True,'no_future_tail_input':True,'funds_fixed':[1100,900],'not_performance_evidence':True}))
