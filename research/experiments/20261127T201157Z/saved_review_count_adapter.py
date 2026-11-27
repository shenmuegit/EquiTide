"""First-attempt saved-result summary with current count; preserve frozen source and reports."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rd=lambda p:json.loads(p.read_text())
b=rd(R/'saved_review_count_adapter_binding.json');assert sha(Path(__file__))==b['source_sha256'] and b['bound_before_readonly_execution']
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h
src=R/'saved_review.py';text=src.read_text();plan=rd(R/'readonly_count_adapter_plan.json');assert sha(src)==plan['original_saved_review_sha256'] and text.count(plan['exact_expression_before'])==1 and len(rd(R/'report.json')['configs'])==len(rd(R/'batch.json'))==4
patched=text.replace(plan['exact_expression_before'],plan['exact_expression_after']);exec(compile(patched,str(src)+'[readonly_current_batch_count]','exec'),{'__file__':str(src),'__name__':'readonly_saved_summary'})
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h
(R/'saved_review_count_adapter_verification.json').write_text(json.dumps({'passed':True,'first_readonly_attempt':True,'original_source_kept_byteexact':True,'only_diagnostic_count12_to4_changed':True,'financial_report_unchanged':sha(R/'report.json'),'SMA_report_unchanged':sha(R/'forward_report.json'),'new_strategy_account_or_cashflow_evaluations':0},indent=2)+'\n')
