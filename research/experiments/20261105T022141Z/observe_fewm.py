"""Continue the original frozen FEWM account; no cash restart or warmup recapture."""
import hashlib,json,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;SOURCE=ROOT/'research/experiments/20261104T201939Z/prospective_fewm';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();POINTER=ROOT/'research/automation/fewm_forward_latest.json'
assert POINTER.exists() and not(R/'fewm_observation').exists();previous=json.loads(POINTER.read_text());sys.path.insert(0,str(SOURCE));import observer as obs
assert previous['cutoff_ns']==obs.c.ns('2026-11-05T00:10:00Z') and time.time_ns()>=obs.c.ns('2026-11-05T02:10:00Z')+obs.c.MIN
for key in ['state','report','delta','complete']:assert sha(ROOT/previous[key])==previous[key+'_sha256']
plan={'recorded_utc':datetime.now(timezone.utc).isoformat(),'window_utc':['2026-11-05T00:10:00Z','2026-11-05T02:10:00Z'],'frozen_plan_sha256':sha(SOURCE/'plan.json'),'binding_sha256':sha(SOURCE/'binding.json'),'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE/'plan.json',SOURCE/'binding.json',SOURCE/'core.py',SOURCE/'observer.py',SOURCE/'check.py']},'previous_pointer':previous,'previous_pointer_sha256':sha(POINTER),'branch_lock_broker_pid':2230650,'first_real_window':False,'no_cash_restart_or_first_order_repeat':True,'no_warmup_redownload':True,'actual_reference_closed_before_capture':True,'strategy_cost_and_registration_semantics_unmodified':True,'scope':'FrozenBTC3750/N750 ETH15000/N4500,D1/K.0005 delayedcloseddatareplay. IndependentfromSMA/single/L4/paper10;no realorders/no BTC1250 adoption.'};(R/'fewm_execution_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
original=obs.request;count=0
def request(path,params,rawdir,receipts):
 global count
 count+=1;print('FEWM_PUBLIC_GET',count,path,params.get('symbol',''),params.get('interval',''),flush=True);data=original(path,params,rawdir,receipts);print('FEWM_CAPTURED',count,len(data) if isinstance(data,list) else 'object',flush=True);return data
obs.request=request;sys.argv=[str(SOURCE/'observer.py'),'run','--round',R.name,'--cutoff','2026-11-05T02:10:00Z','--lock-pid','2230650'];obs.main()
