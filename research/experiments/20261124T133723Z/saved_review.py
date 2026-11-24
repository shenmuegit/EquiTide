"""Read frozen saved evidence and distinguish matched controls from all known NAV aliases."""
import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bind=rd(R/'saved_review_binding.json');assert sha(Path(__file__))==bind['source_sha256'];p=rd(R/'plan.json');r=rd(R/'report.json');aliases=rd(R/'NAV_alias_inventory.json');eco=rd(R/'joint_economic_review.json');first=rd(R/'verification.json')['report_sha256'];sma=rd(R/'forward_verification.json')['report_sha256']
assert sha(R/'report.json')==first and sha(R/'forward_report.json')==sma and aliases['passed'] and eco['passed'] and p['representative_preset']=={'W':.0275,'K':2} and len(r['configs'])==2
rep=next(c for c in r['configs'].values() if c['W']==.0275 and c['K']==2);assert rep['raw_weights']==[1,1] and rep['capital_usdt']==18750 and (rep['NB'],rep['NE'])==(1000,4000)
alias_definitions=sum(len(z['new_names']) for z in aliases['groups'] if z['old_fingerprints']);distinct=len(aliases['groups']);warnings=len(rd(R/'export_verification.json')['cliffs_over_two_std']);ss=rep['scenes'];h=rd(R/'next_research_state.json')['UTC_midnight_handoff']
assert all(h['actual_Nov23_16_counts_by_account'][a]['1795449600000000000']==6 for a in ['candidate','l4h02','fewm'])
before=sha(R/'result.md');text=(R/'result.md').read_text();text+='\n## 保存结果的独立汇总\n\n'
text+=f"事前代表BTC H.0275/ETH D2的1/2/3倍成本净收益为{ss['1']['net_return_pct']:.8f}%/{ss['2']['net_return_pct']:.8f}%/{ss['3']['net_return_pct']:.8f}%，3倍完整连续OOS最大回撤{ss['3']['max_drawdown_pct']:.8f}%。{len(r['configs'])}个新定义对应{distinct}条不同全成本净值路径；与全部16个预声明旧结果比对，有{alias_definitions}个新定义的净值已见于旧配置，不能当作新独立收益证据。该范围不同于同ETH斜率滞后BTC H.03对照；后者的净值别名图数为{eco['allcost_path_alias_new_graphs']}、全成本四指标改善行数{eco['strict_four_metric_improvement_rows']}。中心旧组合弱支配{eco['central_old_dominates_rows']}条成本行。\n\n"
text+=f"敏感性保留{warnings}条相邻边警告；passed仅表示冻结历史绝对门槛通过，不能改称独立未来验证、参数已证明稳健或实盘稳定盈利。没有升级候选，代表和网格未按结果重选或扩展。BTC和ETH机制比较均只使用真实存在的已保存policy字段；没有把缺失可选字段填成0。\n\n"
text+='原资金费16事件现在candidate、L4、FEWM各六个唯一资产/成本键，08也各六，不能重复。下一窗口待处理事件来自新鲜完整实际查询及自身覆盖，先核对首次源SHA、原UTC和真实time/rate/mark再reserve；不推定名义结算时刻、不提前记账。\n'
(R/'result.md').write_text(text);assert sha(R/'report.json')==first and sha(R/'forward_report.json')==sma
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'financial_report_sha256_unchanged':first,'SMA_report_sha256_unchanged':sma,'new_definitions':len(r['configs']),'distinct_allcost_NAV_paths':distinct,'new_definitions_seen_in_all_predeclared_old_results':alias_definitions,'matched_control_alias_scope_distinguished':True,'representative_preset':p['representative_preset'],'representative_3x_net_pct':ss['3']['net_return_pct'],'representative_whole_OOS_DD3_pct':ss['3']['max_drawdown_pct'],'sensitivity_warnings':warnings,'result_before_sha256':before,'result_after_sha256':sha(R/'result.md'),'new_strategy_or_account_evaluations':0};(R/'saved_result_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
