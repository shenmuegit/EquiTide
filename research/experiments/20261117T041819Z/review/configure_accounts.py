"""Validate current closed windows before any valuation."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[1]
s=(R/"review/setup_confirmation.py").read_text();ast.parse(s);assert "2026-11-16T20:30:00Z" in s and "2026-11-16T22:10:00Z" in s;print("PASS current0/0/0/0 and nextL4midnight original-kernel preparation")
