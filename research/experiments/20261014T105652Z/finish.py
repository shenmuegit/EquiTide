#!/usr/bin/env python3
"""Finish every pre-reserved variant, then persist its compact append-only ledger fragment."""
import hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;REG=ROOT/'research/automation/registry.jsonl'
def main():
 batch=json.loads((R/'batch.json').read_text());report=json.loads((R/'report.json').read_text());
 assert report['summary']['candidate_configurations']==28 and all(x['status'] in ('passed','rejected') for x in report['configs'].values())
 # Pre-finish independent replay is a mandatory gate.
 a=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True)
 (R/'audit.log').write_text(a.stdout+a.stderr)
 if a.returncode:raise SystemExit('audit failed; no registry finishes written')
 finishes=[]
 for row in batch:
  status=report['configs'][row['name']]['status']
  p=subprocess.run([sys.executable,'research/automation/registry.py','finish',row['spec'],status,'research/experiments/'+R.name+'/report.json'],cwd=ROOT,text=True,capture_output=True)
  finishes.append({'spec':row['spec'],'fingerprint':row['fingerprint'],'status':status,'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()})
  print(p.returncode,row['name'],status,p.stdout.strip(),p.stderr.strip())
  if p.returncode:break
 (R/'finish.json').write_text(json.dumps(finishes,indent=2,ensure_ascii=False)+'\n')
 if len(finishes)!=len(batch) or any(x['exit_code'] for x in finishes):raise SystemExit('not all registry finish calls succeeded')
 fps={x['fingerprint'] for x in batch};events=[]
 for line in REG.read_text().splitlines():
  row=json.loads(line)
  if row.get('fingerprint') in fps:events.append(row)
 counts={fp:sum(x.get('fingerprint')==fp for x in events) for fp in fps}
 if len(events)!=56 or set(counts.values())!={2}:raise SystemExit(f'registry fragment mismatch: rows={len(events)} counts={set(counts.values())}')
 # Keep the bulky canonical append-only registry unchanged in Git; reader merges this durable sidecar.
 frag=R/'registry_records.jsonl';frag.write_text(''.join(json.dumps(x,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n' for x in events))
 print('all 28 variants finished; 56 immutable reserve/finish events copied to sidecar',hashlib.sha256(frag.read_bytes()).hexdigest())
if __name__=='__main__':main()
