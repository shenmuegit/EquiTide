"""Link retained native failures to already executed recoveries, without changing outcomes."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R))
from common import *
rd=lambda p:json.loads(p.read_text())
f=R/'read_failures.json';before=rd(f);backup=R/'read_failures_before_recovery_reference_links.json';assert not backup.exists();backup.write_bytes(f.read_bytes())
assert not all(z.get('resolved') for z in before['facts'])
report_sha=sha(R/'report.json');guard_paths=[R/'report.json',R/'plan.json',R/'spec.json',R/'batch.json',R/'code_binding_before_evaluation.json',R/'forward_report.json',R/'forward_state.json',*[R/(s+'_observation/state.json') for s in ['candidate','l4h02','fewm']],*list((R/'results').glob('*.gz'))];protected={rel(p):sha(p) for p in guard_paths}
records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl')
for row in rd(R/'batch.json'):
 rec=records[row['fingerprint']];assert rec['result_available'] and rec['report_sha256']==report_sha and rec['status']=='passed'
 seq=[z for z in events if z['fingerprint']==row['fingerprint']]
 assert [z['status'] for z in seq]==['reserved','blocked','reserved','passed'] and not seq[1]['result_available']
for name in ['evaluate_retry1_commands.json','bind_retry2_commands.json','audit_commands.json','finish_0_commands.json']:
 assert all(z['exit_code']==0 for z in rd(R/name))
assert rd(R/'allowlist_recovery_verification.json')['passed'] and rd(R/'rebind_condition_verification.json')['passed']
resolutions={
 'evaluate.log':['allowlist_recovery_verification.json','evaluate_retry1_commands.json','audit_commands.json','finish_0_commands.json'],
 'bind_retry1_bind.log':['rebind_condition_verification.json','bind_retry2_commands.json'],
 'final_checks.log':['allowlist_recovery_verification.json','rebind_condition_verification.json','source_verification.json','feed_verification.json']}
updated=0
for row in before['facts']:
 if row.get('resolved'):continue
 name=Path(row['log']).name;assert name in resolutions and row['exit_code']==1
 row.update(resolved=True,recovery_recorded_utc=now(),recovery_evidence=[{'path':rel(R/n),'sha256':sha(R/n)} for n in resolutions[name]],recovery='Actual original failure fields and log retained. Successful recovery receipts and unchanged financial/account evidence linked;final check failed only because original failure markers lacked these links. Fresh final check will run after this metadata update.')
 updated+=1
assert updated==3 and all(z.get('resolved') for z in before['facts'])
put(f,before)
original=rd(backup)
for a,b in zip(original['facts'],rd(f)['facts']):
 for k,v in a.items():
  if k!='resolved':assert b[k]==v,(k,v)
assert all(sha(ROOT/path)==h for path,h in protected.items())
p=R/'finalize.py';s=p.read_text();assert "'collect', 'final_checks'" in s;s=s.replace("'collect', 'final_checks'","'collect', 'collect_retry1', 'final_checks_retry1'");assert "'repair_rebind_condition.py'" in s;s=s.replace("'repair_rebind_condition.py'","'repair_rebind_condition.py', 'link_recovery_receipts.py', 'validate_sources_final.py'");ast.parse(s);p.write_text(s)
put(R/'recovery_reference_links_verification.json',{'passed':True,'recorded_utc':now(),'original_failure_snapshot':rel(backup),'original_failure_snapshot_sha256':sha(backup),'native_failed_receipts_linked':updated,'original_native_exit_commands_stderr_logs_unchanged':True,'all_original_failure_fields_preserved_except_resolved_marker':True,'financial_and_account_evidence_unchanged':protected,'current_model_or_account_reruns':0,'requires_fresh_final_check':True})
print('PASS3 original native failures linked to actual recoveries;all native failure fields retained;financial/account SHA unchanged')
