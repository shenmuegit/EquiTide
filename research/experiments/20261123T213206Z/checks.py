"""Check saved actual evidence, all original protected bytes and append-only registration."""
import json,subprocess
from common import *
rd=lambda p:json.loads(p.read_text());ctx=rd(R/'context.json');st=rd(R/'startup.json');p=rd(R/'plan.json');bind=rd(R/'code_binding_before_evaluation.json');assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT) and subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='main';PID=st['branch_lock_broker_pid'];assert any('FLOCK' in l and str(PID) in l.split() for l in Path('/proc/locks').read_text().splitlines())
for path,h in {**bind['source_sha256'],**bind['immutable_source_sha256']}.items():assert sha(ROOT/path)==h,path
for z in rd(R/'readonly_formatter_binding.json')['helpers']:assert sha(ROOT/z)==rd(R/'readonly_formatter_binding.json')['helpers'][z],z
old=subprocess.check_output(['git','show',st['base_commit']+':research/automation/registry.jsonl'],cwd=ROOT);assert (ROOT/'research/automation/registry.jsonl').read_bytes().startswith(old)
protected=ctx['account_hashes_before'];assert all(sha(ROOT/path)==h for path,h in protected.items())
market=[]
for a,xs in p['data']['assets'].items():
 for z in xs:assert sha(ROOT/z['path'])==z['sha256'];market.append({'asset':a,**z})
for z in rd(R/'raw_evidence_index.json')['artifacts']:assert sha(ROOT/z['original_path'])==sha(ROOT/z['committed_copy'])==z['sha256']
for fp,z in p['read_only_references'].items():
 for k in ['spec','report','archive']:assert sha(ROOT/z[k])==z[k+'_sha256']
records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');own={fp:x for fp,x in records.items() if x.get('report','').startswith(rel(R)+'/')};assert len(own)==16
for fp,x in own.items():
 assert x['result_available'] and x['status'] in ['passed','rejected'] and sha(ROOT/x['report'])==x['report_sha256'];ev=[e for e in events if e['fingerprint']==fp];assert len(ev)==2 and ev[0]['status']=='reserved' and ev[1]['status']==x['status']
for c in rd(R/'report.json')['configs'].values():
 ev=next(e for e in events if e['fingerprint']==c['fingerprint'] and e['status']=='reserved');assert ev['recorded_at_utc']<rd(R/'report.json')['evaluation_started_utc']
assert len(events)-ctx['registry_events']==32 and len(records)-ctx['registry_ids']==16
for f in ['verification.json','forward_verification.json','l4h02_verification.json','fewm_verification.json','candidate_verification.json','account_window_verification.json','budget_economic_review.json','export_verification.json','definition_check.json','parent_primitive_verification.json','sizing_primitive_verification.json','boundary_unit_verification.json']:assert rd(R/f)['passed'],f
failed=[]
for f in (R/'command_receipts').glob('*.json'):
 d=rd(f)
 if not d['passed']:failed.append(d['phase']);assert d['phase']=='units'
assert failed==['units'];assert rd(R/'pre_reservation_failure.json')['resolved'] and rd(R/'command_receipts/units_retry.json')['passed']
assert all(rd(R/'command_receipts'/f'{phase}.json')['passed'] for phase in ['prepare','freeze','bind','reserve','evaluate','audit','exports','finish','l4','fewm','candidate','forward','registry','collect'])
assert len(rd(R/'command_receipts/evaluate.json')['commands'])==1 and all(sha(ROOT/p)==h for p,h in rd(R/'original_accounts_binding.json')['sources_sha256'].items())
for f in R.rglob('*'):assert f.name!='__pycache__' and f.suffix not in ['.pyc','.tmp','.npy']
put(R/'data_hashes.json',{'financial_real_market_files':market,'raw_retention_index':rel(R/'raw_evidence_index.json'),'raw_retention_index_sha256':sha(R/'raw_evidence_index.json'),'financial_report_sha256':sha(R/'report.json'),'forward_report_sha256':sha(R/'forward_report.json'),'source_binding_sha256':sha(R/'code_binding_before_evaluation.json')})
put(R/'validation_gate.json',{'passed':True,'recorded_utc':now(),'protected_files_checked':len(protected),'market_files_checked':len(market),'new_finished_IDs':len(own),'append_only_new_events':32,'model_or_completed_account_reruns':0,'original_accounts_and_paper10_protected':True,'financial_and_all_forward_reports_independently_audited':True,'first_attempt_failures_retained_and_recovered':failed,'new_readonly_helpers_bound':True,'report_sha256':sha(R/'report.json'),'own_registry_IDs':list(own)});print(json.dumps({'passed':True,'protected':len(protected),'market':len(market),'own_finished':len(own),'events':len(events),'IDs':len(records),'no_model_replays':True}),flush=True)
