"""Final readonly checks with one preserved metadata-binding failure, no financial/account execution."""
from pathlib import Path
import ast,hashlib,json
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,o:p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'readonly_metadata_recovery/checker_binding.json');assert b['bound_before_execution'] and sha(Path(__file__))==b['source_sha256'];old=R/'checks.py';assert sha(old)==b['original_checker_sha256']==rd(R/'code_binding_before_evaluation.json')['source_sha256'][str(old.relative_to(ROOT))]
rec=rd(R/'readonly_metadata_recovery/verification.json');assert rec['passed'] and rec['new_financial_or_account_evaluations']==0
for path,h in rec['unchanged_evidence_sha256'].items():assert sha(ROOT/path)==h,path
bad=rd(R/'command_receipts/next_params.json');good=rd(R/'command_receipts/next_params_recovered.json');assert not bad['passed'] and good['passed'] and [z['exit_code'] for z in bad['commands']]==[1] and [z['exit_code'] for z in good['commands']]==[0]
assert "KeyError: 'new_financial_account_or_cashflow_evaluations'" in (ROOT/bad['commands'][0]['log']).read_text()
t=old.read_text();assert t.count('assert not failed,failed')==1 and t.count("'no_nonzero_native_phases':True")==1
t=t.replace('assert not failed,failed',"assert failed==['next_params'],failed").replace("'no_nonzero_native_phases':True","'no_nonzero_native_phases':False")
ast.parse(t);exec(compile(t,str(old)+'[metadata_recovery]','exec'),{'__name__':'__main__','__file__':str(old)})
gate=rd(R/'validation_gate.json');assert gate['passed'] and gate['nonzero_native_phases']==['next_params'] and not gate['no_nonzero_native_phases'];gate.update(effective_native_failures=[],all_actual_native_attempts_zero_exit=False,known_readonly_binding_failure_recovered=True,original_failed_receipt='command_receipts/next_params.json',effective_readonly_receipt='command_receipts/next_params_recovered.json',readonly_recovery_verification='readonly_metadata_recovery/verification.json',original_checker_unchanged=True,new_financial_or_account_evaluations_from_adapter=0);put(R/'validation_gate.json',gate)
for path,h in rec['unchanged_evidence_sha256'].items():assert sha(ROOT/path)==h,path
print('PASS all original checks and protected inputs; original next_params exit1 retained, corrected readonly retry exit0; financial/account reruns0')
