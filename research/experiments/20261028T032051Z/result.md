# 20261028T032051Z ETH反转入场阈值与周期稳健性验证

实际计算12个ETH原生＋12个BTC/ETH组合，共24配置/72成本场景；历史通过2，淘汰22。完整读取20716事件/10254ID及211份结论，初始16项均有实际证据，无待补缺结果项。

事前预设ETH入场阈值1.5/2/2.5% × 慢周期28/31日 × 反转3/4/5日。每作用域18格，12个H2旧原生/父组合只读，H1.5/H2.5新12原生与12父组合逐项先成功reserve才计算，33相邻边/作用域。ETH银行10000、固定入场3000；BTC固定31日ROC/H4%/退出1%，银行10000、固定入场1000。降低阈值可能增加噪声/成本，提高阈值可能减少弱反转与机会；结果不决定本轮参数或失败门槛。

ETH此前完整L日ROC严格>H反转空/<-H反转多，带内多仅ROC<0、空仅ROC>0保留，零退出。慢S日ROC正仅许多、负仅许空，零或不兼容平实际仓位；现金重入须新严格极端，无隐藏desired。BTC此前完整31日ROC严格>4%多/<-4%空，带内多仅ROC>-1%、空仅ROC<1%保留，反向完整极端先平后开。UTC00:01实际OPEN执行，q=floor(N/此前完整close/lot)*lot，信号/手数不读未来OPEN、资金费或未闭合价格。引擎与171814原字节相同，仅spec阈值不同。

原值1/1指两个完整10000USDT独立银行，父本金20000，入场预算4000=初始父本金20%；不是目标权重/恒定风险，不归一化、不复利调仓、不转账/交叉保证金/再平衡。8个旧原生/24成本NAV从完整账本恢复并核对原SHA；12个新原生实际重算金额专属成交、费用、资金费及风险路径，12个新组合对齐共同(ns,eventcode)时轴承接上一完成点并逐点加总，重新计算整体指标，不平均Sharpe/回撤或线性缩放旧金额结果。每新项与同S/L的旧H2、同资金恒多及解析现金0比较。

8真实合并Parquet及16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo。静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续承接现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓；仅原预定终点计费平仓。该历史反复研究，属于开发验证，不是未触碰最终测试或独立未来市场。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(实际成交金额/此前20日ADV)冲击，参与率≤0.1%，实际不利tick/lot/最小金额及100%抵押入场上限。资金费=-q×实际结算mark×rate，流出乘1/2/3、收入不放大；永续空头无虚构现货借币。报告逐档执行数、成本占比、费用分项和资金费。缺L2/TCA/历史完整保证金阶梯，1%维持保证金＋闭合小时不利mark仅代理，不保证tick清算安全或实盘容量。

门槛保持：全期/近期三档净正，1倍月正折≥9/12且近期≥6/8，3倍完整连续净值最大DD≤25%，三维排序索引半径1含自身邻域3倍净正≥60%，至少4往返、(参考毛利＋资金费)/执行成本≥2.5，现金/拒单/独立银行风险代理违规0，终点空仓且≥180日。旧12格资格不按新邻域重评级。6图36面板，114成本行、1482全期折、912近期折、26712新日边界、66敏感性边与144匹配对照留档。

