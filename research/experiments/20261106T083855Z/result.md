本轮8新BTC组件＋8新组合/48成本场景实算；新组合通过5/8、淘汰3/8。原31日/4%组件及组合只读，未重跑或改资格。

先前多次只改变BTC名义预算未解决近期一致性。本轮固定BTC1000/3750与ETH4500/15000，事前测试BTC回看27/29/31日×严格入场3/4/5%，退出E1%不变；较短响应可能改善反转也可能提高换手/成本。ETH固定D7/K2%、L5/S24/E.005/entry-only/V10cap.045。已有31/4%原组件和组合只读；8新BTC组件与8新父组合先reserve再实际计算。代表点29/4%事先固定；原门槛与原权重1/1不变，不根据当前结果扩展。全部正负结果留存，重复开发历史不能称独立最终或实盘收益。

完整读取28630事件/14193ID、321既往结论。初始16项均有实际证据（11正式恢复、5原ZIP/WF legacy），缺0，不改缺失字段。此前研究定义10000，标实际9787，未标213；不称全部登记都有回测。

BTC3750银行/N1000，L27/29/31×H3/4/5%，E1%固定；ETH15000/N4500固定L5/H2%/E0.5%、有限归一化EWM24 beta23/25、D7/K2%、仅新开/反手慢趋势与V10样本logvol上限4.5%。raw[1,1]相加完整银行，总本金18750，20/80%资本份额不重复乘；BTC名义占自身26.666667%/总5.333333%，ETH占自身30%/总24%。8新BTC按真实价格/旧核算实际生成信号、LOT、数量、费用/价差/滑点/冲击、资金费和风险，不缩放旧NAV。父组合不下额外订单/再平衡/转移/交叉保证金。

370日连续验证2025-10-19UTC00:01至2026-10-24UTC00:01，12×30日完整折＋10日尾折；近期40日继承day330原状态，8×5日，无重开。过去完整收盘形成信号，下一00:01原生OPEN执行，反手先平后开，同向保留实际数量，终点计成本平仓。源上下文33日足够最大32过去收盘；固定规则无拟合/标签，purge/embargo0。原31/4%网格边界行保持原canonical资格，只做当前邻域诊断。完整分钟/事件NAV整体回撤不平均组件统计；反复使用历史及多重选择不是独立最终或未来验证。

成本每边5bp费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本及资金费支出，收入不放大；真实结算ns/rate/mark/当时q，资金费仅事后核算。线性永续不用现货借币，不捏造借费；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark保证金代理均审核。缺历史L2/TCA/完整层级/逐tick强平与真实容量证据。

BTC L/H两轴原生与组合各9格，邻域索引半径1含中心。全部变体收益、整体DD、Sharpe、Calmar、72邻接边、平台/孤峰/最高Sharpe边界均留存；边界不触发本轮事后扩网格。失败门槛沿用：各成本全期/近期净正、1倍至少9/12正月、各成本近期至少6/8正5日、3倍DD<=25%、邻域3倍正收益及全成本近期合格率>=60%、>=4平仓、1倍毛PnL+资金费/执行成本>=2.5、0余额/订单/保证金代理违规、终点flat、>=180日。与匹配同本金/名义持有及现金0%比较。

|新配置|类别|BTC L|H|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---|---|
|btcreaction370_BTC_N1000_L27_H300bp|native|27|0.03|0.235912|-1.195317|-2.626459|11.160945|4/4/4|rejected|
|btcreaction370_BTC_N1000_L27_H400bp|native|27|0.04|3.030432|1.687813|0.345245|10.187324|4/4/4|rejected|
|btcreaction370_BTC_N1000_L27_H500bp|native|27|0.05|1.847861|0.679997|-0.487721|10.001069|3/3/3|rejected|
|btcreaction370_BTC_N1000_L29_H300bp|native|29|0.03|11.999504|10.519700|9.039913|6.818098|5/5/5|rejected|
|btcreaction370_BTC_N1000_L29_H400bp|native|29|0.04|10.179537|8.766659|7.353731|6.853653|5/5/5|rejected|
|btcreaction370_BTC_N1000_L29_H500bp|native|29|0.05|9.755286|8.743441|7.731685|5.649143|5/5/5|rejected|
|btcreaction370_BTC_N1000_L31_H300bp|native|31|0.03|3.010433|1.452903|-0.104613|8.691061|4/4/4|rejected|
|btcreaction370_BTC_N1000_L31_H500bp|native|31|0.05|8.165996|7.037788|5.909566|6.145878|4/4/4|rejected|
|btcreaction370_parent_L27_H300bp|parent|27|0.03|12.200774|11.007193|9.813962|3.691071|5/5/5|rejected|
|btcreaction370_parent_L27_H400bp|parent|27|0.04|12.759678|11.583819|10.408303|3.690810|5/5/5|rejected|
|btcreaction370_parent_L27_H500bp|parent|27|0.05|12.523164|11.382256|10.241710|3.684499|4/4/4|rejected|
|btcreaction370_parent_L29_H300bp|parent|29|0.03|14.553492|13.350196|12.147237|3.696239|6/6/6|passed|
|btcreaction370_parent_L29_H400bp|parent|29|0.04|14.189499|12.999588|11.810000|3.685387|6/6/6|passed|
|btcreaction370_parent_L29_H500bp|parent|29|0.05|14.104649|12.994945|11.885591|3.670038|6/6/6|passed|
|btcreaction370_parent_L31_H300bp|parent|31|0.03|12.755678|11.536837|10.318331|3.698077|6/6/6|passed|
|btcreaction370_parent_L31_H500bp|parent|31|0.05|13.786791|12.653814|11.521167|3.691490|6/6/6|passed|

