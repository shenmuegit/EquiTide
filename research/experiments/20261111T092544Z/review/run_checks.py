"""Execute bounded read-only review helpers; keep every actual failure and receipt."""
import json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];PY='/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python';now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z');env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
for name in sys.argv[1:]:
 source=R/'review'/name;receipt=R/('review_'+name+'_receipt.json');log=R/('review_'+name+'.log');assert not receipt.exists();cmd=[PY,'-B',str(source)];start=now();p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);row={'command':cmd,'cwd':str(ROOT),'started_utc':start,'finished_utc':now(),'actual_exit_code':p.returncode,'log':str(log.relative_to(ROOT)),'stderr':p.stderr};log.write_text(p.stdout+p.stderr);receipt.write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n');print(json.dumps({**row,'last_output':(p.stdout+p.stderr)[-1200:]}),flush=True)
 if p.returncode:
  f=R/'read_failures.json';d=json.loads(f.read_text());d['facts'].append({**row,'resolved':False});f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');raise SystemExit(p.returncode)
