"""Bind exact policy/accounting sources and all full specs before first reservation."""
import ast,json
from common import *
P=ROOT/'research/experiments/20261116T141010Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl')

before=(P/'engine.py').read_text();after=(R/'engine.py').read_text();assert after==before.replace("p['return_hurdle'] in [.025,.03,.035]","p['return_hurdle'] in [.025,.0275,.03,.0325,.035]") and ast.dump(ast.parse(after.replace("p['return_hurdle'] in [.025,.0275,.03,.0325,.035]","p['return_hurdle'] in [.025,.03,.035]")))==ast.dump(ast.parse(before)) and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')

assert len(batch)==6 and len(p['grid'])==6 and len(p['native_grid'])==5 and len(p['read_only_references'])==8
for z in batch:
 sp=json.loads((ROOT/z['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs and q['continuous_oos_days']==391 and q['end_utc']=='2026-11-14T00:01:00Z' and q['tail_fold_days']==1 and q['positive_complete30d_folds_required']==10
 if z['scope']=='native':assert z['asset']=='BTC' and q['lookback_days']==29 and q['return_hurdle']==z['W'] and q['return_hurdle'] in [.0275,.0325] and q['exit_buffer_fraction']==.005 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.0275 and q['entry_directional_confirmation_lookback_days']==5 and q['entry_directional_confirmation_hurdle']==.0025 and q['entry_volatility_gate_scope']=='new_or_reversed_position_only' and (q['initial_capital_usdt'],q['fixed_entry_notional_usdt'])==(3750,1000)
 else:assert [x['weight'] for x in sp['components']]==[1,1] and [x['fingerprint'] for x in sp['components']]==z['source_fingerprints'] and q['initial_capital_usdt']==18750
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items()) and json.loads((R/'parent_primitive_verification.json').read_text())['passed']
descriptor=p['rules']['signal'];assert descriptor.startswith('BTC completedROC L29/strictentryH[.0275,.03,.0325]/fixedexitE.005/V10samplelogvolCap.0275/strictDirectionalRecentROC5DaysMinimum.0025.')
assert all(json.loads((ROOT/z['spec']).read_text())['logic']['signal']==descriptor for z in batch)
assert all(json.loads((ROOT/z['spec']).read_text())['parameters']['return_hurdle']==z['W'] for z in batch if z['scope']=='native')
put(R/'signal_scalar_consistency_before_reservation.json',{'passed':True,'recorded_utc':now(),'explicit_signal':descriptor,'scalar_L':29,'scalar_H':[.0275,.03,.0325],'fixed_E':.005,'native_main_entry_hurdles':[.0275,.0325],'fixed_volatility_cap':.0275,'confirmation_days_fixed':5,'confirmation_min_return_fixed':.0025,'old_H03_bank_readonly':True,'native_V':10,'all_new_specs_match_descriptor_and_scalar_axis':True,'before_first_reservation':True,'no_market_or_account_calculations':True})
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'new_native_models':2,'new_parent_models':4,'readonly_existing_native_models':5,'readonly_existing_parent_models':3,'simulate_and_native_money_AST_unchanged':True,'BTC_entry_risk_policy_intentionally_changed':False,'ETH_AST_and_all_existing_nonpolicy_helpers_unchanged':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':6,'all_exact_new_fingerprints_absent':True,'only_BTC_H_validation_allowlist_extended_money_and_ETH_unchanged':True,'full_core_source_bytes_unchanged':True,'raw_weights_not_normalized':True,'readonly_existing_configs':8});print('PASS6definitions,8read-only;BTCmainentryhurdles bound;engine allowlist-only change; money core bytes, simulate AST and ETH unchanged;bound before first reserve')
