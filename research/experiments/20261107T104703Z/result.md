本轮6新BTC组件＋6新组合/36成本场景实算；新组合通过6/6、淘汰0/6。已有L29/H3%的E0.5/1/1.5%三格原组件和组合只读，未重跑或改资格。

上轮H3/4/5%×E0.5/1/1.5%的新组合虽全通过，但收益都低于旧E1%同H对照；较低H3%位于收益较好边界。本轮固定BTC L29和C3750/N1000，事前扩展H2/2.5/3%×E0.5/1/1.5%，检验更早入场能否覆盖更多趋势，同时识别弱信号、换手与成本恶化。已有H3%三格只读；H2/2.5%六新BTC组件及六新组合全部先reserve再实际核算。ETH固定旧C15000/N4500、L5/H2/E.005/S24/D7/K.02/V10cap.045，raw1/1完整银行不缩放、不归一化。事前代表H2.5%/E1%，全部规则、时间与失败门槛不变，不依当前结果改网格；重复开发历史和众多试验不是独立最终或稳定实盘收益。

完整读取29508事件/14632ID、334既往结论。初始16项实际证据齐全，缺0；此前研究定义10153，标实际9940、未标213，不称所有登记都有结果。

BTC固定L29、C3750/N1000，H2/2.5/3%×退出缓冲E0.5/1/1.5%；strictH入场优先，区间内旧long在ROC>-E时持有、旧short在ROC<E时持有，等于退出边界即平仓。反手先平后开，同方向留实际数量，不日再平衡。ETH固定C15000/N4500、L5/H2%/E0.5%、finiteEWM24 beta23/25、D7/K2%、entry-only V10样本logvol上限4.5%。Raw[1,1]相加完整银行，总本金18750，20/80资本份额不重复乘、不归一化、不缩放旧NAV/数量/成本，无父订单/转账/交叉保证金。

370日连续OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折＋10日尾；近期40日继承day330现金/持仓8×5日，无折间重开。BTC需30过去完整收盘、ETH需31，源33足够；过去完整收盘发信号，下一00:01OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0。报告逐折和完整OOS整体DD；重复开发历史及多重选择不能叫未触碰最终、独立未来或稳定实盘盈利。

每边5bp费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出、收入不放大；真实fundingTime/rate/mark/当时q，线性永续无现货借币。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark保证金代理核验；缺L2/TCA/完整层级/逐tick强平与真实容量证据。

H/E两轴原生和组合各9格，H3%三格只读；索引半径1含中心。保留全部变体收益/整体DD/Sharpe/Calmar、72邻接边、平台/孤峰/边界。门槛原样：全期各成本净正、1倍>=9/12正月、近期各成本净正且>=6/8正五日、3倍DD<=25%、局部三倍净正及严格近期合格率>=60%、>=4原生平仓、毛PnL+资金费/1倍成本>=2.5、零抵押/订单/风险违规、终点flat、>=180日。与同本金/名义常持有及现金0%比较，不以本轮结果改门槛。

|新配置|类别|BTC L|H|E|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|btcHysteresis370_BTC_L29_H200bp_E5000ppm|native|29|0.02|0.005|7.427948|5.689131|3.950297|7.319251|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H250bp_E5000ppm|native|29|0.025|0.005|8.670087|7.074103|5.478133|6.892158|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H200bp_E10000ppm|native|29|0.02|0.01|8.375577|6.702810|5.030061|7.509751|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H250bp_E10000ppm|native|29|0.025|0.01|9.599215|8.027262|6.455327|6.898711|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H200bp_E15000ppm|native|29|0.02|0.015|7.605646|5.953001|4.300207|7.111156|5/5/5|rejected|
|btcHysteresis370_BTC_L29_H250bp_E15000ppm|native|29|0.025|0.015|7.447370|5.846442|4.245394|7.006250|5/5/5|rejected|
|btcHysteresis370_parent_L29_H200bp_E5000ppm|parent|29|0.02|0.005|13.639181|12.384082|11.129313|3.695416|6/6/6|passed|
|btcHysteresis370_parent_L29_H250bp_E5000ppm|parent|29|0.025|0.005|13.887609|12.661077|11.434881|3.693922|6/6/6|passed|
|btcHysteresis370_parent_L29_H200bp_E10000ppm|parent|29|0.02|0.01|13.828707|12.586818|11.345266|3.696841|6/6/6|passed|
|btcHysteresis370_parent_L29_H250bp_E10000ppm|parent|29|0.025|0.01|14.073435|12.851709|11.630319|3.694641|6/6/6|passed|
|btcHysteresis370_parent_L29_H200bp_E15000ppm|parent|29|0.02|0.015|13.674721|12.436856|11.199295|3.704466|6/6/6|passed|
|btcHysteresis370_parent_L29_H250bp_E15000ppm|parent|29|0.025|0.015|13.643065|12.415545|11.188333|3.702257|6/6/6|passed|

