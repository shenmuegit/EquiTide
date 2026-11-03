固定快窗L4的退出缓冲×慢窗真实交叉验证

上轮L4/E0.375%及E0.625%在S28满足L/E历史门槛并改善旧控制，但慢窗S27/29已有脆弱证据。本轮只预设固定快L4、S27/28/29×E0.375/0.5/0.625%交叉，检验退出缓冲能否修复慢窗依赖。五格原生与五格组合实际结果只读，四角ETH参数变化须真实重新计算，四角组合复用实际BTC750及对应ETH新净值。逐项先reserve8定义，再12原生+12组合成本场景；不是历史数据的独立最终测试或实盘稳定利润。

完整读取26494事件/13125ID、288份既往结论。初始16有原档实际证据，缺实际结果0。此前研究定义9607，标实际结果9394，未标213；大量重复历史搜索存在多重选择偏差，不能说所有登记均有实际回测。

预设快L4，慢S27/28/29×退出E0.375/0.5/0.625%，HL1.5%/HS2.5%、V10/cap4.5%。五格原生/五格组合已有实际结果只读。四角新ETH原生各15000本金/N4500，必须真实重算信号、LOT数量、成本、资金费与现金；四角新组合复用实际BTC3750/N750与对应新ETH净值。raw[1,1]为完整银行所有权，总本金18750、银行资金份额20/80%、初始入场名义占比4/24%；不归一化、不重复乘资金份额、不缩放数量/净值，不平均收益/Sharpe/DD，不跨银行转移/调仓。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，真实连续370日、12×30日完整折+10日尾折；完整OOS曲线算整体DD，不按折重开。近期40日从day330真实持仓/现金承接，8×5日。固定规则无拟合/标签，purge0，30日预热+3日间隔，过去已完成日线决定下一00:01原生OPEN，终点计成本平仓。该历史反复使用，不能称未触碰最终测试或独立未来验证。

成本：每侧5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)，不使用未来量价；1/2/3倍压力放大所有支出和资金费支出，收入不放大。真实settlement ns/rate/mark/heldq资金费；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark保证金代理。线性永续空头无现货借币，不虚构借币费。父无新订单/额外成本。匹配持有复用相同银行和入场N750/4500，另比现金0%。缺盘口/TCA、历史完整层级/最大量、逐tick强平与容量证明。

失败门槛事先固定：全年各成本正，1倍>=9/12正完整月，近期各成本总收益正且>=6/8正5日折，3倍整体DD<=25%；含中心S/E索引半径1邻域3倍正与严格近期合格比例均>=60%；>=4底层平仓，毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat，至少180日。所有新原生/新组合按同一门槛分别裁定；旧canonical状态/判据/敏感性和旧报告不改，本批S/E诊断另列。

|新配置|scope|S|E比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|corner750_ETH_L4_S27_E375milliPct|native|27|0.00375|14.202303|12.286488|10.370033|4.170961|8|3/3/3|rejected|
|corner750_ETH_L4_S27_E625milliPct|native|27|0.00625|12.043911|10.111939|8.178637|5.420307|8|3/3/3|rejected|
|corner750_ETH_L4_S29_E375milliPct|native|29|0.00375|15.765269|13.785978|11.805672|4.259356|10|4/4/4|rejected|
|corner750_ETH_L4_S29_E625milliPct|native|29|0.00625|14.332360|12.396176|10.458634|5.518046|9|4/4/4|rejected|
|corner750_parent_L4_S27_E375milliPct|parent|27|0.00375|12.490336|10.764643|9.038444|3.637216|9|4/4/4|rejected|
|corner750_parent_L4_S27_E625milliPct|parent|27|0.00625|10.763623|9.025003|7.285327|4.482669|9|4/4/4|rejected|
|corner750_parent_L4_S29_E375milliPct|parent|29|0.00375|13.740710|11.964234|10.186955|3.627648|11|5/5/5|rejected|
|corner750_parent_L4_S29_E625milliPct|parent|29|0.00625|12.594383|10.852393|9.109325|4.479967|10|5/5/5|rejected|

