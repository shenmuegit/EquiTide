"""Synthetic timing/state fixture only;not strategy-performance evidence."""
from pathlib import Path
from decimal import Decimal as D
import importlib.util,copy,json
s=importlib.util.spec_from_file_location('volume_signal',Path(__file__).with_name('signals.py'));signal=importlib.util.module_from_spec(s);s.loader.exec_module(signal)
assert callable(getattr(signal,'volume_channel',None)),'volume_channel not implemented'
rows=[{'close':'100','quote_volume':'100'}for _ in range(70)]
for j,c,v in [(39,'110','200'),(40,'109','1'),(41,'90','100'),(42,'120','1')]:rows[j].update(close=c,quote_volume=v)
rows[43].update(close='121',quote_volume=str(sum(D(q['quote_volume']) for q in rows[23:43])/20))
a=signal.volume_channel(rows,15,30,20,1,start=40,end=45)
assert [d['long']for d in a]==[True,True,False,False,True]
assert D(a[0]['quote_volume_reference_mean'])==100 and D(a[0]['quote_volume_prior'])==200 and D(a[-1]['relative_quote_volume'])==1 and a[-1]['volume_eligible']
assert not a[1]['volume_eligible'] and a[1]['long'] and a[2]['action']=='exit'
changed=copy.deepcopy(rows)
for j in range(44,len(changed)):changed[j]={'close':'999999','quote_volume':'999999999999'}
assert signal.volume_channel(changed,15,30,20,1,start=40,end=45)==a
zero=[{'close':q['close'],'quote_volume':'0'}for q in rows];b=signal.volume_channel(zero,15,30,20,1,start=40,end=45);assert not any(d['long']for d in b) and all(d['relative_quote_volume'] is None for d in b)
print(json.dumps({'synthetic_fixture_checks':'PASS','tested_close_and_volume_excluded_from_reference':True,'threshold_equality_qualifies':True,'low_volume_preserves_long_until_unfiltered_exit':True,'future_prefix_invariant':True,'zero_reference_disables_entry':True,'not_performance_evidence':True}))
