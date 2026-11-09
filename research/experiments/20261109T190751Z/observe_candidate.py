"""Verified TLS public GET transport only; unchanged original incremental observer."""
import gzip,hashlib,json,subprocess,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261026T110637Z'
sys.path.insert(0,str(SOURCE));import prospective_observer as obs
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
WIN=json.loads((R/'account_windows.json').read_text())['candidate']
assert obs.POINTER.exists() and not(R/'candidate_observation').exists();oldpoint=json.loads(obs.POINTER.read_text());assert oldpoint['cutoff_ns']==obs.c.ns(WIN['start_utc']);attempts=[]
put(R/'candidate_transport_retry_plan.json',{'frozen_utc':datetime.now(timezone.utc).isoformat(),'changes':'Only public GET uses compressed verifiedTLS and separate bounded30secondattempts;original observer/core strategy,registration,quantity,cost,funding,risk and state transitions unchanged.','source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'prospective_core.py',SOURCE/'prospective_observer.py']},'previous_shared_pointer_sha256':sha(obs.POINTER),'previous_pointer':oldpoint,'cutoff_utc':WIN['cutoff_utc'],'new_window_before_capture':True})
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 for attempt in range(3):
  started=datetime.now(timezone.utc).isoformat();cmd=['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--tls-max','1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=70);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');p=rawdir/f'http_attempt_{len(attempts):04d}.gz';p.write_bytes(gzip.compress(body,mtime=0));item={'url':url,'started_utc':started,'http_status':int(code),'raw':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':len(body),'transport':'curl compressed verifiedTLS,separate bounded attempts','curl_exit_code':z.returncode,'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'candidate_transport_attempts.json',attempts);print('CAPTURE_HTTP',len(attempts),int(code),z.returncode,flush=True)
  if z.returncode==0 and int(code)==200:
   data=json.loads(body);receipts.append(item);return data
 receipts.append(item);raise RuntimeError('Public GET failed three bounded attempts;original account preserved')
# Fresh round uses original capture directory; it creates the packet destination before any request.
obs.request=request
original_capture=obs.capture
def capture(cutoff,previous,binding,rawdir,receipts):
 im=json.loads((R/'l4h02_observation/input_manifest.json').read_text());assert json.loads((R/'l4h02_verification.json').read_text())['passed'];cache={}
 for z in im['provenance']:
  if z['http_status']==200 and not z.get('curl_exit_code',0) and z['url'] in ['https://fapi.binance.com/fapi/v1/exchangeInfo','https://fapi.binance.com/fapi/v1/time']:
   assert sha(ROOT/z['raw'])==z['sha256'];cache[z['url'].split('.com',1)[1]]=z
 assert set(cache)=={'/fapi/v1/exchangeInfo','/fapi/v1/time'};server=json.loads(gzip.decompress((ROOT/cache['/fapi/v1/time']['raw']).read_bytes()));assert int(server['serverTime'])*obs.c.MS>=cutoff+obs.c.MIN
 put(R/'candidate_public_response_reuse_plan.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_manifest':str((R/'l4h02_observation/input_manifest.json').relative_to(ROOT)),'source_manifest_sha256':sha(R/'l4h02_observation/input_manifest.json'),'responses':cache,'scope':'Reuse actualcurrentpublicmetadata/timeonly;captureownminute/hour/fundingwindow andcalculateownfrozenaccount. NoL4state,cash,quantity,decision,trade,fundingcashfloworNAVreused.','predeclared_before_reservation':True})
 def cached(path,params,rd,rs):
  if path in cache:
   row=dict(cache[path]);row['reused_public_response_only']=True;rs.append(row);return json.loads(gzip.decompress((ROOT/row['raw']).read_bytes()))
  return request(path,params,rd,rs)
 obs.request=cached
 try:return original_capture(cutoff,previous,binding,rawdir,receipts)
 finally:obs.request=request
obs.capture=capture
sys.argv=[str(SOURCE/'prospective_observer.py'),'run','--round',R.name,'--cutoff',WIN['cutoff_utc'],'--lock-pid','4068083'];obs.main()
