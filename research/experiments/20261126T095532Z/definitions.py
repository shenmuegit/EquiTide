"""Bind every complete new graph, actual read-only source and original account before reserve."""
import ast,json
from common import *
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');batch=rd(R/'batch.json');rs=reg.read_records(ROOT/'research/automation/registry.jsonl');P=ROOT/'research/experiments/20261126T075330Z'
assert len(batch)==4 and len(p['read_only_references'])==14 and len(p['grid'])==9 and not p['native_grid'] and p['representative_preset']=={'W':9,'K':.00625}
for name in ['engine.py','core391_tail_safe.py','market.py','portfolio.py','audit_native.py','observe_l4h02.py','observe_fewm.py','audit_incremental.py']:assert sha(R/name)==sha(P/name)
for row in batch:
 sp=rd(ROOT/row['spec']);q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and q['component_capitals_usdt']==[3750,15000] and q['component_initial_entry_notionals_usdt']==[1000,4000] and q['initial_capital_usdt']==18750 and [x['weight'] for x in sp['components']]==[1,1] and q['continuous_oos_days']==391
 assert q['BTC_return_hurdle']==.03 and q['BTC_entry_volatility_ceiling']==.0275 and q['BTC_entry_volatility_window_days']==row['W'] in [9,10,11] and q['BTC_exit_buffer_fraction']==.005 and q['BTC_entry_directional_confirmation_hurdle']==.0025 and q['ETH_entry_volatility_ceiling']==.05625 and q['ETH_trend_slope_lag_days']==3 and q['ETH_entry_funding_budget_volatility_window_days']==9 and q['ETH_entry_volatility_window_days']==6 and q['ETH_exit_buffer_fraction']==.0075 and q['ETH_trend_slope_hurdle_fraction']==row['K'] in [.00625,.00875] and q['ETH_entry_funding_max_age_hours']==36 and q['ETH_entry_funding_settlement_count']==4 and q['ETH_entry_funding_volatility_ratio']==.0075
 for asset,fp in zip(['BTC','ETH'],row['source_fingerprints']):
  child=rs[fp]['spec']['parameters'];assert rs[fp]['result_available']
  for k,v in q.items():
   if k.startswith(asset+'_') and k[len(asset)+1:] in child:assert v==child[k[len(asset)+1:]],k
for fp,z in p['read_only_references'].items():
 assert rs[fp]['result_available'] and rs[fp]['report_sha256']==z['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/z[k])==z[k+'_sha256']
a=rd(R/'original_accounts_binding.json');assert all(sha(ROOT/z)==h for z,h in a['sources_sha256'].items());assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='simulate' for n in ast.walk(ast.parse((R/'run.py').read_text())))
for name in ['next_funding_checker_binding.json','transport_failure_binding.json']:
 z=rd(R/name);assert z['bound_before_execution'] and sha(ROOT/z['source'])==z['source_sha256']
names=['pre_reserve_source_adaptation.json','startup.json','context.json','plan.json','spec.json','batch.json','account_windows.json','original_accounts_binding.json','SMA_full77_prebinding.json','SMA_markonly_kernel_identity.json','l4h02_resume_plan.json','research_design.json','primary_source_access.json','window_funding_preflight.json','registry_archive_plan.json','joint_parameter_metadata_availability.json','actual08_nov23_prebinding_source.json','actual16_nov23_prebinding_source.json','actual00_nov24_prebinding_source.json','actual08_nov24_prebinding_source.json','actual16_nov24_prebinding_source.json','actual00_nov25_prebinding_source.json','actual08_nov25_prebinding_source.json','actual16_nov25_prebinding_source.json','all_actual_funding_prebinding.json','parent_primitive_verification.json','sizing_primitive_verification.json','boundary_unit_verification.json','readonly_formatter_binding.json','next_funding_checker_binding.json','transport_failure_binding.json']
imm={rel(R/name):sha(R/name) for name in names};imm.update({x['spec']:sha(ROOT/x['spec']) for x in batch});imm.update(a['sources_sha256']);source={rel(f):sha(f) for f in R.glob('*.py')}
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':imm,'new_native_models':0,'new_parent_models':4,'no_new_financial_calculation_yet':True,'raw_weights_not_normalized':True,'actual08_and_actual16_first_sources_rebound_before_any_reserve':True})
put(R/'definition_check.json',{'passed':True,'new_configs':4,'read_only_refs':14,'new_native_models':0,'source_metadata_checked':True,'full_graph_index_verified_before_reserve':True,'all_source_reports_archives_spec_and_account_hashes_bound':True});print('PASS4newgraphs/14actualrefs/0newnative/fullsourceandall-eight-own16binding')
