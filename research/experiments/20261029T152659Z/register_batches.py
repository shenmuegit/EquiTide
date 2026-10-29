"""Five bounded real registry batches,each at most8 complete configurations."""
import json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
phase=sys.argv[1];assert phase in ['reserve','finish'];dest=R/(phase+'_batch_commands.json');assert not dest.exists();out=[];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
for i in range(5):
 cmd=[sys.executable,str(R/(phase+'_batch.py'))];start=datetime.now(timezone.utc).isoformat();p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);log=R/f'{phase}_batch_{i:03d}.log';log.write_text(p.stdout+p.stderr);row={'command':cmd,'cwd':str(ROOT),'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':p.returncode,'log':str(log.relative_to(ROOT))};out.append(row);dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'phase':phase,'batch':i,'exit_code':p.returncode,'last_output':(p.stdout+p.stderr)[-1100:]}),flush=True)
 if p.returncode:
  q=R/'read_failures.json';d=json.loads(q.read_text());d['facts'].append({**row,'stderr':p.stderr});q.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');raise SystemExit(p.returncode)
