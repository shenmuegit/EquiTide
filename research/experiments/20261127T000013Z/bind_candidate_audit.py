"""Bind saved candidate inputs for its preplanned first completed-month audit; no account execution."""
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rel=lambda p:str(p.relative_to(ROOT));rd=lambda p:json.loads(p.read_text());put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
plan=rd(R/'candidate_completed_fold_audit_plan.json');assert plan['planned_before_any_reserve'] and plan['route_from_first_readonly_audit_attempt'];assert not(R/'candidate_30day_recovery_binding.json').exists() and not(R/'candidate_verification.json').exists()
source=R/'audit_candidate_30day_recovery.py';old=R/'audit_incremental.py';assert sha(source)==plan['planned_source_sha256'] and sha(old)==plan['unchanged_original_auditor_sha256']
t=old.read_text();assert t.count("len(z['folds'])==0")==1 and t.count("'complete30day_folds':0")==1
adapted=t.replace("len(z['folds'])==0","len(z['folds'])==_verify_completed_folds(z,full,daily,a,k,c.START,cut,c.DAY,c.END)").replace("'complete30day_folds':0","'complete30day_folds':min(6,(cut-c.START)//(30*c.DAY))")
(R/'candidate_30day_adapted_auditor.py.txt').write_text(adapted)
paths=[R/'report.json',R/'code_binding_before_evaluation.json',old,ROOT/'research/automation/registry.jsonl',ROOT/'research/automation/candidate_forward_latest.json',*[R/'candidate_observation'/n for n in ['state.json','report.json','delta.json.gz','complete.json','previous_pointer.json','input_manifest.json']]]
rep=rd(R/'candidate_observation/report.json');assert all(len(s['folds'])==1 for c in rep['configs'].values() for s in c['scenes'].values())
put(R/'candidate_30day_recovery_binding.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),'bound_before_readonly_execution':True,'planned_first_readonly_audit_attempt':True,'source':rel(source),'source_sha256':sha(source),'previous_auditor':rel(old),'previous_auditor_sha256':sha(old),'adapted_auditor_sha256':hashlib.sha256(adapted.encode()).hexdigest(),'immutable_inputs_sha256':{rel(q):sha(q) for q in paths},'scope':'First-attempt read-only completed30dayfold verification;original observer executed once,no monetary or prior-file changes.'})
print('PASS fresh completed candidate fold binding before first readonly audit; no model/window execution')
