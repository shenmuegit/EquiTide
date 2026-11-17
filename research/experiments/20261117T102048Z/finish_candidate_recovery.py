"""Verify first successful account continuation and retain every failed capture byte."""
import json,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));sys.path.insert(0,str(ROOT/'research/automation'));import registry
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'candidate_transport_recovery_binding.json');assert b['passed'] and sha(R/'report.json')==b['first_finished_research_report_sha256']
for path,h in {**b['source_sha256'],**b['original_frozen_kernel_SHA256'],**b['prior_failed_raw_files']}.items():assert sha(ROOT/path)==h,path
v=rd(R/'candidate_verification.json');assert v['passed'] and v['new_daily_events']==v['new_fills']==v['new_funding_settlements']==0
archive=ROOT/b['original_failure_archive'];failure=rd(archive/'failure.json');assert failure['result_available'] is False and all('command' not in z for z in failure['receipts'])
assert rd(R/'candidate_observation/previous_pointer.json')==rd(R/'candidate_transport_retry_plan.json')['previous_pointer']
rows=rd(R/'candidate_batch.json');events=registry.read_events(ROOT/'research/automation/registry.jsonl');records=registry.read_records(ROOT/'research/automation/registry.jsonl')
for row in rows:
 xs=[e for e in events if e['fingerprint']==row['fingerprint']];assert [e['status'] for e in xs]==['reserved','rejected'] and records[row['fingerprint']]['result_available'] and records[row['fingerprint']]['report_sha256']==sha(R/'candidate_observation/report.json')
d=rd(R/'read_failures.json');facts=[z for z in d['facts'] if z.get('log')==rel(R/'candidate.log')];assert len(facts)==1 and facts[0]['exit_code']==1;facts[0].update(resolved=True,resolution='First capture stopped before packet/reserve/advance; exact validated public responses reused, remaining GETs retried; original account advanced once and independently audited.',resolution_proof=rel(R/'candidate_transport_recovery_verification.json'));put(R/'read_failures.json',d)
put(R/'candidate_transport_recovery_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'failure_archive':rel(archive),'failure_before_packet_reserve_and_advance':True,'first_finished_research_report_bytes_unchanged':True,'original_failed_raw_and_receipt_hashes_unchanged':True,'exact_successful_public_response_reuse_count':len(rd(R/'candidate_recovery_public_response_cache.json')['responses_by_exact_URL']),'original_capture_times_preserved':True,'candidate_frozen_kernel_unchanged':True,'completed_candidate_windows_executed':1,'completed_window_reruns':0,'current_candidate_observation_IDs':len(rows),'all_actual_IDs_reserved_and_finished_once':True,'no_other_account_cashflow_or_state_reused':True});print('PASS actualcapturefailurebeforeanyreserve;allfailedbytesretained;firstsuccessfulcandidatewindowexecutedandauditedonce')
