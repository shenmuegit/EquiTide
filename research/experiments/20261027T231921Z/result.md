# 20261027T231921Z ETH反转入场阈值与周期稳健性验证

实际计算12个ETH原生＋12个BTC/ETH组合，共24配置/72成本场景；历史通过0，淘汰24。完整读取20556事件/10174ID及209份结论，初始16项均有实际证据，无待补缺结果项。

事前预设ETH入场阈值1/2/3% × 慢周期28/31日 × 反转3/4/5日。每作用域18格，12个H2旧原生/父组合只读，H1/H3新12原生与12父组合逐项先成功reserve才计算，33相邻边/作用域。ETH银行10000、固定入场3000；BTC固定31日ROC/H4%/退出1%，银行10000、固定入场1000。降低阈值可能增加噪声/成本，提高阈值可能减少弱反转与机会；结果不决定本轮参数或失败门槛。

ETH此前完整L日ROC严格>H反转空/<-H反转多，带内多仅ROC<0、空仅ROC>0保留，零退出。慢S日ROC正仅许多、负仅许空，零或不兼容平实际仓位；现金重入须新严格极端，无隐藏desired。BTC此前完整31日ROC严格>4%多/<-4%空，带内多仅ROC>-1%、空仅ROC<1%保留，反向完整极端先平后开。UTC00:01实际OPEN执行，q=floor(N/此前完整close/lot)*lot，信号/手数不读未来OPEN、资金费或未闭合价格。引擎与171814原字节相同，仅spec阈值不同。

原值1/1指两个完整10000USDT独立银行，父本金20000，入场预算4000=初始父本金20%；不是目标权重/恒定风险，不归一化、不复利调仓、不转账/交叉保证金/再平衡。8个旧原生/24成本NAV从完整账本恢复并核对原SHA；12个新原生实际重算金额专属成交、费用、资金费及风险路径，12个新组合对齐共同(ns,eventcode)时轴承接上一完成点并逐点加总，重新计算整体指标，不平均Sharpe/回撤或线性缩放旧金额结果。每新项与同S/L的旧H2、同资金恒多及解析现金0比较。

8真实合并Parquet及16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo。静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续承接现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓；仅原预定终点计费平仓。该历史反复研究，属于开发验证，不是未触碰最终测试或独立未来市场。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(实际成交金额/此前20日ADV)冲击，参与率≤0.1%，实际不利tick/lot/最小金额及100%抵押入场上限。资金费=-q×实际结算mark×rate，流出乘1/2/3、收入不放大；永续空头无虚构现货借币。报告逐档执行数、成本占比、费用分项和资金费。缺L2/TCA/历史完整保证金阶梯，1%维持保证金＋闭合小时不利mark仅代理，不保证tick清算安全或实盘容量。

门槛保持：全期/近期三档净正，1倍月正折≥9/12且近期≥6/8，3倍完整连续净值最大DD≤25%，三维排序索引半径1含自身邻域3倍净正≥60%，至少4往返、(参考毛利＋资金费)/执行成本≥2.5，现金/拒单/独立银行风险代理违规0，终点空仓且≥180日。旧12格资格不按新邻域重评级。6图36面板，114成本行、1482全期折、912近期折、26712新日边界、66敏感性边与144匹配对照留档。

