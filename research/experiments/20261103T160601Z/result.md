ETH顺趋势动量×对称入场阈值的实际原生与组合验证

ETH日线顺趋势动量与S28方向确认结合，检验不同7/14/21日回看和1/2/3%对称入场阈值能否减少逆势入场；E0.5%持仓退出滞后带和V10/cap4.5%入场过滤固定。不同于原反向入场策略，必须真实新算九个ETH原生，再结合真实BTC750旧银行生成九个组合。18项全部先reserve，不在看到结果后扩网格。此前逆势S28候选慢窗交叉不足作为已知历史背景，不将新方向的同一复用历史冒充独立最终/未来验证。

完整读取26548事件/13152ID、289份既往结论；初始16有原档实际证据、缺实际结果0。此前研究定义9615，标实际9402、未标213；不将全部登记当全部回测，大量历史搜索有多重选择偏差。

事前固定L7/14/21×H1/2/3%，S28、E0.5%、V10/cap4.5%固定。strict fastROC>H做多、<-H做空；否则实际多仓仅在r>-E时保留，空仓仅在r<E时保留，退出等号平仓；新入场等号不触发，原方向须匹配慢ROC符号。仅对新增/转向持仓应用波动过滤，反手先平后开。全部依据过去完整收盘，下一UTC00:01原生OPEN，数量按前收盘/LOT计算。

九个新ETH原生：各15000本金、固定N4500；九个新组合：完整BTC3750/N750旧银行+对应ETH15000/N4500新银行，raw[1,1]、总本金18750，资金份额20/80%、初始名义入场占比4/24%。不归一化、不按净值线性缩小原生数量、不平均收益/Sharpe/DD、不跨银行调仓/转移/交叉保证金；0父订单。三项旧逆势L4/S28控制E0.375/0.5/0.625%在新网格外只读，主控制E0.375%在看新结果前固定。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30日完整折+10日尾折。逐折不重开现金/持仓，整体DD来自完整分钟/事件OOS净值。近期40日承接day330状态，8×5日。固定规则无拟合/标签、purge0、30日预热+3日间隔，终点计成本平仓。这是反复使用的开发历史，不是未触碰最终测试或独立未来验证。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)；1/2/3倍放大执行支出和资金费支出，收入不放大。真实资金费settlement ns/rate/mark/heldq；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark保证金代理。永续空头无现货借币，不虚构借币费。旧匹配持有同银行/入场N750/4500、现金0%另列。缺盘口/TCA、历史完整层级/最大量、逐tick强平及容量证明。

固定失败门槛：全年各成本正，1倍至少9/12正完整月；近期各成本总收益正且>=6/8正5日折；3倍整体DD<=25%；含中心L/H索引半径1邻域3倍正及严格近期合格比例均>=60%；至少4底层平仓，毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规，终点flat、至少180日。全部18项独立按同一门槛裁定。旧控制原canonical状态/判据/敏感性不改，不能把旧逆势节点混入新动量邻域。

