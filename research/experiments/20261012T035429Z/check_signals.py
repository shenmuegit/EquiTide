"""Synthetic signal and Decimal allocation fixtures only;no performance evidence."""
from pathlib import Path
from decimal import Decimal as D
import json,sys
T=Path(__file__).resolve().parent;ROOT=T.parents[2]
sys.path.insert(0,str(T));from signals import asymmetric_filtered_channel
from design import definitions,BTC_WEIGHTS,ETH_ENTRIES,allocations,eth_weight
sys.path.insert(0,str(ROOT/'research/automation'));import registry
# EMA34 entry-band fixture around the 15-day prior-close channel breakout.
fixtures=[(.0075,'101.1',True),(.01,'101.1',True),(.0125,'101.37',True),(.015,'101.61',True),(.0175,'101.61',False)]
for band,close,want in fixtures:
 values=['100']*185;values[182]=close
 result=asymmetric_filtered_channel(values,15,30,34,band,.005,start=183,end=184)[0]
 assert result['channel_entry'] and result['long']==want,(band,result)
 modified=values.copy();modified[-1]='999999'
 assert result==asymmetric_filtered_channel(modified,15,30,34,band,.005,start=183,end=184)[0]
# Symmetric .5% exit band remains fixed; exercise equality and an EMA-only exit absent a channel break.
values=['100']*185;values[160]='80';values[181]='101';values[182]='99.0'
z=asymmetric_filtered_channel(values,15,30,34,.0125,.005,start=183,end=184)[0]
assert z['EMA_exit'] and not z['channel_exit'] and not z['long']
values=['100']*185;values[181]='110';values[182]='105';values[183]='104'
z=asymmetric_filtered_channel(values,15,30,34,.0175,.005,start=183,end=185)
assert all(not x['channel_entry'] and not x['long'] for x in z)
items=definitions(registry.fingerprint);assert len(items)==110 and len({registry.fingerprint(sp)for sp,_ in items})==110
profile=[([w,eth_weight(w)],allocations(w))for w in BTC_WEIGHTS]
assert profile==[([.45,.55],[900,1100]),([.50,.50],[1000,1000]),([.55,.45],[1100,900]),([.60,.40],[1200,800]),([.65,.35],[1300,700])]
assert all(sum(D(str(x))for x in weights)==D(1)and sum(cash)==2000 for weights,cash in profile)
print(json.dumps({'synthetic_fixtures':'PASS','fixed_ETH_EMA_span_days':34,'entry_bands':ETH_ENTRIES,'fixed_exit_band':.005,'prior_close_channel_exclusion':True,'no_delayed_arming':True,'future_tail_invariance':True,'profiles':profile,'full_grid_definitions':len(items),'performance_evidence':False}))
