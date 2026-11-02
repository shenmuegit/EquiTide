# ETH 最大实际持仓期限验证

完整读取25500事件/12628ID和271份结论；排除持续观察后的历史研究定义数9433。初始16项均有实际证据，不重跑已完成配置。本轮6个新ETH原生与6个新父组合、36成本场景均逐项reserve成功后实际计算，所有正负期间与结果留档。

Limit time in a contrarian ETH position to reduce stale-signal price/funding exposure; earlier forced exits may add turnover or lose profitable continuations. Predeclare fastL3/4/5 x max actual holding D3days/7days/OFF. Fix H.025,E+.0025,S28alwaysgate,V10cap.045,ETH15000/N4500 andBTC3750/N375. OFF three native/three parents readonly; six limited-duration ETH policies and six parent sums are new. Expiry has close/flat priority at current daily execution, may reenter next day; actual filled-entry age carried across folds. No outcome-driven extensions or recent-gate relaxation; reused history is not independent final OOS.

预设两轴：ETH快回望L=[3,4,5]，最长实际持仓D=[3天,7天,None=不限制]。H=0.025、E=+0.0025、S28方向始终门控、V10样本logvol上限0.045固定。OFF三个ETH与三个父、BTC和匹配持有父/两原生共10唯一旧结果只读；有限期限六原生与六父为新定义。旧pairOLS720配对研究曾用48小时上限，规则、资金和市场模型不同，不能据策略族/期限概念相同排除此批；完整spec指纹逐项查重。

完整价格信号不变：ETH fastROC=C[i−1]/C[i−1−L]−1，严格>H空、<−H多；带内实际多仅ROC<E、实际空仅ROC>−E保留，等号退出。绝对slow28方向不匹配退出，V10波动>4.5%只过滤新开/翻向。之后实际非零持仓日龄>=D时强制desired=0，无论原目标同向或翻向：当前日决策先平仓并保持空仓，禁止当次重开/翻向；下一日可按原信号再入场。更早原退出/翻向照常，BTC无新期限。

日龄来自本币本成本场景最近一次成功原生开仓的UTC日索引，到当前00:01决策的整日差；原生开仓和平仓都在00:01，因此到期边界对应实际72/168小时。只在成功成交时更新开仓日期，拒单不重置；实际持仓/日龄跨walk-forward折保持。00资金费若先于00:01平仓，仍按真实持仓支付/收取，不能因即将到期免计。终止平仓照常计成本，不为研究窗口平仓冻结账户。

经济假设是限制陈旧信号的价格与资金费暴露；代价可能是更高换手和错过后续利润。3天/7天期限在结果前固定，不利用近期收益调整持仓日龄、重新选择门槛或宽限6/8近期要求。没有新资金费信号、BTC残差或慢趋势幅度过滤。

资金及原权重：BTC真实银行3750/N375旧ROC31/H4%/E1%曲线只读，ETH15000/N4500独立原生数量/冲击/抵押实际重测。总初始18750，原[1,1]直接相加两银行美元NAV，20%/80%仅初始本金份额，不再次乘权重或自动归一化；初始总名义4875=26%本金。固定N/前完整close按LOT向下取整，下一00:01原生OPEN不利tick，普通翻向先平后开，同向保留实际q。无父调仓、转账、跨抵押、复利调N或线性缩放旧路径。

按时间验证：2025-10-19UTC00:01至2026-10-24UTC00:01连续370天，12完整30日折+10日尾折；现金、数量、费用及开仓日龄跨折不重置，全分钟/事件NAV计算整体回撤。近期40天固定day330与8×5日折。无拟合/标签，purge0、预热30+间隔3，ADV和波动仅前20完整日。该历史经过大量反复开发，全部试验数留档，不称未触碰最终留出、独立未来资格或DSR/PBO显著性。

1/2/3倍成本：每边5bp费用、1bp半价差、2bp滑点及0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)冲击。所有到期平仓及下一日重开均真实付费；真实资金费按settlement/rate/mark/heldq入账，支出倍增、收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押、各银行独立1%闭合小时不利mark维护代理均核验。线性永续无现货借币，不虚构借币费；缺L2/TCA、完整历史档位与逐tick清算/容量证明。匹配本金及初始N持有和现金0%并列，非满仓或同风险持有。

