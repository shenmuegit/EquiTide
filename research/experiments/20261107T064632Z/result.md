本轮6新BTC组件＋6新组合/36成本场景实算；新组合通过0/6、淘汰6/6。原27日三个门槛组件及组合只读，未重跑或改资格。

上轮BTC27日配不同ETH门槛仍近期5/8不足，本轮实际改变BTC响应时钟；不是再组合旧净值。本轮固定BTC1000/3750与ETH4500/15000，事前测试BTC回看23/25/27日×严格入场3/4/5%，退出E1%不变；较短响应可能改善反转也可能提高换手/成本。ETH固定D7/K2%、L5/S24/E.005/entry-only/V10cap.045。已有27日三个门槛原组件和组合只读；6新BTC组件与6新父组合先reserve再实际计算。代表点25/4%事先固定；原门槛与原权重1/1不变，不根据当前结果扩展。全部正负结果留存，重复开发历史不能称独立最终或实盘收益。

完整读取29372事件/14564ID、332既往结论。初始16项均有实际证据（11正式恢复、5原ZIP/WF legacy），缺0，不改缺失字段。此前研究定义10129，标实际9916，未标213；不称全部登记都有回测。

BTC3750银行/N1000，L23/25/27×H3/4/5%，E1%固定；ETH15000/N4500固定L5/H2%/E0.5%、有限归一化EWM24 beta23/25、D7/K2%、仅新开/反手慢趋势与V10样本logvol上限4.5%。raw[1,1]相加完整银行，总本金18750，20/80%资本份额不重复乘；BTC名义占自身26.666667%/总5.333333%，ETH占自身30%/总24%。6新BTC按真实价格/旧核算实际生成信号、LOT、数量、费用/价差/滑点/冲击、资金费和风险，不缩放旧NAV。父组合不下额外订单/再平衡/转移/交叉保证金。

370日连续验证2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折＋10日尾折；近期40日继承day330原状态，8×5日，无重开。过去完整收盘形成信号，下一00:01原生OPEN执行，反手先平后开，同向保留实际数量，终点计成本平仓。源上下文33日足够最大31过去收盘；固定规则无拟合/标签，purge/embargo0。原27日三个门槛网格边界行保持原canonical资格，只做当前邻域诊断。完整分钟/事件NAV整体回撤不平均组件统计；反复使用历史及多重选择不是独立最终或未来验证。

成本每边5bp费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；真实结算ns/rate/mark/当时q，资金费仅事后核算。线性永续不用现货借币，不捏造借费；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark保证金代理均审核。缺历史L2/TCA/完整层级/逐tick强平与真实容量证据。

BTC L/H两轴原生与组合各9格，邻域索引半径1含中心。全部变体收益、整体DD、Sharpe、Calmar、72邻接边、平台/孤峰/最高Sharpe边界均留存；边界不触发本轮事后扩网格。失败门槛沿用：各成本全期/近期净正、1倍至少9/12正月、各成本近期至少6/8正5日、3倍DD<=25%、邻域3倍正收益及全成本近期合格率>=60%、>=4平仓、1倍毛PnL+资金费/执行成本>=2.5、0余额/订单/保证金代理违规、终点flat、>=180日。与匹配同本金/名义持有及现金0%比较。

|新配置|类别|BTC L|H|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|btcreaction370_BTC_N1000_L23_H300bp|native|23|0.03|-3.152643|-4.643139|-6.133656|15.098827|4/4/4|rejected|
|btcreaction370_BTC_N1000_L23_H400bp|native|23|0.04|2.007875|0.726809|-0.554238|12.208302|4/4/4|rejected|
|btcreaction370_BTC_N1000_L23_H500bp|native|23|0.05|4.825975|3.710339|2.594662|8.932247|3/3/3|rejected|
|btcreaction370_BTC_N1000_L25_H300bp|native|25|0.03|-2.304444|-3.805268|-5.306264|12.593459|4/4/4|rejected|
|btcreaction370_BTC_N1000_L25_H400bp|native|25|0.04|3.524156|2.371773|1.219350|7.810869|3/3/3|rejected|
|btcreaction370_BTC_N1000_L25_H500bp|native|25|0.05|6.649507|5.664397|4.679278|5.961575|3/3/3|rejected|
|btcreaction370_parent_L23_H300bp|parent|23|0.03|11.523063|10.317629|9.112523|3.756492|5/5/5|rejected|
|btcreaction370_parent_L23_H400bp|parent|23|0.04|12.555166|11.391618|10.228406|3.779727|5/5/5|rejected|
|btcreaction370_parent_L23_H500bp|parent|23|0.05|13.118786|11.988324|10.858186|3.687771|4/4/4|rejected|
|btcreaction370_parent_L25_H300bp|parent|25|0.03|11.692703|10.485203|9.278001|3.693445|5/5/5|rejected|
|btcreaction370_parent_L25_H400bp|parent|25|0.04|12.858423|11.720611|10.583124|3.732310|4/4/4|rejected|
|btcreaction370_parent_L25_H500bp|parent|25|0.05|13.483493|12.379136|11.275110|3.675672|4/4/4|rejected|

