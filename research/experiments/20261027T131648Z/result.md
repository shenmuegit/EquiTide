# 20261027T131648Z ETH中间趋势过滤周期与反转速度验证

实际计算6个ETH原生策略＋6个组合，共12配置/36成本场景，历史通过0、淘汰12。完整读取20172事件/9982ID、204份结论，初始16项已有真实历史证据，无缺结果项可补。

预设ETH慢25/26/27/28/31日×反转3/4/5日，阈值2%、零交叉退出、原生银行10000、固定入场3000。慢26/27日6原生＋6组合逐项先reserve再计算；慢25/28/31日18旧单元只读，保留旧资格。BTC固定此前完整31日ROC严格>4%多/<-4%空，带内多仅ROC>-1%、空仅ROC<1%保留；完整反向极端先平后开，银行10000/入场1000。

ETH此前完整L日ROC严格>2%反转空/<-2%反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢S日ROC正仅许多、负仅许空，零/不兼容平实际仓位，现金重入须新极端，无隐藏desired。UTC00:01真实OPEN执行，数量floor(N/此前完整close/lot)，不用未来OPEN/未闭合价格/资金费决定信号或手数。引擎仅增加允许26/27慢周期，信号/成交/资金费/风险/指标函数其余字节不变。

原值1/1指两个完整10000USDT独立银行，父本金20000，入场合计4000=初始本金20%；不归一化、不复利调仓、不转账/交叉保证金/再平衡。11个旧原生/33成本NAV只读恢复并核对原SHA，不重跑旧信号/撮合。组合按共同(ns,eventcode)时钟承接上一完成点后逐点相加并重算整体指标，不平均收益率/Sharpe，不缩放旧N净值。每新项与相同L/金额的旧慢28日、同金额恒多及解析现金0逐档比较。

真实8合并Parquet及16年度/近期源文件SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日先验上下文、3日初始embargo，覆盖最大慢31日。静态规则无拟合/未来标签，purge不适用；12完整30日折＋10日尾折连续carry现金/数量/entry/成本，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓，仅预定终点计费平仓。反复使用的开发历史不称最终未触碰留出或独立市场证据。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(成交金额/此前20日ADV)冲击，参与率≤0.1%；真实不利tick/lot/最小金额、100%抵押入场上限。资金费=-q×实际结算mark×rate，流出乘1/2/3，收入不放大；永续空头无虚构现货借币。价差/滑点/冲击为估计，缺L2/TCA/历史完整margin阶梯，1%维持保证金＋闭合小时不利mark仅风险代理，不保证tick清算安全或实盘容量。

预设门槛不变：全期/近期三档净正，1倍完整月正折≥9/12且近期≥6/8，3倍完整连续NAV最大DD≤25%，二维排序相邻索引半径1含自身邻域净正率≥60%，≥4往返、(参考毛利＋资金费)/执行成本≥2.5，现金/拒单/风险代理违规0、终点空仓及≥180日。两个作用域各15格、22边；完整收益/回撤/Sharpe/Calmar/陡变/边界、逐折/逐变体留档，2图12面板。旧单元资格不按新邻域重评级。

