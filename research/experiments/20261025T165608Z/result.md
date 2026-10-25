# 20261025T165608Z 固定总入场预算的金额分配实验

新评估72项（18原生ETH金额变体＋54组合）、216成本场景，0通过/72淘汰。全部先成功reserve，随后计算、完整保留负收益并逐项finish。此前读取15592事件/7692ID及182份结论，初始16项均已有真实历史证据，不重复补算。

BTC趋势固定ROC31日/H4%，退出缓冲0.5/1/2%；ETH反转ROC1/2/3日、H2/4/6%，ROC>H空、ROC<-H多，已有多头仅ROC<0保持、空头仅ROC>0保持，过零退出，反向极端先平后开，阈值等号不从现金入场。下一UTC00:01 OPEN执行，仅用此前完整close，数量floor(N/前收盘/lot)×lot，不用未来OPEN或资金费选方向/手数。新ETH N1000/3000完整重算真实手数、费用、冲击和资金费，未缩放旧NAV。

两币独立各10000 USDT银行，组合20000；权重原值1/1相加整本账簿。预设BTC/ETH入场金额1000/3000、3000/1000，总4000=初始组合本金20%；不是25/75资本权重，也不改变两币本金。原生ETH金额占各自初始本金10%/30%。实际成交后数量保持，价格/缺口会使名义敞口偏离预算。无自动归一化、复利放大、转账、跨币保证金、收益率混加或组合再平衡。

6个BTC已有组件只读从完整账本恢复并核验原NAV SHA；旧ETH N2000的9格、旧2000/2000父组合27格，以及2个原生/2个组合恒多基准只读。原生完整敏感性3×3×3=27格，父组合入场金额×退出缓冲×反转L×H为4维81格；中点只加入邻域计算，保留原资格、原报告字节及登记SHA。新72格逐一独立登记finish，旧46个唯一来源不重评级。

真实8份Binance合并Parquet及16份原始输入哈希/版本/重放路径留manifest，行情留忽略data。OOS2025-10-19 UTC00:01至2026-10-24 UTC00:01，连续370日；33日上下文，12完整30日折＋10日尾折，至少9/12正折，尾折保留不计门槛。近期Sep14至Oct24继承日330决策前现金/持仓，共8个5日折，仍要求6/8正折且1/2/3倍成本全正，不重置或增加诊断交易。无拟合标签、purge不适用；历史已反复见过，不称未触碰最终测试集。

每侧5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×滞后20日对数波动×sqrt(订单金额/滞后20日ADV)，参与率≤0.1%，真实lot/不利tick/最小金额/各银行1倍开仓现金约束。实际线性永续资金费按真实时间/mark入账，流出×成本倍数、流入不放大；做空用现金保证金，不虚构现货借贷。缺历史L2/TCA/排队延迟/完整历史阶梯；1%维持保证金及小时不利高低价仅代理。连续分钟交易代理/小时mark/真实结算混合NAV整体DD不称tick级清算证明。

三项验证已执行：13时间折/8近期折及连续全OOS整体DD；3维原生与4维组合参数敏感性（108含中点格、270相邻边）；216个1/2/3倍成本场景。另需3x整体DD≤25%、局部邻域3x正收益≥60%、至少4往返、(参考价毛利＋资金费)/成本≥2.5，零现金/订单/保证金代理违规及每源终点空仓。逐场景/逐折收益、DD、Sharpe、Calmar、日NAV和全路径SHA均保留，不平均折DD或合成Sharpe。

全期成本1/2/3正收益数量{'1': 50, '2': 45, '3': 37}；门槛失败计数{'positive_all_costs': 35, 'nine_of_twelve_positive_complete30d_1x_folds': 58, 'recent40_positive_all_costs': 35, 'recent40_six_of_eight_positive5d_1x_folds': 72, 'local_positive3_gte60pct': 42, 'gross_plus_funding_to_cost1_gte2_5': 31, 'composite_DD3_lte25pct': 1}。

