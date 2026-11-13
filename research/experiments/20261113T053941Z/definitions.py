"""Bind passive new pairings before any parent valuation."""
import ast,json
from common import *
p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==6 and len(p['grid'])==9
for z in batch:
 sp=json.loads((ROOT/z['spec']).read_text());assert z['scope']=='parent' and reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs and [q['weight'] for q in sp['components']]==[1,1] and sp['parameters']['initial_capital_usdt']==18750
 assert sp['parameters']['source_component_spec_sha256']==[p['read_only_references'][q['fingerprint']]['spec_sha256'] for q in sp['components']]
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
for fs in p['data']['assets'].values():
 for x in fs:assert sha(ROOT/x['path'])==x['sha256']
assert json.loads((R/'parent_primitive_verification.json').read_text())['passed'];ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items())
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'research/experiments/20261113T033939Z/forward_inputs.json.gz',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_parent_calculation_yet':True,'new_native_models':0,'new_parent_models':6,'native_engine_execution_forbidden':True,'all_source_native_results_read_only':True,'original_accounts_separately_bound_before_execution':True})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':6,'new_exact_pairings':6,'read_only_exact_grid_cells':3,'native_source_results':8,'no_NAV_scaling_or_native_policy_run':True});print('PASS6genuinepairs preregistered definitions and immutable sources;0nativepolicyexecution')
