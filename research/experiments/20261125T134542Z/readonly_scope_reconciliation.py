"""Correct inherited descriptive scope only; preserve all account and financial evidence."""
import copy,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'scope_reconciliation_binding.json');assert b['bound_before_readonly_execution'] and b['new_financial_account_or_cashflow_evaluations']==0 and sha(Path(__file__))==b['source_sha256']
for p,h in b['immutable_reports_sha256'].items():assert sha(ROOT/p)==h
path=R/'next_research_state.json';assert sha(path)==b['next_state_before_sha256'];before=rd(path);after=copy.deepcopy(before);h=after['UTC_midnight_handoff'];counts=rd(R/'account_window_verification.json')['current_funding_records_by_account'];assert counts=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0} and counts==h['current_funding_records_by_account']
old=h['rules'];assert 'candidate books six own actual16 records' in old
h['rules']='Current all4 daily0/fills0/funding0: each original account appends only closed marks; cash,quantity,desired and execution costs remain unchanged. All3 original perps already booked each of the five known actual funding sources exactly once (six own asset/cost keys per source);do not repeat Nov24_16 or any earlier source. Next pending='+str(h['next_new_actual_funding_pending_by_own_window'])+';refresh fresh exact public funding timestamps and each own chain before any next reserve;no reset,adoption,paper changes or forced close.'
x=copy.deepcopy(after);x['UTC_midnight_handoff']['rules']=old;assert x==before;put(path,after)
for p,v in b['immutable_reports_sha256'].items():assert sha(ROOT/p)==v
put(R/'scope_reconciliation_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':b['source_sha256'],'descriptive_field_only':'next_research_state.UTC_midnight_handoff.rules','old_description':old,'current_description':h['rules'],'next_state_before_sha256':b['next_state_before_sha256'],'next_state_after_sha256':sha(path),'all_other_JSON_values_unchanged':True,'account_reports_states_ledgers_and_financial_report_unchanged':b['immutable_reports_sha256'],'new_strategy_account_or_cashflow_evaluations':0,'reason':'Inherited narrative referred to the previous window; actual current counts were already correctly zero in the saved state and audits. Correct the prose without replaying any model or account.'});print(json.dumps({'passed':True,'descriptive_field_corrected':True,'actual_counts_unchanged':counts,'new_evaluations':0}))