结果：{"new_financial_configs": 24, "new_native_components": 12, "new_passive_parents": 12, "passed_candidates": 0, "rejected_candidates": 24, "positive_configs_by_cost": {"1": 24, "2": 24, "3": 23}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 12, "recent40_six_of_eight_positive5d_1x_folds": 23, "positive_all_costs": 1, "recent40_positive_all_costs": 2}, "by_scope": {"native": {"new": 12, "passed": 0, "best_full3": {"name": "entrygate370_ETH_N3000_H01_S31_L5", "return3_pct": 11.672808531780209, "whole_DD3_pct": 4.938587334535416, "recent_return3_pct": 0.7387744976101729, "positive_months1": 9, "positive_recent1": 2, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 12, "passed": 0, "best_full3": {"name": "entrygate370_parent_B1000_E3000_H01_S31_L5", "return3_pct": 6.836851506290675, "whole_DD3_pct": 3.127122405491767, "recent_return3_pct": 0.5802542696403012, "positive_months1": 9, "positive_recent1": 4, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 114, "full_folds": 1482, "recent40_folds": 912, "daily_NAV": 26712, "edges": 66, "reference_comparisons": 144}}

原H4/ETH慢28反转3日冻结候选和旧SMA按完整原账本从UTC20:30续接至22:30，不重复08/16资金费，不改长期规则/本金/持仓，不强制截止平仓。依据真实已闭合行情延迟重建，不是十策略实时报价账户或成熟长期资格；paper10只读，partial观察rejected不取消原计划。下个00:01日事件必须由原冻结日决策规则续接并独立核验，不能沿用仅mark驱动跨越。

背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本加密阈值/周期规则是研究推论，不是论文复现或利润/容量移植。24个新相关试验及既往全部试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号、Decimal费用/资金费、风险和完整净值；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读真实证据，不重新reserve/evaluate/summarize已完成配置。main普通非强推、完整远端tree/blob/行情SHA验证后释放本轮锁，不建其他分支/定时任务或重部署。

阈值验证结论：1%和3%新配置共24项全部淘汰。23项近期不足6/8；唯一近期达6/8的H1/S28/L3父组合月度仅7/12，3倍全期收益1.281245%、连续整体回撤4.562546%，仍不合格。H1/S28/L4原生在3倍成本下净亏损0.744564%、整体回撤10.114057%，完整账本保留。2个高阈值原生近期3倍净负亦保留。相邻的全期正收益平台不能代替分折/成本稳定性，不改变旧H2资格或原未来账户。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

12个新ETH原生路径的独立核验实际覆盖：2730笔成交、39960条含空仓的真实资金费结算、13320次日决策，以及86820个独立状态/小时不利价格风险检查；整数ROC阈值判断、实际数量、tick/lot、Decimal费用与资金费、完整现金/持仓分段及每个NAV点均核验。全部原生与父组合按原失败门槛淘汰，不以良好的全期收益或通过核算审计替代稳健性资格。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|entrygate370_ETH_N3000_H01_S31_L5|16.715349|14.194162|11.672809|4.938587|0.738774|9/12|2/8|rejected|
|entrygate370_ETH_N3000_H03_S28_L4|11.508111|10.003449|8.498618|3.979698|1.115554|11/12|3/8|rejected|
|entrygate370_ETH_N3000_H03_S28_L5|10.660736|9.343698|8.026740|4.440367|-0.115331|10/12|1/8|rejected|
|entrygate370_ETH_N3000_H03_S28_L3|10.246749|8.549076|6.849887|4.342843|1.250493|9/12|4/8|rejected|
|entrygate370_parent_B1000_E3000_H01_S31_L5|9.854746|8.345841|6.836852|3.127122|0.580254|9/12|4/8|rejected|
|entrygate370_ETH_N3000_H01_S31_L3|11.628467|9.008793|6.387969|6.527508|1.674610|8/12|4/8|rejected|
|entrygate370_ETH_N3000_H03_S31_L4|8.749044|7.302036|5.854722|3.665017|0.353249|8/12|1/8|rejected|
|entrygate370_ETH_N3000_H03_S31_L5|8.470195|7.161304|5.852603|4.913388|-0.080717|8/12|1/8|rejected|
|entrygate370_parent_B1000_E3000_H03_S28_L4|7.251127|6.250484|5.249756|2.357059|0.771102|9/12|5/8|rejected|
|entrygate370_ETH_N3000_H03_S31_L3|8.583791|6.891724|5.198468|4.410901|1.496735|9/12|3/8|rejected|
|entrygate370_parent_B1000_E3000_H03_S28_L5|6.827439|5.920609|5.013817|2.824125|0.137793|10/12|3/8|rejected|
|entrygate370_parent_B1000_E3000_H03_S28_L3|6.620445|5.523298|4.425391|2.797822|0.836910|10/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H01_S31_L3|7.311305|5.753156|4.194432|3.889943|1.050309|8/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H03_S31_L4|5.871593|4.899778|3.927808|2.574449|0.379754|7/12|3/8|rejected|
|entrygate370_parent_B1000_E3000_H03_S31_L5|5.732168|4.829411|3.926749|3.382683|0.158163|8/12|3/8|rejected|
|entrygate370_ETH_N3000_H01_S31_L4|8.676957|6.253624|3.829564|5.363027|0.955124|8/12|2/8|rejected|
|entrygate370_ETH_N3000_H01_S28_L5|8.777024|6.264928|3.752363|8.693798|0.846960|8/12|3/8|rejected|
|entrygate370_parent_B1000_E3000_H03_S31_L3|5.788967|4.694621|3.599681|2.819997|0.957472|9/12|4/8|rejected|
|entrygate370_parent_B1000_E3000_H01_S31_L4|5.835550|4.375571|2.915229|3.585302|0.682887|10/12|4/8|rejected|
|entrygate370_parent_B1000_E3000_H01_S28_L5|5.885583|4.381224|2.876629|4.984530|0.628508|8/12|5/8|rejected|
|entrygate370_parent_B1000_E3000_H01_S28_L3|4.433205|2.857658|1.281245|4.562546|1.170261|7/12|6/8|rejected|
|entrygate370_parent_B1000_E3000_H01_S28_L4|3.701511|2.165009|0.628165|5.907997|0.519273|9/12|5/8|rejected|
|entrygate370_ETH_N3000_H01_S28_L3|5.872269|3.217797|0.561595|8.301088|1.956106|7/12|5/8|rejected|
|entrygate370_ETH_N3000_H01_S28_L4|4.408879|1.832498|-0.744564|10.114057|0.634631|7/12|3/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 0.9444444444444444, "recent40_3x_positive_Sharpe_fraction": 0.8888888888888888, "full3x_positive_net_fraction": 0.9444444444444444, "recent40_3x_positive_net_fraction": 0.8888888888888888, "highest_observed_full3x_net_cell": "entrygate370_ETH_N3000_H01_S31_L5", "highest_observed_is_on_axis_boundary": {"return_hurdle": true, "trend_lookback_days": true, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 8, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "entrygate370_parent_B1000_E3000_H01_S31_L5", "highest_observed_is_on_axis_boundary": {"reversal_return_hurdle": true, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 6, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 12, "recent40_six_of_eight_positive5d_1x_folds": 23, "positive_all_costs": 1, "recent40_positive_all_costs": 2}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。114成本行、1482全期折、912近期折、26712新日边界、66敏感性边、144匹配对照完整留档；6图36面板已实际打开。
独立只读核验8旧原生/24成本曲线、1512条已保存成交与26640条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；12个新原生实际执行并独立核验整数信号/Decimal成交、资金费和完整净值。24新配置72成本场景共39240936完整NAV点、1008全期/逐折和648近期/逐折指标通过；15旧唯一结果SHA/资格保持，9398受保护文件不变。30新实际ID各自finish，60事件仅追加。
只读监控实际检查exit0：7620研究项，157既有paper观察/10账户；7596旧展示行完整字典不变。原候选累计1379点/场景、1349分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计37376点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录1项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
