#!/usr/bin/env python3
"""Finish this completed, already-reserved batch into an experiment registry fragment."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());canonical=ROOT/'research/automation/registry.jsonl'
events=[json.loads(x) for x in canonical.read_text().splitlines()];latest=registry.read_records(canonical);reservation=[]
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);rec=latest.get(fp)
 assert rec and rec['status']=='reserved' and rec['result_available'] is False,(row['name'],rec)
 matches=[e for e in events if e.get('fingerprint')==fp and e.get('status')=='reserved' and e.get('result_available') is False]
 assert matches
 reservation.append(max(matches,key=lambda x:x['recorded_at_utc']))
side=R/'registry_records.jsonl';side.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in reservation))
log=[]
for row in batch:
 status='rejected' if row['role']=='comparator' else report['configs'][row['name']]['status']
 p=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'--ledger',str(side),'finish',row['spec'],status,str((R/'report.json').relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True)
 rec={'name':row['name'],'role':row['role'],'status':status,'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()};log.append(rec);assert p.returncode==0,rec
(R/'finish.log').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in log)+'\n')
final=registry.read_records(canonical)
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);expected='rejected' if row['role']=='comparator' else report['configs'][row['name']]['status']
 assert final[fp]['status']==expected and final[fp]['result_available'] is True
manifest_path=R/'data_manifest.json';m=json.loads(manifest_path.read_text());m['registry_fragment']={'path':str(side.relative_to(ROOT)),'sha256':hashlib.sha256(side.read_bytes()).hexdigest(),'records':len(log)};m['finish_log_sha256']=hashlib.sha256((R/'finish.log').read_bytes()).hexdigest();manifest_path.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'finished':len(log),'candidates_passed':sum(x['status']=='passed' for x in log if x['role']=='candidate'),'candidates_rejected':sum(x['status']=='rejected' for x in log if x['role']=='candidate'),'comparator_rejected':sum(x['role']=='comparator' and x['status']=='rejected' for x in log),'registry_fragment_sha256':m['registry_fragment']['sha256']}))
