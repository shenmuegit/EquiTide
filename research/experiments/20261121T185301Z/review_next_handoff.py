"""Read-only final references: complete original sources, next windows and no prebooking."""
from common import *
from datetime import datetime,timedelta
rd=lambda p:json.loads(p.read_text())
ns=rd(R/'next_research_state.json');h=ns['UTC_midnight_handoff'];p=rd(R/'next_midnight_preparation.json');w=rd(R/'account_windows.json');a=rd(R/'account_window_verification.json');fv=rd(R/'forward_verification.json');binding=rd(R/'code_binding_before_evaluation.json')
assert all(a['current_daily_event_counts'][x]==a['current_fills_by_account'][x]==a['current_funding_records_by_account'][x]==0 for x in ['SMA','candidate','l4h02','fewm'])
for tag,account in [('SMA_single','SMA'),('L4_FEWM','l4h02')]:
 expected=[w[account]['cutoff_utc'],(datetime.fromisoformat(w[account]['cutoff_utc'].replace('Z','+00:00'))+timedelta(hours=2)).isoformat().replace('+00:00','Z')]
 assert h['next_'+tag+'_window_utc']==p['next_original_windows'][account]==expected and not h['next_'+tag+'_expected_daily_events_utc']
assert h['next_L4_FEWM_next_input_source']==rel(R/'next_midnight_preparation.json') and h['next_L4_FEWM_possible_new_funding_window_utc']==p['next_original_windows']['l4h02']
assert h['SMA_original_latest_daily_adapter']=='research/experiments/20261121T165204Z/forward.py' and h['SMA_current_original_daily_adapter'] is None and h['SMA_current_mark_only_adapter']==rel(R/'forward.py') and h['SMA_next_mark_only_adapter_template']==rel(R/'forward.py') and h['SMA_next_mark_only_registry_template']==rel(R/'forward_registry.py')
assert h['SMA_no_new_daily_capture'] and h['SMA_new_daily_decisions']==0 and not h['SMA_next_requires_original_daily_adapter'] and not h['SMA_next_original_daily_registry_rebinding_required'] and fv['full73_daily_background_readonly']
full=rd(R/'SMA_full73_prebinding.json');assert h['SMA_full73_authority']==full['authority']=='research/experiments/20261121T165204Z/forward_inputs.json.gz' and h['SMA_full73_sha256']==full['sha256']==sha(ROOT/full['authority'])
assert all(h['next_daily_decision_by_account'][x]=='2026-11-22T00:01:00Z' and p['expected_next_daily_events_by_account'][x]==[] for x in ['SMA','candidate','l4h02','fewm'])
assert p['current_or_future_account_funding_or_daily_bookings_created']==0 and rd(R/'next_actual_settlement_first_source.json')['new_first_source'] is None
for path,v in p['all_current_books_pointers_registry_state_hashes_unchanged'].items():assert sha(ROOT/path)==v
for path,v in {**binding['source_sha256'],**binding['immutable_source_sha256']}.items():assert sha(ROOT/path)==v,path
q=rd(R/'age60_selected_history_identity.json');cross=rd(R/'age60_incremental_evidence.json');assert q['passed'] and cross['passed'] and q['actual_saved_policy_decisions_compared']==3519 and cross['all18_new_cost_curves_identical_to_completed_age48_curves']
put(R/'next_handoff_reference_review.json',{'passed':True,'recorded_utc':now(),'current_report_sha256_unchanged':sha(R/'report.json'),'current_and_next_windows':p['next_original_windows'],'SMA_current_full73_authority':full,'SMA_current_mark_adapter':rel(R/'forward.py'),'SMA_last_actual_original_daily_adapter':h['SMA_original_latest_daily_adapter'],'next_L4_FEWM_source':h['next_L4_FEWM_next_input_source'],'all_original_sources_and_accounts_unchanged':True,'all_current_and_next_daily_counts_zero':True,'funding_fresh_lookup_and_own_window_dedup_still_required_next_round':True,'financial_and_account_reruns':0})
print('PASSnextwindows/references/originaldailyvsmarkonly/full73/ownbooks/no-prebooking/immutablebindings')
