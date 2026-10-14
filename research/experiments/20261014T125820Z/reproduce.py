#!/usr/bin/env python3
"""Recompute/audit all 54 saved results locally, without network or registry writes."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
p=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True)
sys.stdout.write(p.stdout);sys.stderr.write(p.stderr)
if p.returncode:raise SystemExit(p.returncode)
print('reproduction passed: 18 configs × 3 costs, full minute-close sample SHA, folds, trade ledger and registry fragment')
