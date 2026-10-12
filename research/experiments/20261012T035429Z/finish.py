"""Finish the 28 historical configs only after bound independent audits."""
from pathlib import Path
import hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;ROOT=T.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((T/'audit.log').read_text());assert a['passed'] and a['report_sha256']==sha(T/'report.json')
report=json.loads((T/'report.json').read_text());batch=json.loads((T/'batch.json').read_text())
assert len(batch)==68 and set(report['summary']['passed'])|set(report['summary']['rejected'])=={b['name'] for b in batch}
for b in batch:
 status=report['configs'][b['name']]['status'];assert status in ('passed','rejected')
 p=subprocess.run([sys.executable,'research/automation/registry.py','finish',b['spec'],status,str((T/'report.json').relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 print(b['name'],status,p.returncode,p.stdout.strip(),flush=True)
 if p.returncode:raise RuntimeError(p.stdout+p.stderr)
