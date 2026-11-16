"""Preserve the zero-curve failure, finish blocked IDs, widen only the declared guard."""
import ast,copy,importlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R))
from common import *
import engine
batch=json.loads((R/'batch.json').read_text());failure=json.loads((R/'evaluate_commands.json').read_text())
assert failure[0]['exit_code']==1 and 'exit_buffer_fraction' in failure[0]['stderr']
assert not (R/'report.json').exists() and (R/'results').is_dir() and not list((R/'results').iterdir())
assert all(reg.read_records(ROOT/'research/automation/registry.jsonl')[z['fingerprint']]['status']=='reserved' for z in batch)
oldguard="p['exit_buffer_fraction'] in [.005,.01,.015]"
newguard="p['exit_buffer_fraction'] in [0.,.0025,.005,.01,.015]"
old=(R/'engine.py').read_text();assert old.count(oldguard)==1
spec=json.loads((ROOT/batch[0]['spec']).read_text());m={'asset':'BTC','closes':[100]*60}
try:engine.base_decide(spec,m,40,0)
except AssertionError:reproduced=True
else:raise AssertionError('Expected exact entry guard failure was not reproduced')
for src,dest in [('engine.py','review/engine_before_allowlist_fix.py'),('definitions.py','review/definitions_before_allowlist_fix.py'),('code_binding_before_evaluation.json','code_binding_before_failed_allowlist_evaluation.json'),('signal_scalar_consistency_before_reservation.json','signal_scalar_consistency_before_failed_allowlist_evaluation.json'),('prebinding_parameter_guard_verification.json','prebinding_parameter_guard_before_failed_allowlist_evaluation.json')]:
 assert not (R/dest).exists();(R/dest).write_bytes((R/src).read_bytes())
blocked={'round':R.name,'recorded_utc':now(),'status':'blocked','result_available':False,'failure_reason':'Copied BTC parameter-validation allowlist omitted the predeclared narrower E0/E.0025 values; assertion at first decision before any curve was completed.','actual_evaluation_exit_code':1,'actual_evaluation_receipt':rel(R/'evaluate_commands.json'),'actual_evaluation_receipt_sha256':sha(R/'evaluate_commands.json'),'first_native_spec':batch[0]['spec'],'first_native_fingerprint':batch[0]['fingerprint'],'completed_financial_curves':0,'completed_configs':0,'saved_results_directory_empty':True,'exact_before_source':rel(R/'review/engine_before_allowlist_fix.py'),'exact_before_source_sha256':sha(R/'review/engine_before_allowlist_fix.py'),'configs':{z['name']:{**z,'status':'blocked','result_available':False,'reason':'No actual completed backtest; implementation allowlist guard blocked the batch.'} for z in batch}}
put(R/'implementation_blocked_report.json',blocked)
done=[]
for z in batch:
 a=now();receipt=call('finish',z,'blocked',rel(R/'implementation_blocked_report.json'));receipt.update(started_utc=a,finished_utc=now());done.append(receipt);put(R/'implementation_blocked_finish_receipts.json',done)
assert all(not reg.read_records(ROOT/'research/automation/registry.jsonl')[z['fingerprint']]['result_available'] for z in batch)
new=old.replace(oldguard,newguard)
assert ast.dump(ast.parse(new.replace(newguard,oldguard)),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)
(R/'engine.py').write_text(new);importlib.reload(engine)
checks=[]
for E in [0.,.0025,.005,.01,.015]:
 sp=copy.deepcopy(spec);sp['parameters']['exit_buffer_fraction']=E
 for actual in [-1,0,1]:
  got=engine.base_decide(sp,m,40,actual);want=engine.btc.target(m['closes'],40,29,.03,actual,E)[0]
  assert got[0]==want
  changed={'asset':'BTC','closes':m['closes'][:40]+[10**12,1]}
  assert engine.base_decide(sp,changed,40,actual)==got
  checks.append({'E':E,'actual':actual,'first_decision_entry_guard_passed':True,'future_suffix_excluded':True})
assert sha(R/'core391_tail_safe.py')==sha(ROOT/'research/experiments/20261115T220354Z/core391_tail_safe.py')
def edit(name,pairs):
 p=R/name;s=p.read_text()
 for a,b in pairs:assert a in s,(name,a);s=s.replace(a,b)
 ast.parse(s);p.write_text(s)
edit('run.py',[("pending=[z for z in batch if z['fingerprint'] not in rs]","pending=[z for z in batch if z['fingerprint'] not in rs or rs[z['fingerprint']]['status'] in ['blocked','abandoned'] and not rs[z['fingerprint']]['result_available']]")])
edit('definitions.py',[
 ("f.read_text().replace('V in [6,8,10,12,14]'","f.read_text().replace(\"p['exit_buffer_fraction'] in [.005,.01,.015]\",\"p['exit_buffer_fraction'] in [0.,.0025,.005,.01,.015]\").replace('V in [6,8,10,12,14]'"),
 ("'before_first_reservation':True","'before_first_reservation':False,'before_restored_reservation':True,'prior_failed_noresult_attempt_preserved':True"),
 ("'no_new_research_calculation_yet':True","'no_completed_research_calculation_yet':True,'prior_zero_curve_guard_failure_retained':True"),
 ("'policy_and_accounting_source_equal_to_prior':True","'policy_and_accounting_AST_equal_after_guard_normalization':True")])
