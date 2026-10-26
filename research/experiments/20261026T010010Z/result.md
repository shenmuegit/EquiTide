# 20261026T010010Z BTC/ETH反转阈值不同的组合与原冻结SMA日决策续接

实际评估54个新组合、162成本场景，0通过/54淘汰。全部先独立成功reserve，后计算并逐项finish；正负/零收益、失败判据完整保留。全文读取16272事件/8032ID和186份旧结论，初始16项均有真实历史证据。54原生组件/162原成本NAV只读恢复，组件信号/撮合/资金费模型重跑0。

预设慢ROC窗口S7/14/28日、短ROC回看L1/2/3日两币相同；BTC阈值H_B和ETH阈值H_E独立取2/4/6%。仅H_B≠H_E的54对为新配置，27旧同H组合只读原三维资格，组成81格四维网格S×L×H_B×H_E。不同资产波动幅度可能使不同阈值改变入场频率、共同空仓和亏损折时点，不假设改善或负相关，不按未来收益切换参数。

原生规则由source指纹/spec/原报告SHA完整固定：前一完整close计算短ROC，>H空、<-H多；带内已有多头仅ROC<0保持、空头仅>0保持，过零退出，反向极端先平后开。慢ROC>0仅允许多、<0仅允许空、=0全平；不兼容时平实际仓位，无隐藏方向，现金重入需严格短ROC极端。下一UTC00:01 OPEN成交，手数按此前close/lot向下取整，同向持有实际数量；54个原生账本已有真实结果，本轮只按保存cash/q/entry/成交/结算路径恢复并验证每条NAV SHA。

权重原值1/1表示两整本各10000 USDT独立银行相加，总本金20000，每币固定入场预算2000、总4000=初始本金20%。不归一化、不缩放原生NAV、不复利放大/转账/交叉保证金/现金生息/组合再平衡，新父无额外成交。纳秒/事件共同轴保留最后已完成样本，不插值，不平均单币Sharpe或收益率。

真实Binance8合并Parquet及16原始年度/近期输入留忽略data，保留版本/字节/哈希/复现路径。OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日，33日上下文；12完整30日折＋10日尾折，至少9/12完整月正收益，尾折保留不计门槛。近期Sep14-Oct24继承日330决策前状态，8连续5日折，仍要求6/8正折和各成本净正，无本金/持仓重置或额外诊断成交。无拟合标签、purge不适用；全历史已见，不称未触碰最终测试集。

每个原生永续每侧5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×滞后20日对数波动×sqrt(订单金额/滞后20日ADV)，参与率≤0.1%，真实lot/不利tick/最小金额/独立1倍开仓现金约束。实际资金费按真实结算时间/mark计入，流出×成本倍数、流入不放大；空头用保证金，不虚构现货借贷。缺历史L2/TCA/排队/完整阶梯，1%维持保证金及小时不利高低价为代理，混合分钟交易代理/小时mark/结算整体DD不称tick级清算保证。复用不是免费用，所有原生成交/资金费逐档计入。

三项验证已执行：13时间折/8近期折及连续OOS整体DD；81格四维网格/216相邻边；162新1/2/3倍成本场景。新组合另需3x整体DD≤25%、局部四维3x净正≥60%、至少4往返、(参考价毛利＋资金费)/执行成本≥2.5、零各源现金/拒单/保证金代理违规、各源终点空仓。旧27同H指标参加新邻域，旧原三维资格和report_sha256完全保持。

全期1/2/3倍成本正收益数量{'1': 42, '2': 33, '3': 27}；近期对应{'1': 23, '2': 23, '3': 22}。失败门槛{'positive_all_costs': 27, 'nine_of_twelve_positive_complete30d_1x_folds': 46, 'recent40_positive_all_costs': 32, 'recent40_six_of_eight_positive5d_1x_folds': 54, 'local_positive3_gte60pct': 33, 'gross_plus_funding_to_cost1_gte2_5': 23}。全期最佳{'name': 'thresh370_S28_L3_BH02_EH04', 'full_return3_pct': 4.653671727678366, 'whole_DD3_pct': 2.797850533772417, 'recent_return3_pct': 1.2680914269254773, 'recent_DD3_pct': 1.2770111629643477, 'positive_complete30d_folds1': 10, 'positive_recent5d_folds1': 4, 'status': 'rejected', 'failed_criteria': ['recent40_six_of_eight_positive5d_1x_folds']}；近期最佳{'name': 'thresh370_S28_L3_BH02_EH04', 'full_return3_pct': 4.653671727678366, 'whole_DD3_pct': 2.797850533772417, 'recent_return3_pct': 1.2680914269254773, 'recent_DD3_pct': 1.2770111629643477, 'positive_complete30d_folds1': 10, 'positive_recent5d_folds1': 4, 'status': 'rejected', 'failed_criteria': ['recent40_six_of_eight_positive5d_1x_folds']}。

