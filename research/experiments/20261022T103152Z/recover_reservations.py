"""Complete the existing frozen batch after a metadata-only family-ID correction."""
import copy
import importlib.util
import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location('cci_frozen_recovery', R / 'run.py')
m = importlib.util.module_from_spec(s)
sys.modules[s.name] = m
s.loader.exec_module(m)

assert not (R / 'report.json').exists() and not (R / 'batch.json').exists()
correction = json.loads((R / 'family_id_correction.json').read_text())
plan = json.loads((R / 'plan.json').read_text())
original = json.loads((R / 'failures/freeze_attempt1_spec.json').read_text())
assert m.sha(R / 'plan.json') == correction['frozen_plan_sha256_unchanged']
assert m.sha(R / 'context.json') == correction['context_sha256_unchanged']
try:
    m.ev.registry.fingerprint(original)
except ValueError as error:
    assert 'lowercase ID' in str(error)
else:
    raise AssertionError('The preserved uppercase-family failure did not reproduce')

template = copy.deepcopy(original)
template['family'] = correction['repaired_family']
assert {k: v for k, v in template.items() if k != 'family'} == {k: v for k, v in original.items() if k != 'family'}
m.ev.registry.fingerprint(template)
batch = []
for asset in plan['grid']['assets']:
    for look in plan['grid']['cci_lookback_days']:
        for threshold in plan['grid']['entry_cci_threshold']:
            spec = copy.deepcopy(template)
            name = f'daily_cci_{asset}_N{look}_E{threshold}'
            spec.update(name=name, universe=[asset + '/USDT'])
            spec['parameters'].update(asset=asset, cci_lookback_days=look, entry_cci_threshold=threshold)
            path = R / 'specs' / (name + '.json')
            m.put(path, spec)
            batch.append({'name': name, 'asset': asset, 'cci_lookback_days': look, 'entry_cci_threshold': threshold, 'spec': m.rel(path), 'fingerprint': m.ev.registry.fingerprint(spec)})
assert len(batch) == len({b['fingerprint'] for b in batch}) == 18
m.put(R / 'batch.json', batch)
m.put(R / 'spec.json', json.loads((R / 'specs/daily_cci_BTC_N40_E100.json').read_text()))
reserves = []
for row in batch:
    reserves.append(m.call('reserve', row))
    m.put(R / 'reserve.json', reserves)
assert m.sha(R / 'plan.json') == correction['frozen_plan_sha256_unchanged']
assert m.sha(R / 'context.json') == correction['context_sha256_unchanged']
print('RECOVERED_SAME_FROZEN_RULES_AND_RESERVED', len(reserves), m.sha(R / 'plan.json'), flush=True)
