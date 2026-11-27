"""Integrity gate for completed results while the next ETH query remains explicitly blocked."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
FAILED={'collect','funding_retry','funding_extended_retry'}
def verify():
 b=rd(R/'blocked_collection_binding.json');v=rd(R/'blocked_collection_verification.json');assert v['passed'] and not v['next_query_complete'] and v['all_next_reserves_blocked_until_complete_fresh_funding_query'] and v['financial_or_account_window_replays']==0
 assert sha(ROOT/b['source'])==b['source_sha256'] and sha(R/'collect.py')==b['original_collector_sha256'] and sha(R/'collect_blocked_adapted.py.txt')==b['adapted_sha256']
 for p,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/p)==h,p
 actual={p.stem for p in (R/'command_receipts').glob('*.json') if not rd(p)['passed']};assert actual==FAILED,actual
 for x in FAILED:assert sha(R/'command_receipts'/(x+'.json'))==v['original_failed_phase_receipt_sha256'][x]
 assert rd(R/'command_receipts/collect_blocked_resume.json')['passed']
 assert sha(R/'report.json')==v['financial_report_sha256_unchanged']==rd(R/'verification.json')['report_sha256'] and sha(R/'forward_report.json')==v['SMA_report_sha256_unchanged']==rd(R/'forward_verification.json')['report_sha256']
 s=rd(R/'next_research_state.json');h=s['UTC_midnight_handoff'];q=rd(R/'next_window_funding_lookup.json');unknown={'SMA':0,'candidate':None,'l4h02':None,'fewm':None}
 assert not q['passed'] and not q['complete_actual_query'] and not q['ETH_complete_HTTP200'] and q['next_reserve_blocked_until_complete_fresh_query']
 assert s['next_funding_query_status']=='blocked_ETH_TLS_transport' and s['next_reserve_requires_complete_actual_funding_query'] and h['next_new_actual_funding_pending_by_own_window']==unknown and q['own_next_window_pending_counts']==unknown
 assert q['ETH_rows_origin']=='known_original_first_settlement_documents_only_not_a_new_successful_HTTP_response'
 return b,v,s,h,q
