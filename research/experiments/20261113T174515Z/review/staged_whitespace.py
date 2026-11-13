"""Verify only this round's exact staged scope; leave index empty for sealing."""
import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import now,put,rel
assert subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
paths=[rel(R),'research/automation/candidate_forward_latest.json','research/automation/l4h02_forward_latest.json','research/automation/fewm_forward_latest.json','research/monitor/latest.json','research/monitor/configs.json.gz'];commands=[]
try:
 for argv in [['git','add','--',*paths],['git','diff','--cached','--check','--','.',':(exclude,glob)**/*.log']]:
  a=now();z=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True);commands.append({'command':argv,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});assert z.returncode==0,(argv,z.stdout,z.stderr)
finally:
 argv=['git','restore','--staged','--',*paths];a=now();z=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True);commands.append({'command':argv,'cwd':str(ROOT),'started_utc':a,'finished_utc':now(),'exit_code':z.returncode,'stdout':z.stdout,'stderr':z.stderr});put(R/'staged_whitespace_verification.json',{'passed':all(x['exit_code']==0 for x in commands) and len(commands)==3,'commands':commands,'raw_logs_only_excluded_from_whitespace':True,'only_own_scope_staged_and_unstaged':True});assert z.returncode==0
assert subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0;print('PASS strict staged whitespace and restored empty index')
