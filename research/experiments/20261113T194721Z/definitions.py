"""Bind unchanged native accounting and only explicitly parameterized BTC branch."""
import ast,json
from common import *
P=ROOT/'research/experiments/20261113T174515Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');fun=lambda f:{n.name:n for n in ast.parse(f.read_text()).body if isinstance(n,ast.FunctionDef)};old,new=fun(P/'engine.py'),fun(R/'engine.py');dump=lambda n:ast.dump(n,include_attributes=False)
assert (R/'core389.py').read_bytes()==(P/'core389.py').read_bytes() and all(dump(old[k])==dump(new[k]) for k in old if k!='base_decide')
assert [dump(n) for n in old['base_decide'].body[:2]]==[dump(n) for n in new['base_decide'].body[:2]] and [dump(n) for n in old['base_decide'].body[3:]]==[dump(n) for n in new['base_decide'].body[3:]]
assert len(batch)==8 and len(p['grid'])==len(p['native_grid'])==9
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs
 if row['scope']=='parent':assert [x['weight'] for x in sp['components']]==[1,1] and sp['parameters']['initial_capital_usdt']==18750 and sp['components'][1]['fingerprint']==p['fixed_ETH_fingerprint']
 else:
  q=sp['parameters'];prior=rs[row['prior_fingerprint']]['spec']['parameters'];assert sp['universe']==['BTC/USDT'] and all(q[k]==v for k,v in prior.items() if k not in ['lookback_days','exit_buffer_fraction']);assert q['lookback_days'] in [27,31] and q['exit_buffer_fraction'] in [.005,.01,.015] and q['return_hurdle']==.03 and q['initial_capital_usdt']==3750 and q['fixed_entry_notional_usdt']==1000 and q['warmup_days']>=q['lookback_days']+1
for fs in p['data']['assets'].values():
 for x in fs:assert sha(ROOT/x['path'])==x['sha256']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
assert json.loads((R/'parent_primitive_verification.json').read_text())['passed'];ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items())
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'original_accounts_have_separate_preexecution_binding':True,'new_native_models':4,'new_parent_models':4,'changed_policy_scope':'OnlyBTC declaredL27/29/31 and E0.5/1/1.5percent;H3percent fixed;ETH and money functions unchanged;5oldgridcells reused','simulate_and_native_money_AST_unchanged':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':8,'exact_previously_unavailable_fingerprints':8,'no_equal_existing_spec_fingerprint':True,'only_BTC_LE_policy_parameterized':True,'ETH_policy_and_all_money_functions_AST_unchanged':True,'two_BTC_lookback_exit_axes_and_readonly_anchors':True});print('PASS8newdefinitions;onlyBTCbranchL/Eparameterized;cash/q/trade/funding/ETHASTunchanged;boundbeforefirstresearchreserve')
