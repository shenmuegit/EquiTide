# 20261028T012050Z BTC与ETH入场阈值联合敏感性验证

实际计算24个新组合/72成本场景，历史通过0、淘汰24。完整读取20636事件/10214ID、210份结论，初始16项已有真实历史证据。

事前固定BTC ROC31/H2/4/6%/退出1% × ETH反转阈值1/2/3% × 慢28/31日 × 反转3/4/5日。完整四维54格：30旧格只读、24缺失具体组件对各自先reserve再计算，135相邻边。21个旧原生/63成本NAV从实际现金/数量/entry状态分段恢复并核对原SHA；不重新运行旧信号、成交、费用或资金费模型。名称、组件顺序或等价数字不制造新配置。BTC金额1000、ETH金额3000均复用真实金额专属路径，不缩放其他金额结果。

原值1/1为两个完整10000USDT独立银行，父本金20000；入场预算4000=初始本金20%，不是目标权重或恒定风险比例。不归一化、不复利调仓、不转账/交叉保证金/再平衡/现金利息。共同(ns,eventcode)时轴上仅承接上一完成源NAV，逐点相加后重算整体收益、Sharpe、Calmar和回撤，不平均指标。逐项与同ETH阈值/周期/资金的旧BTC_H4组合、同资金恒多及解析现金0对照。

BTC此前完整31日ROC严格>H多/<-H空，带内多仅ROC>-1%、空仅ROC<1%保留，反向完整极端先平后开。ETH此前完整L日ROC严格>H反转空/<-H反转多，带内多仅ROC<0、空仅ROC>0保留，零退出；慢S日ROC正仅许多、负仅许空，零或不兼容平实际仓位，现金重入须新严格极端。00:01真实OPEN执行，q=floor(N/此前完整close/lot)*lot，不用未来OPEN/NAV/资金费或未闭合数据生成信号和手数；本轮父层无新增成交。

8真实合并Parquet与16年度/近期源SHA/字节固定。370日连续OOS为2025-10-19UTC00:01至2026-10-24UTC00:01；33日上下文、3日初始embargo，静态规则无拟合/未来标签，purge不适用。12完整30日折＋10日尾折连续承接原现金/数量/entry/费用，近期40日从day330继承状态并分8×5日，不重开本金或诊断平仓，只有原终点计费平仓。该历史反复研究，只是开发验证，不是未触碰最终测试或独立未来市场。

每侧5bp手续费＋1bp半价差＋2bp滑点＋0.5×此前20日日log波动×sqrt(成交金额/此前20日ADV)冲击，参与率≤0.1%，实际不利tick/lot/最小金额及100%抵押入场上限。真实资金费=-q×结算mark×rate，流出乘1/2/3、收入不放大；永续空头无虚构现货借币。报告逐档执行数、成本占比、分项成本与资金费。缺L2/TCA/历史完整保证金阶梯，1%维持保证金＋闭合小时不利mark仅风险代理，不保证tick清算安全或实盘容量。

原门槛不变：全期/近期三档净正，1倍月正折≥9/12、近期≥6/8，3倍完整连续OOS最大DD≤25%，四维排序相邻索引半径1含自身邻域3倍净正≥60%，至少4往返、(参考毛利＋资金费)/执行费用≥2.5，现金/拒单/独立银行风险违规0，终点空仓且≥180日。30旧格原资格不按新邻域重评。9图54面板、165成本行、2145全期折、1320近期折、26712新日边界、135敏感性边和144匹配对照完整留档。