固定失败门槛：每成本全年净正，1倍至少9/12正完整月；每成本近期净正且至少6/8正5日折；3倍整体DD<=25%；L/D索引半径1含中心邻域的3倍净正与严格近期支持均>=60%；至少4平仓，毛参考价格PnL加fund/执行成本>=2.5；零拒单/负抵押/小时维护代理违规，终止flat且>=180天。新原生与父独立判断，OFF原资格/报告不变，当前邻域诊断另列。D=[3,7,None]邻域采用预声明索引，不把None解释为0天。

|新配置|范围|L|期限天|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|holdcap370_ETH_L3_D3_H250_E025_V10|native|3|3|9.605802|8.043874|6.481358|5.407954|8|5/4/4|rejected|
|holdcap370_ETH_L3_D7_H250_E025_V10|native|3|7|12.008510|10.435455|8.861827|3.975470|9|5/4/4|rejected|
|holdcap370_ETH_L4_D3_H250_E025_V10|native|4|3|11.492145|9.963881|8.435612|4.162068|10|4/4/4|rejected|
|holdcap370_ETH_L4_D7_H250_E025_V10|native|4|7|13.233099|11.725876|10.218842|3.979750|10|5/5/5|rejected|
|holdcap370_ETH_L5_D3_H250_E025_V10|native|5|3|9.565782|8.079356|6.593642|4.132523|9|2/2/2|rejected|
|holdcap370_ETH_L5_D7_H250_E025_V10|native|5|7|9.907072|8.501373|7.096215|4.899742|10|3/3/3|rejected|
|holdcap370_parent_L3_D3_H250|parent|3|3|8.319521|6.977721|5.635453|4.239088|9|6/6/6|passed|
|holdcap370_parent_L3_D7_H250|parent|3|7|10.241686|8.890985|7.539829|3.305465|10|6/6/6|passed|
|holdcap370_parent_L4_D3_H250|parent|4|3|9.828595|8.513726|7.198856|3.306886|11|6/5/5|rejected|
|holdcap370_parent_L4_D7_H250|parent|4|7|11.221358|9.923322|8.625440|3.310960|11|6/6/6|rejected|
|holdcap370_parent_L5_D3_H250|parent|5|3|8.287505|7.006107|5.725281|3.400993|11|3/3/3|rejected|
|holdcap370_parent_L5_D7_H250|parent|5|7|8.560537|7.343720|6.127339|3.846302|11|4/4/4|rejected|

