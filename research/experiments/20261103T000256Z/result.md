# ETH 快回望与慢方向窗口联合验证

完整读取26096事件/12926ID、281份既往结论；排除观察后的完整研究定义数9541。初始16条均有真实证据，本轮6个ETH原生和6组合、36成本场景先reserve再实际执行，全部失败/负收益期间保留。

上轮S24/32扰动使全部新配置失败，原S28的L3/L4在新增L/S邻域严格近期支持仅33.3%/22.2%，不能称跨慢窗口稳健。本轮只预设更窄S26/28/30与L3/4/5双轴，检查S28附近表现是否连续或属于窄峰；这是重复开发历史上的敏感性诊断，不是新的独立最终测试。固定E0.005、HL1.5%/HS2.5%、V10/cap4.5%、成本past20和BTC3750/N375、ETH15000/N4500，原[1,1]完整银行NAV相加，不归一化。S28旧实际结果只读；S26/30共6新原生和6新组合逐项reserve后才计算，逐月/近期/邻域/成本门槛不改，所有失败和负收益期间保存。首i33的33完整close足够S30，不缩短预热或引入未来。

既往完整定义9541，登记明确有实际结果9328，未标实际结果213；初始16条原档解析单列。定义数与无结果配置不能全算完成回测，重复历史存在大量选择偏差。

预设L=[3,4,5]与慢趋势S=[26,28,30]日；固定E=0.005（ROC价格收益率阈值0.5%）、HL=0.015、HS=0.025、V10/cap0.045。S28的3原生/3组合、BTC、匹配持有父与其2原生共10旧结果只读。真正改变S是新配置，名称/排序/数字格式不是。

价格规则：fastROC=C[i−1]/C[i−1−L]−1；严格r>0.025空、r<−0.015多，等号不新开。否则已有多仅r<+0.005保留、已有空仅r>−0.005保留，等号退出。慢ROC=C[i−1]/C[i−1−S]−1，其绝对正/负方向门控反转方向，等于0必须flat。最后10个完成日log收益样本std>0.045只过滤新开/翻向，等号允许；实际同向持仓不因高波动单独强平。无额外慢幅度、时限、残差或资金费信号。前完整日信号后下一UTC00:01原生OPEN执行，翻向先平后开。

数据与walk-forward：真实2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12个30日完整折与10日尾折；现金、数量和成本跨折连续，完整分钟/事件NAV计算整体回撤。最近40日继承day330状态，8个5日折单列。固定规则无拟合/标签，purge0；预热30日+3日间隔提供首决策i33的33个完整日收盘，最大S30使用index2，不截短或负索引，不引未来。成本只用前20完整日。历史反复开发，不称未触碰最终留出、独立未来或DSR/PBO显著结果。

资金与权重：BTC真实3750USDT银行/N375复用原ROC31/H4%/E1%的已执行原生曲线；ETH15000银行/N4500实际数量/LOT/OPEN/成本/抵押重算。原[1,1]为两个完整银行美元NAV相加，总本金18750；20%/80%仅初始本金份额，不再乘一次或归一化。初始名义4875为本金26%，无父调仓/转账/跨抵押/NAV复利调N/线性放缩旧净值，翻向及历史终止平仓计成本。

成本：每边手续费5bp、半价差1bp、滑点2bp，冲击0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)，逐1/2/3倍。真实资金费按结算ns/rate/mark/heldq入账，支出倍增、正收入不放大。核验LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押及独立银行1%闭合小时不利mark维护代理。线性永续无现货借币；缺实测L2/TCA、完整历史保证金档位、逐tick清算与容量证明。同期同银行/初始名义持有和现金0%对照，非等风险匹配。

固定失败判据：各成本全年净正；1倍>=9/12正完整月；各成本近期净正且>=6/8正5日折；3倍整体DD<=25%；L/S索引半径1含中心邻域3倍净正和严格近期支持均>=60%；>=4底层平仓；1倍毛参考价格PnL+funding/执行成本>=2.5；零拒单/负抵押/小时代理违规、终止flat且>=180日。新原生和组合分别判断，旧S28资格/旧邻域字段保持，当前网格诊断另列。

