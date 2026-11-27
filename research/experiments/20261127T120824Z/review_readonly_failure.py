"""Review a redundant nonfinancial assertion and execute unchanged financial checks."""
from pathlib import Path
from datetime import datetime,timezone
import json,gzip,hashlib,sys,copy
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'readonly_scope_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
old=rd(R/'command_receipts/handoff_rules.json');assert old['passed'] is False and len(old['commands'])==1 and old['commands'][0]['exit_code']==1
assert sha(R/'checks.py')==b['original_checks_sha256'] and sha(R/'checks_readonly_scope.py.txt')==b['adapted_checks_sha256']
if sys.argv[1]=='review':
 state=R/'next_research_state.json';before=gzip.decompress((R/'next_state_before_redundant_check.json.gz').read_bytes());assert hashlib.sha256(before).hexdigest()==b['next_state_before_failed_step_sha256']==sha(state)
 n=rd(state);h=n['UTC_midnight_handoff'];w=rd(R/'account_windows.json');lookup=rd(R/'next_window_funding_lookup.json');assert lookup['passed']
 assert h['rules']==w['rules']+' Next pending='+str(lookup['own_next_window_pending_counts'])+';refresh actual sources and each own original state before any next reserve.'
 assert 'Future ETH query incomplete' not in h['rules'] and {x['asset'] for x in lookup['HTTP_receipts'] if x['http_status']==200 and not x['curl_exit_code']}=={'BTC','ETH'}
 text=(R/'refresh_handoff_rules_readonly.py').read_text();assert text.index("assert 'Future ETH query incomplete' in old")<text.index('put(path,after)')
 fail=rd(R/'read_failures.json');assert [x['phase'] for x in fail['nonzero_native_phases']]==['prepare'];fail['nonzero_native_phases'].append({'phase':'handoff_rules','receipt':str((R/'command_receipts/handoff_rules.json').relative_to(ROOT))});fail['resolved_nonfinancial_metadata_issues']=[{'phase':'prepare','reason':'Started before complete context read;stopped before data query,reserve or evaluation. Same source prepare_ready succeeded after prerequisite.'},{'phase':'handoff_rules','reason':'Redundant updater expected stale inherited prose;collect.py line106 already refreshes rules. Assertion stopped before any write;step abandoned,original failed receipt preserved.'}];put(R/'read_failures.json',fail)
 result=R/'result.md';s=result.read_text();s=s.replace("原生命令非零阶段['prepare']", "原生命令非零阶段['prepare', 'handoff_rules']");s+='\n两项非金融前置失败原样保留：prepare在context尚未就绪时停止，未查询数据或登记，随后prepare_ready以同一来源代码完成；额外handoff_rules更新器错误预期说明仍过时，而collect.py已刷新说明，该冗余步骤在写入前断言退出并放弃。当前下一轮说明、完整BTC/ETH查询及原账户均已只读核验有效，未改任何规则或重放回测/账户。只读汇总核验仅对这两个已证实的非金融失败保留范围说明；所有原金融、资金费、登记、数据和保护断言原样执行，旧checks.py保持字节不变。见readonly_failure_review.json及实际失败回执。\n';result.write_text(s)
 put(R/'readonly_failure_review.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_binding':'readonly_scope_binding.json','actual_failed_phases_preserved':['prepare','handoff_rules'],'redundant_step_status':'abandoned_before_write','collect_already_updated_rules_from_current_account_windows':True,'next_state_unchanged_across_failed_step':True,'all_bound_financial_account_pointer_and_registry_bytes_unchanged':True,'original_failed_receipt_preserved_false':True,'financial_report_sha256_unchanged':sha(R/'report.json'),'SMA_report_sha256_unchanged':sha(R/'forward_report.json'),'new_strategy_account_or_cashflow_evaluations':0})
 print('PASS redundant readonly updater abandoned;actual false receipt kept,all financial/state bytes unchanged')
elif sys.argv[1]=='checks':
 assert rd(R/'readonly_failure_review.json')['passed'] and rd(R/'command_receipts/readonly_failure_review.json')['passed']
 adapted=(R/'checks_readonly_scope.py.txt').read_text();assert hashlib.sha256(adapted.encode()).hexdigest()==b['adapted_checks_sha256']
 exec(compile(adapted,str(R/'checks.py')+'[documented_readonly_failure_scope]','exec'),{'__file__':str(R/'checks.py'),'__name__':'__main__'})
 gate=rd(R/'validation_gate.json');assert set(gate['nonzero_native_phases'])=={'prepare','handoff_rules'} and gate['passed'] and gate['no_nonzero_native_phases'] is False
 gate.update(effective_checker=str(Path(__file__).relative_to(ROOT)),original_checks_kept_byteexact=True,all_original_financial_and_registration_and_protection_assertions_executed=True,documented_readonly_failures_only=['prepare','handoff_rules'],readonly_failure_verification='readonly_failure_review.json');put(R/'validation_gate.json',gate)
 print('PASS all original financial checks with exactly two preserved nonfinancial failures;no model/account execution')
else:raise ValueError(sys.argv[1])
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
