"""Finish actual configurations only after independent audits bind their exact reports."""
from pathlib import Path
import hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for log,report in [('audit.log','report.json'),('audit_forward.log','forward_report.json')]:
 a=json.loads((T/log).read_text());assert a['passed'] and a['report_sha256']==sha(T/report)
for bf,rf in [('batch.json','report.json'),('forward_batch.json','forward_report.json')]:
 report=json.loads((T/rf).read_text())
 for b in json.loads((T/bf).read_text()):
  status=report['configs'][b['name']]['status'];assert status in ('passed','rejected');p=subprocess.run([sys.executable,'research/automation/registry.py','finish',b['spec'],status,str((T/rf).relative_to(R))],cwd=R,capture_output=True,text=True);print(b['name'],status,p.returncode,p.stdout.strip(),flush=True)
  if p.returncode:raise RuntimeError(p.stdout+p.stderr)
