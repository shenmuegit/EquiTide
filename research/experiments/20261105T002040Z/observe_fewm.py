"""Launch the unmodified frozen FEWM observer for its first actual post-start window."""
import hashlib,json,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261104T201939Z/prospective_fewm';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not(ROOT/'research/automation/fewm_forward_latest.json').exists() and not(R/'fewm_observation').exists();sys.path.insert(0,str(SOURCE));import observer as obs
assert time.time_ns()>=obs.c.ns('2026-11-05T00:10:00Z')+obs.c.MIN and obs.c.START==obs.c.ns('2026-11-05T00:01:00Z')
plan={'recorded_utc':datetime.now(timezone.utc).isoformat(),'planned_first_window_utc':['2026-11-05T00:01:00Z','2026-11-05T00:10:00Z'],'frozen_plan_sha256':sha(SOURCE/'plan.json'),'binding_sha256':sha(SOURCE/'binding.json'),'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'plan.json',SOURCE/'binding.json',SOURCE/'core.py',SOURCE/'observer.py',SOURCE/'check.py']},'branch_lock_broker_pid':2196995,'first_real_window_no_previous_account':True,'actual_reference_closed_before_capture':True,'warmup_start_utc':'2026-10-03T00:00:00Z','strategy_cost_and_registration_semantics_unmodified':True,'scope':'Delayedpubliccloseddatareplay,frozenBTC3750/N750 ETH15000/N4500,D1/K.0005. Notpaper10/notrealorders;initialpartialnot180dayqualification.'};(R/'fewm_execution_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
original=obs.request;count=0
def request(path,params,rawdir,receipts):
 global count
 count+=1;print('FEWM_PUBLIC_GET',count,path,params.get('symbol',''),params.get('interval',''),flush=True);data=original(path,params,rawdir,receipts);print('FEWM_CAPTURED',count,len(data) if isinstance(data,list) else 'object',flush=True);return data
obs.request=request;sys.argv=[str(SOURCE/'observer.py'),'run','--round',R.name,'--cutoff','2026-11-05T00:10:00Z','--lock-pid','2196995'];obs.main()
