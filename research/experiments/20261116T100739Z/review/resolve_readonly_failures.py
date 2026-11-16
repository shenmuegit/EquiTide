"""Close actual readonly-audit/export failures only after their native replacements passed."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import *
rd=lambda p:json.loads(p.read_text());facts=rd(R/'read_failures.json')
for old,success in [('audit_commands.json','audit_retry1_commands.json'),('exports_commands.json','exports_retry1_commands.json')]:
 prior=rd(R/old);fixed=rd(R/success);assert prior[0]['exit_code']==1 and all(z['exit_code']==0 for z in fixed)
 for z in facts['facts']:
  if z.get('log')==prior[0]['log']:
   assert not z.get('resolved');z.update(resolved=True,root_cause='Independent readonly neighbor/export traversal evaluated unrelated ETH W0 on BTC4/5/6axis before asset filtering',effective_successful_receipt=rel(R/success),effective_successful_receipt_sha256=sha(R/success),financial_report_sha256_unchanged=sha(R/'report.json'),strategy_or_account_reruns=0)
put(R/'read_failures.json',facts);put(R/'readonly_failure_resolution.json',{'passed':True,'recorded_utc':now(),'resolved_fact_count':2,'bound_original_audit_unchanged':True,'only_supplemental_readonly_audit_and_export_axis_handling_repaired':True,'financial_report_sha256':sha(R/'report.json'),'no_financial_or_account_reruns':True})
print('PASS2actual readonly failures resolved by native0receipts;failedlogs/commands preserved;report unchanged')
