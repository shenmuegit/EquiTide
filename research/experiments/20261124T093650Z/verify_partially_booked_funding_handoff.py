"""Check first future-own-window public funding sources without booking any cashflow."""
from pathlib import Path
from datetime import datetime,timezone
import json,gzip,hashlib
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=rd(R/'next_funding_checker_binding.json');assert sha(Path(__file__))==b['source_sha256']
report=rd(R/'verification.json')['report_sha256'];assert sha(R/'report.json')==report
h=rd(R/'next_research_state.json')['UTC_midnight_handoff'];aw=rd(R/'account_window_verification.json');w=rd(R/'account_windows.json');lookup=rd(R/'next_window_funding_lookup.json');assert aw['passed'] and {a:w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']}=={'SMA':0,'candidate':0,'l4h02':6,'fewm':6};assert h['next_new_actual_funding_pending_by_own_window']==lookup['own_next_window_pending_counts']
entries=h.get('next_currently_unbooked_actual_funding_sources',[]);sources=[]
for entry in entries:
 file=ROOT/entry['path'];doc=rd(file);assert sha(file)==entry['sha256'] and doc['recorded_utc']==entry['original_capture_utc'] and doc['public_fields_by_asset']==entry['actual_public_fields'] and entry['readonly_no_early_cashflow_booking']
 for z in doc['HTTP_receipts']:
  assert sha(ROOT/z['raw'])==z['sha256']
  if z['http_status']==200 and z['curl_exit_code']==0:
   rows=json.loads(gzip.decompress((ROOT/z['raw']).read_bytes()))
   for asset,fields in doc['public_fields_by_asset'].items():
    if 'symbol='+asset+'USDT' in z['url']:assert all(field in rows for field in fields)
 assert entry['original_capture_utc']=='2026-11-24T08:05:12.897402Z' and entry['sha256']=='50d6fbaac525918a6dc1b90d25d353efc5edf8af55f7d50ec9390df61b4b8299'
 times=entry['actual_timestamp_ns'];assert set(times)=={str(int(z['fundingTime'])*1000000) for xs in doc['public_fields_by_asset'].values() for z in xs}
 for a in ['candidate','l4h02','fewm']:
  assert all(entry['current_own_booked_counts'][a][t]==aw['full_chain_once_counts'][a]['funding'].get(t,0)==(0 if a=='candidate' else 6) for t in times)
 assert entry['next_own_coverage_expected_counts']==lookup['own_next_window_pending_counts'];sources.append({'path':entry['path'],'sha256':entry['sha256'],'first_capture_utc':entry['original_capture_utc'],'exact_public_fields':entry['actual_public_fields'],'prior_current_unique_counts':entry['current_own_booked_counts'],'next_pending_by_own_window':entry['next_own_coverage_expected_counts']})
assert all(aw['full_chain_once_counts'][a]['funding']['1795420800004000000']==6 for a in ['candidate','l4h02','fewm'])
if entries:assert 'Before ANY next reserve' in h['next_actual_funding_prebinding_contract'] and h['next_currently_unbooked_actual_funding_sources']==h['next_window_known_actual_funding_sources'] and lookup['own_next_window_pending_counts']=={'SMA':0,'candidate':6,'l4h02':0,'fewm':0}
assert sha(R/'report.json')==report
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_binding':'next_funding_checker_binding.json','first_actual_sources':sources,'current_actual16_unique_counts':{'candidate':0,'l4h02':6,'fewm':6},'current_actual16_cashflow_booked_only_in_covered_L4_FEWM_windows':True,'existing_Nov23_08_unique_counts6_each_unchanged':True,'first_source_SHA_original_UTC_and_exact_actual_fields_retained':True,'next_window_must_refresh_and_bind_before_reserve':True,'cashflow_or_strategy_or_account_calculations':0,'financial_report_sha256_unchanged':report};(R/'next_funding_handoff_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'new_first_sources':len(sources),'current_actual16_counts':{'candidate':0,'l4h02':6,'fewm':6},'next_pending':lookup['own_next_window_pending_counts'],'strategy_or_account_evaluations':0}))
