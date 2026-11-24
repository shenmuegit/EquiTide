"""Bind retention before its guarded retry, preserving both actual failed guards."""
import ast,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('/home/desktop/Documents/Codex/EquiTide');R=ROOT/'research/experiments/20261124T093650Z';F=ROOT/'.git/automation_proofs'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rd=lambda p:json.loads(p.read_text())
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
now=lambda:datetime.now(timezone.utc).isoformat()
p=R/'retain_transport_failures.py';assert not(R/'transport_failure_binding.json').exists()
failures=[]
for phase in ['transport_failures','transport_failures_retry']:
 receipt=R/'command_receipts'/(phase+'.json');log=R/'command_receipts'/(phase+'_0.log')
 assert not rd(receipt)['passed'] and 'FileNotFoundError' in log.read_text() and 'transport_failure_binding.json' in log.read_text()
 failures.append({'phase':phase,'receipt':str(receipt.relative_to(ROOT)),'sha256':sha(receipt),'log_sha256':sha(log),'cause':'Missing dedicated binding guard at helper first statement,before any mutation.'})
first=sha(R/'report.json');sma=sha(R/'forward_report.json')
assert first=='2a9a6e8172c5d776002112796a96c57a191d738ae371b9063946bd05825c304a' and sma=='9f66c59bebeb5ed1a03fa09395d64ad6c10c236c2bf6ff2cc681fa6ee456ea97'
put(R/'transport_failure_binding.json',{'recorded_utc':now(),'source':str(p.relative_to(ROOT)),'source_sha256':sha(p),'bound_before_execution':True,'bound_before_successful_retry_execution':True,'initial_guard_attempts_failed_before_any_mutation':True,'original_guard_receipts':failures})
recovery={'recorded_utc':now(),'native_guard_attempt_chunks':['62095a','1a9a1c'],'failed_guards':failures,'cause':'Dedicated transport_failure_binding.json omitted. First attempted preparation then had a SyntaxError from accidental leading plus markers,so its Python body never executed and second guarded attempt also stopped before any mutation.','recovery_phase':'transport_failures_bound_retry','source_sha256':sha(p),'financial_report_sha256_unchanged':first,'SMA_report_sha256_unchanged':sma,'raw_index_before_retry_sha256':sha(R/'raw_evidence_index.json'),'result_before_retry_sha256':sha(R/'result.md'),'financial_or_completed_account_window_replays':0}
put(R/'transport_failure_recovery.json',recovery)
put(R/'retention_recovery_preparation_failure.json',{'recorded_utc':now(),'native_chunk':'1a9a1c','exit_code':1,'error':'SyntaxError: cannot assign to expression here; accidental leading +f= in preparation heredoc line14. Entire preparation body did not execute.','subsequent_actual_guard_failure_receipt':failures[1],'financial_or_account_calculations':0,'recovery_source':str(Path(__file__).relative_to(ROOT)),'recovery_source_sha256':sha(Path(__file__))})
entries=[{**x,'recovery_receipt':str((R/'command_receipts/transport_failures_bound_retry.json').relative_to(ROOT))} for x in failures]
doc=rd(R/'read_failures.json');doc['nonzero_native_phases'].extend(entries);doc['transport_guard_recovery']=recovery;put(R/'read_failures.json',doc)
doc=rd(R/'next_research_state.json');doc['native_command_failures'].extend(entries);doc['transport_retention_guard_recovery']='transport_failure_recovery.json';put(R/'next_research_state.json',doc)
text=(R/'result.md').read_text();text+='\n留档保护检查实际中止两次：专用源码绑定JSON缺失；中间准备命令另有SyntaxError，整段未执行，故第二次仍在同一保护检查中止。两次均在任何结果写入前，首次报告及原始索引哈希保留。后续仅补齐绑定并运行transport_failures_bound_retry留档，所有失败退出码、日志及准备错误留档，不重跑回测或账户。\n';(R/'result.md').write_text(text)
# An additive checker accepts only these documented nonfinancial guards with successful recovery.
p=R/'checks_recovered.py';assert not p.exists();s=(R/'checks.py').read_text()
old="assert set(failed)=={'units'} and rd(R/'command_receipts/units_retry.json')['passed'] and sha(R/'command_receipts/units.json')==rd(R/'source_preparation_recovery.json')['original_failed_phase_sha256'],failed"
new="assert set(failed)=={'units','transport_failures','transport_failures_retry'} and rd(R/'command_receipts/units_retry.json')['passed'] and sha(R/'command_receipts/units.json')==rd(R/'source_preparation_recovery.json')['original_failed_phase_sha256'] and rd(R/'command_receipts/transport_failures_bound_retry.json')['passed'] and all(sha(ROOT/z['receipt'])==z['sha256'] for z in rd(R/'transport_failure_recovery.json')['failed_guards']),failed"
assert old in s;s=s.replace(old,new)
needle="put(R/'data_hashes.json'"
insert="assert sha(Path(__file__))==rd(R/'checks_recovery_binding.json')['source_sha256'];assert rd(R/'saved_result_review.json')['passed'] and rd(R/'confirmation_diagnostic_correction.json')['passed'] and rd(R/'next_funding_handoff_verification.json')['passed'];put(R/'data_hashes.json'"
assert needle in s;s=s.replace(needle,insert);ast.parse(s);p.write_text(s)
put(R/'checks_recovery_binding.json',{'recorded_utc':now(),'source':str(p.relative_to(ROOT)),'source_sha256':sha(p),'original_bound_checker':str((R/'checks.py').relative_to(ROOT)),'original_bound_checker_sha256':sha(R/'checks.py'),'changes':'Explicitly require both preserved missing-binding guard failures and successful bound retention retry;all original source,numeric,protected,registration checks unchanged. Additionally require new readonly handoff,diagnostic and saved-result review.','bound_before_execution':True})
p=F/(R.name+'_seal.py');s=p.read_text()
old="{k for k,v in phases.items() if not v['passed']}=={'units'}"
new="{k for k,v in phases.items() if not v['passed']}=={'units','transport_failures','transport_failures_retry'} and phases['transport_failures_bound_retry']['passed'] and all(sha(ROOT/z['receipt'])==z['sha256'] for z in rd(R/'transport_failure_recovery.json')['failed_guards'])"
assert old in s;s=s.replace(old,new)
needle="feed=rd(ROOT/'research/monitor/latest.json');"
insert="for name in ['saved_review_binding.json','checks_recovery_binding.json']:\n z=rd(R/name);assert z['bound_before_execution'] and sha(ROOT/z['source'])==z['source_sha256']\nassert rd(R/'saved_result_review.json')['passed'] and rd(R/'command_receipts/saved_result_review.json')['passed']\n"
assert needle in s;s=s.replace(needle,insert+needle);ast.parse(s);p.write_text(s)
private=F/(R.name+'.json');d=rd(private)
d['native_registry_and_collect_pipeline']={'initial_chunk_id':'d35c03','completion_chunk_id':'851515','exit_code':0,'archived_events':36,'finished_IDs':18,'archive_bytes':242775}
d['native_raw_retention']={'chunk_id':'bf145d','exit_code':0,'source_entries':18,'distinct_copies':18,'bytes':116828}
d['native_next_funding_handoff_check']={'chunk_id':'62095a','phase':'next_funding_handoff','exit_code':0,'next_candidate_only_funding16':True}
d['native_saved_result_review']={'chunk_id':'62095a','phase':'saved_result_review','exit_code':0}
d['native_transport_guard_failures']=recovery
put(private,d)
assert sha(R/'report.json')==first and sha(R/'forward_report.json')==sma
print('Dedicated binding and additive checker prepared; both real guarded failures preserved; first financial and SMA reports unchanged.')
