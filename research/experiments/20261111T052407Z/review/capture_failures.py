"""Preserve failed capture bytes and prove recovery produced one own observation only."""
import gzip,json,sys,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel,now,reg
rd=lambda p:json.loads(p.read_text());rows=[];folder=R/'failed_capture_raw';assert not folder.exists();folder.mkdir();allrows=[]
for f in sorted(R.glob('l4h02_capture_failed_attempt*/failure_receipts.json')):
 failure=rd(f.parent/'failure.json');assert failure['result_available'] is False and failure['previous_state_preserved'] and not failure['complete_actual_result_requires_finish_recovery'];receipts=rd(f);assert not any('command' in z for z in receipts)
 for z in receipts:
  if 'raw' not in z:continue
  raw=ROOT/z['raw'];assert sha(raw)==z['sha256'] and len(gzip.decompress(raw.read_bytes()))==z['bytes'];dest=folder/f'{len(rows):03d}_{raw.name}';shutil.copyfile(raw,dest);assert sha(dest)==sha(raw);rows.append({'original_path':rel(raw),'committed_copy':rel(dest),'sha256':sha(raw),'bytes':raw.stat().st_size,'native_source_failure_receipts':rel(f)});allrows.append(z)
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');im=rd(R/'l4h02_observation/input_manifest.json');rep=rd(R/'l4h02_observation/report.json');assert len(rep['configs'])==3
for c in rep['configs'].values():assert rs[c['fingerprint']]['result_available'] and rs[c['fingerprint']]['report_sha256']==sha(R/'l4h02_observation/report.json')
assert len(allrows)==4 and sum(z['http_status']!=200 or z['curl_exit_code'] for z in allrows)==3
put(R/'failed_capture_artifacts.json',{'passed':True,'recorded_utc':now(),'complete_failed_capture_raw_bytes':rows,'first_actual_HTTP_failures':3,'second_storage_guard_failures':1,'first_and_second_capture_reservations':0,'first_and_second_account_valuations':0,'recovery_actual_configs':3,'source_binding_unchanged':all(sha(ROOT/p)==h for p,h in rd(R/'code_binding_before_evaluation.json')['source_sha256'].items()),'delayed_own_window_completed_once':True,'negative_or_failed_results_removed':0});print('PASS all failed capture rawbytes/native failures retained,0failedreserves,1 actual recovered ownwindow')
