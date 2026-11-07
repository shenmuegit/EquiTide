本轮6新BTC组件＋6新组合/36成本场景实算；新组合通过6/6、淘汰0/6。已有L29/E1%的H3/4/5%三格原组件和组合只读，未重跑或改资格。

上轮BTC23/25日回看未解决近期4–5/8问题。本轮固定旧29日响应与本金/名义，事前测试H3/4/5%×持仓退出缓冲E0.5/1/1.5%。更紧缓冲可能更快退出反向噪声却增加换手，更宽缓冲可能降低抖动却提高趋势逆转损失；不按当前结果选择解释。已有E1%三格只读；6新BTC组件和6新组合全部先reserve，再真实LOT/数量/成本/资金费/风险/完整NAV计算。ETH固定旧D7/K2/V10cap4.5%银行，总C18750和raw1/1不变。事前关注H4%/E1.5%，门槛不改、全部正负结果保留；重复开发历史不是独立留出或实盘稳定收益。

完整读取29440事件/14598ID、333既往结论。初始16项实际证据齐全，缺0；此前研究定义10141，标实际9928、未标213，不称所有登记都有结果。

BTC固定L29、C3750/N1000，H3/4/5%×退出缓冲E0.5/1/1.5%；strictH入场优先，区间内旧long在ROC>-E时持有、旧short在ROC<E时持有，等于退出边界即平仓。反手先平后开，同方向留实际数量，不日再平衡。ETH固定C15000/N4500、L5/H2%/E0.5%、finiteEWM24 beta23/25、D7/K2%、entry-only V10样本logvol上限4.5%。Raw[1,1]相加完整银行，总本金18750，20/80资本份额不重复乘、不归一化、不缩放旧NAV/数量/成本，无父订单/转账/交叉保证金。

370日连续OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折＋10日尾；近期40日继承day330现金/持仓8×5日，无折间重开。BTC需30过去完整收盘、ETH需31，源33足够；过去完整收盘发信号，下一00:01OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。报告逐折和完整OOS整体DD；重复开发历史及多重选择不能叫未触碰最终、独立未来或稳定实盘盈利。

每边5bp费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出、收入不放大；真实fundingTime/rate/mark/当时q，线性永续无现货借币。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark保证金代理核验；缺L2/TCA/完整层级/逐tick强平与真实容量证据。

H/E两轴原生和组合各9格，E1%三格只读；索引半径1含中心。保留全部变体收益/整体DD/Sharpe/Calmar、72邻接边、平台/孤峰/边界。门槛原样：全期各成本净正、1倍>=9/12正月、近期各成本净正且>=6/8正五日、3倍DD<=25%、局部三倍净正及严格近期合格率>=60%、>=4原生平仓、毛PnL+资金费/1倍成本>=2.5、零抵押/订单/风险违规、终点flat、>=180日。与同本金/名义常持有及现金0%比较，不以本轮结果改门槛。

|新配置|类别|BTC L|H|E|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|btcHysteresis370_BTC_L29_H300bp_E5000ppm|native|29|0.03|0.005|11.070375|9.566541|8.062719|6.811608|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H400bp_E5000ppm|native|29|0.04|0.005|9.250408|7.813500|6.376537|6.847095|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H500bp_E5000ppm|native|29|0.05|0.005|8.877905|7.827754|6.777657|6.130237|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H300bp_E15000ppm|native|29|0.03|0.015|9.847658|8.338880|6.829980|7.030198|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H400bp_E15000ppm|native|29|0.04|0.015|8.219791|6.784910|5.349867|6.947580|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H500bp_E15000ppm|native|29|0.05|0.015|9.217251|8.190758|7.164380|5.678897|5/5/5|rejected|
|btcHysteresis370_parent_L29_H300bp_E5000ppm|parent|29|0.03|0.005|14.367666|13.159565|11.951798|3.695519|6/6/6|passed|
|btcHysteresis370_parent_L29_H400bp_E5000ppm|parent|29|0.04|0.005|14.003673|12.808956|11.614561|3.684669|6/6/6|passed|
|btcHysteresis370_parent_L29_H500bp_E5000ppm|parent|29|0.05|0.005|13.929172|12.811807|11.694785|3.670038|6/6/6|passed|
|btcHysteresis370_parent_L29_H300bp_E15000ppm|parent|29|0.03|0.015|14.123123|12.914032|11.705250|3.703861|6/6/6|passed|
|btcHysteresis370_parent_L29_H400bp_E15000ppm|parent|29|0.04|0.015|13.797550|12.603238|11.409227|3.691531|6/6/6|passed|
|btcHysteresis370_parent_L29_H500bp_E15000ppm|parent|29|0.05|0.015|13.997042|12.884408|11.772130|3.670038|6/6/6|passed|

