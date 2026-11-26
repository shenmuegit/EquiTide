"""Save the next original SMA adapter contract from completed evidence; no account execution."""
import copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');rel=lambda p:str(p.relative_to(ROOT))
b=rd(R/'handoff_contract_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h
path=R/'next_research_state.json';before=rd(path);oldhash=sha(path);after=copy.deepcopy(before);h=after['UTC_midnight_handoff'];bg=rd(R/'SMA_full77_prebinding.json');aw=rd(R/'account_window_verification.json');assert aw['passed'] and bg['full77_exact_original76_prefix']
assert all(z['new_daily_events']==z['new_funding_settlements']==z['new_fills']==0 for z in aw['accounts'].values()) and all(n==6 for n in aw['actualNov25_00_unique_counts'].values()) and all(n==6 for n in aw['actualNov25_00_daily_once_counts'].values())
assert not h['next_window_original_daily_events']['SMA'] and h['next_new_actual_funding_pending_by_own_window']['SMA']==0
assert 'next_SMA_rebinding_contract' not in before
contract={'current_original_state':rel(R/'forward_state.json'),'current_original_report':rel(R/'forward_report.json'),'next_window_utc':h['next_SMA_single_window_utc'],'mode':'marks_only','full77_authority':bg['authority'],'full77_sha256':bg['sha256'],'old_full76_prefix_authority':bg['full76_authority'],'old_full76_sha256':bg['full76_sha256'],'template_sources':{k:h[k] for k in ['SMA_next_mark_only_adapter_template','SMA_next_mark_only_registry_template','SMA_next_mark_only_audit_template']},'all_templates_require_rebinding_before_any_next_reservation':True,'future_Nov26_daily_requires_new_full78_and_original_Float_daily_adapter':True}
after['next_SMA_rebinding_contract']=contract;check=copy.deepcopy(after);check.pop('next_SMA_rebinding_contract');assert check==before;put(path,after)
for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h
put(R/'handoff_contract_verification.json',{'passed':True,'source_sha256':b['source_sha256'],'only_next_adapter_contract_added':True,'all_financial_account_and_old_next_state_fields_unchanged':True,'next_state_before_sha256':oldhash,'next_state_after_sha256':sha(path),'new_strategy_account_or_cashflow_evaluations':0});print('PASS next original mark-only adapter contract/full77+76prefix saved; no account or strategy evaluation')
