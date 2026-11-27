"""Verify published original account/report artifacts and clean only own rebuildable helpers."""
import hashlib,json,os,subprocess
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path.cwd();R=ROOT/'research/experiments/20261127T000013Z';F=ROOT/'.git/automation_proofs';path=F/(R.name+'.json');d=json.loads(path.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');m=json.loads((R/'data_manifest.json').read_text());assert d['push_status']=='success' and d['remote_main_verified']==d['commit'] and d['native_publication_receipt']['exit_code']==0 and d['native_flock_release']['exit_code']==0 and not Path('/proc/'+str(d['broker_pid'])).exists();assert all(sha(ROOT/p)==h for p,h in m['artifacts'].items()) and sha(R/'data_manifest.json')==d['manifest_sha256'];assert sha(R/'report.json')==d['first_financial_report_sha256'] and sha(R/'forward_report.json')==d['first_actual_SMA_report_sha256'];assert set(str(p.relative_to(ROOT)) for p in R.rglob('*') if p.is_file())==set(m['artifacts'])|{str((R/'data_manifest.json').relative_to(ROOT))}
commands=[]
def run(a):
 import time
 network=a[:2] in (['git','fetch'],['git','ls-remote'])
 actual=(['git','-c','http.version=HTTP/1.1','-c','http.sslVersion=tlsv1.2','-c','http.sslVerify=true','-c','remote.origin.url=git@github.com:shenmuegit/EquiTide.git']+a[1:]) if network else a
 for attempt in range(1,(3 if network else 1)+1):
  started=datetime.now(timezone.utc).isoformat()
  try:
   z=subprocess.run(actual,cwd=ROOT,capture_output=True,text=True,timeout=45)
   row={'command':actual,'attempt':attempt,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr}
  except subprocess.TimeoutExpired as e:
   row={'command':actual,'attempt':attempt,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'exit_code':124,'stdout':str(e.stdout or ''),'stderr':str(e.stderr or ''),'timeout_seconds':45}
  commands.append(row);put(F/(R.name+'_postrelease_readonly_retry_commands.json'),commands)
  if row['exit_code']==0:return row['stdout'].strip()
  print(json.dumps({'readonly_transport_failed':True,'attempt':attempt,'exit_code':row['exit_code'],'stderr':row['stderr']},ensure_ascii=False),flush=True)
  if network and attempt<3:time.sleep(1)
 raise RuntimeError('read-only verification command failed after bounded attempts: '+repr(actual))
assert run(['git','branch','--show-current'])=='main';assert run(['git','for-each-ref','--format=%(refname)','refs/heads'])=='refs/heads/main';head=run(['git','rev-parse','HEAD']);assert subprocess.run(['git','merge-base','--is-ancestor',d['commit'],head],cwd=ROOT).returncode==0;run(['git','fetch','origin','main']);remote_main=run(['git','rev-parse','origin/main']);assert subprocess.run(['git','merge-base','--is-ancestor',d['commit'],remote_main],cwd=ROOT).returncode==0;heads=run(['git','ls-remote','--heads','git@github.com:shenmuegit/EquiTide.git']).splitlines();assert len(heads)==1 and heads[0].split('\t')[1]=='refs/heads/main';status=run(['git','status','--short']);assert '?? data/normalized' in status.splitlines();staged=run(['git','diff','--cached','--name-only']);assert not any(x.startswith(str(R.relative_to(ROOT))+'/') for x in staged.splitlines());assert not run(['git','diff','--name-only','HEAD','--',str(R.relative_to(ROOT))]);assert not any(p.name=='__pycache__' or p.suffix in ['.pyc','.tmp','.npy'] for p in R.rglob('*'))
removed=[];removed_bytes=0
for suffix in ['prepare_round.py','adapt_collector.py','bind_late.py','bootstrap.log','source_inventory.log']:
 p=F/(R.name+'_'+suffix)
 if p.exists():removed_bytes+=p.stat().st_size;p.unlink();removed.append(str(p.relative_to(ROOT)))
# These prior-valid monitor copies are rebuildable from the verified base commit.
for item in d.get('monitor_previous_valid_files',[]):
 p=ROOT/item['backup'];assert p.parent==F and p.name.startswith(R.name+'_monitor_previous_') and sha(p)==item['sha256'];removed_bytes+=p.stat().st_size;p.unlink();removed.append(str(p.relative_to(ROOT)))
qa=F/(R.name+'_review_QA.json')
if qa.exists():
 assert json.loads((R/'runtime_note.json').read_text())['visual_QA']==json.loads(qa.read_text());removed_bytes+=qa.stat().st_size;qa.unlink();removed.append(str(qa.relative_to(ROOT)))
assert all(sha(ROOT/p)==h for p,h in m['artifacts'].items()) and sha(R/'data_manifest.json')==d['manifest_sha256']
d['cleaned_rebuildable_private_bytes']=removed_bytes
d.update(status='completed_published_verified_unlocked_cleaned',postrelease_verified_utc=datetime.now(timezone.utc).isoformat(),postrelease_commands=commands,final_HEAD=head,postrelease_remote_main=remote_main,postrelease_worktree_status=status,peer_work_preserved=True,own_artifacts_immutable=True,original_untracked_data_normalized_preserved=True,cleaned_private_rebuildable_helpers=removed);put(path,d);print(json.dumps({'completed':True,'commit':d['commit'],'current_main':head,'own_artifacts':len(m['artifacts'])+1,'push':'verified','lock_released':True,'private_helpers_removed':removed,'only_original_untracked_data':status=='?? data/normalized','peer_work_preserved':True}),flush=True)
