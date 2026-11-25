"""Append truthful engineering/read-only limitations without changing any financial evidence."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();put=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
b=rd(R/'complete_evidence_review_binding.json');assert b['bound_before_readonly_execution'] and sha(Path(__file__))==b['source_sha256']
for path,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/path)==h
aw=rd(R/'account_window_verification.json');assert aw['passed'] and aw['current_funding_records_by_account']=={'SMA':0,'candidate':6,'l4h02':0,'fewm':0}
h=rd(R/'next_research_state.json')['UTC_midnight_handoff'];assert all(d=='2026-11-26T00:01:00Z' for d in h['next_daily_decision_by_account'].values())
assert all(n==6 for n in aw['actualNov25_00_unique_counts'].values()) and all(n==6 for n in aw['actualNov25_00_daily_once_counts'].values())
assert rd(R/'pre_reserve_inspection_failure.json')['facts'][0]['reserves_or_evaluations']==0 and rd(R/'readonly_inspection_failure.json')['writes_or_new_model_calculations']==0
before=sha(R/'result.md');text=(R/'result.md').read_text();text+='\n工程与只读检查留档：预登记适配曾因旧图表标签匹配 guard 退出1，所有适配仍在内存，未写源码、未登记或计算；另一次只读报告打印命令有括号语法错误，退出1，未写文件或计算。两次原始失败分别见 pre_reserve_inspection_failure.json 与 readonly_inspection_failure.json。boundary_units 的旧轮次 PASS 文字已用 boundary_output_prose_note.json 澄清，实际断言及 JSON 从首次执行起就是本轮 SMA/C 日决策各1、candidate资金费6、L4/FEWM两项均0。财务报告、账户结果和冻结源码均未因这些说明而重写。\n'
text+='\n本轮独立账本审计确认：三永续原账户在实际 Nov25_00:00:00.003 结算各累计六唯一键，在原 Nov25_00:01 日决策各累计六唯一键；candidate本轮补齐，L4/FEWM上轮已完成且本轮未重复。SMA本轮使用新77天真实SPOT背景和原始Float日决策算术。下一窗口模式必须以已保存的实际资金费查询及原日决策日期为准；SMA标记适配必须重绑当前full77和旧full76前缀，未来Nov26原日决策另需full78。现有收益来自反复研究的历史/延迟shadow，不是未触碰最终测试或稳定实盘盈利。\n'
(R/'result.md').write_text(text)
for path,h in b['immutable_inputs_sha256'].items():assert sha(ROOT/path)==h
put(R/'complete_evidence_review_verification.json',{'passed':True,'source_sha256':b['source_sha256'],'all_financial_reports_and_next_state_unchanged':True,'actual_native_inspection_failures_preserved':[1,1],'new_strategy_account_or_cashflow_evaluations':0,'result_before_sha256':before,'result_after_sha256':sha(R/'result.md')});print('PASS original first reports/next-state unchanged; actual engineering failures and completed own-book midnight once counts clarified')
