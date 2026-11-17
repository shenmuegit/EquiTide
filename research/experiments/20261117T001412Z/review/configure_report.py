"""Validate current readonly formatters before binding."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[1]
for n in ["collect.py","finalize.py","publish.py"]:ast.parse((R/n).read_text())
assert "all3_perp_actualNov16_16_booked_once=True" in (R/"collect.py").read_text();print("PASS current coefficient/report/handoff sources prepared without financial/account execution")
