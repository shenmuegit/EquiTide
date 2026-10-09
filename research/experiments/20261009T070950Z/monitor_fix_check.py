"""Prove supplementary report discovery adds only finished source evidence."""
from pathlib import Path
import gzip,hashlib,importlib.util,json,subprocess
T=Path(__file__).resolve().parent;R=T.parents[2]
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
oldcode=subprocess.check_output(['git','show',prior['base_head']+':research/monitor/snapshot.py'],cwd=R,text=True)
namespace={'__file__':str(R/'research/monitor/snapshot.py'),'__name__':'monitor_before_fix'};exec(compile(oldcode,'snapshot_before.py','exec'),namespace)
s=importlib.util.spec_from_file_location('monitor_after_fix',R/'research/monitor/snapshot.py');new=importlib.util.module_from_spec(s);s.loader.exec_module(new)
protected=[R/p for p in ('research/paper10/plan.json','research/paper10/state.json','research/paper10/run.py','research/automation/registry.jsonl')];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before={str(p.relative_to(R)):sha(p) for p in protected}
a=namespace['build_research'](R);b=new.build_research(R);aa={c['fingerprint']:c for c in a['configs']};bb={c['fingerprint']:c for c in b['configs']}
assert len(aa)==2221 and len(bb)==2225 and all(bb[k]==v for k,v in aa.items())
expected={c['fingerprint'] for c in json.loads((T/'component_batch.json').read_text())};assert set(bb)-set(aa)==expected and len(expected)==4 and a['rounds']==b['rounds'] and a['last_run']==b['last_run']
for fp in expected:
 c=bb[fp];assert c['report']==str((T/'components_report.json').relative_to(R)) and c['capital_usdt']==1500 and c['validation']=={'walk_forward_folds':6,'cost_scenarios':['1','2','3'],'sensitivity_recorded':True} and all(c['scenes'][k]['return_pct']>0 for k in ('1','2','3'))
assert before=={str(p.relative_to(R)):sha(p) for p in protected} and before['research/paper10/state.json']==prior['paper10_state_sha256']
proof={'passed':True,'base_commit':prior['base_head'],'cause':'Discovery of only */report.json omitted four finished sources in components_report.json. Ledger hashes and source results were valid.','old_ranked_rows_preserved':2221,'new_actual_component_rows':4,'added_fingerprints':sorted(expected),'existing_rounds_unchanged':True,'paper_state_unchanged':True,'protected_inputs_sha256':before,'before_snapshot_source_sha256':hashlib.sha256(oldcode.encode()).hexdigest(),'after_snapshot_source_sha256':sha(R/'research/monitor/snapshot.py'),'red_regression_log_sha256':sha(T/'monitor_nondefault_red.log'),'green_regression_log_sha256':sha(T/'monitor_check.log')}
(T/'monitor_fix_check.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({k:v for k,v in proof.items() if k not in ('protected_inputs_sha256','added_fingerprints')}))