实际失败项：{'btcreaction370_BTC_N1000_L23_H300bp': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_positive3_gte60pct', 'local_recent6of8_allcost_gte60pct', 'gross_plus_funding_to_cost1_gte2_5'], 'btcreaction370_BTC_N1000_L23_H400bp': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_positive3_gte60pct', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L23_H500bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L25_H300bp': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_positive3_gte60pct', 'local_recent6of8_allcost_gte60pct', 'gross_plus_funding_to_cost1_gte2_5'], 'btcreaction370_BTC_N1000_L25_H400bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_positive3_gte60pct', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L25_H500bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L23_H300bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L23_H400bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L23_H500bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L25_H300bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L25_H400bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L25_H500bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

四个原冻结账户分别续自己的现金/实际q/成本/风险/fullNAV，不采用研究L/H。SMA/single Nov7_02:30→04:30；L4/FEWM04:10→06:10，均只增加闭合mark/风险，无新日决策、资金费或成交，不重复午夜。当前与上一轮SMA为分钟数组，完整65日现货上下文仍20261107T024625Z/forward_inputs.json.gz；保留原Float/SMA65±1%及10bp成本。FEWM仍D1/K.0005、BTC750/ETH4500；所有为未成熟延迟shadow，非180日/六折或十策略实时报价模拟业绩。

同main排他锁内登记/必要检查后只读生成monitor，不回测监控、不造新成交或改冻结规则/本金/持仓；不重新部署或建定时任务。全部正负/淘汰结果、完整账本/登记/输入/必要代码保留，仅清理可重建中间物。实际非强制push、远端完整tree/blob及解锁终态在.git/automation_proofs/20261107T064632Z.json。

实际三项验证结论：walk-forward时序与逐折核验已完成；组合6/6满足全期1倍至少9/12正月，但近期仅4–5/8，BTC组件6/6近期与正月均不足。两轴敏感性已完成，原生与组合各9格严格近期合格均0/9，12个新配置严格近期邻域门槛均失败。1/2/3倍成本已完成，组合6/6净正、原生仅3/6三档均净正；三倍成本原生范围−6.133656%至+4.679278%，组合+9.112523%至+11.275110%，组合连续OOS整体DD3.675672%至3.779727%。全部12个真实新配置淘汰，负收益和负折永久保留，不因组合总收益正而放宽近期或邻域要求。事前代表L25/H4组合三倍10.583124%、DD3.732310%，近期4/8，仍淘汰。

预登记前工程失败：合成检查实际退出1，原因是旧引擎允许值仅27/29/31日；原源码和首版spec/plan完整保存在prebinding_failed_initial/。仅变更允许值为23/25/27，AST核验信号公式和核算完全相同，在首次reserve前重新冻结并通过检查。未发生任何完整回测或账户窗口重跑。部分沿用检查stdout仍写旧批次16/48等标签；结构化report/plan、36场景CSV、独立审计与登记均为本轮12定义/36场景，保留stdout原字节，不将旧字样计为实际执行数量。

已于2026-11-07查阅[Binance官方市场数据字段](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对K线与fundingTime/fundingRate/markPrice；费用与冲击仍为声明估计，没有真实盘口TCA或容量证明。

原账户实际续接：SMA NAV52027→52147，累计52109分钟/36完整日，三个成本累计收益−6.982980%/−7.226287%/−7.468958%，原Float现金/units/desired/交易成本保持。single NAV16358→16480、405ID/16109分钟；L4 NAV9095→9217、228ID/9009分钟；FEWM NAV3203→3325、84ID/3249分钟。三永续各自完整前缀、真实持仓、现金、风险与上下文独立核对；当前所有窗口新日事件、资金费和成交均0。SMA一次TLS连接失败由既有GET重试恢复，原stderr留档，最终两份真实分钟响应及重叠bar核验通过；没有重跑完整账户或回测。下一日决策均Nov8_00:01，后续08资金费只按实际窗口与自身q/rate/mark/ns计入。全部是partial延迟shadow，不是十策略实时报价业绩或180日资格。

封存：6新BTC组件＋6新组合/36成本场景，新组合通过0、淘汰6；24ID/48事件全部finish，42843旧保护文件保持。18旧原生成本路径只读，18新BTC原生成本路径/6660实际新决策及18新组合路径独立核验。
原SMA NAV52027→52147，single NAV16358→16480，L4 NAV9095→9217，FEWM NAV3203→3325。L4/FEWM实际新资金费记录0/0，各自按真实rate/mark/ns/持仓独立计算；日事件与成交均0，不重复00或复制现金流。FEWM累计3249分钟/84ID，全部账户partial、非180日资格。
只读监控9700行，原9688行完整不变，10报价账户/280观察，gzip4446714字节。行情HTTP/传输失败1次原证据保留；所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。实际push、完整远端tree/blob及解锁终态见.git/automation_proofs/20261107T064632Z.json。
