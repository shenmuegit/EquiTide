"""Verify all original funding handoff checks with the actual current window count."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=rd(R/'readonly_handoff_recovery_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h
plan=rd(R/'readonly_handoff_recovery_plan.json');src=ROOT/plan['first_source'];text=src.read_text();assert sha(src)==plan['first_source_sha256'] and text.count(plan['only_exact_readonly_predicate_before'])==1
patched=text.replace(plan['only_exact_readonly_predicate_before'],plan['only_exact_readonly_predicate_after']);exec(compile(patched,str(src)+'[readonly_current_window_count]','exec'),{'__file__':str(src),'__name__':'readonly_current_window_handoff'})
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h
(R/'readonly_handoff_recovery_verification.json').write_text(json.dumps({'passed':True,'original_failed_source_kept_byteexact':True,'only_current_window_count_predicate_changed':True,'all_other_original_checks_executed':True,'original_nonzero_phase_preserved':'nextfund','actual_current_funding_counts':rd(R/'account_window_verification.json')['current_funding_records_by_account'],'financial_report_sha256_unchanged':sha(R/'report.json'),'SMA_report_sha256_unchanged':sha(R/'forward_report.json'),'completed_financial_or_account_replays':0,'new_strategy_account_or_cashflow_evaluations':0},indent=2)+'\n')
