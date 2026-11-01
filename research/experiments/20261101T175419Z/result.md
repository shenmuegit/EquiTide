# ETH连续入场确认联合验证

完整读取25190登记事件/12473ID、266份既往结论，初始16项实际结果证据齐全。本轮固定L3/4/5×K1/2/3，K1的3个原生及3个父格点、匹配持有父和来源共10个旧定义只读。K2/K3新增6个ETH原生与6个BTC/ETH父定义；12配置36成本场景均先reserve再计算并独立finish，所有负收益及失败保留。

Predeclared causal entry confirmation K1/2/3 crossed with fast L3/4/5, fixed S28/H.025/E.0025/V10cap.045 and actual BTC3750/N375+ETH15000/N4500. Multi-day confirmation may reject transient extremes and reduce turnover; it may also miss profitable early reversals. K1 cells readonly, K2/K3 fresh. All outcomes retained, no later refinement. This is reused development history selected after prior weak slow-gate results, not untouched final OOS.

经济假设：连续多个已完成日的同向ROC极值可减少瞬时反转噪声与换手，也可能错过反转早段。只测这一预定机制与快周期敏感性；历史SMA或排名确认实验的不同完整配置不能替代本次真实结果。

BTC unchanged ROC31/H.04/E.01. ETH fastROC=C[i-1]/C[i-1-L]-1, L3/4/5; slow fixed S28 ROC=C[i-1]/C[i-29]-1. Strict fast>.025 short, fast<-.025 long. Inside bands actual long retained only fast<.0025, actual short only fast>-.0025, equality exits. Current slow direction always gates. Fresh entry/flip requires K consecutive completed daily fastROC extremes of same contrarian direction, K1/2/3, offsets d=0..K-1, C[i-1-d]/C[i-1-d-L]-1. Prior slow or vol has no confirmation requirement; current V10 sample logvol<=.045 also gates fresh entry/flip. Never suppress mandatory exits or retained same-direction actual q. No hidden counter or future close.

BTCactual3750bank/N375 andETHactual15000bank/N4500,rawchildweights[1,1]unchanged,total18750,capitalshares20/80percent. Onebankperasset,no sameassetclones,NAVresize,cashtransfer,crossmargin orrenormalization. ParentNAVdollarsum,notweightedagainbycapitalshare.

Priorclosedfullbars only,q=floor(fixedN/priorcompleteclose/LOT)*LOT,nextUTC00:01nativeOPENadversetick,reverseclosebeforeopen,retainsameactualq. Continuous370d,terminalcostedclose,no foldresets. Parentsownactualbankswithoutparentrebalance/fills.

5bpfee+1bphalfspread+2bpslippage+0.5*past20samplelogvol*sqrt(actualq*OPEN/past20completequoteADV),1/2/3xstress. Realfundingsettlementns/mark/rate/heldq,outflowsstressed,inflowsunchanged. LOT/tick/minnotional,participation<=.001,postfee1xentrycap,independent1percentclosedhouradversemarkmaintenanceproxy. Linearperpetualshortno spotborrow;noinventedborrowfee,TCA/L2,historicalmaxqty/tier,tickliquidation orcapacityproof.

真实数据边界2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12完整30日折加10日尾段；不按折重开账户，近期40日继承day330现金/数量/成本，8个5日折。固定规则没有训练标签，purge0，30日预热加3日间隔；所有确认日和过去20日成本统计来自当时已完成数据。此历史已反复用于选择，不能称未触碰最终测试或独立未来证据；登记试验数见context，多重选择偏差未由局部比例消除，未声称DSR/PBO统计显著性。

失败判据沿用：每档全年净正、1倍>=9/12正完整月；每档近期净正且>=6/8正5日折；3倍全曲线DD<=25%；L/K索引半径1含中心的局部3倍净正、严格近期比例均>=60%；至少4次平仓、毛参考PnL加fund/执行成本>=2.5；零拒单/负抵押/维护代理违规、终止flat、至少180日。单币与父组合分别判断；旧canonical状态、原敏感性与报告字节均不重写，当前邻域仅另作诊断。

