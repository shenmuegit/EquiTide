# 20261027T051247Z ETH反转速度与独立入场金额交互验证

实际计算90新候选组合/270成本场景：0历史通过、90淘汰。逐项先成功reserve才计算；所有正负结果保留。全文读取19636事件/9714ID、200份既往结论，初始16项均有实际历史证据。

本轮事前固定BTC ROC31日/H2%/退出1%；ETH反转回看1/2/3日×慢趋势28/31日×阈值2/4/6%，联合BTC_N、ETH_N各1000/2000/3000。完整NB×NE×S×ETH_H×ETH_L五维162格：72旧只读＋90缺格、513相邻边；9同预算恒多均旧控制。完整源组件对、原1/1、父本金与时间边界查重，名称/顺序/等价数字格式不算新配置。

原值1/1代表两个各10000USDT独立银行，父本金20000。N是新入场固定名义金额，合计2000..6000占初始父本金10%..30%，不是资金权重，不归一化、不复利调仓/转账/交叉保证金/再平衡。直接使用原N与原回看周期的真实cash/q/entry/成本/资金费/风险路径，不缩放净值；反转速度改变真实敞口和换手，同预算不等于等实现风险。

BTC此前完整31日ROC严格>2%多/<-2%空，带内多仅ROC>-1%、空仅ROC<1%保持，相反极端先平再反开。ETH此前完整L=1/2/3日ROC>H反转空/<-H反转多，带内多仅ROC<0、空仅ROC>0保留，过零退出；慢ROC28/31日正仅许多、负仅许空、零空仓，不兼容即平实际仓位，现金重入须新极端，无隐藏desired。UTC00:01 OPEN执行，q=floor(N/此前完整close/lot)，不以未来OPEN/资金费决定信号或手数，真实资金费先记旧仓。

57旧原生（BTC3个N、ETH54个N×慢周期×反转周期×阈值）/171成本NAV只读恢复并核对原SHA，不重跑旧信号/撮合/成本/资金费模型。共同(ns,eventcode)轴仅承接上一已完成源NAV，保留前后顺序，无插值/归一化；两绝对NAV逐点相加重算整体指标，不平均Sharpe/收益。每新项与同预算ETH反转3日旧组合、同预算恒多、现金0逐档比较。

真实8合并Parquet＋16年度/近期源文件SHA/字节固定；连续OOS2025-10-19UTC00:01至2026-10-24UTC00:01共370日，33日先验上下文、3日初始embargo，无拟合或未来标签，purge不适用。12完整30日折＋10日尾折连续carry原cash/q/entry/成本。近期40日从Sep14继承第330日决策前状态并分8×5日，不重开本金/诊断平仓。反复研究的历史仅为开发验证，不能称未触碰最终测试或独立市场证据。

每侧5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×此前20日日log波动×sqrt(金额/此前20日ADV)，参与率≤0.1%；真实不利tick/lot/最小金额、100%抵押入场。资金费=-q×真实结算mark×rate，流出乘1/2/3、收入不放大；永续空头无虚构现货借币。估计价差/滑点/冲击及1%维持保证金与闭合小时不利mark只是代理，缺L2/TCA/历史margin阶梯/tick清算，不能证明实际容量或精确清算安全。

资格在看结果前固定：三档全期/近期净正；1倍完整月至少9/12正、近期至少6/8正；3倍整体DD≤25%；五维排序索引相邻含自身邻域净正≥60%；1倍至少4往返、(参考毛利＋资金费)/执行成本≥2.5；现金/拒单/各银行风险代理违规0、终点空仓。旧72项与原候选不按新网格重评级。慢周期间隔3天、反转周期间隔1天，邻域按排序索引解释。

三项验证实际完成：13全期折、8近期折及连续完整NAV回撤；五维162格收益/回撤/Sharpe/Calmar/陡变/边界；270新成本场景。含9旧恒多共171展示格，513成本行、6669全期折、4104近期折、100170新日边界、513邻接边、540逐成本对照；6图36面板。

