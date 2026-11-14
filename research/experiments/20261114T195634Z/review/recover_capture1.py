"""Archive a failed public capture before any reservation or account advance; original observer unchanged."""
import ast,json,sys,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,rel,now
W=R/'l4h02_observation';f=json.loads((W/'failure.json').read_text());assert not f['result_available'] and not f['complete_actual_result_requires_finish_recovery'] and f['previous_state_preserved'] and set(x.name for x in W.iterdir())=={'failure.json','failure_receipts.json'}
point=ROOT/'research/automation/l4h02_forward_latest.json';plan=json.loads((R/'l4h02_resume_plan.json').read_text());assert sha(point)==plan['previous_pointer_sha256'];b=json.loads((R/'code_binding_before_evaluation.json').read_text());assert all(sha(ROOT/p)==h for p,h in {**b['source_sha256'],**b['immutable_source_sha256']}.items())
raw=ROOT/'data/raw/binance/l4h02_forward'/R.name;dest=raw.with_name(R.name+'_capture_failed_attempt1');assert not dest.exists();mapping=[]
for z in f['receipts']:
 assert 'command' not in z and sha(ROOT/z['raw'])==z['sha256'];mapping.append({'original_raw':z['raw'],'relocated_raw':rel(dest/Path(z['raw']).name),'sha256':z['sha256']})
archive=R/'l4h02_capture_failed_attempt1';assert not archive.exists();W.rename(archive);raw.rename(dest);original=archive/'failure_receipts.json';shutil.copyfile(original,archive/'failure_receipts_original.json');receipts=json.loads(original.read_text())
for z in receipts:z['raw']=next(x['relocated_raw'] for x in mapping if x['original_raw']==z['raw']);assert sha(ROOT/z['raw'])==z['sha256']
put(original,receipts)
for name in ['l4h02_reference_closure.json','l4h02_transport_plan.json']:shutil.copyfile(R/name,archive/name)
put(R/'l4h02_capture_recovery.json',{'passed':True,'recorded_utc':now(),'failed_capture_archive':rel(archive),'original_failure_and_receipts_bytes_retained':True,'immutable_public_bytes_relocated_to_unique_paths':mapping,'original_frozen_observer_sources_unchanged':True,'no_observation_reserved_or_computed_before_capture_failure':True,'previous_pointer_sha256_unchanged':sha(point),'completed_financial_or_account_reruns':0,'retry_same_closed_window_permitted':True})
p=R/'commands.py';s=p.read_text();line="if phase=='l4h02_retry1':jobs=[('l4h02_audit.log',['audit_l4h02.py']),('l4h02_index.log',['project_l4h02_batch.py'])]\n";assert line in s;s=s.replace(line,'');ast.parse(s);p.write_text(s)
p=R/'finalize.py';s=p.read_text();old="key=phase+'_commands.json';required[key]=allcommands[key]";assert old in s;s=s.replace(old,"key=('l4h02_retry1' if phase=='l4h02' else phase)+'_commands.json';required[key]=allcommands[key]");ast.parse(s);p.write_text(s)
print('PASS archived 1successful+3failed actualGET bodies/receipts;0observation reservations/calculations,sourcebindings/pointer intact;permit samewindow capture retry')