新父历史通过2、淘汰4。逐项失败判据{'holdcap370_ETH_L3_D3_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'holdcap370_ETH_L3_D7_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'holdcap370_ETH_L4_D3_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'holdcap370_ETH_L4_D7_H250_E025_V10': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'holdcap370_ETH_L5_D3_H250_E025_V10': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'holdcap370_ETH_L5_D7_H250_E025_V10': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'holdcap370_parent_L3_D3_H250': [], 'holdcap370_parent_L3_D7_H250': [], 'holdcap370_parent_L4_D3_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'holdcap370_parent_L4_D7_H250': ['local_recent6of8_allcost_gte60pct'], 'holdcap370_parent_L5_D3_H250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'holdcap370_parent_L5_D7_H250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。年度正收益不能代替近期、月折和邻域门槛。

同L匹配OFF三成本完整NAV全同6/12；逐成本收益/DD及来源hash见equivalent_realized_NAV_paths.json。新参数不等于独立alpha，同路径别名明确披露，不删结果或改旧资格。

11CSV保存36场景、逐月/尾折/近期折、每日NAV、两个9格完整敏感性面、72相邻边、持有/现金、旧来源与原分配。两面八指标图分别显示收益/全曲线DD/Sharpe/近期正折；Sharpe正格比例、边界峰值、描述性2std悬崖另列，不作为显著性。CSV空期限值表示OFF不限制，不是缺失结果。

合成TDD先确认旧decide接口不接受实际日龄而红灯；加入期限后验证L3/4/5×3/7/OFF、年龄2/3/6/7/8边界、多空到期、当次不翻向、下一次正常开仓、原更早退出、未来bar追加不变、非法日龄与vol边界。独立审核从保存的成功开仓成交时间戳推导entry_day，核对决策真实时间戳/日龄及过期平仓优先级，再用Fraction重算信号、Decimal重建成交、费用、资金费、小时风险及完整NAV；不调用simulate/decide/trade重新回测。

原冻结账户单独续接：SMA及singleS28从Nov2UTC00:30至02:30，Nov2零点日决策/资金费已完成，不重复。独立未过滤L4/H2从02:10至04:10，仅04:11参考闭合后采集。全部保留cash/q/desired/risk/上下文/NAV前缀，不注入本轮持仓期限，不用部分延迟shadow替代十策略真实报价模拟，未取消长期计划或新建账户。

官方一手资料实际访问2026-11-02：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。原生bars/mark/funding/约束8文件hash与边界见plan/data_manifest；API文档不证明期限策略盈利或历史网络到达时间。本轮期限假设与可得时间局限单列。

同main排他锁内逐项finish、检查、生成只读监控、提交非强制push。汇总不生成交易、不改冻结规则/本金/持仓、不部署网页或新建定时任务。不下真实订单，正回测不称稳定实盘盈利。

封存：12个新配置均逐项finish，6父历史通过2、淘汰4；6原生均未通过独立组件门槛。全部新父3倍370日净收益5.635453%至8.625440%，整体DD3.305465%至4.239088%。两个通过配置都是L3：D3为实际路径变化，D7三成本完整NAV与旧OFF完全相同。所有D7的3原生/3父共6个配置都是旧OFF实现路径别名，均如实留档，不计作独立alpha。

L3/D3组合1/2/3倍净收益8.319521%/6.977721%/5.635453%，3倍全曲线DD4.239088%，1倍9/12正月，近期每成本6/8正小折，局部严格近期支持75%。L3/D7为10.241686%/8.890985%/7.539829%，3倍DD3.305465%，10/12正月，近期每成本6/8、局部支持5/6，但它是旧不限期结果别名。D3的收益及DD在全部成本下均未优于匹配OFF，passed_candidate_evidence逐成本核实。不能称风险改进、整体全域稳健或独立未来/稳定实盘盈利。

当前全9格严格近期父5/9、原生0/9，描述性全域悬崖仍存在；不据此改写预定的局部门槛或旧资格。L4/D3未过近期及局部支持，L4/D7近期合格但局部仅5/9，L5两期限近期不足；原生组件各自失败原因已完整列出。

独立审核：19620468新完整对齐NAV点、6660决策，核算计数{'funding': 39960, 'fills': 1644, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 133797}。实际成交时间戳独立推导日龄和到期优先级，source交易按成本/现金/funding/小时风险重建，父不新增成交。research_evidence_counts分开新/旧实际资金费、成交、到期标记和真正改变目标的到期意图；不把原本也应退出的到期标记当额外成交。24865旧保护文件不变，21新ID/42条追加事件完整。无simulate/decide/trade金融重跑。

原SMA65续至2026-11-02T02:30:00Z：旧NAV44702+120=44822，累计44789分钟/31完整日，本窗0日决策/成交，完整Floatcash/q/desired/cost/trades保留。下次日决策2026-11-03T00:01:00Z，继续使用Nov2真实65日上下文，不重复零点决策。

原singleS28续2026-11-02T00:30:00Z至2026-11-02T02:30:00Z，NAV8993、累计ID222；本窗新决策0、成交0、资金费[]，小时检查9。独立L4/H2续2026-11-02T02:10:00Z至2026-11-02T04:10:00Z，04:11参考闭合后采集，NAV1730、累计1689分钟/45ID；新决策0、成交0、资金费[]、小时检查6。二者风险0违规，真实00已计资金费不重复、完整前缀/上下文保留，新持仓期限未注入；仍无180天资格。

只读监控检查通过：9004研究行、8992旧行完整字典不变，10原报价账户/219观察，gzip4075265字节，保持现有5MB预算。本轮实际HTTP/传输失败1次，所有被输出的失败尝试/原始响应/真实stderr保留；未记录的逐次响应体不补造，预期合成红灯另存。没有继承上轮元数据或提交辅助错误为本轮事实，无完成观察/金融重跑。

核验后清理22204字节可重建一次性脚本，保留原hash和复现方式；真实金融结果、完整账户账本删除0。轻量结果、必要代码、规则、原始响应和数据hash完整保存。main提交/非强制push、远端完整tree/blob及实际进程终态/解锁证明存.git/automation_proofs/20261102T035722Z.json。