四个新组合通过0、淘汰4；四个新原生独立状态亦在表内。逐项失败{'corner750_ETH_L4_S27_E375milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'corner750_ETH_L4_S27_E625milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'corner750_ETH_L4_S29_E375milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'corner750_ETH_L4_S29_E625milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'corner750_parent_L4_S27_E375milliPct': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'corner750_parent_L4_S27_E625milliPct': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'corner750_parent_L4_S29_E375milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'corner750_parent_L4_S29_E625milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。新组合对同E/S28控制全成本NAV同路径0/4，差异及同S/E0.5%控制逐成本对比均保存。正收益不等于稳健或稳定实盘盈利。

11CSV保存24新场景、312逐月/尾折、192近期折、8904日NAV、两张九格敏感性、15旧组合场景、72相邻边、27持有/现金比较、36新旧原生成本路径与10资金分配。图中两个scope均为四角N=新、五格O=旧只读；完整DD/Sharpe/Calmar与负收益折全部保留。边界按真实S/E端点检查；相邻悬崖为描述性依赖样本统计，不是DSR/PBO或事后新增门槛。

原SMA65与single续10:30→12:30；独立原L4/H2续12:10→14:10，仅14:11执行参考闭合后采集。原现金/q/desired/成本/risk/context/完整NAV前缀连续，不改冻结规则/本金/持仓/终止日，不重复08/00资金费，不采纳本批参数。SMA真实65日上下文源20261103T020232Z/forward_inputs.json.gz不变。延迟真实数据shadow与十策略实盘报价模拟分开，部分观测不冒充180日/六折资格。

一手资料2026-11-03实际访问：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。官方真实资金费字段不证明策略盈利、容量或实时成交。8行情/mark/资金费/元数据文件边界/字节/SHA与不可变实现哈希见plan和data_manifest。

全部八项先逐项成功reserve，才计算12原生及12组合成本路径。预登记前合成检查覆盖完整银行资本恒等式、平均DD/收益错误、事件轴错位、18个S/E邻域、未来close不可见、S27与S29索引区分及退出等号边界。独立Fraction信号与Decimal数量/成本/资金费/小时风险及全净值核验；旧实现、源和报告保留。原生/组合成功与负结果均分别finish，失败记录不删。

本轮只清理可重建中间件，保留完整账本及核验必需证据；同一main排他锁内生成只读监控、提交非强制push，发布/远端完整tree/锁释放终态见.git/automation_proofs/20261103T140600Z.json。

封存：8新定义/24成本场景分别finish，4新组合通过0、淘汰4；4新原生通过0、淘汰4。独立核验4440新信号决策、12新原生成本曲线及12新父曲线，全部新NAV13080312点，计数{'funding': 39960, 'fills': 1962, 'rejects': 0, 'metric_checks': 672, 'margin_checks': 154854}。24旧原生成本曲线只读核验，资金费/成交为旧账本记录；新原生资金费13320条、成交846笔是实际历史回测模拟。0新BTC/基准/父订单。17新ID/34追加事件；29316旧保护文件不变。

四个新组合对同E/S28控制全成本同路径0/4。旧S28/E0.375、E0.5、E0.625等格在本轮S/E邻域支持另列[{'fingerprint': 'ba2f6359edf2736207258286d8dd158a860e6f8e2622177d3ea9b7d0f48112c8', 'L': 4, 'S': 27, 'E': 0.005, 'canonical_status': 'rejected', 'current_neighbors': 6, 'current_local_strict_recent_fraction': 0.5}, {'fingerprint': 'f8670c088f666dc9082c837cdad6ff298176204f8f2abbd00318683bc345e69d', 'L': 4, 'S': 28, 'E': 0.00375, 'canonical_status': 'passed', 'current_neighbors': 6, 'current_local_strict_recent_fraction': 0.3333333333333333}, {'fingerprint': '6bfd73012abf91fc461b9570030d75830985f75a128cf28bc7fad00b9c10e6f9', 'L': 4, 'S': 28, 'E': 0.005, 'canonical_status': 'passed', 'current_neighbors': 9, 'current_local_strict_recent_fraction': 0.3333333333333333}, {'fingerprint': '0f08d4bfea2b4dae3d263ea0a5f4004e8d5ad585ad40619bb40a5adfae3026ec', 'L': 4, 'S': 28, 'E': 0.00625, 'canonical_status': 'passed', 'current_neighbors': 6, 'current_local_strict_recent_fraction': 0.3333333333333333}, {'fingerprint': 'f55c912eb4f7d1089487b0145d7d05d4b793de71eda926c43e69d64ae2ad7316', 'L': 4, 'S': 29, 'E': 0.005, 'canonical_status': 'rejected', 'current_neighbors': 6, 'current_local_strict_recent_fraction': 0.5}]。此前L/E通过记录仍保留原资格，不能据年度净收益称跨慢窗稳健；这次是真实参数变化后的交叉证据，不是旧净值缩放。完整差异与同S/E0.5%控制比较见equivalent_realized_NAV_paths.json。

原SMA续2026-11-03T10:30:00Z至2026-11-03T12:30:00Z，NAV46743+120=46863、累计46829分钟/32完整日；single续2026-11-03T10:30:00Z至2026-11-03T12:30:00Z，NAV11078、累计273ID；L4/H2续2026-11-03T12:10:00Z至2026-11-03T14:10:00Z，仅14:11参考闭合后采集，NAV3815、累计96ID。新资金费single=[]、L4=[]，成交single=0、L4=0，0新日决策。所有真实book/risk/context/NAV前缀连续，08/00不重复、不改冻结规则/本金/终止日；partial不冒充180日/六折，不采纳本批参数。

监控通过：9174研究行、9166旧完整行不变，10报价账户/236观察，gzip4178881字节。实际HTTP/传输失败3次及HTTPSGit预检失败保留，必要pipeline实际退出0。错误双重加权负对照实际exit1，正确完整银行资本/收益/DD与错位事件轴拒绝、未来价格不可见/退出等号/S索引及18邻域检查均通过。0已完成回测或观察重跑。清理0真实结果/完整账本、无可重建缓存遗留。

全部正负场景、逐折/全曲线DD、spec/代码/数据和NAV哈希/完整账本/失败响应保存。main非强制push、完整远端tree与实际终态/解锁凭据见.git/automation_proofs/20261103T140600Z.json。
