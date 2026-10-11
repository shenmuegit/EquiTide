"""Accept only the documented read-only asymmetricEMA label hash transition."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,importlib.util,json,subprocess,sys
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
meta=json.loads((T/'monitor_label_checks.json').read_text());current=R/meta['source_path'];before=T/'monitor_snapshot_before.py'
assert sha(current)==meta['after_sha256']and sha(before)==meta['before_sha256']
assert current.read_text()==before.read_text().replace(meta['literal_old_block'],meta['literal_new_block'])and before.read_text().count(meta['literal_old_block'])==1
assert subprocess.check_output(['git','show',f"HEAD:{meta['source_path']}"],cwd=R)==before.read_bytes()
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
sys.path.insert(0,str(R/'research/automation'));import registry
prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));records=registry.read_records(R/'research/automation/registry.jsonl');old=load('prior_monitor_indicators',before);new=load('current_monitor_indicators',current)
for fp,rec in prior['records'].items():assert old.indicator(rec['spec'],prior['records'])==new.indicator(rec['spec'],records),fp
count=0
for b in json.loads((T/'batch.json').read_text()):
 sp=records[b['fingerprint']]['spec'];label=new.indicator(sp,records);expected=f"EMA20 +{b['BTC_EMA_entry_band_fraction']*100:g}%/−{b['BTC_EMA_exit_band_fraction']*100:g}%";assert expected in label,label;count+=1
out={'passed':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'source_path':meta['source_path'],'before_sha256':meta['before_sha256'],'after_sha256':meta['after_sha256'],'all_prior_preserved_ids_labels_unchanged':len(prior['records']),'all_new_actual_strategy_labels_verified':count,'accepted_for_future_observation_preflight':'Onlythisread-onlymonitorlabelsourcehash transition is intentional;checkoldsource==before_sha256/current==after_sha256 and keepall otherprotectedinputs unchanged. Do not rewriteold preflightjournals or frozenfinancialcode/accounts.'}
(T/'monitor_compatibility.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
