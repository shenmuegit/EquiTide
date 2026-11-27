"""Verify known first sources/current books and explicitly incomplete future funding metadata."""
import hashlib,json
from datetime import datetime
from pathlib import Path
from blocked_recovery_integrity import verify,ROOT,R,rd,sha
b=rd(R/'blocked_handoff_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256'] and sha(R/'blocked_recovery_integrity.py')==b['integrity_helper_sha256'];_,v,s,h,q=verify();aw=rd(R/'account_window_verification.json');assert aw['passed'] and aw['current_funding_records_by_account']=={'SMA':0,'candidate':0,'l4h02':6,'fewm':6} and aw['actualNov26_16_unique_counts']=={'candidate':0,'l4h02':6,'fewm':6} and len(aw['own_actualNov26_16_cashflows'])==12 and not aw['own_actualNov26_08_cashflows']
sources=[];known_counts={a:0 for a in ['SMA','candidate','l4h02','fewm']};ms=lambda x:int(datetime.fromisoformat(x.replace('Z','+00:00')).timestamp()*1000)
for e in h['next_window_known_actual_funding_sources']:
 doc=rd(ROOT/e['path']);assert sha(ROOT/e['path'])==e['sha256'] and doc['recorded_utc']==e['original_capture_utc'] and doc['public_fields_by_asset']==e['actual_public_fields']
 for a,ts in e['current_own_booked_counts'].items():
  for t,n in ts.items():assert aw['full_chain_once_counts'][a]['funding'].get(t,0)==n
 for a in known_counts:
  win=h['next_SMA_single_window_utc'] if a in ['SMA','candidate'] else h['next_L4_FEWM_window_utc'];n=0 if a=='SMA' else 3*sum(ms(win[0])<int(z['fundingTime'])<=ms(win[1]) for xs in doc['public_fields_by_asset'].values() for z in xs);assert n==e['next_own_coverage_expected_counts'][a];known_counts[a]+=n
 sources.append(e)
assert len(sources)==11 and known_counts==h['known_source_only_coverage_counts']==q['known_source_coverage_counts']=={'SMA':0,'candidate':6,'l4h02':0,'fewm':0}
assert h['L4_FEWM_actualNov26_16_booked_once'] and h['single_actualNov26_16_not_yet_booked'] and not h['all3_perp_actualNov26_16_booked_once']
for p,expected in [('midnight_handoff_verification.json',{'passed':True,'scope':'current_book_integrity_and_blocked_future_query','new_strategy_or_account_or_cashflow_executions':0,'next_complete_actual_query':False,'all_next_reserves_blocked_until_complete_fresh_query':True,'known_source_only_coverage_counts':known_counts}),('next_funding_handoff_verification.json',{'passed':True,'scope':'known_source_integrity_only_future_query_BLOCKED','first_actual_sources':sources,'all3_original_perps_actual16_and08_unique_counts6_each':True,'legacy_count_scope':'Nov23_16 and Nov24_08 only;Nov26_16 currentlycandidate0,L4_6,FEWM_6','newNov26_16_counts':aw['actualNov26_16_unique_counts'],'known_first_source_SHA_original_UTC_and_exact_fields_retained':True,'next_pending_from_fresh_complete_actual_query':None,'next_complete_actual_query':False,'known_source_only_coverage_counts':known_counts,'all_next_reserves_blocked_until_complete_fresh_query':True,'no_early_or_duplicate_bookings':True,'next_window_must_refresh_and_bind_before_reserve':True,'cashflow_or_strategy_or_account_calculations':0,'financial_report_sha256_unchanged':sha(R/'report.json')})]:
 path=R/p;assert not path.exists();path.write_text(json.dumps(expected,ensure_ascii=False,indent=2)+'\n')
print('PASS current-source integrity;next ETH query BLOCKED,known-only counts cannot authorize next reserve')