edit('checks.py',[
 ('len(res)==len(fin)==6','len(res)==12 and len(fin)==6'),
 ("len(reserves)==1 and max","len(reserves)==2 and max"),
 ("ctx['registry_events']+36","ctx['registry_events']+48"),
 ("'append_only_events':36","'append_only_events':48"),
 ('PASS18finishedIDs/36exactappend','PASS18finishedIDs/48exactappend')])
edit('journal.py',[
 ('len(events)==2*len(batch)','len(events)==2*len(batch)+12'),
 ("assert len(es)==2 and es[0]['status']=='reserved' and es[1]['result_available'] and es[1]['status'] in ['passed','rejected']","assert len(es)==(4 if row['fingerprint'] in {z['fingerprint'] for z in json.loads((R/'batch.json').read_text())} else 2) and es[0]['status']=='reserved' and es[-1]['result_available'] and es[-1]['status'] in ['passed','rejected'];assert len(es)==2 or es[1]['status']=='blocked' and not es[1]['result_available'] and es[2]['status']=='reserved'")])
edit('collect.py',[
 ("'registry_append_events':36","'registry_append_events':48"),
 ('策略引擎与资金核算源码和上轮原字节一致。','资金核算核心与上轮原字节一致；策略引擎仅扩展预声明E值的参数白名单，归一化该白名单后完整AST相同。'),
 ('金融完整评估一次，未重跑已完成配置；','首轮入口白名单失败形成0曲线，6项先finish blocked，扩白名单并重新绑定/reserve后完成一次实际评估；失败源/回执、全部状态变迁保留，未重跑已完成配置；')])
edit('finalize.py',[
 ("'bind', 'reserve_0', 'evaluate'","'bind', 'bind_retry1', 'reserve_0', 'reserve_1', 'evaluate_retry1'"),
 ("'staged_whitespace.py', 'validate_sources.py'","'staged_whitespace.py', 'validate_sources.py', 'update_collection.py', 'recover_allowlist.py'"),
 ("ctx['registry_events']+36","ctx['registry_events']+48"),
 ("'append_only_events':36","'append_only_events':48"),
 ("'registry_events':36","'registry_events':48"),
 ("guard['before_first_reservation_or_market_calculation']","guard['before_restored_reservation_and_first_completed_curve']"),
 ("'policy_and_money_source_bytes_exactly_unchanged':True","'policy_and_money_source_bytes_exactly_unchanged':False,'money_core_bytes_unchanged':True,'engine_AST_equal_after_allowlist_normalization':True"),
 ("'zero_market_or_account_evaluations_before_binding':True","'zero_completed_market_or_account_curves_before_restored_binding':True,'initial_failed_zero_curve_attempt_preserved':True"),
 ("'checked_before_first_reserve':True","'checked_before_first_reserve':False,'checked_before_restored_reserve':True"),
 ("'financial_evaluation_runs':1","'financial_evaluation_runs':2"),
 ("'interrupted_evaluation_attempts':0","'interrupted_evaluation_attempts':1"),
 ("interrupted_evaluation_attempts=0","interrupted_evaluation_attempts=1")])
guard=json.loads((R/'prebinding_parameter_guard_before_failed_allowlist_evaluation.json').read_text())
guard.update(recorded_utc=now(),new_sha256=sha(R/'engine.py'),exact_only_source_changes=[{'old':oldguard,'new':newguard,'scope':'assertion parameter allowlist only;formula,accounting and frozen specs unchanged'}],policy_and_money_source_bytes_exactly_unchanged=False,money_core_bytes_unchanged=True,engine_AST_equal_after_allowlist_normalization=True,before_first_reservation_or_market_calculation=False,before_restored_reservation_and_first_completed_curve=True,current_evaluation_failures=1,current_preparation_failures=0,first_decision_synthetic_reproducer_before_fix_failed=True,first_decision_synthetic_checks_after_fix=checks,completed_financial_curves_before_recovery=0)
put(R/'prebinding_parameter_guard_verification.json',guard)
put(R/'allowlist_recovery_verification.json',{'passed':True,'recorded_utc':now(),'actual_original_evaluation_exit_code':1,'completed_initial_curves':0,'blocked_IDs':6,'all_blocked_finish_receipts':done,'original_sources_and_binding_preserved':True,'only_engine_guard_AST_changed':True,'money_core_bytes_unchanged':True,'first_decision_checks':checks,'all_original_plan_specs_axes_preset_and_gates_unchanged':True,'requires_fresh_binding_and_successful_reserve_before_actual_retry':True,'failed_completed_config_reruns':0})
facts=json.loads((R/'read_failures.json').read_text());facts['facts'].append({'type':'initial_BTC_exit_allowlist_guard_failure','native_start_chunk':'e01bce','native_completion_chunk':'579a92','native_session':62900,'actual_exit_code':1,'receipt':rel(R/'evaluate_commands.json'),'blocked_report':rel(R/'implementation_blocked_report.json'),'completed_curves':0,'resolved':True,'recovery':'Exact first-decision synthetic failure reproduced;only assertion allowlist extended for preregistered E0/.0025. Six IDs finished blocked then must rebind/reserve. Original source,binding,failed receipt and no-result states retained;no completed result rerun.'});put(R/'read_failures.json',facts)
(R/'results').rmdir()
print('PASS guard-only recovery;6 blocked finishes preserved;15 direct entry guards pass;0 completed initial curves. Rebind then reserve before actual retry.')
