# 20261026T030210Z BTC/ETH短ROC回看不同的组合

真实评估54个新组合、162成本场景，0通过/54淘汰。全部先成功reserve，再计算并逐项finish；所有负收益、零收益和失败门槛保存。全文读取16406事件/8099ID与187份旧结论；初始16项均有真实历史证据。54原生组件/162原成本NAV只读恢复，组件信号/撮合/资金费模型重跑0。

预设两币共享慢ROC窗口S7/14/28日、入场阈值H2/4/6%；BTC短回看L_B和ETH短回看L_E独立取1/2/3日。只有L_B≠L_E的54对是新配置，27旧同L组合只读原三维资格，组成81格四维S×H×L_B×L_E网格。不同资产短期响应速度可能改变成交/空仓/亏损折时点，不预设改善或负相关，不用未来收益选择或切换参数。

原生完整规则由source指纹/spec/原报告SHA固定：以前一完整close计算短ROC，>H空、<-H多；带内已有多头仅ROC<0保持、空头仅>0保持，过零退出、反向极端先平后开。慢ROC>0仅多、<0仅空、=0全平；不兼容平实际仓位，不保留隐藏状态，现金重入必须严格短ROC极端。次日UTC00:01 OPEN执行，手数按此前close/lot向下取整，同向保留实际数量。全部54原生都有真实结果，本轮只按保存cash/q/entry/成交/结算路径重建、验证原NAV SHA，不重跑组件。

原值权重1/1表示两个各10000 USDT完整独立银行相加，本金20000，每币原生固定2000入场预算，总4000占初始本金20%。不自动归一化、NAV缩放、复利、转账、交叉保证金、现金生息或组合再平衡，无额外父成交。同档成本绝对NAV按共同纳秒/事件轴相加，只向前保留最后已完成源样本、不插值、不平均Sharpe或单币收益率。

真实Binance8合并Parquet和16原始年度/近期输入保留忽略data、版本/字节/哈希/复现路径。OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日，33日上下文；12完整30日折＋10日尾折，至少9/12完整月净正，尾折保留不计门槛。近期Sep14-Oct24继承日330决策前状态、8连续5日折，仍要求6/8正折及各成本净正，不重置本金/持仓或添加诊断成交。无拟合标签，purge不适用；全部历史已见，不称未触碰最终测试。

每个原生永续每侧5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×滞后20日对数波动×sqrt(订单金额/滞后20日ADV)，参与率≤0.1%，真实lot/不利tick/最小金额、独立1倍开仓现金约束。实际资金费按结算时间/mark入账，流出×成本倍数、流入不放大；空头用保证金，不虚构现货借贷。缺历史L2/TCA/排队/完整阶梯，1%维持保证金及小时不利高低价仅代理，混合分钟交易代理/小时mark/结算整体DD不称tick级清算保证。复用不等于零费用。

三项验证已执行：13时间折/8近期折及连续OOS整体DD；81格四维完整敏感性/216相邻边；162个新1/2/3倍成本场景。新组合还需3x整体DD≤25%、局部四维3x净正≥60%、至少4往返、(参考价毛利＋资金费)/成本≥2.5、零各源现金/拒单/保证金代理违规、各源终点空仓。旧27同L仅用原指标进入新邻域，不改变原三维资格或report_sha256。

全期1/2/3倍成本正收益数量{'1': 48, '2': 42, '3': 33}，近期对应{'1': 21, '2': 20, '3': 15}；失败门槛{'positive_all_costs': 21, 'nine_of_twelve_positive_complete30d_1x_folds': 52, 'recent40_positive_all_costs': 39, 'recent40_six_of_eight_positive5d_1x_folds': 54, 'local_positive3_gte60pct': 27, 'gross_plus_funding_to_cost1_gte2_5': 16}。全期最佳{'name': 'look370_S28_H04_BL2_EL3', 'full_return3_pct': 3.9055292995878066, 'whole_DD3_pct': 1.7531673213244559, 'recent_return3_pct': 0.5431299757469921, 'recent_DD3_pct': 0.8604518027112262, 'positive_complete30d_folds1': 8, 'positive_recent5d_folds1': 3, 'status': 'rejected', 'failed_criteria': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_1x_folds']}，近期最佳{'name': 'look370_S28_H02_BL3_EL2', 'full_return3_pct': 0.38605104259643586, 'whole_DD3_pct': 3.2628429125015845, 'recent_return3_pct': 0.8712087025075421, 'recent_DD3_pct': 1.3425300347482239, 'positive_complete30d_folds1': 8, 'positive_recent5d_folds1': 4, 'status': 'rejected', 'failed_criteria': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_1x_folds']}。

