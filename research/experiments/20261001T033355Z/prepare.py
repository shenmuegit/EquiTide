"""Reserve full pair/carry grid, including comparators, before any real simulation."""
import copy
import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
ROUND=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('registry',ROOT/'research/automation/registry.py')
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)
ledger=ROOT/'research/automation/registry.jsonl'
records=m.read_records(ledger)
legacy={k:records[v]['spec'] for k,v in {'pairs':'918c7fe5b7fcc3e068c0e68492a6d94e341c5ba65a46cdd538dbc28d81806f42','cross':'c18984238a12bdde2478a5a3bd052c3a4be93b625181d0240becf6f64e4f5cd0'}.items()}
(ROUND/'prior_ledger_summary.json').write_text(json.dumps({'read_at_utc':datetime.now(timezone.utc).isoformat(),'ledger_sha256':hashlib.sha256(ledger.read_bytes()).hexdigest(),'event_count':len(ledger.read_text().splitlines()),'historical_id_count':len(records),'distinct_definitions':len({m.fingerprint(x['spec']) for x in records.values()}),'reserved_before_round':[k for k,v in records.items() if v['status']=='reserved'],'remaining_initial_missing':5},indent=2)+'\n')
items=[]
def save(name,spec,role='candidate'):
 spec=copy.deepcopy(spec)
 spec.update(name=name,validation_plan='research/experiments/20261001T033355Z/plan.json')
 path=ROUND/'specs'/(name+'.json')
 path.parent.mkdir(exist_ok=True)
 path.write_text(json.dumps(spec,indent=2)+'\n')
 p=subprocess.run(['python3',str(ROOT/'research/automation/registry.py'),'reserve',str(path.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(f'{name}: {p.returncode}: {p.stdout} {p.stderr}')
 items.append({'name':name,'fingerprint':m.fingerprint(spec),'spec':str(path.relative_to(ROOT)),'role':role,'direction':'pairs' if name.startswith('pairs') else 'cross' if name.startswith('cross') else 'benchmark'})
for window in [600,720,840]:
 for z in [1.8,2,2.2]:
  spec=copy.deepcopy(legacy['pairs']);spec['parameters'].update(window_hours=window,entry_z=z)
  save(f'pairs_w{window}_z{z}',spec)
for window in [240,270,300]:
 for z in [1.8,2,2.2]:
  spec=copy.deepcopy(legacy['cross']);spec['parameters'].update(window_settlements=window,entry_z=z)
  save(f'cross_w{window}_z{z}',spec)
# Timestamp boundaries determined by 6 folds of 28 days after fixed training+3-day embargo.
for name,assets,start,end,capital in [('benchmark_pairs_hold',['BTC/USDT','ETH/USDT'],'2026-03-18T00:01:00Z','2026-09-02T00:01:00Z',2000),('benchmark_cross_hold',['BTC/USDT'],'2026-03-29T01:01:00Z','2026-09-13T01:01:00Z',100000)]:
 save(name,{'kind':'strategy','family':'spot-hold-comparator','market':'spot','universe':assets,'timeframe':'1h','logic':{'entry':'initial equal-capital long spot sleeves at first validation 00:01 or 01:01 minute open','exit':'scheduled terminal exit at prespecified minute open','sizing':'unlevered spot; no transfers between sleeves; cash zero yield'},'parameters':{'start_utc':start,'end_utc':end,'initial_capital_usdt':capital}},'comparator')
(ROUND/'batch.json').write_text(json.dumps(items,indent=2)+'\n')
print(json.dumps({'reserved':len(items),'candidates':18,'comparators':2}))
