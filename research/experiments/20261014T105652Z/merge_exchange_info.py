#!/usr/bin/env python3
"""Rebuild the canonical two-symbol exchangeInfo snapshot from the two captured public GET bodies."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
b=json.loads((R/'exchange_info_BTCUSDT_response.json').read_text())
e=json.loads((R/'exchange_info_ETHUSDT_response.json').read_text())
assert len(b['symbols'])==len(e['symbols'])==1
assert b['symbols'][0]['symbol']=='BTCUSDT' and e['symbols'][0]['symbol']=='ETHUSDT'
b['symbols']+=e['symbols'];b['serverTime']=max(b.get('serverTime',0),e.get('serverTime',0))
(R/'exchange_info_raw.json').write_text(json.dumps(b,separators=(',',':'))+'\n')
print('merged captured public GET responses into canonical snapshot')
