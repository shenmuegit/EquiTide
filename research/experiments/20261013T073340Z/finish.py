#!/usr/bin/env python3
"""Finish every actual candle-turn and comparator configuration."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;report=R/'report.json';done=[]
for row in json.loads((R/'batch.json').read_text()):
 status='rejected'
 p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'finish',str(ROOT/row['spec']),status,str(report)],cwd=ROOT,capture_output=True,text=True)
 item={'name':row['name'],'fingerprint':row['fingerprint'],'status':status,'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()};done.append(item)
 if p.returncode:
  (R/'finish_partial.json').write_text(json.dumps(done,indent=2,ensure_ascii=False)+'\n')
  raise SystemExit(f"finish failed {row['name']}: {p.stdout} {p.stderr}")
(R/'finish.json').write_text(json.dumps(done,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'finished':len(done),'rejected':sum(x['status']=='rejected' for x in done),'report_sha256':__import__('hashlib').sha256(report.read_bytes()).hexdigest()},ensure_ascii=False))
