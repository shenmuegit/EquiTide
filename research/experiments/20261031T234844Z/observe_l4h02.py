"""Invoke the unchanged separately frozen observer only after its real first cutoff closes."""
import hashlib,json,os,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;P=ROOT/'research/experiments/20261031T174613Z/prospective_l4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads((R/'future_integration_plan.json').read_text());assert time.time_ns()>=p['first_cutoff_ns']+60_000_000_000
for path,h in p['code_and_frozen_source_sha256'].items():assert sha(ROOT/path)==h,path
assert not(ROOT/'research/automation/l4h02_forward_latest.json').exists() and not(R/'l4h02_observation').exists()
cmd=[os.sys.executable,str(P/'observer.py'),'run','--round',R.name,'--cutoff',p['first_cutoff_utc'],'--lock-pid',str(p['branch_lock_broker_pid'])]
raise SystemExit(subprocess.call(cmd,cwd=ROOT))
