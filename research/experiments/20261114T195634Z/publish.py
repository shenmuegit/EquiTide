"""Ordinary SSH publication and complete remote-tree/blob evidence verification.

Must run with this round's existing flock broker held. Publication receipts stay
in .git so completed evidence is never rewritten to append a post-push SHA.
"""
import gzip,hashlib,json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
proofpath=ROOT/'.git/automation_proofs'/(R.name+'.json')
proofpath.parent.mkdir(exist_ok=True)
proof=json.loads(proofpath.read_text()) if proofpath.exists() else {'round':R.name,'commands':[]}
def save():proofpath.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GIT_SSH_COMMAND':'ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=yes'}
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env=env).strip()
def call(*args):
 start=now();p=subprocess.run(['git',*args],cwd=ROOT,env=env,capture_output=True,text=True);receipt={'command':['git',*args],'cwd':str(ROOT),'started_utc':start,'finished_utc':now(),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};proof['commands'].append(receipt);save();brief={**receipt,'stdout':p.stdout if len(p.stdout)<4000 else p.stdout[:250]+'...[full output retained in proof]','stderr':p.stderr if len(p.stderr)<4000 else p.stderr[:250]+'...[full output retained in proof]'};print(json.dumps(brief),flush=True);assert p.returncode==0,{'command':args,'exit_code':p.returncode,'full_receipt_in':str(proofpath)};return p.stdout.strip()
def held(pid):
 os.kill(pid,0);return any(len(row.split())>4 and row.split()[1]=='FLOCK' and row.split()[4]==str(pid) for row in Path('/proc/locks').read_text().splitlines())
def scopes():
 changed=[]
 for raw in subprocess.check_output(['git','status','--porcelain=v1','-z','--untracked-files=all'],cwd=ROOT).split(b'\0'):
  if raw:
   status,path=raw[:2].decode(),raw[3:].decode();assert 'R' not in status and 'C' not in status;changed.append((status,path))
 return changed
def expected_hashes(m):
 expected={**m['artifacts'],str((R/'data_manifest.json').relative_to(ROOT)):sha(R/'data_manifest.json'),**m['code_and_frozen_source_sha256'],**m['protected_inputs_sha256']}
 for path,info in m['shared_files'].items():expected[path]=info['sha256']
 return expected
def prepare():
 m=json.loads((R/'data_manifest.json').read_text());assert git('for-each-ref','--format=%(refname)','refs/heads')==b'refs/heads/main';pid=m['branch_lock_broker_pid'];assert held(pid);assert git('rev-parse','--show-toplevel').decode()==str(ROOT) and git('branch','--show-current')==b'main';assert git('rev-parse','HEAD').decode()==m['base_commit'];assert subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
 expected=expected_hashes(m)
 for path,h in expected.items():assert sha(ROOT/path)==h,path
 changed_scope={path for status,path in scopes()};shared={path for path in m['shared_files'] if path in changed_scope};own={str((R/'data_manifest.json').relative_to(ROOT)),*m['artifacts']};allowed=own|shared
 changed=scopes();assert {p for s,p in changed if p!='data/normalized'}==allowed and all(p=='data/normalized' or p in allowed for s,p in changed);assert all(p.startswith(str(R.relative_to(ROOT))+'/') for p in own)
 assert all(row['exit_code']==0 or (m.get('monitor_publication',{}).get('authorized_fallback') and row==m['monitor_publication']['native_failure_receipt'] and row['command'][0]=='python3' and (row['command'][2] if row['command'][1]=='-B' else row['command'][1]) in [str(ROOT/'research/monitor/snapshot.py'),str(ROOT/'checks/monitor_snapshot.py')]) for rows in m['required_command_receipts'].values() for row in rows)
 proof.update(base_commit=m['base_commit'],precommit_sha256={p:expected[p] for p in allowed},branch_lock_broker_pid=pid);save()
 call('add','--',str(R.relative_to(ROOT)),*sorted(shared));staged=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().strip('\0').split('\0'));assert staged==allowed
 proof['precommit_tree']=git('write-tree').decode();proof['staged_paths']=len(staged);save()
 call('diff','--cached','--check','--','.',':(exclude,glob)**/*.log')
 proof['prepared_only']=True;save();print(json.dumps({'prepared':True,'staged_paths':len(staged),'tree':proof['precommit_tree'],'base':m['base_commit']}),flush=True)