逐项失败判据：{'btcHysteresis370_BTC_L29_H200bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H250bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H200bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H250bp_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H200bp_E15000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_BTC_L29_H250bp_E15000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcHysteresis370_parent_L29_H200bp_E5000ppm': [], 'btcHysteresis370_parent_L29_H250bp_E5000ppm': [], 'btcHysteresis370_parent_L29_H200bp_E10000ppm': [], 'btcHysteresis370_parent_L29_H250bp_E10000ppm': [], 'btcHysteresis370_parent_L29_H200bp_E15000ppm': [], 'btcHysteresis370_parent_L29_H250bp_E15000ppm': []}。

原四冻结账户独立续自己的现金/实际q/成本/风险/fullNAV，不采用研究E。SMA/single Nov7_06:30→08:30，single须按自己实际q、rate/mark/ns核验08资金费，SMA现货无资金费；L4/FEWM08:10→10:10只闭合mark/风险，原08已计入不能重复。四者不复制现金流、不从现金重开。各自下一日决策Nov8_00:01。SMA最后完整65日源仍R024625，当前和上一续接输入为minute数组。所有原账户partial延迟shadow，不是十策略实时报价模拟业绩或180日资格。

同main排他锁内finish和必要检查后生成只读monitor并检查；保存全部正负折、变体、完整账户账本/冻结规则/登记/必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。实际非强制push、完整远端tree/blob核验与解锁终态见.git/automation_proofs/20261107T104703Z.json。

实际三项验证：6新组合均11/12正30日折、各成本近期6/8正五日；H/E组合九格严格近期9/9，六个新组合局部严格近期率均1。三档成本下12个新配置均净正，组合三倍净收益11.129313%–11.630319%、连续OOS整体DD3.693922%–3.704466%。6新组合历史通过；6 BTC单独组件各仅5/8正近期折、6–8/12正月及局部严格近期率0，全部淘汰。事前代表H2.5%/E1%组合三倍11.630319%、DD3.694641%，仍待独立前向；保留所有负折与描述性边界/cliff，不依结果改资格。

官方文档读取情况：本轮web工具连接失败（Fatal connection failed:error sending request）已保留真实失败记录，未声称本轮实时读取成功；使用同一UTC日期先前已核验的[Binance官方字段说明](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)及原回执SHA。行情、资金费和核算均依保留的真实原始数据独立核验，费用仍是声明估计，不是盘口TCA。

工程中断及恢复：批处理外层实际退出143，最后完成L4。恢复前核验fewm/candidate/SMA当前目录、收据和预登记均不存在，且两者共享指针仍指向上一轮；保留检查与原退出证据。仅将这三个此前未启动阶段分别执行一次，均实际退出0；已完成财务报告、L4报告、36个绑定源码SHA保持，没有回测/账户窗口重跑，也未重复资金费。原SIGTERM原因未确定，不作推断。

同E旧H3%对照补充（只读事后诊断，不改资格）：6个新组合在1/2/3倍成本下收益均低于同退出缓冲、同C/N及同ETH银行的旧H3%组合；部分DD略低，但未出现同时提高收益与降低整体DD的组合。全部6新组合仍按事前原门槛历史通过，未因对照不占优而事后改为淘汰；无新增独立未来账户。全部负折、组件淘汰原因和旧资格保持。

原账户续接：SMA NAV52267→52387、累计52349分钟/36完整日，原Float现金/q/desired/交易成本保持，1/2/3倍累计收益仍−6.982980%/−7.226287%/−7.468958%。single NAV16602→16726、411ID/16349分钟，真实08资金费6条；BTC自己的q=−0.012、实际rate0.00001332、mark76061.70739130、ns1794038400000000000，每成本收入0.012157703309425392 USDT不放大，ETH真实rate0.00004541/mark2245.05856589、实际q=0推出0。不是复制L4/FEWM现金流。L4 NAV9341→9463、234ID/9249分钟；FEWM NAV3449→3571、90ID/3489分钟，两者本轮新资金费0，之前08保持且不重复。所有日决策和成交均0，完整NAV前缀/风险/各自账本核验通过。全部partial延迟shadow，不是十策略实时报价或180日资格。

封存：6新BTC组件＋6新组合/36成本场景，新组合通过6、淘汰0；24ID/48事件全部finish，43535旧保护文件保持。18旧原生成本路径只读，18新BTC原生成本路径/6660实际新决策及18新组合路径独立核验。
原SMA NAV52267→52387，single NAV16602→16726，L4 NAV9341→9463，FEWM NAV3449→3571。single/L4/FEWM实际新资金费记录6/0/0，按各自真实rate/mark/ns/q独立核验；日事件与成交均0，不重复00/08或复制现金流。FEWM累计3489分钟/90ID，全部账户partial、非180日资格。
只读监控9724行，原9712行完整不变，10报价账户/282观察，gzip4461259字节。行情HTTP/传输失败2次原证据保留；所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。实际push、完整远端tree/blob及解锁终态见.git/automation_proofs/20261107T104703Z.json。
