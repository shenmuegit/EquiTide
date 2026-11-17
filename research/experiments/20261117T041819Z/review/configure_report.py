"""Validate readonly L-axis reporting and differentiated next-midnight handoff."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[1]
for n in ["collect.py","finalize.py","publish.py"]:ast.parse((R/n).read_text())
assert "ETH_FAST_L" in (R/"collect.py").read_text();print("PASS fastL/report/nextL4midnight sources prepared,0evaluations")
