"""Clarify the pending account's text without changing saved results or account state."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'handoff_clarification_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for p,h in b['immutable_reports_and_next_state'].items():assert sha(ROOT/p)==h
p=R/'result.md';s=p.read_text();before=sha(p);changes=[('下轮新增实际资金费首次来源：','下轮candidate待入账的既有首次来源：'),('本轮只读留档，没有提前计入现金流。','本段为下轮candidate保留首次来源，没有提前计入candidate现金流；L4/FEWM已在本轮各自按实际事件记六键。')]
for a,z in changes:assert s.count(a)==1;s=s.replace(a,z)
p.write_text(s)
for path,h in b['immutable_reports_and_next_state'].items():assert sha(ROOT/path)==h
put(R/'handoff_clarification_verification.json',{'passed':True,'descriptive_scope_only':True,'changes':changes,'result_before_sha256':before,'result_after_sha256':sha(p),'all_financial_reports_and_next_state_unchanged':True,'new_model_account_or_cashflow_evaluations':0});print('PASS pending-candidate wording clarified; completed L4/FEWM funding unchanged;0evaluations')