实际失败项：{'btcreaction370_BTC_N1000_L27_H300bp': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'gross_plus_funding_to_cost1_gte2_5'], 'btcreaction370_BTC_N1000_L27_H400bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L27_H500bp': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L29_H300bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L29_H400bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L29_H500bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L31_H300bp': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_BTC_N1000_L31_H500bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L27_H300bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L27_H400bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L27_H500bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'btcreaction370_parent_L29_H300bp': [], 'btcreaction370_parent_L29_H400bp': [], 'btcreaction370_parent_L29_H500bp': [], 'btcreaction370_parent_L31_H300bp': [], 'btcreaction370_parent_L31_H500bp': []}。

四个原冻结账户分别续自己的现金/实际q/成本/风险/fullNAV，不采用研究L/H。SMA/single Nov6_04:30→06:30；L4/FEWM06:10→08:10，其中08资金费须以实际API响应及各自结算前q核验，ETH实际q=0时金额0也是原始rate/mark推导，不以缺数据补零，不重复00。当前与上一轮SMA为分钟数组，完整65日现货上下文仍20261106T023552Z/forward_inputs.json.gz；保留原Float/SMA65±1%及10bp成本。FEWM仍D1/K.0005、BTC750/ETH4500；所有为未成熟延迟shadow，非180日/六折或十策略实时报价模拟业绩。

同main排他锁内登记/必要检查后只读生成monitor，不回测监控、不造新成交或改冻结规则/本金/持仓；不重新部署或建定时任务。全部正负/淘汰结果、完整账本/登记/输入/必要代码保留，仅清理可重建中间物。实际非强制push、远端完整tree/blob及解锁终态在.git/automation_proofs/20261106T083855Z.json。

本轮5个新组合历史通过：L29/H3%、4%、5%，以及L31/H3%、5%；各自1/2/3倍成本近期均6/8正5日。L27三格仅4–5/8，严格近期邻域合格率50%，仍淘汰。8个BTC组件独立均淘汰；组合资格来自完整组合净值，不代表组件单独合格。事前代表L29/H4%的1/2/3倍净收益14.189499%/12.999588%/11.810000%，3倍整体DD3.685387%，1倍11/12正月，严格近期邻域合格率2/3；相对旧L31/H4%，3倍收益+0.403603个百分点、DD−0.014113个百分点，近期正折数仍6/8。保留边界/cliff、旧中心资格及全部负折，不以本历史择优结果冒充独立未来；原四账户不采用新规则，未创建新的前向账户。

封存：8新BTC组件＋8新组合/48成本场景，新组合通过5、淘汰3；28ID/56事件全部finish，39283旧保护文件保持。12旧原生成本路径只读，24新BTC原生成本路径/8880实际新决策及24新组合路径独立核验。
原SMA NAV50706→50826，single NAV15007→15129，L4 NAV7744→7868，FEWM NAV1852→1976。L4/FEWM实际新资金费记录6/6，各自按真实rate/mark/ns/持仓独立计算；日事件与成交均0，不重复00或复制现金流。FEWM累计1929分钟/51ID，全部账户partial、非180日资格。
只读监控9575行，原9559行完整不变，10报价账户/269观察，gzip4377897字节。行情HTTP/传输失败1次原证据保留；所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。实际push、完整远端tree/blob及解锁终态见.git/automation_proofs/20261106T083855Z.json。
