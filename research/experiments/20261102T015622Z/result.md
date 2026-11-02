# 慢趋势强度入场过滤验证

完整读取25438事件/12597ID、270份历史结论；排除持续观察后的历史研究定义数9421。初始16项实际证据齐全，无缺失回测需要重跑。本轮6新ETH原生+6新父组合、36成本场景，逐项reserve后实际计算，全部正负期间及结果保存。

Strong established slow trends may support contrarian fast pullback entries; weak-trend entries may be noise. Predeclare L3/4/5 x minimumabs(slow28ROC) T0/2.5/5percent only for freshentries/flips, fixedH.025,E+.0025,V10cap.045,ETH15000/N4500 andBTC3750/N375. T0 native/parent actualresults readonly; six positiveT ETH paths and six parent sums new. Larger threshold may miss profitable transitions and reduce sample size. No result-driven extensions or recent-gate relaxation; all history reused development, not independent final OOS.

预定两轴：快回望L=[3,4,5]与最低慢趋势幅度T=[0,0.025,0.05]。H=0.025、正退出缓冲E=0.0025、S28方向始终门控、V10样本logvol上限0.045均固定。T0三个原生与三个父、BTC及匹配持有父/两原生共10唯一旧结果只读；T2.5%/5%六原生与六父为新配置。完整spec指纹查重，不按family排除；不添加资金费预测特征或BTC残差控制。

完整信号：ETH fastROC=C[i−1]/C[i−1−L]−1，严格>H空、<−H多；带内实际多仅ROC<E、实际空仅ROC>−E保留，等号退出。绝对slow28方向始终门控，不匹配退出；V10波动>4.5%只拦新开/翻向。之后仅非零且与实际持仓方向不同的desired要求abs(slow28ROC)>=T；严格小于拦截，等号允许。同向保留不要求幅度门槛，必须退出不受新门槛阻止；被拦翻向先退出旧方向而不新开。价格全为过去完整bar，Fraction精确阈值，不做未来收益调参。

经济假设是强慢趋势中的快回撤或反弹可能比弱慢趋势更可靠，较大门槛也可能错失趋势初期、缩小成交样本。该假设由本轮提出，不来自官方API盈利承诺，不在结果后放宽近期6/8或邻域60%门槛。

真实资金：BTC独立银行3750USDT/N375的ROC31/H4%/E1%旧路径只读，ETH15000/N4500按原生数量/冲击/抵押重新计算。总初始本金18750，原权重[1,1]是两完整银行美元NAV相加；20%/80%只是本金份额，不再次乘权重或自动归一化。初始名义总4875即26%本金。固定N/前完整close按LOT向下取整，下一00:01原生OPEN不利tick，翻向先平后开、保留实际同向q、终止成本平仓；无父调仓、转账、跨抵押、NAV复利调N或线性缩放旧路径。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01连续370天；12完整30日折+10日尾折，现金/数量/费用跨折不重置，全分钟/事件NAV计算整体回撤。近期40天继承day330，8×5日折。固定规则无拟合/标签，purge0，预热30+间隔3；ADV/波动只用前20完整日。所有历史已反复开发，多重试验计数见context；不称未触碰最终留出、独立前向或DSR/PBO显著性。

1/2/3倍成本：每边5bp费用、1bp半价差、2bp滑点及0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击。实际资金费按每次真实settlement/rate/mark/heldq记账，支出倍增、正收入不放大；本轮不把funding用于入场信号。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押及各银行独立1%闭合小时不利mark维护代理均核验。线性永续无现货借币，不虚构借币费；没有L2/TCA/完整历史档位或逐tick清算/容量证明。匹配本金与初始N持有及现金0%并列，非满仓或同风险持有。

预先固定失败门槛：每成本全年净正，1倍至少9/12正完整月；每成本近期净正且至少6/8正5日折；3倍整体DD<=25%；两轴索引半径1含中心邻域的3倍净正比例与严格近期支持均>=60%；>=4平仓，毛参考价格PnL加fund/执行成本>=2.5；零拒单、负抵押、小时维护代理违规，终止flat且>=180天。原生与父分别判断，旧T0原资格和报告不改，只列当前邻域诊断。

