#!/usr/bin/env python3
"""Repeat all 54 deterministic sleeve runs and verify published metrics without HTTP."""
import hashlib,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
files=['report.json','result.md','fold_results.csv','cost_scenarios.csv','equity_curves_daily.csv','sensitivity.csv','sensitivity_surface.svg']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before={name:sha(R/name) for name in files}
p=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True)
if p.returncode:raise SystemExit(p.stdout+'\n'+p.stderr)
after={name:sha(R/name) for name in files}
assert before==after,{'before':before,'after':after}
print('reproduction passed: 54 deterministic configurations/scenes, exact report and artifacts, no HTTP or registry write')
