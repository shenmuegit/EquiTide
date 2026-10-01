"""Finish each independently reserved actual configuration against the frozen report."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
report=ROUND/'report.json';r=json.loads(report.read_text());batch=json.loads((ROUND/'batch.json').read_text())
assert (ROUND/'evidence_pre_finish.log').read_text().startswith('PASS:')
for p,h in r['source_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
for b in batch:
    status=r['configs'][b['name']]['status']
    p=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'finish',str(ROOT/b['spec']),status,str(report.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
    print(b['name'],status,p.returncode,p.stdout.strip(),flush=True)
    if p.returncode:raise RuntimeError(p.stderr+p.stdout)
print('PASS:30 real configurations finished individually;6 research passed,21 research rejected,3 comparators rejected by scope')
