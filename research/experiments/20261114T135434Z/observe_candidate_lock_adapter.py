"""Supply this round's verified lock owner to the unchanged bound observer entrypoint."""
import hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];sys.path.insert(0,str(ROOT/'research/experiments/20261026T110637Z'));import prospective_observer as observer
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();b=json.loads((R/'candidate_lock_adapter_binding.json').read_text());assert b['before_account_evaluation'] and sha(R/'observe_candidate.py')==b['unchanged_original_observer_sha256'] and sha(Path(__file__))==b['adapter_sha256'];assert sha(R/'report.json')==b['completed_financial_report_sha256'];assert not (R/'candidate_observation').exists();original_main=observer.main

def main_with_current_owner():
 pos=sys.argv.index('--lock-pid')+1;assert sys.argv[pos]=='1698571';sys.argv[pos]=str(b['current_broker_pid']);observer.owner(b['current_broker_pid']);return original_main()

observer.main=main_with_current_owner
runpy.run_path(str(R/'observe_candidate.py'),run_name='__main__')
