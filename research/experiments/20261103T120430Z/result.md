固定BTC N750后的退出缓冲组合研究

前两轮增加BTC入场额不能修复慢窗敏感性。本轮固定BTC3750/N750和ETH15000/N4500、慢窗S28，只预设快L3/4/5×退出缓冲E0.375/0.5/0.625%双轴，检验迟延退出能否减轻近期反复交易及成本，而非继续加BTC敞口。E0.5%三父只读，六个新组合逐项先reserve。16旧实际结果/36旧原生成本路径复用，无新原生模型/源交易/父订单。既有S27/29脆弱证据继续披露，本批L/E通过也不等于跨S稳健或独立未来盈利。

完整读取26444事件/13100ID、287份既往结论；初始16均有原档实际证据。此前完整研究定义9601，登记有结果9388、未标结果213，全部登记不能算全部完成回测。大量重复历史搜索有多重选择偏差。

预设ETH快L3/4/5 × 退出缓冲E0.375/0.5/0.625%，慢S28固定，固定BTC真实银行3750/N750，ETH真实15000/N4500、HL1.5%/HS2.5%、V10/cap4.5%。raw[1,1]代表完整银行所有权，初始本金18750、资金份额20/80%；不归一化、不再乘资金份额、不线性缩放数量或净值，不平均Sharpe/收益/DD。E0.5%三个父、BTC、九个ETH源与匹配持有父及其源共16旧实际结果只读。六个E0.375/0.625%父逐项reserve后才对齐完整分钟/事件净值计算；0新原生策略、0新源成交、0新持有基准、0父订单。

Walk-forward：实际2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日，12×30日完整折+10日尾折。现金/数量/费用不按折重开，完整OOS曲线算整体DD。近期40日继承day330状态、8×5日折。固定规则无拟合/标签，purge0、30日预热+3日间隔，过去完整收盘生成信号、下一00:01原生OPEN执行、终点平仓成本已在原生源内。历史反复开发，不能叫未触碰最终测试、独立未来或实盘稳定盈利。

成本全部来自真实已执行原生源：5bp费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)，LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark维持保证金代理；真实settlement ns/rate/mark/heldq资金费，1/2/3倍放大支出、收入不放大。永续空头不借现货，不虚构借币费。父没有调仓或额外成本；匹配持有为相同银行与初始入场N750/4500，现金0%另列。缺盘口/TCA/历史全层级/逐tick强平和真实容量验证，估计及代理局限保留。

原资格门槛保持：各成本全年正；1倍至少9/12正完整月；各成本近期40日正且>=6/8正5日折；3倍整体DD<=25%；含中心索引半径1的L/E邻域3倍正比例与严格近期合格比例均>=60%；至少4底层平仓、毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规，终点flat。旧原生/父的canonical status/criteria/sensitivity及报告字节不改，新L/E诊断另列。

|新组合|L|E(比例)|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|exit750_parent_L3_S28_E375milliPct|3|0.00375|13.350642|11.618669|9.885917|3.502611|11|6/6/6|passed|
|exit750_parent_L3_S28_E625milliPct|3|0.00625|13.018440|11.261660|9.504180|4.405505|11|6/6/6|passed|
|exit750_parent_L4_S28_E375milliPct|4|0.00375|12.733268|11.099142|9.464481|3.950896|11|6/6/6|passed|
|exit750_parent_L4_S28_E625milliPct|4|0.00625|11.602304|10.002672|8.402238|4.805394|10|6/6/6|passed|
|exit750_parent_L5_S28_E375milliPct|5|0.00375|15.336937|13.575742|11.815624|3.974112|11|4/4/4|rejected|
|exit750_parent_L5_S28_E625milliPct|5|0.00625|16.066262|14.290191|12.514877|3.965952|11|4/4/4|rejected|

