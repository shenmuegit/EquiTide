"""Finish <=8 invalid intended-rule attempts as blocked;full invalid curves retained."""
import json
from run import ROOT,R,reg,put,call,rel,now
rows=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[]
for row in rows:
 x=records[row['fingerprint']]
 if x['status']=='reserved':pending.append(row)
 else:assert x['status']=='blocked' and x['result_available'] is False
folder=R/'invalid_finish_batches';folder.mkdir(exist_ok=True);p=folder/f'batch_{len(list(folder.glob("batch_*.json"))):03d}.json';done=[]
for row in pending[:8]:done.append({**call('finish',row,'blocked',rel(R/'invalid_attempt/invalid_spec_report.json')),'finished_utc':now()});put(p,{'actual_command_receipts':done})
print('INVALID_BLOCKED_THIS_BATCH',len(done),'remaining',len(pending)-len(done))
