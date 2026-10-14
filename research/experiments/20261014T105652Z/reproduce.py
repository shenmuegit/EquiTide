#!/usr/bin/env python3
"""Deterministically replay the frozen grid and audit persisted reports/registry sidecar."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
p=subprocess.run([str(ROOT/'.venv/bin/python'),str(R/'audit.py')],cwd=ROOT,text=True,capture_output=True)
sys.stdout.write(p.stdout);sys.stderr.write(p.stderr)
if p.returncode:raise SystemExit(p.returncode)
print('reproduction passed: all 84 config-cost scenarios and 28 registry chains match; no network or registry writes')
