"""Finish only complete actual results after all three independent audits pass."""
from pathlib import Path
import hashlib,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2]
for log,report in [('audit_components.log','components_report.json'),('audit.log','report.json'),('audit_forward.log','forward_report.json')]:
 a=json.loads((T/log).read_text());assert a['passed'] and a['report_sha256']==hashlib.sha256((T/report).read_bytes()).hexdigest()
for batch,report in [('component_batch.json','components_report.json'),('batch.json','report.json'),('forward_batch.json','forward_report.json')]:
 r=json.loads((T/report).read_text())
 for b in json.loads((T/batch).read_text()):
  status=r['configs'][b['name']]['status'];assert status in ('passed','rejected')
  p=subprocess.run([sys.executable,'research/automation/registry.py','finish',b['spec'],status,str((T/report).relative_to(R))],cwd=R,capture_output=True,text=True)
  print(b['name'],status,p.returncode,p.stdout.strip(),flush=True)
  if p.returncode:raise RuntimeError(p.stdout+p.stderr)
