"""Check actual saved trial evidence, report hashes, reserve order and recovered queue."""
import hashlib
import json
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
s=spec_from_file_location('registry_evidence',ROOT/'research/automation/registry.py')
m=module_from_spec(s)
s.loader.exec_module(m)
ledger=ROOT/'research/automation/registry.jsonl'
rows=[json.loads(x) for x in ledger.read_text().splitlines()]
records=m.read_records(ledger)
report_path=ROUND/'report.json'
report=json.loads(report_path.read_text())
sha=hashlib.sha256(report_path.read_bytes()).hexdigest()
batch=json.loads((ROUND/'batch.json').read_text())
comparators=json.loads((ROUND/'benchmark_batch.json').read_text())
assert len(batch)==42 and len(comparators)==2 and len(report['configs'])==42
assert len(report['folds'])==6
for item in batch+comparators:
 spec=json.loads((ROOT/item['spec']).read_text())
 assert m.fingerprint(spec)==item['fingerprint']
 row=records[item['fingerprint']]
 assert row['status'] in ('passed','rejected') and row['result_available'] is True
 assert row['report_sha256']==sha
 events=[r for r in rows if r['fingerprint']==item['fingerprint']]
 assert events[-1]['status']!='reserved'
 assert any(r.get('status')=='reserved' and r['recorded_at_utc']<events[-1]['recorded_at_utc'] for r in events)
for name,row in report['configs'].items():
 for k,r in row['cost_scenarios'].items():
  assert len(r['folds'])==6 and len(r['equity_usdt'])==182
  value=1
  for f in r['folds']:
   value*=1+f['net_return_pct']/100
  assert abs(value-(1+r['net_return_pct']/100))<1e-12,(name,k)
 assert row['status']=='rejected' and any(not x for x in row['criteria'].values())
assert not any(x['status']=='reserved' for x in records.values())
initial=rows[:16]
assert sum(records[x['fingerprint']]['result_available'] for x in initial)==11
assert len({m.fingerprint(x['spec']) for x in records.values()})==54
manifest=json.loads((ROUND/'data_manifest.json').read_text())
assert len(manifest['archives'])==54 and not manifest['errors']
for archive in manifest['archives']:
 assert hashlib.sha256((ROOT/archive['path']).read_bytes()).hexdigest()==archive['sha256']==archive['published_sha256']
for asset,row in manifest['normalized'].items():
 assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
print('PASS: 44 completed configs, report SHA256, append-only reserve/finish events, 126 continuous curves, 11/16 original results, 54 true definitions, 54 official archive hashes')
