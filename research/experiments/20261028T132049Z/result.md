# 20261028T132049Z 多数表决策略的入场阈值与周期联合敏感性验证

实际计算12个新ETH原生＋12个BTC/ETH组合，共24配置/72成本场景；历史通过2、淘汰22。完整读取21036登记事件/10414ID及216份结论；初始16项已有实际证据。

事前固定多数表决规则下的ETH入场阈值2/2.5/3% × 慢中心27/28/29日 × 反转3/4日。每作用域18格，12个H2.5旧原生/父组合只读且原资格保持；H2/H3新增12原生＋12父组合先逐个成功reserve再计算。33相邻边/作用域。假设：阈值±20%扰动是否改善或破坏前轮S28的历史资格，计算前固定全部规则/金额/边界/门槛，不在本批结果上重调。

ETH前一完整L日ROC严格>H反转空/<-H反转多；带内仅实际多且ROC<0、实际空且ROC>0保留，零退出。慢门控用S−1/S/S+1三个完整ROC，至少两票严格正允许多、至少两票严格负允许空，否则平仓；快反转方向与慢多数方向一致才持仓，现金重入须新严格极端，无隐藏desired。UTC00:01实际OPEN执行，q=floor(N/前一完整close/lot)*lot；不读未来OPEN/资金费/未闭合价格决定信号或数量。引擎与112019多数规则原字节相同，仅spec阈值变化；已运行新H2/H3严格等号不入场、微小越界多空入场及未来数据不变性检查。

ETH独立银行10000、固定新入场3000；BTC固定ROC31/H4%/退出1%、银行10000、入场1000。原值1/1为两个完整独立银行，父本金20000、预算4000=初始父本金20%，不是目标权重或恒定风险；不归一化、不复利调仓、不转账/交叉保证金/再平衡。8旧原生/24成本NAV由真实已保存现金/数量/entry分段恢复并核对SHA；12新原生实际执行专属成交/成本/资金费/风险，12父组合沿共同(ns,eventcode)时轴因果承接上一个完成源点并逐点相加，整体指标重新从连续净值计算，不平均Sharpe/回撤或缩放其他金额。与同S/L的旧多数H2.5、同资金恒多及现金0比较。

8真实合并Parquet及16年度/近期源SHA/字节固定。370日连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01，33日上下文、3日初始embargo。静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续承接现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓；仅原预定终点计费平仓。该历史反复研究，属于开发验证，不是未触碰最终测试或独立未来市场。

每侧5bp费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(实际成交金额/此前20日ADV)冲击，参与率≤0.1%，实际不利tick/lot/最小金额及100%抵押入场上限。资金费=-q×实际结算mark×rate，流出乘1/2/3、收入不放大；永续空头无虚构现货借币。报告逐档执行数、成本占比、费用分项和资金费。缺L2/TCA/历史完整保证金阶梯，1%维持保证金＋闭合小时不利mark仅代理，不保证tick清算安全或实盘容量。

门槛保持：全期/近期三档净正、1倍月正折≥9/12且近期≥6/8、三倍完整连续净值DD≤25%、三维排序索引半径1含自身邻域三倍净正≥60%、至少4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/独立银行风险违规0、终点空仓且≥180日。旧H2.5十二格是同多数规则的真实参数邻居，但保持原状态，不以新邻域重评级。6图36面板、114成本行、1482全期折、912近期折、26712新日边界、66敏感性边及144匹配对照完整保存。

结果：{"new_financial_configs": 24, "new_native_components": 12, "new_passive_parents": 12, "passed_candidates": 2, "rejected_candidates": 22, "positive_configs_by_cost": {"1": 24, "2": 24, "3": 24}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 4, "recent40_six_of_eight_positive5d_1x_folds": 22}, "by_scope": {"native": {"new": 12, "passed": 0, "best_full3": {"name": "votehurdle370_ETH_H030_S28_L4_N3000", "return3_pct": 11.410515279703315, "whole_DD3_pct": 3.5284484860888643, "recent_return3_pct": 1.0860805542602048, "positive_months1": 11, "positive_recent1": 3, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}, "parent": {"new": 12, "passed": 2, "best_full3": {"name": "votehurdle370_parent_B1000_E3000_H030_S28_L4", "return3_pct": 6.705704880252239, "whole_DD3_pct": 2.1800708262104673, "recent_return3_pct": 0.7605006912305479, "positive_months1": 10, "positive_recent1": 5, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}}}, "rows": {"cost": 114, "full_folds": 1482, "recent40_folds": 912, "daily_NAV": 26712, "edges": 66, "reference_comparisons": 144}}

