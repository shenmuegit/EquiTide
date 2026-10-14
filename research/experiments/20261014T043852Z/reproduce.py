#!/usr/bin/env python3
"""Re-run the frozen grid on a temporary registry and restore published evidence."""
import json,os,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
outputs=['report.json','trades.csv.gz','decisions.csv.gz','daily_equity.csv.gz','sensitivity.csv','sensitivity_surface.svg','data_manifest.json','result.md']
def stable(p):
 x=json.loads(Path(p).read_text());x.pop('evaluation_started_utc',None);return x
with tempfile.TemporaryDirectory(prefix='equitide-reclaim-repro-') as td:
 tmp=Path(td);backup=tmp/'original';backup.mkdir()
 for name in outputs:shutil.copy2(R/name,backup/name)
 try:
  for item in json.loads((R/'batch.json').read_text()):
   p=subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'research/automation/registry.py'),'--ledger',str(tmp/'registry.jsonl'),'reserve',item['spec']],cwd=ROOT,text=True,capture_output=True)
   if p.returncode:raise RuntimeError(p.stdout+p.stderr)
  env=os.environ.copy();env['RECLAIM_REGISTRY_LEDGER']=str(tmp/'registry.jsonl')
  for program in ('evaluate.py','audit.py'):
   p=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/program)],cwd=ROOT,text=True,capture_output=True,env=env)
   if p.returncode:raise RuntimeError(f'{program} failed\n{p.stdout}\n{p.stderr}')
  assert stable(backup/'report.json')==stable(R/'report.json'),'reproduced report differs'
  print('reproduction passed: all nine configs, source hashes, causal state replay, ledger balances, 27 cost scenes and 12 folds')
 finally:
  for name in outputs:shutil.copy2(backup/name,R/name)
