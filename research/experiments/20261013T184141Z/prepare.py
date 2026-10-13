#!/usr/bin/env python3
"""Read-only verification of the frozen 27-spec batch; never rewrites or reserves it."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text())
assert plan['status']=='frozen_before_evaluation' and len(batch)==27
fps=set()
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec)
 assert fp==row['fingerprint'] and fp not in fps;fps.add(fp)
 assert spec['parameters']['entry_breakout_lookback_days']==row['entry_breakout_lookback_days']
 assert spec['parameters']['exit_close_channel_lookback_days']==row['exit_close_channel_lookback_days']
 assert spec['parameters']['compression_percentile']==row['compression_percentile']
print(json.dumps({'status':'frozen_specs_verified','count':len(batch),'mutates_plan':False,'reserves':False}))
