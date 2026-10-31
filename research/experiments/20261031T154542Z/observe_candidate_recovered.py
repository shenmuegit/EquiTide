"""Recover only missing public capture pages; original immutable observer advances once."""
import gzip,hashlib,json,subprocess,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261026T110637Z';sys.path.insert(0,str(SOURCE));import prospective_observer as obs
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');plan=json.loads((R/'candidate_recovery_plan.json').read_text());assert sha(obs.POINTER)==plan['previous_pointer_sha256'] and not(R/'candidate_observation').exists()
for p,h in plan['original_failure_protected_sha256'].items():assert sha(ROOT/p)==h
old=json.loads((R/'candidate_transport_attempts.json').read_text());cache={x['url']:x for x in old if x['http_status']==200 and x['curl_exit_code']==0};attempts=[];reuse=[];retrydir=ROOT/'data/raw/binance/candidate_forward'/(R.name+'_recovery1');assert not retrydir.exists()
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 if url in cache:
  item=cache[url];p=ROOT/item['raw'];assert sha(p)==item['sha256'];raw=gzip.decompress(p.read_bytes());assert len(raw)==item['bytes'];receipts.append({**item,'recovery_readonly_raw_reuse':True});reuse.append({'url':url,'raw':item['raw'],'sha256':item['sha256']});put(R/'candidate_reused_pages.json',reuse);print('CACHE_REUSE',len(reuse),flush=True);return json.loads(raw)
 for attempt in range(2):
  started=datetime.now(timezone.utc).isoformat();cmd=['curl','--ipv4','--compressed','--http1.1','--tlsv1.2','--tls-max','1.2','--silent','--show-error','--connect-timeout','10','--max-time','30','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=70);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else(z.stdout,b'000');p=rawdir/f'http_attempt_{len(attempts):04d}.gz';p.write_bytes(gzip.compress(body,mtime=0));item={'url':url,'started_utc':started,'http_status':int(code),'raw':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':len(body),'transport':'curl verifiedTLS1.2/HTTP1.1, sameexactURL, boundedseparateattempts','curl_exit_code':z.returncode,'stderr':z.stderr.decode(errors='replace')};attempts.append(item);put(R/'candidate_recovery_attempts.json',attempts);print('RECOVERY_HTTP',len(attempts),int(code),z.returncode,flush=True)
  if z.returncode==0 and int(code)==200:receipts.append(item);return json.loads(body)
 receipts.append(item);raise RuntimeError('Missing publicpage failed boundedrecovery; originalaccount stillpreserved')
original_capture=obs.capture
def capture(cut,previous,binding,rawdir,receipts):
 assert rawdir.exists() and not(rawdir/'packet.json.gz').exists();return original_capture(cut,previous,binding,retrydir,receipts)
obs.request=request;obs.capture=capture
sys.argv=[str(SOURCE/'prospective_observer.py'),'run','--round',R.name,'--cutoff','2026-10-31T14:30:00Z','--lock-pid','542216'];obs.main()
assert len(reuse)==6
for p,h in plan['original_failure_protected_sha256'].items():assert sha(ROOT/p)==h
put(R/'candidate_recovery_verification.json',{'passed':True,'six_successful_pages_reused_by_exactURL_SHA':len(reuse),'new_capture_HTTP_attempts':len(attempts),'original_failed_capture_pages_preserved':len(old),'previous_pointer_before_advance_sha256':plan['previous_pointer_sha256'],'original_failed_capture_had_no_registry_or_advance':True,'no_completed_observation_or_financial_backtest_reruns':True,'original_failed_driver_sha256':sha(R/'observe_candidate.py'),'recovery_driver_sha256':sha(R/'observe_candidate_recovered.py'),'complete_report_sha256':sha(R/'candidate_observation/report.json')});print('PASS missingpagecapture recovery, originalaccount advanced exactlyonce',flush=True)
