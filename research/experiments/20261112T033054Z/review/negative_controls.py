import os,subprocess,sys,json
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
for name,flag in [('negative_fixed_N','--fixed-N'),('negative_future_open','--future-open'),('negative_linear_impact','--linear-impact'),('negative_doubleweight','--doubleweight')]:
 path=R/(name+'_receipt.json');assert not path.exists();cmd=[sys.executable,'-B',str(R/'units.py'),flag];a=now();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});(R/(name+'.log')).write_text(p.stdout+p.stderr);path.write_text(json.dumps({'command':cmd,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':p.returncode,'expected_exit_code':1,'synthetic_only':True,'log':str((R/(name+'.log')).relative_to(ROOT))},indent=2)+'\n');print(name,p.returncode,flush=True);assert p.returncode==1
