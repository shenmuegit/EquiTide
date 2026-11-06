"""Finish at most eight reserved IDs; preserve actual receipts and reconcile prior completion."""
import json,sys
from run import ROOT,R,reg,sha,put,rel,now,call
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');pending=[]
for row in batch:
 rec=records[row['fingerprint']];c=report['configs'][row['name']]
 if rec['status']=='reserved':pending.append(row)
 else:assert rec['status']==c['status'] and rec['result_available'] is True and rec['report_sha256']==sha(R/'report.json')
folder=R/'finish_batches';folder.mkdir(exist_ok=True);path=folder/f'batch_{len(list(folder.glob("batch_*.json"))):03d}.json';done=[]
for row in pending[:8]:
 start=now();item=call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json'));item.update(started_utc=start,finished_utc=now());done.append(item);put(path,{'started_utc':done[0].get('started_utc'),'actual_command_receipts':done,'reported_after_utc':now()})
records=reg.read_records(ROOT/'research/automation/registry.jsonl');remaining=sum(records[x['fingerprint']]['status']=='reserved' for x in batch);print(json.dumps({'batch_receipt':rel(path) if done else None,'actual_finish_calls':len(done),'remaining_financial_IDs':remaining,'no_financial_recalculation':True}),flush=True)
