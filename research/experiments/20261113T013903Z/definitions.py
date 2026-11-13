"""Bind actual input data, exact accounting and preset grid before new research reservation."""
import ast,json
from common import *
P=ROOT/'research/experiments/20261112T233703Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl')
fun=lambda f:{n.name:ast.dump(n,include_attributes=False) for n in ast.parse(f.read_text()).body if isinstance(n,ast.FunctionDef)}
assert (R/'core389.py').read_bytes()==(P/'core389.py').read_bytes()
old,new=fun(P/'engine.py'),fun(R/'engine.py');assert all(old[k]==new[k] for k in old if k!='decide')
node=next(n for n in ast.parse((R/'engine.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='base_decide');node.name='decide';assert ast.dump(node,include_attributes=False)==old['decide']
assert len(batch)==18 and len(p['grid'])==len(p['native_grid'])==9
for z in batch:
 sp=json.loads((ROOT/z['spec']).read_text());assert reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs
 if z['scope']=='parent':assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['initial_capital_usdt']==18750
 else:
  q=sp['parameters'];prior=rs[z['prior_fingerprint']]['spec']['parameters'];assert all(q[k]==v for k,v in prior.items());assert q['initial_capital_usdt']==15000 and q['fixed_entry_notional_usdt']==4000
for fs in p['data']['assets'].values():
 for x in fs:assert sha(ROOT/x['path'])==x['sha256']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
for n in ['flow_data_manifest.json','parent_primitive_verification.json']:assert json.loads((R/n).read_text())['passed']
ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items())
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'flow_data_manifest.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
for z in p['flow_data']['assets'].values():immutable[z['raw']]=z['sha256']
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'original_accounts_have_separate_preexecution_binding':True,'new_native_models':9,'new_parent_models':9,'original_base_policy_AST_unchanged':True,'simulate_and_native_money_AST_unchanged':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':18,'exact_previously_unavailable_fingerprints':18,'no_equal_existing_spec_fingerprint':True,'accounting_and_base_policy_unchanged':True,'two_new_flow_parameters_only':True});print('PASS18exactnewdefinitions;wholebasepolicyandmoneyASTunchanged;boundbeforefirstresearchreserve')
