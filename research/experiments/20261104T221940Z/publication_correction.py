"""Verify a manifest-key correction against the immutable first pushed commit."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
cor=json.loads((R/'publication_correction.json').read_text());origin=cor['original_pushed_commit'];path=str((R/'data_manifest.json').relative_to(ROOT));oldraw=subprocess.check_output(['git','show',origin+':'+path],cwd=ROOT);assert sha(oldraw)==cor['original_manifest_sha256'];old=json.loads(oldraw);new=json.loads((R/'data_manifest.json').read_text())
assert 'prospective_readiness' not in old and old['fewm_status']['actual_candidate_observations']==321
assert 'fewm_status' not in new and new['prospective_readiness']==old['fewm_status'] and new['prospective_readiness']['actual_candidate_observations']==321
for key in old:
 if key not in ['fewm_status','artifacts']:assert new[key]==old[key],key
changed=cor['intentional_original_artifact_changes'];assert set(changed)=={str((R/n).relative_to(ROOT)) for n in ['finalize.py','result.md']}
for file,h in old['artifacts'].items():
 raw=(ROOT/file).read_bytes()
 if file in changed:
  assert sha(subprocess.check_output(['git','show',origin+':'+file],cwd=ROOT))==h==changed[file]['original_sha256'];assert sha(raw)==changed[file]['corrected_sha256']
 else:assert sha(raw)==h,file
for file,h in new['artifacts'].items():assert sha((ROOT/file).read_bytes())==h,file
assert sha((R/'report.json').read_bytes())==old['finished_report_sha256']==new['finished_report_sha256']
assert sha((R/'registry_records.jsonl').read_bytes())==new['registry']['logical_append_sha256'] and new['registry']['append_only_events']==30 and new['registry']['new_finished_IDs']==15
source=(R/'finalize.py').read_text();assert "'prospective_readiness':{'actual_candidate_observations'" in source and "'fewm_status':{'actual_candidate_observations'" not in source
required=new['required_command_receipts'];assert 'fewm_status_commands.json' in required and all(row['exit_code']==0 for rows in required.values() for row in rows)
print(json.dumps({'passed':True,'original_commit':origin,'original_manifest_sha256':sha(oldraw),'corrected_manifest_sha256':sha((R/'data_manifest.json').read_bytes()),'canonical_field':'prospective_readiness','actual_candidate_observations':321,'new_FEWM_actual_observations':new['new_FEWM_independent_future_plan']['actual_observations'],'all_financial_results_ledgers_registry_and_33_calculation_sources_unchanged':True,'source_manifest_template_fixed':True,'complete_original_artifact_changes_retained_in_git_history':list(changed),'financial_or_observation_reruns':0}))
