import hashlib,json,os,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261031T174613Z/prospective_l4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();p=json.loads((R/'l4h02_resume_plan.json').read_text());assert time.time_ns()>=p['cutoff_ns']+60000000000
for path,h in p['source_sha256'].items():assert sha(ROOT/path)==h,path
assert sha(ROOT/'research/automation/l4h02_forward_latest.json')==p['previous_pointer_sha256'] and not(R/'l4h02_observation').exists()
cmd=[os.sys.executable,str(P/'observer.py'),'run','--round',R.name,'--cutoff',p['cutoff_utc'],'--lock-pid',str(p['branch_lock_broker_pid'])];raise SystemExit(subprocess.call(cmd,cwd=ROOT))
