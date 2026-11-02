# 滞后资金费均值窗口稳健性验证

完整读取 25376 条事件、12566 个ID、269份既往结论；初始16项实际证据齐全。既往研究定义数（排除观察）9409，查重依据完整配置。新6个ETH组件+6个BTC/ETH父组合共12定义，36成本场景，先逐项reserve后计算；所有正负结果完整保留。

Predeclared N1/3/6 mean of latest eligible realized funding may reduce noise in single-settlement screening, but could blur changing funding regimes and miss profitable price paths. Fixed payment cap0; L3/4/5 x N1/3/6, H.025,E+.0025,slow28 alwaysgate,V10cap.045,ETHactual15000/N4500 andBTC3750/N375. N1 actual results readonly; N3/N6 six fresh ETH native paths and six parent sums. Historical older mean6 studies used other rules/capital; full exact specs scanned. Reused development history, no independent final test or outcome-driven extensions.

固定两轴：ETH快回望L=[3,4,5] × 资金费均值窗口N=[1,3,6]，支付率上限F=0。N1三个原生与三个父旧结果只读，BTC及匹配持有父/原生另4定义，共10旧结果重建；6个原始OFF定义只读报告指标和哈希，不重新估值。N3/N6六个组件与六个父组合为新配置。旧均值6研究还涉及其他退出、慢门或资金配置，与本轮完整规则不同；没有因为family相同排除。

价格规则：ETH快ROC=C[i−1]/C[i−1−L]−1；H=2.5%，严格>H空、<−H多，带内实际多仅ROC<0.25%、实际空仅ROC>−0.25%保留，等号退出。绝对slow28方向始终门控；当前V10样本logvol>4.5%只过滤新开/翻向。之后仅非零且与实际方向不同的desired检验 direction×最近N条已可得realized_rate的精确Fraction算术均值<=0；同向保留和必须退出不受资金费过滤阻止。N1旧政策不重算。

资金费特征：1212条原始真实结算，按settlement排序取最近完整N条；每条settlement<=当日UTC00且normalized available+3600秒<=UTC00；最新一条年龄<=16h。N3/N6较旧来源自然跨24/48小时，16h检查仅针对最新来源，不能错误裁剪旧N事件。缺N、重复结算或最新过期阻断，不降N、不补0。normalized available=settlement+1h另加1h是保守2h模型，未证明历史网络到达。00刚结算费率不能进入00信号。特征原率不随成本倍数放大，也不预测下一结算；实际现金资金费仍按未来各真实结算时刻、rate、mark和当时q逐笔记账。

资金与原始权重：BTC实际本金3750、固定名义375的ROC31/H4%/E1%完整路径只读；ETH本金15000、固定名义4500。本轮父初始本金18750，原权重[1,1]直接相加两独立银行美元NAV；20%/80%仅初始本金份额，不再次相乘或归一化。初始总名义4875即26%本金。数量=固定N/前完整close/LOT向下取整，下一UTC00:01原生OPEN不利tick，翻向先平后开、同向保留实际数量、终止计成本平仓。无父调仓、资金转移、跨抵押、复利调N或缩放旧曲线。

按时间验证：2025-10-19UTC00:01至2026-10-24UTC00:01连续370天，12完整30日折+10日尾折；现金/数量/成本跨折不重置，全曲线计算整体回撤。近期40天固定day330、8×5日折。无模型拟合/标签，purge0、预热30+间隔3；ADV及波动只用前20完整日，价格与资金费按可得时间。历史已反复开发及多重筛选，全部trial计数保留，不能称未触碰最终OOS、独立未来资格或DSR/PBO显著性。

预先固定失败门槛：每成本全年净正，1倍>=9/12正完整月；每成本近期净正且>=6/8正5日折；3倍全曲线DD<=25%；L/N索引半径1含中心邻域中3倍净正比例与严格近期支持均>=60%；>=4平仓，毛参考价格PnL加fund/执行成本>=2.5；零拒单/负抵押/小时维护代理违规，终止flat且>=180天。新原生与父分别判断，旧N1原状态/门槛/报告不改，只另列当前邻域诊断。

