"""Resume only interrupted verification/finish; preserve completed financial bytes."""
import json,os,subprocess,sys
from pathlib import Path
from run import ROOT,R,reg,sha,put,now
PY=sys.executable
rows=json.loads((R/'research_commands.json').read_text());assert len(rows)==3 and all(x['exit_code']==0 for x in rows) and rows[-1]['command'][-1].endswith('summarize.py')
report_sha=sha(R/'report.json');report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert len(batch)==108 and all(records[x['fingerprint']]['status']=='reserved' for x in batch) and not (R/'finish.json').exists()
assert all(sha(ROOT/c['archive'])==c['archive_sha256'] for c in report['configs'].values())
fact={'command':[PY,str(R/'commands.py'),'research'],'cwd':str(ROOT),'started_utc':rows[0]['started_utc'],'observed_finished_utc':now(),'exit_code':143,'tool_session':73353,'log':str((R/'research_session_interruption.json').relative_to(ROOT)),'stderr':'Observed exec session ended143(SIGNAL15); sender/cause not established. First3 jobs actualexit0;finalaudit process/receipt absent at inspection;verificationfile matches finalreportSHA but no exit0 is inferred. No financialrerun.','completed_financial_report_sha256':report_sha,'completed_new_archives':108,'registry_financial_still_reserved':108,'own_branch_broker_still_held':True,'system_mem_available_kb_at_inspection':11444820}
put(R/'research_session_interruption.json',fact);facts=json.loads((R/'read_failures.json').read_text());assert not any(x.get('tool_session')==73353 for x in facts['facts']);facts['facts'].append(fact);put(R/'read_failures.json',facts)
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
for log,args in [('audit_final_recovery.log',[str(R/'audit.py')]),('finish.log',[str(R/'run.py'),'finish'])]:
 command=[PY,*args];start=now();p=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True);end=now();(R/log).write_text(p.stdout+p.stderr);receipt={'command':command,'cwd':str(ROOT),'started_utc':start,'finished_utc':end,'exit_code':p.returncode,'log':str((R/log).relative_to(ROOT)),'stderr':p.stderr,'recovery_of_interrupted_tool_session':73353};rows.append(receipt);put(R/'research_commands.json',rows);print(json.dumps({'log':log,'exit_code':p.returncode,'last_output':(p.stdout+p.stderr)[-1500:]}),flush=True)
 if p.returncode:
  facts=json.loads((R/'read_failures.json').read_text());facts['facts'].append(receipt);put(R/'read_failures.json',facts);raise SystemExit(p.returncode)
 assert sha(R/'report.json')==report_sha
print('RECOVERED_FINAL_AUDIT_AND_FINISH_ONLY_ZERO_NEW_FINANCIAL_EVALUATIONS',report_sha,flush=True)
