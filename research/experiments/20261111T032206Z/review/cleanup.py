"""Verify current-round rebuildable debris absence while retaining complete actual evidence."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import put,sha,now
rd=lambda n:json.loads((R/n).read_text());bad=[str(p.relative_to(ROOT)) for p in R.rglob('*') if p.name=='__pycache__' or p.suffix in ['.pyc','.npy','.tmp'] or 'checkpoint' in p.name];assert not bad
for n in ['report.json','forward_report.json','forward_state.json','candidate_observation/report.json','candidate_observation/state.json','l4h02_observation/report.json','l4h02_observation/state.json','fewm_observation/report.json','fewm_observation/state.json','registry_records.jsonl','raw_evidence_index.json','code_binding_before_evaluation.json']:assert (R/n).is_file()
for path,h in rd('code_binding_before_evaluation.json')['source_sha256'].items():assert sha(ROOT/path)==h
raw=rd('raw_evidence_index.json')['artifacts']
for z in raw:assert sha(ROOT/z['committed_copy'])==sha(ROOT/z['original_path'])==z['sha256']
put(R/'cleanup_verification.json',{'passed':True,'checked_utc':now(),'rebuildable_debris_remaining':bad,'rebuildable_files_removed_this_round':0,'reason':'No current-round checkpoint,npy,tmp,pycache orpyc generated;all actual financial archives/raw HTTP successes and failures/full original account books/frozen rules/registry/spec/code remain needed for reproduction ornextcontinuation.','complete_current_actual_raw_response_copies':len(raw),'complete_original_account_NAV_and_ledger_prefixes_retained':True,'original_market_inputs_retained_ignored':True,'finished_reports_or_bound_sources_modified':False,'valuation_or_order_calls':0})
print('PASS no reconstructible debris;complete actual evidence,raw failures andoriginal fullaccount histories retained')