六个新组合历史通过4、淘汰2，逐项失败{'exit750_parent_L3_S28_E375milliPct': [], 'exit750_parent_L3_S28_E625milliPct': [], 'exit750_parent_L4_S28_E375milliPct': [], 'exit750_parent_L4_S28_E625milliPct': [], 'exit750_parent_L5_S28_E375milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'exit750_parent_L5_S28_E625milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。相对E0.5%同L/N750原中心，三成本完整NAV同路径0/6；与同L/E原N375逐成本差异及近期折数保留。本批L/E门槛通过也不能解决先前S27/29敏感性证据，不能称全参数稳健或独立未来盈利。

11CSV包含18新场景、234逐月/尾折、144近期折、6678日NAV、原生只读九格与新父九格敏感性、72相邻边及来源/分配/匹配持有现金。图中ETH原生全部O=只读，父E0.375/0.625% N=新、E0.5% O=旧。全部Sharpe/Calmar/完整DD及负收益期间保留，描述性悬崖不是统计显著性，也不是事后加门槛。

原SMA65与single仅续Nov3_08:30→10:30；L4/H2续10:10→12:10，仅12:11参考闭合后采集，逐条核对实际新增资金费，不预填固定时间/费率/mark，不重复既有08/00。所有cash/q/desired/已付成本/risk/context/完整NAV前缀保留，不采纳本批E、不改本金或冻结终止计划。部分延迟shadow与十策略真实报价模拟分开，不作180日/六折资格。SMA真实65日源仍为20261103T020232Z/forward_inputs.json.gz。

一手资料2026-11-03实际访问：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。官方字段不证明盈利或实时执行；8源行情/mark/资金费/约束文件边界/单位/字节/SHA见plan和data_manifest。

金融计算前合成检查覆盖原始完整银行资本恒等式、收益/DD不能平均、不同事件轴必须拒绝与18个L/E索引邻域。当前L/E双轴网格与账户运输适配在reserve前固定，一次绑定32个来源文件；没有结果后改规则或门槛。

所有实际定义先reserve后计算并finish；正负结果和失败均保留，检查后只清理可重建中间件，完整账本不删。同main锁内生成只读监控、提交非强制push；真实发布/终态/解锁凭据见.git/automation_proofs/20261103T120430Z.json。

封存：6新组合/18成本场景分别finish，本批历史门槛通过4、淘汰2。0新原生模型/源成交/父订单。16旧实际结果只读，36旧原生成本路径核验资金费39960条、成交1992笔；均是旧账本。新父NAV独立核验9810234点，计数{'funding': 39960, 'fills': 1992, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 150090}。15新ID/30追加事件，29059旧保护文件字节不变。

本批新定义相对同L/E0.5%控制全成本NAV相同0/6；通过者同路径0/4。同路径是参数定义变动，没有新增收益路径；全部hash/差异及同L/E原N375比较见equivalent_realized_NAV_paths.json。旧E0.5%中心在本批L/E支持{3: 1.0, 4: 0.6666666666666666, 5: 0.5}，既有慢S诊断仍为[{'fingerprint': '097ca4abc3ec89606bae435a392bc671fdff027d38b077d5d51a6def51fe03f6', 'L': 3, 'S': 28, 'N': 750, 'canonical_status': 'passed', 'current_neighbors': 6, 'current_local_strict_recent_fraction': 0.3333333333333333}, {'fingerprint': '6bfd73012abf91fc461b9570030d75830985f75a128cf28bc7fad00b9c10e6f9', 'L': 4, 'S': 28, 'N': 750, 'canonical_status': 'passed', 'current_neighbors': 9, 'current_local_strict_recent_fraction': 0.2222222222222222}, {'fingerprint': '329ded5adec8dc3603ef35c1be8736f76cf4bfb09d73cbd5278d0088d161c6f0', 'L': 5, 'S': 28, 'N': 750, 'canonical_status': 'rejected', 'current_neighbors': 6, 'current_local_strict_recent_fraction': 0.16666666666666666}]。本批L/E通过不意味着S27/29脆弱性已解决，不能称独立最终测试/未来或稳定实盘利润；不修改冻结账户。

原SMA续2026-11-03T08:30:00Z至2026-11-03T10:30:00Z，NAV46623+120=46743，46709分钟/32完整日。single续2026-11-03T08:30:00Z至2026-11-03T10:30:00Z，NAV10956、累计270ID。L4/H2续2026-11-03T10:10:00Z至2026-11-03T12:10:00Z，仅12:11参考闭合后采集，NAV3693、累计93ID。实际新增资金费single=[]、L4=[]，成交single=0、L4=0。逐项从实际响应核算，08/00不重复。原cash/q/desired/成本/risk/context/完整NAV前缀保持，0新日决策，不冒充180日/六折。

只读监控通过：9166研究行、9160旧完整行不变，10报价账户/235观察，gzip4174078字节。HTTP/传输失败实录3次；全部必要pipeline实际退出0。草稿文件工具拒绝及其他实际异常见read_failures/failure_receipts，修复过程保留。合成错误加权负对照实际exit1，正确资本/收益/DD/事件轴与18个L/E邻域检查通过。0金融或已完成观察重跑。清理0真实结果/完整账本，无可重建缓存遗留。

三项验证、spec/数据与源净值哈希/复现代码/完整账本/正负折均保存。main非强制push与完整远端tree/解锁终态见.git/automation_proofs/20261103T120430Z.json。

边界标记已按真实L/E端点独立核对。预登记检查器含旧S轴27/29常量，但本批六个最大值均在L5边界，其已保存标记正确；全部九格正确端点分类另存boundary_verification.json。保留原计算代码绑定，下一轮修正该描述性检查后再绑定；不改本批资格门槛/净值/状态。

通过定义exit750_parent_L3_S28_E375milliPct：3倍收益9.885917%，整体DD3.502611%，与原控制全成本NAV相同=False；仅本批L/E重复历史资格。

通过定义exit750_parent_L3_S28_E625milliPct：3倍收益9.504180%，整体DD4.405505%，与原控制全成本NAV相同=False；仅本批L/E重复历史资格。

通过定义exit750_parent_L4_S28_E375milliPct：3倍收益9.464481%，整体DD3.950896%，与原控制全成本NAV相同=False；仅本批L/E重复历史资格。

通过定义exit750_parent_L4_S28_E625milliPct：3倍收益8.402238%，整体DD4.805394%，与原控制全成本NAV相同=False；仅本批L/E重复历史资格。
