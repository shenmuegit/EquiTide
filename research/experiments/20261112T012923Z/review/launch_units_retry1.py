import json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
for name in sys.argv[1:]:
 path=R/name;receipt=R/'review'/('native_retry1_'+path.name+'_receipt.json');assert not receipt.exists();a=now();cmd=['/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python','-B',str(path)];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'});log=receipt.with_suffix('.log');log.write_text(p.stdout+p.stderr);receipt.write_text(json.dumps({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':p.returncode,'log':str(log.relative_to(ROOT))},indent=2)+'\n');print(name,p.returncode,(p.stdout+p.stderr)[-3000:],flush=True)
 if p.returncode:raise SystemExit(p.returncode)
