"""Reserve at most eight fresh configurations; no curve,signal,metric or market evaluation."""
import json
from run import ROOT,R,reg,sha,put,rel,now,call
assert not(R/'report.json').exists();batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[]
for row in batch:
 rec=records.get(row['fingerprint'])
 if rec is None or rec['result_available'] is False and rec['status'] in ['blocked','abandoned']:pending.append(row)
 else:assert rec['status']=='reserved' and rec['spec']==json.loads((ROOT/row['spec']).read_text())
folder=R/'reserve_batches';folder.mkdir(exist_ok=True);path=folder/f'batch_{len(list(folder.glob("batch_*.json"))):03d}.json';done=[]
for row in pending[:8]:
 start=now();item=call('reserve',row);item.update(started_utc=start,finished_utc=now());done.append(item);put(path,{'actual_command_receipts':done,'reported_after_utc':now()})
records=reg.read_records(ROOT/'research/automation/registry.jsonl');remaining=sum(x['fingerprint'] not in records or records[x['fingerprint']]['status']!='reserved' for x in batch);print(json.dumps({'batch_receipt':rel(path) if done else None,'actual_reserve_calls':len(done),'remaining_financial_IDs':remaining,'financial_evaluations':0}),flush=True)