结果：{"new_financial_configs": 12, "new_native_components": 6, "new_passive_parents": 6, "passed_candidates": 0, "rejected_candidates": 12, "positive_configs_by_cost": {"1": 12, "2": 12, "3": 12}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 5, "recent40_six_of_eight_positive5d_1x_folds": 12, "recent40_positive_all_costs": 4}, "by_scope": {"native": {"new": 6, "passed": 0, "best_full3": {"name": "midgate370_ETH_N3000_S26_L5_H02", "return3_pct": 11.327070772590053, "whole_DD3_pct": 6.102743012488232, "recent_return3_pct": 0.6438570556278167, "positive_months1": 10, "positive_recent1": 2, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 6, "passed": 0, "best_full3": {"name": "midgate370_parent_B1000_E3000_S26_L5_H02", "return3_pct": 6.663982626695586, "whole_DD3_pct": 4.07820875841487, "recent_return3_pct": 0.5305979882290535, "positive_months1": 10, "positive_recent1": 4, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 96, "full_folds": 1248, "recent40_folds": 768, "daily_NAV": 13356, "edges": 44, "reference_comparisons": 72}}

原H4/ETH慢28日反转3日冻结候选与旧SMA只续接至Oct27UTC12:30，承接10:30完整现金/数量/entry/成本/资金费/风险段和NAV链，不重复08:00.001已记资金费，不改长期规则或强制平仓。两者为延迟闭合行情重建，不能当paper10真实报价账户或成熟前向资格。paper10账本只读，部分观察rejected不取消原长期计划。

一手背景复用此前2026-10-27已实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）和[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05）。加密26/27日过滤与3/4/5日反转为本研究推论，非论文复现或传统市场利润/容量移植。12新相关试验有多重选择偏差，未证明DSR/PBO或稳定实盘盈利。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py调用独立audit_native.verify核验整数信号、Decimal费用/资金费/状态/NAV；check_sources.py、audit_candidate.py、audit_forward.py、forward.py --reproduce只读已有真实证据，不重复reserve/evaluate/summarize已完成配置。普通main非强推及完整远端tree/blob/行情SHA证明后释放自己锁，不建分支、任务、重部署或真实下单。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|midgate370_ETH_N3000_S26_L5_H02|15.289266|13.308485|11.327071|6.102743|0.643857|10/12|2/8|rejected|
|midgate370_ETH_N3000_S26_L3_H02|15.843483|13.275610|10.705951|8.503783|1.444842|8/12|4/8|rejected|
|midgate370_ETH_N3000_S26_L4_H02|14.062560|11.968071|9.872989|4.530973|-0.355273|8/12|3/8|rejected|
|midgate370_ETH_N3000_S27_L5_H02|10.508688|8.654096|6.799836|4.533671|-0.628506|9/12|2/8|rejected|
|midgate370_parent_B1000_E3000_S26_L5_H02|9.141704|7.903002|6.663983|4.078209|0.530598|10/12|4/8|rejected|
|midgate370_parent_B1000_E3000_S26_L3_H02|9.418813|7.886565|6.353423|5.157910|0.944627|9/12|5/8|rejected|
|midgate370_ETH_N3000_S27_L3_H02|11.035087|8.668533|6.300584|6.738804|0.186382|6/12|4/8|rejected|
|midgate370_parent_B1000_E3000_S26_L4_H02|8.528351|7.232795|5.936942|3.147982|0.010383|8/12|5/8|rejected|
|midgate370_ETH_N3000_S27_L4_H02|8.902073|6.907709|4.912649|6.293909|-0.360152|6/12|2/8|rejected|
|midgate370_parent_B1000_E3000_S27_L5_H02|6.751415|5.575808|4.400365|3.260116|-0.125202|9/12|5/8|rejected|
|midgate370_parent_B1000_E3000_S27_L3_H02|7.014615|5.583026|4.150739|4.039460|0.294427|10/12|5/8|rejected|
|midgate370_parent_B1000_E3000_S27_L4_H02|5.948108|4.702614|3.456772|3.077329|0.016689|9/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"cells": 15, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 0.6, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 0.6, "highest_observed_full3x_net_cell": "midgate370_ETH_N3000_S26_L5_H02", "highest_observed_is_on_axis_boundary": {"trend_lookback_days": false, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 9, "old_qualifications_preserved": true, "not_an_untouched_test_or_global_optimum": true}, "parent": {"cells": 15, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 0.8, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 0.8, "highest_observed_full3x_net_cell": "midgate370_parent_B1000_E3000_S26_L5_H02", "highest_observed_is_on_axis_boundary": {"trend_filter_lookback_days": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 6, "old_qualifications_preserved": true, "not_an_untouched_test_or_global_optimum": true}}。最高观测单元位于L=5的预设边界，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 5, "recent40_six_of_eight_positive5d_1x_folds": 12, "recent40_positive_all_costs": 4}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。96成本行、1248全期折、768近期折、13356新日边界、44敏感性边、72匹配对照完整留档；2图12面板已实际打开。
独立核验1452新成交、19980资金费记录、6660因果决策和43899状态小时风险检查；36新成本场景共19620468完整NAV点、504全期/逐折和324近期/逐折指标。11旧原生/33成本路径、21旧唯一结果SHA/资格保持，未重跑旧模型；8363受保护文件不变。18新实际ID各自finish，36事件仅追加。
只读监控实际检查exit0：7496研究项，152既有paper观察/10账户；7484旧展示行完整字典不变。原候选累计767点/场景、749分钟，0新增日决策/成交/资金费，08:00.001旧收入未重复；旧SMA累计36776点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实非零命令/传输退出0项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
