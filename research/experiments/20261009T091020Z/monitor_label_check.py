"""Verify complete new factor labels and unchanged prior labels,without new financial evaluation."""
from pathlib import Path
import gzip,hashlib,importlib.util,json,subprocess
T=Path(__file__).resolve().parent;R=T.parents[2];prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
oldcode=subprocess.check_output(['git','show',prior['base_head']+':research/monitor/snapshot.py'],cwd=R,text=True);namespace={'__file__':str(R/'research/monitor/snapshot.py'),'__name__':'old_indicator_module'};exec(compile(oldcode,'old_indicator.py','exec'),namespace)
s=importlib.util.spec_from_file_location('new_monitor_label',R/'research/monitor/snapshot.py');new=importlib.util.module_from_spec(s);s.loader.exec_module(new);records=new.registry_module(R).read_records(R/'research/automation/registry.jsonl')
assert all(namespace['indicator'](rec['spec'],prior['records'])==new.indicator(rec['spec'],records) for rec in prior['records'].values())
data=gzip.decompress((R/'research/monitor/configs.json.gz').read_bytes());root=json.loads(data);rows=root if isinstance(root,list)else root['configs'];byfp={c['fingerprint']:c for c in rows};batch=json.loads((T/'batch.json').read_text());assert len(batch)==36
for b in batch:
 c=byfp[b['fingerprint']];assert f"成交额/均额{b['volume_lookback_days']}≥{b['minimum_volume_ratio']:g}×" in c['indicator'] and c['status']==records[b['fingerprint']]['status']
proof={'passed':True,'prior_labels_unchanged':len(prior['records']),'new_actual_factors_labeled':36,'correct_lookback_and_ratio':True,'registry_result_status_preserved':True,'snapshot_source_sha256':hashlib.sha256((R/'research/monitor/snapshot.py').read_bytes()).hexdigest(),'checker_source_sha256':hashlib.sha256((R/'checks/monitor_snapshot.py').read_bytes()).hexdigest()};(T/'monitor_label_check.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof))
