"""Append each evaluated definition to the immutable registry."""
import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];report=R/'report.json';r=json.loads(report.read_text());qualifications={x['fingerprint']:x['qualification'] for x in r['trials']}
for x in json.loads((R/'batch.json').read_text()):
 status=qualifications.get(x['fingerprint'],'rejected');p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'finish',x['spec'],status,str(report.relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True);print(x['name'],status,p.returncode,p.stdout.strip(),flush=True)
 if p.returncode:raise SystemExit(p.stdout+p.stderr)
print('All21 definitions finished; all20 concrete backtests and initial scope evidence retained.')