成本模型包含5bp费用、1bp半价差、2bp滑点、按实际成交q/过去20日quoteADV和logvol的平方根冲击；1/2/3倍费用与负资金费压力，真实funding结算时刻/rate/mark/当时q，正收入不放大。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押、独立银行1%闭合小时不利mark维护代理。线性永续没有现货借币；不虚构借币费、历史完整档位、TCA/L2/逐tick清算或容量证明。匹配持有与现金0%为对照，匹配持有仅同资金/初始N，并非满仓或同风险配置。

|新配置|范围|L|K|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|confirmgate370_ETH_L3_K2_H250_E025_V10|native|3|2|9.166102|8.324718|7.483074|3.546846|9|1/1/0|rejected|
|confirmgate370_ETH_L3_K3_H250_E025_V10|native|3|3|6.081355|5.626317|5.171228|2.784629|5|0/0/0|rejected|
|confirmgate370_ETH_L4_K2_H250_E025_V10|native|4|2|11.096784|10.371661|9.646843|2.952176|8|2/2/1|rejected|
|confirmgate370_ETH_L4_K3_H250_E025_V10|native|4|3|4.244380|3.784908|3.325903|3.220925|3|0/0/0|rejected|
|confirmgate370_ETH_L5_K2_H250_E025_V10|native|5|2|11.721785|10.742223|9.763082|3.190165|8|1/1/1|rejected|
|confirmgate370_ETH_L5_K3_H250_E025_V10|native|5|3|3.429196|2.978648|2.528786|2.499383|6|0/0/0|rejected|
|confirmgate370_parent_L3_K2_H250|parent|3|2|7.967760|7.202396|6.436826|2.970988|11|4/4/4|rejected|
|confirmgate370_parent_L3_K3_H250|parent|3|3|5.499962|5.043675|4.587349|2.351320|9|4/4/4|rejected|
|confirmgate370_parent_L4_K2_H250|parent|4|2|9.512306|8.839950|8.167841|2.482676|10|4/4/4|rejected|
|confirmgate370_parent_L4_K3_H250|parent|4|3|4.030383|3.570548|3.111089|2.683701|9|4/4/4|rejected|
|confirmgate370_parent_L5_K2_H250|parent|5|2|10.012307|9.136400|8.260833|2.411446|11|3/3/3|rejected|
|confirmgate370_parent_L5_K3_H250|parent|5|3|3.378236|2.925540|2.473395|2.154806|9|3/3/3|rejected|

