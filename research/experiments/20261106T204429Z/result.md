本轮12个实际新配置：6个ETH原生银行+6个父组合，36成本场景；父组合历史通过6、淘汰0，原生通过0。

前两轮完成K1%和K2%的D/VC批次，K1新组合全部淘汰，K2六新组合通过但ETH单独均近期2/8淘汰，仍有边界和多重选择风险。K3%的VC4.5%三个D旧组合已有实际通过，本轮事前固定K3%，交叉D6/7/8×VC4/4.5/5%，检验更强斜率筛选在邻近波动上限下是否保留原支持。旧VC4.5%的3原生和3父格只读，六新ETH原生和六新父组合各自先reserve后计算，失败门槛、BTC29/H4/E1银行3750/N1000、ETH15000/N4500和raw1/1不变。整份engine与核算字节不改，比较只改变ETH的D/VC、K固定.03；不缩放旧NAV/数量/成本，不改旧资格或四冻结账户。补充只读D×K×VC三维27格对照预先声明，使用K1/K2既有结果及本轮K3登记结果，不新回测/新配置/改判，仅诊断依赖指标。开发历史不称未触碰最终或独立未来。

完整读取29022事件/14389ID与327既往结论；初始16项实际证据齐全（11正式恢复、5原ZIP/WF legacy），保留原缺失字段。此前研究定义10064、标实际9851、未标213，不称所有登记均有回测。

BTC固定ROC29/H4%/E1%、C3750/N1000只读；ETH contrarianROC5/H2%/E0.5%、有限归一化EWM24 beta23/25、strictK3%、D6/7/8、V10样本logvolcap4/4.5/5%，仅新开/反手检查慢趋势与波动门槛，同向保留原q，失败反手平旧不新开。ETHC15000/N4500。raw[1,1]将全银行相加，总18750；资本20/80%不再乘，BTC名义自身26.666667%/总5.333333%，ETH自身30%/总24%。新ETH从原始市场重算数量/LOT/费用/冲击/资金费/风险，不缩放旧NAV或订单；0父订单/转账/重平衡/交叉保证金。

原VC4.5%三个D的原生/父组合共6格只读，原status/criteria/sensitivity不改，原父中心资格原样保留。六个新原生+六个新父各自预登记和finish，成本压力1/2/3；10个旧结果/6原生银行18成本路径只读。基准为同本金/名义BTC1000+ETH4500原常持有与现金0%。

真实370日2025-10-19 UTC00:01至2026-10-24 UTC00:01，12×30日完整折+10日尾折，近期40日继承day330真实状态8×5日，无折间重开。过去完整收盘信号，下一00:01原生OPEN执行、终点计成本平仓。33上下文满足最多32过去收盘，无fit/labels，purge/embargo0；旧spec遗留warmup30/embargo3字段不改，新spec明确33/0与实际固定规则一致。逐折及整条连续OOS整体DD，不平均组件Sharpe。反复使用开发历史/多重选择，不是未触碰最终或独立未来验证。

二维D/VC半径1含中心；保留所有变体Sharpe/Calmar/整体DD/净收益、72邻接边和边界/cliff，不能据本轮结果扩网格或放宽门槛。原门槛：各成本全期/近期净正，1倍>=9/12正月，各成本近期>=6/8正5日，3倍DD<=25%，邻域3倍正及严格近期合格率>=60%，>=4原生平仓，1倍毛PnL+资金费/执行成本>=2.5，0现金/订单/保证金代理违规、末端flat、>=180日。

成本每边fee5bp+半价差1bp+滑点2bp，impact0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出，收入不放大；真实结算ns/rate/mark/自己的q，资金费不作信号。线性永续无现货借币，不捏造借费；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押与1%闭合小时不利mark风险代理均审计。缺L2/TCA/完整层级/逐tick强平/实际容量证据。

|配置|scope|D|VC|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|volgateK3_370_ETH_D6_VC40000ppm|native|6|0.04|6.445124|6.032176|5.619560|2.199826|1/1/1|rejected|
|volgateK3_370_ETH_D6_VC50000ppm|native|6|0.05|7.627641|7.056742|6.486328|4.319870|1/1/1|rejected|
|volgateK3_370_ETH_D7_VC40000ppm|native|7|0.04|9.064224|8.378416|7.693149|4.597594|2/2/2|rejected|
|volgateK3_370_ETH_D7_VC50000ppm|native|7|0.05|9.255199|8.356377|7.457943|4.541797|2/2/2|rejected|
|volgateK3_370_ETH_D8_VC40000ppm|native|8|0.04|8.310337|7.575268|6.840740|4.597594|2/2/2|rejected|
|volgateK3_370_ETH_D8_VC50000ppm|native|8|0.05|8.501311|7.553229|6.605534|4.541797|2/2/2|rejected|
|volgateK3_370_parent_D6_VC40000ppm|parent|6|0.04|7.192007|6.579073|5.966394|1.945462|6/6/6|passed|
|volgateK3_370_parent_D6_VC50000ppm|parent|6|0.05|8.138020|7.398726|6.659809|3.342141|6/6/6|passed|
|volgateK3_370_parent_D7_VC40000ppm|parent|7|0.04|9.287287|8.456065|7.625266|4.696779|6/6/6|passed|
|volgateK3_370_parent_D7_VC50000ppm|parent|7|0.05|9.440067|8.438433|7.437101|4.651242|6/6/6|passed|
|volgateK3_370_parent_D8_VC40000ppm|parent|8|0.04|8.684177|7.813546|6.943338|4.696779|6/6/6|passed|
|volgateK3_370_parent_D8_VC50000ppm|parent|8|0.05|8.836956|7.795915|6.755173|4.651242|6/6/6|passed|

