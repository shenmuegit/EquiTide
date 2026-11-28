"""Verify every retained exact source and own-chain boundary, without a cashflow execution."""
import gzip,json
from datetime import datetime
from common import *
rd=lambda p:json.loads(p.read_text());b=rd(R/'next_funding_checker_binding.json');assert sha(Path(__file__))==b['source_sha256'];h=rd(R/'next_research_state.json')['UTC_midnight_handoff'];aw=rd(R/'account_window_verification.json');lookup=rd(R/'next_window_funding_lookup.json');first=rd(R/'verification.json')['report_sha256'];assert aw['passed'] and sha(R/'report.json')==first
sources=[];pre=rd(R/'all_actual_funding_prebinding.json');assert pre['source_count']==15
for e in h['next_window_known_actual_funding_sources']:
 doc=rd(ROOT/e['path']);assert sha(ROOT/e['path'])==e['sha256'] and doc['recorded_utc']==e['original_capture_utc'] and doc['public_fields_by_asset']==e['actual_public_fields']
 for item in doc['HTTP_receipts']:
  assert sha(ROOT/item['raw'])==item['sha256']
  if item['http_status']==200 and not item['curl_exit_code']:
   rows=json.loads(gzip.decompress((ROOT/item['raw']).read_bytes()))
   for asset,fields in doc['public_fields_by_asset'].items():
    if 'symbol='+asset+'USDT' in item['url']:assert all(z in rows for z in fields)
 times={str(int(z['fundingTime'])*1000000) for xs in doc['public_fields_by_asset'].values() for z in xs}
 for a in ['candidate','l4h02','fewm']:assert all(e['current_own_booked_counts'][a][t]==aw['full_chain_once_counts'][a]['funding'].get(t,0) for t in times)
 sources.append({'path':e['path'],'sha256':e['sha256'],'first_capture_utc':e['original_capture_utc'],'actual_public_fields':e['actual_public_fields'],'current_own_counts':e['current_own_booked_counts'],'next_pending_by_own_window':e['next_own_coverage_expected_counts']})
for z in pre['sources']:
 q=rd(ROOT/z['path']);assert sha(ROOT/z['path'])==z['sha256']
 for a,counts in q['prior_unique_counts'].items():
  for t,n in counts.items():assert aw['full_chain_once_counts'][a]['funding'].get(t,0)==n+q['expected_current_increment_counts'][a][t]
assert aw['current_funding_records_by_account']=={a:rd(R/'account_windows.json')[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']}
assert aw['actualNov28_00_unique_counts']==aw['actualNov28_00_daily_once_counts']=={'candidate':0,'l4h02':6,'fewm':6} and len(aw['own_actualNov28_00_cashflows'])==12 and aw['own_actualNov27_16_cashflows']==[]
s15=rd(R/'actual00_nov28_prebinding_source.json');assert s15['sha256']=='58d0e5f4bd388031e31fe25c23aff636d71cb1acb75ed4568a8dc585b82e3e88' and s15['first_capture_utc']=='2026-11-28T16:45:24.928869Z';assert all(int(z['fundingTime'])==1795824000000 for xs in s15['actual_public_fields'].values() for z in xs)
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000);pending={}
for a in ['SMA','candidate','l4h02','fewm']:
 ww=h['next_SMA_single_window_utc'] if a in ['SMA','candidate'] else h['next_L4_FEWM_window_utc'];pending[a]=0 if a=='SMA' else 3*sum(ms(ww[0])<int(z['fundingTime'])<=ms(ww[1]) for xs in lookup['public_fields_by_asset'].values() for z in xs)
 expected='original_daily_decision_and_actual_funding_if_covered' if h['next_window_original_daily_events'][a] else 'original_actual_funding_settlement_and_closed_marks_no_daily_decision' if pending[a] else 'closed_minute_marks_only_no_daily_decision';assert h['next_required_resume_mode_by_account'][a]==expected
assert pending==h['next_new_actual_funding_pending_by_own_window']==lookup['own_next_window_pending_counts']=={'SMA':0,'candidate':6,'l4h02':0,'fewm':0}
assert 'Before ANY next reserve' in h['next_actual_funding_prebinding_contract']
assert h['next_daily_decision_by_account']=={'candidate':'2026-11-28T00:01:00Z','SMA':'2026-11-28T00:01:00Z','l4h02':'2026-11-29T00:01:00Z','fewm':'2026-11-29T00:01:00Z'}
hp=rd(R/'midnight_handoff_plan.json');assert hp['planned_before_any_reserve_or_outcomes'] and h['next_SMA_single_window_utc']==hp['next_SMA_candidate_window'] and h['next_L4_FEWM_window_utc']==hp['next_L4_FEWM_window'];assert all(h['next_window_original_daily_events'][a]==hp['next_L4_FEWM_original_daily_events'] for a in ['l4h02','fewm']) and all(h['next_window_original_daily_events'][a]==hp['next_SMA_candidate_original_daily_events'] for a in ['SMA','candidate'])
assert h['current_original_signed_units_by_asset_cost']=={a:{asset:{k:z['signed_units'] for k,z in books.items()} for asset,books in rd(R/(a+'_observation/state.json'))['books'].items()} for a in ['candidate','l4h02','fewm']}
full=rd(R/'SMA_full79_prebinding.json');assert h['SMA_full79_sha256']==sha(ROOT/full['authority'])==full['sha256'] and h['SMA_next_daily_event_requires_full_days']==80 and not h['SMA_next_mark_only_adapter_applicable_to_next_window']
put(R/'midnight_handoff_verification.json',{'passed':True,'current_funding_records_by_account':aw['current_funding_records_by_account'],'next_daily_events':h['next_window_original_daily_events'],'next_funding_pending':pending,'source15_SHA':s15['sha256'],'source15_LF_funding_before_original_daily_verified':True,'SMA_current_full79_verified_next_daily_requires_new_closed_full80':True,'new_strategy_or_account_or_cashflow_executions':0})
put(R/'next_funding_handoff_verification.json',{'passed':True,'first_actual_sources':sources,'all3_original_perps_actual16_and08_unique_counts6_each':True,'known_first_source_SHA_original_UTC_and_exact_fields_retained':True,'next_pending_from_fresh_complete_actual_query':pending,'no_early_or_duplicate_bookings':True,'next_window_must_refresh_and_bind_before_reserve':True,'cashflow_or_strategy_or_account_calculations':0,'financial_report_sha256_unchanged':first});print(json.dumps({'passed':True,'known_sources':len(sources),'next_pending':pending,'new_evaluations':0}))
