"""Audit every saved public GET phase before sealing; no market or account execution."""
import gzip,hashlib,json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());guard=[R/'report.json',ROOT/'research/automation/registry.jsonl',*[R/(s+'_observation/state.json') for s in ['candidate','l4h02','fewm']]];before={rel(p):sha(p) for p in guard};allrows={}
def add(phase,row):
 raw=row.get('raw',row.get('raw_gzip_path'));path=ROOT/raw;compressed=sha(path);expected=row.get('sha256',row.get('raw_gzip_sha256'));assert compressed==expected;body=gzip.decompress(path.read_bytes());assert len(body)==row.get('bytes',len(body));assert row.get('raw_response_sha256',row.get('body_sha256',hashlib.sha256(body).hexdigest()))==hashlib.sha256(body).hexdigest();stamp=row.get('started_utc',row.get('retrieved_utc'));key=(raw,stamp,row['url']);status=row.get('http_status',row.get('status'));curl=row.get('curl_exit_code',0);z={'phase':phase,'url':row['url'],'original_capture_utc':stamp,'http_status':status,'curl_exit_code':curl,'raw':raw,'sha256':compressed,'raw_bytes':len(body),'stderr':row.get('stderr',''),'failed':status!=200 or curl!=0}
 if key in allrows:assert {k:v for k,v in allrows[key].items() if k!='phase'}=={k:v for k,v in z.items() if k!='phase'}
 else:allrows[key]=z
for row in rd(R/'window_funding_preflight_attempts.json'):add('funding_preflight',row)
for stem in ['l4h02','candidate','fewm']:
 for row in rd(R/(stem+'_observation/input_manifest.json'))['provenance']:add('perp_account_capture',row)
for row in rd(R/'candidate_transport_attempts.json'):add('perp_account_capture',row)
for f in R.glob('l4h02_capture_failed_attempt*/failure_receipts.json'):
 for row in rd(f):
  if 'raw' in row:add('perp_account_capture',row)
for row in rd(R/'forward_report.json')['provenance']:add('SMA_public_spot_capture',row)
rows=list(allrows.values());failed=[z for z in rows if z['failed']];phases={p:{'attempts':sum(z['phase']==p for z in rows),'failures':sum(z['phase']==p and z['failed'] for z in rows)} for p in sorted({z['phase'] for z in rows})}
sma_errors=[{'log':z['log'],'stderr':z['stderr'],'curl_error_codes':re.findall(r'curl: \((\d+)\)',z['stderr'])} for z in rd(R/'forward_commands.json') if 'curl:' in z.get('stderr','')];unpackaged=sum(len(z['curl_error_codes']) for z in sma_errors)
assert all(sha(ROOT/path)==h for path,h in before.items());put(R/'complete_transport_verification.json',{'passed':True,'recorded_utc':now(),'saved_unique_public_GET_attempts':len(rows),'observed_actual_transport_failures':len(failed)+unpackaged,'saved_failed_attempts':len(failed),'failed_attempts_with_preserved_raw':failed,'SMA_internal_retry_stderr':sma_errors,'SMA_unpackaged_internal_retry_failure_count':unpackaged,'SMA_failed_attempt_body_not_separately_persisted_by_original_curl':bool(unpackaged),'scope':'All saved funding-preflight,perp-account andSMAcapture receipts;FEWM and cachedmetadata/time reuse deduplicated by exactoriginal rawpath/capture/URL. Counts public GET attempts,not underlying TCPconnections;unpackaged internal retries separately disclosed.','phase_counts':phases,'all_saved_requests':rows,'prior_transport_scope_erratum_read':'research/experiments/20261113T174515Z/transport_count_erratum.json','failure_count_not_assumed':True,'no_new_market_GETs':True,'no_financial_account_or_registry_writes':True,'unchanged_evidence_sha256':before,'source_sha256':sha(Path(__file__))});print(json.dumps({'passed':True,'actual_saved_GETs':len(rows),'actual_transport_failures':len(failed)+unpackaged,'phase_counts':phases}),flush=True)
