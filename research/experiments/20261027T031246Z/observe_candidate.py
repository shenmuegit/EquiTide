"""Verified TLS public GET transport only; unchanged original incremental observer."""
import gzip,hashlib,json,subprocess,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261026T110637Z'
sys.path.insert(0,str(SOURCE));import prospective_observer as obs
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert not(R/'candidate_observation').exists();oldpoint=json.loads(obs.POINTER.read_text());initial=json.loads((R/'candidate_transport_initial_plan.json').read_text());assert sha(obs.POINTER)==initial['previous_shared_pointer_sha256'] and oldpoint['cutoff_ns']==obs.c.ns('2026-10-27T00:30:00Z')
retryraw=ROOT/'data/raw/binance/candidate_forward'/(R.name+'_curl_retry');oldcapture=obs.capture;attempts=[]
put(R/'candidate_transport_retry_plan.json',{'frozen_utc':datetime.now(timezone.utc).isoformat(),'changes':'Public GET uses compression and separate bounded60secondattempts;failed attempt bytes isolated from successful JSON. VerifiedTLS,original signal/cost/registration/state transition rules unchanged.','source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'prospective_core.py',SOURCE/'prospective_observer.py']},'previous_shared_pointer_sha256':sha(obs.POINTER),'previous_pointer':oldpoint,'cutoff_utc':'2026-10-27T02:30:00Z','initial_failure_archived':'candidate_capture_failure','no_completed_new_window_before_retry':True})
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 for attempt in range(2):
  started=datetime.now(timezone.utc).isoformat();cmd=['curl','--compressed','--silent','--show-error','--connect-timeout','10','--max-time','60','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=70);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');p=rawdir/f'http_attempt_{len(attempts):04d}.gz';p.write_bytes(gzip.compress(body,mtime=0));item={'url':url,'started_utc':started,'http_status':int(code),'raw':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':len(body),'transport':'curl compressed verifiedTLS,separate bounded attempts','curl_exit_code':z.returncode,'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'candidate_transport_attempts.json',attempts);print('CAPTURE_HTTP',len(attempts),int(code),z.returncode,flush=True)
  if z.returncode==0 and int(code)==200:
   data=json.loads(body);receipts.append(item);return data
 receipts.append(item);raise RuntimeError('Public GET failed both bounded attempts;original account preserved')
def capture(cutoff,previous,binding,rawdir,receipts):return oldcapture(cutoff,previous,binding,retryraw,receipts)
obs.request=request;obs.capture=capture
sys.argv=[str(SOURCE/'prospective_observer.py'),'run','--round',R.name,'--cutoff','2026-10-27T02:30:00Z','--lock-pid','2897610'];obs.main()
