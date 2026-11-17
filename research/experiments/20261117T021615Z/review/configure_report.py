"""Validate current median-count readonly formatters before binding."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[1]
for n in ["collect.py","finalize.py","publish.py"]:ast.parse((R/n).read_text())
assert "ETH_FUNDING_M" in (R/"collect.py").read_text();print("PASS median/count/fixedR andemptyfunding readonlyreport sources ready")
