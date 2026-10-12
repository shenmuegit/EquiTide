#!/usr/bin/env python3
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; R=Path(__file__).resolve().parent
report=json.loads((R/'report.json').read_text()); batch=json.loads((R/'batch.json').read_text())
with (R/'finish.log').open('w') as log:
 for row in batch:
  status='rejected' if row['is_comparator'] else report['configs'][row['name']]['cost_scenarios']['status']
  assert status in ('passed','rejected')
  args=[sys.executable,str(ROOT/'research/automation/registry.py'),'finish',str(ROOT/row['spec']),status,str(R/'report.json')]
  cp=subprocess.run(args,cwd=ROOT,text=True,capture_output=True)
  log.write(json.dumps({'name':row['name'],'fingerprint':row['fingerprint'],'status':status,'returncode':cp.returncode,'stdout':cp.stdout.strip(),'stderr':cp.stderr.strip()},ensure_ascii=False)+'\n');log.flush()
  if cp.returncode:raise SystemExit(f"finish failed: {row['name']} {cp.stderr}")
print(f'finished {len(batch)} configurations: 18 actual strategy trials rejected, 2 hold references rejected as historical comparators')
