"""Only source integrity/availability and context coverage;no strategy PnL."""
import json
import polars as pl
from run import ROOT,R,sha,put
p=json.loads((ROOT/'research/experiments/20261029T192831Z/plan.json').read_text());out={}
for asset,files in p['data']['assets'].items():
 for x in files:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).stat().st_size==x['bytes']
 f=next(x for x in files if x['path'].endswith('/funding_settlement.parquet'));rows=pl.read_parquet(ROOT/f['path']).to_dicts();assert len(rows)==1212 and all(x['available_ts']>=x['settlement_ts'] for x in rows) and len({x['settlement_ts'] for x in rows})==len(rows)
 out[asset]={'funding_rows':len(rows),'availability_lag_ns':sorted({x['available_ts']-x['settlement_ts'] for x in rows}),'actual_interval_hours':sorted({str(x['actual_interval_hours']) for x in rows}),'min_settlement_ns':min(x['settlement_ts'] for x in rows),'max_settlement_ns':max(x['settlement_ts'] for x in rows),'input_sha256':f['sha256']}
put(R/'data_preflight.json',{'passed':True,'financial_evaluations':0,'assets':out,'policy':'Real funding timestamps/availability preserved for ex-post cash accounting only, no funding signal.33day context supports source N30 excluding tested close.'});print('PASS funding data hashes/availability',json.dumps(out))
