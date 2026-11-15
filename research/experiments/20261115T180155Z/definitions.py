"""Bind exact policy/accounting sources and all full specs before first reservation."""
import ast,json
from common import *
P=ROOT/'research/experiments/20261115T160124Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');funs=lambda f:{x.name:ast.dump(x,include_attributes=False) for x in ast.parse(f.read_text().replace('V in [6,8,10,12,14]','V in [6,10,14]').replace('window in [6,8,10,12,14]','window in [6,10,14]')).body if isinstance(x,ast.FunctionDef)}
assert funs(P/'engine.py')==funs(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
assert len(batch)==6 and len(p['grid'])==6 and len(p['native_grid'])==5 and len(p['read_only_references'])==8
for z in batch:
 sp=json.loads((ROOT/z['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs and q['continuous_oos_days']==391 and q['end_utc']=='2026-11-14T00:01:00Z' and q['tail_fold_days']==1 and q['positive_complete30d_folds_required']==10
 if z['scope']=='native':assert z['asset']=='BTC' and q['lookback_days'] in [28,30] and q['return_hurdle']==.03 and q['exit_buffer_fraction']==.005 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.0275 and q['entry_volatility_gate_scope']=='new_or_reversed_position_only' and (q['initial_capital_usdt'],q['fixed_entry_notional_usdt'])==(3750,1000)
 else:assert [x['weight'] for x in sp['components']]==[1,1] and [x['fingerprint'] for x in sp['components']]==z['source_fingerprints'] and q['initial_capital_usdt']==18750
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items()) and json.loads((R/'parent_primitive_verification.json').read_text())['passed']
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'new_native_models':2,'new_parent_models':4,'readonly_existing_native_models':5,'readonly_existing_parent_models':3,'simulate_and_native_money_AST_unchanged':True,'policy_and_accounting_source_equal_to_prior':True,'policy_and_money_formulas_unchanged_except_predeclared_parameter_allowlist':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':6,'all_exact_new_fingerprints_absent':True,'all_policy_and_native_money_AST_unchanged_after_allowlist_normalization':True,'full_core_source_bytes_unchanged':True,'raw_weights_not_normalized':True,'readonly_existing_configs':8});print('PASS6definitions,8read-only;allpolicy/corebytesunchanged;boundbeforefirstreserve')
