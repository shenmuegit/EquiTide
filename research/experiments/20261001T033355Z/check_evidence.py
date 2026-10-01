"""Validate saved outputs, event order, source hashes, fold reconciliation and registry."""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('registry_check',ROOT/'research/automation/registry.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ledger=ROOT/'research/automation/registry.jsonl'
records=m.read_records(ledger)
events=[json.loads(x) for x in ledger.read_text().splitlines()]
report_path=ROUND/'report.json';report=json.loads(report_path.read_text())
digest=hashlib.sha256(report_path.read_bytes()).hexdigest()
batch=json.loads((ROUND/'batch.json').read_text())
assert len(batch)==20 and len(report['configs'])==20
assert len(report['summary']['rejected'])==20 and not report['summary']['passed'] and not report['summary']['blocked']
for item in batch:
 spec=json.loads((ROOT/item['spec']).read_text());fp=m.fingerprint(spec)
 assert fp==item['fingerprint']
 row=records[fp]
 assert row['status']=='rejected' and row['result_available'] is True
 assert row['report_sha256']==digest
 e=[x for x in events if x['fingerprint']==fp]
 assert any(x.get('status')=='reserved' and x['recorded_at_utc']<e[-1]['recorded_at_utc'] for x in e)
 for k,out in report['configs'][item['name']]['cost_scenarios'].items():
  assert len(out['folds'])==6
  product=math.prod(1+x['net_return_pct']/100 for x in out['folds'])
  assert abs(product-(1+out['net_return_pct']/100))<1e-11
  assert abs((out['equity_usdt'][-1]/out['equity_usdt'][0]-1)*100-out['net_return_pct'])<1e-10
  if item['role']=='candidate':assert not out['margin_violations']
assert sum(records[x['fingerprint']]['result_available'] for x in events[:16])==13
assert len({m.fingerprint(x['spec']) for x in records.values()})==72
assert not any(x['status']=='reserved' for x in records.values())
manifest=json.loads((ROUND/'binance_data_manifest.json').read_text())
assert len(manifest['archives'])==108 and not manifest['errors']
for x in manifest['archives']:
 assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']==x['published_sha256']
for asset in ('BTC','ETH'):
 for x in manifest['normalized'][asset].values():
  assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']
  for repair in x['official_rest_repairs']:
   assert repair['actual_restored_rows']==24
   assert hashlib.sha256((ROOT/repair['path']).read_bytes()).hexdigest()==repair['sha256']
 x=manifest['funding'][asset];assert x['normalized']['rows']==1095
 for p in x['sources']+[x['normalized'],manifest['metadata'][asset]]:
  assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256']
x=report['data']['cross']
assert hashlib.sha256((ROOT/x['okx_actual_volume_path']).read_bytes()).hexdigest()==x['okx_actual_volume_sha256']
base=ROOT/'data/normalized/okx/BTC/cross_exchange_carry_20260930'
okx=json.loads((ROUND/'okx_data_manifest.json').read_text())
for path,sha in [('perp_bars.parquet','bars_sha256'),('funding_settlement.parquet','funding_sha256')]:
 assert hashlib.sha256((base/path).read_bytes()).hexdigest()==okx[sha]
for sources in okx['sources'].values():
 for p in sources:assert hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()==p['sha256']
# Current/future observation must not alter estimates trained on the previous window.
s=importlib.util.spec_from_file_location('legacy_signal_check',ROOT/'checks/perp_pairs_oos.py')
old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
x=np.linspace(3,4,720)+.03*np.sin(np.arange(720)/7)
y=12*x**.6*np.exp(.002*np.cos(np.arange(720)/12))
b1,z1,r1=old.signal(y,x,float(y[-1]),float(x[-1]))
b2,z2,r2=old.signal(y,x,float(y[-1])*1.1,float(x[-1]))
assert b1==b2 and np.array_equal(r1,r2) and z1!=z2
print('PASS: 20 finished trials, report hashes, all six-fold products, 13/16 initial results, 72 canonical configs, 108 archive hashes and real mark repairs, exact funding data, prior-only OLS fit')
