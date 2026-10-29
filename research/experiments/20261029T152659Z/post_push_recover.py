"""Correct a manifest status alias after real successful push;verify full final tree."""
import hashlib,json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
mp=R/'data_manifest.json';m=read(mp);pp=ROOT/'.git/automation_proofs/20261029T152659Z.json';proof=read(pp);first='9fb39fb423ea20da2397cb5e567a5bbfd56b888b'
env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GIT_SSH_COMMAND':'ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=yes','PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,env=env,text=True).strip()
assert git('rev-parse','--show-toplevel')==str(ROOT) and git('branch','--show-current')=='main' and git('for-each-ref','--format=%(refname)','refs/heads')=='refs/heads/main'
assert git('rev-parse','HEAD')==git('rev-parse','origin/main')==proof['commit']==first
assert subprocess.run(['git','diff','--quiet'],cwd=ROOT).returncode==0 and subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
assert any(len(s.split())>4 and s.split()[1]=='FLOCK' and s.split()[4]==str(m['branch_lock_broker_pid']) for s in Path('/proc/locks').read_text().splitlines())
for path,h in m['artifacts'].items():assert sha(ROOT/path)==h,path
for path,h in m['protected_inputs_sha256'].items():assert sha(ROOT/path)==h,path
arch=pp.with_name('20261029T152659Z.after_push_status_failure.json');assert not arch.exists();arch.write_bytes(pp.read_bytes())
assert proof['failures'][-1]['type']=='KeyError' and proof['failures'][-1]['error']=="'status'"
record={'actual_previous_publisher_exit_code':1,'already_successfully_pushed_commit':first,'already_verified_HEAD_origin_FETCH_and_lsremote_equal':True,'root_cause':'Manifest emitted original_status for22readonly references;final publisher verifier expectedstatus alias. Actual report,registry qualification,oldstatuses and earlier independent source checks were correct.','fix':'Add status alias exactly equal to original_status for all22references,keep original_status and alloriginal source hashes;fix finalizer producer for future use. No verifier condition waived.','original_failure_proof':{'path':str(arch.relative_to(ROOT)),'sha256':sha(arch)},'financial_evaluations_repeated':0,'financial_report_SHA256':sha(R/'report.json'),'original_funding_cash_state_and_all_ledgers_unchanged':True,'recorded_utc':now()}
assert len(m['read_only_source_results'])==22
for ref in m['read_only_source_results'].values():assert 'status' not in ref and ref['original_status'] in ['passed','rejected'];ref['status']=ref['original_status']
p=R/'finalize.py';text=p.read_text();a="unique={x['fingerprint']:x for x in refs}";b="unique={x['fingerprint']:{**x,'status':x['original_status']} for x in refs}";assert a in text;text=text.replace(a,b);p.write_text(text)
put(R/'post_push_verification_recovery.json',record)
facts=read(R/'read_failures.json');facts['facts'].append({'phase':'post-push full verification','publisher_exit_code':1,'successful_push_commit':first,'error_type':'KeyError','error':'status','metadata_only_fix':'post_push_verification_recovery.json','financial_evaluation_repeats':0});put(R/'read_failures.json',facts)
resolution=read(R/'review_resolution.json');resolution['post_push_status_alias_recovery']=record;resolution['failure_fact_records']=len(facts['facts']);put(R/'review_resolution.json',resolution)
with (R/'result.md').open('a') as f:f.write('\n第一结果提交9fb39fb423ea20da2397cb5e567a5bbfd56b888b已真实push，远端树/文件核验后在只读来源status别名处KeyError停止。修复manifest生产器，为22个original_status增加相同status字段；不改实际资格、报告、数据或账本。后续元数据修复提交和最终完整核验/实际退出证明见.git/automation_proofs/20261029T152659Z.json及post_push_verification_recovery.json。\n')
m['recorded_at_utc']=now();m['post_push_metadata_only_correction']=record;m['failure_facts']=facts;m['original_failures_and_recoveries']=resolution;m['artifacts']={str(p.relative_to(ROOT)):sha(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='data_manifest.json'};put(mp,m)
assert sha(R/'report.json')==m['finished_report_sha256']==record['financial_report_SHA256']
changed=[]
for raw in subprocess.check_output(['git','status','--porcelain=v1','-z','--untracked-files=all'],cwd=ROOT).split(b'\0'):
 if raw:
  path=raw[3:].decode()
  if path!='data/normalized':assert path.startswith(str(R.relative_to(ROOT))+'/');changed.append(path)
assert changed and len(changed)==7,changed
proof.update(prior_successfully_pushed_commit=first,base_commit=m['base_commit'],post_push_metadata_correction=record,precommit_sha256={**m['artifacts'],str(mp.relative_to(ROOT)):sha(mp),**{p:x['sha256'] for p,x in m['shared_files'].items()}});put(pp,proof)
def call(*args):
 started=now();p=subprocess.run(['git',*args],cwd=ROOT,env=env,capture_output=True,text=True);row={'command':['git',*args],'cwd':str(ROOT),'started_utc':started,'finished_utc':now(),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};proof['commands'].append(row);put(pp,proof);print(json.dumps({**row,'stdout':p.stdout[:3000],'stderr':p.stderr[:3000]}),flush=True);assert p.returncode==0,{'command':args,'exit_code':p.returncode};return p.stdout.strip()
call('add','--',str(R.relative_to(ROOT)));staged=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().strip('\0').split('\0'));assert staged==set(changed)
proof['precommit_tree']=git('write-tree');proof['staged_paths']=len(staged);put(pp,proof)
call('diff','--cached','--check','--','.',':(exclude,glob)**/*.log');call('commit','-q','-m','research: bind original statuses in publication manifest');proof['commit']=git('rev-parse','HEAD');put(pp,proof)
call('push','git@github.com:shenmuegit/EquiTide.git','HEAD:refs/heads/main');call('fetch','git@github.com:shenmuegit/EquiTide.git','refs/heads/main:refs/remotes/origin/main');proof['independent_ls_remote']=call('ls-remote','--heads','git@github.com:shenmuegit/EquiTide.git');put(pp,proof)
cmd=[sys.executable,str(R/'publish.py'),'verify'];started=now();z=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);proof=read(pp);proof['metadata_correction_final_verification_command']={'command':cmd,'cwd':str(ROOT),'started_utc':started,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr};put(pp,proof);print(json.dumps({'final_verifier_actual_exit_code':z.returncode,'stdout':z.stdout[-4000:],'stderr':z.stderr[-3000:]}),flush=True);assert z.returncode==0
assert proof['complete_tree_and_evidence_verification']['passed'] and proof['complete_tree_and_evidence_verification']['HEAD']==proof['commit'];print(json.dumps({'actual_final_publisher_verifier_exit_code':0,'final_commit':proof['commit'],'prior_result_commit':first,'metadata_only_followup_paths':len(staged),'full_remote_verification_passed':True}),flush=True)
