"""Synthetic causality fixtures only; never market performance or trial returns."""
import json
from signals import filtered_channel
from design import AXES
for span in AXES['EMA_span_days']:
 for band in AXES['EMA_symmetric_band']:
  values=['100']*182+['120','80','9999']
  a=filtered_channel(values,15,30,span,band,start=183,end=185)
  assert [x['long'] for x in a]==[True,False]
  assert [x['action'] for x in a]==['entry','exit']
  assert a==filtered_channel(values[:-1]+['0.0001'],15,30,span,band,start=183,end=185)
  assert a[0]['entry_channel_prior']=='100' and a[0]['prior_close']=='120'
  flat=filtered_channel(['100']*185,15,30,span,band,start=183,end=185)
  assert all(not x['long'] and x['action']=='hold' for x in flat)
print(json.dumps({'synthetic_fixture_checks':'PASS','predeclared_parameter_cells':9,'strict_prior_close_channel':True,'entry_and_either_exit':True,'current_future_close_unused':True,'not_performance_evidence':True}))
