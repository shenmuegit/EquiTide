"""Bind every exact sizing/benchmark definition and creator before any reserve."""
import json
from common import *
P=ROOT/'research/experiments/20261119T043148Z';rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');batch=rd(R/'batch.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(sha(P/n)==sha(R/n) for n in ['engine.py','core391_tail_safe.py']);assert len(batch)==10 and len(p['grid'])==6 and len(p['native_grid'])==5 and len(p['read_only_references'])==8
for z in batch:
 sp=rd(ROOT/z['spec']);q=sp['parameters'];assert reg.fingerprint(sp)==z['fingerprint'] and z['fingerprint'] not in rs and q['continuous_oos_days']==391 and q['end_utc']=='2026-11-14T00:01:00Z' and q['positive_complete30d_folds_required']==10
 if z['scope']=='native':
  assert z['asset']=='BTC' and z['N'] in [1250,1500] and q['fixed_entry_notional_usdt']==z['N'] and q['initial_capital_usdt']==3750 and abs(q['raw_entry_notional_fraction_of_initial_capital']-z['N']/3750)<1e-15
  old=rd(ROOT/p['read_only_references'][z['prior_fingerprint']]['spec'])['parameters'];allowed={'fixed_entry_notional_usdt','raw_entry_notional_fraction_of_initial_capital','prior_370day_source_fingerprint'}|({'warmup_days','embargo_days'} if z['role']=='benchmark' else set());assert {k for k in set(q)|set(old) if q.get(k)!=old.get(k)}<=allowed
  if z['role']=='component':assert q['lookback_days']==29 and q['return_hurdle']==.03 and q['exit_buffer_fraction']==.005 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling']==.0275 and q['entry_directional_confirmation_lookback_days']==5 and q['entry_directional_confirmation_hurdle']==.0025
  else:assert q['signal_mode']=='constant_long_reference'
 else:
  assert [c['weight'] for c in sp['components']]==[1,1] and [c['fingerprint'] for c in sp['components']]==z['source_fingerprints'] and q['initial_capital_usdt']==18750 and q['BTC_entry_notional_usdt']==z['NB'] and q['component_initial_entry_notionals_usdt']==[z['NB'],4000] and q['component_capitals_usdt']==[3750,15000]
  src=[rd(ROOT/next(x for x in batch+list(p['read_only_references'].values()) if x['fingerprint']==f)['spec']) for f in z['source_fingerprints']];assert [x['parameters']['fixed_entry_notional_usdt'] for x in src]==[z['NB'],4000]
 assert sp['logic']==p['rules']
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['status']==z['status'] and rs[fp]['report_sha256']==z['report_sha256']
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
ab=rd(R/'original_accounts_binding.json');assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items());assert rd(R/'parent_primitive_verification.json')['passed'] and rd(R/'sizing_primitive_verification.json')['passed']
put(R/'signal_scalar_consistency_before_reservation.json',{'passed':True,'recorded_utc':now(),'explicit_signal':p['rules']['signal'],'new_strategy_asset':'BTC','new_actual_entry_N':[1250,1500],'readonly_entry_N':1000,'fixed_capitals':[3750,15000],'fixed_ETH_entry_N':4000,'readonly_ETH_risk_caps':[.0525,.05625],'matched_benchmark_by_N':p['benchmark_by_W'],'before_first_reservation':True,'no_market_or_account_calculations':True})
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py','bootstrap.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for z in batch:immutable[z['spec']]=sha(ROOT/z['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'new_native_models':4,'new_strategy_models':2,'new_native_holds':2,'new_parent_models':6,'full_accounting_source_bytes_unchanged':True,'complete_engine_source_bytes_unchanged':True,'readonly_formatters_excluded':sorted(excluded)});put(R/'definition_check.json',{'passed':True,'new_financial_configs':10,'all_exact_new_fingerprints_absent':True,'actual_BTC_quantity_and_impact_recomputed_for_N':True,'engine_and_accounting_bytes_exact':True,'raw_weights_not_normalized':True,'matched_native_notional_holds_included':True,'readonly_existing_configs':8});print('PASS10new/8readonly;actualnewBTCstrategyandholdN;allmathbytesexact;boundbeforefirstreserve')