逐项失败判据：{'volgateK3_370_ETH_D6_VC40000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK3_370_ETH_D6_VC50000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK3_370_ETH_D7_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK3_370_ETH_D7_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK3_370_ETH_D8_VC40000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK3_370_ETH_D8_VC50000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'volgateK3_370_parent_D6_VC40000ppm': [], 'volgateK3_370_parent_D6_VC50000ppm': [], 'volgateK3_370_parent_D7_VC40000ppm': [], 'volgateK3_370_parent_D7_VC50000ppm': [], 'volgateK3_370_parent_D8_VC40000ppm': [], 'volgateK3_370_parent_D8_VC50000ppm': []}。

四个原冻结账户独立续接、不采用新VC研究：SMA/single Nov6_16:30→18:30，L4/FEWM18:10→20:10。single的16UTC已在前轮结算，L4/FEWM的16UTC更早已各自结算；本轮三个永续账户都在16之后，只据各自真实响应和游标续记新行情，不重复资金费。ETH零持仓也由真实记录推导，不复制账户现金流或重复08/16。SMA原现货Float/SMA65±1%/10bp，无永续资金费。只共享公开行情，原冻结计划/本金/数量/资金费/NAV各自保留；最新完整SMA65日字典仍20261106T023552Z，当前/上一轮为分钟数组，不替代日上下文。全部partial延迟shadow，不冒充180日资格或10策略真实报价。

同main FLOCK内finish后执行只读monitor及检查；不新回测/模拟新成交/改冻结规则或持仓，不重部署/新建定时任务。正负结果、完整账户账本/冻结规则/登记/真实输入永久保留，清理仅可重建中间物。实际push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261106T204429Z.json。

实际结论：六新父组合各成本全期/近期净正，1倍9–11/12完整月正折，各成本近期均6/8正五日折，D/VC邻域3倍正率及严格近期合格率均100%，通过原筛选。三倍全期净收益5.966394%–7.625266%，连续整体DD1.945462%–4.696779%。六新ETH组件因近期仅1/8(D6)或2/8(D7/8)、邻域严格近期率0全部淘汰，D6另仅7或8/12正月未达门槛；即便全期与近期净正也不改判。逐折负数和零折永久保留。

逐格查看8面板：两侧新格N、中列VC4.5%旧格O正确；所有scope/成本都有描述性Sharpe邻接变化标记，最高Sharpe位于D6/VC4.5%边界，不称无悬崖或广泛稳定平台。更强K3并未修复ETH近期稀疏正折，组合6/8不能解释成ETH组件独立稳健。K1/K2/K3三维补充只读取已登记的原结果，不重算旧配置或改判。

事前声明的三维只读对照实际完成：D×K×VC每scope27格、共54已登记格，162成本指标行、324邻接边，0新估值。组合严格近期指标合格格数K1/K2/K3为3/9、9/9、9/9；ETH原生各K均0/9。全部格三倍全期净正，但不能把严格近期格数当总体passed数，也不重写原canonical资格。所有原scenes/criteria/sensitivity/登记report SHA逐格一致。共享BTC和ETH账本导致依赖，多重选择和边界/邻接变化风险保留，不称54独立新试验、稳定实盘盈利或独立前向验证。

四账户本轮均没有新日事件/成交/资金费，原16资金费游标保留；完整SMA51,546点、single15,865点、L4 8,602点、FEWM2,710点净值全部保留并独立核验。candidate首次GET发生curl35/HTTP0，重试成功，失败原始响应及全部19份当前raw证据保留。

所有实际配置完成finish；财务链、输出/账户链、五review及登记/只读monitor/feed/collect链工具进程均真实退出0，见execution_tool_terminal_receipts.json。监控9635研究行、原9623行完整不变，10报价账户/275观察，gzip4408924字节；完整账本、冻结规则、登记、正负折和必要数据保留，0实际结果或账本删除。

只读三维对照：54个既有登记格/162成本指标行/324邻接边，新增估值0；原canonical资格不改。各K诊断详见readonly_cross_K_diagnostic.json，不称独立54次试验或未来验证。
封存：6新ETH原生+6新组合/36成本场景，历史通过6、淘汰0；24ID/48事件全部finish，41158旧保护文件保持。6旧原生银行/18成本路径与VC4.5%基线只读，6新ETH原生实际核算。
SMA NAV51426→51546，single NAV15743→15865，L4 NAV8480→8602，FEWM NAV2588→2710。实际新资金费记录single/L4/FEWM为0/0/0，各自真实响应/当时q独立核验，不复制现金流或重复00/08/16；本轮没有新日事件/成交。FEWM累计2649分钟/69ID，所有账户partial、非180日资格。
只读监控9635行，原9623行完整不变，10报价账户/275观察，gzip4408924字节。行情HTTP/传输失败1次保留；全部正负/淘汰结果、完整账本/冻结规则/登记/真实输入保留。实际push、完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261106T204429Z.json。