def publish():
 prepare()
 call('commit','-q','-m','research: test BTC momentum memories with early exit and reused ETH banks')
 proof['commit']=git('rev-parse','HEAD').decode();save()
 call('push','git@github.com:shenmuegit/EquiTide.git','HEAD:refs/heads/main')
 for attempt in range(1,4):
  try:call('-c','http.version=HTTP/1.1','-c','http.lowSpeedLimit=1000','-c','http.lowSpeedTime=30','-c','protocol.version=2','fetch','--filter=blob:none','https://github.com/shenmuegit/EquiTide.git','refs/heads/main:refs/remotes/origin/main');break
  except AssertionError:
   proof.setdefault('readonly_fetch_transport_retries',[]).append({'attempt':attempt,'receipt_index':len(proof['commands'])-1,'TLS_verification_disabled':False,'commit_or_push_repeated':False});save()
 else:raise AssertionError('All3boundedreadonlyHTTPSfetchesfailed;successfulcommit/pushpreserved')
 for attempt in range(1,4):
  try:proof['independent_ls_remote']=call('-c','http.version=HTTP/1.1','ls-remote','--heads','https://github.com/shenmuegit/EquiTide.git');save();break
  except AssertionError:
   proof.setdefault('readonly_ref_transport_retries',[]).append({'attempt':attempt,'actual_command_receipt_index':len(proof['commands'])-1,'TLS_verification_disabled':False,'commit_or_push_repeated':False});save()
 else:raise AssertionError('All bounded independent public ref reads failed; original successful commit/push and actual failures retained')
 verify()
