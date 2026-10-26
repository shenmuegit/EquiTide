# 20261026T050406Z BTC慢趋势约束反转＋ETH顺趋势

真实评估81个新组合、243个1/2/3倍成本场景，0通过/81淘汰。全部先成功reserve，计算及独立核验后逐项finish；所有负收益、零收益和淘汰保留。全文读取16540事件/8166ID和188份旧结论；初始16项均有真实历史证据，无缺实际结果项。30个原生组件/90原成本NAV只读恢复并核对原SHA，组件信号/撮合/资金费模型重跑0。

预设BTC慢ROC S7/14/28日、短ROC L1/2/3日、入场H2/4/6%；ETH顺趋势ROC28日、入场2%，退出E0.5/1/2%。S×L×H×E完整81格四维网格，216相邻边，资产角色固定，不根据未来表现切换。本轮把ETH从反转换成顺趋势，检验其活动与BTC回撤折的组合效果，不预设负相关或改善。27个旧无BTC慢门槛组合只作同L/H/ETH_E匹配对照，原资格/登记/报告字节不变，不加入新网格重新评级。

BTC完整规则：以前一完整close计算短ROC，>H空、<-H多；带内实际已有多头仅ROC<0保持、空头仅ROC>0保持，过零退出；反向极端先平后开。慢ROC>0仅允许多、<0仅空、=0全平；不兼容立即平实际仓位，不保留隐藏desired，现金重入须新严格极端。ETH以前一完整close算28日ROC，>2%多、<-2%空；带内实际多头仅ROC>-E保持，空头仅ROC<E保持；跨反向严格入场带先平后开；精确入场等号不新开、精确退出等号平仓。两币次日UTC00:01 OPEN执行，数量按前一close/lot向下取整，同向保持实际q。每个源spec/报告/完整账本SHA固定，不以过滤旧NAV代替门槛造成的真实持仓变化。

原值权重1/1代表两个各10000USDT完整独立银行相加，父本金20000，每币固定2000入场预算、总4000占初始本金20%。不自动归一化、按收益缩放手数、复利、转账、交叉保证金、现金生息或父再平衡，没有额外父成交。同档绝对NAV按共同纳秒/事件轴相加，只携带已完成源样本、不插值或平均单币收益率/Sharpe。

真实Binance8合并Parquet及16年度/近期原输入留忽略data，保存路径/版本/字节/SHA。连续OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01共370日、33日上下文，12完整30日折＋10日尾折。完整月正折至少9/12，尾折保留但不计入门槛。近期Sep14-Oct24从日330决策前现金/仓位续接，8个连续5日折，要求至少6/8净正且所有成本总净正。无模型或未来标签拟合，purge不适用；3日初始embargo/因果执行保留，状态跨全部折不重开。历史均反复使用，不能称未触碰最终测试集。

原生永续每侧5bp手续费＋1bp半价差＋2bp滑点，冲击0.5×滞后20日对数波动×sqrt(订单参考金额/滞后20日ADV)，参与率≤0.1%；原真实lot/不利tick/最小金额和独立现金约束保持。实际资金费按真实结算时点及mark对当时持仓入账，流出×成本倍数、流入不放大。永续空头以现金保证金，不虚构现货借贷。缺历史L2/排队/TCA/完整阶梯；1%维持保证金及小时不利mark高低价只作代理，分钟交易代理＋小时mark＋结算的整体DD不等于tick级清算保证。

三项验证实际执行：13时间折/8近期折及完整连续OOS回撤；81格四维敏感性、216相邻边和Sharpe陡变；243新成本场景含手续费/价差/滑点/成交量冲击/资金费。其他资格门槛为3x整体DD≤25%、局部邻域3x净正≥60%、至少4往返、(参考价毛利＋资金费)/执行成本≥2.5、源现金/拒单/保证金代理违规0、各源终点空仓。原生旧报告ETH近期字段extension40按相同Sep14-Oct24区间只读识别，不改原报告。

