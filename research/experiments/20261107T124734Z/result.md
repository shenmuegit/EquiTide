本轮6新BTC组件＋6新组合/36成本场景实算；新组合通过6/6、淘汰0/6。已有L29/H3%的E0.5/1/1.5%三格原组件和组合只读，未重跑或改资格。

前两轮退出缓冲及H2/2.5%的新组合虽历史通过，收益仍低于同E旧H3%对照。本轮固定BTC L29/C3750/N1000，事前细化H2.75/3/3.25%×E0.5/1/1.5%，检验3%附近是否有平坦的成本后表现或局部尖峰，而不是直接沿低门槛继续扩展。已有H3%三格只读；H2.75/3.25%六新BTC组件及六新组合全部先reserve再实际核算。ETH固定C15000/N4500、L5/H2/E.005/S24/D7/K.02/V10cap.045；raw1/1完整银行不缩放、不归一化，不转账/再平衡/交叉保证金。事前关注H3.25%/E1%，全部时间、规则和失败门槛不变，所有正负结果保留；反复开发历史与大量试验不是独立最终或稳定实盘收益。

完整读取29576事件/14666ID、335既往结论。初始16项实际证据齐全，缺0；此前研究定义10165，标实际9952、未标213，不称所有登记都有结果。

BTC固定L29、C3750/N1000，H2.75/3/3.25%×退出缓冲E0.5/1/1.5%；strictH入场优先，区间内旧long在ROC>-E时持有、旧short在ROC<E时持有，等于退出边界即平仓。反手先平后开，同方向留实际数量，不日再平衡。ETH固定C15000/N4500、L5/H2%/E0.5%、finiteEWM24 beta23/25、D7/K2%、entry-only V10样本logvol上限4.5%。Raw[1,1]相加完整银行，总本金18750，20/80资本份额不重复乘、不归一化、不缩放旧NAV/数量/成本，无父订单/转账/交叉保证金。

370日连续OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折＋10日尾；近期40日继承day330现金/持仓8×5日，无折间重开。BTC需30过去完整收盘、ETH需31，源33足够；过去完整收盘发信号，下一00:01OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。报告逐折和完整OOS整体DD；重复开发历史及多重选择不能叫未触碰最终、独立未来或稳定实盘盈利。

每边5bp费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出、收入不放大；真实fundingTime/rate/mark/当时q，线性永续无现货借币。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark保证金代理核验；缺L2/TCA/完整层级/逐tick强平与真实容量证据。

H/E两轴原生和组合各9格，H3%三格只读；索引半径1含中心。保留全部变体收益/整体DD/Sharpe/Calmar、72邻接边、平台/孤峰/边界。门槛原样：全期各成本净正、1倍>=9/12正月、近期各成本净正且>=6/8正五日、3倍DD<=25%、局部三倍净正及严格近期合格率>=60%、>=4原生平仓、毛PnL+资金费/1倍成本>=2.5、零抵押/订单/风险违规、终点flat、>=180日。与同本金/名义常持有及现金0%比较，不以本轮结果改门槛。

|新配置|类别|BTC L|H|E|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|btcHysteresis370_BTC_L29_H275bp_E5000ppm|native|29|0.0275|0.005|8.446806|6.900484|5.354212|6.811608|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H325bp_E5000ppm|native|29|0.0325|0.005|10.532377|9.032025|7.531684|6.811608|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H275bp_E10000ppm|native|29|0.0275|0.01|9.375934|7.853642|6.331406|6.818098|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H325bp_E10000ppm|native|29|0.0325|0.01|11.461505|9.985183|8.508878|6.818098|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H275bp_E15000ppm|native|29|0.0275|0.015|7.224088|5.672822|4.121473|7.030198|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H325bp_E15000ppm|native|29|0.0325|0.015|9.309659|7.804363|6.298944|7.030198|5/5/5|rejected|
|btcHysteresis370_parent_L29_H275bp_E5000ppm|parent|29|0.0275|0.005|13.842953|12.626353|11.410096|3.695519|6/6/6|passed|
|btcHysteresis370_parent_L29_H325bp_E5000ppm|parent|29|0.0325|0.005|14.260067|13.052661|11.845591|3.695519|6/6/6|passed|
|btcHysteresis370_parent_L29_H275bp_E10000ppm|parent|29|0.0275|0.01|14.028778|12.816985|11.605535|3.696239|6/6/6|passed|
|btcHysteresis370_parent_L29_H325bp_E10000ppm|parent|29|0.0325|0.01|14.445892|13.243293|12.041030|3.696239|6/6/6|passed|
|btcHysteresis370_parent_L29_H275bp_E15000ppm|parent|29|0.0275|0.015|13.598409|12.380821|11.163549|3.703861|6/6/6|passed|
|btcHysteresis370_parent_L29_H325bp_E15000ppm|parent|29|0.0325|0.015|14.015523|12.807129|11.599043|3.703861|6/6/6|passed|

