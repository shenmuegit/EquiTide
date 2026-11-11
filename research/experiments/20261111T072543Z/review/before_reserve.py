"""Native complete-context, actual synthetic domain RED, four mutants and fixed source binding."""
import ast,json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];PY='/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python';env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'};now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def go(name,args,expected=0,domain=False):
 cmd=[PY,'-B',str(R/args[0]),*args[1:]];t=now();z=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True);(R/(name+'.log')).write_text(z.stdout+z.stderr);v={'command':cmd,'cwd':str(ROOT),'started_utc':t,'finished_utc':now(),'exit_code':z.returncode,'expected_exit_code':expected,'real_executor_missing_domain_failure':domain,'deliberate_synthetic_mutant':expected==1 and not domain,'log':str((R/(name+'.log')).relative_to(ROOT))};(R/(name+'_receipt.json')).write_text(json.dumps(v,indent=2)+'\n');print(name,z.returncode,(z.stdout+z.stderr)[-1400:],flush=True)
 if z.returncode!=expected:
  f=R/'read_failures.json';d=json.loads(f.read_text());d['facts'].append({**v,'resolved':False});f.write_text(json.dumps(d,indent=2)+'\n');raise SystemExit(z.returncode or 90)
go('bootstrap',['bootstrap.py']);go('TDD_red',['review/test_price_gates.py'],1,True)
p=R/'engine.py';s=p.read_text();old='cap in [.045,.05,.0525,.055,.0575,.06]';assert s.count(old)==1;s=s.replace(old,'cap in [.045,.05,.0525,.055,.05625,.0575,.06]');ast.parse(s);p.write_text(s)
for name,args in [('TDD_doubleweight_red',['check_asymmetric.py','--negative-control-double-weighting']),('TDD_funding_causality_red',['check_asymmetric.py','--negative-control-future-funding']),('TDD_price_ceiling_red',['review/test_price_gates.py','--fixed-old-price-ceiling-bug']),('TDD_ROC_lookback_red',['review/test_price_gates.py','--fixed-old-ROC-lookback-bug'])]:go(name,args,1)
go('preflight_reviews',['review/run_checks.py','funding_signal_preflight.py','public00_reuse.py','public08_reuse.py','public16_reuse.py','public_nov10_08_reuse.py','public_nov10_16_reuse.py','public_nov11_00_reuse.py','test_price_gates.py']);go('freeze_native',['commands.py','freeze']);go('initial_native',['commands.py','initial'])
