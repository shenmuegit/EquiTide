"""Record a native driver interruption and readonly audit recovery without executing any model."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'native_recovery_render_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256'] and b['no_new_model_or_account_evaluations']
for p,h in b['immutable_result_sources'].items():assert sha(ROOT/p)==h
initial=rd(R/'native_pipeline_interruption.json');plan=rd(R/'native_recovery_plan.json');assert initial['exit_code']==143 and plan['completed_original_observation_not_replayed']
original=rd(ROOT/plan['original_command_receipt_snapshot']);cur=rd(R/'command_receipts/l4.json');audit=rd(R/'command_receipts/l4_recovery_audit.json');assert len(original['commands'])==1 and original['commands'][0]['exit_code']==0 and cur['commands'][0]==original['commands'][0] and len(cur['commands'])==2 and cur['commands'][1]==audit['commands'][0] and audit['passed'] and cur['passed']
assert cur['commands'][1]['command'][-1].endswith('/audit_l4h02.py') and rd(R/'l4h02_verification.json')['passed'] and b['native_remaining_windows_receipt']['exit_code']==0
for kind in ['report','state','delta']:
 p=R/'l4h02_observation'/(kind+('.json.gz' if kind=='delta' else '.json'));assert sha(p)==plan['L4_completed_hashes'][kind+'_sha256']
for phase in ['fewm','candidate','forward']:assert rd(R/'command_receipts'/(phase+'.json'))['passed']
fail=rd(R/'read_failures.json');assert 'native_runtime_interruptions' not in fail;fail['native_runtime_interruptions']=[{**initial,'known_boundary':plan['proven_boundary'],'termination_origin':plan['termination_origin'],'readonly_L4_audit_recovered':True,'completed_L4_observation_not_replayed':True,'remaining_windows_executed_only_after_initial_driver_stopped':True}];put(R/'read_failures.json',fail)
p=R/'result.md';text=p.read_text();before=sha(p);needle='原生命令非零阶段[]';assert text.count(needle)==1;text=text.replace(needle,'已登记子阶段非零[]，另有外层运行进程143中断');text+='\n原生执行恢复说明：外层进程以143退出，来源未查明。中断时L4实际窗口已完成、三组reserve/finish均返回0且完整报告/状态/账本哈希与原指针一致，因此没有重跑该窗口；仅补做原字节只读审计，然后继续此前未执行的FEWM、candidate和SMA窗口。首次财务报告和L4已完成结果原字节保持。原始143回执、完整边界证据、补审计与后续实际命令均已留档，见native_recovery_verification.json。\n';p.write_text(text)
for path,h in b['immutable_result_sources'].items():assert sha(ROOT/path)==h
put(R/'native_recovery_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':b['source_sha256'],'initial_native_exit_code':143,'termination_origin':plan['termination_origin'],'L4_original_completed_observation_exit_code':0,'L4_original_completed_results_unchanged':True,'readonly_L4_audit_completed':True,'native_remaining_windows_receipt':b['native_remaining_windows_receipt'],'financial_or_completed_account_replays':0,'immutable_results_sha256':b['immutable_result_sources'],'result_before_sha256':before,'result_after_sha256':sha(p),'new_strategy_account_or_cashflow_evaluations':0});print(json.dumps({'passed':True,'native143_preserved':True,'completed_L4_not_replayed':True,'readonly_audit_recovered':True,'new_evaluations':0}))