逐项失败判据：{'btcHysteresis370_BTC_L29_H300bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H400bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H500bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H300bp_E15000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H400bp_E15000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H500bp_E15000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_parent_L29_H300bp_E5000ppm': [], 'btcHysteresis370_parent_L29_H400bp_E5000ppm': [], 'btcHysteresis370_parent_L29_H500bp_E5000ppm': [], 'btcHysteresis370_parent_L29_H300bp_E15000ppm': [], 'btcHysteresis370_parent_L29_H400bp_E15000ppm': [], 'btcHysteresis370_parent_L29_H500bp_E15000ppm': []}。

原四冻结账户独立续自己的现金/实际q/成本/风险/fullNAV，不采用研究E。SMA/single Nov7_04:30→06:30只闭合mark/风险；L4/FEWM06:10→08:10须真实08资金费按自身q、实际rate/mark/ns核验，不能复制对方现金流或重复午夜，不从现金重开。各自下一日决策Nov8_00:01。SMA最后完整65日源仍R024625，当前和上一续接输入为minute数组。所有原账户partial延迟shadow，不是十策略实时报价模拟业绩或180日资格。

同main排他锁内finish和必要检查后生成只读monitor并检查；保存全部正负折、变体、完整账户账本/冻结规则/登记/必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。实际非强制push、完整远端tree/blob核验与解锁终态见.git/automation_proofs/20261107T084632Z.json。

实际三项验证：6新组合均11/12正30日折、各成本近期6/8正五日；H/E九格组合严格近期9/9，六个新组合局部严格近期率均1。三档成本下12个新配置全净正，组合三倍净收益11.409227%–11.951798%、连续OOS整体DD3.670038%–3.703861%。6新组合历史通过，6 BTC单独组件近期仅5/8、邻域严格近期率0，全部淘汰；其中4个组件正月不足9/12。保留描述性边界/cliff标记及全部负折，不将其事后用作新资格门槛。事前关注H4%/E1.5%组合三倍11.409227%、DD3.691531%，仍须独立前向。

已于2026-11-07访问[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对fundingTime毫秒、fundingRate、关联markPrice和请求时间含端点；原始代码中的exactFraction target本来就支持E参数，本轮仅传入预声明E，不改交易/成本/资金费/风险核算。费用仍为声明估计，不是盘口TCA。

原账户实际续接：SMA NAV52147→52267、累计52229分钟/36完整日，原现金/数量/desired/成本与历史交易保持，三个成本累计净收益仍−6.982980%/−7.226287%/−7.468958%。single NAV16480→16602、408ID/16229分钟，本轮无新资金费/日决策/成交。L4 NAV9217→9341、231ID/9129分钟；FEWM NAV3325→3449、87ID/3369分钟；两者各6个实际新资金费记录，原本BTC空仓数量分别−0.006/−0.009，08UTC真实rate0.00001332、mark76061.70739130、ns1794038400000000000，每成本收入分别0.006078851654712696/0.009118277482069044 USDT，收入不放大。ETH真实rate0.00004541、mark2245.05856589，因各自实际q=0推出金额0，非缺失填零。所有日事件与成交为0，不重复00/08或首笔，不复制现金流，原冻结规则与完整NAV前缀独立核验。

一次公开BTC资金费GET发生TLS EOF，失败空响应gzip、stderr、真实时间与原始回执保留，既有有界GET重试成功；所有回测和账户窗口均未重跑。此后FEWM仅复用同窗真实公共行情与provenance，独立使用自己的计划/现金/q/资金费/风险/NAV。SMA/single下一窗06:30→08:30，其中single尚未跨过08，须按自己−0.012等实际q重新推导08现金流，不能复制L4/FEWM；L4/FEWM下一窗08:10→10:10保持08后状态，不重复结算。全部下一日决策Nov8_00:01，长期计划不变；原账户partial延迟shadow，不是十策略实时报价业绩或180日资格。

匹配旧对照补充（只读事后诊断，不改资格）：6个新组合在1/2/3倍成本下的收益均低于同H、同C/N、同ETH组件的旧E1%组合。部分回撤略低，但没有一个新组合同时提高收益并降低整体回撤；因此本轮保留6个历史通过设置，未找到优于旧中心的新方案，也未启动新前向账户。全部旧资格和当前预设门槛保持。

封存：6新BTC组件＋6新组合/36成本场景，新组合通过6、淘汰0；24ID/48事件全部finish，43200旧保护文件保持。18旧原生成本路径只读，18新BTC原生成本路径/6660实际新决策及18新组合路径独立核验。
原SMA NAV52147→52267，single NAV16480→16602，L4 NAV9217→9341，FEWM NAV3325→3449。L4/FEWM实际新资金费记录6/6，各自按真实rate/mark/ns/持仓独立计算；日事件与成交均0，不重复00或复制现金流。FEWM累计3369分钟/87ID，全部账户partial、非180日资格。
只读监控9712行，原9700行完整不变，10报价账户/281观察，gzip4454195字节。行情HTTP/传输失败1次原证据保留；所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。实际push、完整远端tree/blob及解锁终态见.git/automation_proofs/20261107T084632Z.json。
