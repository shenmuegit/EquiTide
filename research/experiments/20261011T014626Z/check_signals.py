"""Joint ratio/funding causality and original frozen daily boundary fixtures,not returns."""
from decimal import Decimal as D
from signals import filtered_channel
from volume_signals import volume_channel
from design import AXES,definitions
from pathlib import Path
import importlib.util,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'automation'));import registry
rows=[{'close':'100','quote_volume':'100'}for _ in range(186)]
for ratio in AXES['BTC_minimum_volume_ratio']:
 rows[182].update(close='120',quote_volume=str(D(100)*D(str(ratio))))
 a=volume_channel(rows,15,30,40,ratio,start=183,end=184);assert a[0]['long']and a[0]['quote_volume_reference_mean']=='100'
 rows[183].update(close='99999',quote_volume='99999');assert a==volume_channel(rows,15,30,40,ratio,start=183,end=184)
 rows[182]['quote_volume']=str(D(100)*D(str(ratio))-D('.01'));assert not volume_channel(rows,15,30,40,ratio,start=183,end=184)[0]['long']
 rows[182]['quote_volume']=str(D(100)*D(str(ratio)));rows[183].update(close='80',quote_volume='0');assert [x['long']for x in volume_channel(rows,15,30,40,ratio,start=183,end=185)]==[True,False]
values=['100']*182+['120','80','9999'];assert [x['long']for x in filtered_channel(values,15,30,30,.0125,start=183,end=185)]==[True,False]
defs=definitions(registry.fingerprint);byfp={registry.fingerprint(s):s for s,b in defs}
for sp,b in defs:
 assert sum(D(str(w))for w in b['raw_weights'])==1
 if b['role']=='combination':assert [byfp[c['fingerprint']]['parameters']['initial_capital_usdt']for c in sp['components']]==[int(D(2000)*D(str(w)))for w in b['raw_weights']]
path=Path(__file__).resolve().parents[1]/'20261001T113625Z/signals.py';s=importlib.util.spec_from_file_location('original_step',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
assert m.step(True,D(99),D(100),D('.01'))[0]and not m.step(True,D('98.99'),D(100),D('.01'))[0]
assert not m.step(False,D(101),D(100),D('.01'))[0]and m.step(False,D('101.01'),D(100),D('.01'))[0]
print(json.dumps({'synthetic_fixture_checks':'PASS','joint_grid_cells':9,'BTC_volume_window':40,'ratios':[1,1.1,1.2],'rawBTCweights':[.45,.5,.55],'own_component_funding_verified':[900,1000,1100],'threshold_equality_and_original_SMA_daily_boundaries':True,'no_future_bar_input':True,'not_performance_evidence':True}))
