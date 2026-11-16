"""Bind exact policy/accounting sources and all full specs before first reservation."""
import ast,json
from common import *
P=ROOT/'research/experiments/20261116T020401Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl')
funs=lambda f:{x.name:ast.dump(x,include_attributes=False) for x in ast.parse(f.read_text()).body if isinstance(x,ast.FunctionDef)}
before,after=funs(P/'engine.py'),funs(R/'engine.py');assert set(after)-set(before)=={'btc_directional_risk'} and all(before[k]==after[k] for k in before if k!='base_decide') and before['base_decide']!=after['base_decide']
oldnode=ast.parse((P/'engine.py').read_text()).body;newnode=ast.parse((R/'engine.py').read_text()).body
oldbase=next(x for x in oldnode if isinstance(x,ast.FunctionDef) and x.name=='base_decide');newbase=next(x for x in newnode if isinstance(x,ast.FunctionDef) and x.name=='base_decide')
assert all(ast.dump(x,include_attributes=False)==ast.dump(y,include_attributes=False) for x,y in zip(oldbase.body[3:],newbase.body[3:])) and len(oldbase.body)==len(newbase.body)
assert sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')

assert len(batch)==6 and len(p['grid'])==6 and len(p['native_grid'])==5 and len(p['read_only_references'])==8
for z in batch:
 sp=json.loads((ROOT/z['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs and q['continuous_oos_days']==391 and q['end_utc']=='2026-11-14T00:01:00Z' and q['tail_fold_days']==1 and q['positive_complete30d_folds_required']==10
 if z['scope']=='native':assert z['asset']=='BTC' and q['lookback_days']==29 and q['return_hurdle']==.03 and q['exit_buffer_fraction']==.005 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.0275 and q['entry_adverse_volatility_blend'] in [.25,.5] and q['entry_volatility_gate_scope']=='new_or_reversed_position_only' and (q['initial_capital_usdt'],q['fixed_entry_notional_usdt'])==(3750,1000)
 else:assert [x['weight'] for x in sp['components']]==[1,1] and [x['fingerprint'] for x in sp['components']]==z['source_fingerprints'] and q['initial_capital_usdt']==18750
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items()) and json.loads((R/'parent_primitive_verification.json').read_text())['passed']
descriptor=p['rules']['signal'];assert descriptor.startswith('BTC completedROC L29/strictentryH.03/fixedexitE.005/V10directionalAdverseBlend[0,.25,.5]/cap.0275.')
assert all(json.loads((ROOT/z['spec']).read_text())['logic']['signal']==descriptor for z in batch)
assert all(json.loads((ROOT/z['spec']).read_text())['parameters']['entry_adverse_volatility_blend']==z['W'] for z in batch if z['scope']=='native')
put(R/'signal_scalar_consistency_before_reservation.json',{'passed':True,'recorded_utc':now(),'explicit_signal':descriptor,'scalar_L':29,'scalar_H':.03,'fixed_E':.005,'native_blends':[.25,.5],'old_blend_readonly':0,'fixed_cap':.0275,'native_V':10,'all_new_specs_match_descriptor_and_scalar_axis':True,'before_first_reservation':True,'no_market_or_account_calculations':True})
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'new_native_models':2,'new_parent_models':4,'readonly_existing_native_models':5,'readonly_existing_parent_models':3,'simulate_and_native_money_AST_unchanged':True,'BTC_entry_risk_policy_intentionally_changed':True,'ETH_AST_and_all_existing_nonpolicy_helpers_unchanged':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':6,'all_exact_new_fingerprints_absent':True,'only_BTC_entry_risk_policy_changed_all_money_and_ETH_unchanged':True,'full_core_source_bytes_unchanged':True,'raw_weights_not_normalized':True,'readonly_existing_configs':8});print('PASS6definitions,8read-only;BTC directional adverse-risk formula bound; money core bytes, simulate AST and ETH unchanged;bound before first reserve')
