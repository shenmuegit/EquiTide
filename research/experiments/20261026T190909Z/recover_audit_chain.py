"""Adopt only an actually successful read-only audit; retain failed chain intact."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
old=json.loads((R/'research_commands.json').read_text());new=json.loads((R/'audit_recovery_commands.json').read_text())
assert len(old)==2 and old[0]['exit_code']==0 and old[1]['exit_code']==1
assert len(new)==1 and new[0]['exit_code']==0 and new[0]['command'][-1].endswith('/audit.py')
assert json.loads((R/'verification.json').read_text())['passed'] and json.loads((R/'verification.json').read_text())['report_sha256']==sha(R/'report.json')
assert not(R/'research_effective_commands.json').exists()
put(R/'research_effective_commands.json',[old[0],new[0]])
put(R/'audit_recovery_proof.json',{'passed':True,'original_failed_chain_sha256':sha(R/'research_commands.json'),'actual_recovery_receipt_sha256':sha(R/'audit_recovery_commands.json'),'read_only_audit_passed_report_sha256':sha(R/'report.json'),'financial_evaluate_receipt_reused_unchanged':old[0],'financial_evaluation_not_repeated':True,'original_failure_log_retained':old[1]['log']})
print('Actual successful audit adopted; original failed receipts and financial outputs retained.')
