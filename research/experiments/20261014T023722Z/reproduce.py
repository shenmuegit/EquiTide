#!/usr/bin/env python3
"""Rerun the frozen research grid with a temporary registry and restore published outputs."""
import hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
outputs=['report.json','trades.csv.gz','decisions.csv.gz','daily_equity.csv.gz','sensitivity.csv','sensitivity_surface.svg','data_manifest.json','result.md']
def stable(p):
 x=json.loads(Path(p).read_text());x.pop('evaluation_started_utc',None);return x
with tempfile.TemporaryDirectory(prefix='equitide-cmf-repro-') as td:
 t=Path(td);backup=t/'original';backup.mkdir()
 for name in outputs:shutil.copy2(R/name,backup/name)
 try:
  for row in json.loads((R/'batch.json').read_text()):
   p=subprocess.run([str(ROOT/'.venv/bin/python'),str(ROOT/'research/automation/registry.py'),'--ledger',str(t/'registry.jsonl'),'reserve',row['spec']],cwd=ROOT,text=True,capture_output=True)
   if p.returncode:raise RuntimeError(p.stdout+p.stderr)
  env=os.environ.copy();env['CMF_REGISTRY_LEDGER']=str(t/'registry.jsonl')
  ev=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'evaluate.py')],cwd=ROOT,text=True,capture_output=True,env=env)
  if ev.returncode:raise RuntimeError('evaluate.py failed\n'+ev.stdout+'\n'+ev.stderr)
  au=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True,env=env)
  if au.returncode:raise RuntimeError('audit.py failed\n'+au.stdout+'\n'+au.stderr)
  assert stable(backup/'report.json')==stable(R/'report.json'),'reproduced economic report differs from saved report'
  print('reproduction passed: report economics, 12 folds, cost scenes and NAV hashes matched')
  print(ev.stdout.splitlines()[-1])
 finally:
  for name in outputs:shutil.copy2(backup/name,R/name)