原单S28冻结候选和旧SMA从Oct28UTC10:30续接至12:30；承接各成本场景现金、数量、entry、费用、已计08:00资金费、已完成日决策、上下文、风险栈和完整净值链。不切换多数规则、不重开本金、不重复事件、不强制截止平仓。真实闭合数据延迟重建，区别于paper10实时报价执行；partial的rejected不取消长期计划。下一资金费16:00、下一日决策Oct29UTC00:01。

背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)与[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本多数表决与阈值/周期规则是研究推论，不是论文复现或利润/容量移植。24个新相关试验及既往全部试验存在多重选择偏差，无DSR/PBO、独立未来资格或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide。audit.py/audit_native.py独立整数信号、Decimal费用/资金费、风险和完整净值；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读真实证据，不重新reserve/evaluate/summarize已完成配置。main普通非强推、完整远端tree/blob/行情SHA验证后释放本轮锁，不建其他分支/定时任务或重部署。

本轮预检查真实失败与恢复：首次冻结脚本引用旧清单文件名，在 plan/spec/reserve 和任何金融计算前失败；随后一次手动前置断言及缺 plan 的 evaluate 请求也失败，保护条件阻止了计算。修正文件名后，24 项均先成功 reserve，金融评估仅实际执行一次，独立核验后全部 finish。原失败源码、命令退出码及日志完整保留，见 preflight_recovery.json/read_failures.json。旧 SMA 的公开 GET 出现一次可见 TLS 错误，由原 curl 重试恢复，最终阶段退出 0；未能从原合并 stderr 区分失败请求的币种，不推断。

只读逐折平台诊断：固定 L3/L4，父组合 H2/H2.5、S28 近期正折为6/8；相邻 S27/S29 均5/8，H3 的S28也降为5/8。因此两个新增通过项仍集中在S28，不能解释为宽阔的近期稳健平台。原生18格近期均不足6/8。详见 recent_platform_diagnostics.json；该诊断只读取已登记指标，不增加试验或改变旧资格。

历史通过项目只读冻结检查：2项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。
votehurdle370_parent_B1000_E3000_H020_S28_L3：1/2/3倍370日收益[8.877587891685534, 7.466158990373328, 6.05382620518613]%，整体3倍回撤3.401670309799687%，近期3倍收益1.2614092102564811%；完整月正折9/12、近期6/8，邻域全期3倍净正12/12、原始近期6/8仅4/12。仅通过预设历史门槛，尚无该新配置独立未来证据。
votehurdle370_parent_B1000_E3000_H020_S28_L4：1/2/3倍370日收益[8.452308882429316, 7.204811116940202, 5.956967390576073]%，整体3倍回撤2.9456008395056577%，近期3倍收益1.2032682055681976%；完整月正折11/12、近期6/8，邻域全期3倍净正12/12、原始近期6/8仅4/12。仅通过预设历史门槛，尚无该新配置独立未来证据。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|votehurdle370_ETH_H030_S28_L4_N3000|14.555896|12.983167|11.410515|3.528448|1.086081|11/12|3/8|rejected|
|votehurdle370_ETH_H030_S27_L4_N3000|13.565553|12.131475|10.697503|3.527041|0.901896|11/12|1/8|rejected|
|votehurdle370_ETH_H020_S29_L3_N3000|15.192021|12.913303|10.632805|5.290287|2.017539|8/12|4/8|rejected|
|votehurdle370_ETH_H030_S29_L4_N3000|13.134691|11.674281|10.214075|3.851604|1.060400|10/12|2/8|rejected|
|votehurdle370_ETH_H020_S27_L3_N3000|14.748605|12.468703|10.187113|5.515769|1.868350|8/12|3/8|rejected|
|votehurdle370_ETH_H020_S28_L3_N3000|14.761034|12.434799|10.106758|5.503984|2.065734|9/12|5/8|rejected|
|votehurdle370_ETH_H020_S28_L4_N3000|13.910476|11.912103|9.913040|4.607138|1.953337|9/12|4/8|rejected|
|votehurdle370_ETH_H020_S27_L4_N3000|13.578983|11.574857|9.569857|5.328480|1.763031|9/12|2/8|rejected|
|votehurdle370_ETH_H020_S29_L4_N3000|12.240177|10.305013|8.369426|4.884483|1.942801|8/12|3/8|rejected|
|votehurdle370_ETH_H030_S29_L3_N3000|10.655807|8.906834|7.156351|4.346030|1.208085|9/12|3/8|rejected|
|votehurdle370_parent_B1000_E3000_H030_S28_L4|8.775019|7.740343|6.705705|2.180071|0.760501|10/12|5/8|rejected|
|votehurdle370_ETH_H030_S27_L3_N3000|10.115058|8.403577|6.690996|5.022488|1.053329|8/12|2/8|rejected|
|votehurdle370_ETH_H030_S28_L3_N3000|9.793362|8.097554|6.400325|4.442479|1.255843|9/12|4/8|rejected|
|votehurdle370_parent_B1000_E3000_H030_S27_L4|8.279848|7.314497|6.349199|2.179571|0.664090|9/12|4/8|rejected|
|votehurdle370_parent_B1000_E3000_H020_S29_L3|9.093081|7.705411|6.316850|3.284946|1.238695|9/12|5/8|rejected|
|votehurdle370_parent_B1000_E3000_H030_S29_L4|8.064416|7.085900|6.107485|2.719950|0.745419|9/12|4/8|rejected|
|votehurdle370_parent_B1000_E3000_H020_S27_L3|8.871373|7.483111|6.094004|3.407698|1.160726|10/12|5/8|rejected|
|votehurdle370_parent_B1000_E3000_H020_S28_L3|8.877588|7.466159|6.053826|3.401670|1.261409|9/12|6/8|passed|
|votehurdle370_parent_B1000_E3000_H020_S28_L4|8.452309|7.204811|5.956967|2.945601|1.203268|11/12|6/8|passed|
|votehurdle370_parent_B1000_E3000_H020_S27_L4|8.286563|7.036188|5.785376|3.008019|1.104862|10/12|5/8|rejected|
|votehurdle370_parent_B1000_E3000_H020_S29_L4|7.617160|6.401266|5.185160|3.043412|1.192458|9/12|5/8|rejected|
|votehurdle370_parent_B1000_E3000_H030_S29_L3|6.824974|5.702176|4.578623|2.798868|0.815960|9/12|4/8|rejected|
|votehurdle370_parent_B1000_E3000_H030_S27_L3|6.554600|5.450548|4.345945|2.922161|0.736526|9/12|4/8|rejected|
|votehurdle370_parent_B1000_E3000_H030_S28_L3|6.393752|5.297536|4.200610|2.841555|0.838730|9/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"native": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "vote370_ETH_H025_S28_L4_N3000", "highest_observed_is_on_axis_boundary": {"return_hurdle": false, "trend_lookback_days": false, "lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 6, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}, "parent": {"dimension_count": 3, "cells": 18, "full3x_positive_Sharpe_fraction": 1.0, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 1.0, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "vote370_parent_B1000_E3000_H025_S28_L4", "highest_observed_is_on_axis_boundary": {"reversal_return_hurdle": false, "trend_filter_lookback_days": false, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 3, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 4, "recent40_six_of_eight_positive5d_1x_folds": 22}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。114成本行、1482全期折、912近期折、26712新日边界、66敏感性边、144匹配对照完整留档；6图36面板已实际打开。
独立只读核验8旧原生/24成本曲线、1326条已保存成交与26640条已保存资金费记录，原完整NAV SHA保持；没有旧原生模型重跑或父层新增成交；12个新原生实际执行并独立核验整数信号/Decimal成交、资金费和完整净值。24新配置72成本场景共39240936完整NAV点、1008全期/逐折和648近期/逐折指标通过；15旧唯一结果SHA/资格保持，10833受保护文件不变。30新实际ID各自finish，60事件仅追加。
只读监控实际检查exit0：7748研究项，164既有paper观察/10账户；7724旧展示行完整字典不变。原候选累计2240点/场景、2189分钟，0新增日决策/成交，实际新增资金费记录0条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计38217点，0新日决策/成交。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录5项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
