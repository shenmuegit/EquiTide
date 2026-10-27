# 20261027T151819Z ETH六至七日反转与慢趋势交互验证

实际计算4个ETH原生策略＋4个组合，共8配置/24成本场景，历史通过0、淘汰8。完整读取20228事件/10010ID及205份结论，初始16项均有真实历史证据，无缺结果条目可补。

事前预设ETH慢28/31日×反转5/6/7日，阈值2%、零交叉退出、原生银行10000、固定入场3000。6/7日4原生＋4组合各自先reserve后计算，5日旧2原生＋2组合只读，保留旧资格。BTC固定此前完整31日ROC严格>4%多/<-4%空，带内多仅ROC>-1%、空仅ROC<1%保持；完整反向极端先平后开，银行10000、固定入场1000。此前L5位于回看网格边界，扩大周期检验频率与近期分折，不能把结果当独立新市场证据。

ETH此前完整L日ROC严格>2%反转空/<-2%反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢S日ROC正仅许多、负仅许空，零/不兼容平实际仓位，现金重入须新极端，无隐藏desired。UTC00:01真实OPEN执行，数量floor(N/此前完整close/lot)，信号/手数不使用未来OPEN、未闭合价格或资金费。引擎仅扩大允许反转回看到6/7，其余信号、订单、成本、资金费、风险、指标代码保持字节一致。

原值1/1指两个完整10000USDT独立银行，组合本金20000；入场预算合计4000=初始本金20%，不是实际恒定风险比例，不归一化、不复利调仓、不转账/交叉保证金/再平衡。4旧原生/12成本NAV从真实账本只读恢复并核对原SHA，不重跑旧模型；新N3000原生逐档实际模拟。父组合按共同(ns,eventcode)时轴承接上一完成点后逐点相加并重算指标，不平均Sharpe/收益或缩放旧净值。每新项与相同S/N的旧L5、同金额恒多及解析现金0逐档比较。

真实8合并Parquet和16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo，覆盖最大慢31/反转7日。静态规则无拟合/未来标签，purge不适用；12完整30日折＋10日尾折连续carry现金/数量/entry/成本，近期40日继承day330状态并分8×5日，不重开本金/诊断平仓，仅预定终点计费平仓。反复使用历史只属开发验证，不称最终未触碰留出。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(成交金额/此前20日ADV)冲击，参与率≤0.1%；实际不利tick/lot/最小金额、100%抵押入场。资金费=-q×实际结算mark×rate，流出乘1/2/3，收入不放大；永续无虚构现货借币。成本金额、分项、占本金比例、资金费和交易数逐档保存。价差/滑点/冲击是估计，缺L2/TCA/完整历史margin阶梯；1%维持保证金＋闭合小时不利mark仅代理，不保证容量或tick清算安全。

预设门槛保持：全期/近期三档净正，1倍完整月正折≥9/12且近期≥6/8，3倍完整连续NAV最大DD≤25%，二维排序相邻索引半径1含自身邻域净正≥60%，≥4往返、(参考毛利＋资金费)/费用≥2.5，现金/拒单/风险代理违规0、终点空仓且≥180日。两作用域各6格、7边，全部收益/回撤/Sharpe/Calmar、陡变/边界、逐折/逐变体留档。旧资格不按新邻域重评级。

