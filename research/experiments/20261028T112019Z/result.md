# 20261028T112019Z ETH相邻慢周期多数表决的原生与组合验证

实际计算6个新ETH原生＋6个BTC/ETH组合，共12配置/36成本场景；历史通过2、淘汰10。完整读取20980登记事件/10386ID、215份结论；初始16项均有实际证据。

针对前轮慢28日近期资格孤立于27/29日的问题，事前固定新规则：ETH快ROC L3/4，阈值2.5%、零交叉退出；S27/28/29中心各取S−1/S/S+1三个慢ROC，至少两票严格正允许多、至少两票严格负允许空，其他平仓。快反转方向与慢多数方向一致才持仓；现金须新严格极端入场，无隐藏desired，不新建三个并行ETH订单。S和L二维6格/作用域、7相邻边/作用域，新多数规则自身邻域用于资格；12旧单S对照保持原结果与状态，不混入新规则邻域。

新ETH银行10000USDT、固定入场3000。BTC固定ROC31/H4%/退出1%、银行10000、入场1000；父层原值1/1代表两个完整独立银行，本金20000、入场预算4000=初始父本金20%。不归一化、不复利调仓、不转账/交叉保证金/再平衡/现金利息。8旧原生/24成本NAV按实际现金/数量/entry分段恢复并核对SHA；新6原生实际执行专属成交/成本/资金费/风险，新6组合按共同(ns,eventcode)轴因果承接上一完成NAV再逐点相加，不平均收益/Sharpe/回撤或缩放其他金额结果。

UTC00:01实际OPEN执行，信号与q=floor(N/前一完整close/lot)*lot只读此前已闭合信息。先平不兼容持仓后按新极端开仓；同方向保留实际数量。TDD先观察旧单S在“两邻负/中心正”例子中不能开空，再验证新规则、镜像开多、零票、带内现金不入场、实际持仓保留、零退出、精确中位ROC及未来数据不变性。仅新target选择与三票证据记录改变；原单S函数、成本/资金费/行情/风险/统计函数原字节保持。真实回测另用独立整数票决、Decimal成交/资金费和全净值核验。

8真实合并Parquet与16年度/近期源SHA/字节固定。连续370日OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo，最大慢视窗30日可用。静态规则无拟合或未来标签，purge不适用。12完整30日折＋10日尾折承接现金/数量/费用；近期40日从day330真实状态继承并分8×5日，不重开本金或诊断平仓；只在原终点计费平仓。这些数据反复研究，属于开发验证，不是未触碰最终测试或独立未来证据。

每侧5bp手续费＋1bp半价差＋2bp滑点＋0.5×此前20日log收益样本波动×sqrt(实际成交金额/此前20日quoteADV)冲击，参与率≤0.1%，真实不利tick/lot/最小金额及100%抵押入场约束。永续资金费=-q×真实结算mark×rate，流出按1/2/3倍、收入不放大；无虚构现货借币。缺L2/TCA/完整历史保证金阶梯，1%维持保证金＋闭合小时不利mark仅风险代理，不保证tick清算安全或实盘容量。

门槛不变：全期/近期三档净正、1倍月正折≥9/12及近期≥6/8、三倍完整连续净值DD≤25%、二维排序相邻索引半径1含自身且仅同新规则邻域三倍净正≥60%、至少4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/风险代理违规0、终点空仓且≥180日。2图24面板比较旧单S/新多数过滤的全期及近期收益、Sharpe、回撤；78成本行、1014全期折、624近期折、13356新日边界、14敏感性边及72匹配对照均保存。

结果：{"new_financial_configs": 12, "new_native_components": 6, "new_passive_parents": 6, "passed_candidates": 2, "rejected_candidates": 10, "positive_configs_by_cost": {"1": 12, "2": 12, "3": 12}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 1, "recent40_six_of_eight_positive5d_1x_folds": 10}, "by_scope": {"native": {"new": 6, "passed": 0, "best_full3": {"name": "vote370_ETH_H025_S28_L4_N3000", "return3_pct": 11.650822583371223, "whole_DD3_pct": 4.559197782154223, "recent_return3_pct": 1.9223497175211435, "positive_months1": 10, "positive_recent1": 4, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 6, "passed": 2, "best_full3": {"name": "vote370_parent_B1000_E3000_H025_S28_L4", "return3_pct": 6.825858532086193, "whole_DD3_pct": 2.929782426033012, "recent_return3_pct": 1.1933643692488616, "positive_months1": 11, "positive_recent1": 6, "failed_criteria": []}}}, "rows": {"cost": 78, "full_folds": 1014, "recent40_folds": 624, "daily_NAV": 13356, "edges": 14, "reference_comparisons": 72}}

原单S冻结候选与旧SMA从Oct28UTC08:30续接至10:30，不切换到新多数规则。保留实际现金、数量、entry、费用、已计08:00资金费及完整净值链；09:00闭合小时检查承接08小时结算前/后风险栈，不重计资金费、不重开本金、不强制截止平仓。下一资金费16:00、下一日决策Oct29UTC00:01。真实闭合行情延迟重建，区别于paper10十策略实时报价账户；partial的rejected不取消长期计划。