BL1_EL2：{'configs': 9, 'passed': 0, 'full_positive3': 4, 'recent_positive3': 0, 'full3_range_pct': [-2.5756504426929006, 2.394759284729253], 'recent3_range_pct': [-0.4479770982962372, 0.0], 'positive_complete30d_folds1_counts': {6: 4, 5: 1, 3: 2, 7: 2}, 'positive_recent5d_folds1_counts': {0: 5, 1: 3, 3: 1}, 'failed_criteria_counts': {'positive_all_costs': 5, 'nine_of_twelve_positive_complete30d_1x_folds': 9, 'recent40_positive_all_costs': 9, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 6, 'gross_plus_funding_to_cost1_gte2_5': 5}}

BL1_EL3：{'configs': 9, 'passed': 0, 'full_positive3': 9, 'recent_positive3': 4, 'full3_range_pct': [0.6265853577775982, 3.702459072679276], 'recent3_range_pct': [-0.007944747171451105, 0.8265393992664238], 'positive_complete30d_folds1_counts': {7: 3, 4: 2, 6: 2, 9: 1, 8: 1}, 'positive_recent5d_folds1_counts': {2: 1, 0: 4, 3: 2, 4: 1, 1: 1}, 'failed_criteria_counts': {'nine_of_twelve_positive_complete30d_1x_folds': 8, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 1, 'recent40_positive_all_costs': 5}}

BL2_EL1：{'configs': 9, 'passed': 0, 'full_positive3': 3, 'recent_positive3': 2, 'full3_range_pct': [-5.739525886025554, 0.17232247286065316], 'recent3_range_pct': [-0.29011895513436636, 0.16499689295352837], 'positive_complete30d_folds1_counts': {3: 1, 5: 3, 1: 1, 4: 2, 0: 1, 2: 1}, 'positive_recent5d_folds1_counts': {1: 2, 0: 5, 4: 1, 2: 1}, 'failed_criteria_counts': {'positive_all_costs': 6, 'nine_of_twelve_positive_complete30d_1x_folds': 9, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 8, 'gross_plus_funding_to_cost1_gte2_5': 6, 'recent40_positive_all_costs': 7}}

BL2_EL3：{'configs': 9, 'passed': 0, 'full_positive3': 8, 'recent_positive3': 4, 'full3_range_pct': [-0.044688890555677485, 3.9055292995878066], 'recent3_range_pct': [-0.007959559610637434, 0.8319163691554943], 'positive_complete30d_folds1_counts': {8: 4, 5: 1, 4: 1, 6: 2, 7: 1}, 'positive_recent5d_folds1_counts': {2: 1, 0: 4, 3: 2, 4: 1, 1: 1}, 'failed_criteria_counts': {'nine_of_twelve_positive_complete30d_1x_folds': 9, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'positive_all_costs': 1, 'recent40_positive_all_costs': 5}}

BL3_EL1：{'configs': 9, 'passed': 0, 'full_positive3': 3, 'recent_positive3': 3, 'full3_range_pct': [-2.5478387551675197, 0.8497160068649867], 'recent3_range_pct': [-0.16799816913095622, 0.48705206496288955], 'positive_complete30d_folds1_counts': {7: 1, 4: 4, 2: 1, 6: 2, 1: 1}, 'positive_recent5d_folds1_counts': {2: 3, 0: 5, 4: 1}, 'failed_criteria_counts': {'positive_all_costs': 6, 'nine_of_twelve_positive_complete30d_1x_folds': 9, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 8, 'gross_plus_funding_to_cost1_gte2_5': 4, 'recent40_positive_all_costs': 6}}

BL3_EL2：{'configs': 9, 'passed': 0, 'full_positive3': 6, 'recent_positive3': 2, 'full3_range_pct': [-0.6469729908625599, 2.52235220479311], 'recent3_range_pct': [-0.2662330224191045, 0.8712087025075421], 'positive_complete30d_folds1_counts': {9: 1, 5: 1, 3: 2, 8: 2, 6: 1, 7: 2}, 'positive_recent5d_folds1_counts': {1: 3, 0: 4, 2: 1, 4: 1}, 'failed_criteria_counts': {'positive_all_costs': 3, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 4, 'nine_of_twelve_positive_complete30d_1x_folds': 8, 'recent40_positive_all_costs': 7, 'gross_plus_funding_to_cost1_gte2_5': 1}}

