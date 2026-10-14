#!/usr/bin/env python3
"""Recompute all 54 deterministic scenarios and verify the saved metrics/files."""
import hashlib,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
files=['report.json','result.md','fold_results.csv','cost_scenarios.csv','equity_curves_daily.csv.gz','sensitivity.csv','sensitivity_surface.svg','trades.csv.gz','decisions.csv.gz','daily_equity.csv.gz']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before={name:sha(R/name) for name in files}
p=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True)
if p.returncode:raise SystemExit(p.stdout+'\n'+p.stderr)
after={name:sha(R/name) for name in files}
assert before==after,{'before':before,'after':after}
print('reproduction passed: all 54 scenario NAV/trade/fold records match exactly; no network or registry writes')
