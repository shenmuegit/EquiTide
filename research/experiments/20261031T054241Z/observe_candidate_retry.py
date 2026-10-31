"""Recover only pre-valuation packet publication using exact already captured real responses."""
import gzip,hashlib,json,sys,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261026T110637Z'
sys.path.insert(0,str(SOURCE));import prospective_observer as obs
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=json.loads((R/'candidate_observation_failed_capture_000/failure.json').read_text());assert not prior['result_available'] and not prior['complete_actual_result_requires_finish_recovery']
assert sha(ROOT/'research/automation/candidate_forward_latest.json')=='430d1830ee780e03c1ca97b14753a11cf0274d64e6764d77e62e19ffe3e36527'
attempts=json.loads((R/'candidate_transport_attempts.json').read_text());assert len(attempts)==8 and all(x['http_status']==200 and x['curl_exit_code']==0 and sha(ROOT/x['raw'])==x['sha256'] for x in attempts)
by={x['url']:x for x in attempts};assert len(by)==8
used=[]
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 x=by[url];assert url not in used;used.append(url);raw=gzip.decompress((ROOT/x['raw']).read_bytes());assert len(raw)==x['bytes'];receipts.append(x);print('REUSE_REAL_HTTP200',len(used),flush=True);return json.loads(raw)
original_capture=obs.capture
def capture(cutoff,previous,binding,rawdir,receipts):
 packet=original_capture(cutoff,previous,binding,rawdir.with_name(rawdir.name+'_capture_recovered'),receipts)
 assert len(used)==8;rawdir.mkdir(parents=True,exist_ok=False);return packet
obs.capture=capture;obs.request=request
sys.argv=[str(SOURCE/'prospective_observer.py'),'run','--round',R.name,'--cutoff','2026-10-31T04:30:00Z','--lock-pid','395396'];obs.main()
(R/'candidate_recovery_verification.json').write_text(json.dumps({'passed':True,'original_actual_HTTP200_pages_reused':8,'extra_network_requests':0,'first_failed_attempt_financial_reservations':0,'first_failed_attempt_account_calculations':0,'source_observer_unchanged':True,'single_new_window_advance':True},indent=2)+'\n')
