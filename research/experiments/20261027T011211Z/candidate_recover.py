"""Resume transport-only capture before any candidate reservation or state transition."""
import gzip,hashlib,importlib.util,json,os,subprocess,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261026T110637Z';PY=sys.executable
sys.path.insert(0,str(SOURCE));import prospective_observer as obs
sys.path.insert(0,str(ROOT/'research/automation'));import registry
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'candidate_observation';failure=json.loads((old/'failure.json').read_text());assert not failure['complete_actual_result_requires_finish_recovery'] and not obs.POINTER.exists() and not any(x.get('spec',{}).get('name','').startswith('forward_snapshot_candidate_') for x in registry.read_records(ROOT/'research/automation/registry.jsonl').values());assert set(p.name for p in old.iterdir())=={'failure.json','failure_receipts.json'}
archive=R/'candidate_capture_failure';assert not archive.exists();old.rename(archive);cache={x['url']:x for x in failure['receipts'] if x.get('http_status')==200 and '/klines?' in x['url']};source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'prospective_core.py',SOURCE/'prospective_observer.py']};retryraw=ROOT/'data/raw/binance/candidate_forward'/(R.name+'_curl_retry');assert not retryraw.exists();oldcapture=obs.capture
put(R/'candidate_transport_recovery_plan.json',{'frozen_before_retry_utc':datetime.now(timezone.utc).isoformat(),'original_failed_window':str(archive.relative_to(ROOT)),'source_hashes':source_hashes,'cached_closed_minute_pages':len(cache),'no_candidate_registration_or_state_before_retry':True,'retry_raw_directory':str(retryraw.relative_to(ROOT)),'changes':'Only public GET transport uses verified curl, bounded retries and exact URL/body/SHA reuse of prior successful closed pages. Signal,Decimal costs,quantity,collateral,funding,cutoff and registry/state transition functions unchanged.'})
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 if url in cache:
  item=cache[url];raw=ROOT/item['raw'];assert sha(raw)==item['sha256'];body=gzip.decompress(raw.read_bytes());assert len(body)==item['bytes'];receipts.append({**item,'reused_verified_prior_capture':True});return json.loads(body)
 start=datetime.now(timezone.utc).isoformat();cmd=['curl','--fail','--silent','--show-error','--retry','2','--retry-all-errors','--max-time','20','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=65);body,code=z.stdout.rsplit(b'\n',1) if b'\n' in z.stdout else (z.stdout,b'000');dest=rawdir/f'http_{len(receipts):04d}.gz';dest.write_bytes(gzip.compress(body,mtime=0));item={'url':url,'started_utc':start,'http_status':int(code),'raw':str(dest.relative_to(ROOT)),'sha256':sha(dest),'bytes':len(body),'transport':'curl verifiedTLS withboundedretry','curl_exit_code':z.returncode,'stderr':z.stderr.decode(errors='replace')};receipts.append(item);print('CAPTURE_HTTP',len(receipts),int(code),z.returncode,flush=True);assert z.returncode==0 and int(code)==200,item;return json.loads(body)
def capture(cut,previous,binding,rawdir,receipts):return oldcapture(cut,previous,binding,retryraw,receipts)
obs.request=request;obs.capture=capture;sys.argv=[str(SOURCE/'prospective_observer.py'),'run','--round',R.name,'--cutoff','2026-10-27T00:30:00Z','--lock-pid','2861372'];obs.main();assert all(sha(ROOT/p)==h for p,h in source_hashes.items())
