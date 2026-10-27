# 20261027T031246Z BTC退出缓冲与独立预算交互验证

实际计算108新候选组合/324成本场景：2历史通过、106淘汰。逐项先成功reserve才计算，正负结果全部保存。全文读取19388事件/9590ID、199份结论；初始16均已有真实历史证据。

上一轮独立预算在BTC退出1%下未修复近期正折不足。本轮事前固定BTC退出0.5/1/2%，联合BTC_N、ETH_N各1000/2000/3000、ETH慢周期28/31和入场阈值2/4/6%；ETH短反转回看固定3日，BTC仍ROC31日/H2%。完整NB×NE×S×ETH_H×BTC_exit五维162格，54旧只读＋108缺格、513相邻边；9同预算恒多均旧控制。仅改名称、顺序或等价数值不算新配置，按完整源组件对、原1/1和区间语义查重，不重跑旧原生模型。

原值1/1为两个各10000USDT独立银行，父本金始终20000；N是新入场固定名义预算，合计2000到6000占初始父本金10%到30%，不是资金权重，不归一化、不复利调仓、不转账/交叉保证金/再平衡。直接使用实际N和BTC退出对应的完整cash/q/entry/费用/资金费/风险路径，不线性缩放NAV；新退出改变持仓时间和真实敞口，同预算并不等于等实现风险。

BTC此前完整31日ROC严格>2%多/<-2%空；带内多仅ROC>-E、空仅ROC<E保持，相反完整极端先平再反开，E=0.5/1/2%。ETH此前完整3日ROC>H反转空/<-H反转多，带内多仅ROC<0/空仅ROC>0保留，过零退出；慢ROC28/31日正仅许多、负仅许空、零空仓，不兼容平实际仓位，现金重入须新极端，无隐藏desired。UTC00:01OPEN执行，q=floor(N/此前完整close/lot)，信号和手数不用未来OPEN/资金费；00:00或毫秒偏移资金费先计旧仓。

27旧原生（BTC9个N×退出、ETH18个N×慢周期×阈值）/81成本NAV只读从真实状态分段恢复并核对原SHA，不重跑旧信号/撮合/费用/资金费模型。共同(ns,eventcode)轴缺点仅承接上一已完成源NAV，保留前后顺序，无插值/归一化；两绝对NAV逐点相加重算整体指标，不平均Sharpe/收益。新项与同预算BTC退出1%旧组合、同预算恒多和现金0逐档比较。

真实8合并Parquet＋16年度/近期源文件路径/字节/SHA固定，连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01共370日；33日先验上下文、3日初始embargo，无拟合/未来标签，purge不适用。12完整30日折＋10日尾折carry原cash/q/entry/成本，近期40日从Sep14继承第330日决策前状态并分8×5日，不重开本金或诊断平仓。历史已反复研究，只作开发验证，不称未触碰最终测试或独立新数据。

继承真实1/2/3倍成本路径：每侧5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×此前20日日log波动×sqrt(金额/此前20日ADV)，参与率≤0.1%；真实不利tick/lot/最小金额、100%抵押入场上限。资金费=-q×结算mark×真实rate，流出乘k、收入不放大；永续空头无虚构现货借币。缺L2/队列/TCA/完整历史margin阶梯，闭合小时不利mark＋1%维持保证金和分钟/小时/结算NAV仅代理，不是tick级清算或容量保证。

预定资格：三档全期/近期净正，1x完整月至少9/12正、近期至少6/8正；3x整体DD≤25%，5D相邻索引含自身邻域净正≥60%，1x≥4往返、(参考毛利＋资金费)/执行成本≥2.5、现金/拒单/各银行风险代理违规0、终点空仓。旧54资格和原候选不按新邻域重评级。退出轴0.5/1/2%的间隔不等，邻域按预定排序索引，不解释为等距离。

三项验证实际执行：13全期折、8近期折和连续完整NAV回撤；5D162格净收益/Sharpe/Calmar/陡变/边界与6图36面板；324新成本场景。含9旧恒多共171展示格、513成本行、6669全期折、4104近期折、120204新日边界、513邻接边、648逐成本对照。

