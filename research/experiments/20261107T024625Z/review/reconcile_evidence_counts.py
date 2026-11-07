"""Reconcile a saved display counter with already finished report/audit; no valuation."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
assert not (R/'data_manifest.json').exists() and not(R/'evidence_count_reconciliation.json').exists()
binding=rd(R/'code_binding_before_evaluation.json')
for path,h in {**binding['source_sha256'],**binding['immutable_source_sha256']}.items():assert sha(ROOT/path)==h,path
reports=[R/'report.json',R/'forward_report.json']+[R/(s+'_observation/report.json') for s in ['candidate','l4h02','fewm']];before={str(p.relative_to(ROOT)):sha(p) for p in reports}
rep=rd(R/'report.json');audit=rd(R/'verification.json');plan=rd(R/'plan.json');original=rd(R/'research_evidence_counts.json');actual=0
for c in rep['configs'].values():
 assert c['scope']=='parent' and sha(ROOT/c['archive'])==c['archive_sha256'];arc=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()))
 assert arc['fingerprint']==c['fingerprint'] and set(arc['scenes'])=={'1','2','3'}
 for k,z in arc['scenes'].items():assert z['summary']==c['scenes'][k];actual+=1
assert len(rep['configs'])==15 and actual==45==audit['new_parent_curves']==plan['expected_counts']['new_cost_scenes']==rep['summary']['new_cost_scenes']
assert original['new_parent_cost_curves']==36 and original['new_aligned_parent_NAV_points']==audit['new_NAV_points']==sum(s['NAV_points'] for c in rep['configs'].values() for s in c['scenes'].values())
archive=R/'research_evidence_counts_original.json';assert not archive.exists();shutil.copyfile(R/'research_evidence_counts.json',archive)
corrected=dict(original);corrected['new_parent_cost_curves']=actual;corrected['scope']='Old42costledgers readonly,zero newnativepolicy/order/valuation calls.45newalignedwholebankparentNAVcurves actually valued in alreadyfinished report and independentlyaudited. Metadata count reconciled from15savedarchives x3,not a newevaluation orsource-policy rerun.'
put(R/'research_evidence_counts.json',corrected)
changed={k for k in original if original[k]!=corrected[k]};assert changed=={'new_parent_cost_curves','scope'} and before=={str(p.relative_to(ROOT)):sha(p) for p in reports}
put(R/'evidence_count_reconciliation.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'actual_original_saved_curve_count':36,'actual_finished_and_independently_audited_curve_count':actual,'saved_parent_archives_verified':15,'changed_metadata_fields':sorted(changed),'original_output_snapshot':str(archive.relative_to(ROOT)),'original_output_sha256':sha(archive),'corrected_output_sha256':sha(R/'research_evidence_counts.json'),'bound_count_source_preserved_sha256':sha(R/'count_evidence.py'),'root_cause':'Legacy count_evidence.py display counter andscope used literal36;actual15configs x3 archives andaudit45 were already correct. Preserve executed bound source andoriginal output;reconcile summary only.','five_finished_reports_sha256_unchanged':before,'all36_bound_sources_unchanged':True,'market_or_policy_calculations':0,'completed_backtest_or_observation_reruns':0,'no_qualification_gate_or_status_change':True})
print(json.dumps({'passed':True,'corrected_metadata_counter':actual,'old_literal_preserved':36,'actual_new_financial_evaluations':0,'finished_reports_unchanged':True}),flush=True)
