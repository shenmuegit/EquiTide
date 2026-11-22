"""Resume unreserved read-only public lookup without replacing any first attempt."""
import json,gzip,subprocess,hashlib
from common import ROOT,R,sha,rel,put,now
rd=lambda p:json.loads(p.read_text());a=rd(R/'window_funding_preflight_attempts.json');assert not(R/'reserve_batches').exists() and not(R/'account_windows.json').exists();responses={};good=[]
for asset in ['BTC','ETH']:
 prior=[z for z in a if z['asset']==asset and z['http_status']==200 and z['curl_exit_code']==0]
 if prior:
  z=prior[-1];responses[asset]=json.loads(gzip.decompress((ROOT/z['raw']).read_bytes()));good.append(z);continue
 url=next(z['url'] for z in a if z['asset']==asset)
 for n in range(1,4):
  at=now();z=subprocess.run(['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--tls-max','1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--write-out','\n%{http_code}',url],cwd=ROOT,capture_output=True,timeout=65);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else(z.stdout,b'000');raw=R/'window_funding_responses'/f'{asset}_recovery1_{n}.json.gz';assert not raw.exists();raw.write_bytes(gzip.compress(body,mtime=0));row={'asset':asset,'url':url,'started_utc':at,'finished_utc':now(),'http_status':int(code),'curl_exit_code':z.returncode,'raw':rel(raw),'sha256':sha(raw),'raw_body_sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body),'stderr':z.stderr.decode(errors='replace')};a.append(row);put(R/'window_funding_preflight_attempts.json',a)
  if z.returncode==0 and int(code)==200:responses[asset]=json.loads(body);good.append(row);break
 else:raise RuntimeError('Read-only recovery exhausted; all attempts kept; no reservation/evaluation')
assert all(len(xs)<1000 for xs in responses.values());put(R/'window_funding_preflight.json',{'recorded_utc':now(),'public_fields_by_asset':responses,'query_window_utc':['2026-11-21T22:30:00Z','2026-11-22T02:11:00Z'],'all_pages_completed':True,'HTTP_receipts':good,'purpose':'Fresh complete actual source; successful pages reused without altering captureUTC; failed3TLSattempts preserved in full attempts file. No financial/account calculations.'})
facts=rd(R/'read_failures.json')
for z in facts['facts']:
 if z.get('log')==rel(R/'prepare.log'):z.update(resolved=True,resolution='Original native failure retained; successful public page recovery before any reserve or computation; prepare_retry1 uses complete captured pages.')
put(R/'read_failures.json',facts);print('PASS public lookup recovered; original attempts/captureUTC retained, zero computations')
