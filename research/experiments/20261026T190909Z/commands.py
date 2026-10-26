"""Record each actual stage separately; never rerun completed financial evaluation."""
import json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;PY='/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python'
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
phase=sys.argv[1];research=[('evaluate','evaluate.log',['run.py','evaluate']),('audit_initial','audit_initial.log',['audit.py']),('summary','summary.log',['summarize.py']),('audit_final','audit_final.log',['audit.py']),('finish','finish.log',['run.py','finish'])]
if phase in [x[0] for x in research]:
 index=next(i for i,x in enumerate(research) if x[0]==phase);dest=R/('research_effective_commands.json' if (R/'research_effective_commands.json').exists() else 'research_commands.json');out=json.loads(dest.read_text()) if dest.exists() else [];assert len(out)==index and all(x['exit_code']==0 for x in out);jobs=[research[index][1:]]
else:
 dest=R/(phase+'_commands.json');assert not dest.exists();out=[]
 jobs={'initial':[('alignment.log',['check_alignment.py']),('engine_domain.log',['check_engine_domain.py']),('reserve.log',['run.py','freeze'])],'forward':[('forward_reserve.log',['forward_registry.py','reserve']),('forward_evaluate.log',['forward.py']),('forward_audit.log',['audit_forward.py']),('forward_finish.log',['forward_registry.py','finish']),('forward_replay.log',['forward.py','--reproduce'])],'observer_checks':[('observer_checks.log',['check_prospective_observer.py'])], 'observer_status':[('observer_status.log',['ROOT:research/experiments/20261026T110637Z/prospective_observer.py','status'])], 'audit_recovery':[('audit_initial_recovery.log',['audit.py'])], 'review_recovery':[('source_checks_recovery.log',['check_sources.py'])],'review':[('candidate_validation.log',['candidate_validation.py']),('source_checks.log',['check_sources.py'])],'gates':[('registry_gate.log',['ROOT:checks/strategy_registry.py']),('snapshot.log',['ROOT:research/monitor/snapshot.py']),('monitor_check_final.log',['ROOT:checks/monitor_snapshot.py'])],'feed':[('feed_attribution.log',['check_feed.py'])]}[phase]
if phase in ['review','gates','feed']:
 rr=json.loads((R/('research_effective_commands.json' if (R/'research_effective_commands.json').exists() else 'research_commands.json')).read_text());assert len(rr)==5 and all(x['exit_code']==0 for x in rr)
if phase in ['gates','feed']:
 effective=R/'review_effective_commands.json';assert all(x['exit_code']==0 for x in json.loads((effective if effective.exists() else R/'review_commands.json').read_text()))
saved={p:p.read_bytes() for p in [ROOT/'research/monitor/latest.json',ROOT/'research/monitor/configs.json.gz']} if phase=='gates' else {}
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
for log,args in jobs:
 script=str(ROOT/args[0][5:]) if args[0].startswith('ROOT:') else str(R/args[0]);cmd=['python3' if phase=='gates' else PY,script,*args[1:]];start=now();p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);end=now();(R/log).write_text(p.stdout+p.stderr);row={'command':cmd,'cwd':str(ROOT),'started_utc':start,'finished_utc':end,'exit_code':p.returncode,'log':str((R/log).relative_to(ROOT)),'stderr':p.stderr};out.append(row);put(dest,out);print(json.dumps({'phase':phase,'log':log,'exit_code':p.returncode,'last_output':(p.stdout+p.stderr)[-1800:]}),flush=True)
 if p.returncode:
  for path,data in saved.items():path.write_bytes(data)
  if saved:row['previous_valid_monitor_pair_restored']=True
  facts=json.loads((R/'read_failures.json').read_text());facts['facts'].append(row);put(R/'read_failures.json',facts);raise SystemExit(p.returncode)
