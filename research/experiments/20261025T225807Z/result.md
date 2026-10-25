# 20261025T225807Z BTC与ETH慢趋势窗口不同的反转组合

实际评估54个新组合、162成本场景，0通过/54淘汰。全部先独立成功reserve，再计算、逐项finish；负收益/零收益/失败门槛完整保留。全文读取16138事件/7965ID和185份旧结论；初始16项均已有实际证据。54个原生组件/162条原成本NAV只读恢复，组件信号/撮合/资金费模型重跑0。

预设BTC慢ROC窗口S_B和ETH慢窗口S_E独立取7/14/28日，短ROC回看L1/2/3日及阈值H2/4/6%两币相同。仅S_B≠S_E的54对为新配置；已有同S的27对只读原指标和原三维资格，不重跑或重评级，组成81格完整四维网格。不同资产时间尺度可能改变共同空仓/成交/亏损折时点，不预设负相关、收益改善或未来择时切换。

原生完整规则由各source指纹/spec/原报告SHA固定：此前完整close计算短ROC，>H空、<-H多，带内已有多头仅ROC<0保持、空头仅>0保持，过零退出；慢ROC>0仅允许多、<0仅允许空、=0平仓。不兼容则平实际仓位，无隐藏状态，现金重入需严格短ROC极端。下一UTC00:01 OPEN成交，手数按此前close/lot向下取整，同向保留实际数量。54个两币原生账本均已有真实结果；本轮只重建其保存的cash/q/entry/成交/结算路径，校验每条完整NAV SHA，不用新参数重新simulate。

权重原值1/1代表两整本各10000 USDT独立银行，总本金20000；每币原生N2000入场预算，总4000占初始本金20%。不自动归一化、NAV缩放、复利放大、转账、交叉保证金、现金生息或组合再平衡；新父无额外订单。同档成本的绝对NAV相加，纳秒/事件共同轴仅取最后已完成源样本，不插值、不平均Sharpe或单币收益率。

真实Binance8合并Parquet及16原始年度/近期输入保留忽略data、版本/字节/SHA及复现路径。OOS2025-10-19 UTC00:01到2026-10-24 UTC00:01连续370日，33日上下文；12完整30日折＋10日尾折，至少9/12完整月净正、尾折不计门槛。近期Sep14-Oct24继承日330决策前原状态，8个连续5日折，仍要求6/8正折和各成本净正，不重置或加诊断交易。无拟合标签，purge不适用；历史已反复见过，不称未触碰最终测试集。

原生每侧5bp手续费＋1bp半价差＋2bp滑点；成交量冲击0.5×滞后20日对数波动×sqrt(订单金额/滞后20日ADV)，参与率≤0.1%，真实lot/不利tick/最小金额/独立1倍开仓现金约束。实际线性永续结算资金费流出×成本倍数、流入不放大，空头用保证金，不虚构现货借贷。缺L2/TCA/排队/完整历史阶梯，1%维持保证金及小时不利高低价仅代理，混合分钟交易代理/小时mark/结算完整DD不称tick级清算保证。复用NAV不表示免费用，原生成交/资金费逐档全计入。

三项验证已实际执行：13时间折、8近期折及连续OOS整体DD；81格四维完整敏感性、216相邻边；162个新1/2/3倍成本场景。旧对角线27格指标加入新邻域、旧原三维资格保持。新组合另需3x整体DD≤25%、局部四维3x净正≥60%、至少4往返、(参考价毛利＋资金费)/成本≥2.5、零各源现金/拒单/保证金代理违规及每源终点空仓。

