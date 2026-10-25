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
 start=now();p=subprocess.run(['git',*args],cwd=ROOT,env=env,capture_output=True,text=True);receipt={'command':['git',*args],'cwd':str(ROOT),'started_utc':start,'finished_utc':now(),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};proof['commands'].append(receipt);save();print(json.dumps(receipt),flush=True);assert p.returncode==0,receipt;return p.stdout.strip()
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
def publish():
 m=json.loads((R/'data_manifest.json').read_text());assert git('for-each-ref','--format=%(refname)','refs/heads')==b'refs/heads/main';pid=m['branch_lock_broker_pid'];assert held(pid);assert git('rev-parse','--show-toplevel').decode()==str(ROOT) and git('branch','--show-current')==b'main';assert git('rev-parse','HEAD').decode()==m['base_commit'];assert subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
 expected=expected_hashes(m)
 for path,h in expected.items():assert sha(ROOT/path)==h,path
 shared=set(m['shared_files']);own={str((R/'data_manifest.json').relative_to(ROOT)),*m['artifacts']};allowed=own|shared
 changed=scopes();assert {p for s,p in changed if p!='data/normalized'}==allowed and all(p=='data/normalized' or p in allowed for s,p in changed);assert all(p.startswith(str(R.relative_to(ROOT))+'/') for p in own)
 assert all(row['exit_code']==0 for rows in m['required_command_receipts'].values() for row in rows)
 proof.update(base_commit=m['base_commit'],precommit_sha256={p:expected[p] for p in allowed},branch_lock_broker_pid=pid);save()
 call('add','--',str(R.relative_to(ROOT)),*sorted(shared));staged=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().strip('\0').split('\0'));assert staged==allowed
 proof['precommit_tree']=git('write-tree').decode();proof['staged_paths']=len(staged);save()
 call('commit','-q','-m','research: test different BTC-ETH slow windows from cached NAV')
 proof['commit']=git('rev-parse','HEAD').decode();save()
 call('push','git@github.com:shenmuegit/EquiTide.git','HEAD:refs/heads/main')
 call('fetch','git@github.com:shenmuegit/EquiTide.git','refs/heads/main:refs/remotes/origin/main')
 proof['independent_ls_remote']=call('ls-remote','--heads','git@github.com:shenmuegit/EquiTide.git');save()
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
 for info in m['forward_raw_responses']:
  raw=gzip.decompress((ROOT/info['raw_gzip_path']).read_bytes());assert sha(ROOT/info['raw_gzip_path'])==info['raw_gzip_sha256'] and hashlib.sha256(raw).hexdigest()==info['raw_response_sha256']
 prefix=subprocess.check_output(['git','show',m['base_commit']+':research/automation/registry.jsonl'],cwd=ROOT);ledger=(ROOT/'research/automation/registry.jsonl').read_bytes();assert ledger.startswith(prefix) and hashlib.sha256(prefix).hexdigest()==m['registry']['main_sha256_before_reserve'];appended=[json.loads(x) for x in ledger[len(prefix):].splitlines()];assert len(appended)==114
 sys.path.insert(0,str(ROOT/'research/automation'));import registry
 records=registry.read_records(ROOT/'research/automation/registry.jsonl');report=json.loads((R/'report.json').read_text());forward=json.loads((R/'forward_report.json').read_text());batch=json.loads((R/'batch.json').read_text())+json.loads((R/'forward_batch.json').read_text());assert len(batch)==57 and {x['fingerprint'] for x in appended}=={x['fingerprint'] for x in batch}
 for row in batch:
  r=records[row['fingerprint']];part=row['name'].startswith('forward_snapshot');c=(forward if part else report)['configs'][row['name']];assert r['status']==c['status'] and r['result_available'] is True and r['report_sha256']==sha(R/('forward_report.json' if part else 'report.json'))
 for fp,r in m['read_only_source_results'].items():assert records[fp]['status']==r['status'] and records[fp]['report_sha256']==r['report_sha256']
 assert json.loads((R/'verification.json').read_text())['passed'] and json.loads((R/'feed_verification.json').read_text())['passed'];assert subprocess.run(['git','diff','--quiet'],cwd=ROOT).returncode==0 and subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
 assert all(path=='data/normalized' for status,path in scopes());assert not any(p.name=='__pycache__' or 'checkpoint' in p.name or p.suffix in ['.pyc','.npy','.tmp'] for p in R.rglob('*'))
 proof['complete_tree_and_evidence_verification']={'passed':True,'verified_at_utc':now(),'HEAD':head,'origin':remote,'FETCH_HEAD':fetch,'independent_ls_remote':independent,'complete_recursive_tree_entries':entries,'complete_tree_sha':tree,'remote_blob_content_SHA256_verified':len(expected),'gitlinks':gitlinks,'real_market_inputs_sha_verified':len(m['real_market_inputs']),'forward_original_raw_responses_sha_verified':len(m['forward_raw_responses']),'append_only_registry_events':len(appended),'new_finished_IDs':len(batch),'protected_files':len(m['protected_inputs_sha256']),'finished_report_original_bytes_preserved':True,'working_tree_only_preexisting_data_normalized':True,'own_flock_still_held':True};save();print(json.dumps(proof['complete_tree_and_evidence_verification']),flush=True)
if __name__=='__main__':
 try:
  {'publish':publish,'verify':verify}[sys.argv[1]]()
 except BaseException as e:
  proof.setdefault('failures',[]).append({'at_utc':now(),'exit_code':1,'type':type(e).__name__,'error':str(e)});save();raise
