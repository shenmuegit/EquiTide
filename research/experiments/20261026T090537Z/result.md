# 20261026T090537Z BTC退出带宽与门槛反转预算的五维敏感性

真实新评估108组合/324个1/2/3倍成本场景：2通过/106淘汰。全部逐项先reserve，计算、独立核验后finish；负收益/零收益/失败门槛完整保存。全文读取17186事件/8489ID与190份旧结论，初始16均有真实历史证据。复用90完整原生账本/270成本NAV原SHA，源信号/撮合/资金费模型重跑0。

预设BTC顺趋势ROC31日、入场4%、退出E0.5/1/2%；ETH慢趋势约束反转S7/14/28日、短L1/2/3日、H2/4/6%，ETH_N1000/2000/3000且BTC_N=4000-ETH_N。N×S×L×H×E完整243格五维网格，810相邻边；旧N2000三退出81项及旧非对称预算E1%54项共135控制只读，108缺格（N≠2000且E≠1%）才是新配置。原070542历史合格候选完整spec/参数/资格/报告SHA不变；本轮是BTC退出敏感性，不是其独立前向验证，不根据结果切换旧候选。

原值权重1/1代表两个各10000USDT完整独立银行，父本金20000，总固定入场预算4000占初始本金20%。1000/3000为风险预算，不自动归一化资本或按NAV复利。各源新入场按N/此前完整close/lot向下取整，同向保留实际q；不缩放旧NAV替代新手数。本轮所用每种N的真实源路径均已有实际结果，按保存cash/q/entry与真实价格恢复后核对每条原NAV SHA。无转账、交叉保证金、现金生息、父再平衡或额外父成交。

BTC前一完整close的31日ROC>4%多、<-4%空，带内实际多头仅ROC>-E保持，空头仅ROC<E保持；退出等号平仓，入场等号不新开，反向极端先平后开。ETH短ROC>H空、<-H多；带内实际多头仅ROC<0保持、空头仅ROC>0保持，过零退出；慢ROC>0仅许多、<0仅许空、=0全平，不兼容平实际仓位，无隐藏desired，现金重入须新严格极端。均只用此前完整close，次日UTC00:01 OPEN执行。完整规则、实际数量、费用和风险路径由源spec/账本/报告指纹固定。

真实Binance8合并Parquet＋16年度/近期源文件留忽略data并固定路径/字节/版本/SHA。连续OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日、33日上下文；12完整30日折＋10日尾折，至少9/12完整月净正，尾折保留但不计门槛。近期Sep14-Oct24继承日330决策前状态，8个连续5日折至少6/8净正且各成本净正，无本金/仓位重开或诊断成交。无拟合模型/未来标签、purge不适用，因果执行及初始3日embargo保持。全部历史已反复使用，不称未触碰最终测试。

每原生每侧5bp手续费＋1bp半价差＋2bp滑点，冲击0.5×滞后20日对数波动×sqrt(订单参考金额/滞后20日ADV)，参与率≤0.1%；真实lot/不利tick/最小金额与各源独立现金约束。真实资金费按结算时点/mark及当时q入账，流出×k、流入不放大，未来公开费率不用于信号/数量。永续空头以现金保证金，不虚构现货借贷。缺历史L2/队列/TCA/完整阶梯，1%维持保证金＋小时不利mark高低价仅代理；完整分钟交易代理/小时mark/结算NAV回撤不称tick级清算保证。复用不等于零费用。

三项验证已执行：13时间折、8近期折、连续OOS整体DD；243格五维敏感性及810边、Sharpe/Calmar/边界诊断；324新1/2/3倍成本场景。其他预设门槛3x整体DD≤25%、局部五维3x净正≥60%、至少4往返、(参考价毛利＋资金费)/执行成本≥2.5、各源现金/拒单/保证金代理违规0、终点空仓。旧135资格维持原三维/四维定义，只将原指标用于新邻域，不重评级。

