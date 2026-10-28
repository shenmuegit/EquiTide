# 20261028T072053Z ETH慢周期一日扰动与阈值/反转周期交叉验证

实际计算4个ETH原生＋4个BTC/ETH组合，共8配置/24成本场景；历史通过0，淘汰8。完整读取20876事件/10334ID及213份结论；初始16项均有实际证据。

事前预设ETH阈值2/2.5% × 慢周期27/28/29日 × 反转3/4日。每作用域12格，16个旧原生/父组合格只读；H2.5、S27/29、L3/4的新4原生＋4父组合先逐项成功reserve才计算。20相邻边/作用域，固定门槛，检验慢周期一日偏移是否破坏资格。ETH银行10000、入场3000；BTC固定L31/H4%/退出1%，银行10000、入场1000。

ETH此前完整L日ROC严格>H反转空/<-H反转多，带内多仅ROC<0、空仅ROC>0保留，零退出。慢S日ROC正仅许多、负仅许空，零或不兼容平实际仓位；现金重入须新严格极端，无隐藏desired。BTC此前完整31日ROC严格>4%多/<-4%空，带内多仅ROC>-1%、空仅ROC<1%保留，反向完整极端先平后开。UTC00:01实际OPEN执行，q=floor(N/此前完整close/lot)*lot，信号/手数不读未来OPEN、资金费或未闭合价格。引擎与171814原字节相同，仅spec慢周期/反转周期不同。

原值1/1指两个完整10000USDT独立银行，父本金20000、入场预算4000=初始本金20%；不归一化、不复利调仓、不转账/交叉保证金/再平衡。10个旧原生/30成本NAV恢复原账本并核对SHA。4个新原生实际执行独立成本/资金费/风险路径；4父组合对齐共同(ns,eventcode)轴因果承接上一完成点并加总，整体指标从完整曲线计算，不平均Sharpe/回撤。每新项对照同H/L旧S28、同资金恒多及解析现金0。

8真实合并Parquet及16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo。静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续承接现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓；仅原预定终点计费平仓。该历史反复研究，属于开发验证，不是未触碰最终测试或独立未来市场。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(实际成交金额/此前20日ADV)冲击，参与率≤0.1%，实际不利tick/lot/最小金额及100%抵押入场上限。资金费=-q×实际结算mark×rate，流出乘1/2/3、收入不放大；永续空头无虚构现货借币。报告逐档执行数、成本占比、费用分项和资金费。缺L2/TCA/历史完整保证金阶梯，1%维持保证金＋闭合小时不利mark仅代理，不保证tick清算安全或实盘容量。

门槛保持：全期/近期三档净正、1倍月正折≥9/12且近期≥6/8、3倍连续全净值DD≤25%、三维索引半径1含自身邻域3倍净正≥60%、至少4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/独立银行风险代理违规0、终点空仓且≥180日。旧16格资格不重评级；4图24面板，78成本行、1014全期折、624近期折、8904新日边界、40敏感性边、48匹配对照完整留档。

