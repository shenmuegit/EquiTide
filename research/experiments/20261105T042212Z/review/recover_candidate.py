"""Recover capture-only TLS failure; frozen core, specs and state transition unchanged."""
import copy,gzip,hashlib,json,os,runpy,shutil,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'research/experiments/20261026T110637Z'));import prospective_observer as obs
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text());put=lambda p,x:p.write_text(json.dumps(x,indent=2)+chr(10))
f=R/'candidate_observation';failed=read(f/'failure.json');attempts=read(R/'candidate_transport_attempts.json');oldpoint=obs.POINTER.read_bytes();assert failed['result_available'] is False and not failed['complete_actual_result_requires_finish_recovery'];assert {p.name for p in f.iterdir()}=={'failure.json','failure_receipts.json'};assert all('command' not in x for x in failed['receipts']);assert len(attempts)==3 and sum(x['curl_exit_code']!=0 for x in attempts)==2
li=read(R/'l4h02_observation/input_manifest.json');cached={}
for x in li['provenance']:
 if x['http_status']==200 and x.get('curl_exit_code',0)==0 and x['url'] in ['https://fapi.binance.com/fapi/v1/time','https://fapi.binance.com/fapi/v1/exchangeInfo']:
  assert sha(ROOT/x['raw'])==x['sha256'];cached[x['url'].split('.com',1)[1]]=x
assert set(cached)=={'/fapi/v1/time','/fapi/v1/exchangeInfo'} and json.loads(gzip.decompress((ROOT/cached['/fapi/v1/time']['raw']).read_bytes()))['serverTime']*obs.c.MS>=obs.c.ns('2026-11-05T02:30:00Z')+obs.c.MIN
arch=R/'candidate_capture_failure0';assert not arch.exists();f.rename(arch)
for n in ['candidate_transport_attempts.json','candidate_transport_retry_plan.json']:shutil.copyfile(R/n,arch/n)
bind=read(R/'code_binding_before_evaluation.json');assert all(sha(ROOT/p)==h for p,h in bind['source_sha256'].items())
raworig=ROOT/'data/raw/binance/candidate_forward'/R.name;recovery=raworig.with_name(R.name+'_capture_retry1');assert not recovery.exists();original=obs.capture
def capture(cutoff,previous,binding,rawdir,receipts):
 req=obs.request
 def request(path,params,rd,rs):
  if path in cached:
   row=copy.deepcopy(cached[path]);row['reused_actual_public_response_from']='current L4 capture;public metadata/time only, no L4 account fields';rs.append(row);return json.loads(gzip.decompress((ROOT/row['raw']).read_bytes()))
  return req(path,params,rd,rs)
 obs.request=request
 try:return original(cutoff,previous,binding,recovery,receipts)
 finally:obs.request=req
obs.capture=capture
put(R/'candidate_capture_recovery_plan.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),'cause':'TwoactualverifiedTLSunexpectedEOF failures at public/time before any observation reservation or advance. CurrentL4 capture succeeded at exactsameofficialendpoints;reuseonlyitsverifiedrealmetadata/serverTime responses,requestownminute/hour/funding data andcalculateownfrozenaccount.','frozen_original_sources_unchanged':True,'original_bound_adapter_sha256':sha(R/'observe_candidate.py'),'old_pointer_sha256':hashlib.sha256(oldpoint).hexdigest(),'archive':str(arch.relative_to(ROOT)),'original_all_attempts_preserved':attempts,'new_raw_directory':str(recovery.relative_to(ROOT)),'actual_cached_metadata_time_responses':cached,'no_account_data_or_cashflows_reused':True,'new_actual_financial_calculation_repeated':False,'new_actual_observation_calculation_repeated':False,'retry_only_capture_not_completed_results':True})
try:runpy.run_path(str(R/'observe_candidate.py'),run_name='__main__')
finally:
 if (R/'candidate_transport_attempts.json').exists():
  fresh=read(R/'candidate_transport_attempts.json');put(R/'candidate_transport_attempts.json',attempts+fresh)
assert obs.POINTER.read_bytes()!=oldpoint and (R/'candidate_observation/complete.json').exists();assert all(sha(ROOT/p)==h for p,h in bind['source_sha256'].items())
put(R/'candidate_capture_recovery_verification.json',{'passed':True,'capture_failure_retained':True,'original_pointer_preserved_until_one_successful_advance':True,'no_financial_or_actual_observation_rerun':True,'completed_current_window_once':True,'failure_archive':str(arch.relative_to(ROOT)),'bound_sources_unchanged':True});print('PASScapture-onlyretry,currentaccountadvancedonce,allfailedattemptsretained',flush=True)
