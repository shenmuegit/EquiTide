import json
from run import ROOT,R,sha,put,reg,now
p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');by={r['fingerprint']:json.loads((ROOT/r['spec']).read_text()) for r in rows};assert len(rows)==66 and sum(x['role']=='candidate' for x in rows)==27 and sum(x['scope']=='native' for x in rows)==36
for x in rows:
 sp=by[x['fingerprint']];q=sp['parameters'];a=x['fast_ETH_bank_units'];assert reg.fingerprint(sp)==x['fingerprint'] and a in [.25,.5,.75]
 if x['scope']=='native':assert q['initial_capital_usdt']==x['capital_usdt'] and q['fixed_entry_notional_usdt']==x['fixed_entry_notional_usdt'] and q['raw_entry_notional_fraction_of_initial_capital']==q['fixed_entry_notional_usdt']/q['initial_capital_usdt']
 else:
  assert q['raw_component_multipliers']==[1,1,1] and q['component_capitals_usdt']==[5000,15000*a,15000*(1-a)] and q['initial_capital_usdt']==20000 and q['source_component_parameters']==[(by[f] if f in by else records[f]['spec'])['parameters'] for f in x['source_fingerprints']] and [v['fixed_entry_notional_usdt'] for v in q['source_component_parameters']]==[500,4500*a,1500*(1-a)] and sum(q['component_capitals_usdt'])==20000
assert p['gates']['recent40_positive5d_each_cost_min']==6
files=['plan.json','run.py','audit.py','audit_native.py','audit_helpers.py','engine.py','fast_engine.py','freeze_batch.py','check_definitions.py','check_engine.py','check_data.py'];put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':{str((R/f).relative_to(ROOT)):sha(R/f) for f in files}});put(R/'definition_check.json',{'passed':True,'new_complete_specs':66,'candidates':27,'references_and_components':39,'new_native_components':36,'old_source_banks':14,'3D_cells':27,'edges':54,'rawweights_not_normalized':True,'native_new_capital_notional_simulations_required':True});print('PASS66 complete independentcashbank native/parent definitions')
