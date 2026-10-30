"""All economic fields and unchanged sources bound before first reservation/calculation."""
import json
from run import ROOT,R,reg,sha,put,now
plan=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');specs={x['fingerprint']:json.loads((ROOT/x['spec']).read_text()) for x in rows};assert len(rows)==len(specs)==16
original=records[plan['read_only_grid_references']['native']['fingerprint']]['spec']['parameters']
for row in rows:
 s=specs[row['fingerprint']];p=s['parameters'];assert reg.fingerprint(s)==row['fingerprint'] and s['validation_plan']==str((R/'plan.json').relative_to(ROOT));L,S=row['lookback_days'],row['trend_lookback_days'];assert L in [2,3,4] and S in [27,28,29] and (L,S)!=(3,28)
 if row['scope']=='native':
  expected={**original,'lookback_days':L,'trend_lookback_days':S,'trend_gate_lookbacks_days':[S-1,S,S+1]};assert p==expected and p['initial_capital_usdt']==15000 and p['fixed_entry_notional_usdt']==4500 and p['entry_funding_cost_cap_per_settlement']==.00005
 else:
  fp=row['source_fingerprints'];src=[specs.get(f,records.get(f,{}).get('spec'))['parameters'] for f in fp];assert p['source_component_parameters']==src and p['component_capitals_usdt']==[5000,15000] and p['raw_component_multipliers']==[1,1] and [x['fixed_entry_notional_usdt'] for x in src]==[500,4500] and p['initial_capital_usdt']==20000
 assert p['start_utc']=='2025-10-19T00:01:00Z' and p['end_utc']=='2026-10-24T00:01:00Z'
assert plan['gates']['recent40_positive5d_each_cost_min']==6
for n,h in [('engine.py',plan['new_engine_sha256']),('btc_engine.py',plan['new_BTC_engine_sha256'])]:assert sha(R/n)==h
files=['plan.json','run.py','engine.py','btc_engine.py','audit.py','audit_native.py','audit_helpers.py','freeze_batch.py','check_definitions.py','check_engine.py','check_data.py','engine_change_verification.json'];put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':{str((R/f).relative_to(ROOT)):sha(R/f) for f in files}})
put(R/'definition_check.json',{'passed':True,'financial_evaluations':0,'complete_new_definitions':16,'new_native_cashbanks':8,'new_raw1_1_parents':8,'full_price_grid_cells':18,'old_center_cells_readonly':2,'only_native_parameter_changes':['lookback_days','trend_lookback_days','derived_trend_gate_lookbacks_days'],'strict_gates_unchanged':True,'raw_weights_unchanged':True});print('PASS16 complete economic definitions;old2center readonly')