|新配置|范围|L|慢窗口S日|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|slow370_ETH_L3_HL150_HS250_S26_E500milliPct|native|3|26|12.393298|10.078681|7.762788|7.262028|8|4/4/4|rejected|
|slow370_ETH_L3_HL150_HS250_S30_E500milliPct|native|3|30|13.771212|11.823361|9.875362|4.841611|8|4/4/4|rejected|
|slow370_ETH_L4_HL150_HS250_S26_E500milliPct|native|4|26|10.379534|8.453662|6.527259|5.620023|8|4/4/4|rejected|
|slow370_ETH_L4_HL150_HS250_S30_E500milliPct|native|4|30|8.022217|6.360874|4.698578|6.197222|7|3/3/3|rejected|
|slow370_ETH_L5_HL150_HS250_S26_E500milliPct|native|5|26|16.141889|14.210092|12.279268|4.746717|10|1/1/1|rejected|
|slow370_ETH_L5_HL150_HS250_S30_E500milliPct|native|5|30|13.333120|11.479385|9.626276|5.684048|9|1/1/1|rejected|
|slow370_parent_L3_HL150_HS250_S26_E500milliPct|parent|3|26|10.549517|8.605566|6.660597|6.125220|9|5/5/5|rejected|
|slow370_parent_L3_HL150_HS250_S30_E500milliPct|parent|3|30|11.651849|10.001310|8.350657|3.930264|9|5/5/5|rejected|
|slow370_parent_L4_HL150_HS250_S26_E500milliPct|parent|4|26|8.938506|7.305551|5.672174|4.540468|9|5/5/5|rejected|
|slow370_parent_L4_HL150_HS250_S30_E500milliPct|parent|4|30|7.052652|5.631320|4.209229|4.967022|8|4/4/4|rejected|
|slow370_parent_L5_HL150_HS250_S26_E500milliPct|parent|5|26|13.548390|11.910695|10.273781|3.850849|11|3/2/2|rejected|
|slow370_parent_L5_HL150_HS250_S30_E500milliPct|parent|5|30|11.301375|9.726129|8.151387|4.588231|10|3/2/2|rejected|

