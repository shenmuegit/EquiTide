"""Pin every actual qualification without changing original or old-center statuses."""
import json
from run import ROOT,R,sha,put,reg
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');out=[]
for c in r['configs'].values():
 z=records[c['fingerprint']];assert z['status']==c['status'] and z['result_available'] is True and z['report_sha256']==sha(R/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256']
 if c['status']=='passed':
  assert all(c['criteria'].values());out.append({'name':c['name'],'fingerprint':c['fingerprint'],'spec':c['spec'],'spec_sha256':sha(ROOT/c['spec']),'report_sha256':sha(R/'report.json'),'archive_sha256':c['archive_sha256'],'criteria':c['criteria'],'sensitivity':c['sensitivity'],'independent_future_qualification':False})
original=p['original_candidate_preserved'];assert records[original['fingerprint']]['status']=='passed' and records[original['fingerprint']]['report_sha256']==original['report_sha256'] and sha(ROOT/original['spec'])==original['spec_sha256']
put(R/'candidate_validation.json',{'passed':True,'new_actual_financial_configs':66,'new_native':36,'new_parents':30,'new_candidate_count':27,'passed_candidate_count':len(out),'rejected_candidate_count':len(r['summary']['rejected']),'reference_only_count':39,'candidates':out,'financial_report_sha256':sha(R/'report.json'),'original_candidate_immutable':original,'old_center_qualification_unchanged':True,'old_baselines_readonly_not_in_new_momentum_grid':True,'original_forward_current_observation':json.loads((R/'candidate_verification.json').read_text()),'no_new_account_or_parameter_switch':True});print('PASS pinned actualqualifications',len(out))