结果：{"new_financial_configs": 24, "new_native_components": 12, "new_passive_parents": 12, "passed_candidates": 2, "rejected_candidates": 22, "positive_configs_by_cost": {"1": 24, "2": 24, "3": 23}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 12, "recent40_six_of_eight_positive5d_1x_folds": 20, "positive_all_costs": 1, "recent40_positive_all_costs": 2}, "by_scope": {"native": {"new": 12, "passed": 0, "best_full3": {"name": "nearentry370_ETH_N3000_H015_S31_L5", "return3_pct": 12.604365054028666, "whole_DD3_pct": 5.210067198840706, "recent_return3_pct": 0.7326179675948286, "positive_months1": 9, "positive_recent1": 2, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 12, "passed": 2, "best_full3": {"name": "nearentry370_parent_B1000_E3000_H015_S31_L5", "return3_pct": 7.302629767414914, "whole_DD3_pct": 2.637714329872942, "recent_return3_pct": 0.5777209558647911, "positive_months1": 9, "positive_recent1": 4, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 114, "full_folds": 1482, "recent40_folds": 912, "daily_NAV": 26712, "edges": 66, "reference_comparisons": 144}}

原H4/ETH慢28反转3日冻结候选和旧SMA从Oct28UTC00:30续接至02:30，保留刚完成00:01日决策、00:00.001资金费及完整风险状态，不重开本金/持仓，不重复日决策或资金费，不强制截止平仓。独立检查01:00闭合小时中资金费前后两个现金状态。依据真实闭合行情延迟重建，不是十策略实时报价账户或成熟长期资格；paper10只读，partial的rejected不取消长期计划。下一日决策Oct29UTC00:01。

背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本加密阈值/周期规则是研究推论，不是论文复现或利润/容量移植。24个新相关试验及既往全部试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号、Decimal费用/资金费、风险和完整净值；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读真实证据，不重新reserve/evaluate/summarize已完成配置。main普通非强推、完整远端tree/blob/行情SHA验证后释放本轮锁，不建其他分支/定时任务或重部署。

历史通过项目只读冻结检查：2项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。
nearentry370_parent_B1000_E3000_H025_S28_L3：1/2/3倍370日收益[8.472111773522695, 7.300251137029612, 6.12771348276151]%，整体3倍回撤2.76842204474671%，近期3倍收益1.260519933362536%；完整月正折10/12、近期6/8，邻域全期3倍净正8/8、原始近期6/8仅4/8。仅通过预设历史门槛，尚无该新配置独立未来证据。
nearentry370_parent_B1000_E3000_H025_S28_L4：1/2/3倍370日收益[7.584016845324282, 6.4771980092381165, 5.369909676526952]%，整体3倍回撤2.954369214866781%，近期3倍收益1.210053212346729%；完整月正折10/12、近期6/8，邻域全期3倍净正12/12、原始近期6/8仅4/12。仅通过预设历史门槛，尚无该新配置独立未来证据。

本轮12新原生实际成交与成本核验：2778笔成交、39960条含空仓资金费、13320次日决策和87168个状态/小时风险检查均独立核验。所有3倍全期或近期负收益与失败分折留档；最高全期收益项并未通过近期门槛，不作为合格候选。
原冻结候选从00:30至02:30新增122个真实事件键，原1506点精确保留至1628点/场景。已在00:00.001计入的资金费未重复，日决策00:01未重复；01:00完整小时中资金费前后两个现金状态均保留核验，本窗口累计9个闭合小时风险状态检查、违规0。候选0新增成交/日决策/资金费，旧SMA0新增成交/日决策；下一日决策仍为Oct29UTC00:01。
发生的预备脚本失败及旧SMA重复截止草案均完整保留。重复reserve实际退出3，旧实际结果已读取并绑定SHA；未执行重复回测，也没有新登记ID被搁置。修复后的00:30→02:30窗口单独reserve/evaluate/audit/finish/reproduce五项命令实际退出0，见forward_recovery_commands.json。所有原登记/账户/规则均保留。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|nearentry370_ETH_N3000_H015_S31_L5|17.288206|14.946313|12.604365|5.210067|0.732618|9/12|2/8|rejected|
|nearentry370_ETH_N3000_H025_S28_L3|13.950081|12.102983|10.254532|4.254194|2.062908|9/12|5/8|rejected|
|nearentry370_ETH_N3000_H025_S28_L4|12.173891|10.456877|8.738925|4.633922|1.974845|10/12|4/8|rejected|
|nearentry370_ETH_N3000_H025_S28_L5|11.832920|10.239855|8.646775|4.447234|-0.273453|10/12|2/8|rejected|
|nearentry370_ETH_N3000_H025_S31_L3|11.981328|10.088402|8.194327|4.319481|1.932645|9/12|4/8|rejected|
|nearentry370_ETH_N3000_H015_S31_L3|12.587277|10.088236|7.587600|5.541319|1.655628|8/12|4/8|rejected|
|nearentry370_parent_B1000_E3000_H015_S31_L5|10.141174|8.721916|7.302630|2.637714|0.577721|9/12|4/8|rejected|
|nearentry370_parent_B1000_E3000_H025_S28_L3|8.472112|7.300251|6.127713|2.768422|1.260520|10/12|6/8|passed|
|nearentry370_ETH_N3000_H025_S31_L4|9.469020|7.757767|6.045713|4.701610|1.223170|9/12|2/8|rejected|
|nearentry370_parent_B1000_E3000_H025_S28_L4|7.584017|6.477198|5.369910|2.954369|1.210053|10/12|6/8|passed|
|nearentry370_ETH_N3000_H025_S31_L5|8.488682|6.907882|5.326876|4.913388|-0.331494|7/12|1/8|rejected|
|nearentry370_parent_B1000_E3000_H025_S28_L5|7.413531|6.368687|5.323835|2.826402|0.055016|10/12|4/8|rejected|
|nearentry370_parent_B1000_E3000_H025_S31_L3|7.487735|6.292960|5.097611|2.790132|1.186686|9/12|5/8|rejected|
|nearentry370_parent_B1000_E3000_H015_S31_L3|7.790710|6.292877|4.794247|3.388821|1.044235|8/12|5/8|rejected|
|nearentry370_ETH_N3000_H015_S31_L4|8.910224|6.695068|4.478673|5.024593|1.241744|7/12|2/8|rejected|
|nearentry370_ETH_N3000_H015_S28_L5|8.873499|6.487676|4.101496|10.373505|0.844096|8/12|3/8|rejected|
|nearentry370_parent_B1000_E3000_H025_S31_L4|6.231581|5.127643|4.023304|2.972272|0.821503|9/12|4/8|rejected|
|nearentry370_parent_B1000_E3000_H025_S31_L5|5.741412|4.702700|3.663885|3.382683|0.030601|8/12|3/8|rejected|
|nearentry370_parent_B1000_E3000_H015_S31_L4|5.952183|4.596293|3.239784|3.130063|0.827789|8/12|4/8|rejected|
|nearentry370_parent_B1000_E3000_H015_S28_L5|5.933821|4.492597|3.051195|5.306201|0.627437|8/12|5/8|rejected|
|nearentry370_ETH_N3000_H015_S28_L3|7.939639|5.447540|2.953435|7.301416|1.909794|7/12|5/8|rejected|
|nearentry370_parent_B1000_E3000_H015_S28_L3|5.466891|3.972529|2.477165|4.389646|1.156446|8/12|6/8|rejected|
|nearentry370_parent_B1000_E3000_H015_S28_L4|3.193011|1.763480|0.333309|6.133033|1.271569|8/12|6/8|rejected|
|nearentry370_ETH_N3000_H015_S28_L4|3.391880|1.029441|-1.334276|10.847155|2.180862|6/12|4/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 0.9444444444444444, "recent40_3x_positive_Sharpe_fraction": 0.8888888888888888, "full3x_positive_net_fraction": 0.9444444444444444, "recent40_3x_positive_net_fraction": 0.8888888888888888, "highest_observed_full3x_net_cell": "nearentry370_ETH_N3000_H015_S31_L5", "highest_observed_is_on_axis_boundary": {"return_hurdle": true, "trend_lookback_days": true, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 9, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "nearentry370_parent_B1000_E3000_H015_S31_L5", "highest_observed_is_on_axis_boundary": {"reversal_return_hurdle": true, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 6, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 12, "recent40_six_of_eight_positive5d_1x_folds": 20, "positive_all_costs": 1, "recent40_positive_all_costs": 2}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。114成本行、1482全期折、912近期折、26712新日边界、66敏感性边、144匹配对照完整留档；6图36面板已实际打开。
独立只读核验8旧原生/24成本曲线、1512条已保存成交与26640条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；12个新原生实际执行并独立核验整数信号/Decimal成交、资金费和完整净值。24新配置72成本场景共39240936完整NAV点、1008全期/逐折和648近期/逐折指标通过；15旧唯一结果SHA/资格保持，9831受保护文件不变。30新实际ID各自finish，60事件仅追加。
只读监控实际检查exit0：7668研究项，159既有paper观察/10账户；7644旧展示行完整字典不变。原候选累计1628点/场景、1589分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计37617点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录4项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
