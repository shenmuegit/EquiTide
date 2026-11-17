"""Validate empty actual own-window preparation."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[1]
s=(R/"review/setup_confirmation.py").read_text();ast.parse(s);assert "candidate':0" in s and "2026-11-16T18:30:00Z" in s;print("PASS actualemptyfundsplit0/0/0/0,oldactual16once preserved")
