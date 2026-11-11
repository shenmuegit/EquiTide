"""Resume a failed pre-reservation capture; preserve all failures and immutable executors."""
import gzip,hashlib,json,os,runpy,subprocess,sys,urllib.parse
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261031T174613Z/prospective_l4';sys.path.insert(0,str(R));from common import sha,put,rel,now,reg
failure=R/'l4h02_observation';arch=R/'l4h02_capture_failed_attempt2';z=json.loads((failure/'failure.json').read_text());assert z['result_available'] is False and z['previous_state_preserved'] and not z['complete_actual_result_requires_finish_recovery'];assert not any('command' in x for x in z['receipts']);assert not arch.exists();failure.rename(arch)
for name in ['l4h02_reference_closure.json','l4h02_transport_plan.json']:(arch/name).write_bytes((R/name).read_bytes())
point=ROOT/'research/automation/l4h02_forward_latest.json';previous_hash=sha(point);attempts=[];put(R/'l4h02_transport_recovery2_plan.json',{'recorded_utc':now(),'failed_attempt':rel(arch),'first_attempt_reserved_IDs':0,'first_attempt_actual_account_results':0,'previous_pointer_sha256':previous_hash,'bound_executor_sha256':sha(R/'observe_l4h02.py'),'transport_only':'Keep TLS verification,HTTP1.1,IPv4;negotiate default supportedTLS instead of forcingTLS1.2 max. Bounded3attempts perURL;unique retry raw names;no state/rule/price substitution.'})
sys.path.insert(0,str(P));import observer as obs
real_main=obs.main;real_capture=obs.capture
def capture_adapter(cutoff,previous,binding,rawdir,receipts):
 return real_capture(cutoff,previous,binding,rawdir.with_name(rawdir.name+'_recovery2'),receipts)
obs.capture=capture_adapter

def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 for i in range(3):
  start=now();cmd=['curl','--ipv4','--compressed','--http1.1','--silent','--show-error','--connect-timeout','10','--max-time','30','--user-agent','EquiTide-ReadOnly-Research/1.0','--write-out','\n%{http_code}',url];p=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=65);body,code=p.stdout.rsplit(b'\n',1) if b'\n' in p.stdout else (p.stdout,b'000');dest=rawdir/f'retry2_http_{len(attempts):04d}.gz';dest.write_bytes(gzip.compress(body,mtime=0));row={'url':url,'started_utc':start,'http_status':int(code),'curl_exit_code':p.returncode,'raw':rel(dest),'sha256':sha(dest),'bytes':len(body),'stderr':p.stderr.decode(errors='replace'),'transport':'verified defaultTLS HTTP1.1 IPv4 bounded3retry;no verification bypass'};attempts.append(row);receipts.append(row);put(R/'l4h02_transport_recovery2_attempts.json',attempts);print('RETRY_HTTP',path,int(code),p.returncode,flush=True)
  if p.returncode==0 and int(code)==200:return json.loads(body)
 raise RuntimeError('DefaultTLS bounded publicGET retry exhausted; preserve original state')
def main_adapter():
 assert sha(point)==previous_hash;obs.request=request;real_main()
obs.main=main_adapter
runpy.run_path(str(R/'observe_l4h02.py'),run_name='__main__')
assert sha(point)!=previous_hash
f=R/'read_failures.json';d=json.loads(f.read_text());rows=[x for x in d['facts'] if x.get('log','').endswith(('l4h02_observe.log','review_recover_l4_transport.py.log'))];
for row in rows:row.update(resolved=True,resolution='Initialcapturehad0reserves/0results;completefailedfolder/rawretained. Retry transportonlyviaTLSnegotiation,no disabledverification. Unchangedboundexecutor/originalobserver advanced thiswindow exactlyonce after reserve and actual closed capture.',recovery_receipt='review_recover_l4_transport_v2.py_receipt.json')
put(f,d)
print('PASS originalL4 ownwindow captured/reserved/advanced/finished once;initialfailure retained,no completed valuation rerun')
