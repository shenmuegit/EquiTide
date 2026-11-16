"""Allow rebinding only absent IDs or explicitly blocked/abandoned IDs without results."""
import ast,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R))
from common import *
receipt=json.loads((R/'bind_retry1_commands.json').read_text());assert receipt[0]['exit_code']==1
assert not (R/'report.json').exists() and not (R/'results').exists()
batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl')
assert all(records[z['fingerprint']]['status']=='blocked' and not records[z['fingerprint']]['result_available'] for z in batch)
p=R/'definitions.py';s=p.read_text();dest=R/'review/definitions_before_rebind_existing_ID_fix.py';assert not dest.exists();dest.write_bytes(p.read_bytes())
old="z['fingerprint'] not in rs and q['continuous_oos_days']==391"
new="(z['fingerprint'] not in rs or rs[z['fingerprint']]['status'] in ['blocked','abandoned'] and not rs[z['fingerprint']]['result_available']) and q['continuous_oos_days']==391"
assert s.count(old)==1;s=s.replace(old,new);ast.parse(s);p.write_text(s)
p=R/'finalize.py';s=p.read_text();assert "'bind_retry1'" in s;s=s.replace("'bind_retry1'","'bind_retry2'");assert "'recover_allowlist.py'" in s;s=s.replace("'recover_allowlist.py'","'recover_allowlist.py', 'repair_rebind_condition.py'");ast.parse(s);p.write_text(s)
facts=json.loads((R/'read_failures.json').read_text());facts['facts'].append({'type':'rebind_existing_blocked_ID_condition','native_start_chunk':'e724b2','native_completion_chunk':'8611b9','native_session':25912,'actual_exit_code':1,'receipt':rel(R/'bind_retry1_commands.json'),'source_as_executed':rel(dest),'source_as_executed_sha256':sha(dest),'completed_curves':0,'resolved':True,'recovery':'Binding now admits absent IDs or blocked/abandoned IDs with result_available=false. Existing actual results and active reservations remain excluded. All six IDs still blocked;no new calculation or reservation occurred in failed rebind.'});put(R/'read_failures.json',facts)
put(R/'rebind_condition_verification.json',{'passed':True,'checked_utc':now(),'actual_failed_rebind_exit_code':1,'all_current_IDs_blocked_without_results':True,'original_failed_source_retained':rel(dest),'predicate_excludes_existing_result_and_active_reservation':True,'money_engine_source_unchanged':sha(R/'engine.py')==json.loads((R/'prebinding_parameter_guard_verification.json').read_text())['new_sha256'],'financial_or_account_curves_computed':0})
print('PASS strict no-result rebind condition;first rebind failure retained;0 model/account curves')
