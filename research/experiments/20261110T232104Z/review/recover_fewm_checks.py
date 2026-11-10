"""Resume only interrupted read-only FEWM checks;preserve actual outer143 and original observe0."""
import hashlib,json,os,subprocess
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];PY='/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python';now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
rd=lambda p:json.loads(p.read_text());dst=R/'fewm_commands.json';rows=rd(dst);assert len(rows)==1 and rows[0]['exit_code']==0 and rows[0]['command'][-1].endswith('/observe_fewm.py')
report=R/'fewm_observation/report.json';before=hashlib.sha256(report.read_bytes()).hexdigest();assert not (R/'fewm_verification.json').exists()
assert any('FLOCK' in s and s.split()[4]=='326399' for s in Path('/proc/locks').read_text().splitlines())
for script,log in [('audit_fewm.py','fewm_audit.log'),('project_fewm_batch.py','fewm_index.log')]:
 cmd=[PY,str(R/script)];start=now();p=subprocess.run(cmd,cwd=ROOT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'},capture_output=True,text=True);(R/log).write_text(p.stdout+p.stderr);row={'command':cmd,'cwd':str(ROOT),'started_utc':start,'finished_utc':now(),'exit_code':p.returncode,'log':str((R/log).relative_to(ROOT)),'stderr':p.stderr,'recovery_after_actual_outer_exit143':True};rows.append(row);dst.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(json.dumps({**row,'last_output':(p.stdout+p.stderr)[-1500:]}),flush=True);assert p.returncode==0
assert hashlib.sha256(report.read_bytes()).hexdigest()==before
f=R/'read_failures.json';d=rd(f);z=next(z for z in d['facts'] if z.get('native_completion_chunk')=='0655b7');z.update(resolved=True,resolution='Preserved native143 and original partial receipt;resumed only missing independent audit/index,each actual exit0;finished FEWM observation/report never reevaluated or rewritten',recovery_receipt='research/experiments/'+R.name+'/review_recover_fewm_checks.py_receipt.json');f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('PASS actual143 preserved;only FEWM audit/index resumed,observe/report unchanged')
