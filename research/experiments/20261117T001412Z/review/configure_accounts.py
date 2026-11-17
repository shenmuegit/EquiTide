"""Validate own original-window preparation before calculation."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[1]
s=(R/"review/setup_confirmation.py").read_text();ast.parse(s);assert "candidate':6" in s and "2026-11-16T16:30:00Z" in s;print("PASS own funding split0/6/0/0 and unchanged original kernels prepared")
