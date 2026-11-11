"""Full context, genuine H-domain RED, four semantic mutants and source binding before valuation."""
import ast,json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];PY='/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python';env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'};now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def go(name,args,expected=0,domain=False):
 cmd=[PY,'-B',str(R/args[0]),*args[1:]];start=now();p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);(R/(name+'.log')).write_text(p.stdout+p.stderr);row={'command':cmd,'cwd':str(ROOT),'started_utc':start,'finished_utc':now(),'exit_code':p.returncode,'expected_exit_code':expected,'real_executor_missing_domain_failure':domain,'deliberate_synthetic_mutant':expected==1 and not domain,'log':str((R/(name+'.log')).relative_to(ROOT))};(R/(name+'_receipt.json')).write_text(json.dumps(row,indent=2)+'\n');print(name,p.returncode,(p.stdout+p.stderr)[-1500:],flush=True)
 if p.returncode!=expected:
  f=R/'read_failures.json';d=json.loads(f.read_text());d['facts'].append({**row,'resolved':False});f.write_text(json.dumps(d,indent=2)+'\n');raise SystemExit(p.returncode or 90)
go('bootstrap',['bootstrap.py']);go('TDD_red',['review/test_price_gates.py'],1,True)
f=R/'engine.py';s=f.read_text();old='H in [.0175,.02,.0225]';assert s.count(old)==1;s=s.replace(old,'H in [.0175,.019,.02,.021,.0225]');ast.parse(s);f.write_text(s)
for name,args in [('TDD_doubleweight_red',['check_asymmetric.py','--negative-control-double-weighting']),('TDD_funding_causality_red',['check_asymmetric.py','--negative-control-future-funding']),('TDD_entry_H_red',['review/test_price_gates.py','--fixed-old-entry-H-bug']),('TDD_retention_E_red',['review/test_price_gates.py','--fixed-old-retention-E-bug'])]:go(name,args,1)
go('preflight_reviews',['review/run_checks.py','funding_signal_preflight.py','public00_reuse.py','public08_reuse.py','public16_reuse.py','public_nov10_08_reuse.py','public_nov10_16_reuse.py','public_nov11_00_reuse.py','test_price_gates.py']);go('freeze_native',['commands.py','freeze']);go('initial_native',['commands.py','initial'])