新组合历史通过0、淘汰6；全部失败判据{'slow370_ETH_L3_HL150_HS250_S26_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_ETH_L3_HL150_HS250_S30_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_ETH_L4_HL150_HS250_S26_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_ETH_L4_HL150_HS250_S30_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_ETH_L5_HL150_HS250_S26_E500milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_ETH_L5_HL150_HS250_S30_E500milliPct': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_parent_L3_HL150_HS250_S26_E500milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_parent_L3_HL150_HS250_S30_E500milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_parent_L4_HL150_HS250_S26_E500milliPct': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_parent_L4_HL150_HS250_S30_E500milliPct': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_parent_L5_HL150_HS250_S26_E500milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'slow370_parent_L5_HL150_HS250_S30_E500milliPct': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。不以年度峰值替代近期/逐月/邻域要求。

相对同L旧S28/E0.5中心，完整NAV全同0/12；相对上一轮整个L/E网格同路径0/12。hash和每成本收益/完整DD差异逐项保存；新参数不等于独立alpha。

11CSV包含36成本场景、全部完整月/尾折/近期折、每日NAV、原生和组合九格敏感性、72相邻边以及来源/分配/匹配持有现金。图含收益/整体DD/Sharpe/近期折数，Calmar在表内。边界及2std相邻悬崖仅为描述诊断，不作显著性或结果后加门槛。

合成检查先确认旧S28接纳范围拒绝S24，再仅扩展S26/28/30接纳；Fraction价格、退出和会计公式复用。144个严格阈值/翻向/慢门控/波动/未来不变fixture，18个准确S滞后与慢ROC等号flat案例，18个旧行补S元数据/4-6-9索引邻域/原资格保持案例另存。S30最早i31有31完整close时可执行、只有30close时必须拒绝；实际首i33有33完整close可用，防负索引暖启动泄漏。独立核验不调用simulate/decide/trade重新评估。

原SMA65与singleS28从Nov2UTC20:30续22:30；独立未过滤L4/H2从Nov2_22:10续Nov3_00:10，仅00:11参考闭合后采集。Nov2_00/08/16已记不重复，新的Nov3实际午夜结算按旧持仓入账一次，然后00:01使用新完成Nov2日close/QV和past20成本按原冻结规则决策，不假定零成交。全部cash/q/desired/risk/context/NAV前缀连续，不采纳本批新S。SMA65日源继续20261102T015622Z。部分延迟shadow与十策略实时报价模拟区分，长期规则/本金/终止日期保持，不重开账户/下真实单。

一手资料2026-11-03实际访问：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。8份源年bars/mark/funding/约束文件路径、单位、边界/字节/hash见plan/data_manifest；文档不证明假设盈利、历史发布延迟或实际成本。

全部实际配置逐项finish，负收益/失败结果完整保存；同main排他锁内完成登记/来源/导出/监控检查、提交非强制push。只读监控不新回测/成交，不改冻结账户，不部署网页/增任务/下真实订单。

封存：12新配置分别finish，6组合历史通过0、淘汰6；6ETH原生通过0。三倍成本组合370日净收益范围4.209229%至10.273781%，完整曲线DD3.850849%至6.125220%。相对同L旧S28/E0.5%三成本完整NAV全同0/12，实际收益/回撤差异均保留。

扩大同L旧对照后，0个历史通过组合中，0个三成本完整NAV与已知旧格相同，0个被某个同L旧格严格支配（全部成本收益不高、DD不低且至少一项更差）。逐成本完整原始报告来源、hash与差异在passed_candidate_evidence；与S28/E0.5中心相比改善不等于超越整个已知同L的L/E旧网格，资格判据和登记状态不因此改写。

新增跨慢窗口证据：旧S28中心在本轮L/S邻域的严格近期支持为{3: 0.3333333333333333, 4: 0.2222222222222222, 5: 0.16666666666666666}，低于60%的中心表示当前邻域支持不足，达到门槛也仅代表本次更窄开发邻域；上一轮更宽S24/32扰动的失败证据不能被覆盖，先前L/E通过不代表跨慢窗口稳健。原canonical状态/旧资格不改，当前诊断单列；本轮12新定义均按原门槛独立finish，不据此重写旧报告或提前采用新规则。

全九格严格近期合格：组合2/9、原生0/9。每成本正Sharpe、最高位置/边界和描述性悬崖见sensitivity_diagnostics/edge_flags；以固定逐折、近期、邻域和成本门槛裁决，未按峰值事后扩大本批、重跑旧定义、追加资金或更换冻结账户。原中心canonical status/criteria/sensitivity与报告字节均保持。

独立审核19620468新对齐NAV点、6660决策，核算计数{'funding': 39960, 'fills': 2016, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 151479}。新原生funding19980条、实际成交1278笔；旧只读funding19980条、成交738笔。Fraction/Decimal核验实际数量、费用、成交量冲击、真实结算与小时风险，父只对齐加总，0父订单。27432旧保护文件字节不变，21新ID/42追加事件完整。

预登记前合成验证144个L/S严格退出/开仓、翻向、慢门控/波动/未来不变fixture，18个准确S滞后及慢ROC等号flat案例，另用已完成真实Nov2午夜账本核对日volume/close、6资金费和6原规则决策（只读回归，不是新观察）、18个旧行补S/4-6-9邻域fixture；S30最早i31用31完整close可执行，少于31必须拒绝；真实首i33另核验33完整close可用。本轮观察审核时间边界与全部源文件在唯一的首次正式绑定前固定，原策略退出/会计公式复用，仅扩展本批慢窗口接纳和补充准确S审计字段。正式reserve先于计算，audit成功后计数/资格、summary成功后网格/导出，无实际金融或完成观察重跑。

原SMA65从2026-11-02T20:30:00Z续至2026-11-02T22:30:00Z：旧NAV45902+120=46022，累计45989分钟/31完整日，0新日决策/成交，Float现金/数量/desired/已付成本连续。65日真实上下文引用20261102T015622Z。原singleS28从2026-11-02T20:30:00Z续至2026-11-02T22:30:00Z，NAV10217，累计9989分钟/252ID；0新决策/成交，资金费[]，小时检查6。原BTC持仓−.012与ETHflat连续，本次无新结算；00/08/16已记不重复，所有真实响应和零资金费结果均核对。

独立未过滤L4/H2从2026-11-02T22:10:00Z续至2026-11-03T00:10:00Z，仅Nov3UTC00:11参考闭合后采集；NAV2959，累计2889分钟/75ID。新日事件1、精确原规则决策6、实际成交0，新Nov3资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793664000002000000, 'base_usdt': '0.04607478000000000000000000000', 'amount_usdt': '0.04607478000000000000000000000', 'mark': '76791.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793664000002000000, 'base_usdt': '0.04607478000000000000000000000', 'amount_usdt': '0.04607478000000000000000000000', 'mark': '76791.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793664000002000000, 'base_usdt': '0.04607478000000000000000000000', 'amount_usdt': '0.04607478000000000000000000000', 'mark': '76791.30000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793664000002000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2252.80000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793664000002000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2252.80000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793664000002000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2252.80000000', 'rate': '0.00010000'}]，Nov2_00/08/16此前已计不重复，新Nov3实际结算另计一次；小时检查6，新风险违规0。原book/risk/context与NAV前缀完整，部分观察不当180日/六折资格。下一SMA/single从Nov2_22:30→Nov3_00:30等00:31闭合，届时必须按原冻结计划处理日决策及新资金费；L4下一00:10→02:10等02:11闭合，本轮已经记过的Nov3实际00结算和00:01决策不可重复。三个冻结账户不采纳本批慢窗口参数、不重开资金、不取消原终止计划。

本轮只读监控检查通过：9112研究行，9100旧完整行保持，10原报价账户/229观察，gzip4139595字节，5MB预算不变。实际观察到HTTP/传输失败1次，必要命令均实际退出0；旧稀疏慢窗口接纳范围的预期红灯独立保留。另一次私有核验脚本重复准备保护断言实际exit1，确认已有文件与预期模板原字节一致后保留，真实失败/解决记录归档；本轮无金融或完成观察重跑。原生/组合、相同路径与收益不高/DD不低且至少一项更差的对照关系分别披露。

核验后无遗留可重建缓存/检查点/编译文件，清理0真实金融结果、0完整账户账本。保留完整原始短窗响应、规则、登记、所有正负折与必要代码/hash/复现命令。main非强制push、远端完整tree/blob与真实终态/解锁凭据见.git/automation_proofs/20261103T000256Z.json。历史通过不代表独立未来或稳定实盘盈利。
