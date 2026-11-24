"""Verify actual known funding sources, own unique counts and fresh next-window coverage read-only."""
import gzip,json
from datetime import datetime,timezone
from common import *
rd=lambda p:json.loads(p.read_text());binding=rd(R/'next_funding_checker_binding.json');assert sha(Path(__file__))==binding['source_sha256'];first=rd(R/'verification.json')['report_sha256'];assert sha(R/'report.json')==first
h=rd(R/'next_research_state.json')['UTC_midnight_handoff'];aw=rd(R/'account_window_verification.json');lookup=rd(R/'next_window_funding_lookup.json');assert aw['passed'];sources=[]
for entry in h['next_window_known_actual_funding_sources']:
 doc=rd(ROOT/entry['path']);assert sha(ROOT/entry['path'])==entry['sha256'] and doc['recorded_utc']==entry['original_capture_utc'] and doc['public_fields_by_asset']==entry['actual_public_fields']
 for z in doc['HTTP_receipts']:
  assert sha(ROOT/z['raw'])==z['sha256']
  if z['http_status']==200 and not z['curl_exit_code']:
   rows=json.loads(gzip.decompress((ROOT/z['raw']).read_bytes()))
   for asset,fields in doc['public_fields_by_asset'].items():
    if 'symbol='+asset+'USDT' in z['url']:assert all(field in rows for field in fields)
 times={str(int(z['fundingTime'])*1000000) for xs in doc['public_fields_by_asset'].values() for z in xs}
 for a in ['candidate','l4h02','fewm']:assert all(entry['current_own_booked_counts'][a][t]==aw['full_chain_once_counts'][a]['funding'].get(t,0) for t in times)
 sources.append({'path':entry['path'],'sha256':entry['sha256'],'first_capture_utc':entry['original_capture_utc'],'actual_public_fields':entry['actual_public_fields'],'current_own_counts':entry['current_own_booked_counts'],'next_pending_by_own_window':entry['next_own_coverage_expected_counts']})
assert all(aw['full_chain_once_counts'][a]['funding']['1795420800004000000']==6 and aw['full_chain_once_counts'][a]['funding']['1795449600000000000']==6 for a in ['candidate','l4h02','fewm'])
known=next(z for z in sources if z['sha256']=='50d6fbaac525918a6dc1b90d25d353efc5edf8af55f7d50ec9390df61b4b8299');assert known['first_capture_utc']=='2026-11-24T08:05:12.897402Z'
ms=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*1000);pending={}
for a in ['SMA','candidate','l4h02','fewm']:
 window=h['next_SMA_single_window_utc'] if a in ['SMA','candidate'] else h['next_L4_FEWM_window_utc'];pending[a]=0 if a=='SMA' else 3*sum(ms(window[0])<int(z['fundingTime'])<=ms(window[1]) for xs in lookup['public_fields_by_asset'].values() for z in xs)
assert pending==h['next_new_actual_funding_pending_by_own_window']==lookup['own_next_window_pending_counts'] and 'Before ANY next reserve' in h['next_actual_funding_prebinding_contract'] and sha(R/'report.json')==first
pre24=rd(R/'actual00_nov24_prebinding_source.json');assert pre24['sha256']=='8a476216d35fbacff319b02e10697418dc4604f5e89c9b9adaa4c07aa1d1647b' and pre24['first_capture_utc']=='2026-11-24T16:08:09.873310Z'
assert {a:aw['full_chain_once_counts'][a]['funding'].get('1795478400001000000',0) for a in ['candidate','l4h02','fewm']}=={'candidate':6,'l4h02':6,'fewm':6}
assert {a:aw['full_chain_once_counts'][a]['daily'].get('1795478460000000000',0) for a in ['candidate','l4h02','fewm']}=={'candidate':6,'l4h02':6,'fewm':6}
assert h['next_window_original_daily_events']=={'SMA':[],'candidate':[],'l4h02':[],'fewm':[]} and h['SMA_next_daily_event_requires_full_days']==77 and not h['SMA_next_original_daily_registry_rebinding_required'];full=rd(R/'SMA_full76_prebinding.json');assert h['SMA_full76_authority']==full['authority'] and h['SMA_full76_sha256']==full['sha256']==sha(ROOT/full['authority']) and all(v=='2026-11-25T00:01:00Z' for v in h['next_daily_decision_by_account'].values()) and h['all4_originalNov24_daily_booked_once'] and h['all3_perp_actualNov24_00_booked_once']
put(R/'midnight_handoff_verification.json',{'passed':True,'recorded_utc':now(),'known_actual00_source_SHA':pre24['sha256'],'original_capture_UTC':pre24['first_capture_utc'],'actual00_own_counts':h['actual_Nov24_00_counts_by_account'],'originalNov24_daily_own_counts':h['original_Nov24_daily_counts_by_account'],'next_daily_events':h['next_window_original_daily_events'],'next_funding_pending':pending,'SMA_current_full76_verified_and_next_markonly_rebinding_required':True,'SMA_future_dailyNov25_requires_full77_completedNov24':True,'current_financial_report_unchanged':first,'new_strategy_or_account_or_cashflow_executions':0})
put(R/'next_funding_handoff_verification.json',{'passed':True,'recorded_utc':now(),'source_binding':'next_funding_checker_binding.json','first_actual_sources':sources,'all3_original_perps_actual16_and08_unique_counts6_each':True,'known_first_source_SHA_original_UTC_and_exact_fields_retained':True,'next_pending_from_fresh_complete_actual_query':pending,'no_early_or_duplicate_bookings':True,'next_window_must_refresh_and_bind_before_reserve':True,'cashflow_or_strategy_or_account_calculations':0,'financial_report_sha256_unchanged':first});print(json.dumps({'passed':True,'known_sources':len(sources),'current16_counts_each':6,'next_pending':pending,'strategy_or_account_evaluations':0}))
