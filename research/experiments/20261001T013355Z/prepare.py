"""Freeze individual configurations and reserve every grid point before evaluating."""
import copy
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path(__file__).resolve().parent
from importlib.util import spec_from_file_location, module_from_spec
modspec = spec_from_file_location('registry', ROOT / 'research/automation/registry.py')
registry = module_from_spec(modspec)
modspec.loader.exec_module(registry)
records = registry.read_records(ROOT / 'research/automation/registry.jsonl')
legacy = {row['fingerprint']: row for row in records.values()}
BASE = {
 'sma_BTC': 'ad27e637fd22f66eb07bb9f7d833cea3489f745e6ece62ad66cfaad19a4776be',
 'sma_ETH': '0e3813f10247e6b4eea16f291f4c3dba20ceb0d3a22d20eaff55128ff54cdcb2',
 'obv_BTC': '0bea2c9cfcc5c5ac41324ccf17d8322920d98d84ffe8ce32027e285c5cb53947',
 'obv_ETH': '159f1a2a25efa89150df9add859c3c6528c45e43b2bc20d9fd10606b40481f0e',
 'sma_equal': 'bf8c57afa75b965ce47e0350ce1f2955b21101c2fbd161b503ef7d1db213b542',
 'obv_equal': 'ab9452ab0b625ca6f7babc1529a4e06b4a3823fe865095d6b47a05727cf2557a'
}

def save_reserve(name, spec):
 spec = copy.deepcopy(spec)
 spec['name'] = name
 spec['validation_plan'] = 'research/experiments/20261001T013355Z/plan.json'
 path = ROUND / 'specs' / (name + '.json')
 path.parent.mkdir(exist_ok=True)
 path.write_text(json.dumps(spec, indent=2) + '\n')
 proc = subprocess.run(['python3', str(ROOT / 'research/automation/registry.py'), 'reserve', str(path)], cwd=ROOT, capture_output=True, text=True)
 if proc.returncode:
  raise RuntimeError(f'{name}: {proc.returncode}: {proc.stdout} {proc.stderr}')
 fp = registry.fingerprint(spec)
 return {'name': name, 'fingerprint': fp, 'spec': str(path.relative_to(ROOT))}

items = []
for key in ('sma_BTC', 'sma_ETH', 'obv_BTC', 'obv_ETH'):
 items.append(save_reserve(key, legacy[BASE[key]]['spec']))
for asset, lookbacks in [('BTC', [60,65,70]), ('ETH', [16,20,24])]:
 for n in lookbacks:
  for allocation in [.5, .75, 1.0]:
   if n == (65 if asset == 'BTC' else 20) and allocation == 1.0:
    continue
   spec = copy.deepcopy(legacy[BASE[f'sma_{asset}']]['spec'])
   spec['parameters']['lookback_days'] = n
   if allocation != 1:
    spec['parameters']['initial_risky_sleeve_fraction'] = allocation
    spec['logic']['sizing'] = 'unlevered spot; next 00:01 UTC minute open; fixed initial risky sleeve fraction, remaining capital permanent USDT; no transfers'
   items.append(save_reserve(f'sma_{asset}_{n}_a{allocation}', spec))
for asset in ('BTC','ETH'):
 for short in (1,2,3):
  for long in (4,6,8):
   if short == 2 and long == 6:
    continue
   spec = copy.deepcopy(legacy[BASE[f'obv_{asset}']]['spec'])
   spec['parameters'].update(short_days=short, long_days=long)
   items.append(save_reserve(f'obv_{asset}_{short}_{long}', spec))
for family in ('sma','obv'):
 items.append(save_reserve(f'{family}_equal', legacy[BASE[f'{family}_equal']]['spec']))
 for w in (.25,.75):
  spec = {'kind':'combination','family':f'daily-{family}-initial-capital','logic':{'allocation':'weights are initial fractions of 2000 USDT capital; sum must equal one; no leverage','rebalance':'no transfers between sleeves'},'parameters':{'initial_capital_usdt':2000},'components':[{'fingerprint':BASE[f'{family}_BTC'],'weight':w},{'fingerprint':BASE[f'{family}_ETH'],'weight':1-w}]}
  items.append(save_reserve(f'{family}_w{w}', spec))
(ROUND / 'batch.json').write_text(json.dumps(items, indent=2) + '\n')
print(json.dumps({'reserved':len(items),'strategy_count':sum('_equal' not in x['name'] and '_w' not in x['name'] for x in items)}))