全期1/2/3倍成本净正数量{'1': 81, '2': 81, '3': 81}，近期对应{'1': 3, '2': 3, '3': 0}；失败门槛{'recent40_positive_all_costs': 81, 'recent40_six_of_eight_positive5d_1x_folds': 81, 'nine_of_twelve_positive_complete30d_1x_folds': 18}。全期最佳{'name': 'mixedgate370_BG_ET_S14_L3_H02_E200', 'full_return3_pct': 9.799507714876343, 'whole_DD3_pct': 3.244165862495074, 'recent_return3_pct': -0.6718479779449948, 'recent_DD3_pct': 2.761246242557247, 'positive_complete30d_folds1': 9, 'positive_recent5d_folds1': 3, 'status': 'rejected', 'failed_criteria': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_1x_folds']}；近期最佳{'name': 'mixedgate370_BG_ET_S28_L3_H02_E200', 'full_return3_pct': 9.729549262569414, 'whole_DD3_pct': 3.533520563399617, 'recent_return3_pct': -0.022840369847620945, 'recent_DD3_pct': 3.0623603457975213, 'positive_complete30d_folds1': 12, 'positive_recent5d_folds1': 3, 'status': 'rejected', 'failed_criteria': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_1x_folds']}。

S7：{'configs': 27, 'passed': 0, 'full_positive3': 27, 'recent_positive3': 0, 'full3_range_pct': [3.9461150725207617, 8.686259028678545], 'recent3_range_pct': [-1.0208832678814006, -0.6797687976546452], 'positive_complete30d_folds1_counts': {9: 9, 8: 4, 10: 10, 7: 3, 6: 1}, 'positive_recent5d_folds1_counts': {3: 27}, 'failed_criteria_counts': {'recent40_positive_all_costs': 27, 'recent40_six_of_eight_positive5d_1x_folds': 27, 'nine_of_twelve_positive_complete30d_1x_folds': 8}}

S14：{'configs': 27, 'passed': 0, 'full_positive3': 27, 'recent_positive3': 0, 'full3_range_pct': [5.306705207710083, 9.799507714876343], 'recent3_range_pct': [-1.00605871355669, -0.6718479779449948], 'positive_complete30d_folds1_counts': {8: 5, 7: 1, 10: 9, 9: 12}, 'positive_recent5d_folds1_counts': {3: 27}, 'failed_criteria_counts': {'nine_of_twelve_positive_complete30d_1x_folds': 6, 'recent40_positive_all_costs': 27, 'recent40_six_of_eight_positive5d_1x_folds': 27}}

S28：{'configs': 27, 'passed': 0, 'full_positive3': 27, 'recent_positive3': 0, 'full3_range_pct': [3.8280601060763475, 9.729549262569414], 'recent3_range_pct': [-1.0166259878073403, -0.022840369847620945], 'positive_complete30d_folds1_counts': {8: 3, 7: 1, 9: 9, 10: 11, 12: 3}, 'positive_recent5d_folds1_counts': {3: 27}, 'failed_criteria_counts': {'nine_of_twelve_positive_complete30d_1x_folds': 4, 'recent40_positive_all_costs': 27, 'recent40_six_of_eight_positive5d_1x_folds': 27}}

每个新组合对照同L/H/ETH_E无BTC慢门槛旧组合及相同本金/预算恒多，486个逐成本对照完整保留；30原生＋27旧组合＋1恒多共58个旧唯一结果原状态/资格/报告字节/登记SHA不变。不同组件配对是真新配置，不因family相同排除；仅改名、组件顺序或等价数字格式不是新配置。

原冻结SMA65/对称1%、BTC1500/ETH500从上轮UTC02:30续至2026-10-26T04:30:00Z，仅追加120闭合分钟mark、无新日决策/参考/成交。Oct26UTC00:01的BTC卖出已经完成，不重复执行。逐币逐成本cash/units/desired/历史费用/成交与旧34735点严格继承，新总34855点；下一日决策2026-10-27 UTC00:01、终点2027-03-31不变。两币现金续接不从2000本金重开；现金期间NAV不变不代表新alpha。

原SMA沿用历史Float手数、10bp手续费模型，不套新永续5bp/lot/tick。24日初期延迟shadow不足180日/六折，不冒充paper10真实报价模拟；partial rejected不取消冻结计划。最近65日日线上下文仍指010010/forward_inputs.json.gz及原SHA，下一日从该字典续接；当前mark-only输入仅分钟数组。