|新配置|范围|L|T|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|trendfloor370_ETH_L3_T250bp_H250_E025_V10|native|3|0.0250|11.597980|10.333682|9.069164|4.509742|8|4/3/3|rejected|
|trendfloor370_ETH_L3_T500bp_H250_E025_V10|native|3|0.0500|11.676055|10.666013|9.655548|4.509742|8|3/2/2|rejected|
|trendfloor370_ETH_L4_T250bp_H250_E025_V10|native|4|0.0250|10.323477|9.126903|7.930845|3.757436|8|4/4/4|rejected|
|trendfloor370_ETH_L4_T500bp_H250_E025_V10|native|4|0.0500|10.929361|9.993489|9.057793|4.104029|8|3/3/3|rejected|
|trendfloor370_ETH_L5_T250bp_H250_E025_V10|native|5|0.0250|7.954829|6.866149|5.777949|4.321331|9|3/3/3|rejected|
|trendfloor370_ETH_L5_T500bp_H250_E025_V10|native|5|0.0500|8.384361|7.544006|6.704030|4.910760|8|2/2/2|rejected|
|trendfloor370_parent_L3_T250bp_H250|parent|3|0.0250|9.913263|8.809567|7.705698|3.637902|9|5/5/5|rejected|
|trendfloor370_parent_L3_T500bp_H250|parent|3|0.0500|9.975723|9.075432|8.174805|3.637902|8|5/5/5|rejected|
|trendfloor370_parent_L4_T250bp_H250|parent|4|0.0250|8.893661|7.844144|6.795042|3.015310|9|5/5/5|rejected|
|trendfloor370_parent_L4_T500bp_H250|parent|4|0.0500|9.378368|8.537412|7.696601|3.313813|8|5/5/5|rejected|
|trendfloor370_parent_L5_T250bp_H250|parent|5|0.0250|6.998742|6.035540|5.072726|3.501228|10|4/4/4|rejected|
|trendfloor370_parent_L5_T500bp_H250|parent|5|0.0500|7.342368|6.577826|5.813590|3.973044|10|4/4/4|rejected|