结果：{"new_financial_configs": 8, "new_native_components": 4, "new_passive_parents": 4, "passed_candidates": 0, "rejected_candidates": 8, "positive_configs_by_cost": {"1": 8, "2": 8, "3": 8}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 2, "recent40_six_of_eight_positive5d_1x_folds": 8, "recent40_positive_all_costs": 1}, "by_scope": {"native": {"new": 4, "passed": 0, "best_full3": {"name": "nearslow370_ETH_N3000_H025_S29_L4", "return3_pct": 11.080953529676218, "whole_DD3_pct": 4.573930948442317, "recent_return3_pct": 1.8944775676554393, "positive_months1": 11, "positive_recent1": 3, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 4, "passed": 0, "best_full3": {"name": "nearslow370_parent_B1000_E3000_H025_S29_L4", "return3_pct": 6.540924005238691, "whole_DD3_pct": 2.934660926364141, "recent_return3_pct": 1.177104570494114, "positive_months1": 11, "positive_recent1": 5, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 78, "full_folds": 1014, "recent40_folds": 624, "daily_NAV": 8904, "edges": 40, "reference_comparisons": 48}}

原H4/ETH慢28反转3日冻结候选和旧SMA从Oct28UTC04:30续接至06:30，原现金/数量/entry/费用/已处理资金费/NAV完整承接；不重开本金、不重复日决策/资金费、不截止强平。真实闭合行情延迟重建，两者独立于paper10十策略；partial的rejected不取消长期计划。下一资金费08:00，下一日决策Oct29UTC00:01。

背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本加密阈值/周期规则是研究推论，不是论文复现或利润/容量移植。8个新相关试验及既往全部试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号、Decimal费用/资金费、风险和完整净值；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读真实证据，不重新reserve/evaluate/summarize已完成配置。main普通非强推、完整远端tree/blob/行情SHA验证后释放本轮锁，不建其他分支/定时任务或重部署。

本轮关键结论：同阈值2.5%、同反转L3或L4，旧S28组合近期正折均为6/8且原状态passed；S27和S29四个新组合均降至5/8、rejected，尽管全期三档收益仍正。由此可见历史资格对慢周期一天扰动脆弱，全期净收益平台不能替代近期稳健性；不改写旧状态，也不据此宣称长期负期望。完整匹配对照见slow_neighbor_diagnostics.json。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|nearslow370_ETH_N3000_H025_S29_L4|14.868439|12.974860|11.080954|4.573931|1.894478|11/12|3/8|rejected|
|nearslow370_ETH_N3000_H025_S29_L3|14.094792|12.087222|10.078403|4.587979|2.027906|10/12|4/8|rejected|
|nearslow370_parent_B1000_E3000_H025_S29_L4|8.931291|7.736189|6.540924|2.934661|1.177105|11/12|5/8|rejected|
|nearslow370_ETH_N3000_H025_S27_L4|10.061504|8.280419|6.499002|6.242122|-0.354807|7/12|2/8|rejected|
|nearslow370_ETH_N3000_H025_S27_L3|10.104874|8.157315|6.209113|5.660640|0.186543|6/12|4/8|rejected|
|nearslow370_parent_B1000_E3000_H025_S29_L3|8.544467|7.292370|6.039649|2.895382|1.241973|9/12|5/8|rejected|
|nearslow370_parent_B1000_E3000_H025_S27_L4|6.527823|5.388969|4.249948|3.064302|0.016562|9/12|5/8|rejected|
|nearslow370_parent_B1000_E3000_H025_S27_L3|6.549508|5.327417|4.105004|3.376775|0.294556|9/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 3, "cells": 12, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 0.8333333333333334, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 0.8333333333333334, "highest_observed_full3x_net_cell": "nearslow370_ETH_N3000_H025_S29_L4", "highest_observed_is_on_axis_boundary": {"return_hurdle": true, "trend_lookback_days": true, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 6, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 3, "cells": 12, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "nearslow370_parent_B1000_E3000_H025_S29_L4", "highest_observed_is_on_axis_boundary": {"reversal_return_hurdle": true, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 4, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 2, "recent40_six_of_eight_positive5d_1x_folds": 8, "recent40_positive_all_costs": 1}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。78成本行、1014全期折、624近期折、8904新日边界、40敏感性边、48匹配对照完整留档；4图24面板已实际打开。
独立只读核验10旧原生/30成本曲线、1992条已保存成交与33300条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；4个新原生实际执行并独立核验整数信号/Decimal成交、资金费和完整净值。8新配置24成本场景共13080312完整NAV点、336全期/逐折和216近期/逐折指标通过；19旧唯一结果SHA/资格保持，10263受保护文件不变。14新实际ID各自finish，28事件仅追加。
只读监控实际检查exit0：7700研究项，161既有paper观察/10账户；7692旧展示行完整字典不变。原候选累计1872点/场景、1829分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计37857点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录0项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
