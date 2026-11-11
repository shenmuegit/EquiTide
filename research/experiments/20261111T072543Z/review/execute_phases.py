"""Sequential execution of named phases; each keeps native command evidence."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
for phase in sys.argv[1:]:
 print('BEGIN',phase,flush=True);p=subprocess.run([sys.executable,'-B',str(R/'commands.py'),phase],cwd=ROOT,env=env)
 if p.returncode:raise SystemExit(p.returncode)
