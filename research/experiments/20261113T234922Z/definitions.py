"""Bind390day adapter with unchanged policy and native money AST before reservation."""
import ast,json
from common import *
P=ROOT/'research/experiments/20261113T214818Z';p=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());rs=reg.read_records(ROOT/'research/automation/registry.jsonl');funs=lambda f:{x.name:ast.dump(x,include_attributes=False) for x in ast.parse(f.read_text()).body if isinstance(x,ast.FunctionDef)}
assert funs(P/'engine.py')==funs(R/'engine.py');a,b=funs(P/'core389.py'),funs(R/'core390.py');assert all(a[k]==b[k] for k in a if k!='load_market')
assert len(batch)==11 and len(p['grid'])==len(p['native_grid'])==4
for row in batch:
 sp=json.loads((ROOT/row['spec']).read_text());q=sp['parameters'];assert reg.fingerprint(sp)==row['fingerprint'] and row['fingerprint'] not in rs and q['end_utc']=='2026-11-13T00:01:00Z' and q['continuous_oos_days']==390 and q['complete_30day_folds']==13 and q['tail_fold_days']==0 and q['positive_complete30d_folds_required']==10
 if row['scope']=='native':
  assert (q['initial_capital_usdt'],q['fixed_entry_notional_usdt'])==((3750,1000) if row['asset']=='BTC' else (15000,4000))
  if row['role']=='component':
   if row['asset']=='BTC':assert q['lookback_days']==29 and q['return_hurdle']==.03 and q['exit_buffer_fraction']==.01 and q['entry_volatility_window_days']==10 and q['entry_volatility_ceiling'] in [.03,.04]
   else:assert q['entry_direction_mode']=='long_only' and q['entry_funding_volatility_ratio'] in [.00875,.01] and q['entry_funding_budget_volatility_window_days']==8
 else:assert q['initial_capital_usdt']==18750 and [x['weight'] for x in sp['components']]==[1,1] and [x['fingerprint'] for x in sp['components']]==row['source_fingerprints']
for xs in p['data']['assets'].values():
 for z in xs:assert sha(ROOT/z['path'])==z['sha256']
ab=json.loads((R/'original_accounts_binding.json').read_text());assert all(sha(ROOT/x)==h for x,h in ab['sources_sha256'].items()) and json.loads((R/'parent_primitive_verification.json').read_text())['passed']
excluded={'commands.py','publish.py','exports.py','checks.py','collect.py','finalize.py','journal.py'};source={rel(f):sha(f) for f in R.glob('*.py') if f.name not in excluded};immutable={rel(f):sha(f) for f in [R/'account_windows.json',R/'l4h02_resume_plan.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'original_accounts_binding.json',R/'extended_data_manifest.json',ROOT/'checks/monitor_snapshot.py',ROOT/'research/monitor/snapshot.py']}
for row in batch:immutable[row['spec']]=sha(ROOT/row['spec'])
put(R/'code_binding_before_evaluation.json',{'recorded_utc':now(),'source_sha256':source,'immutable_source_sha256':immutable,'no_new_research_calculation_yet':True,'original_accounts_have_separate_preexecution_binding':True,'new_native_models':6,'new_parent_models':5,'changed_policy_scope':'No policy or moneyformula ASTchanges;only declared390daymarket/calendar geometry,13fullmonthgates andBVC/R combo. Old389dayresultsimmutable.','simulate_and_native_money_AST_unchanged':True,'readonly_formatters_excluded':sorted(excluded)})
put(R/'definition_check.json',{'passed':True,'new_financial_configs':11,'all_exact_fingerprints_unavailable_before_reserve':True,'all_policy_AST_and_money_AST_unchanged':True,'calendar_only_market_adapter_changed':True,'two_parent_axes_and_single_appropriate_native_axes':True,'all_old_data_rows_verified_equal':True});print('PASS11new390daydefinitions;fullpolicy/moneyASTunchanged;boundbeforefirstreserve')
