"""Preserve raw command logs and resume a precommit whitespace failure without rewriting finance."""
import hashlib,importlib.util,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('round_publication',R/'publish.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
def main():
 m=json.loads((R/'data_manifest.json').read_text());rec=json.loads((R/'publication_preflight_recovery.json').read_text());assert p.held(m['branch_lock_broker_pid']) and p.git('branch','--show-current')==b'main' and p.git('for-each-ref','--format=%(refname)','refs/heads')==b'refs/heads/main' and p.git('rev-parse','HEAD').decode()==m['base_commit']
 assert p.git('write-tree').decode()==rec['initial_staged_tree']==p.proof['precommit_tree'] and p.proof.get('commit') is None
 assert rec['failed_command']['exit_code']==2 and rec['failed_command']['command']==['git','diff','--cached','--check']
 expected=p.expected_hashes(m);shared=set(m['shared_files']);own={str((R/'data_manifest.json').relative_to(ROOT)),*m['artifacts']};allowed=own|shared
 assert {x for status,x in p.scopes() if x!='data/normalized'}==allowed
 for path,h in expected.items():assert p.sha(ROOT/path)==h,path
 for path,h in rec['unchanged_financial_evidence_sha256'].items():assert p.sha(ROOT/path)==h,path
 assert all(z['exit_code']==0 for rows in m['required_command_receipts'].values() for z in rows)
 p.proof['publication_recovery']={'reason':'Original failed command stdout/stderr contains intentional terminal blank line;retain exact raw log bytes. Restrict whitespace lint to code/spec/report/nonlog files;all paths and raw log bytes still fully SHA256/tree-verified.','initial_failed_staged_tree':rec['initial_staged_tree'],'initial_unpublished_manifest_sha256':rec['initial_unpublished_manifest_sha256'],'raw_log_paths_excluded_only_from_whitespace_lint':[str((R/'reserve.log').relative_to(ROOT))],'finance_and_frozen_definitions_unchanged':True,'committed_recovery_record':str((R/'publication_preflight_recovery.json').relative_to(ROOT))};p.proof['precommit_sha256']={x:expected[x] for x in allowed};p.save()
 p.call('add','--',str(R.relative_to(ROOT)),*sorted(shared));staged=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().strip('\0').split('\0'));assert staged==allowed
 p.call('diff','--cached','--check','--','.',':(exclude,glob)**/*.log')
 p.proof['precommit_tree']=p.git('write-tree').decode();p.proof['staged_paths']=len(staged);p.proof['publication_recovery']['scoped_whitespace_check_actual_exit0']=True;p.save()
 p.call('commit','-q','-m','research: test BTC confirmation across ETH 27 and 29 day slow gates');p.proof['commit']=p.git('rev-parse','HEAD').decode();p.save();p.call('push','git@github.com:shenmuegit/EquiTide.git','HEAD:refs/heads/main');p.call('fetch','git@github.com:shenmuegit/EquiTide.git','refs/heads/main:refs/remotes/origin/main');p.proof['independent_ls_remote']=p.call('ls-remote','--heads','git@github.com:shenmuegit/EquiTide.git');p.save();p.verify()
if __name__=='__main__':
 try:main()
 except BaseException as e:p.proof.setdefault('recovery_failures',[]).append({'at_utc':p.now(),'type':type(e).__name__,'error':str(e)});p.save();raise
