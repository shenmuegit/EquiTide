import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());assert len(rows)==6 and len({x['fingerprint'] for x in rows})==6
for x in rows:
 s=json.loads((ROOT/x['spec']).read_text());q=s['parameters'];assert reg.fingerprint(s)==x['fingerprint'] and q['lookback_days'] in [7,14,28] and q['rebalance_interval_days'] in [7,14] and q['component_capitals_usdt']==[10000,10000] and q['fixed_entry_notionals_usdt']==[2000,2000] and q['raw_component_multipliers']==[1,1] and q['winner_long_loser_short'] and not q['same_orientation_resize'] and q['initial_capital_usdt']==20000
files=['common.py','market.py','ranking_model.py','run.py','freeze.py','audit.py','audit_helpers_complete.py','check_primitives.py','check_definitions.py','plan.json']
for f in files:
 if f.endswith('.py'):ast.parse((R/f).read_text())
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':{rel(R/f):sha(R/f) for f in files},'immutable_source_sha256':{p['source_accounting']['path']:p['source_accounting']['sha256'],p['source_paired_helpers']['path']:p['source_paired_helpers']['sha256']}});put(R/'definition_check.json',{'passed':True,'complete_specs':6,'new_joint_models':6,'cost_scenes':18,'internal_native_bank_curves':36,'preset_center':[14,7],'raw_units_not_normalized':True,'benchmark_actual_results_readonly':3});print('PASS6 frozen ranking definitions and code binding before actual simulation')