结果：{"new_financial_configs": 8, "new_native_components": 4, "new_passive_parents": 4, "passed_candidates": 0, "rejected_candidates": 8, "positive_configs_by_cost": {"1": 8, "2": 8, "3": 8}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 6, "recent40_positive_all_costs": 6, "recent40_six_of_eight_positive5d_1x_folds": 8}, "by_scope": {"native": {"new": 4, "passed": 0, "best_full3": {"name": "slowreversal370_ETH_N3000_S31_L6_H02", "return3_pct": 7.694667600701877, "whole_DD3_pct": 4.824020814594887, "recent_return3_pct": 0.1402922205091084, "positive_months1": 9, "positive_recent1": 2, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 4, "passed": 0, "best_full3": {"name": "slowreversal370_parent_B1000_E3000_S31_L6_H02", "return3_pct": 4.847781040751498, "whole_DD3_pct": 2.9360237863621297, "recent_return3_pct": 0.2699808981801999, "positive_months1": 9, "positive_recent1": 3, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 42, "full_folds": 546, "recent40_folds": 336, "daily_NAV": 8904, "edges": 14, "reference_comparisons": 48}}

原H4/ETH慢28日反转3日冻结前向候选及旧SMA仅续接至Oct27UTC14:30，承接12:30完整现金/数量/entry/费用/资金费/风险段/NAV链，不重复08:00.001旧资金费。无新增日决策/强制平仓，两者为延迟闭合行情重建，不能当paper10真实报价账户或成熟前向资格。paper10冻结账本只读，部分观察rejected不取消长期计划。

一手背景复用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05）。加密6/7日反转与慢门槛为本研究推论，非论文复现或传统市场利润/容量移植。8个新相关试验存在多重选择偏差，无DSR/PBO或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py调用audit_native.verify独立核验整数信号、Decimal费用/资金费/状态/NAV。check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读已有实际证据，不重复reserve/evaluate/summarize已完成配置。main普通非强推并完成freshfetch/独立allheads/完整tree/blob/行情SHA证明后释放自己锁，不建分支/重复任务、不重部署或真实下单。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|slowreversal370_ETH_N3000_S31_L6_H02|11.538284|9.617128|7.694668|4.824021|0.140292|9/12|2/8|rejected|
|slowreversal370_parent_B1000_E3000_S31_L6_H02|7.266213|6.057323|4.847781|2.936024|0.269981|9/12|3/8|rejected|
|slowreversal370_parent_B1000_E3000_S28_L6_H02|4.026160|2.792665|1.558635|4.917918|-0.158482|8/12|3/8|rejected|
|slowreversal370_parent_B1000_E3000_S31_L7_H02|3.999968|2.760943|1.521676|3.218690|-0.368796|6/12|4/8|rejected|
|slowreversal370_parent_B1000_E3000_S28_L7_H02|3.710767|2.494829|1.278628|2.997388|-0.802473|7/12|4/8|rejected|
|slowreversal370_ETH_N3000_S28_L6_H02|5.058178|3.087810|1.116376|8.774324|-0.722765|8/12|2/8|rejected|
|slowreversal370_ETH_N3000_S31_L7_H02|5.005794|3.024368|1.042457|5.999462|-1.140153|7/12|2/8|rejected|
|slowreversal370_ETH_N3000_S28_L7_H02|4.427391|2.492139|0.556361|6.706488|-2.000176|7/12|2/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"cells": 6, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 0.5, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 0.5, "highest_observed_full3x_net_cell": "longfast370_ETH_N3000_S31_L5_H02", "highest_observed_is_on_axis_boundary": {"trend_lookback_days": true, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 3, "old_qualifications_preserved": true, "not_an_untouched_test_or_global_optimum": true}, "parent": {"cells": 6, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 0.5, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 0.5, "highest_observed_full3x_net_cell": "longfast370_parent_B1000_E3000_S31_L5_H02", "highest_observed_is_on_axis_boundary": {"trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 1, "old_qualifications_preserved": true, "not_an_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已留档，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 6, "recent40_positive_all_costs": 6, "recent40_six_of_eight_positive5d_1x_folds": 8}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。42成本行、546全期折、336近期折、8904新日边界、14敏感性边、48匹配对照完整留档；2图12面板已实际打开。
独立核验888新成交、13320资金费记录、4440因果决策和30003状态小时风险检查；24新成本场景共13080312完整NAV点、336全期/逐折和216近期/逐折指标。4旧原生/12成本路径、7旧唯一结果SHA/资格保持，未重跑旧模型；8552受保护文件不变。14新实际ID各自finish，28事件仅追加。
只读监控实际检查exit0：7504研究项，153既有paper观察/10账户；7496旧展示行完整字典不变。原候选累计889点/场景、869分钟，0新增日决策/成交/资金费，08:00.001旧收入未重复；旧SMA累计36896点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录1项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