BH02_EH04：{'configs': 9, 'passed': 0, 'full_positive3': 5, 'recent_positive3': 3, 'full3_range_pct': [-2.2517529832665195, 4.653671727678366], 'recent3_range_pct': [-0.4112401993206394, 1.2680914269254773], 'positive_complete30d_folds1_counts': {5: 2, 6: 2, 7: 2, 9: 2, 10: 1}, 'positive_recent5d_folds1_counts': {0: 4, 1: 2, 2: 1, 3: 1, 4: 1}, 'failed_criteria_counts': {'positive_all_costs': 4, 'nine_of_twelve_positive_complete30d_1x_folds': 6, 'recent40_positive_all_costs': 6, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 6, 'gross_plus_funding_to_cost1_gte2_5': 4}}

BH02_EH06：{'configs': 9, 'passed': 0, 'full_positive3': 4, 'recent_positive3': 4, 'full3_range_pct': [-2.151558422550115, 3.8313767302050383], 'recent3_range_pct': [-0.056515156175307446, 0.8082465084925827], 'positive_complete30d_folds1_counts': {4: 1, 6: 2, 7: 2, 11: 2, 5: 1, 8: 1}, 'positive_recent5d_folds1_counts': {0: 4, 1: 2, 2: 1, 3: 1, 4: 1}, 'failed_criteria_counts': {'positive_all_costs': 5, 'nine_of_twelve_positive_complete30d_1x_folds': 7, 'recent40_positive_all_costs': 5, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 5, 'gross_plus_funding_to_cost1_gte2_5': 4}}

BH04_EH02：{'configs': 9, 'passed': 0, 'full_positive3': 3, 'recent_positive3': 6, 'full3_range_pct': [-3.4990514101666315, 3.8454277160113737], 'recent3_range_pct': [-0.3944504316824138, 0.9006346594900405], 'positive_complete30d_folds1_counts': {4: 2, 7: 4, 6: 2, 10: 1}, 'positive_recent5d_folds1_counts': {1: 3, 0: 1, 3: 3, 4: 1, 5: 1}, 'failed_criteria_counts': {'positive_all_costs': 6, 'nine_of_twelve_positive_complete30d_1x_folds': 8, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 6, 'gross_plus_funding_to_cost1_gte2_5': 5, 'recent40_positive_all_costs': 3}}

BH04_EH06：{'configs': 9, 'passed': 0, 'full_positive3': 6, 'recent_positive3': 2, 'full3_range_pct': [-0.8817364636504177, 3.0077569952698058], 'recent3_range_pct': [0.0, 0.1707224748888514], 'positive_complete30d_folds1_counts': {2: 2, 3: 1, 4: 3, 7: 1, 6: 1, 8: 1}, 'positive_recent5d_folds1_counts': {0: 7, 1: 2}, 'failed_criteria_counts': {'nine_of_twelve_positive_complete30d_1x_folds': 9, 'recent40_positive_all_costs': 7, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 4, 'positive_all_costs': 3, 'gross_plus_funding_to_cost1_gte2_5': 2}}

BH06_EH02：{'configs': 9, 'passed': 0, 'full_positive3': 3, 'recent_positive3': 6, 'full3_range_pct': [-3.4177895888097165, 4.077770829049321], 'recent3_range_pct': [-0.39404287700612883, 0.869908091361804], 'positive_complete30d_folds1_counts': {4: 2, 7: 4, 6: 2, 11: 1}, 'positive_recent5d_folds1_counts': {1: 3, 0: 1, 3: 3, 4: 1, 5: 1}, 'failed_criteria_counts': {'positive_all_costs': 6, 'nine_of_twelve_positive_complete30d_1x_folds': 8, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 6, 'gross_plus_funding_to_cost1_gte2_5': 6, 'recent40_positive_all_costs': 3}}

BH06_EH04：{'configs': 9, 'passed': 0, 'full_positive3': 6, 'recent_positive3': 1, 'full3_range_pct': [-0.5910498145196064, 4.0623951057811025], 'recent3_range_pct': [-0.373466430133218, 0.4535271544288344], 'positive_complete30d_folds1_counts': {4: 3, 5: 2, 3: 1, 6: 1, 7: 1, 10: 1}, 'positive_recent5d_folds1_counts': {0: 6, 2: 1, 1: 1, 3: 1}, 'failed_criteria_counts': {'nine_of_twelve_positive_complete30d_1x_folds': 8, 'recent40_positive_all_costs': 8, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 6, 'positive_all_costs': 3, 'gross_plus_funding_to_cost1_gte2_5': 2}}

每个新组合对照两个旧同H组合：用H_B作为两币同H、用H_E作为两币同H，及同本金/预算恒多。486逐成本对照全部保留；54原生＋27旧同H＋1恒多共82旧唯一结果原状态/资格/报告字节/登记SHA不改。不同阈值配对是新具体配置，不因family相同排除，改名/排列不算新。

