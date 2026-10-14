#!/usr/bin/env python3
"""Finish the nine audited, pre-reserved configurations in a durable sidecar."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());canonical=ROOT/'research/automation/registry.jsonl'
events=[json.loads(x) for x in canonical.read_text().splitlines()];latest=registry.read_records(canonical);reserves=[]
for item in batch:
 spec=json.loads((ROOT/item['spec']).read_text());fp=registry.fingerprint(spec);rec=latest.get(fp)
 assert report['configs'][item['name']]['fingerprint']==fp and report['configs'][item['name']]['status']=='rejected'
 assert rec and rec['status']=='reserved' and rec['result_available'] is False,(item['name'],rec)
 matches=[x for x in events if x.get('fingerprint')==fp and x.get('status')=='reserved' and x.get('result_available') is False]
 assert matches;reserves.append(max(matches,key=lambda x:x['recorded_at_utc']))
side=R/'registry_records.jsonl';side.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in reserves))
logs=[]
for item in batch:
 p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'--ledger',str(side),'finish',item['spec'],'rejected',str((R/'report.json').relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True)
 logs.append({'name':item['name'],'status':'rejected','returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()})
 assert p.returncode==0,logs[-1]
(R/'finish.log').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in logs))
final=registry.read_records(canonical)
for item in batch:
 fp=registry.fingerprint(json.loads((ROOT/item['spec']).read_text()));assert final[fp]['status']=='rejected' and final[fp]['result_available'] is True
mfile=R/'data_manifest.json';m=json.loads(mfile.read_text());m['registry_fragment']={'path':str(side.relative_to(ROOT)),'sha256':hashlib.sha256(side.read_bytes()).hexdigest(),'events':len(reserves)};m['finish_log_sha256']=hashlib.sha256((R/'finish.log').read_bytes()).hexdigest();mfile.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'finished':len(logs),'rejected':len(logs),'sidecar_sha256':m['registry_fragment']['sha256']}))
