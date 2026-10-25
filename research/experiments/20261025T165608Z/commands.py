"""Record actual subprocess status,stdout/stderr and timing,including failures."""
import json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
PY='/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python'
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
phase=sys.argv[1]
if phase in ['review','review_recovery','gates','gates_recovery','feed']:
 completed=json.loads((R/'research_commands.json').read_text());assert len(completed)==5 and completed[-1]['command'][-1]=='finish' and all(x['exit_code']==0 for x in completed),'Research finish must actually exit0 before dependent checks'
if phase in ['gates','gates_recovery','feed']:
 checked='review_recovery_commands.json' if (R/'review_recovery_commands.json').exists() else 'review_commands.json'
 assert all(x['exit_code']==0 for x in json.loads((R/checked).read_text())),'Source consistency gate must actually exit0 first'
jobs={
 'initial': [('notional_engineering.log',['check_notional.py']),('alignment.log',['check_alignment.py']),('reserve.log',['run.py','freeze'])],
 'initial_recovery': [('reserve_recovery.log',['run.py','freeze'])],
 'forward': [('forward_reserve.log',['forward_registry.py','reserve']),('forward_evaluate.log',['forward.py']),('forward_audit.log',['audit_forward.py']),('forward_finish.log',['forward_registry.py','finish']),('forward_replay.log',['forward.py','--reproduce'])],
 'research_recovery': [('summary_recovery.log',['summarize.py']),('audit_final.log',['audit.py']),('finish.log',['run.py','finish'])],
 'research': [('evaluate.log',['run.py','evaluate']),('audit_initial.log',['audit.py']),('summary.log',['summarize.py']),('audit_final.log',['audit.py']),('finish.log',['run.py','finish'])],
 'gates': [('registry_gate.log',['ROOT:checks/strategy_registry.py']),('snapshot.log',['ROOT:research/monitor/snapshot.py']),('monitor_check_final.log',['ROOT:checks/monitor_snapshot.py'])],
 'feed': [('feed_attribution.log',['check_feed.py'])],
 'review': [('source_checks.log',['check_sources.py'])]
}[phase]
out=[];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
saved_feeds={p:p.read_bytes() for p in [ROOT/'research/monitor/latest.json',ROOT/'research/monitor/configs.json.gz']} if phase in ['gates','gates_recovery'] else {}
for name,args in jobs:
 script=args[0];script=str(ROOT/script[5:]) if script.startswith('ROOT:') else str(R/script)
 cmd=[('python3' if phase in ['gates','gates_recovery'] else PY),script,*args[1:]];start=now();p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,env=env);end=now()
 (R/name).write_text(p.stdout+p.stderr)
 row={'command':cmd,'cwd':str(ROOT),'started_utc':start,'finished_utc':end,'exit_code':p.returncode,'log':str((R/name).relative_to(ROOT)),'stderr':p.stderr};out.append(row);put(R/(phase+'_commands.json'),out)
 print(json.dumps({'phase':phase,'log':name,'exit_code':p.returncode,'last_output':(p.stdout+p.stderr)[-1800:]}),flush=True)
 if p.returncode:
  if saved_feeds:
   for path,content in saved_feeds.items():path.write_bytes(content)
   row['previous_valid_monitor_pair_restored']=True
  facts=json.loads((R/'read_failures.json').read_text());facts['facts'].append(row);put(R/'read_failures.json',facts);sys.exit(p.returncode)