def verify():
 m=json.loads((R/'data_manifest.json').read_text());assert held(m['branch_lock_broker_pid']);assert git('for-each-ref','--format=%(refname)','refs/heads')==b'refs/heads/main';assert len(proof['independent_ls_remote'].splitlines())==1 and proof['independent_ls_remote'].split()[1]=='refs/heads/main';head=git('rev-parse','HEAD').decode();remote=git('rev-parse','origin/main').decode();fetch=git('rev-parse','FETCH_HEAD').decode();independent=proof['independent_ls_remote'].split()[0];assert head==remote==fetch==independent==proof['commit'];assert subprocess.run(['git','merge-base','--is-ancestor',m['base_commit'],head],cwd=ROOT).returncode==0
 tree=git('rev-parse','HEAD^{tree}').decode();assert tree==git('rev-parse','origin/main^{tree}').decode()==git('write-tree').decode()==proof['precommit_tree']
 a=subprocess.check_output(['git','ls-tree','-r','-z',head],cwd=ROOT);b=subprocess.check_output(['git','ls-tree','-r','-z',remote],cwd=ROOT);assert a==b
 blobs={};gitlinks={};entries=0
 for record in b.split(b'\0'):
  if not record:continue
  meta,path=record.split(b'\t',1);mode,kind,oid=meta.decode().split();path=path.decode();entries+=1
  if kind=='blob':blobs[path]=oid
  elif kind=='commit':assert mode=='160000';gitlinks[path]=oid
  else:raise AssertionError((kind,path))
 assert gitlinks.get('Freqtrade')=='30c00ed632305df2fd076e1efa25b544e1110a55'
 expected=expected_hashes(m)
 for path,h in expected.items():assert path in blobs and sha(ROOT/path)==h,path
 # Read every required remote blob's exact bytes, including complete account history.
 proc=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for path,h in expected.items():
  proc.stdin.write((blobs[path]+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().decode().split();assert header[0]==blobs[path] and header[1]=='blob';size=int(header[2]);raw=proc.stdout.read(size);assert len(raw)==size and proc.stdout.read(1)==b'\n';assert hashlib.sha256(raw).hexdigest()==h,path
 proc.stdin.close();assert proc.wait()==0
 for info in m['real_market_inputs']:assert (ROOT/info['path']).stat().st_size==info['bytes'] and sha(ROOT/info['path'])==info['sha256']
 for info in m['source_annual_and_recent_inputs']:assert sha(ROOT/info['path'])==info['sha256'] and (ROOT/info['path']).stat().st_size==info['bytes']
 for z in json.loads((R/'raw_evidence_index.json').read_text())['artifacts']:assert sha(ROOT/z['original_path'])==sha(ROOT/z['committed_copy'])==z['sha256']
 prefix=subprocess.check_output(['git','show',m['base_commit']+':research/automation/registry.jsonl'],cwd=ROOT);fragment=(R/'registry_records.jsonl').read_bytes();assert (ROOT/'research/automation/registry.jsonl').read_bytes()==prefix and hashlib.sha256(prefix).hexdigest()==m['registry']['main_sha256_before_reserve'];tail=[json.loads(x) for x in fragment.splitlines()];assert len(tail)==18
 sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
 records=reg.read_records(ROOT/'research/automation/registry.jsonl');report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());blocked=json.loads((R/'blocked_batch.json').read_text());assert len(batch)==6 and len(blocked)==3 and len(tail)==2*(len(batch)+len(blocked)) and {x['fingerprint'] for x in tail}=={x['fingerprint'] for x in batch+blocked}
 for row in batch:
  c=report['configs'][row['name']];z=records[row['fingerprint']];assert z['result_available'] and z['status']==c['status']==('passed' if all(c['criteria'].values()) else 'rejected') and z['report_sha256']==sha(R/'report.json')
 for row in blocked:
  z=records[row['fingerprint']];assert not z['result_available'] and z['status']=='blocked' and z['report_sha256']==sha(R/'account_capture_blocked.json')
 for fp,z in m['read_only_source_results'].items():assert records[fp]['status']==z['status'] and records[fp]['report_sha256']==z['report_sha256']
 noaccount=json.loads((R/'account_capture_blocked.json').read_text());assert not noaccount['result_available'] and noaccount['account_calculations']==noaccount['account_fills']==noaccount['new_account_NAV_points']==0
 for stem,z in noaccount['original_account_pointers'].items():assert sha(ROOT/z['path'])==z['sha256'] and json.loads((ROOT/z['path']).read_text())==z['pointer']
 for z in json.loads((R/'last_actual_account_evidence.json').read_text())['rows']:assert sha(ROOT/z['readonly_compatibility_copy'])==sha(ROOT/z['last_actual_source'])==z['sha256']
 assert json.loads((R/'verification.json').read_text())['passed'] and json.loads((R/'feed_verification.json').read_text())['passed'];assert subprocess.run(['git','diff','--quiet'],cwd=ROOT).returncode==0 and subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
 assert all(path=='data/normalized' for status,path in scopes());assert not any(p.name=='__pycache__' or 'checkpoint' in p.name or p.suffix in ['.pyc','.npy','.tmp'] for p in R.rglob('*'))
 proof['prepared_only']=False;proof['complete_tree_and_evidence_verification']={'passed':True,'verified_at_utc':now(),'HEAD':head,'origin':remote,'FETCH_HEAD':fetch,'independent_ls_remote':independent,'complete_recursive_tree_entries':entries,'complete_tree_sha':tree,'remote_blob_content_SHA256_verified':len(expected),'gitlinks':gitlinks,'real_market_inputs_sha_verified':len(m['real_market_inputs']),'all_old_source_market_inputs_verified':len(m['source_annual_and_recent_inputs']),'append_only_registry_events':18,'new_finished_IDs':9,'actual_financial_configs':6,'blocked_missing_result_observation_IDs':3,'actual_new_account_observations':0,'original_accounts_and_paper10_unchanged':True,'protected_files':len(m['protected_inputs_sha256']),'all_actual_success_failure_diagnostic_packets_verified':len(json.loads((R/'raw_evidence_index.json').read_text())['artifacts']),'working_tree_only_preexisting_data_normalized':True,'own_flock_still_held':True};save();print(json.dumps(proof['complete_tree_and_evidence_verification']),flush=True)
if __name__=='__main__':
 try:
  {'prepare':prepare,'publish':publish,'verify':verify}[sys.argv[1]]()
 except BaseException as e:
  proof.setdefault('failures',[]).append({'at_utc':now(),'exit_code':1,'type':type(e).__name__,'error':str(e)});save();raise
