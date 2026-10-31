"""Append-only correction of a publisher diagnostic; original sealed files remain exact."""
import contextlib,importlib.util,io,json,hashlib,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));rd=lambda p:json.loads(p.read_text());put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
original_spec=importlib.util.spec_from_file_location('preserved_original_publisher',R/'publish.py');p=importlib.util.module_from_spec(original_spec);original_spec.loader.exec_module(p)
def continuity():
 m=rd(R/'data_manifest.json');cv=rd(R/'candidate_verification.json');point=rd(ROOT/'research/automation/candidate_forward_latest.json');seen=set();ids=set();windows=0;lastcut=point['cutoff_ns'];lastpoints=rd(ROOT/point['state'])['nav_points'];sys.path.insert(0,str(ROOT/'research/automation'));import registry
 records=registry.read_records(ROOT/'research/automation/registry.jsonl')
 while point:
  assert point['delta'] not in seen;seen.add(point['delta'])
  for key in ['state','report','delta','complete']:assert sha(ROOT/point[key])==point[key+'_sha256']
  report=rd(ROOT/point['report']);assert len(report['configs'])==3
  for c in report['configs'].values():
   fp=c['fingerprint'];assert fp not in ids;ids.add(fp);z=records[fp];assert z['result_available'] and z['status']==c['status'] and z['report_sha256']==point['report_sha256']
  windows+=1;prev=point.get('previous_pointer')
  if prev:assert sha(ROOT/prev['path'])==prev['sha256'];point=rd(ROOT/prev['path'])
  else:point=None
 actual=len(ids);assert actual==3*windows==m['prospective_readiness']['actual_candidate_observations']==cv['cumulative_finished_candidate_observations'];assert lastpoints==cv['NAV_points_per_scene'] and cv['passed'] and sha(R/'candidate_observation/report.json')==cv['report_sha256'] and sha(R/'candidate_observation/state.json')==cv['state_sha256']
 for path,h in m['artifacts'].items():assert sha(ROOT/path)==h,path
 return {'passed':True,'actual_complete_windows':windows,'actual_unique_finished_observation_IDs':actual,'manifest_observation_IDs':m['prospective_readiness']['actual_candidate_observations'],'independent_original_audit_observation_IDs':cv['cumulative_finished_candidate_observations'],'full_current_NAV_points':lastpoints,'cutoff_ns':lastcut,'derived_count_equals_manifest_and_audit':True,'original_publisher_wrong_constant':105,'original_false_diagnostic_retained_in_original_receipt':True,'original_sealed_artifacts_unchanged':len(m['artifacts']),'financial_or_observation_reruns':0,'method':'Read every complete pointer/hash/report and distinct registryFP; derive3IDs/window dynamically, do not substitute a new magic comparison constant.'}
def publish():
 s=rd(R/'publication_supplement.json');m=rd(R/'data_manifest.json');assert sha(R/'data_manifest.json')==s['original_sealed_manifest_sha256'];assert p.git('rev-parse','HEAD').decode()==s['previous_published_commit'] and p.held(m['branch_lock_broker_pid']);assert p.git('for-each-ref','--format=%(refname)','refs/heads')==b'refs/heads/main'
 check=continuity();assert rd(R/'publication_continuity_check.json')==check
 extra={**s['new_artifacts'],rel(R/'publication_supplement.json'):sha(R/'publication_supplement.json')}
 for path,h in extra.items():assert sha(ROOT/path)==h
 base_expected=p.expected_hashes;p.expected_hashes=lambda manifest:{**base_expected(manifest),**extra};p.proofpath=ROOT/'.git/automation_proofs'/(R.name+'_supplement.json');assert not p.proofpath.exists();p.proof={'round':R.name,'commands':[],'original_publication_commit':s['previous_published_commit'],'base_commit':m['base_commit'],'append_only_metadata_correction':True};p.save()
 changed={path for status,path in p.scopes() if path!='data/normalized'};assert changed==set(extra);assert subprocess.run(['git','diff','--cached','--quiet'],cwd=ROOT).returncode==0
 p.call('add','--',*sorted(extra));staged=set(subprocess.check_output(['git','diff','--cached','--name-only','-z'],cwd=ROOT).decode().strip('\0').split('\0'));assert staged==set(extra);p.proof['precommit_tree']=p.git('write-tree').decode();p.proof['staged_paths']=len(staged);p.save();p.call('diff','--cached','--check');p.call('commit','-q','-m','research: verify observation count in publication receipt');p.proof['commit']=p.git('rev-parse','HEAD').decode();p.save();p.call('push','git@github.com:shenmuegit/EquiTide.git','HEAD:refs/heads/main');p.call('fetch','git@github.com:shenmuegit/EquiTide.git','refs/heads/main:refs/remotes/origin/main');p.proof['independent_ls_remote']=p.call('ls-remote','--heads','git@github.com:shenmuegit/EquiTide.git');p.save()
 captured=io.StringIO()
 with contextlib.redirect_stdout(captured):p.verify()
 corrected=continuity();assert corrected==check;detail=p.proof['complete_tree_and_evidence_verification'];oldflag=detail['prospective_candidate_continuation_verified'];assert oldflag is False;detail['legacy_count_diagnostic_result']=oldflag;detail['legacy_wrong_constant']=105;detail['prospective_candidate_continuation_verified']=corrected['derived_count_equals_manifest_and_audit'];detail['strict_derived_observation_IDs']=corrected['actual_unique_finished_observation_IDs'];detail['strict_complete_windows']=corrected['actual_complete_windows'];detail['append_only_supplement_artifacts_verified']=len(extra);p.proof['legacy_verifier_original_stdout']=captured.getvalue();p.proof['corrected_dynamic_continuity_check']=corrected;p.save();print(json.dumps(detail),flush=True)
if __name__=='__main__':
 if sys.argv[1]=='check':d=continuity();put(R/'publication_continuity_check.json',d);print(json.dumps(d),flush=True)
 else:
  try:publish()
  except BaseException as error:
   p.proof.setdefault('failures',[]).append({'type':type(error).__name__,'error':str(error)});p.save();raise
