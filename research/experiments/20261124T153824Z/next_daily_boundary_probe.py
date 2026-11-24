"""Expose the saved collector's empty-calendar assumption using real frozen window boundaries."""
import ast,json,hashlib
from pathlib import Path
from datetime import datetime,timedelta
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());parse=lambda s:datetime.fromisoformat(s.replace('Z','+00:00'))
source=R/'collect.py';tree=ast.parse(source.read_text())
nodes=[n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name) and t.value.id=='h' and isinstance(t.slice,ast.Constant) and t.slice.value=='next_window_original_daily_events' for t in n.targets)]
assert len(nodes)==1 and isinstance(nodes[0].value,ast.DictComp) and isinstance(nodes[0].value.value,ast.List) and not nodes[0].value.value.elts
cases=[]
for base in [ROOT/'research/experiments/20261124T133723Z',R]:
 windows=rd(base/'account_windows.json');expected={}
 for account in ['SMA','candidate','l4h02','fewm']:
  start=parse(windows[account]['cutoff_utc']);end=start+timedelta(hours=2);event=parse(windows[account]['next_daily_decision_utc']);rows=[]
  while event<=end:
   if start<event:rows.append(event.isoformat().replace('+00:00','Z'))
   event+=timedelta(days=1)
  expected[account]=rows
 legacy={a:[] for a in expected};cases.append({'round':base.name,'legacy_empty':legacy,'derived_from_real_frozen_timestamps':expected,'legacy_matches':legacy==expected})
print(json.dumps({'collector_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':cases,'new_financial_or_account_calculations':0}),flush=True)
assert cases[0]['legacy_matches']
assert cases[1]['legacy_matches'],'Current next L4/FEWM windows cross the saved original UTC00:01 daily decision; the constant empty calendar is wrong.'
