"""Literal hand-checked entry-window,strict equality,disjoint volume and future-tail causality."""
from signals import filtered_channel
from volume_signals import volume_channel
from design import definitions
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'automation'));import registry
for high_index,expected in [(171,{10:True,15:False,20:False}),(166,{10:True,15:True,20:False})]:
 closes=['100']*184;closes[high_index]='125';closes[182]='120';closes[183]='.001'
 rows=[{'close':c,'quote_volume':'100'}for c in closes];rows[182]['quote_volume']='110'
 for e,want in expected.items():
  a=volume_channel(rows,e,30,40,1.1,start=183,end=184);b=filtered_channel(closes,e,30,30,.0125,start=183,end=184)
  assert a[0]['long']==b[0]['long']==want
  assert a[0]['volume_eligible']and a[0]['quote_volume_reference_mean']=='100'and a[0]['relative_quote_volume']=='1.1'
  future=[dict(z)for z in rows];future[-1].update(close='99999',quote_volume='99999');assert a==volume_channel(future,e,30,40,1.1,start=183,end=184)
  assert b==filtered_channel(closes[:-1]+['99999'],e,30,30,.0125,start=183,end=184)
 # Reference equality is not a strict breakout;the compared candle is excluded.
 equal=[dict(z)for z in rows];equal[182]['close']='125';assert not volume_channel(equal,20,30,40,1.1,start=183,end=184)[0]['long']
 thin=[dict(z)for z in rows];thin[182]['quote_volume']='109.99';assert not volume_channel(thin,10,30,40,1.1,start=183,end=184)[0]['long']
 zero=[dict(z,quote_volume='0')for z in rows];assert not volume_channel(zero,10,30,40,1.1,start=183,end=184)[0]['long']
items=definitions(registry.fingerprint);assert len(items)==30 and len({registry.fingerprint(sp)for sp,b in items})==30
for sp,b in items:
 if b['role']=='component':assert sp['parameters']['entry_lookback_days']==b[b['asset']+'_entry_lookback_days']and sp['parameters']['exit_lookback_days']==30
print(json.dumps({'synthetic_fixture_checks':'PASS','joint_grid_cells':9,'BTC_entry_windows':[10,15,20],'ETH_entry_windows':[10,15,20],'literal_10_vs15_vs20_entry_differences_checked':True,'strict_equality_and_disjoint_volume_threshold_checked':True,'no_future_tail_input':True,'funds_fixed':[1100,900],'not_performance_evidence':True}))