结果：{"new_financial_configs": 108, "new_candidate_configs": 108, "new_benchmark_configs": 0, "new_native_backtests": 0, "new_passive_parents": 108, "readonly_native_components": 27, "readonly_old_parent_cells": 54, "readonly_matched_holds": 9, "full_grid_cells": 162, "passed_candidates": 2, "rejected_candidates": 106, "positive_configs_by_cost": {"1": 108, "2": 108, "3": 108}, "recent_positive_configs_by_cost": {"1": 108, "2": 108, "3": 108}, "failed_criteria_counts": {"recent40_six_of_eight_positive5d_1x_folds": 106, "nine_of_twelve_positive_complete30d_1x_folds": 51}, "best_full": {"name": "lowentry_exitind370_B3000_E3000_S31_H06_BX005", "full_return3_pct": 7.022458907170703, "whole_DD3_pct": 3.839064299122541, "recent_return3_pct": 0.8059130292442651, "recent_DD3_pct": 1.4431130622304167, "positive_complete30d_folds1": 9, "positive_recent5d_folds1": 4, "status": "rejected", "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}, "best_recent": {"name": "lowentry_exitind370_B3000_E3000_S28_H02_BX020", "full_return3_pct": 4.077927046370244, "whole_DD3_pct": 6.790437249789982, "recent_return3_pct": 1.7104232513443618, "recent_DD3_pct": 2.795876763548355, "positive_complete30d_folds1": 10, "positive_recent5d_folds1": 5, "status": "rejected", "failed_criteria": ["recent40_six_of_eight_positive5d_1x_folds"]}, "rows": {"cost": 513, "full_folds": 6669, "recent40_folds": 4104, "daily_NAV": 120204, "edges": 513, "reference_comparisons": 648}, "by_budget": {"B1000_E1000": {"configs": 12, "total_entry_budget_usdt": 2000, "entry_fraction_of_initial_parent": 0.1, "passed": 0, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [0.9795307153524169, 2.3489266726173907]}, "B1000_E2000": {"configs": 12, "total_entry_budget_usdt": 3000, "entry_fraction_of_initial_parent": 0.15, "passed": 0, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [2.2957132396095536, 4.2371421657160235]}, "B1000_E3000": {"configs": 12, "total_entry_budget_usdt": 4000, "entry_fraction_of_initial_parent": 0.2, "passed": 2, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [3.610016825966622, 6.123151779883362]}, "B2000_E1000": {"configs": 12, "total_entry_budget_usdt": 3000, "entry_fraction_of_initial_parent": 0.15, "passed": 0, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [0.6034659459866587, 2.8047954252431007]}, "B2000_E2000": {"configs": 12, "total_entry_budget_usdt": 4000, "entry_fraction_of_initial_parent": 0.2, "passed": 0, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [1.9196484702438177, 4.693010918341756]}, "B2000_E3000": {"configs": 12, "total_entry_budget_usdt": 5000, "entry_fraction_of_initial_parent": 0.25, "passed": 0, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [3.233952056600864, 6.57902053250905]}, "B3000_E1000": {"configs": 12, "total_entry_budget_usdt": 4000, "entry_fraction_of_initial_parent": 0.2, "passed": 0, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [0.19238142203474862, 3.2482337999047095]}, "B3000_E2000": {"configs": 12, "total_entry_budget_usdt": 5000, "entry_fraction_of_initial_parent": 0.25, "passed": 0, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [1.5085639462919076, 5.1364492930033645]}, "B3000_E3000": {"configs": 12, "total_entry_budget_usdt": 6000, "entry_fraction_of_initial_parent": 0.3, "passed": 0, "positive3": 12, "recent_positive3": 12, "full3_range_pct": [2.822867532648954, 7.022458907170703]}}}

原BTC31/H4/E1 N1000＋ETH S28/L3/H2 N3000前瞻规则保持冻结。本轮只续接已有真实账户cash/q/entry/费用/资金费/小时风险段/完整NAV链，不随新历史参数结果切换；未成熟部分观察rejected不取消原180日计划。旧SMA仅从Oct27UTC00:30续接02:30闭合分钟mark，下一日决策Oct28UTC00:01，不强制平仓。两者都是延迟闭合行情重建，不是paper10实时报价账户或真实下单。实际数字和独立核验另见本轮candidate_verification/forward_verification。paper10全部冻结账本只读。

一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-27。传统期货趋势/股票费用仅作背景，加密退出和预算交互为推论，不是论文复现或利润/容量移植。108相关试验受多重选择偏差影响，无DSR/PBO校正或稳定实盘盈利证明。

复现目录/home/desktop/Documents/Codex/EquiTide；audit.py、check_sources.py、check_definitions.py、check_alignment.py及forward.py --reproduce/audit_forward.py只读已保存证据，不重新reserve/evaluate/summarize精确已完成配置。保留完整结果/账户账本/冻结规则/登记/失败/复现代码，仅清可重建缓存。只在main和同一branch.lock下提交非强推，经freshfetch/独立全heads/完整tree和必要blob/data/report核验后释放自己锁；不建分支/定时任务、重部署网页或真实下单。

历史通过候选的冻结spec/报告/账本SHA与实际三档收益见candidate_validation.json。仅将原始指标作只读邻域诊断，不重评级旧控制。
lowentry_exitind370_B1000_E3000_S28_H02_BX005：邻域全期3x净正32/32，原始近期达到6/8正折仅2/32，边界轴['BTC_fixed_entry_notional_usdt', 'ETH_fixed_entry_notional_usdt', 'trend_filter_lookback_days', 'reversal_return_hurdle', 'trend_exit_buffer_fraction']。仅满足预设历史资格，当前配置尚无独立未来证据；保留spec冻结待新数据，不将旧SMA或paper10当作其前向账户，不启动新账户、不改原持仓。
lowentry_exitind370_B1000_E3000_S28_H02_BX020：邻域全期3x净正32/32，原始近期达到6/8正折仅2/32，边界轴['BTC_fixed_entry_notional_usdt', 'ETH_fixed_entry_notional_usdt', 'trend_filter_lookback_days', 'reversal_return_hurdle', 'trend_exit_buffer_fraction']。仅满足预设历史资格，当前配置尚无独立未来证据；保留spec冻结待新数据，不将旧SMA或paper10当作其前向账户，不启动新账户、不改原持仓。

两项新历史通过配置均为BTC ROC31/H2%、N1000＋ETH慢28/反转3日/H2%、N3000；各10000独立银行，父本金20000、原1/1、初始入场总4000。只有BTC退出缓冲不同。

| BTC退出 | 1倍收益 | 2倍收益 | 3倍收益 | 3倍整体回撤 | 近期3倍收益 | 1倍月正折 | 近期正折 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0.5% | 8.581488% | 7.122918% | 5.663370% | 3.445642% | 1.266129% | 9/12 | 6/8 |
| 2% | 7.801431% | 6.333737% | 4.865076% | 3.603900% | 1.275891% | 10/12 | 6/8 |

同资金原冻结H4%/退出1%候选3倍370日收益6.2023392605370375%、整体回撤3.2575347331928683%。两项H2新候选虽满足预设历史门槛，均未同时改善原候选的全期3倍收益与回撤。不得切换正在进行的原H4前瞻账户；新候选没有独立未来盈利资格。相邻近期正折稀疏/网格边界、多重选择及重复历史限制见candidate_validation.json。

根登记、snapshot、监控与逐行归属检查均实际exit0：7284研究配置、147既有paper观察/10账户；7176旧展示行完整字典不变。114新ID全部finish（108候选＋3真实SMA＋3原冻结候选部分观察），228事件仅追加；6904受保护文件和90旧唯一结果原资格/报告SHA保持。
监控首次3MB门禁实际失败后，精确恢复上一有效汇总，保留原检查/README及原失败；仅将大小预算提至4MB。新汇总gzip实际3058863字节，所有7176旧展示行完整字典保持；8个前端源文件只读核验无3MB运行限制，无需重部署。
27旧原生81成本NAV原SHA一致，独立核验4338旧成交/89910旧资金费事件；324新成本场景共176584212完整NAV点、4536整体/逐折及2916近期指标；6图36面板实际打开检查。对照见budget_comparison.json。
旧SMA截止2026-10-27T02:30:00Z，36056旧点继承至36176点、0新日决策/成交，原65日上下文保留。冻结候选8个新HTTP200分页、155点/场景完整链、0新决策/成交/资金费，3次新增闭合整小时风险代理检查通过；原cash/q/entry/cost保留、无强平/重置。候选和旧SMA均为延迟闭合行情重建；paper10不是其前向结果。原观察器status静态actual_observations_created=0不代表实际数量，实际累计已finish6项、本轮3项见共享指针/complete/report。
真实非零退出失败4项见read_failures.json，原始日志/失败capture完整保留。仅修复公开GET传输、登记前源路径和监控文件大小预算，未重跑已经完成的金融结果；所有原始非零退出和恢复回执分别留档。所有最终必要门禁0。完整结果、冻结规则/账户状态/增量/登记/复现代码、2份SMA原响应、候选原响应和packet、8合并＋16源Parquet哈希保留；大行情留ignoreddata。仅清自己的可重建缓存。main普通SSH非强推，freshfetch/独立allheads/完整tree及必要blob/data/report核验后释放自己锁，发布回执仅.git。
