"""Refresh inherited next-window labels using saved audited facts, without advancing accounts."""
import copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');rel=lambda p:str(p.relative_to(ROOT))
b=rd(R/'handoff_label_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for p,h in b['immutable_financial_inputs_sha256'].items():assert sha(ROOT/p)==h
path=R/'next_research_state.json';before=rd(path);oldhash=sha(path);after=copy.deepcopy(before);h=after['UTC_midnight_handoff'];aw=rd(R/'account_window_verification.json');full=rd(R/'SMA_full77_prebinding.json')
assert aw['passed'] and full['full77_exact_original76_prefix'] and h['SMA_current_full_daily_context']==77 and all(n==6 for n in aw['actualNov25_00_unique_counts'].values()) and all(n==6 for n in aw['actualNov25_00_daily_once_counts'].values())
assert all(n==0 for n in h['next_new_actual_funding_pending_by_own_window'].values()) and not any(h['next_window_original_daily_events'].values())
move=['SMA_next_full71_authority_not_yet_captured','SMA_current_full71_preserved_exact70_prefix','SMA_next_full72_authority_preparation','SMA_next_template_requires_previous_round_and_full72_authority_update','SMA_next_full73_realSPOT_exact72_prefix','SMA_next_template_requires_previous_round_and_full73_authority_update'];legacy={k:h.pop(k) for k in move if k in h}
updates={'SMA_next_full_daily_context_required':77,'SMA_original_latest_daily_adapter':rel(R/'forward.py'),'SMA_next_completed_SPOT_day_utc':'2026-11-25T00:00:00Z','SMA_originalNov25_daily_booked_once':True,'all3_perp_originalNov25_daily_booked_once':True,'SMA_full77_exact76_prefix_verified':True}
prior={k:h.get(k) for k in updates};h.update(updates);after['inherited_historical_handoff_labels_preserved']={'moved_previous_labels':legacy,'updated_previous_values':prior,'scope':'Historical values preserved here; active next-window metadata uses full77 readonly marks, while next dailyNov26 requires full78 throughNov25.'}
after['next_required_effective_SMA_readonly_audit_source']=h['SMA_next_mark_only_audit_template'];after['next_SMA_rebinding_contract']={'current_original_state':rel(R/'forward_state.json'),'current_original_report':rel(R/'forward_report.json'),'next_window_utc':h['next_SMA_single_window_utc'],'mode':'marks_only','full77_authority':full['authority'],'full77_sha256':full['sha256'],'old_full76_prefix_authority':full['full76_authority'],'old_full76_sha256':full['full76_sha256'],'template_sources':{k:h[k] for k in ['SMA_next_mark_only_adapter_template','SMA_next_mark_only_registry_template','SMA_next_mark_only_audit_template']},'all_templates_require_rebinding_before_any_next_reservation':True,'future_Nov26_daily_requires_new_full78_and_original_Float_daily_adapter':True}
# Assert the only changes are explicitly listed metadata labels/pointers.
check=copy.deepcopy(after);check.pop('inherited_historical_handoff_labels_preserved');check.pop('next_SMA_rebinding_contract');check['next_required_effective_SMA_readonly_audit_source']=before['next_required_effective_SMA_readonly_audit_source'];hh=check['UTC_midnight_handoff'];hh.update(legacy)
for k in updates:
 if k in before['UTC_midnight_handoff']:hh[k]=prior[k]
 else:hh.pop(k)
assert check==before
put(path,after);text=(R/'result.md').read_text();beforetext=sha(R/'result.md');text+='\n只读交接标签修订：继承的full71/72/73“next/current”标签及旧75天要求已在本轮交接中保留为历史标签；活跃说明改为下一窗口使用当前原账户、77天背景与76天前缀，重绑旧mark-only模板。未来Nov26日决策需要新78天SPOT及原始Float日决策模板。全部修改仅涉及交接标签和审计模板指针，实际报告、冻结源码、现金、持仓、账本和登记均保持首次结果。\n';(R/'result.md').write_text(text)
for p,h in b['immutable_financial_inputs_sha256'].items():assert sha(ROOT/p)==h
put(R/'handoff_label_verification.json',{'passed':True,'source_sha256':b['source_sha256'],'only_explicit_metadata_labels_changed':True,'all_financial_and_account_evidence_unchanged':True,'next_state_before_sha256':oldhash,'next_state_after_sha256':sha(path),'result_before_sha256':beforetext,'result_after_sha256':sha(R/'result.md'),'historical_labels_preserved':len(legacy)+len(prior),'new_strategy_account_or_cashflow_evaluations':0});print('PASS stale inherited handoff labels preserved with corrected full77/nextfull78 metadata; no model or account executions')