1/2/3倍成本：每边5bp费用、1bp半价差、2bp滑点、0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击；资金费支出倍增、正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、各银行独立1%闭合小时不利mark维护代理。线性永续无现货借币，未虚构借币费。缺L2/TCA、完整历史档位及逐tick清算/容量证明；匹配本金和初始N持有及现金0%并列，不是满仓或等风险基准。

|新配置|范围|L|均值N|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|fundmean370_ETH_L3_N3_F0_H250_E025_V10|native|3|3|11.136806|10.216977|9.296984|3.515464|6|3/3/2|rejected|
|fundmean370_ETH_L3_N6_F0_H250_E025_V10|native|3|6|10.269485|9.361149|8.452728|3.515464|6|1/1/1|rejected|
|fundmean370_ETH_L4_N3_F0_H250_E025_V10|native|4|3|14.182474|13.254325|12.326662|3.110737|9|3/3/2|rejected|
|fundmean370_ETH_L4_N6_F0_H250_E025_V10|native|4|6|12.350692|11.575829|10.801261|3.110737|8|2/2/2|rejected|
|fundmean370_ETH_L5_N3_F0_H250_E025_V10|native|5|3|10.642955|9.816523|8.990545|2.927752|8|1/1/1|rejected|
|fundmean370_ETH_L5_N6_F0_H250_E025_V10|native|5|6|11.665670|10.943327|10.221704|2.927752|8|1/1/1|rejected|
|fundmean370_parent_L3_N3_F0_H250|parent|3|3|9.544324|8.716203|7.887954|2.917992|9|5/5/5|rejected|
|fundmean370_parent_L3_N6_F0_H250|parent|3|6|8.850467|8.031541|7.212549|2.973175|10|5/5/5|rejected|
|fundmean370_parent_L4_N3_F0_H250|parent|4|3|11.980858|11.146082|10.311696|2.621926|11|5/5/5|rejected|
|fundmean370_parent_L4_N6_F0_H250|parent|4|6|10.515432|9.803285|9.091376|2.621926|11|5/5/5|rejected|
|fundmean370_parent_L5_N3_F0_H250|parent|5|3|9.149243|8.395840|7.642803|2.463924|11|3/3/3|rejected|
|fundmean370_parent_L5_N6_F0_H250|parent|5|6|9.967415|9.297283|8.627730|2.463924|11|3/3/3|rejected|

