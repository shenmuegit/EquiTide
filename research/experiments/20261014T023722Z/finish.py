#!/usr/bin/env python3
"""Finish only already-reserved, audited CMF configurations into a durable sidecar."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());canonical=ROOT/'research/automation/registry.jsonl'
events=[json.loads(x) for x in canonical.read_text().splitlines()];latest=registry.read_records(canonical);reserve=[]
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);rec=latest.get(fp)
 assert rec and rec['status']=='reserved' and rec['result_available'] is False,(row['name'],rec)
 matches=[x for x in events if x.get('fingerprint')==fp and x.get('status')=='reserved' and x.get('result_available') is False]
 assert matches;reserve.append(max(matches,key=lambda x:x['recorded_at_utc']))
side=R/'registry_records.jsonl';side.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in reserve))
log=[]
for row in batch:
 status=report['configs'][row['name']]['status'];assert status in ('passed','rejected')
 p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'--ledger',str(side),'finish',row['spec'],status,str((R/'report.json').relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True)
 item={'name':row['name'],'status':status,'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()};log.append(item);assert p.returncode==0,item
(R/'finish.log').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in log)+'\n')
final=registry.read_records(canonical)
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);status=report['configs'][row['name']]['status']
 assert final[fp]['status']==status and final[fp]['result_available'] is True
mfile=R/'data_manifest.json';m=json.loads(mfile.read_text());m['registry_fragment']={'path':str(side.relative_to(ROOT)),'sha256':hashlib.sha256(side.read_bytes()).hexdigest(),'events':len(side.read_text().splitlines())};m['finish_log_sha256']=hashlib.sha256((R/'finish.log').read_bytes()).hexdigest();mfile.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'finished':len(log),'passed':sum(x['status']=='passed' for x in log),'rejected':sum(x['status']=='rejected' for x in log),'sidecar_sha256':m['registry_fragment']['sha256']}))
