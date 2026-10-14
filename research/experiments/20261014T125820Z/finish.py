#!/usr/bin/env python3
"""Audit, finish all 18 completed runs, and persist compact reserve/finish records."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;REG=ROOT/'research/automation/registry.jsonl'
def main():
 batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text())
 assert len(batch)==18 and report['summary']['rejected']==18 and report['summary']['passed']==0
 p=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True)
 (R/'audit.log').write_text(p.stdout+p.stderr)
 if p.returncode:raise SystemExit('independent audit failed; no finishes written')
 events=[]
 for row in batch:
  status=report['configs'][row['name']]['status'];assert status in ('passed','rejected')
  q=subprocess.run([sys.executable,'research/automation/registry.py','finish',row['spec'],status,'research/experiments/'+R.name+'/report.json'],cwd=ROOT,text=True,capture_output=True)
  events.append({'spec':row['spec'],'fingerprint':row['fingerprint'],'status':status,'exit_code':q.returncode,'stdout':q.stdout.strip(),'stderr':q.stderr.strip()})
  print(q.returncode,row['name'],status,q.stdout.strip(),q.stderr.strip())
  if q.returncode:break
 (R/'finish.json').write_text(json.dumps(events,indent=2,ensure_ascii=False)+'\n')
 if len(events)!=len(batch) or any(x['exit_code'] for x in events):raise SystemExit('not all finish calls succeeded')
 fps={x['fingerprint'] for x in batch};ledger=[json.loads(x) for x in REG.read_text().splitlines() if x.strip()];records=[x for x in ledger if x.get('fingerprint') in fps]
 assert len(records)==36 and all(sum(x.get('fingerprint')==fp for x in records)==2 for fp in fps)
 frag=R/'registry_records.jsonl';frag.write_text(''.join(json.dumps(x,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n' for x in records))
 print('finished 18 variants; sidecar events=36; sha256='+hashlib.sha256(frag.read_bytes()).hexdigest())
if __name__=='__main__':main()
