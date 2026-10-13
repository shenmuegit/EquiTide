#!/usr/bin/env python3
"""Finish the already-reserved batch using a compact registry fragment."""
import hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation')); import registry
batch=json.loads((R/'batch.json').read_text()); report=json.loads((R/'report.json').read_text())
canonical=ROOT/'research/automation/registry.jsonl'; events=[json.loads(x) for x in canonical.read_text().splitlines()]
records=registry.read_records(canonical)
reservations=[]
for row in batch:
    spec=json.loads((ROOT/row['spec']).read_text()); fp=registry.fingerprint(spec); rec=records.get(fp)
    assert rec and rec['status']=='reserved' and rec['result_available'] is False, (row['name'],rec)
    matches=[e for e in events if e.get('fingerprint')==fp and e.get('status')=='reserved' and e.get('result_available') is False]
    assert matches
    reservations.append(max(matches,key=lambda e:e['recorded_at_utc']))
sidecar=R/'registry_records.jsonl'
sidecar.write_text(''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in reservations))
finish_log=[]
for row in batch:
    spec_path=ROOT/row['spec']; status='rejected' if row['is_comparator'] else report['configs'][row['name']]['status']
    p=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'--ledger',str(sidecar),'finish',str(spec_path),status,str(R/'report.json')],cwd=ROOT,text=True,capture_output=True)
    rec={'name':row['name'],'status':status,'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
    finish_log.append(rec)
    assert p.returncode==0, rec
(R/'finish.log').write_text('\n'.join(json.dumps(x,ensure_ascii=False) for x in finish_log)+'\n')
merged=registry.read_records(canonical)
for row in batch:
    spec=json.loads((ROOT/row['spec']).read_text()); fp=registry.fingerprint(spec)
    assert merged[fp]['status']==('rejected' if row['is_comparator'] else report['configs'][row['name']]['status'])
    assert merged[fp]['result_available'] is True
manifest_path=R/'data_manifest.json'; manifest=json.loads(manifest_path.read_text())
manifest['registry_fragment']={'path':str(sidecar.relative_to(ROOT)),'sha256':hashlib.sha256(sidecar.read_bytes()).hexdigest(),'records':len(finish_log),'finished_at_utc':finish_log[-1]['stdout'] if finish_log else None}
manifest['finish_log_sha256']=hashlib.sha256((R/'finish.log').read_bytes()).hexdigest()
manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'finished':len(finish_log),'passed_candidates':sum(x['status']=='passed' for x in finish_log),'rejected_candidates':sum(x['status']=='rejected' and x['name']!='hold_360d_4h_BTC_ETH_50_50' for x in finish_log),'comparator_status':'rejected/comparator-only','registry_fragment_sha256':manifest['registry_fragment']['sha256']},ensure_ascii=False))
