"""Capture explicit process exits for every read-only reproduction phase."""
from pathlib import Path
import json, subprocess, sys
T=Path(__file__).resolve().parent;R=T.parents[2]
commands=[
    ['.venv/bin/python',str((T/'check_signals.py').relative_to(R))],
    ['.venv/bin/python',str((T/'restore_cache.py').relative_to(R))],
    ['.venv/bin/python',str((T/'forward.py').relative_to(R)),'--reproduce'],
    ['.venv/bin/python',str((T/'evaluate.py').relative_to(R)),'--reproduce'],
    ['.venv/bin/python',str((T/'audit.py').relative_to(R))],
    ['.venv/bin/python',str((T/'audit_forward_240.py').relative_to(R))],
    ['.venv/bin/python','checks/strategy_registry.py'],
]
results=[]
with (T/'reproduce.log').open('w') as log:
    for command in commands:
        result=subprocess.run(command,cwd=R,capture_output=True,text=True)
        log.write(result.stdout);log.write(result.stderr);log.flush()
        results.append({'command':command,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
        (T/'reproduction_execution.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps({'phase':command[1],'exit_code':result.returncode}),flush=True)
        if result.returncode:sys.exit(result.returncode)
print('READONLY_REPRODUCTION_ALL_7_EXIT_ZERO',flush=True)