原冻结SMA65/对称1%、BTC1500/ETH500从上一22:30续至2026-10-26T00:30:00Z，跨过2026-10-26 UTC00:01日决策。每币使用65根已闭合日线、64根原始重叠逐字核对，信号到执行间隔1分钟，成本只用滞后20日ADV/波动。新增120闭合分钟mark、1个日决策参考/场景及合计3个原规则虚拟成交；完整旧34494点精确保持，新总34615点。逐成本继承旧cash/units/desired/成本/成交，不重置或重复首笔，不把规则退出改作截点强制卖出。下一决策2026-10-27T00:01:00Z、终点2027-03-31不变。

原SMA保留历史Float手数及其原始每侧10bp手续费、1bp半价差、2bp滑点和20日ADV冲击，不套用新永续5bp/lot/tick规则。它是延迟真实历史bar重建，24日初期观察不足180日/六折，不称同时成交或paper10真实报价；partial rejected不取消冻结计划。日线/分钟的原始4页和重叠/完整性/价格一致性检查保存。一次只读源码查找旧模块不存在的verify函数发生ValueError，原日志在read_failures；使用已有Oct25日续接器后续，不改冻结模型。

本轮读取AQR官方[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）和[交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统期货12月趋势、股票反转成本仅作背景，2/4/6%加密双币阈值不同是本轮推断，非论文复现或利润/容量移植。54相关新试验基于已见历史，不称DSR/PBO、未触碰留出或稳定实盘盈利，不据回测更改冻结账户。

复现目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_alignment.py读取已finish研究结果，forward.py --reproduce和audit_forward.py核验原SMA日线/分钟/信号/费用/余额/完整NAV及下一状态，不HTTP取数/写登记。不要重新reserve/evaluate/summarize已finish配置。真实失败保留，门禁以实际exit为准。只清可重建缓存/checkpoint，已finish报告原字节优先，行情留忽略data和SHA。普通SSH非强推main，fetch/全heads/完整tree与blob/data/report核验后释放本轮broker。

根登记、snapshot、监控及逐行归属检查实际exit0；监控6006研究配置/134观察/10账户，5952旧展示行完整字典不变，exclusive-end历史别名保留。57新ID全部finish、114事件只追加；5104受保护输入和82个旧唯一结果状态/原报告SHA不变。
独立从54个原生保存账本恢复162条成本NAV、原SHA逐条相同，核验6084成交/179820资金结算，不重跑组件模型。162新父成本场景88292106完整NAV点、2268整体/逐折及1458近期指标通过；3张18面板图实际打开核验，旧同H对角线星号标注，旧资格不改。
54项全淘汰：全部近期正折不达6/8、46项完整月正折不达9/12。全期/近期最佳thresh370_S28_L3_BH02_EH04三倍全期+4.653672%/整体DD2.797851%，10/12完整月、近期+1.268091%/4正折；另有配置最多5/8仍不合格。正总收益、低DD或局部正收益占比不代替一致性门槛，不据此改冻结账户。
近期1x始终现金原生数量{'BTC': 16, 'ETH': 13}，新父活动归属{'both_cash': 13, 'BTC_cash_ETH_active': 19, 'ETH_cash_BTC_active': 13, 'both_active': 9}。完整81格三倍净正/Sharpe正占比0.5308641975308642/0.5308641975308642；陡变和边界最优限制见surface_diagnostics，仅只读指标，不新增试验或改门槛。
原冻结SMA续至2026-10-26T00:30:00Z，00:01使用65根闭合日线和64根原始重叠，信号/成本/Float账本函数AST与原Oct25续接器相同。BTC先前持仓按1%冻结退出信号卖出，每成本场景1笔、共3虚拟卖出，ETH维持原现金；未下真实订单，不把它冒充paper10报价成交。全9场景旧34494点精确保持，新增120分钟mark及1日执行参考，现每场景34615点、累计34589分钟/24完整日；三倍组合累计-7.468957811529354%。原10bp手续费/1bp半价差/2bp滑点和20日ADV冲击保留，下一日决策2026-10-27T00:01:00Z，冻结Mar31终点/本金/规则不改，partial rejected不取消计划。
本轮4份1d/1m原HTTP响应及65日上下文全部保留；日线/分钟末收盘一致、输入结构兼容和完整性核验通过。研究报告4769417字节、forward报告5800968字节保持已finish原字节/登记SHA。54父结果、54旧原生、27旧同H父、恒多参考、4原始响应及下一日上下文都是核验/续接必需；8合并＋16源Parquet留忽略data和SHA/路径。本轮无可重建checkpoint/重复研究下载页/NAV缓存或字节码可清。
read_failures保留本轮1个实际失败：准备阶段在旧Oct11模块查找不存在verify函数的只读ValueError，随后使用已存在Oct25日续接验证器；当时无结果计算/账户改动。所有最终必要门禁实际exit0，历史失败未删。普通SSH非强推main、freshfetch/全heads/完整tree和必要blob/data/report核验后释放本轮broker，发布/释放回执留.git。
