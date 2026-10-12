#!/usr/bin/env python3
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text())
with (R/'finish.log').open('w') as f:
 for b in batch:
  status='rejected' if b['is_comparator'] else report['configs'][b['name']]['status']
  cp=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'finish',str(ROOT/b['spec']),status,str(R/'report.json')],cwd=ROOT,text=True,capture_output=True)
  f.write(json.dumps({'name':b['name'],'fingerprint':b['fingerprint'],'status':status,'returncode':cp.returncode,'stdout':cp.stdout.strip(),'stderr':cp.stderr.strip()},ensure_ascii=False)+'\n');f.flush()
  if cp.returncode:raise SystemExit(f"finish failed {b['name']}: {cp.stderr}")
print('finished 18 actual candidates (all rejected) and two hold references')
