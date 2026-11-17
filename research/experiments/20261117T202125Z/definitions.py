"""Bind every full spec and immutable kernel before the first reservation."""
import json
from common import *
P=ROOT/'research/experiments/20261117T182123Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl')
assert sha(P/'engine.py')==sha(R/'engine.py') and sha(P/'core391_tail_safe.py')==sha(R/'core391_tail_safe.py')
assert len(batch)==6 and len(p['grid'])==6 and len(p['native_grid'])==5 and len(p['read_only_references'])==8
for z in batch:
 sp=json.loads((ROOT/z['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs and q['continuous_oos_days']==391 and q['end_utc']=='2026-11-14T00:01:00Z' and q['tail_fold_days']==1 and q['positive_complete30d_folds_required']==10
 if z['scope']=='native':
  assert z['asset']=='ETH' and q['entry_funding_budget_volatility_window_days']==z['W'] and z['W'] in [10,12] and q['entry_funding_volatility_ratio']==.0075 and q['entry_funding_settlement_count']==4 and q['lookback_days']==5 and q['return_hurdle']==q['long_entry_return_hurdle']==q['short_entry_return_hurdle']==.02 and q['exit_buffer_fraction']==.0075 and q['trend_lookback_days']==16 and q['trend_slope_lag_days']==3 and q['trend_slope_hurdle_fraction']==.0075 and q['entry_volatility_window_days']==6 and q['entry_volatility_ceiling']==.05625 and q['entry_direction_mode']=='long_only' and (q['initial_capital_usdt'],q['fixed_entry_notional_usdt'])==(15000,4000)
 else:assert [x['weight'] for x in sp['components']]==[1,1] and [x['fingerprint'] for x in sp['components']]==z['source_fingerprints'] and q['initial_capital_usdt']==18750
 assert sp['logic']['signal']==p['rules']['signal']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items());assert json.loads((R/'parent_primitive_verification.json').read_text())['passed'] and json.loads((R/'budget_window_verification.json').read_text())['passed']
put(R/'signal_scalar_consistency_before_reservation.json',{'passed':True,'recorded_utc':now(),'explicit_signal':p['rules']['signal'],'new_native_asset':'ETH','new_ETH_budget_window':[10,12],'old_ETH_budget_window':9,'fixed_ETH_funding_ratio':.0075,'fixed_ETH_entry_cap':.05625,'fixed_ETH_entry_V':6,'fixed_ETH_trend_K':.0075,'fixed_ETH_L':5,'fixed_ETH_H':.02,'fixed_ETH_E':.0075,'readonly_BTC_H':[.03,.0325],'before_first_reservation':True,'no_market_or_account_calculations':True})
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py','bootstrap.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for z in batch:immutable[z['spec']]=sha(ROOT/z['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'new_native_models':2,'new_parent_models':4,'readonly_existing_native_models':5,'readonly_existing_parent_models':3,'ETH_and_BTC_full_engine_source_bytes_unchanged':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':6,'all_exact_new_fingerprints_absent':True,'only_ETH_budget_window_parameter_changed_engine_money_bytes_exact':True,'raw_weights_not_normalized':True,'readonly_existing_configs':8});print('PASS6newbudgetWindowspecs/8readonly;engine/moneybytesexact;boundbeforefirstreserve')