结果：{"new_financial_configs": 90, "new_candidate_configs": 90, "new_benchmark_configs": 0, "new_native_backtests": 0, "new_passive_parents": 90, "readonly_native_components": 57, "readonly_old_parent_cells": 72, "readonly_matched_holds": 9, "full_grid_cells": 162, "passed_candidates": 0, "rejected_candidates": 90, "positive_configs_by_cost": {"1": 79, "2": 75, "3": 39}, "recent_positive_configs_by_cost": {"1": 84, "2": 80, "3": 75}, "failed_criteria_counts": {"positive_all_costs": 51, "nine_of_twelve_positive_complete30d_1x_folds": 87, "recent40_six_of_eight_positive5d_1x_folds": 90, "local_positive3_gte60pct": 60, "gross_plus_funding_to_cost1_gte2_5": 16, "recent40_positive_all_costs": 15}, "best_full": {"name": "speedbudget370_B2000_E3000_S28_L2_H04_BH02", "full_return3_pct": 3.047437610218351, "whole_DD3_pct": 3.585839128381152, "recent_return3_pct": -0.15683862661078907, "recent_DD3_pct": 1.9138559350872053, "positive_complete30d_folds1": 7, "positive_recent5d_folds1": 4, "status": "rejected", "failed_criteria": ["nine_of_twelve_positive_complete30d_1x_folds", "recent40_positive_all_costs", "recent40_six_of_eight_positive5d_1x_folds"]}, "best_recent": {"name": "speedbudget370_B3000_E3000_S28_L2_H02_BH02", "full_return3_pct": -1.5152930601159076, "whole_DD3_pct": 7.614149998463937, "recent_return3_pct": 0.6903274146983218, "recent_DD3_pct": 2.6001821885070053, "positive_complete30d_folds1": 8, "positive_recent5d_folds1": 5, "status": "rejected", "failed_criteria": ["positive_all_costs", "nine_of_twelve_positive_complete30d_1x_folds", "recent40_six_of_eight_positive5d_1x_folds", "local_positive3_gte60pct"]}, "rows": {"cost": 513, "full_folds": 6669, "recent40_folds": 4104, "daily_NAV": 100170, "edges": 513, "reference_comparisons": 540}, "by_budget": {"B1000_E1000": {"configs": 12, "total_entry_budget_usdt": 2000, "entry_fraction_of_initial_parent": 0.1, "passed": 0, "positive3": 5, "recent_positive3": 11, "full3_range_pct": [-1.9364073015012417, 1.0054599309560652]}, "B1000_E2000": {"configs": 12, "total_entry_budget_usdt": 3000, "entry_fraction_of_initial_parent": 0.15, "passed": 0, "positive3": 5, "recent_positive3": 7, "full3_range_pct": [-3.815491870394505, 2.0783188245013573]}, "B1000_E3000": {"configs": 6, "total_entry_budget_usdt": 4000, "entry_fraction_of_initial_parent": 0.2, "passed": 0, "positive3": 3, "recent_positive3": 3, "full3_range_pct": [-4.253954965898377, 2.4421082855109244]}, "B2000_E1000": {"configs": 12, "total_entry_budget_usdt": 3000, "entry_fraction_of_initial_parent": 0.15, "passed": 0, "positive3": 5, "recent_positive3": 12, "full3_range_pct": [-2.039455501099585, 0.9024117313576774]}, "B2000_E2000": {"configs": 6, "total_entry_budget_usdt": 4000, "entry_fraction_of_initial_parent": 0.2, "passed": 0, "positive3": 3, "recent_positive3": 5, "full3_range_pct": [-2.9584912534202146, 1.5032875703668402]}, "B2000_E3000": {"configs": 12, "total_entry_budget_usdt": 5000, "entry_fraction_of_initial_parent": 0.25, "passed": 0, "positive3": 5, "recent_positive3": 7, "full3_range_pct": [-5.796977381408263, 3.047437610218351]}, "B3000_E1000": {"configs": 6, "total_entry_budget_usdt": 4000, "entry_fraction_of_initial_parent": 0.2, "passed": 0, "positive3": 3, "recent_positive3": 6, "full3_range_pct": [-1.680253603544335, 0.5449820556711504]}, "B3000_E2000": {"configs": 12, "total_entry_budget_usdt": 5000, "entry_fraction_of_initial_parent": 0.25, "passed": 0, "positive3": 5, "recent_positive3": 12, "full3_range_pct": [-4.039250916352288, 1.8545597785435852]}, "B3000_E3000": {"configs": 12, "total_entry_budget_usdt": 6000, "entry_fraction_of_initial_parent": 0.3, "passed": 0, "positive3": 5, "recent_positive3": 12, "full3_range_pct": [-5.917688227767681, 2.9267267638589223]}}}

