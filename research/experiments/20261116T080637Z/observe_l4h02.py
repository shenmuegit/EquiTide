"""Three bounded verified-TLS public GET attempts; frozen observer/account semantics."""
import gzip,hashlib,json,subprocess,sys,time,urllib.parse
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261031T174613Z/prospective_l4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();plan=json.loads((R/'l4h02_resume_plan.json').read_text());assert time.time_ns()>=plan['cutoff_ns']+60000000000
(R/'l4h02_reference_closure.json').write_text(json.dumps({'actual_launch_ns':time.time_ns(),'required_closed_reference_after_ns':plan['cutoff_ns']+60000000000,'future_window_not_evaluated_before_reference_closed':True},indent=2)+'\n')
for path,h in plan['source_sha256'].items():assert sha(ROOT/path)==h,path
assert sha(ROOT/'research/automation/l4h02_forward_latest.json')==plan['previous_pointer_sha256'] and not (R/'l4h02_observation').exists()
sys.path.insert(0,str(SOURCE));import observer as obs
(R/'l4h02_transport_plan.json').write_text(json.dumps({'recorded_utc':datetime.now(timezone.utc).isoformat(),'public_GET_attempts_per_URL':3,'TLS_verification':True,'strategy_state_transition_frozen':True,'adapter_sha256':sha(Path(__file__)),'frozen_sources_sha256':plan['source_sha256']},indent=2)+'\n')
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 assert path in ['/fapi/v1/exchangeInfo','/fapi/v1/time','/fapi/v1/klines','/fapi/v1/markPriceKlines','/fapi/v1/fundingRate']
 for attempt in range(3):
  started=datetime.now(timezone.utc).isoformat();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=65);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');dest=rawdir/f'http_{len(receipts):04d}.gz';dest.write_bytes(gzip.compress(body,mtime=0));item={'url':url,'started_utc':started,'http_status':int(code),'curl_exit_code':z.returncode,'raw':str(dest.relative_to(ROOT)),'sha256':sha(dest),'bytes':len(body),'stderr':z.stderr.decode(errors='replace'),'transport':'verifiedDefaultTLSHTTP1.1 publicGET,bounded3attempts'};receipts.append(item)
  if z.returncode==0 and int(code)==200:return json.loads(body)
 raise RuntimeError('Three bounded public GET attempts failed;preserve account and capture failure')
obs.request=request;sys.argv=[str(SOURCE/'observer.py'),'run','--round',R.name,'--cutoff',plan['cutoff_utc'],'--lock-pid',str(plan['branch_lock_broker_pid'])];obs.main()
