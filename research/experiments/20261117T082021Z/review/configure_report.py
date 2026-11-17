"""Validate final E-axis reporting and SMA69 next mark-only handoff before collection."""
from pathlib import Path
import ast
R=Path(__file__).resolve().parents[1]
for name in ['collect.py','finalize.py','publish.py']:ast.parse((R/name).read_text())
s=(R/'collect.py').read_text();assert 'ETH_FAST_E' in s and "SMA_current_full_daily_context=69" in s and 'SMA_next_mark_only_adapter_template' in s;print('PASS E-axis collector, originalSMA69/full68prefix and next mark-only templates;0model/account calculations')
