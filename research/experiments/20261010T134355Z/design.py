"""Predeclared ETH EMA span/band neighbourhood; definitions only, no evaluation."""
from copy import deepcopy
import json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
EMA_LOGIC=json.loads((R/'research/experiments/20261002T235103Z/specs/filtered_2026_ETH_e15_s50.json').read_text())['logic']
AXES={'EMA_span_days':[27,30,33],'EMA_symmetric_band':[.01,.0125,.015]}
def source_spec(old,span,band):
 sp=deepcopy(old);sp['parameters'].update(EMA_span_days=span,EMA_symmetric_band=band)
 return sp
