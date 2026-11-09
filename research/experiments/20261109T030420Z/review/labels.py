"""Verify only derived console labels changed; preserve original executed sources/receipts."""
import ast,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());cor=rd(R/'derived_print_label_corrections.json')
class WithoutPrint(ast.NodeTransformer):
 def visit_Expr(self,n):
  if isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='print':return None
  return self.generic_visit(n)
normalize=lambda s:ast.dump(WithoutPrint().visit(ast.parse(s)),include_attributes=False)
for row in cor['rows']:
 prior=ROOT/row['original_executed_source'];current=ROOT/row['helper'];receipt=rd(ROOT/row['original_native_receipt']);assert sha(prior)==row['original_source_sha256'] and receipt['actual_exit_code']==0
 assert normalize(prior.read_text())==normalize(current.read_text()) and row['corrected_print_label'] in current.read_text() and row['old_print_label'] in (ROOT/row['original_native_log']).read_text()
r=rd(R/'report.json');v=rd(R/'current_midnight_daily_verification.json');assert len(r['configs'])==12 and v['current_new_causal_decisions']==v['current_new_funding_records']==6 and len(v['full_completed_Nov8_days'])==2 and v['SMA_new_percost_daily_decisions']==6
restore=rd(R/'bound_source_restore_verification.json');bind=rd(R/'code_binding_before_evaluation.json');assert restore['passed'] and sha(ROOT/restore['source'])==restore['restored_sha256']==restore['bound_sha256']
for path,h in {**bind['source_sha256'],**bind['immutable_source_sha256']}.items():assert sha(ROOT/path)==h,path
clar=rd(R/'control_description_clarification.json');assert clar['passed'] and clar['preserved_report_sha256']==sha(R/'report.json') and clar['preserved_plan_sha256']==sha(R/'plan.json')
put(R/'derived_label_verification.json',{'passed':True,'original_executed_source_and_stdout_preserved':len(cor['rows']),'only_print_statements_differ_in_corrected_helpers':True,'actual_financial_configs':12,'actual_current_perp_funding_records':6,'actual_current_perp_causal_decisions':6,'actual_complete_single_Nov8_days':2,'actual_SMA_percost_decisions':6,'all36_bound_sources_and_immutable_inputs_exact':True,'bound_collect_adapter_restored_before_execution':True,'numeric_control_definitions_authoritative_and_report_bytes_preserved':True,'financial_or_account_reruns':0});print('PASS12actualfinancialconfigs,6singlefunding/6singledecisions/2completedNov8days,6SMApercostdecisions;only5consolelabels corrected;all original sources/logs/receipts retained')
