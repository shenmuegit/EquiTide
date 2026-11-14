"""Reserve each blocked exact spec again only after the recovered source binding and synthetic test pass."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
assert json.loads((R/'review/native_test_tail_stats_green.py_receipt.json').read_text())['exit_code']==0;batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');binding=json.loads((R/'code_binding_before_evaluation.json').read_text());assert all(records[x['fingerprint']]['status']=='blocked' and not records[x['fingerprint']]['result_available'] for x in batch)
for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256']}.items():assert sha(ROOT/path)==h
rows=[]
for row in batch:
 a=now();z=call('reserve',row);z.update(started_utc=a,finished_utc=now());rows.append(z);put(R/'recovery_reserve_receipts.json',rows)
print('PASS11exact noresult configs successfully re-reserved after repaired source bind')
