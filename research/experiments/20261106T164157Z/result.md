本轮12个实际新配置：6个ETH原生银行+6个父组合，36成本场景；父组合历史通过0、淘汰6，原生通过0。

此前BTC H3/4/5三个层近期失败区完全相同，BTC侧阈值未解决ETH K1%在D7/8的近期不稳。本轮固定BTC29/H4/E1及原银行名义，直接检验ETH入场波动上限：预定D6/7/8×VC4/4.5/5%，K1%、V10和有限EWM24不变。VC4.5%三组原生与三组父结果只读，其余6ETH原生与6父组合逐项先reserve后实际计算，重算原生数量/成本/资金费/风险，不缩放旧净值。不改门槛或旧资格、不重置四个冻结账户，保留全部正负结果。复用开发历史与多重试验不是独立最终或未来证据。

完整读取28886事件/14321ID与325既往结论；初始16项实际证据齐全（11正式恢复、5原ZIP/WF legacy），保留原缺失字段。此前研究定义10040、标实际9827、未标213，不称所有登记均有回测。

BTC固定ROC29/H4%/E1%、C3750/N1000只读；ETH contrarianROC5/H2%/E0.5%、有限归一化EWM24 beta23/25、strictK1%、D6/7/8、V10样本logvolcap4/4.5/5%，仅新开/反手检查慢趋势与波动门槛，同向保留原q，失败反手平旧不新开。ETHC15000/N4500。raw[1,1]将全银行相加，总18750；资本20/80%不再乘，BTC名义自身26.666667%/总5.333333%，ETH自身30%/总24%。新ETH从原始市场重算数量/LOT/费用/冲击/资金费/风险，不缩放旧NAV或订单；0父订单/转账/重平衡/交叉保证金。

原VC4.5%三个D的原生/父组合共6格只读，原status/criteria/sensitivity不改，D7原父中心原为rejected并保留。六个新原生+六个新父各自预登记和finish，成本压力1/2/3；10个旧结果/6原生银行18成本路径只读。基准为同本金/名义BTC1000+ETH4500原常持有与现金0%。

真实370日2025-10-19 UTC00:01至2026-10-24 UTC00:01，12×30日完整折+10日尾折，近期40日继承day330真实状态8×5日，无折间重开。过去完整收盘信号，下一00:01原生OPEN执行、终点计成本平仓。33上下文满足最多32过去收盘，无fit/labels，purge/embargo0；旧spec遗留warmup30/embargo3字段不改，新spec明确33/0与实际固定规则一致。逐折及整条连续OOS整体DD，不平均组件Sharpe。反复使用开发历史/多重选择，不是未触碰最终或独立未来验证。

二维D/VC半径1含中心；保留所有变体Sharpe/Calmar/整体DD/净收益、72邻接边和边界/cliff，不能据本轮结果扩网格或放宽门槛。原门槛：各成本全期/近期净正，1倍>=9/12正月，各成本近期>=6/8正5日，3倍DD<=25%，邻域3倍正及严格近期合格率>=60%，>=4原生平仓，1倍毛PnL+资金费/执行成本>=2.5，0现金/订单/保证金代理违规、末端flat、>=180日。

成本每边fee5bp+半价差1bp+滑点2bp，impact0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出，收入不放大；真实结算ns/rate/mark/自己的q，资金费不作信号。线性永续无现货借币，不捏造借费；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押与1%闭合小时不利mark风险代理均审计。缺L2/TCA/完整层级/逐tick强平/实际容量证据。

|配置|scope|D|VC|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|volgate370_ETH_D6_VC40000ppm|native|6|0.04|14.239859|12.940640|11.641997|5.346535|2/2/2|rejected|
|volgate370_ETH_D6_VC50000ppm|native|6|0.05|14.907396|13.395589|11.884206|5.230623|2/2/2|rejected|
|volgate370_ETH_D7_VC40000ppm|native|7|0.04|13.326113|11.969381|10.613341|5.346535|2/2/2|rejected|
|volgate370_ETH_D7_VC50000ppm|native|7|0.05|13.993650|12.424330|10.855549|5.230623|2/2/2|rejected|
|volgate370_ETH_D8_VC40000ppm|native|8|0.04|15.660050|14.240411|12.821341|5.346535|3/3/3|rejected|
|volgate370_ETH_D8_VC50000ppm|native|8|0.05|16.327587|14.695360|13.063549|5.230623|3/3/3|rejected|
|volgate370_parent_D6_VC40000ppm|parent|6|0.04|13.427794|12.105844|10.784344|4.933545|6/6/6|rejected|
|volgate370_parent_D6_VC50000ppm|parent|6|0.05|13.961824|12.469803|10.978111|4.845537|6/6/6|rejected|
|volgate370_parent_D7_VC40000ppm|parent|7|0.04|12.696798|11.328837|9.961419|4.933545|5/5/5|rejected|
|volgate370_parent_D7_VC50000ppm|parent|7|0.05|13.230828|11.692796|10.155185|4.845537|5/5/5|rejected|
|volgate370_parent_D8_VC40000ppm|parent|8|0.04|14.563947|13.145661|11.727819|4.933545|5/5/5|rejected|
|volgate370_parent_D8_VC50000ppm|parent|8|0.05|15.097977|13.509620|11.921586|4.845537|5/5/5|rejected|

