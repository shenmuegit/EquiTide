"""Finish each actual configuration against the already frozen common report."""
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
report=ROUND/'report.json';r=json.loads(report.read_text());batch=json.loads((ROUND/'batch.json').read_text())+json.loads((ROUND/'comparator_batch.json').read_text())
for item in batch:
    status=(r['configs'] if item['role']!='comparator' else r['comparator_configs'])[item['name']]['status']
    result=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'finish',item['spec'],status,str(report.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
    print(item['name'],status,result.returncode,result.stdout.strip(),result.stderr.strip(),flush=True)
    if result.returncode:raise RuntimeError('Finish failed '+item['name'])
print('FINISHED:39 research +1 comparison configurations; all outcomes and disclosed comparator preregistration deviation retained')
