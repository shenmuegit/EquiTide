#!/usr/bin/env python3
"""Reproduce all 162 deterministic ATR strategy/cost results and audit ledgers locally."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
p=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True)
sys.stdout.write(p.stdout);sys.stderr.write(p.stderr)
if p.returncode:raise SystemExit(p.returncode)
print('reproduction passed: 54 configurations × 3 costs, 12-fold ledgers, ATR recursion, trade identities and registry fragment; no network or registry writes')
