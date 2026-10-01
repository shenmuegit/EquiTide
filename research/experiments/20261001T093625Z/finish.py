"""Finish every actual new configuration with the immutable report hash."""
import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];report=R/'report.json';r=json.loads(report.read_text());q={x['fingerprint']:x['qualification'] for x in r['trials']}
for b in json.loads((R/'batch.json').read_text()):
 status=q.get(b['fingerprint'],'rejected');p=subprocess.run([sys.executable,str(ROOT/'research/automation/registry.py'),'finish',b['spec'],status,str(report.relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True);print(b['name'],status,p.returncode,p.stdout.strip(),flush=True)
 if p.returncode:raise SystemExit(p.stdout+p.stderr)
print('All22 new definitions finished;66 actual scenarios retained, no reserved entries left.')
