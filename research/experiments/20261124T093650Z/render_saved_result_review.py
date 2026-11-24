"""Review only finished, source-bound results and render the diagnostic correction."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=rd(R/'saved_review_binding.json');assert sha(Path(__file__))==b['source_sha256']
r=rd(R/'report.json');p=rd(R/'plan.json');e=rd(R/'joint_economic_review.json');corr=rd(R/'confirmation_diagnostic_correction.json');aw=rd(R/'account_window_verification.json');h=rd(R/'next_research_state.json')['UTC_midnight_handoff']
first=rd(R/'verification.json')['report_sha256'];sma=rd(R/'forward_verification.json')['report_sha256'];assert sha(R/'report.json')==first and sha(R/'forward_report.json')==sma
assert p['axes']=={'BTC_CONFIRMATION_HURDLE':[0,.0025,.005],'ETH_TREND_STRENGTH':[.00625,.0075,.00875]} and p['representative_preset']=={'W':0,'K':.0075}
assert len(r['configs'])==6 and len(r['all_current_grid'])==9
for c in r['configs'].values():
 assert c['W'] in [0,.005] and c['K'] in [.00625,.0075,.00875] and c['raw_weights']==[1,1] and c['capital_usdt']==18750 and (c['NB'],c['NE'])==(1000,4000)
assert corr['passed'] and corr['superseded_review_sha256']==sha(R/'joint_economic_review.json') and corr['financial_report_sha256_unchanged']==first
assert h['actual_Nov23_16_counts_by_account']=={a:{'1795449600000000000':n} for a,n in [('candidate',0),('l4h02',6),('fewm',6)]}
assert h['next_new_actual_funding_pending_by_own_window']=={'SMA':0,'candidate':6,'l4h02':0,'fewm':0}
assert rd(R/'next_funding_handoff_verification.json')['passed'] and all(v['new_daily_events']==0 and v['new_fills']==0 for v in aw['accounts'].values())
rep=next(c for c in r['configs'].values() if c['W']==0 and c['K']==.0075);ss=rep['scenes'];cliffs=rd(R/'export_verification.json')['cliffs_over_two_std']
before=sha(R/'result.md');text=(R/'result.md').read_text()
text+='\n## 保存结果独立审阅补充\n\n'
text+=f"事前代表Q0/K.0075，1/2/3倍成本净收益分别为{ss['1']['net_return_pct']:.8f}%/{ss['2']['net_return_pct']:.8f}%/{ss['3']['net_return_pct']:.8f}%，3倍完整连续OOS回撤{ss['3']['max_drawdown_pct']:.8f}%。六个新定义形成四条不同的全成本净值路径，其中三个定义与事前同ETH趋势强度旧Q.0025对照完全相同；其余更低，四指标联合改善0条。敏感性{len(cliffs)}条相邻边警告完整保留，不能把历史门槛passed称为参数稳健或新独立alpha；没有升级候选。\n\n"
text+='旧只读joint_economic_review中的BTC confirmation_block_flag_changes列读取不存在的可选字段，原0值无效；其余实际金额、方向和对照均不变。该列由confirmation_diagnostic_correction.json和exports/confirmation_block_flags_corrected.csv替代：严格Fraction ROC/门槛、实际confirmation_applied及最终desired逐决策核对，Q0相对Q.0025每成本有4次拦截状态不同、5次最终desired不同、增加1次往返，Q.005与Q.0025各成本相同。原错误列与更正来源均保留，未改首次金融报告或重跑策略。\n\n'
text+='当前16事件独立账本计数candidate0、L4六、FEWM六。下一candidate14:30→16:30覆盖16，下一L4/FEWM16:10→18:10不覆盖16；不得把三个账户一律重记或要求已记账户的旧计数为0。保留首次源SHA和原始2026-11-24T08:05:12.897402Z，任何下轮reserve之前都要重新核对真实timestamp/rate/mark和各自唯一键。旧08事件三个账户均各六，不得重复。\n\n'
text+='准备阶段的真实缩进失败及旧轴/预期资金费断言失败均发生在reserve和回测前，失败源与实际退出回执保留；修复后units_retry通过。有效发布与清理程序为current_seal_procedure.py、current_publish_procedure.py、current_postrelease_procedure.py；其余同名旧程序只为保留预先绑定的源字节，未执行。\n'
(R/'result.md').write_text(text)
assert sha(R/'report.json')==first and sha(R/'forward_report.json')==sma
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'financial_report_sha256':first,'SMA_report_sha256':sma,'source_binding':'saved_review_binding.json','new_definitions':6,'new_distinct_allcost_paths':4,'old_matched_alias_definitions':e['allcost_path_alias_new_graphs'],'strict_four_metric_improvement_cost_rows':e['strict_four_metric_improvement_rows'],'sensitivity_cliff_warnings':len(cliffs),'representative_preset':p['representative_preset'],'representative_3x':ss['3'],'result_before_sha256':before,'result_after_sha256':sha(R/'result.md'),'new_financial_or_account_calculations':0,'frozen_rules_and_first_financial_report_unchanged':True}
(R/'saved_result_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'representative_3x_net_pct':ss['3']['net_return_pct'],'representative_whole_OOS_DD3_pct':ss['3']['max_drawdown_pct'],'cliffs':len(cliffs),'first_reports_unchanged':True}))