新父历史通过0、淘汰6。逐配置失败判据：{'fundmean370_ETH_L3_N3_F0_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_ETH_L3_N6_F0_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_ETH_L4_N3_F0_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_ETH_L4_N6_F0_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_ETH_L5_N3_F0_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_ETH_L5_N6_F0_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_parent_L3_N3_F0_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_parent_L3_N6_F0_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_parent_L4_N3_F0_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_parent_L4_N6_F0_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_parent_L5_N3_F0_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fundmean370_parent_L5_N6_F0_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。年度正收益不能替代近期和邻域门槛，负收益期间完整保留。

新配置完整NAV与同L/N1三成本全同0/12，与原始OFF三成本全同0/12；逐成本收益/DD差值与匹配来源见equivalent_realized_NAV_paths.json。参数新颖不等于独立alpha，不删除别名结果或改旧资格。

11份CSV包括所有36成本场景、逐月/尾折/近期折、每日NAV、两张9格敏感性面、72相邻边、匹配持有与现金、旧来源和原分配。两面八指标图同时显示收益/DD/Sharpe/近期折；完整Sharpe正比例、最大值边界及描述性2std悬崖单列，不作为显著性。未按结果增加阈值或重测变体。

合成TDD先确认旧N1实现错误拦截最近三次均值为负但最近一次为正的新多仓，再实现最小均值扩展；实际检查N1/3/6、完整窗口、最新年龄、未来扰动、available+1h等号与+1ns、0均值等号、同向保留/等号退出/翻向及vol边界。独立Fraction审核从历史重新选N来源并算均值/信号；Decimal账本重建费用、数量、冲击、funding、小时风险及完整NAV，不调用simulate/decide/trade重新回测。

原SMA与singleS28本轮续UTC20:30至22:30；独立未过滤L4/H2续22:10至次日00:10，仅00:11参考分钟闭合后采集。L4必须处理真实00资金费和00:01原冻结日决策；只适配只读审核的跨日窗口，冻结执行器/计划不改。新均值过滤不注入旧账户。完整cash/q/risk/上下文/NAV前缀保持，部分延迟shadow不替代十策略真实报价模拟，也不取消原长期冻结计划。

一手来源实际访问2026-11-02：[Binance官方资金费历史API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。文档支持真实率/结算/mark字段，不证明历史网络发布时间或策略盈利；primary_sources.json与funding_data_availability.json分别记录假设和真实输入哈希。

同main排他锁内逐项finish、检查、只读监控汇总、提交与非强制push。汇总不生成模拟成交，不改冻结规则/本金/持仓，不部署网页或创建任务，不下真实订单。正回测不是稳定实盘盈利；未新增前向账户。

封存：12个实际新配置逐个finish，父候选历史通过0、淘汰6；6原生组件亦按各自门槛判断。父3倍370日净收益7.212549%至10.311696%，整体DD2.463924%至2.973175%。6父均未达到近期6/8正折及局部严格近期支持60%，没有按年度正收益放宽门槛。当前9格严格近期父2/9、原生0/9；旧N1资格不改，当前窗口轴未证明稳健。

独立审核：19620468新完整对齐NAV点、6660决策，核算计数{'funding': 39960, 'fills': 1056, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 119004}。计数包含只读旧原生与新原生，research_evidence_counts.json分列新/旧资金费与成交。父引用同源交易，不另计成交；未调用simulate/decide/trade金融重跑。24327个旧保护文件字节未变，21新ID/42条追加事件完整。

原SMA65续至2026-11-01T22:30:00Z：旧NAV44461+120=44581，累计44549分钟，本窗0日决策/成交。原singleS28续2026-11-01T20:30:00Z至2026-11-01T22:30:00Z，NAV8744、累计ID216；新funding[]，新决策0、成交0、小时风险检查6。

独立未过滤L4/H2续2026-11-01T22:10:00Z至2026-11-02T00:10:00Z，闭合参考后采集，NAV1486、累计1449分钟/39ID。本窗原冻结日决策6、成交0，独立验证逐条[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793577660000000000, 'wanted': -1, 'returns_exact': ['-32583/424148'], 'prior_complete_close': '78313.00'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793577660000000000, 'wanted': -1, 'returns_exact': ['-32583/424148'], 'prior_complete_close': '78313.00'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793577660000000000, 'wanted': -1, 'returns_exact': ['-32583/424148'], 'prior_complete_close': '78313.00'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793577660000000000, 'wanted': 0, 'returns_exact': ['-196/5485', '-15048/90857'], 'prior_complete_close': '2274.27'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793577660000000000, 'wanted': 0, 'returns_exact': ['-196/5485', '-15048/90857'], 'prior_complete_close': '2274.27'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793577660000000000, 'wanted': 0, 'returns_exact': ['-196/5485', '-15048/90857'], 'prior_complete_close': '2274.27'}]；资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0.04698859840929600000000000000', 'amount_usdt': '0.04698859840929600000000000000', 'mark': '78314.33068216', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0.04698859840929600000000000000', 'amount_usdt': '0.04698859840929600000000000000', 'mark': '78314.33068216', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0.04698859840929600000000000000', 'amount_usdt': '0.04698859840929600000000000000', 'mark': '78314.33068216', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2274.27000000', 'rate': '0.00001316'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2274.27000000', 'rate': '0.00001316'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2274.27000000', 'rate': '0.00001316'}]。正时长小时检查6、0风险违规。实际00资金费与00:01日决策只处理一次；不重记旧16资金费，完整上下文/cash/q/risk/NAV前缀保持，新均值筛选未注入。三份部分观察继续原长期计划，未获得180日资格。

网页只读汇总检查通过：8980研究行、8968旧行完整字典不变，10原报价账户/217观察，gzip4061008字节，5MB现有预算未改。实际可确认HTTP/传输失败0次，候选/L4响应及SMA真实stderr均留档；未被原传输器输出的失败响应体不补造。预期TDD红灯与本轮真实失败回执独立保留，不继承上轮失败，无完成金融/观察重跑。

核验后清理25421字节可重建中间文件，原哈希与复现方式保留；真实金融结果及账户账本删除0。全部轻量证据、必要代码、原始响应、规则与数据哈希保留；main提交/非强制push、完整远端tree核验、进程实际终态和解锁证据存.git/automation_proofs/20261101T235656Z.json。
