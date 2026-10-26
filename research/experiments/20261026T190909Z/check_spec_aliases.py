"""Precalculation consistency, including duplicate parameter aliases; no model execution."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
rows=json.loads((R/'batch.json').read_text());assert len(rows)==108
for row in rows:
 p=json.loads((ROOT/row['spec']).read_text())['parameters']
 if row['scope']=='native':assert p['trend_lookback_days']==row['trend_lookback_days'] in [21,31] and p['fixed_entry_notional_usdt']==row['fixed_entry_notional_usdt'] and p['raw_entry_notional_fraction_of_initial_capital']==p['fixed_entry_notional_usdt']/10000
 else:assert p['trend_filter_lookback_days']==p['ETH_trend_lookback_days']==row['trend_filter_lookback_days'] in [21,31],(row['name'],p['trend_filter_lookback_days'],p['ETH_trend_lookback_days'])
print('PASS:all108 concrete native/parent definitions and slow aliases agree before calculation')
