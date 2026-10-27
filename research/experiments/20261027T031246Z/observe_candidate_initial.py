"""Public GET transport adapter; original frozen observer/core transitions unchanged."""
import gzip,hashlib,json,subprocess,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261026T110637Z'
sys.path.insert(0,str(SOURCE));import prospective_observer as obs
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert obs.POINTER.exists() and not(R/'candidate_observation').exists()
oldpoint=json.loads(obs.POINTER.read_text());assert oldpoint['cutoff_ns']==obs.c.ns('2026-10-27T00:30:00Z')
put(R/'candidate_transport_plan.json',{'frozen_utc':datetime.now(timezone.utc).isoformat(),'changes':'Only publicGET verifiedTLS boundedcurlretry;original core/observer signal,cost,funding,quantity,state,registration unchanged. No priorfailedcapture thisround.','source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'prospective_core.py',SOURCE/'prospective_observer.py']},'previous_shared_pointer_sha256':sha(obs.POINTER),'previous_pointer':oldpoint,'cutoff_utc':'2026-10-27T02:30:00Z'})
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 start=datetime.now(timezone.utc).isoformat();cmd=['curl','--fail','--silent','--show-error','--retry','2','--retry-all-errors','--max-time','20','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=65);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');dest=rawdir/f'http_{len(receipts):04d}.gz';dest.write_bytes(gzip.compress(body,mtime=0));item={'url':url,'started_utc':start,'http_status':int(code),'raw':str(dest.relative_to(ROOT)),'sha256':sha(dest),'bytes':len(body),'transport':'curl verifiedTLS withboundedretry','curl_exit_code':z.returncode,'stderr':z.stderr.decode(errors='replace')};receipts.append(item);print('CAPTURE_HTTP',len(receipts),int(code),z.returncode,flush=True);assert z.returncode==0 and int(code)==200,item;return json.loads(body)

obs.request=request
sys.argv=[str(SOURCE/'prospective_observer.py'),'run','--round',R.name,'--cutoff','2026-10-27T02:30:00Z','--lock-pid','2897610']
obs.main()