全期1/2/3倍成本净正数量{'1': 105, '2': 104, '3': 97}，近期{'1': 100, '2': 100, '3': 100}；失败门槛{'nine_of_twelve_positive_complete30d_1x_folds': 50, 'recent40_six_of_eight_positive5d_1x_folds': 106, 'positive_all_costs': 11, 'gross_plus_funding_to_cost1_gte2_5': 6, 'recent40_positive_all_costs': 8}。全期最佳{'name': 'exitbudget370_B1000_E3000_S28_L3_H02_X050', 'full_return3_pct': 6.308708983366418, 'whole_DD3_pct': 3.2575347331928683, 'recent_return3_pct': 1.2583468344960602, 'recent_DD3_pct': 1.7813913175972251, 'positive_complete30d_folds1': 10, 'positive_recent5d_folds1': 6, 'status': 'passed', 'failed_criteria': []}；近期最佳{'name': 'exitbudget370_B1000_E3000_S7_L3_H02_X200', 'full_return3_pct': 4.576527070886849, 'whole_DD3_pct': 3.803717976421239, 'recent_return3_pct': 1.4869773135204323, 'recent_DD3_pct': 0.6399139336416559, 'positive_complete30d_folds1': 9, 'positive_recent5d_folds1': 4, 'status': 'rejected', 'failed_criteria': ['recent40_six_of_eight_positive5d_1x_folds']}。

ETH_N1000：{'configs': 54, 'passed': 0, 'full_positive3': 54, 'recent_positive3': 54, 'full3_range_pct': [0.7798298566539685, 5.161922551420695], 'recent3_range_pct': [0.4272460304831638, 1.0479505931716648], 'positive_complete30d_folds1_counts': {8: 14, 9: 40}, 'positive_recent5d_folds1_counts': {4: 54}, 'failed_criteria_counts': {'nine_of_twelve_positive_complete30d_1x_folds': 14, 'recent40_six_of_eight_positive5d_1x_folds': 54}}

ETH_N3000：{'configs': 54, 'passed': 2, 'full_positive3': 43, 'recent_positive3': 46, 'full3_range_pct': [-4.760967534235972, 6.308708983366418], 'recent3_range_pct': [-0.38006555779787066, 1.4869773135204323], 'positive_complete30d_folds1_counts': {7: 12, 9: 14, 8: 14, 5: 3, 6: 6, 4: 1, 10: 4}, 'positive_recent5d_folds1_counts': {5: 12, 4: 40, 6: 2}, 'failed_criteria_counts': {'positive_all_costs': 11, 'nine_of_twelve_positive_complete30d_1x_folds': 36, 'recent40_six_of_eight_positive5d_1x_folds': 52, 'gross_plus_funding_to_cost1_gte2_5': 6, 'recent40_positive_all_costs': 8}}

每个新组合对照同N/S/L/H的旧BTC退出1%和相同预算恒多/现金，648个逐成本对照完整保留。90原生＋135旧父＋3恒多共228旧唯一结果原状态/资格/报告字节/登记SHA不变。不同BTC退出源组件为真实新组合，不因family相同排除；仅改名、顺序、数字格式不算新配置。

原SMA65/对称1%、BTC1500/ETH500从UTC06:30现金状态续至2026-10-26T08:30:00Z，新增120闭合分钟mark，零日决策/参考/成交，旧34975点严格继承、新总35095点。Oct26UTC00:01BTC退出已完成不重复；下一日2026-10-27UTC00:01、终点2027-03-31不变。逐币逐成本cash/units/desired/费用/成交完整延续，不从2000本金重开。

旧SMA继续历史Float手数/10bp模型，不套新永续5bp/lot/tick；24日延迟shadow不足180日/六折，非paper10实盘报价模拟，也非070542候选的独立前向。最近65日日线上下文仍010010/forward_inputs.json.gz及原SHA，当前mark-only输入仅分钟数组，下一日不得误作日线。所有既有冻结账户/本金/持仓保持。

