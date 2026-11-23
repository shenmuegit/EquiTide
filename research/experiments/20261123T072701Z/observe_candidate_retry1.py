"""Resume unreserved capture using exact-URL saved public bytes; original finance unchanged."""
import gzip,hashlib,json,subprocess,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261123T052700Z';SOURCE=ROOT/'research/experiments/20261026T110637Z'
sys.path.insert(0,str(SOURCE));import prospective_observer as obs
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rd=lambda p:json.loads(p.read_text());put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');PID=rd(R/'startup.json')['branch_lock_broker_pid'];WIN=rd(R/'account_windows.json')['candidate'];old=rd(R/'candidate_transport_retry_plan.json');assert not(R/'candidate_observation').exists() and sha(obs.POINTER)==old['previous_shared_pointer_sha256'];assert rd(R/'l4h02_verification.json')['passed'] and rd(R/'fewm_verification.json')['passed'];cache={}
for z in rd(R/'l4h02_observation/input_manifest.json')['provenance']:
 if z['url'] in ['https://fapi.binance.com/fapi/v1/exchangeInfo','https://fapi.binance.com/fapi/v1/time'] and z['http_status']==200 and not z.get('curl_exit_code',0):cache[z['url']]=z
for z in rd(P/'l4h02_observation/input_manifest.json')['provenance']:
 if '/fapi/v1/markPriceKlines?' in z['url'] and z['http_status']==200 and not z.get('curl_exit_code',0):cache[z['url']]=z
for z in rd(R/'candidate_transport_attempts.json'):
 if z['http_status']==200 and not z.get('curl_exit_code',0):cache[z['url']]=z
assert len(cache)==5
for z in cache.values():assert sha(ROOT/z['raw'])==z['sha256'];json.loads(gzip.decompress((ROOT/z['raw']).read_bytes()))
source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'prospective_core.py',SOURCE/'prospective_observer.py']};assert source_hashes==old['source_hashes'];put(R/'candidate_capture_recovery_plan.json',{'passed':True,'frozen_utc':datetime.now(timezone.utc).isoformat(),'exact_URL_public_responses':cache,'original_capture_UTC_bytes_SHA256_preserved':True,'source_hashes':source_hashes,'previous_shared_pointer_SHA256':sha(obs.POINTER),'before_any_candidate_reservation':True,'new_financial_or_account_calculations_yet':0,'scope':'Reuse only closed public HTTP200 bytes at identical original request URLs; no account state/cash/q/decision/funding amount/NAV reused. All original strategy, source accounting, costs, registration, signal availability and terminal rules unchanged.'});attempts=[]
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 if url in cache:
  z=dict(cache[url]);z['reused_public_response_only']=True;z['recovery_exact_URL_cache']=True;receipts.append(z);return json.loads(gzip.decompress((ROOT/z['raw']).read_bytes()))
 for attempt in range(3):
  started=datetime.now(timezone.utc).isoformat();cmd=['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--tls-max','1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=70);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');dest=rawdir/'recovery1'/f'http_attempt_{len(attempts):04d}.gz';dest.parent.mkdir(exist_ok=True,parents=True);assert not dest.exists();dest.write_bytes(gzip.compress(body,mtime=0));item={'url':url,'started_utc':started,'http_status':int(code),'raw':str(dest.relative_to(ROOT)),'sha256':sha(dest),'bytes':len(body),'transport':'Unchanged verifiedTLS1.2HTTP1.1,bounded3attempts;only unreserved capture resumed','curl_exit_code':z.returncode,'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'candidate_transport_retry1_attempts.json',attempts);print('CAPTURE_HTTP_RECOVERY1',len(attempts),int(code),z.returncode,flush=True)
  if z.returncode==0 and int(code)==200:data=json.loads(body);receipts.append(item);return data
 receipts.append(item);raise RuntimeError('Pending capture public GET failed bounded recovery; original accounts preserved')
obs.request=request;sys.argv=[str(SOURCE/'prospective_observer.py'),'run','--round',R.name,'--cutoff',WIN['cutoff_utc'],'--lock-pid',str(PID)];obs.main()
