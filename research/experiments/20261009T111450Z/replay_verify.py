"""Capture explicit exits from the required synthetic, exact replay and evidence audits."""
from pathlib import Path
import json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2]
commands=[['.venv/bin/python',str((T/'check_signals.py').relative_to(R))],['.venv/bin/python',str((T/'restore_cache.py').relative_to(R))],['.venv/bin/python',str((T/'forward.py').relative_to(R)),'--reproduce'],['.venv/bin/python',str((T/'evaluate.py').relative_to(R)),'--reproduce'],['.venv/bin/python',str((T/'audit.py').relative_to(R))],['.venv/bin/python',str((T/'audit_forward.py').relative_to(R))],['.venv/bin/python','checks/strategy_registry.py']];done=[]
with (T/'reproduce.log').open('w')as log:
 for command in commands:
  p=subprocess.run(command,cwd=R,capture_output=True,text=True);log.write(p.stdout+p.stderr);log.flush();done.append({'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});(T/'reproduction_execution.json').write_text(json.dumps(done,indent=2)+'\n');print(json.dumps({'phase':command[1],'exit_code':p.returncode}),flush=True)
  if p.returncode:sys.exit(p.returncode)
print('READONLY_REPRODUCTION_ALL_7_EXIT_ZERO',flush=True)
