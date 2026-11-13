import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
for phase in sys.argv[1:]:
 print('BEGIN',phase,flush=True);p=subprocess.run([sys.executable,'-B',str(R/'commands.py'),phase],cwd=ROOT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 if p.returncode:raise SystemExit(p.returncode)