背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本多数规则是研究推论，不是论文复现或利润/容量移植。全登记关键词命中的资金费中位数、岭回归中位插补、现货滚动价格中位策略，与此ETH永续快反转＋相邻慢ROC票决的完整规则不同。12新相关试验及所有既往试验存在多重选择偏差，无DSR/PBO、独立前向盈利或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py、check_sources.py、audit_candidate.py、audit_forward.py、forward.py --reproduce只读已完成真实证据；勿重新reserve/evaluate/summarize相同已完成配置。原始命令日志保持字节，发布空白检查排除*.log，全部日志仍做完整tree/blob/SHA验证；main普通非强推，不建分支、定时任务或重部署。

关键稳健性结论（仅汇总已完成结果）：{"native": {"cells": 6, "full3x_net_positive": 6, "recent6of8_new": 0, "recent6of8_single": 0, "full3x_improved_vs_single": 4, "all_parent_recent_fold_counts_identical_to_single": null}, "parent": {"cells": 6, "full3x_net_positive": 6, "recent6of8_new": 2, "recent6of8_single": 2, "full3x_improved_vs_single": 4, "all_parent_recent_fold_counts_identical_to_single": true}}。多数规则改变了6个原生策略的实际决策与净值，确为新规则。父组合近期正折数与同参数旧单S对照全部相同：仅S28的L3/L4两项达到6/8，S27/S29四邻格仍为5/8；因此“扩大近期资格平台”的假设未获支持。两项按预设门槛保留passed历史标签，但不得把全期收益提升、邻域全期净正或已有历史通过称为消除近期脆弱性或独立前向盈利。

历史通过项目只读冻结检查：2项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。
vote370_parent_B1000_E3000_H025_S28_L3：1/2/3倍370日收益[8.37698329536407, 7.178406331162335, 5.97920042741058]%，整体3倍回撤2.772379472130715%，近期3倍收益1.2623086499592429%；完整月正折9/12、近期6/8，邻域全期3倍净正6/6、原始近期6/8仅2/6。仅通过预设历史门槛，尚无该新配置独立未来证据。
vote370_parent_B1000_E3000_H025_S28_L4：1/2/3倍370日收益[9.1079093052703, 7.9670567513032475, 6.825858532086193]%，整体3倍回撤2.929782426033012%，近期3倍收益1.1933643692488616%；完整月正折11/12、近期6/8，邻域全期3倍净正6/6、原始近期6/8仅2/6。仅通过预设历史门槛，尚无该新配置独立未来证据。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|vote370_ETH_H025_S28_L4_N3000|15.221676|13.436595|11.650823|4.559198|1.922350|10/12|4/8|rejected|
|vote370_ETH_H025_S27_L4_N3000|14.127730|12.432691|10.737142|5.273052|1.744122|10/12|2/8|rejected|
|vote370_ETH_H025_S29_L3_N3000|14.359139|12.460741|10.560997|4.257252|2.018876|9/12|4/8|rejected|
|vote370_ETH_H025_S29_L4_N3000|13.571372|11.849519|10.127243|4.640987|1.911197|10/12|3/8|rejected|
|vote370_ETH_H025_S27_L3_N3000|13.818391|11.957484|10.095641|4.919669|1.869932|8/12|3/8|rejected|
|vote370_ETH_H025_S28_L3_N3000|13.759824|11.859294|9.957506|4.266023|2.068596|9/12|5/8|rejected|
|vote370_parent_B1000_E3000_H025_S28_L4|9.107909|7.967057|6.825859|2.929782|1.193364|11/12|6/8|passed|
|vote370_parent_B1000_E3000_H025_S27_L4|8.560936|7.465105|6.369018|2.991868|1.098733|10/12|5/8|rejected|
|vote370_parent_B1000_E3000_H025_S29_L3|8.676641|7.479130|6.280946|2.769446|1.239119|9/12|5/8|rejected|
|vote370_parent_B1000_E3000_H025_S29_L4|8.282757|7.173519|6.064069|2.956674|1.182459|10/12|5/8|rejected|
|vote370_parent_B1000_E3000_H025_S27_L3|8.406266|7.227501|6.048268|2.891409|1.161232|9/12|5/8|rejected|
|vote370_parent_B1000_E3000_H025_S28_L3|8.376983|7.178406|5.979200|2.772379|1.262309|9/12|6/8|passed|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 2, "cells": 6, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "vote370_ETH_H025_S28_L4_N3000", "highest_observed_is_on_axis_boundary": {"trend_lookback_days": false, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 2, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 2, "cells": 6, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "vote370_parent_B1000_E3000_H025_S28_L4", "highest_observed_is_on_axis_boundary": {"trend_filter_lookback_days": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 2, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 1, "recent40_six_of_eight_positive5d_1x_folds": 10}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。78成本行、1014全期折、624近期折、13356新日边界、14敏感性边、72匹配对照完整留档；2图24面板已实际打开。新多数规则与旧单S对照分开，新规则邻域只含同新规则。。
独立只读核验8旧原生/24成本曲线、1368条已保存成交与26640条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；6个新原生实际执行并独立核验整数信号/Decimal成交、资金费和完整净值。12新配置36成本场景共19620468完整NAV点、504全期/逐折和324近期/逐折指标通过；15旧唯一结果SHA/资格保持，10640受保护文件不变。18新实际ID各自finish，36事件仅追加。
只读监控实际检查exit0：7724研究项，163既有paper观察/10账户；7712旧展示行完整字典不变。原候选累计2118点/场景、2069分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计38097点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录0项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
