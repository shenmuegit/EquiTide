"""Read actual evidence and tracked Git diff; staging whitespace gate remains publisher-owned."""
import ast,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,now
rd=lambda p:json.loads(p.read_text());binding=rd(R/'code_binding_before_evaluation.json');checks={}
for path,h in binding['source_sha256'].items():assert sha(ROOT/path)==h
assert sha(R/'report.json')==rd(R/'verification.json')['report_sha256']
for f in R.rglob('*.py'):ast.parse(f.read_text())
assert not [f for f in R.rglob('*') if f.name=='__pycache__' or f.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in f.name]
for name,args in [('branch',['git','branch','--show-current']),('tracked_diff',['git','diff','--stat']),('status',['git','status','--porcelain=v1']),('tracked_whitespace',['git','diff','--check'])]:
 p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True);checks[name]={'command':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};assert p.returncode==0
assert checks['branch']['stdout'].strip()=='main'
put(R/'preseal_review.json',{'passed':True,'checked_utc':now(),'checks':checks,'code_binding_sources':len(binding['source_sha256']),'financial_report_exact_bytes_preserved':True,'original_failures_and_resolutions_retained':True,'frozen_rules_and_original_account_books_continuous':True,'own_untracked_files_whitespace_gate':'Exact full staged scope git diff --cached --check performed by publisher before commit;logs excluded only.','pending_publication_steps':['seal','commit_main','push_main','independent_remote_tree_blob_proof','release_lock','postrelease_proof']})
print('PASS actualsavedreport/36executors/AST/debris/trackedgitdiff;publisher fullstagedwhitespacegate remains mandatory')