冻结原BTC31/H4/退出1% N1000＋ETH慢28/反转3日/H2% N3000前瞻账户只续接，不随新历史速度/金额结果切换。候选与旧SMA延迟闭合行情重建从Oct27UTC02:30续至04:30，保留原现金/数量/entry/风险段/完整净值链；未成熟部分观察rejected不取消长期计划。不强制平仓，不把旧SMA或候选重建当paper10实时报价账户；paper10全部冻结账本只读。实际续接结果与哈希另见candidate_verification/forward_verification。

一手背景：[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）、[Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），此前实际访问2026-10-27、链接与版本复用。传统期货趋势/股票成本只作背景，加密速度与预算交互为推论，不是论文复现或收益/容量移植。90相关试验承受多重选择偏差，未证明DSR/PBO或稳定实盘盈利。

复现目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_definitions.py/check_alignment.py、forward.py --reproduce/audit_forward.py、audit_candidate.py只读保存证据，不再次reserve/evaluate/summarize已完成精确配置。只在main和同一branch.lock内提交非强推，经freshfetch/独立allheads/完整tree及必要blob/data/report核验后释放自己锁；不新建分支/任务、部署网页或真实下单。

较快ETH速度与同金额快3日旧对照的已完成结果只读诊断见speed_cost_diagnostics.json：三档净正79/75/39，三倍净负51。所有90项近期正折低于6/8，87项月正折低于9/12，60项邻域净正率不足60%，16项成本安全比低于2.5。最高全期收益项3倍+3.047438%、整体DD3.585839%，近期3倍−0.156839%、月7/12与近期4/8，未降低门槛或切换前向候选。

历史通过候选的冻结spec/报告/账本SHA与实际三档收益见candidate_validation.json。仅将原始指标作只读邻域诊断，不重评级旧控制。

匹配控制的真实数据进一步表明：所有90新项在1/2/3倍成本下均未超过同金额快3日旧组合。快2日45项的执行次数均少2..10次、执行成本均较低，但净收益仍全部较低；快1日仅15/45执行次数与费用更高，三倍全期45/45净负。由已保存费用与净收益差额推论，费用节约未弥补路径收益变化；不能把结果概括为较快回看必然增加换手。具体45项/周期/成本分组与范围、SHA见speed_cost_diagnostics.json。

根登记、snapshot、监控与逐行归属检查均实际exit0：7374研究配置、148既有paper观察/10账户；7284旧展示行完整字典不变。96新ID全部finish（90候选＋3真实SMA＋3原冻结候选部分观察），192事件仅追加；7301受保护文件和138旧唯一结果原资格/报告SHA保持。
本轮沿用既有4MB检查预算与README，未修改监控代码；全部7284旧展示行完整字典保持，无需重部署。
57旧原生171成本NAV原SHA一致，独立核验8694旧成交/189810旧资金费事件；270新成本场景共147153510完整NAV点、3780整体/逐折及2430近期指标；6图36面板实际打开检查。对照见budget_comparison.json。
旧SMA截止2026-10-27T04:30:00Z，36176旧点继承至36296点、0新日决策/成交，原65日上下文保留。冻结候选8个新HTTP200分页、277点/场景完整链、0新决策/成交/资金费，6次新增闭合整小时风险代理检查通过；原cash/q/entry/cost保留、无强平/重置。候选和旧SMA均为延迟闭合行情重建；paper10不是其前向结果。原观察器status静态actual_observations_created=0不代表实际数量，实际累计已finish9项、本轮3项见共享指针/complete/report。
真实非零退出失败0项见read_failures.json，原始日志/失败capture完整保留。失败如有均按真实原始回执留档，恢复只做必要工程处理，未重跑已完成的金融结果。所有最终必要门禁0。完整结果、冻结规则/账户状态/增量/登记/复现代码、2份SMA原响应、候选原响应和packet、8合并＋16源Parquet哈希保留；大行情留ignoreddata。仅清自己的可重建缓存。main普通SSH非强推，freshfetch/独立allheads/完整tree及必要blob/data/report核验后释放自己锁，发布回执仅.git。