逐项失败判据：{'volgate370_ETH_D6_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_ETH_D6_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_ETH_D7_VC40000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_ETH_D7_VC50000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_ETH_D8_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_ETH_D8_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_parent_D6_VC40000ppm': ['local_recent6of8_allcost_gte60pct'], 'volgate370_parent_D6_VC50000ppm': ['local_recent6of8_allcost_gte60pct'], 'volgate370_parent_D7_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_parent_D7_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_parent_D8_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgate370_parent_D8_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

四个原冻结账户独立续接、不采用新VC研究：SMA/single Nov6_12:30→14:30，L4/FEWM14:10→16:10。L4/FEWM覆盖16UTC，必须用实际ns/rate/mark和自己的q/cash结算，ETH零持仓也由真实记录推导，不复制账户现金流或重复08/16。SMA原现货Float/SMA65±1%/10bp，无永续资金费。只共享公开行情，原冻结计划/本金/数量/资金费/NAV各自保留；最新完整SMA65日字典仍20261106T023552Z，当前/上一轮为分钟数组，不替代日上下文。全部partial延迟shadow，不冒充180日资格或10策略真实报价。

同main FLOCK内finish后执行只读monitor及检查；不新回测/模拟新成交/改冻结规则或持仓，不重部署/新建定时任务。正负结果、完整账户账本/冻结规则/登记/真实输入永久保留，清理仅可重建中间物。实际push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261106T164157Z.json。

最终结论：本轮无合格新候选，6个新ETH原生和6个新组合全部rejected，已有真实结果且完整保存。六个新组合3倍成本全期净收益9.961419%至11.921586%，整体DD4.845537%至4.933545%；原生3倍净收益10.613341%至13.063549%，DD5.230623%至5.346535%，但全期正收益不能替代近期/邻域门槛。D6两组合每成本6/8正折，邻域合格仅50%<60%；D7/8每成本仅5/8，邻域分别约33.3%与0%。新ETH组件仅2–3/8，D7近期总收益还为负。

新旧VC4/4.5/5%各层近期形状相同：父组合仅D6行满足自身6/8（全网3/9），原生0/9。改变波动过滤未修复K1%弱斜率D7/8失败区。旧VC4.5%的status/criteria/sensitivity仍按旧原邻域保留；这次D/VC是额外诊断，不重写旧资格，也不据当前结果放宽门槛或追加试验。全部36新成本场景、468全期折、288近期折及正负结果留档；无新前向账户、不采用新VC到原冻结规则。

四原账户续接完整且审计通过：SMA NAV51186→51306、累计51269分钟；single NAV15497→15619、384观察ID；L4 NAV8234→8358、207观察ID；FEWM NAV2342→2466、63观察ID/2409分钟。L4/FEWM各用本身持仓独立核算6条实际16UTC资金费，ETH零金额亦有真实rate/mark/ns；single当前0条且下轮独立处理16，不复制现金流或重复结算。原规则/本金/完整NAV链保持，均为partial延迟shadow，无本轮日决策或成交，不冒充180日资格。

封存：6新ETH原生+6新组合/36成本场景，历史通过0、淘汰6；24ID/48事件全部finish，40519旧保护文件保持。6旧原生银行/18成本路径与VC4.5%基线只读，6新ETH原生实际核算。
SMA NAV51186→51306，single NAV15497→15619，L4 NAV8234→8358，FEWM NAV2342→2466。实际新资金费记录single/L4/FEWM为0/6/6，各自真实响应/当时q独立核验，不复制现金流或重复00/08；本轮没有新日事件/成交。FEWM累计2409分钟/63ID，所有账户partial、非180日资格。
只读监控9611行，原9599行完整不变，10报价账户/273观察，gzip4395389字节。行情HTTP/传输失败0次保留；全部正负/淘汰结果、完整账本/冻结规则/登记/真实输入保留。实际push、完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261106T164157Z.json。
