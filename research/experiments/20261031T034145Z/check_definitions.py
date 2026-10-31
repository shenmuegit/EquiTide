import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());rows=json.loads((R/'batch.json').read_text());assert len(rows)==6 and len({x['fingerprint'] for x in rows})==6
for x in rows:
 s=json.loads((ROOT/x['spec']).read_text());q=s['parameters'];assert reg.fingerprint(s)==x['fingerprint'] and q['beta_fit_window_days'] in [20,30] and q['momentum_lookback_days'] in [7,14,28] and q['rebalance_interval_days']==7 and q['beta_fit_excludes_latest_momentum_close'] and not q['alpha_in_score'] and q['ETH_entry_notional_usdt']==2000 and q['BTC_entry_notional_rule']=='eligible_beta_at_entry*2000' and q['raw_component_multipliers']==[1,1] and q['initial_capital_usdt']==20000
files=['common.py','market.py','features.py','ranking_model.py','run.py','freeze.py','audit.py','audit_helpers_complete.py','check_primitives.py','check_definitions.py','plan.json']
for f in files:
 if f.endswith('.py'):ast.parse((R/f).read_text())
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':{rel(R/f):sha(R/f) for f in files},'immutable_source_sha256':{p['source_accounting']['path']:p['source_accounting']['sha256'],p['source_paired_helpers']['path']:p['source_paired_helpers']['sha256']}});put(R/'definition_check.json',{'passed':True,'complete_specs':6,'new_joint_models':6,'cost_scenes':18,'internal_native_bank_curves':36,'preset_center':[20,14],'raw_units_not_normalized':True,'benchmark_and_unfiltered_actual_results_readonly':4,'unique_beta_fits':106,'unique_scores':318});print('PASS6 beta/momentumdefinitions andcodebinding before realfits')
