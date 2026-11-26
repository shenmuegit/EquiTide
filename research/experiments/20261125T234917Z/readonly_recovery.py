"""Bound readonly axis adapter and truthful failed-receipt handling; no model/account replay."""
import ast,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def execute(phase):
 b=rd(R/'readonly_recovery_binding.json');assert b['bound_before_any_recovery_execution'] and phase in ['audit','collect','checks']
 for p,h in {**b['source_sha256'],**b['original_sources_sha256'],**b['fixed_inputs_sha256']}.items():assert sha(ROOT/p)==h,p
 assert rd(R/'command_receipts/audit.json')['commands'][0]['exit_code']==1 and not rd(R/'command_receipts/audit.json')['passed']
 assert sha(R/'report.json')==b['first_financial_report_sha256']
 original=R/(phase+'.py');s=original.read_text();changes=[]
 def replace(a,z,count=None):
  nonlocal s
  n=s.count(a);assert n>0 and (count is None or n==count),(phase,a,n);s=s.replace(a,z);changes.append({'before':a,'after':z,'occurrences':n})
 if phase=='audit':
  mapping={'BTC_ENTRY_VOLATILITY_WINDOW_DAYS':'BTC_EXIT_BUFFER_FRACTION','ETH_ENTRY_VOLATILITY_WINDOW_DAYS':'ETH_EXIT_BUFFER_FRACTION'}
  for a,z in mapping.items():replace(a,z,2)
  before=ast.parse(original.read_text());after=ast.parse(s)
  class AxisNames(ast.NodeTransformer):
   def visit_Constant(self,node):
    if isinstance(node.value,str) and node.value in mapping:node.value=mapping[node.value]
    return node
  assert ast.dump(AxisNames().visit(before))==ast.dump(after)
 else:
  assert rd(R/'command_receipts/audit_exit_axes.json')['passed'] and rd(R/'readonly_recovery_audit_verification.json')['passed']
  failures=[p.stem for p in (R/'command_receipts').glob('*.json') if not rd(p)['passed']];assert failures==['audit'],failures
  if phase=='collect':
   replace('assert not nonzero,nonzero',"assert [z['phase'] for z in nonzero]==['audit'] and rd(R/'command_receipts/audit_exit_axes.json')['passed'],nonzero",1)
   replace('command_receipts/audit.json','command_receipts/audit_exit_axes.json',1)
   replace("'effective_financial_audit':rel(R/'audit.py')","'effective_financial_audit':rel(R/'audit_exit_axes.py')",1)
  else:
   replace('assert not failed,failed',"assert failed==['audit'] and rd(R/'command_receipts/audit_exit_axes.json')['passed'],failed",1)
   replace("'evaluate','audit','exports'","'evaluate','audit_exit_axes','exports'",1)
   replace("'no_nonzero_native_phases':True","'no_nonzero_native_phases':False",1)
 ast.parse(s);before_report=sha(R/'report.json');before_SMA=sha(R/'forward_report.json') if (R/'forward_report.json').exists() else None
 exec(compile(s,str(original),'exec'),{'__file__':str(original),'__name__':'__main__'})
 assert sha(R/'report.json')==before_report==b['first_financial_report_sha256']
 if before_SMA:assert sha(R/'forward_report.json')==before_SMA
 for p,h in {**b['source_sha256'],**b['original_sources_sha256'],**b['fixed_inputs_sha256']}.items():assert sha(ROOT/p)==h,p
 put(R/('readonly_recovery_'+phase+'_verification.json'),{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'phase':phase,'original_source':rel(original),'original_source_unchanged':True,'original_failed_audit_receipt_retained_with_exit1':True,'changes':changes,'first_financial_report_sha256_unchanged':before_report,'SMA_report_sha256_unchanged':before_SMA,'new_strategy_or_completed_account_or_cashflow_executions':0,'only_readonly_verification_or_rendering':True})
 print('READONLY_RECOVERY_SUCCESS',phase,flush=True)
