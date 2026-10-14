#!/usr/bin/env python3
"""Require full replay audit, finish every completed candidate, and save a ledger sidecar."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;REG=ROOT/'research/automation/registry.jsonl'
def main():
 batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());assert len(batch)==54 and report['summary']['rejected']+report['summary']['passed']==54
 p=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True);(R/'audit.log').write_text(p.stdout+p.stderr)
 if p.returncode:raise SystemExit('audit failed; no finish event appended')
 done=[]
 for row in batch:
  status=report['configs'][row['name']]['status'];q=subprocess.run([sys.executable,'research/automation/registry.py','finish',row['spec'],status,'research/experiments/'+R.name+'/report.json'],cwd=ROOT,text=True,capture_output=True)
  done.append({'spec':row['spec'],'fingerprint':row['fingerprint'],'status':status,'exit_code':q.returncode,'stdout':q.stdout.strip(),'stderr':q.stderr.strip()});print(q.returncode,row['name'],status,q.stdout.strip())
  if q.returncode:break
 (R/'finish.json').write_text(json.dumps(done,indent=2,ensure_ascii=False)+'\n')
 if len(done)!=len(batch) or any(x['exit_code'] for x in done):raise SystemExit('finish incomplete')
 fps={x['fingerprint'] for x in batch};rows=[json.loads(x) for x in REG.read_text().splitlines() if x.strip()];events=[x for x in rows if x.get('fingerprint') in fps]
 assert len(events)==108 and all(sum(x['fingerprint']==fp for x in events)==2 for fp in fps)
 frag=R/'registry_records.jsonl';frag.write_text(''.join(json.dumps(x,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n' for x in events))
 print('54 candidates finished; 108 reserve/finish events, sidecar sha256='+hashlib.sha256(frag.read_bytes()).hexdigest())
if __name__=='__main__':main()
