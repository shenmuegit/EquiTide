本轮12个实际新配置：6个ETH原生银行+6个父组合，36成本场景；父组合历史通过6、淘汰0，原生通过0。

前轮K1%在D/VC二维邻域全部12新配置淘汰，且改变入场波动上限未修复弱斜率近期失败。K2%的VC4.5%三D父组合已有历史通过，本轮事前固定更强K2%，交叉D6/7/8×VC4/4.5/5%，检验原支持是否能延伸到两侧波动上限。六个旧原生/父基线只读，6新ETH原生+6新父组合各自先reserve后实际核算；BTC29/H4/E1银行3750/N1000与ETH15000/N4500、raw1/1及失败门槛不改。整份策略引擎与账户核算字节不变，只改变新spec中的K/VC；不缩放旧NAV/数量/成本、不改旧canonical资格或四个冻结账户。保留全部正负结果，复用开发历史与多重选择不是独立最终或未来验证。

完整读取28954事件/14355ID与326既往结论；初始16项实际证据齐全（11正式恢复、5原ZIP/WF legacy），保留原缺失字段。此前研究定义10052、标实际9839、未标213，不称所有登记均有回测。

BTC固定ROC29/H4%/E1%、C3750/N1000只读；ETH contrarianROC5/H2%/E0.5%、有限归一化EWM24 beta23/25、strictK2%、D6/7/8、V10样本logvolcap4/4.5/5%，仅新开/反手检查慢趋势与波动门槛，同向保留原q，失败反手平旧不新开。ETHC15000/N4500。raw[1,1]将全银行相加，总18750；资本20/80%不再乘，BTC名义自身26.666667%/总5.333333%，ETH自身30%/总24%。新ETH从原始市场重算数量/LOT/费用/冲击/资金费/风险，不缩放旧NAV或订单；0父订单/转账/重平衡/交叉保证金。

原VC4.5%三个D的原生/父组合共6格只读，原status/criteria/sensitivity不改，原父中心资格原样保留。六个新原生+六个新父各自预登记和finish，成本压力1/2/3；10个旧结果/6原生银行18成本路径只读。基准为同本金/名义BTC1000+ETH4500原常持有与现金0%。

真实370日2025-10-19 UTC00:01至2026-10-24 UTC00:01，12×30日完整折+10日尾折，近期40日继承day330真实状态8×5日，无折间重开。过去完整收盘信号，下一00:01原生OPEN执行、终点计成本平仓。33上下文满足最多32过去收盘，无fit/labels，purge/embargo0；旧spec遗留warmup30/embargo3字段不改，新spec明确33/0与实际固定规则一致。逐折及整条连续OOS整体DD，不平均组件Sharpe。反复使用开发历史/多重选择，不是未触碰最终或独立未来验证。

二维D/VC半径1含中心；保留所有变体Sharpe/Calmar/整体DD/净收益、72邻接边和边界/cliff，不能据本轮结果扩网格或放宽门槛。原门槛：各成本全期/近期净正，1倍>=9/12正月，各成本近期>=6/8正5日，3倍DD<=25%，邻域3倍正及严格近期合格率>=60%，>=4原生平仓，1倍毛PnL+资金费/执行成本>=2.5，0现金/订单/保证金代理违规、末端flat、>=180日。

成本每边fee5bp+半价差1bp+滑点2bp，impact0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出，收入不放大；真实结算ns/rate/mark/自己的q，资金费不作信号。线性永续无现货借币，不捏造借费；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押与1%闭合小时不利mark风险代理均审计。缺L2/TCA/完整层级/逐tick强平/实际容量证据。

|配置|scope|D|VC|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|volgateK2_370_ETH_D6_VC40000ppm|native|6|0.04|13.221871|12.348916|11.476407|4.016910|2/2/2|rejected|
|volgateK2_370_ETH_D6_VC50000ppm|native|6|0.05|13.412846|12.326877|11.241201|4.211092|2/2/2|rejected|
|volgateK2_370_ETH_D7_VC40000ppm|native|7|0.04|14.387539|13.362100|12.337235|3.953481|2/2/2|rejected|
|volgateK2_370_ETH_D7_VC50000ppm|native|7|0.05|14.578514|13.340060|12.102029|4.097498|2/2/2|rejected|
|volgateK2_370_ETH_D8_VC40000ppm|native|8|0.04|15.630154|14.490284|13.350990|3.935413|2/2/2|rejected|
|volgateK2_370_ETH_D8_VC50000ppm|native|8|0.05|16.403404|15.002140|13.601301|4.424854|2/2/2|rejected|
|volgateK2_370_parent_D6_VC40000ppm|parent|6|0.04|12.613404|11.632465|10.651872|3.732829|6/6/6|passed|
|volgateK2_370_parent_D6_VC50000ppm|parent|6|0.05|12.766184|11.614833|10.463707|3.696684|6/6/6|passed|
|volgateK2_370_parent_D7_VC40000ppm|parent|7|0.04|13.545939|12.443012|11.340535|3.685387|6/6/6|passed|
|volgateK2_370_parent_D7_VC50000ppm|parent|7|0.05|13.698719|12.425380|11.152370|3.650151|6/6/6|passed|
|volgateK2_370_parent_D8_VC40000ppm|parent|8|0.04|14.540031|13.345559|12.151538|3.671819|6/6/6|passed|
|volgateK2_370_parent_D8_VC50000ppm|parent|8|0.05|15.158630|13.755044|12.351787|3.727298|6/6/6|passed|

