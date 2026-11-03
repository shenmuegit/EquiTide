"""Recover a capture-only TLS failure; original account, rules and observer stay frozen."""
import gzip,hashlib,json,sys,time,urllib.parse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
SOURCE=ROOT/'research/experiments/20261031T174613Z/prospective_l4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rd=lambda p:json.loads(p.read_text())
proof=rd(R/'l4h02_capture_recovery_binding.json');plan=rd(R/'l4h02_resume_plan.json')
assert sha(Path(__file__))==proof['adapter_sha256']
for path,h in proof['unchanged_sources_sha256'].items():assert sha(ROOT/path)==h,path
assert sha(ROOT/'research/automation/l4h02_forward_latest.json')==plan['previous_pointer_sha256']
assert time.time_ns()>=plan['cutoff_ns']+60000000000
failed=R/'l4h02_observation';saved=R/'l4h02_capture_failure'
assert failed.is_dir() and not saved.exists() and sorted(p.name for p in failed.iterdir())==['failure.json','failure_receipts.json']
failure=rd(failed/'failure.json');assert failure['result_available'] is False and failure['previous_state_preserved'] and not failure['complete_actual_result_requires_finish_recovery']
assert not any('command' in x or 'recovery_finish_fp' in x for x in failure['receipts'])
cache={}
for item in failure['receipts']:
 assert sha(ROOT/item['raw'])==item['sha256']
 if item['http_status']==200 and item['curl_exit_code']==0:cache[item['url']]=item
assert len(cache)==7
failed.rename(saved)
sys.path.insert(0,str(SOURCE));import observer as obs
original_request,original_capture=obs.request,obs.capture
failed_rows=[x for x in failure['receipts'] if x['http_status']!=200 or x['curl_exit_code']]
assert len(failed_rows)==2 and all('symbol=ETHUSDT' in x['url'] and '/fundingRate?' in x['url'] for x in failed_rows)
def request(path,params,rawdir,receipts):
 url='https://fapi.binance.com'+path+('?' + urllib.parse.urlencode(params) if params else '')
 if url in cache:
  item=cache[url];receipts.append(item);return json.loads(gzip.decompress((ROOT/item['raw']).read_bytes()))
 assert all(x['url']==url for x in failed_rows)
 receipts.extend(failed_rows)
 return original_request(path,params,rawdir,receipts)
def capture(cut,previous,binding,rawdir,receipts):
 assert cut==plan['cutoff_ns'] and previous['cutoff_ns']==plan['previous_pointer']['cutoff_ns']
 return original_capture(cut,previous,binding,rawdir.with_name(rawdir.name+'_transport_recovery'),receipts)
obs.request,obs.capture=request,capture
sys.argv=[str(SOURCE/'observer.py'),'run','--round',R.name,'--cutoff',plan['cutoff_utc'],'--lock-pid',str(plan['branch_lock_broker_pid'])]
obs.main()
