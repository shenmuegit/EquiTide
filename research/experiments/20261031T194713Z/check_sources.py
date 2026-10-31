import json,subprocess,hashlib
from common import *
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');batch=json.loads((R/'batch.json').read_text());assert len(batch)==14 and r['frozen_plan_sha256']==sha(R/'plan.json')
for fp,x in p['read_only_references'].items():
 z=records[fp];assert z['result_available'] and z['status']==x['status'] and z['report_sha256']==x['report_sha256']
 for k in ['spec','report','archive']:assert sha(ROOT/x[k])==x[k+'_sha256']
for c in r['configs'].values():
 z=records[c['fingerprint']];assert z['result_available'] and z['status']==c['status'] and z['report_sha256']==sha(R/'report.json') and sha(ROOT/c['archive'])==c['archive_sha256']
base=json.loads((R/'startup.json').read_text())['base_commit'];prefix=subprocess.check_output(['git','show',base+':research/automation/registry.jsonl'],cwd=ROOT);raw=(ROOT/'research/automation/registry.jsonl').read_bytes();assert raw.startswith(prefix) and hashlib.sha256(prefix).hexdigest()==ctx['main_registry_sha256_before_reserve'];events=[json.loads(x) for x in raw[len(prefix):].splitlines()];allrows=batch+json.loads((R/'forward_batch.json').read_text())+json.loads((R/'candidate_batch.json').read_text());assert len(allrows)==20 and len(events)==40 and {x['fingerprint'] for x in events}=={x['fingerprint'] for x in allrows}
for row in allrows:
 es=[x for x in events if x['fingerprint']==row['fingerprint']];assert len(es)==2 and es[0]['status']=='reserved' and es[-1]['result_available'] is True and es[-1]['status'] in ['passed','rejected']
 if row in batch:assert es[0]['recorded_at_utc']<r['evaluation_started_utc']<es[-1]['recorded_at_utc']
for path,h in ctx['account_hashes_before'].items():assert sha(ROOT/path)==h,path
for path,h in json.loads((R/'code_binding_before_evaluation.json').read_text())['source_sha256'].items():assert sha(ROOT/path)==h,path
res=[x for f in (R/'reserve_batches').glob('*.json') for x in json.loads(f.read_text())['actual_command_receipts']];fin=[x for f in (R/'finish_batches').glob('*.json') for x in json.loads(f.read_text())['actual_command_receipts']];assert len(res)==len(fin)==14 and all(x['exit_code']==0 for x in res+fin)
put(R/'source_verification.json',{'passed':True,'new_actual_financial_configs':14,'new_candidates':14,'new_matched_hold_controls':0,'new_benchmarks':0,'old_source_results_unchanged':len(p['read_only_references']),'new_finished_IDs':20,'registry_append_only_events':40,'actual_reserve_receipts':14,'actual_finish_exit0_receipts':14,'all_financial_reservations_precede_first_valuation':True,'protected_files_unchanged':len(ctx['account_hashes_before']),'original_code_binding_preserved':True,'financial_report_sha256':sha(R/'report.json')});print('PASS14financial+6observations/40append events;originalsource/account/code bytes unchanged')
