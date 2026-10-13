#!/usr/bin/env python3
"""Read-only validation of the frozen 4h momentum parameter batch."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text())
assert plan['status']=='frozen_before_evaluation' and len(batch)==28
seen=set()
for item in batch:
 spec=json.loads((ROOT/item['spec']).read_text());fp=registry.fingerprint(spec)
 assert fp not in seen;seen.add(fp)
 for key in ('lookback_4h_bars','entry_return_threshold_bps','exit_return_threshold_bps'):
  if key in item:assert spec['parameters'][key]==item[key]
print(json.dumps({'status':'frozen_specs_verified','candidates':27,'comparators':1,'read_only':True,'reserved':False}))