新父历史通过0、淘汰6。全部新配置失败判据：{'trendfloor370_ETH_L3_T250bp_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_ETH_L3_T500bp_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_ETH_L4_T250bp_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_ETH_L4_T500bp_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_ETH_L5_T250bp_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_ETH_L5_T500bp_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_parent_L3_T250bp_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_parent_L3_T500bp_H250': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_parent_L4_T250bp_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_parent_L4_T500bp_H250': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_parent_L5_T250bp_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'trendfloor370_parent_L5_T500bp_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。年度正收益不能替代近期和邻域稳定性。

新配置与匹配T0三成本完整NAV哈希全同0/12，逐成本收益/DD差异及来源见equivalent_realized_NAV_paths.json。参数新颖不等于新独立alpha，同路径不删除结果、不改旧资格。

11CSV保存36成本场景、逐月/尾折/近期折、每日NAV、原生和父完整9格敏感性、72相邻边、持有/现金、旧来源及原分配。两面八指标图显示收益、全曲线DD、Sharpe及近期正折；Sharpe正格比例、边界峰值、描述性2std悬崖单列，不作统计显著性或按结果扩展阈值。

合成TDD先证明旧规则会允许1.05%慢趋势中新多仓，而新2.5%门槛应拦截；实际先红后绿，检查多空、阈值等号、未来bar追加不变、弱趋势持仓保留、等号退出、被拦翻向和vol边界。独立Fraction重算全部新信号；Decimal账本核对真实数量、成交、费用、资金费、小时风险、全NAV/回撤及父来源对齐，不调用simulate/decide/trade重新回测。

冻结账户独立延续：原SMA65及singleS28从Nov1UTC22:30至Nov2UTC00:30，必须按原日切换规则处理00:01决策、single实际00资金费；独立未过滤L4/H2从Nov2UTC00:10至02:10，仅02:11参考闭合后采集，00资金费已记账不重复。新趋势强度门槛不注入任何冻结账户，保留全cash/q/desired/risk/上下文/NAV前缀。部分延迟shadow继续长期冻结计划，不替代十策略实时报价模拟。

官方一手资料实际访问2026-11-02：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，提供原生klines、mark、资金费和约束字段；真实8文件哈希见plan/data_manifest。官方文档不证明策略盈利或历史网络到达时间。

同main排他锁内逐项finish、登记/导出/监控检查、提交非强制push。只读监控不产生交易、不改规则/本金/持仓、不部署网页或增加定时任务。正回测不称稳定实盘盈利，未新增前向账户。

封存：12个新配置逐个finish；新父历史通过0、淘汰6，6原生组件按各自门槛独立判断。父3倍370天净收益5.072726%至8.174805%，整体DD3.015310%至3.973044%。新父近期各成本仅4或5/8正折、邻域严格近期支持0至1/3，低于6/8和60%门槛；L3/T5%和L4/T5%还少于9/12正月，不以年度正收益放宽。当前9格严格近期父2/9、原生0/9。旧T0原资格不改。

独立审核通过：19620468新完整对齐NAV点、6660决策，核算计数{'funding': 39960, 'fills': 1320, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 128208}。范围含只读旧原生与新原生，research_evidence_counts.json分列新/旧实际资金费与成交和新门槛拦截意图；父不新增成交。不调用simulate/decide/trade金融重跑。24595旧保护文件不变，21新ID/42条追加事件完整。

原SMA65续2026-11-01T22:30:00Z至2026-11-02T00:30:00Z：旧NAV44581+120闭合分钟+1日参考=44702，累计44669分钟/31完整日，2个资产日决策/6成本场景，新增虚拟成交0。原FloatSMA65/1%信号、费用和cash/q/desired/trades不变；刷新完整65日上下文，下一日决策2026-11-03T00:01:00Z，不重开本金、不跳过日切换。

原singleS28续2026-11-01T22:30:00Z至2026-11-02T00:30:00Z，原6个成本日决策逐条[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793577660000000000, 'wanted': -1, 'returns_exact': ['-32583/424148'], 'prior_complete_close': '78313.00'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793577660000000000, 'wanted': -1, 'returns_exact': ['-32583/424148'], 'prior_complete_close': '78313.00'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793577660000000000, 'wanted': -1, 'returns_exact': ['-32583/424148'], 'prior_complete_close': '78313.00'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793577660000000000, 'wanted': 0, 'returns_exact': ['17/1746', '-15048/90857'], 'prior_complete_close': '2274.27'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793577660000000000, 'wanted': 0, 'returns_exact': ['17/1746', '-15048/90857'], 'prior_complete_close': '2274.27'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793577660000000000, 'wanted': 0, 'returns_exact': ['17/1746', '-15048/90857'], 'prior_complete_close': '2274.27'}]，新增成交0、资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0.09397719681859200000000000000', 'amount_usdt': '0.09397719681859200000000000000', 'mark': '78314.33068216', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0.09397719681859200000000000000', 'amount_usdt': '0.09397719681859200000000000000', 'mark': '78314.33068216', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0.09397719681859200000000000000', 'amount_usdt': '0.09397719681859200000000000000', 'mark': '78314.33068216', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2274.27000000', 'rate': '0.00001316'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2274.27000000', 'rate': '0.00001316'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793577600005000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2274.27000000', 'rate': '0.00001316'}]，NAV8871、累计ID219；小时风险检查6且零违规，原BTC-.012尺寸独立核验，不继承L4的半尺寸现金。

独立未过滤L4/H2续2026-11-02T00:10:00Z至2026-11-02T02:10:00Z，02:11闭合参考后采集，NAV1608、累计1569分钟/42ID；本窗新增决策0、成交0、资金费[]。00实际已记资金费不重复，小时检查9、零违规。完整cash/q/risk/上下文/NAV前缀保持，新趋势门槛未注入。三份部分观察均继续长期冻结计划，未获得180天资格。

只读网页汇总通过：8992研究行、8980旧行完整字典不变，10原报价账户/218观察，gzip4067883字节，保留现有5MB预算。实际可确认HTTP/传输失败1次；环境元数据辅助读取误用系统Python的异常与改用原研究虚拟环境的成功回执留档，金融/账户/检查均按实际终态；未捕获的单独辅助子命令退出码不补造。预期TDD红灯另存，不继承上轮失败，无完成金融/观察重跑。

清理21927字节可重建脚本，原hash与复现方式保留；真实金融结果与完整账户账本删除0。所有轻量结果、必要代码、原始响应、冻结规则及数据hash保留。main提交/非强制push、远端完整tree/blob校验、真实进程终态与解锁证据存.git/automation_proofs/20261102T015622Z.json。
