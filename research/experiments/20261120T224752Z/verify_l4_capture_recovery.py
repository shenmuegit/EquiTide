"""Verify an initially unreserved capture failure and a single real successful account continuation."""
import gzip,json,hashlib,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sys.path.insert(0,str(ROOT/'research/automation'));import registry
b=rd(R/'observer_lock_recovery_binding.json');assert b['passed'] and sha(R/'report.json')==b['first_finished_financial_report_sha256']
for p,h in {**b['source_sha256'],**b['original_frozen_kernel_SHA256'],**b['failed_evidence_sha256'],**b['protected_sources_sha256']}.items():assert sha(ROOT/p)==h,p
failed=rd(R/'l4h02_capture_failed_attempt1/failure.json');assert failed['result_available'] is False and not failed['complete_actual_result_requires_finish_recovery'];assert rd(R/'l4h02_commands.json')[0]['exit_code']==1;eff=rd(R/'l4h02_retry1_commands.json');assert len(eff)==3 and all(x['exit_code']==0 for x in eff)
v=rd(R/'l4h02_verification.json');assert v['passed'] and v['new_funding_settlements']==6 and v['new_daily_events']==v['new_fills']==0
rs=registry.read_records(ROOT/'research/automation/registry.jsonl');events=registry.read_events(ROOT/'research/automation/registry.jsonl');batch=rd(R/'l4h02_batch.json');assert len(batch)==3
for row in batch:
 fp=row['fingerprint'];es=[e for e in events if e['fingerprint']==fp];assert len(es)==2 and es[0]['status']=='reserved' and es[1]['result_available'] and rs[fp]['result_available'];assert rs[fp]['report_sha256']==sha(R/'l4h02_observation/report.json')
manifest=rd(R/'l4h02_observation/input_manifest.json');assert sha(ROOT/manifest['packet'])==manifest['sha256'] and manifest['packet']==f'data/raw/binance/l4h02_forward/{R.name}/packet.json.gz' and any('_retry1/' in x['raw'] and x['http_status']==200 for x in manifest['provenance']);assert all(sha(ROOT/x['raw'])==x['sha256'] for x in manifest['provenance']);assert any(x['url']=='https://fapi.binance.com/fapi/v1/time' and x['http_status']==200 and x['curl_exit_code']==0 for x in manifest['provenance'])
result={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'actual_initial_failed_phase':'l4h02','effective_native_phase':'l4h02_retry1','actual_effective_receipts':rel(R/'l4h02_retry1_commands.json'),'failed_before_any_window_reservation_or_advance':True,'actual_finished_window_configs':3,'each_current_window_ID_reserved_and_finished_once':True,'full_NAV_and_own_funding_account_audit_passed':True,'current_window_actual_funding_rows':6,'new_daily_decisions':0,'new_fills':0,'frozen_original_kernel_sources_unchanged':True,'first_finished_financial_report_sha256':sha(R/'report.json'),'old_failed_capture_and_all_raw_bytes_retained':True,'actual_completed_financial_or_account_reruns':0,'transport_only_recovery':b['only_change']};put(R/'l4h02_capture_recovery_verification.json',result)
f=R/'read_failures.json';d=rd(f);hits=0
for z in d['facts']:
 if z.get('log')==rel(R/'l4h02_observe.log') and z.get('exit_code')==1:
  z.update(resolved=True,resolution='Original capture failed before reserve/advance; actual l4h02_retry1 succeeded once and full account audit passed; original failures and source hashes retained.',effective_recovery_verification=rel(R/'l4h02_capture_recovery_verification.json'));hits+=1
assert hits==1;put(f,d);print(json.dumps({'passed':True,'original_capture_failed_before_reserve':True,'actual_finished_window_configs':3,'actual_current_funding_rows':6,'financial_report_unchanged':True}))