本轮读取AQR官方[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）与[交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-26。传统期货12个月趋势和股票反转成本仅作背景；BTC短期反转加慢趋势门槛与ETH28日顺趋势的组合是本轮推断，非论文复现或利润/容量移植。81相关试验基于已见历史，不称未触碰留出、DSR/PBO校正或稳定实盘盈利，不据此改变冻结账户。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py/check_sources.py/check_alignment.py只读已finish证据；forward.py --reproduce及audit_forward.py不HTTP取数或写登记。不要重新reserve/evaluate/summarize已finish配置。真实失败留read_failures，必要门禁以实际exit为准；行情忽略data，只清本轮可重建缓存/checkpoint。普通SSH非强推main，经freshfetch/全heads/完整tree与必要blob/data/reportSHA核验后释放本轮broker；发布/释放回执留.git。

根登记、snapshot、监控及逐行归属检查实际exit0；监控6141研究配置/136观察/10账户，6060旧展示行完整字典不变，exclusive-end历史别名保留。84新ID全部finish、168事件只追加；5172受保护输入和58个旧唯一结果状态/原报告SHA不变。
独立从30个保存原生账本恢复90条成本NAV、每条原SHA相同，核验2640源成交/99900源资金结算，不重跑信号、撮合或资金费模型。243新父成本场景132438159完整NAV点、3402整体/逐折及2187近期指标均核验。3张18面板图实际打开检查；新S/L/H/ETH_E四维81格完整保留，27无门槛旧组合只读对照、不重新评级。
81项完整结果：0通过/81淘汰，失败门槛计数{'recent40_positive_all_costs': 81, 'recent40_six_of_eight_positive5d_1x_folds': 81, 'nine_of_twelve_positive_complete30d_1x_folds': 18}；全期最佳{'name': 'mixedgate370_BG_ET_S14_L3_H02_E200', 'full_return3_pct': 9.799507714876343, 'whole_DD3_pct': 3.244165862495074, 'recent_return3_pct': -0.6718479779449948, 'recent_DD3_pct': 2.761246242557247, 'positive_complete30d_folds1': 9, 'positive_recent5d_folds1': 3, 'status': 'rejected', 'failed_criteria': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_1x_folds']}，近期最佳{'name': 'mixedgate370_BG_ET_S28_L3_H02_E200', 'full_return3_pct': 9.729549262569414, 'whole_DD3_pct': 3.533520563399617, 'recent_return3_pct': -0.022840369847620945, 'recent_DD3_pct': 3.0623603457975213, 'positive_complete30d_folds1': 12, 'positive_recent5d_folds1': 3, 'status': 'rejected', 'failed_criteria': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_1x_folds']}。总收益、局部平台与最佳点不能代替预登记近期/月度折数及费用门槛；旧27项保持原资格。
真实状态/成交分段核验近期1x始终现金原生数量{'BTC': 16, 'ETH': 0}，新父活动归属{'both_cash': 0, 'BTC_cash_ETH_active': 48, 'ETH_cash_BTC_active': 0, 'both_active': 33}。全81格三倍净正及Sharpe正占比1.0/1.0；陡变/边界最优限制见surface_diagnostics，仅只读指标，不加试验或改变门槛。现金腿不贡献持续alpha。
原SMA续至2026-10-26T04:30:00Z，三倍累计-7.468957811529354%，每场景34855点、旧34735点严格不变，追加120闭合分钟mark/0成交。研究报告7186590字节、forward报告5852327字节按已finish原字节保留；81父结果、30完整旧原生账本、27旧无门槛父、恒多控制及2份原HTTP响应为审计/重放必需。8合并＋16源Parquet留忽略data和哈希/复现路径。本轮无可重建checkpoint、重复研究下载页、磁盘NAV或字节码缓存。
read_failures记录本轮实际失败0项，所有最终必要门禁实际exit0；此前轮次失败事实保持。未重算已完成精确配置、改已finish报告、调整冻结账户或下真实订单。普通SSH非强推main，freshfetch/独立全heads/完整tree与必要blob/data/report核验后释放本轮broker；发布/释放回执留.git，不回写结果。
