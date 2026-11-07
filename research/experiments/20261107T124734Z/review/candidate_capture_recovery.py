"""Recover an unreserved failed public capture without changing bound account code."""
import copy,gzip,hashlib,json,sys,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];SOURCE=ROOT/'research/experiments/20261026T110637Z';rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();plan=rd(R/'candidate_capture_recovery_plan.json');point=ROOT/'research/automation/candidate_forward_latest.json';assert sha(point)==plan['previous_shared_pointer_sha256'] and not (R/'candidate_observation').exists();bind=rd(R/'code_binding_before_evaluation.json')
for p,h in bind['source_sha256'].items():assert sha(ROOT/p)==h,p
sys.path.insert(0,str(SOURCE));import prospective_observer as obs
original_capture=obs.capture;cache={x['url']:x for x in plan['successful_BTC_public_responses_to_reuse']};assert len(cache)==3
for x in cache.values():assert sha(ROOT/x['raw'])==x['sha256']
def capture(cutoff,previous,binding,rawdir,receipts):
 assert cutoff==obs.c.ns(rd(R/'account_windows.json')['candidate']['cutoff_utc']);current_request=obs.request
 def cached(path,params,dest,rows):
  url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
  if url in cache:
   x=copy.deepcopy(cache[url]);x['reused_successful_public_response_from_failed_capture']=True;rows.append(x);return json.loads(gzip.decompress((ROOT/x['raw']).read_bytes()))
  return current_request(path,params,dest,rows)
 obs.request=cached
 try:return original_capture(cutoff,previous,binding,rawdir/'recovery_001',receipts)
 finally:obs.request=current_request
obs.capture=capture
# Execute the exact bound root source; its only injected capture changes are above.
script=R/'observe_candidate.py';assert sha(script)==bind['source_sha256'][str(script.relative_to(ROOT))];exec(compile(script.read_text(),str(script),'exec'),{'__file__':str(script),'__name__':'__main__'})
# Merge actual attempts only after successful original observer return; finished reports stay untouched.
old=rd(R/'candidate_capture_failed_attempt/candidate_transport_attempts.json');fresh=rd(R/'candidate_transport_attempts.json');assert all('/recovery_001/' in x['raw'] for x in fresh);(R/'candidate_recovery_fresh_attempts.json').write_text(json.dumps(fresh,indent=2)+'\n');(R/'candidate_transport_attempts.json').write_text(json.dumps(old+fresh,indent=2)+'\n')
print('PASS failedcapturepreserved,3BTCsuccessfulpublicresponsesreused,onlymissingETHcaptured;unchangedaccountcontinuedonce')
