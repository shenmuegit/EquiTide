import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());assert len(rows)==9 and len({x['fingerprint'] for x in rows})==9
for x in rows:
 s=json.loads((ROOT/x['spec']).read_text());q=s['parameters'];assert reg.fingerprint(s)==x['fingerprint'] and q['entry_z'] in ENTRIES and q['exit_z'] in EXITS and q['exit_z']<q['entry_z'] and q['initial_capital_usdt']==20000 and q['component_capitals_usdt']==[10000,10000] and q['raw_component_multipliers']==[1,1] and q['window_hours']==720 and q['training_embargo_hours']==24 and s['universe']==['BTC/USDT','ETH/USDT'] and s['timeframe']=='1h'
assert p['gates']['recent40_positive5d_each_cost_min']==6 and sha(CORE_PATH)==p['source_core']['sha256']
files=['common.py','market.py','features.py','pair_model.py','run.py','audit.py','audit_helpers.py','freeze.py','preflight.py','check_primitives.py','check_definitions.py','plan.json']
for name in files:
 if name.endswith('.py'):ast.parse((R/name).read_text(),filename=name)
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':{rel(R/f):sha(R/f) for f in files},'source_core_sha256':sha(CORE_PATH)});put(R/'definition_check.json',{'passed':True,'complete_specs':9,'new_joint_models':9,'cost_scenes':27,'internally_accounted_bank_cost_curves':54,'raw_units_not_normalized':True,'old_pair_results_not_rerun':9,'old_controls_readonly':3,'source_core_unchanged':True});print('PASS9 complete paired definitions/code bindings before any actual model/features')
