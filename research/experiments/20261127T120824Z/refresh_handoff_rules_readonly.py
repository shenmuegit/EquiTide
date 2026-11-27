"""Refresh inherited descriptive handoff prose from completed current evidence only."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'handoff_rules_refresh_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for s,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/s)==h
path=R/'next_research_state.json';before=rd(path);assert sha(path)==b['next_state_before_sha256'];after=copy.deepcopy(before);h=after['UTC_midnight_handoff'];w=rd(R/'account_windows.json');lookup=rd(R/'next_window_funding_lookup.json');aw=rd(R/'account_window_verification.json');assert lookup['passed'] and aw['passed']
assert {x['asset'] for x in lookup['HTTP_receipts'] if x['http_status']==200 and x['curl_exit_code']==0}=={'BTC','ETH'}
assert aw['current_funding_records_by_account']=={'SMA':0,'candidate':6,'l4h02':0,'fewm':0} and aw['actualNov26_16_unique_counts']==dict.fromkeys(['candidate','l4h02','fewm'],6)
old=h['rules'];h['rules']=w['rules']+' Current complete BTC/ETH funding preflight and current completed-account chain checks passed. All11 known sources are now booked exactly6 unique asset-cost keys per originalperp. Next pending='+str(lookup['own_next_window_pending_counts'])+' from actual complete next-window BTC/ETH HTTP200 query;refresh both assets before any next reserve.'
assert 'Future ETH query incomplete' in old and 'Future ETH query incomplete' not in h['rules'];check=copy.deepcopy(after);check['UTC_midnight_handoff']['rules']=old;assert check==before
put(path,after)
for s,x in b['immutable_inputs_sha256'].items():assert sha(ROOT/s)==x
put(R/'handoff_rules_refresh_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_binding':'handoff_rules_refresh_binding.json','scope':'Only current descriptive handoff rules replaced;all prior-round artifacts and original failed receipts preserved.','old_inherited_prose_preserved':old,'current_rules':h['rules'],'next_state_before_sha256':b['next_state_before_sha256'],'next_state_after_sha256':sha(path),'all_other_current_next_state_fields_unchanged':True,'financial_report_sha256_unchanged':sha(R/'report.json'),'SMA_report_sha256_unchanged':sha(R/'forward_report.json'),'current_original_account_artifacts_unchanged':True,'new_strategy_account_or_cashflow_evaluations':0})
print('PASS current handoff descriptive rules refreshed from actual completed queries;no strategy/account/cashflow execution')
