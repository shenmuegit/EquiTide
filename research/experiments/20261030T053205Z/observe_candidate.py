"""Verified TLS public GET transport only; unchanged original incremental observer."""
import gzip,hashlib,json,subprocess,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261026T110637Z'
sys.path.insert(0,str(SOURCE));import prospective_observer as obs
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert obs.POINTER.exists() and not(R/'candidate_observation').exists();oldpoint=json.loads(obs.POINTER.read_text());assert oldpoint['cutoff_ns']==obs.c.ns('2026-10-30T02:30:00Z');attempts=[]
put(R/'candidate_transport_plan.json',{'frozen_utc':datetime.now(timezone.utc).isoformat(),'changes':'Only public GET uses compressed verifiedTLS and separate bounded60secondattempts;original observer/core strategy,registration,quantity,cost,funding,risk and state transitions unchanged.','source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'prospective_core.py',SOURCE/'prospective_observer.py']},'previous_shared_pointer_sha256':sha(obs.POINTER),'previous_pointer':oldpoint,'cutoff_utc':'2026-10-30T04:30:00Z','new_window_before_capture':False})
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 for attempt in range(2):
  started=datetime.now(timezone.utc).isoformat();cmd=['curl','--compressed','--silent','--show-error','--connect-timeout','10','--max-time','60','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=70);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');p=rawdir/f'http_attempt_{len(attempts):04d}.gz';p.write_bytes(gzip.compress(body,mtime=0));item={'url':url,'started_utc':started,'http_status':int(code),'raw':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':len(body),'transport':'curl compressed verifiedTLS,separate bounded attempts','curl_exit_code':z.returncode,'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'candidate_transport_attempts.json',attempts);print('CAPTURE_HTTP',len(attempts),int(code),z.returncode,flush=True)
  if z.returncode==0 and int(code)==200:
   data=json.loads(body);receipts.append(item);return data
 receipts.append(item);raise RuntimeError('Public GET failed both bounded attempts;original account preserved')
obs.request=request
sys.argv=[str(SOURCE/'prospective_observer.py'),'run','--round',R.name,'--cutoff','2026-10-30T04:30:00Z','--lock-pid','15422'];obs.main()