native_N1000：0/9通过；全期3x范围[-8.39339600754161, 1.68670783296907]%，近期3x范围[-1.153348118966857, 0.7317234449879528]%；完整月正折分布{5: 4, 7: 1, 6: 2, 8: 2}，近期五日正折分布{3: 3, 2: 2, 0: 1, 1: 3}。全期最佳{'name': 'reversal370_ETH_N1000_L3_H06', 'full_return3_pct': 1.68670783296907, 'whole_DD3_pct': 3.725990832430137, 'recent_return3_pct': -0.1379773165023246, 'recent_DD3_pct': 0.884083762239174, 'positive_complete30d_folds1': 6, 'positive_recent5d_folds1': 1, 'status': 'rejected'}；近期最佳{'name': 'reversal370_ETH_N1000_L3_H02', 'full_return3_pct': -0.16370973195038996, 'whole_DD3_pct': 4.51151883682257, 'recent_return3_pct': 0.7317234449879528, 'recent_DD3_pct': 1.184974612625589, 'positive_complete30d_folds1': 8, 'positive_recent5d_folds1': 3, 'status': 'rejected'}。

native_N3000：0/9通过；全期3x范围[-25.28315373888549, 5.033423087424005]%，近期3x范围[-3.780627770281597, 2.231555782698025]%；完整月正折分布{5: 4, 7: 1, 6: 2, 8: 2}，近期五日正折分布{3: 3, 2: 2, 0: 1, 1: 3}。全期最佳{'name': 'reversal370_ETH_N3000_L3_H06', 'full_return3_pct': 5.033423087424005, 'whole_DD3_pct': 10.852091016170762, 'recent_return3_pct': -0.402092280047639, 'recent_DD3_pct': 2.5584906321077128, 'positive_complete30d_folds1': 6, 'positive_recent5d_folds1': 1, 'status': 'rejected'}；近期最佳{'name': 'reversal370_ETH_N3000_L3_H02', 'full_return3_pct': -0.5484167636018888, 'whole_DD3_pct': 13.094145624049814, 'recent_return3_pct': 2.231555782698025, 'recent_DD3_pct': 3.568892845452698, 'positive_complete30d_folds1': 8, 'positive_recent5d_folds1': 3, 'status': 'rejected'}。

parent_N1000：0/27通过；全期3x范围[-11.777420526948845, 3.623528506941942]%，近期3x范围[-1.5415801448384725, 1.3014464832806327]%；完整月正折分布{5: 7, 6: 4, 7: 6, 9: 5, 8: 3, 10: 1, 4: 1}，近期五日正折分布{4: 9, 3: 18}。全期最佳{'name': 'budgetmix370_B1000_E3000_E050_L3_H06', 'full_return3_pct': 3.623528506941942, 'whole_DD3_pct': 4.64966017175088, 'recent_return3_pct': -0.004968829084717186, 'recent_DD3_pct': 0.8485305483125871, 'positive_complete30d_folds1': 10, 'positive_recent5d_folds1': 3, 'status': 'rejected'}；近期最佳{'name': 'budgetmix370_B1000_E3000_E200_L3_H02', 'full_return3_pct': 0.5899479606929603, 'whole_DD3_pct': 5.800531430009426, 'recent_return3_pct': 1.3014464832806327, 'recent_DD3_pct': 1.8644889816130772, 'positive_complete30d_folds1': 9, 'positive_recent5d_folds1': 4, 'status': 'rejected'}。

parent_N3000：0/27通过；全期3x范围[-1.5492661506956606, 4.26800635509863]%，近期3x范围[0.08113287449458273, 0.9832004933016281]%；完整月正折分布{7: 3, 8: 14, 9: 8, 6: 2}，近期五日正折分布{4: 24, 5: 3}。全期最佳{'name': 'budgetmix370_B3000_E1000_E050_L3_H06', 'full_return3_pct': 4.26800635509863, 'whole_DD3_pct': 3.0651373773121993, 'recent_return3_pct': 0.5455505643978897, 'recent_DD3_pct': 1.4169307313565138, 'positive_complete30d_folds1': 9, 'positive_recent5d_folds1': 4, 'status': 'rejected'}；近期最佳{'name': 'budgetmix370_B3000_E1000_E200_L3_H02', 'full_return3_pct': 2.56557698709996, 'whole_DD3_pct': 3.559287041716208, 'recent_return3_pct': 0.9832004933016281, 'recent_DD3_pct': 1.7085386615874665, 'positive_complete30d_folds1': 9, 'positive_recent5d_folds1': 5, 'status': 'rejected'}。