6个新父候选：0历史通过、6淘汰。全部新配置失败原因：{'confirmgate370_ETH_L3_K2_H250_E025_V10': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_ETH_L3_K3_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_ETH_L4_K2_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_ETH_L4_K3_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_ETH_L5_K2_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_ETH_L5_K3_H250_E025_V10': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_parent_L3_K2_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_parent_L3_K3_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_parent_L4_K2_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_parent_L4_K3_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_parent_L5_K2_H250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'confirmgate370_parent_L5_K3_H250': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。不根据新结果放宽门槛或加测格点。

11个CSV保留全部成本场景、逐折/近期折、每日NAV、原生和父完整九格敏感性、72相邻边、匹配持有和现金比较、旧来源路径与固定资金分配。完整NAV哈希、必要逐笔/资金费/状态段/父来源哈希支持独立重建。两张多指标曲面及描述性相邻2std悬崖检查不等于统计显著性；最大值在边界时如实指出，不自动追加试验。

冻结账户分别延续原现金/q/desired/risk与完整NAV前缀：原SMA65和singleS28计划续14:30至16:30，需实际处理singleS28的16资金费；独立未过滤L4/H2续16:10至18:10，仅18:11参考闭合后采集，carry已计16funding并核验正时长风险段。此次确认/缓冲/过滤参数不注入任何原账户。部分观察rejected不取消长期计划，延迟shadow不充当十策略真实报价成交。

源码合成检查采用TDD：旧代码在单日极值K2测试预期失败，新规则加入后确认/等号/退出/保留/翻向/未来扰动通过。此为预登记前合成工程证据，没有真实回测或账户重跑。

一手数据接口说明已于2026-11-01访问：[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，字段与路由记录见primary_sources.json；实际数据与哈希独立核验，文档样例不作行情证据。

所有研究/登记/快照/提交在main排他锁内；快照只读取既有账户与报告，不产生成交或改冻结规则/本金/持仓，不部署网页或增加定时任务，不下真实订单。

资金与权重：BTC实际本金3750USDT、固定入场名义375，ETH本金15000、固定名义4500；原权重[1,1]代表两份完整独立银行，总本金18750。20%/80%只是资金份额，不再次乘权重；初始名义预算合计4875即26%本金。按同一真实时间轴美元净值相加，不归一化、不线性缩放旧净值、不设父调仓、资金转移或跨账户抵押。

封存：12个新配置已逐一finish，其中新父历史通过0，淘汰6。新父3倍370日净收益2.473395%至8.260833%，整体DD2.154806%至2.970988%。实际逐配置失败原因见上表及report；全年正收益不能替代近期和邻域门槛。当前严格近期父2/9、原生0/9；旧K1原资格保留，不称当前全域稳健。

独立审计通过：19620468完整新NAV点、6660决策；核算计数{'funding': 39960, 'fills': 1074, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 115530}。计数范围包含只读旧来源及新原生；research_evidence_counts.json另行分开：新原生19980资金费/456成交，旧来源19980资金费/618成交，父只引用同源交易不新增成交。不调用simulate/decide/trade做金融重跑。23531个旧保护文件字节相同，21新ID/42条追加事件完整。

原SMA65续至2026-11-01T16:30:00Z：44101旧NAV+120=44221，累计44189分钟；无新日决策/成交。原singleS28续2026-11-01T14:30:00Z至2026-11-01T16:30:00Z，NAV8378，累计观察ID207；本窗真实funding[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793548800000000000, 'base_usdt': '0.09354111372174000000000000000', 'amount_usdt': '0.09354111372174000000000000000', 'mark': '77950.92810145', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793548800000000000, 'base_usdt': '0.09354111372174000000000000000', 'amount_usdt': '0.09354111372174000000000000000', 'mark': '77950.92810145', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793548800000000000, 'base_usdt': '0.09354111372174000000000000000', 'amount_usdt': '0.09354111372174000000000000000', 'mark': '77950.92810145', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793548800000000000, 'base_usdt': '-0E-16', 'amount_usdt': '-0E-16', 'mark': '2265.78263566', 'rate': '-0.00001034'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793548800000000000, 'base_usdt': '-0E-16', 'amount_usdt': '-0E-16', 'mark': '2265.78263566', 'rate': '-0.00001034'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793548800000000000, 'base_usdt': '-0E-16', 'amount_usdt': '-0E-16', 'mark': '2265.78263566', 'rate': '-0.00001034'}]，6正时长小时风险检查、零违规。

独立未过滤L4/H2续2026-11-01T16:10:00Z至2026-11-01T18:10:00Z，仅参考分钟闭合后采集；NAV1115，累计1089分钟/30ID。本窗funding[]、6正时长风险检查、零违规；16资金费现金不重复，完整原cash/q/desired/risk/NAV前缀保持，研究确认不注入原账户。三份部分观察均继续长期冻结计划。

监控只读汇总通过：8944研究行，8932旧行完整字典相同，10固定报价账户/214既有观察；gzip4040595字节，现有5MB预算保持。可确认HTTP/传输失败1次，候选/L4逐次原始响应与SMA真实stderr均保留；SMA内部curl重试未逐次记录失败响应体，不虚构精确尝试数。预期TDD红灯、rg不可用及可选pyarrow元数据探测失败回执保留；改用已安装分发包元数据读取，无依赖安装及金融/完成观察重跑。

清理22027字节可重建语义查重材料，原哈希和复现命令留档；金融结果/完整账户账本删除0。全部轻量证据、必要代码、状态、真实响应及数据哈希保留。main提交/非强制push及完整远端核验、真实进程终态和解锁证明在.git/automation_proofs/20261101T175419Z.json。