逐项失败判据：{'volgateK2_370_ETH_D6_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK2_370_ETH_D6_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK2_370_ETH_D7_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK2_370_ETH_D7_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK2_370_ETH_D8_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK2_370_ETH_D8_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK2_370_parent_D6_VC40000ppm': [], 'volgateK2_370_parent_D6_VC50000ppm': [], 'volgateK2_370_parent_D7_VC40000ppm': [], 'volgateK2_370_parent_D7_VC50000ppm': [], 'volgateK2_370_parent_D8_VC40000ppm': [], 'volgateK2_370_parent_D8_VC50000ppm': []}。

四个原冻结账户独立续接、不采用新VC研究：SMA/single Nov6_14:30→16:30，L4/FEWM16:10→18:10。single本轮跨越16UTC，用实际ns/rate/mark和自己的q/cash结算；L4/FEWM的16UTC已在前轮各自结算，本轮16:10之后只续记新行情，保留各自资金费游标，不能重复结算。ETH零持仓也由真实记录推导，不复制账户现金流或重复08/16。SMA原现货Float/SMA65±1%/10bp，无永续资金费。只共享公开行情，原冻结计划/本金/数量/资金费/NAV各自保留；最新完整SMA65日字典仍20261106T023552Z，当前/上一轮为分钟数组，不替代日上下文。全部partial延迟shadow，不冒充180日资格或10策略真实报价。

同main FLOCK内finish后执行只读monitor及检查；不新回测/模拟新成交/改冻结规则或持仓，不重部署/新建定时任务。正负结果、完整账户账本/冻结规则/登记/真实输入永久保留，清理仅可重建中间物。实际push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261106T184255Z.json。

本轮结论：六个新组合在三档成本下全期及近期净正，1倍完整月正折为10或11/12，各成本近期均6/8正五日折；二维邻域3倍净正率和严格近期合格率均100%，通过原筛选。三倍成本净收益10.463707%–12.351787%，连续整体DD3.650151%–3.732829%。六个新ETH组件全期/近期净正，但近期均2/8正折、邻域严格近期合格率0，全部淘汰。没有负收益单项被隐藏，逐折负数和零折保留。

敏感性图逐格复核：9格组合近期均6/8、9格ETH原生均2/8；中列VC4.5%三个D格为旧结果O，外侧六格为新结果N。全部网格与三个成本都有描述性Sharpe邻接变化标记，最大Sharpe格在D8/VC4.5%边界；不称无参数悬崖、广泛稳定平台或独立样本。本轮支持固定K2%在预定波动上限邻域的历史组合筛选，但没有修复单ETH近期稀疏正折。与上轮K1%的差异只作开发历史比较，不据此认定独立改进。report中current_grid_diagnostic_sensitivity.scope的D/K为遗留文字；真实已冻结且核验的两轴为D/VC，K固定.02，保留finish后的原report字节。

完成核验：summary/exports/decisions/grid及四账户续记整个工具进程退出0；四独立review与source/registry/monitor/feed/collect整个工具进程退出0，真实tool终态见execution_tool_terminal_receipts.json。48事件/24ID全部finish；同锁只读监控9623研究行、10报价账户/274观察，gzip4402640字节。19个当前raw证据（含candidate一次curl35失败）及旧FEWM暖机均保留。

封存：6新ETH原生+6新组合/36成本场景，历史通过6、淘汰0；24ID/48事件全部finish，40835旧保护文件保持。6旧原生银行/18成本路径与VC4.5%基线只读，6新ETH原生实际核算。
SMA NAV51306→51426，single NAV15619→15743，L4 NAV8358→8480，FEWM NAV2466→2588。实际新资金费记录single/L4/FEWM为6/0/0，各自真实响应/当时q独立核验，不复制现金流或重复00/08/16；本轮没有新日事件/成交。FEWM累计2529分钟/66ID，所有账户partial、非180日资格。
只读监控9623行，原9611行完整不变，10报价账户/274观察，gzip4402640字节。行情HTTP/传输失败1次保留；全部正负/淘汰结果、完整账本/冻结规则/登记/真实输入保留。实际push、完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261106T184255Z.json。