原冻结SMA65/对称1%、BTC1500/ETH500原始状态续接至2026-10-25T16:30:00Z，新增120闭合分钟mark，0日决策/参考价/成交；不重置本金/持仓/费用，完整旧NAV前缀校验，下一日决策2026-10-26 UTC00:01、终点2027-03-31不变。23日延迟shadow不足180日/六折，不替代paper10真实报价账户，不因partial rejected停止冻结计划。

方向选择受此前2000/2000混合结果影响，属于已见历史探索；预设金额分配后完整评估，不降低近期6/8或改变规则。相关多重试验不是独立证据，不称DSR/PBO校正或稳定实盘盈利，不据回测更换冻结账户。AQR[交易成本作者原页](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)本轮实际读取，2012-12-05传统股票研究仅作反转成本脆弱性动机，不移植论文收益或容量。

本轮冻结前旧恒多父报告缺asset字段触发KeyError，尚无plan/spec/reserve/回测；以只读引用默认COMBO兼容修复，失败原日志及恢复记录保留。此处没有改旧收益或跳过门禁。其他实际执行失败如有均记read_failures，不能以cat日志exit0替代检查命令真实退出码。

复现工作目录/home/desktop/Documents/Codex/EquiTide；audit.py、check_sources.py、forward.py --reproduce、audit_forward.py、check_feed.py和根checks读取完整已finish证据。不要重新reserve/evaluate/summarize已完成精确配置。所有结果原字节优先于体积优化，仅清理可重建本轮缓存/checkpoint。普通SSH非强推main后fetch/ls-remote完整tree与blob核验，最后释放本轮broker。

根登记、snapshot、监控和逐行归属检查实际exit0，监控5736研究配置/130观察/10账户；5664个旧展示行完整字典相同，历史exclusive-end别名保留。75新ID全部finish、150事件仅追加；4968受保护输入及46个旧唯一来源状态/原报告SHA保持。
独立核验216成本场景共117722808完整NAV点、3024整体/逐折指标、1944近期指标；新ETH6300成交/59940资金结算，BTC旧账本612成交/19980资金结算恢复；4张24面板图均实际打开核验。
72项全部淘汰，近期正折门槛72项全失败。BTC3000/ETH1000的27格近期三倍成本均正，但仅4–5/8正折；全期最佳父组合三倍+4.268006%/整体DD3.065137%，9/12完整月正折，近期仍仅4/8。BTC1000/ETH3000近期最高三倍+1.301446%，但仅4/8，全期仅+0.589948%。不降低6/8门槛，不将正总收益称稳定实盘盈利。
原SMA累计三倍收益-6.822922246885166%，每场景34134点、旧34014点严格不变，新增120分钟mark/0成交。已finish研究报告6410163字节及forward报告5730590字节保持原字节和登记SHA；18完整新原生账本/54父结果、旧来源路径和2份原HTTP响应为审计/重放必需。没有本轮checkpoint、重复研究下载页、磁盘NAV或编译缓存可清理；8合并＋16源Parquet留忽略data并保留哈希/复现路径。
本轮2个实际失败均原样保留：冻结前旧parent缺asset，以及只读恒多40日字段extension40别名。均仅修读取兼容，无重算已完成配置，无改旧收益或已finish报告；恢复和所有最终门禁实际exit0。普通SSH非强推main后freshfetch/独立全heads/完整tree与必需blob/data/report核验，最后释放自己的broker；发布及释放回执留.git。