|新配置|scope|L|H比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|trend370_ETH_L7_H100bp_S28_E500milliPct|native|7|0.01|-2.145854|-4.766002|-7.385450|16.291314|4|2/2/2|rejected|
|trend370_ETH_L7_H200bp_S28_E500milliPct|native|7|0.02|7.327384|5.226227|3.125422|14.880028|5|2/2/2|rejected|
|trend370_ETH_L7_H300bp_S28_E500milliPct|native|7|0.03|10.939674|9.154761|7.370178|12.436598|5|1/1/1|rejected|
|trend370_ETH_L14_H100bp_S28_E500milliPct|native|14|0.01|12.175586|9.950746|7.725636|9.567096|6|4/4/4|rejected|
|trend370_ETH_L14_H200bp_S28_E500milliPct|native|14|0.02|11.280122|9.162352|7.044288|9.899065|6|4/4/4|rejected|
|trend370_ETH_L14_H300bp_S28_E500milliPct|native|14|0.03|9.780113|8.006772|6.232871|9.958103|5|4/4/4|rejected|
|trend370_ETH_L21_H100bp_S28_E500milliPct|native|21|0.01|7.562749|5.297371|3.031938|11.896720|5|3/3/3|rejected|
|trend370_ETH_L21_H200bp_S28_E500milliPct|native|21|0.02|8.121158|6.071669|4.022420|11.540562|6|3/3/3|rejected|
|trend370_ETH_L21_H300bp_S28_E500milliPct|native|21|0.03|5.561538|3.622364|1.682894|12.238116|6|3/3/3|rejected|
|trend370_parent_BTC750_ETHL7_H100bp|parent|7|0.01|-0.588189|-2.877350|-5.165942|14.140600|4|3/3/2|rejected|
|trend370_parent_BTC750_ETHL7_H200bp|parent|7|0.02|6.990401|5.116433|3.242756|13.005319|5|4/3/2|rejected|
|trend370_parent_BTC750_ETHL7_H300bp|parent|7|0.03|9.880234|8.259261|6.638561|10.998403|5|3/3/2|rejected|
|trend370_parent_BTC750_ETHL14_H100bp|parent|14|0.01|10.868963|8.896049|6.922927|7.748046|7|5/5/3|rejected|
|trend370_parent_BTC750_ETHL14_H200bp|parent|14|0.02|10.152592|8.265334|6.377848|8.015411|7|5/5/3|rejected|
|trend370_parent_BTC750_ETHL14_H300bp|parent|14|0.03|8.952584|7.340870|5.728715|8.052714|6|5/5/3|rejected|
|trend370_parent_BTC750_ETHL21_H100bp|parent|21|0.01|7.178693|5.173349|3.167968|10.582383|6|4/4/3|rejected|
|trend370_parent_BTC750_ETHL21_H200bp|parent|21|0.02|7.625420|5.792787|3.960354|10.293290|6|4/4/3|rejected|
|trend370_parent_BTC750_ETHL21_H300bp|parent|21|0.03|5.577724|3.833343|2.088733|10.859493|6|4/4/3|rejected|

九个新组合通过0、淘汰9；九个新原生独立状态亦在表内。逐项失败{'trend370_ETH_L7_H100bp_S28_E500milliPct': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'gross_plus_funding_to_cost1_gte2_5'], 'trend370_ETH_L7_H200bp_S28_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_ETH_L7_H300bp_S28_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_ETH_L14_H100bp_S28_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_ETH_L14_H200bp_S28_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_ETH_L14_H300bp_S28_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_ETH_L21_H100bp_S28_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_ETH_L21_H200bp_S28_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_ETH_L21_H300bp_S28_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_parent_BTC750_ETHL7_H100bp': ['positive_all_costs', 'nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct', 'gross_plus_funding_to_cost1_gte2_5'], 'trend370_parent_BTC750_ETHL7_H200bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_parent_BTC750_ETHL7_H300bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_parent_BTC750_ETHL14_H100bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_parent_BTC750_ETHL14_H200bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_parent_BTC750_ETHL14_H300bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_parent_BTC750_ETHL21_H100bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_parent_BTC750_ETHL21_H200bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trend370_parent_BTC750_ETHL21_H300bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。组合对预设旧强控制全成本NAV同路径0/9；同网格净值别名组另存，不把别名当新收益路径。

11CSV含54新场景、702逐月/尾折、432近期折、20034日NAV、两个九格L/H面、9旧控制场景、72相邻边、27持有/现金比较、45新旧原生成本路径及10资金分配。图中两个九格全部N=新；正负收益/成本/Sharpe/Calmar/完整DD与逐折结果均保留。边界按真实L/H端点检查，相邻悬崖只是依赖样本描述性指标，不是DSR/PBO显著性或事后门槛。

原SMA65与single续12:30→14:30；独立原L4/H2续14:10→16:10，仅16:11参考闭合后采集。原现金/q/desired/费用/risk/context/完整NAV前缀保持，不采用新研究规则/本金或持仓、不强制截点平仓。L4新16时资金费逐项按真实时间/rate/mark/本账户heldq记一次；08/00不重复。single本轮尚未跨16，下轮必须独立取得16资金费，不能复制L4金额。SMA65日上下文源20261103T020232Z不变。延迟shadow与十策略真实报价模拟分开，partial不冒充180日/六折资格。

