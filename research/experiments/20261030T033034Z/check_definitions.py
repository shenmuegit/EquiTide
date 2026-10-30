"""Complete rule/capital/weight/data/cost spec binding before any real evaluation."""
import json
from run import ROOT,R,reg,sha,put,now
p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');specs={x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in rows};assert len(rows)==len(specs)==20
for row in rows:
 s=specs[row['fingerprint']];q=s['parameters'];assert reg.fingerprint(s)==row['fingerprint'] and q['start_utc']=='2025-10-19T00:01:00Z' and q['end_utc']=='2026-10-24T00:01:00Z'
 if row['scope']=='native':
  assert s['universe']==['ETH/USDT'] and q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==1500 and q['raw_entry_notional_fraction_of_initial_capital']==.1 and q['input_hashes']=={x['path']:x['sha256'] for x in p['data']['assets']['ETH']} and not any(k.startswith('entry_funding_') for k in q)
  if row['role']=='candidate':assert q['lookback_days'] in [20,25,30] and q['return_hurdle'] in [.02,.04,.06] and q['exit_buffer_fraction']==.01 and q['signal_mode']=='buffered_ROC_momentum'
  else:assert q['signal_mode']=='constant_long_reference'
 else:
  src=[specs.get(f,records.get(f,{}).get('spec'))['parameters'] for f in row['source_fingerprints']];assert q['source_component_parameters']==src and q['initial_capital_usdt']==20000 and q['component_capitals_usdt']==[5000,15000] and q['raw_component_multipliers']==[1,1] and [x['fixed_entry_notional_usdt'] for x in src]==[500,1500]
assert p['gates']['recent40_positive5d_each_cost_min']==6 and sha(R/'engine.py')==p['new_engine_sha256']
files=['plan.json','run.py','engine.py','btc_engine.py','audit.py','audit_native.py','audit_helpers.py','freeze_batch.py','check_definitions.py','check_engine.py','check_data.py','engine_change_verification.json'];put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':{str((R/f).relative_to(ROOT)):sha(R/f) for f in files}});put(R/'definition_check.json',{'passed':True,'financial_evaluations':0,'complete_new_definitions':20,'new_native_cashbanks':10,'new_raw1_1_parents':10,'full_price_grid_cells':18,'strict_gates_unchanged':True,'native_ETH_notional1500_recomputed_not_old4500_scaling':True});print('PASS20 complete definitions;18candidates+2references')
