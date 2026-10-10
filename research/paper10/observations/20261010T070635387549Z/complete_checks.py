"""Record necessary fixtures, exact offline replay, ledger and read-only dashboard process exits."""
from pathlib import Path
import json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[3]
commands=[('preexecution_fixtures',['.venv/bin/python','research/paper10/check.py']),('actual_observation_replay',['.venv/bin/python','research/paper10/run.py','--reproduce',T.name]),('registry_checks',['.venv/bin/python','checks/strategy_registry.py']),('monitor_snapshot',['python3','research/monitor/snapshot.py']),('monitor_snapshot_checks',['python3','checks/monitor_snapshot.py'])]
checks=[]
for kind,command in commands:
 p=subprocess.run(command,cwd=R,capture_output=True,text=True);checks.append({'kind':kind,'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});(T/'supplemental_checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps({'kind':kind,'exit_code':p.returncode}),flush=True)
 if p.returncode:sys.exit(p.returncode)
print('PAPER31_ALL_FIVE_CHECKS_EXIT_ZERO',flush=True)