一手资料2026-11-03UTC重试实际访问：[Binance USD-M市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。首次网页超时保留，精确USD-M页面重试成功；COIN-M搜索结果未用于本线性USDT模型。官方字段不证明策略盈利/实时成交或容量。8行情/mark/资金费/约束文件边界/字节/SHA和新策略/旧核算实现哈希见plan与data_manifest。

全部18个spec先成功reserve三批，才计算27原生+27组合成本路径。33来源文件在首个reserve前绑定；合成检查覆盖双重加权错误、非平均DD/收益、事件轴错位、18个L/H邻域、未来close不可见、回看差异、双向动量及入场/退出等号。独立Fraction信号、Decimal真实数量/成本/资金费/小时风险及全NAV复核，完整负结果也独立finish。

仅清理本轮可重建中间件，完整账本、登记、原始短窗响应、代码/spec/结果与核验必需证据保留。同main排他锁内生成只读监控和非强制push；发布、远端完整tree/实际终态/解锁凭据见.git/automation_proofs/20261103T160601Z.json。

封存：18新定义/54成本场景分别finish，9新组合通过0、淘汰9；9新原生通过0、淘汰9。独立核验9990新信号决策、27新原生成本曲线及27新父曲线，全部新NAV29430702点，核验计数{'funding': 49950, 'fills': 2490, 'rejects': 0, 'metric_checks': 1008, 'margin_checks': 288882}。18旧原生成本曲线只读核验，其资金费/成交是旧账本记录；新原生资金费29970条、成交1794笔来自本轮实际历史模拟。0新BTC/基准/父订单。27新ID/54追加事件；29578旧保护文件不变。

九个新组合对预设旧强逆势控制全成本NAV同路径0/9。同网格别名另存；旧逆势L4/S28控制E0.375/0.5/0.625%不混入新动量L/H邻域，旧canonical状态保持，前轮慢窗交叉不足仍有效。没有因本批年度正收益而扩大参数、改门槛、修改实测账户或声称独立未来资格。

原SMA续2026-11-03T12:30:00Z至2026-11-03T14:30:00Z，NAV46863+120=46983、累计46949分钟/32完整日；single续2026-11-03T12:30:00Z至2026-11-03T14:30:00Z，NAV11200、累计276ID；L4/H2续2026-11-03T14:10:00Z至2026-11-03T16:10:00Z，仅16:11参考闭合后采集，NAV3939、累计99ID。新资金费single=[]、L4=[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0.04659858000000000000000000000', 'amount_usdt': '0.04659858000000000000000000000', 'mark': '77664.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0.04659858000000000000000000000', 'amount_usdt': '0.04659858000000000000000000000', 'mark': '77664.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0.04659858000000000000000000000', 'amount_usdt': '0.04659858000000000000000000000', 'mark': '77664.30000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2298.67000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2298.67000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2298.67000000', 'rate': '0.00010000'}]，成交single=0、L4=0，0新日决策。所有book/risk/context/NAV前缀连续；L4当前16结算一次，下轮不重复，single下轮需独立补16、按其-.012持仓计算。partial不冒充180日/六折，不采纳新研究规则。

监控通过：9192研究行、9174旧完整行不变，10报价账户/237观察，gzip4190538字节。实际HTTP/传输失败0次，初次官方网页访问失败及成功重试均保留。所有必要pipeline实际退出0。双重加权负对照exit1，正确资本/收益/DD与错位事件轴拒绝、未来价格不可见/双向动量/入退场等号/L回看及18邻域检查通过。0已完成回测或观察重跑。清理0真实结果/完整账本，无本轮可重建缓存遗留。

完整正负场景、逐折/全曲线DD、spec/代码/数据和NAV哈希、完整账本、原始短窗响应及失败事实保留。main非强制push、完整远端tree与实际终态/解锁凭据见.git/automation_proofs/20261103T160601Z.json。
