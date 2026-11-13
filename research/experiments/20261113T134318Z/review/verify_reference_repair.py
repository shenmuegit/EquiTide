"""Verify the pre-reservation reference-table repair and retain actual failures."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());old=rd(R/'plan_before_reference_fix.json');new=rd(R/'plan.json');strip=lambda x:{k:v for k,v in x.items() if k not in ['read_only_references','frozen_at_utc']};assert strip(old)==strip(new) and len(new['read_only_references'])==8
assert not (R/'report.json').exists() and not (R/'reserve_batches').exists();receipts=rd(R/'bind_retry1_commands.json');assert all(z['exit_code']==0 for z in receipts) and rd(R/'definition_check.json')['passed']
facts=rd(R/'read_failures.json');resolved=0
for z in facts['facts']:
 if z.get('kind')=='definition_reference_table_missing' or z.get('log')==rel(R/'bind.log'):
  z.update(resolved=True,successful_bind_receipt=rel(R/'bind_retry1_commands.json'),successful_freeze_receipt=rel(R/'freeze_retry1_commands.json'),financial_rules_parameters_axes_boundaries_and_failure_gates_unchanged=True,completed_model_or_account_window_reruns=0);resolved+=1
assert resolved==2
facts['facts'].append({'kind':'readonly_reference_repair_summary_schema_error','native_completion_chunk':'08c46b','exit_code':1,'error':'Initial summary assumed every preserved failure dict had kind;original command receipt uses log/command fields. Failed before writing any file.','resolved':True,'repair':'This verifier uses optional kind and exact original bind.log matching; financial and account results untouched.','successful_native_receipt':rel(R/'review/native_verify_reference_repair.py_receipt.json')});put(R/'read_failures.json',facts)
put(R/'definition_reference_repair.json',{'passed':True,'verified_utc':now(),'old_plan':rel(R/'plan_before_reference_fix.json'),'old_plan_sha256':sha(R/'plan_before_reference_fix.json'),'new_plan_sha256':sha(R/'plan.json'),'only_added_reference_table_and_new_pre_reservation_timestamp':True,'all_financial_parameters_rules_boundaries_and_gates_identical':True,'original_failed_bind_receipt':rel(R/'bind_commands.json'),'successful_bind_receipt':rel(R/'bind_retry1_commands.json'),'successful_source_sha256':sha(Path(__file__)),'actual_summary_schema_failure_preserved':True,'no_financial_model_or_account_window_rerun':True})
f=R/'finalize.py';s=f.read_text().replace("'component_attribution.json']","'component_attribution.json','definition_reference_repair.json']").replace("'reporting_setup.py','attribution.py'","'reporting_setup.py','verify_reference_repair.py','attribution.py'");f.write_text(s)
f=R/'collect.py';s=f.read_text();needle="(R/'result.md').write_text('\\n'.join(lines)+'\\n')";assert needle in s;s=s.replace(needle,"lines += ['', '实际失败留档：初始计划漏写read_only_references，bind在策略预登记/金融及账户计算前KeyError停止；原源码、plan/spec及exit1保留。补入8项精确已完成引用后重做freeze/bind通过，逐字段核对仅新增引用表及预登记前时间戳，规则/参数/轴/边界/判据不变。只读修复摘要首轮假定失败字典均有kind，已保留错误并按原bind.log修正匹配；无金融或账户重跑。']\n"+needle);f.write_text(s)
print('PASS exact references repaired before financial reservation;all parameters/gates/boundaries unchanged;initial failures retained')