每项新配置对照两个旧同L组合：分别以L_B、L_E作为两币共同L，及同本金/预算恒多；486逐成本对照完整保留。54原生＋27旧同L＋1恒多共82旧唯一结果原状态/资格/报告字节/登记SHA不变。不同回看是新实际组件配对，不因family相同排除；仅改名、组件排列或等价数字格式不是新配置。

原冻结SMA65/对称1%、BTC1500/ETH500从上轮00:30续至2026-10-26T02:30:00Z，仅追加120闭合分钟mark，无新日决策/参考/成交；原00:01BTC卖出已在上轮发生，本轮不得重复。继承两币逐成本cash/units/desired/历史费用/成交，完整旧34615点保持，新总34735点；下一日决策仍2026-10-27 UTC00:01、终点2027-03-31不变。

两币现为现金，新增分钟NAV无价格收益不代表新alpha，也不从初始2000本金重开；原SMA保持历史Float手数、10bp手续费等旧模型，不套用新永续lot/tick/5bp。24日初期延迟shadow不足180日/六折，不冒充paper10真实报价模拟；partial rejected不取消冻结计划。最近一次65日上下文仍指向010010/forward_inputs.json.gz及原SHA，供下一日续接；当前mark-only输入仅分钟数组，不能误作日线。

本轮读取AQR官方[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）与[交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统期货12个月趋势和股票反转成本只作背景；加密双币不同1/2/3日反转回看是本轮推断，非论文复现或利润/容量移植。54个相关新试验依据已见历史，不称DSR/PBO校正、未触碰留出或稳定实盘盈利，不据回测改冻结账户。

复现目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_alignment.py读取已finish结果，forward.py --reproduce和audit_forward.py核验原SMA分钟/完整NAV/下一状态，不HTTP取数或写登记。不要重新reserve/evaluate/summarize已finish配置。真实失败如有保留，门禁以实际exit为准。只清可重建缓存/checkpoint，已finish报告原字节优先，行情留忽略data和SHA。普通SSH非强推main，经fetch/全heads/完整tree与blob/data/report核验后释放本轮broker。

根登记、snapshot、监控及逐行归属检查实际exit0；监控6060研究配置/135观察/10账户，6006旧展示行完整字典不变，exclusive-end历史别名保留。57新ID全部finish、114事件只追加；5138受保护输入和82个旧唯一结果状态/原报告SHA不变。
独立从54个保存原生账本恢复162条成本NAV、每条原SHA相同，核验6084源成交/179820源资金结算，不重跑信号、撮合或资金费模型。162新父成本场景88292106完整NAV点、2268整体/逐折及1458近期指标均核验。3张18面板图实际打开检查；旧同L行标明只读，新短回看不同组合完整保留。
54项全淘汰：全部近期正折不达6/8、52项月折不达9/12。全期最佳look370_S28_H04_BL2_EL3三倍3.9055292995878066%/整体DD1.7531673213244559%，完整月8/12、近期3/8；近期最佳look370_S28_H02_BL3_EL2近期三倍0.8712087025075421%，完整月8/12、近期4/8。正总收益及四维局部正收益占比不替代近期门槛；旧27项保持原三维资格，不重评级。
真实状态/成交分段核验近期1x始终现金原生数量{'BTC': 16, 'ETH': 13}，新父活动归属{'both_cash': 26, 'BTC_cash_ETH_active': 6, 'ETH_cash_BTC_active': 0, 'both_active': 22}。全81格三倍净正及Sharpe正占比0.6049382716049383/0.6049382716049383；陡变/边界最优限制见surface_diagnostics，仅只读指标，不加试验或改变门槛。现金腿不贡献持续alpha。
原SMA续至2026-10-26T02:30:00Z，三倍累计-7.468957811529354%，每场景34735点、旧34615点严格不变，追加120闭合分钟mark/0成交。研究报告4714507字节、forward报告5832167字节按已finish原字节保留；54父结果、54完整旧原生账本、27旧同L父、恒多控制及2份原HTTP响应为审计/重放必需。8合并＋16源Parquet留忽略data和哈希/复现路径。本轮无可重建checkpoint、重复研究下载页、磁盘NAV或字节码缓存。
read_failures记录本轮实际失败0项，所有最终必要门禁实际exit0；此前轮次失败事实保持。未重算已完成精确配置、改已finish报告、调整冻结账户或下真实订单。普通SSH非强推main，freshfetch/独立全heads/完整tree与必要blob/data/report核验后释放本轮broker；发布/释放回执留.git，不回写结果。