结果：{"new_financial_configs": 24, "new_native_components": 0, "new_passive_parents": 24, "passed_candidates": 0, "rejected_candidates": 24, "positive_configs_by_cost": {"1": 24, "2": 24, "3": 23}, "failed_criteria_counts": {"nine_of_twelve_positive_complete30d_1x_folds": 10, "positive_all_costs": 1, "recent40_six_of_eight_positive5d_1x_folds": 22}, "best_full3": {"name": "coupledgate370_BH06_EH01_S31_L5_B1000_E3000", "return3_pct": 7.106080801373582, "whole_DD3_pct": 3.0094699348869214, "recent_return3_pct": 0.5902316478653136, "positive_months1": 9, "positive_recent1": 4, "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}, "rows": {"cost": 165, "full_folds": 2145, "recent40_folds": 1320, "daily_NAV": 26712, "edges": 135, "reference_comparisons": 144}}

原冻结候选和旧SMA从Oct27UTC22:30跨日至Oct28UTC00:30，完整承接各成本场景账本，不重开本金、不重复08/16旧资金费、不强制观察截止平仓。SMA按原SMA65/1%规则使用新65日上下文，00:01完成当日日决策；候选按原H4/ETH28L3规则执行实际00:00资金费与00:01日决策。独立核验完整前缀、跨日上下文、资金费前后顺序、日边界净值及风险状态。取得行情晚于参考时点，属于延迟闭合行情重建，不是paper10实时报价执行。paper10只读，短期partial的rejected不取消长期计划。

背景沿用此前2026-10-27实际访问的[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)及[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)。本加密联合阈值组合为研究推论，不是论文复现或利润/容量移植。24个相关新组合及所有既往试验有多重选择偏差，无DSR/PBO、独立长期未来资格或稳定实盘盈利证明。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py独立恢复原生已存现金/数量账本，核验共同纳秒时轴和完整组合净值；check_sources.py、audit_candidate.py、audit_forward.py及forward.py --reproduce只读已存证据，不重新reserve/evaluate/summarize已完成配置。main普通非强推，完整远端tree/blob/行情SHA验证后释放自己锁；不建分支、定时任务、重部署或真实订单。

历史通过项目只读冻结检查：0项。完整spec/来源/报告/账本SHA见candidate_validation.json；不改原冻结L3未来账户。

新组合22项近期不足6/8；另2项虽达到近期6/8，完整月正折仍低于9/12，全部淘汰。唯一3倍全期负收益配置BTC_H2/ETH_H1/S28/L4净亏损0.441087%、完整连续OOS最大回撤6.566942%，完整证据保留；不以较高全期收益放宽门槛。只读明细见coupled_threshold_diagnostics.json。
跨日候选实际核验：6个按币种/成本场景计的日决策，6条资金费记录，0新增成交。BTC持有-0.012，Oct28UTC00:00.001按mark80868.40、rate0.00005373，各成本档实际收入0.052140709584USDT，收入不放大；ETH空仓结算0。00:01 BTC维持原空头持仓、ETH保持空仓。前1379点与原现金/数量/entry/累计成本精确承接，本窗口127新事件键至1506点/场景，日边界增至2，34日滚动上下文和完整00小时风险状态留给下一窗口；未重复旧08/16结算。旧SMA两币各1次冻结日决策，无新成交，保留37376旧点并追加120分钟与1个日执行参考至37497点，65日上下文/64日重叠核验通过。仍只是初期延迟观察，非长期前向资格。

逐配置结果（收益/回撤单位%，三倍全期回撤使用完整连续OOS）：

|配置|1x收益|2x收益|3x收益|3x最大回撤|近期3x收益|1x月正折|1x近期正折|结论|
|---|---:|---:|---:|---:|---:|---:|---:|---|
|coupledgate370_BH06_EH01_S31_L5_B1000_E3000|9.994891|8.550528|7.106081|3.009470|0.590232|9/12|4/8|rejected|
|coupledgate370_BH02_EH01_S31_L5_B1000_E3000|8.942898|7.355298|5.767599|3.314741|0.586155|8/12|4/8|rejected|
|coupledgate370_BH06_EH03_S28_L4_B1000_E3000|7.391272|6.455172|5.518985|2.456262|0.780780|9/12|5/8|rejected|
|coupledgate370_BH06_EH03_S28_L5_B1000_E3000|6.967584|6.125296|5.283046|2.874576|0.148981|10/12|3/8|rejected|
|coupledgate370_BH06_EH03_S28_L3_B1000_E3000|6.760590|5.727985|4.694620|2.840469|0.846507|10/12|5/8|rejected|
|coupledgate370_BH06_EH01_S31_L3_B1000_E3000|7.451450|5.957843|4.463661|3.556939|1.059418|8/12|5/8|rejected|
|coupledgate370_BH06_EH03_S31_L4_B1000_E3000|6.011738|5.104465|4.197038|2.242671|0.390486|8/12|3/8|rejected|
|coupledgate370_BH06_EH03_S31_L5_B1000_E3000|5.872313|5.034099|4.195978|3.054198|0.169419|9/12|3/8|rejected|
|coupledgate370_BH02_EH03_S28_L4_B1000_E3000|6.339280|5.259941|4.180503|2.417327|0.779078|9/12|5/8|rejected|
|coupledgate370_BH02_EH03_S28_L5_B1000_E3000|5.915592|4.930066|3.944565|2.829377|0.139213|10/12|3/8|rejected|
|coupledgate370_BH06_EH03_S31_L3_B1000_E3000|5.929112|4.899309|3.868910|2.862899|0.966856|9/12|4/8|rejected|
|coupledgate370_BH02_EH03_S28_L3_B1000_E3000|5.708598|4.532755|3.356138|2.811180|0.845641|10/12|5/8|rejected|
|coupledgate370_BH06_EH01_S31_L4_B1000_E3000|5.975695|4.580259|3.184458|3.250674|0.692997|9/12|4/8|rejected|
|coupledgate370_BH06_EH01_S28_L5_B1000_E3000|6.025728|4.585911|3.145858|4.793023|0.638753|8/12|5/8|rejected|
|coupledgate370_BH02_EH01_S31_L3_B1000_E3000|6.399458|4.762613|3.125179|4.079363|1.061315|9/12|5/8|rejected|
|coupledgate370_BH02_EH03_S31_L4_B1000_E3000|4.959746|3.909235|2.858556|2.765218|0.383716|7/12|3/8|rejected|
|coupledgate370_BH02_EH03_S31_L5_B1000_E3000|4.820321|3.838869|2.857496|3.570302|0.159810|8/12|3/8|rejected|
|coupledgate370_BH02_EH03_S31_L3_B1000_E3000|4.877120|3.704078|2.530429|2.982577|0.967554|9/12|4/8|rejected|
|coupledgate370_BH02_EH01_S31_L4_B1000_E3000|4.923702|3.385029|1.845977|3.776122|0.690106|9/12|4/8|rejected|
|coupledgate370_BH02_EH01_S28_L5_B1000_E3000|4.973736|3.390681|1.807376|5.630055|0.635151|8/12|5/8|rejected|
|coupledgate370_BH06_EH01_S28_L3_B1000_E3000|4.573351|3.062346|1.550474|4.371485|1.179334|8/12|6/8|rejected|
|coupledgate370_BH06_EH01_S28_L4_B1000_E3000|3.841656|2.369696|0.897394|5.717151|0.530014|8/12|5/8|rejected|
|coupledgate370_BH02_EH01_S28_L3_B1000_E3000|3.521358|1.867115|0.211992|5.219460|1.182895|7/12|6/8|rejected|
|coupledgate370_BH02_EH01_S28_L4_B1000_E3000|2.789664|1.174466|-0.441087|6.566942|0.524879|9/12|5/8|rejected|

全网格Sharpe正值比例、收益正值比例及最高观测单元边界诊断（只读已有结果，不改变资格）：{"parent": {"dimension_count": 4, "cells": 54, "full3x_positive_Sharpe_fraction": 0.9814814814814815, "recent40_3x_positive_Sharpe_fraction": 1.0, "full3x_positive_net_fraction": 0.9814814814814815, "recent40_3x_positive_net_fraction": 1.0, "highest_observed_full3x_net_cell": "coupledgate370_BH06_EH01_S31_L5_B1000_E3000", "highest_observed_is_on_axis_boundary": {"BTC_return_hurdle": true, "reversal_return_hurdle": true, "trend_filter_lookback_days": true, "reversal_lookback_days": true}, "descriptive_full_Sharpe_cliff_edges": 24, "old_qualifications_preserved": true, "not_untouched_test_or_global_optimum": true}}。最高观测单元的预设网格边界标记已保存，不称全局最优；全期平台不能消除近期正折不足。

实际失败门槛计数：{"nine_of_twelve_positive_complete30d_1x_folds": 10, "positive_all_costs": 1, "recent40_six_of_eight_positive5d_1x_folds": 22}。逐项真实结论见上表和report.json，不因全期收益正而放宽门槛。165成本行、2145全期折、1320近期折、26712新日边界、135敏感性边、144匹配对照完整留档；9图54面板已实际打开。
独立只读核验21旧原生/63成本曲线、4452条已保存成交与69930条已保存资金费记录，原完整NAV SHA保持；没有原生模型重跑或父层新增成交。24新组合72成本场景共39240936完整NAV点、1008全期/逐折和648近期/逐折指标通过；52旧唯一结果SHA/资格保持，9609受保护文件不变。30新实际ID各自finish，60事件仅追加。
只读监控实际检查exit0：7644研究项，158既有paper观察/10账户；7620旧展示行完整字典不变。原候选累计1506点/场景、1469分钟，新增6个按币种/成本场景的因果日决策、0成交，实际新增资金费记录6条；现金与资金费逐条独立核验，收入不随成本放大，08旧结算未重复；旧SMA累计37497点，两币各完成1个SMA65日决策、0新成交；已独立核验新65日上下文及64日重叠。两者均非十策略实时报价执行或长期盈利证据。
真实命令/传输异常记录1项，见read_failures.json。本轮登记、账户续接及提交由持续stdin排他锁保护。所有真实负收益分折/近期、成功/失败和完整账户账本保留；行情与HTTPpacket留ignoreddata并绑定SHA，不提交大行情或凭据。main普通非强推，freshfetch/独立allheads/完整tree/blob/行情核验通过后释放自己锁。