逐项失败判据：{'btcHysteresis370_BTC_L29_H275bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H325bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H275bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H325bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H275bp_E15000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H325bp_E15000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_parent_L29_H275bp_E5000ppm': [], 'btcHysteresis370_parent_L29_H325bp_E5000ppm': [], 'btcHysteresis370_parent_L29_H275bp_E10000ppm': [], 'btcHysteresis370_parent_L29_H325bp_E10000ppm': [], 'btcHysteresis370_parent_L29_H275bp_E15000ppm': [], 'btcHysteresis370_parent_L29_H325bp_E15000ppm': []}。

原四冻结账户独立续自己的现金/实际q/成本/风险/fullNAV，不采用研究E。SMA/single Nov7_08:30→10:30，L4/FEWM10:10→12:10，均仅闭合mark/风险，无新日决策、资金费或成交。各自08已计入，不重复00/08，未来16只在实际窗口到达时独立结算。四者不复制现金流、不从现金重开。各自下一日决策Nov8_00:01。SMA最后完整65日源仍R024625，当前和上一续接输入为minute数组。所有原账户partial延迟shadow，不是十策略实时报价模拟业绩或180日资格。

同main排他锁内finish和必要检查后生成只读monitor并检查；保存全部正负折、变体、完整账户账本/冻结规则/登记/必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。实际非强制push、完整远端tree/blob核验与解锁终态见.git/automation_proofs/20261107T124734Z.json。

实际三项验证：6新组合均11/12正30日折、各成本近期6/8正五日；H/E组合九格严格近期9/9，六个新组合局部严格近期率均1。三档成本下12个新配置均净正，组合三倍净收益11.163549%–12.041030%、连续OOS整体DD3.695519%–3.703861%。6新组合历史通过，6 BTC单独组件因6–8/12正月、5/8正近期及局部严格近期率0而全部淘汰。事前关注H3.25%/E1%组合三倍12.041030%、整体DD3.696239%，保留全部负折、边界/cliff说明和重复开发历史选择偏差，待独立前向。

已于2026-11-07本轮成功访问[Binance官方市场数据字段](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对fundingTime毫秒、fundingRate、关联markPrice及UTC时钟/含端点请求。费用、价差、滑点和冲击系数仍为声明估计，未声称真实盘口TCA或实盘容量证明。

行情采集失败与恢复：首次single采集BTC首个GET TLS失败后成功，BTC三份真实响应取得；随后ETH分钟GET连续两次TLS EOF，实际退出1，尚未生成任何spec、reserve或advance，原账户指针未变。失败目录、三份失败空响应与三份成功BTC响应、stderr及收据原样保留。恢复仅重定向新的raw子目录、复用三个已成功BTC公共响应并补采三份ETH真实响应；执行原绑定root观察器/冻结账户代码，三个新观察分别先reserve再实际advance和finish，独立audit/index退出0，完整NAV前缀保留，无完整回测或账户窗口重跑，不重复资金费。36绑定源码未修改，恢复源码与来源SHA留档。

原账户实际续接：SMA NAV52387→52507、52469分钟/36完整日，原Float现金/q/desired/交易成本保持，1/2/3倍累计收益仍−6.982980%/−7.226287%/−7.468958%。single NAV16726→16848、414ID/16469分钟；L4 NAV9463→9585、237ID/9369分钟；FEWM NAV3571→3693、93ID/3609分钟。四个原窗口新日事件、资金费和成交均0，各自08已计入账本并保持，不重复或从现金重开；下一资金费16只在后续自身实际窗口达到时按真实rate/mark/ns/q推导。下一日决策均Nov8_00:01，规则/本金/持仓不改。全部partial延迟shadow，不是十策略实时报价业绩或180日资格。

同E旧H3%对照补充（只读事后诊断，不改资格）：6个新组合在1/2/3倍成本下收益均低于同退出缓冲、同C/N和同ETH银行的旧H3%组合；本轮没有同时改善收益与整体DD的新方案。事前关注H3.25%/E1%的三倍收益12.041030%，低于旧H3%/E1%的12.147237%，整体DD均3.696239%。6新组合仍按预声明原门槛历史通过，6原生组件按原门槛淘汰，不事后更改资格。

完整净值路径只读比对：与此前15个相同BTC C3750/N1000/L29原生及15个同ETH银行/raw1/1组合定义的已保存全期三档NAV哈希、点数和相同时间边界比较，12新定义均没有三档完整路径同时匹配旧结果；该事实说明本轮保存了不同的实际路径，不代表新市场数据、数学上的策略独立性或独立最终留出。所有旧报告与状态保持。

封存：6新BTC组件＋6新组合/36成本场景，新组合通过6、淘汰0；24ID/48事件全部finish，43873旧保护文件保持。18旧原生成本路径只读，18新BTC原生成本路径/6660实际新决策及18新组合路径独立核验。
原SMA NAV52387→52507，single NAV16726→16848，L4 NAV9463→9585，FEWM NAV3571→3693。single/L4/FEWM实际新资金费记录0/0/0，按各自真实rate/mark/ns/q独立核验；日事件与成交均0，不重复00/08或复制现金流。FEWM累计3609分钟/93ID，全部账户partial、非180日资格。
只读监控9736行，原9724行完整不变，10报价账户/283观察，gzip4466934字节。行情HTTP/传输失败3次原证据保留；所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。实际push、完整远端tree/blob及解锁终态见.git/automation_proofs/20261107T124734Z.json。
