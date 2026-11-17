"""Run authorized phases sequentially and retain actual process results."""
import os,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2]
for phase in sys.argv[1:]:
 z=subprocess.run(['/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python','-B',str(R/'commands.py'),phase],cwd=ROOT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'})
 if z.returncode:raise SystemExit(z.returncode)
