#!/usr/bin/env python3
"""Finish all pre-reserved real-result configurations without rewriting the ledger."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
batch=json.loads((R/'batch.json').read_text());report=R/'report.json';done=[]
for row in batch:
 status='rejected'
 p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'finish',str(ROOT/row['spec']),status,str(report)],cwd=ROOT,capture_output=True,text=True)
 item={'name':row['name'],'fingerprint':row['fingerprint'],'status':status,'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()};done.append(item)
 if p.returncode:
  (R/'finish_partial.json').write_text(json.dumps(done,indent=2,ensure_ascii=False)+'\n')
  raise SystemExit(f"finish failed for {row['name']}: {p.stdout} {p.stderr}")
(R/'finish.json').write_text(json.dumps(done,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'finished':len(done),'status_counts':{'rejected':sum(x['status']=='rejected' for x in done)}},ensure_ascii=False))