全期1/2/3倍成本正收益数量{'1': 44, '2': 38, '3': 33}，近期对应{'1': 23, '2': 23, '3': 17}；失败门槛计数{'positive_all_costs': 21, 'nine_of_twelve_positive_complete30d_1x_folds': 49, 'recent40_six_of_eight_positive5d_1x_folds': 54, 'local_positive3_gte60pct': 24, 'gross_plus_funding_to_cost1_gte2_5': 19, 'recent40_positive_all_costs': 37, 'four_round_trips1': 1}。全期最佳{'name': 'stagger370_BS14_ES28_L3_H02', 'full_return3_pct': 4.739005903253557, 'whole_DD3_pct': 2.404519599238819, 'recent_return3_pct': 0.8339432913633704, 'recent_DD3_pct': 0.9287362357123574, 'positive_complete30d_folds1': 9, 'positive_recent5d_folds1': 4, 'status': 'rejected', 'failed_criteria': ['recent40_six_of_eight_positive5d_1x_folds']}；近期最佳{'name': 'stagger370_BS28_ES7_L3_H02', 'full_return3_pct': 3.6773871132398828, 'whole_DD3_pct': 2.7683307947036107, 'recent_return3_pct': 1.6909522405034405, 'recent_DD3_pct': 0.6685673838938588, 'positive_complete30d_folds1': 8, 'positive_recent5d_folds1': 4, 'status': 'rejected', 'failed_criteria': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_1x_folds']}。

B7_E14：{'configs': 9, 'passed': 0, 'full_positive3': 5, 'recent_positive3': 2, 'full3_range_pct': [-3.6584839362636568, 2.4872124451868594], 'recent3_range_pct': [-0.4562886214079742, 0.7456682168748952], 'positive_complete30d_folds1_counts': {5: 2, 3: 2, 1: 1, 6: 3, 7: 1}, 'positive_recent5d_folds1_counts': {1: 2, 0: 6, 3: 1}, 'failed_criteria_counts': {'positive_all_costs': 4, 'nine_of_twelve_positive_complete30d_1x_folds': 9, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 5, 'gross_plus_funding_to_cost1_gte2_5': 4, 'recent40_positive_all_costs': 7}}

B7_E28：{'configs': 9, 'passed': 0, 'full_positive3': 6, 'recent_positive3': 2, 'full3_range_pct': [-4.970693694069849, 3.610381493787518], 'recent3_range_pct': [-0.44168596317391007, 0.8444143562705175], 'positive_complete30d_folds1_counts': {5: 1, 4: 1, 2: 1, 7: 2, 6: 1, 10: 1, 9: 1, 8: 1}, 'positive_recent5d_folds1_counts': {3: 3, 2: 1, 0: 1, 1: 3, 4: 1}, 'failed_criteria_counts': {'positive_all_costs': 3, 'nine_of_twelve_positive_complete30d_1x_folds': 7, 'recent40_positive_all_costs': 7, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 3, 'gross_plus_funding_to_cost1_gte2_5': 3}}

B14_E7：{'configs': 9, 'passed': 0, 'full_positive3': 5, 'recent_positive3': 2, 'full3_range_pct': [-2.0125998540825862, 3.7473455655468113], 'recent3_range_pct': [-0.09410905700129035, 0.9795277488480414], 'positive_complete30d_folds1_counts': {5: 3, 4: 2, 1: 1, 8: 1, 3: 1, 10: 1}, 'positive_recent5d_folds1_counts': {1: 1, 0: 7, 2: 1}, 'failed_criteria_counts': {'positive_all_costs': 4, 'nine_of_twelve_positive_complete30d_1x_folds': 8, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 5, 'gross_plus_funding_to_cost1_gte2_5': 3, 'recent40_positive_all_costs': 7, 'four_round_trips1': 1}}

B14_E28：{'configs': 9, 'passed': 0, 'full_positive3': 6, 'recent_positive3': 2, 'full3_range_pct': [-4.260880784391807, 4.739005903253557], 'recent3_range_pct': [-0.43842564624481106, 0.8339432913633704], 'positive_complete30d_folds1_counts': {6: 2, 4: 1, 2: 1, 8: 2, 7: 1, 9: 2}, 'positive_recent5d_folds1_counts': {3: 3, 2: 1, 0: 1, 1: 3, 4: 1}, 'failed_criteria_counts': {'positive_all_costs': 3, 'nine_of_twelve_positive_complete30d_1x_folds': 7, 'recent40_positive_all_costs': 7, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 3, 'gross_plus_funding_to_cost1_gte2_5': 2}}

B28_E7：{'configs': 9, 'passed': 0, 'full_positive3': 6, 'recent_positive3': 5, 'full3_range_pct': [-3.2612593101476683, 3.6773871132398828], 'recent3_range_pct': [0.0, 1.6909522405034405], 'positive_complete30d_folds1_counts': {4: 2, 6: 4, 2: 1, 3: 1, 8: 1}, 'positive_recent5d_folds1_counts': {3: 2, 0: 4, 1: 2, 4: 1}, 'failed_criteria_counts': {'positive_all_costs': 3, 'nine_of_twelve_positive_complete30d_1x_folds': 9, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 5, 'gross_plus_funding_to_cost1_gte2_5': 3, 'recent40_positive_all_costs': 4}}

B28_E14：{'configs': 9, 'passed': 0, 'full_positive3': 5, 'recent_positive3': 4, 'full3_range_pct': [-4.197330482650685, 3.7053165017256973], 'recent3_range_pct': [-0.3047042041197323, 1.4439768756157267], 'positive_complete30d_folds1_counts': {4: 2, 2: 1, 6: 1, 7: 4, 3: 1}, 'positive_recent5d_folds1_counts': {3: 1, 0: 4, 2: 1, 1: 2, 4: 1}, 'failed_criteria_counts': {'positive_all_costs': 4, 'nine_of_twelve_positive_complete30d_1x_folds': 9, 'recent40_six_of_eight_positive5d_1x_folds': 9, 'local_positive3_gte60pct': 3, 'gross_plus_funding_to_cost1_gte2_5': 4, 'recent40_positive_all_costs': 5}}

每个新配置同时对照两个旧同S父组合：以S_B作为两币同S、以S_E作为两币同S，以及同本金/同预算恒多参考。共486逐成本对照；old82唯一结果（54原生＋27对角线＋1恒多）状态/资格/原报告字节及登记SHA不改。不同慢窗口是新组件配对，不因family相同排除；仅改名或组件次序不算新。

原冻结SMA65/对称1%、BTC1500/ETH500连续续到2026-10-25T22:30:00Z，120新闭合分钟mark、0新日决策/参考/成交；现金/数量/desired/费用及完整旧NAV前缀保持，下一日决策2026-10-26 UTC00:01、终点2027-03-31不变。23日初期延迟shadow不足180日/六折，不替代paper10真实报价，partial rejected不取消冻结计划。

本轮重新读取AQR官方[Time Series Momentum](https://www.aqr.com/Insights/Research/Journal-Article/Time-Series-Momentum)（2012-05-01）及[交易成本研究](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)（2012-12-05），访问2026-10-25。传统12个月期货趋势/股票反转成本仅作背景，跨币时间尺度不同的7/14/28日配对为本轮推断，非论文复现或利润/容量移植。选择受旧结果影响，54相关试验不是54份独立证据，不称DSR/PBO、未触碰留出或稳定实盘盈利，不据回测更换冻结账户。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py、check_sources.py、check_alignment.py、forward.py --reproduce、audit_forward.py、check_feed.py及根登记/监控检查读取真实保存结果；不重新reserve/evaluate/summarize已finish配置。失败如有保留原日志，以实际命令exit为准。只清理可重建缓存/checkpoint，已finish报告原字节优先；行情留忽略data和哈希。SSH普通非强推main，fetch/独立全heads/完整tree与必需blob/data/report核验后释放本轮broker。

根登记、snapshot、监控及逐行归属检查实际exit0；监控5952研究配置/133观察/10账户，5898旧展示行完整字典不变，exclusive-end历史别名保留。57新ID全部finish、114事件只追加；5070受保护输入和82个旧唯一结果状态/原报告SHA不变。
独立从54个保存原生账本恢复162条成本NAV、每条原SHA相同，核验6084源成交/179820源资金结算，不重跑信号、撮合或资金费模型。162新父成本场景88292106完整NAV点、2268整体/逐折及1458近期指标均核验。3张18面板图实际打开检查；旧同S行标明只读，新窗口不同组合完整保留。
54项全淘汰：全部近期正折不达6/8、49项月折不达9/12。全期最佳stagger370_BS14_ES28_L3_H02三倍+4.739006%/整体DD2.404520%，9/12完整月、近期4/8；近期最佳BS28/ES7/L3/H2三倍近期+1.690952%，全期+3.677387%/DD2.768331%，8/12完整月、近期4/8。正总收益及四维局部正收益占比不替代近期门槛；旧27项保持原三维资格，不重评级。
真实状态/成交分段核验近期1x始终现金原生数量{'BTC': 16, 'ETH': 13}，新父活动归属{'both_cash': 22, 'BTC_cash_ETH_active': 10, 'ETH_cash_BTC_active': 4, 'both_active': 18}。全81格三倍净正及Sharpe正占比0.6049382716049383/0.6049382716049383；陡变/边界最优限制见surface_diagnostics，仅只读指标，不加试验或改变门槛。现金腿不贡献持续alpha。
原SMA续至2026-10-25T22:30:00Z，三倍累计-6.883935095818872%，每场景34494点、旧34374点严格不变，追加120闭合分钟mark/0成交。研究报告4729272字节、forward报告5790528字节按已finish原字节保留；54父结果、54完整旧原生账本、27旧同S父、恒多控制及2份原HTTP响应为审计/重放必需。8合并＋16源Parquet留忽略data和哈希/复现路径。本轮无可重建checkpoint、重复研究下载页、磁盘NAV或字节码缓存。
read_failures记录本轮实际失败0项，所有最终必要门禁实际exit0；此前轮次失败事实保持。未重算已完成精确配置、改已finish报告、调整冻结账户或下真实订单。普通SSH非强推main，freshfetch/独立全heads/完整tree与必要blob/data/report核验后释放本轮broker；发布/释放回执留.git，不回写结果。