本轮读AQR官方[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）和[交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统12月期货趋势与股票反转成本只作背景；加密双币S/L/H/预算/BTC退出研究为本轮推断，不是论文复现或利润/容量移植。108相关新组合依赖已见历史，不能称独立确认、DSR/PBO校正或稳定实盘盈利。旧候选需单独预定的新数据前向验证，尚无该候选的独立前向收益。

复现目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_alignment.py读取已finish证据，forward.py --reproduce及audit_forward.py不HTTP/写登记。不要重新reserve/evaluate/summarize已finish精确配置；本轮计算/审计/汇总/finish分阶段记录实际退出，避免长会话结束丢失回执。行情留忽略data，保留完整账本与核验必要证据，只清本轮可重建缓存。普通SSH非强推main，freshfetch/全heads/完整tree及必要blob/data/report核验后释放本轮broker；发布回执留.git。

历史通过候选的冻结spec/报告/账本SHA与实际三档收益见candidate_validation.json。仅将原始指标作只读邻域诊断，不重评级旧控制。
exitbudget370_B1000_E3000_S28_L3_H02_X050：邻域全期3x净正30/32，原始近期达到6/8正折仅2/32，边界轴['ETH_fixed_entry_notional_usdt', 'trend_filter_lookback_days', 'reversal_lookback_days', 'reversal_return_hurdle', 'trend_exit_buffer_fraction']。仅满足预设历史资格，当前配置尚无独立未来证据；保留spec冻结待新数据，不将旧SMA或paper10当作其前向账户，不启动新账户、不改原持仓。
exitbudget370_B1000_E3000_S28_L3_H02_X200：邻域全期3x净正30/32，原始近期达到6/8正折仅2/32，边界轴['ETH_fixed_entry_notional_usdt', 'trend_filter_lookback_days', 'reversal_lookback_days', 'reversal_return_hurdle', 'trend_exit_buffer_fraction']。仅满足预设历史资格，当前配置尚无独立未来证据；保留spec冻结待新数据，不将旧SMA或paper10当作其前向账户，不启动新账户、不改原持仓。

根登记、snapshot、监控及逐行归属检查实际exit0；监控6357研究配置/138观察/10账户，6249旧展示行完整字典不变，exclusive-end历史别名保留。111新ID全部finish、222事件只追加；5244受保护输入和228个旧唯一结果状态/原报告SHA不变。
独立从90个保存原生账本恢复270条成本NAV、每条原SHA相同，核验12348源成交/299700源资金结算，不重跑信号、撮合或资金费模型。324新父成本场景176584212完整NAV点、4536整体/逐折及2916近期指标均核验。9张54面板图实际打开检查；243格五维及135旧控制完整保留，旧资格/原候选不重新评级。
108项新结果：2通过/106淘汰，失败门槛{'nine_of_twelve_positive_complete30d_1x_folds': 50, 'recent40_six_of_eight_positive5d_1x_folds': 106, 'positive_all_costs': 11, 'gross_plus_funding_to_cost1_gte2_5': 6, 'recent40_positive_all_costs': 8}，全期最佳{'name': 'exitbudget370_B1000_E3000_S28_L3_H02_X050', 'full_return3_pct': 6.308708983366418, 'whole_DD3_pct': 3.2575347331928683, 'recent_return3_pct': 1.2583468344960602, 'recent_DD3_pct': 1.7813913175972251, 'positive_complete30d_folds1': 10, 'positive_recent5d_folds1': 6, 'status': 'passed', 'failed_criteria': []}，近期最佳{'name': 'exitbudget370_B1000_E3000_S7_L3_H02_X200', 'full_return3_pct': 4.576527070886849, 'whole_DD3_pct': 3.803717976421239, 'recent_return3_pct': 1.4869773135204323, 'recent_DD3_pct': 0.6399139336416559, 'positive_complete30d_folds1': 9, 'positive_recent5d_folds1': 4, 'status': 'rejected', 'failed_criteria': ['recent40_six_of_eight_positive5d_1x_folds']}。旧候选保持原spec/资格，新增历史敏感性不能充作独立前向验证。
真实状态/成交分段核验近期1x始终现金原生数量{'BTC': 0, 'ETH': 39}，新父活动归属{'both_cash': 0, 'BTC_cash_ETH_active': 0, 'ETH_cash_BTC_active': 52, 'both_active': 56}。全243格三倍净正及Sharpe正占比0.9135802469135802/0.9218106995884774；陡变/边界最优限制见surface_diagnostics，仅只读指标，不加试验或改变门槛。现金腿不贡献持续alpha。
原SMA续至2026-10-26T08:30:00Z，三倍累计-7.468957811529354%，每场景35095点、旧34975点严格不变，追加120闭合分钟mark/0成交。研究报告10576080字节、forward报告5892647字节按已finish原字节保留；108父结果、90完整旧原生账本、135旧父与3同预算恒多、恒多控制及2份原HTTP响应为审计/重放必需。8合并＋16源Parquet留忽略data和哈希/复现路径。本轮无可重建checkpoint、重复研究下载页、磁盘NAV或字节码缓存。
read_failures记录本轮实际失败0项，所有最终必要门禁实际exit0；此前轮次失败事实保持。未重算已完成精确配置、改已finish报告、调整冻结账户或下真实订单。普通SSH非强推main，freshfetch/独立全heads/完整tree与必要blob/data/report核验后释放本轮broker；发布/释放回执留.git，不回写结果。
原候选独立前向计划candidate_prospective_plan已固定，拟2026-10-27UTC00:01至2027-04-25UTC00:01共180日；资金计划为两独立10000、N1000/3000，规则和费用沿原spec。当前执行器待准备、账户/观测/收益均未创建；计划本身不计实际评估、未reserve未来窗口，不冒充已经开始。下一轮优先准备并核验增量观察器，实际窗口前逐项预登记，旧SMA/paper10不变。
