本轮8个新候选组合通过5/8，1个新BTC1250动量组件通过0/1。另2个新持有组件/组合仅作基准，rejected是非候选身份，正负结果全部保留。实际新增11金融配置/33成本场景。连续370日walk-forward、N/K敏感性和1/2/3倍成本验证完成。新组合3倍净收益8.606332%～9.673513%，连续整体DD3.540488%～4.596417%。本批是受上轮启发的复用开发历史，任何通过都只代表当前历史判据，不能称独立最终/未来或稳定实盘盈利。

上轮BTCN1000/ETHD1只有单点自身近期达6/8，宽N/D邻域最高25%未过。本轮事前固定D1，把BTC实际金额750/1000/1250与ETH最小斜率门槛K0.025/0.05/0.075%联合，检验相邻金额和相邻门槛能否构成平台。只复用已有BTC750/1000、ETH三条D1实际路径；新BTC1250原生核算，同金额持有匹配。旧N1000/K0.05%中心不重复计算或修改旧裁定，新邻域诊断与旧canonical资格分开。本轮继续使用开发历史，已经受上轮观察启发，不能称独立最终/未来验证，不在本轮结果后扩网格/松门槛。

完整读取27470事件/13613ID、302既往结论，另读三技能/README/OOS检查及原freqtradeZIP。初始16项都有实际证据、缺结果0。此前研究定义9829、标实际9616、未标213；不把全部登记当回测，承认多重选择偏差。

预先固定D1，BTC实际入场N750/1000/1250 × ETH最小斜率K0.025/0.05/0.075%。BTC原ROC31/H4%/E1%不变；ETH复用有限EWM S24、D1、快L5/H2%/E0.5%、仅新开仓/反手检查趋势门槛、V10/cap4.5%的三条实际净值。旧BTC750/1000、旧N1000/K0.05%中心与旧持有基准只读；只新算BTC1250动量和持有、8个新策略父组合、1个新持有父组合。引擎整个文件与上轮字节一致。

两个实际银行BTC3750+ETH15000、总18750，raw[1,1]加完整银行，不归一化或再乘20/80%资本份额。BTC名义预算占总资金4/5.333333/6.666667%，占自身银行20/26.666667/33.333333%；ETH4500占总资金24%。数量用过去完整收盘做LOT取整，下一UTC00:01原生OPEN，反手先平后开，同向保留实际数量、终点计成本平仓。无NAV/数量/成本缩放、克隆、父订单、转移、调仓或交叉保证金。

完整九格包含8新+1旧中心；BTC金额源三格包含1新+2旧；持有父组合三档包含1新+2旧。旧中心原criteria/status/sensitivity原样保留，新邻域诊断另命名；不把旧中心计作本轮新通过，也不重复reserve/evaluate/finish旧定义。11新ID全部8+3预留成功才估值。15旧实际结果/9原生/27成本路径只读。每个N都有同本金/同预算BTC+ETH持有与现金0%对比。

时间2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30完整折+10日尾折；近期40日继承day330实际状态、8×5日，不按折重开。上下文33日、BTC最多32日，ETHD1窗口最多25日。无拟合/标签、purge0；固定规则、金额未在测试期间拟合。已反复使用历史不是未触碰最终留出，整体DD从完整分钟/事件净值算，不平均单腿Sharpe/回撤。

成本5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)。1/2/3倍执行和资金费支出、收入不放大；实际结算ns/rate/mark/heldq。逐笔核对LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理。线性永续无现货借币，不虚构借币费；缺盘口/TCA、完整历史层级/最大量、逐tick强平和容量证明。

冻结判据保持：所有成本全期净正、1倍>=9/12正月；各成本近期净正且>=6/8正五日折；3倍整体DD<=25%；N/K索引半径1含中心，邻域3倍正和严格近期合格比例都>=60%；>=4原生平仓、毛参考PnL+资金费/执行成本>=2.5；0现金/订单/保证金代理违规、终点flat、>=180日。BTC源仅N一维，父组合N/K二维；基准不参与候选资格。最高Sharpe边界/相邻cliff仅作依赖样本描述，不据结果扩批或放宽门槛，也不冒充DSR/PBO显著性。

|新配置|角色|BTC N|ETH K|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|localmix370_BTC_N1250_momentum|component|1250|None|10.000911|8.328489|6.655746|9.156191|9|4/4/4|rejected|
|localmix370_BTC_N1250_constantlong|benchmark_native|1250|None|-8.485978|-9.533883|-10.581790|18.221668|6|4/4/4|rejected|
|localmix370_parent_BTCN750_ETHentryGateK250ppm_D1|candidate|750|0.00025|11.129286|9.867785|8.606332|4.088733|12|6/6/6|passed|
|localmix370_parent_BTCN750_ETHentryGateK500ppm_D1|candidate|750|0.0005|11.343181|10.213998|9.084782|3.540488|12|6/6/6|passed|
|localmix370_parent_BTCN750_ETHentryGateK750ppm_D1|candidate|750|0.00075|11.327169|10.198422|9.069643|3.540488|12|6/6/6|passed|
|localmix370_parent_BTCN1000_ETHentryGateK250ppm_D1|candidate|1000|0.00025|11.597667|10.264343|8.931057|4.336854|12|6/6/6|passed|
|localmix370_parent_BTCN1000_ETHentryGateK750ppm_D1|candidate|1000|0.00075|11.795550|10.594980|9.394369|3.689721|12|6/6/6|passed|
|localmix370_parent_BTCN1250_ETHentryGateK250ppm_D1|candidate|1250|0.00025|12.000974|10.598030|9.195063|4.596417|12|6/6/5|rejected|
|localmix370_parent_BTCN1250_ETHentryGateK500ppm_D1|candidate|1250|0.0005|12.214869|10.944244|9.673513|3.844805|12|6/6/5|rejected|
|localmix370_parent_BTCN1250_ETHentryGateK750ppm_D1|candidate|1250|0.00075|12.198856|10.928668|9.658374|3.844805|12|6/6/5|rejected|
|localmix370_parent_BTCN1250_constantlong|benchmark_parent|1250|None|-11.442367|-12.298046|-13.153728|20.971690|6|4/4/4|rejected|

新配置失败项：{'localmix370_BTC_N1250_momentum': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'localmix370_BTC_N1250_constantlong': ['benchmark_control_not_strategy_candidate'], 'localmix370_parent_BTCN750_ETHentryGateK250ppm_D1': [], 'localmix370_parent_BTCN750_ETHentryGateK500ppm_D1': [], 'localmix370_parent_BTCN750_ETHentryGateK750ppm_D1': [], 'localmix370_parent_BTCN1000_ETHentryGateK250ppm_D1': [], 'localmix370_parent_BTCN1000_ETHentryGateK750ppm_D1': [], 'localmix370_parent_BTCN1250_ETHentryGateK250ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'localmix370_parent_BTCN1250_ETHentryGateK500ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'localmix370_parent_BTCN1250_ETHentryGateK750ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'localmix370_parent_BTCN1250_constantlong': ['benchmark_control_not_strategy_candidate']}。旧中心仍为rejected，旧canonical裁定不因这轮邻域改变而重写，当前诊断见sensitivity_grid.csv及单独保留校验。

11CSV包含33新增成本场景、429月/尾折、264近期折、12243日NAV、27父N/K格行、9原生N格行、9旧N500基线场景、42相邻边、27同N持有/现金比较、33新旧原生成本路径和12资金配置；所有正负折及完整回撤保留。

2026-11-04UTC读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对fundingTime/fundingRate/markPrice和tick/step单位；数值只取真实parquet/公开API。配比盈利是项目假设，官方文档不提供盈利结论；8源行情及spec/report/archive/code SHA见plan/binding/data_manifest。

原SMA65与single继续Nov4UTC14:30→16:30，独立L4为16:10→18:10。single本窗可能跨16:00.001资金费，按自己的原BTC q=-0.012及真实ns/rate/mark核算，不能复制L4上轮现金流；L4已入账16:00不能重复。无新日决策时保留原规则/本金/数量/risk/context和完整NAV前缀，不采纳本轮研究，不在每轮截止强平。SMA完整日线仍来自20261104T021133Z/forward_inputs.json.gz；partial不冒充180日/六折，旧延迟shadow与十策略真实报价观察分开。

同main排他锁内完成全部真实结果登记、只读snapshot和monitor核验，只清理可重建中间物。完整账本/冻结规则/登记/真实API与失败证据保留，不重部署网页或新建定时任务。真实push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261104T181839Z.json。

独立核验通过5个新历史候选：BTCN750×K0.025/0.05/0.075%，以及BTCN1000×K0.025/0.075%，均固定D1；各成本近期均6/8，邻域严格近期比例为100%或66.67%。BTCN1250三格3倍成本近期均5/8、邻域50%，淘汰。旧N1000/K0.05%中心保持原rejected/原criteria/原sensitivity，只展示新邻域诊断。新原生108笔成本场景成交中96笔LOT数量和全部108笔冲击不能从旧N1000按1.25倍线性得到。通过仅限复用历史，不是独立前向或稳定实盘结论，三个原冻结账户不采纳本批规则。

封存：11新金融配置/33成本场景逐项finish，组合通过5、淘汰3，1个新BTC金额组件通过0；2个新持有对照不作候选。新原生决策2220次、资金费6660条、成交108笔；旧27成本账本资金费29970条、成交720笔均是旧记录。独立审计{'funding': 36630, 'fills': 828, 'rejects': 0, 'metric_checks': 840, 'margin_checks': 239454}，0父订单。20新ID/40追加事件，33433旧保护文件不变。

原SMA续2026-11-04T14:30:00Z至2026-11-04T16:30:00Z，NAV48424+120=48544，累计48509分钟。single续2026-11-04T14:30:00Z至2026-11-04T16:30:00Z，NAV12673+124=12797，累计315ID；本窗实际新增资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0.09632916000000000000000000000', 'amount_usdt': '0.09632916000000000000000000000', 'mark': '80274.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0.09632916000000000000000000000', 'amount_usdt': '0.09632916000000000000000000000', 'mark': '80274.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0.09632916000000000000000000000', 'amount_usdt': '0.09632916000000000000000000000', 'mark': '80274.30000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2425.77209302', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2425.77209302', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2425.77209302', 'rate': '0.00010000'}]。L4续2026-11-04T16:10:00Z至2026-11-04T18:10:00Z，NAV5412+122=5534，累计138ID，本窗资金费[]，不重复上轮08结算。三者新日决策/成交SMA 0/0、single 0/0、L4 0/0。原规则/本金与完整前缀保留，partial不冒充180日/六折，不采纳本批研究。

监控通过：9399研究行，9388旧完整行不变，10报价账户/250观察，gzip4304785字节。本轮必要正式管线均实际退出0。HTTP/传输失败0次全部保留；取得共用锁后写入，官方文档本轮读取成功，实际资金费字段/现金流已核验。0已完成金融/观察重跑，清理0真实结果/账本，零可重建缓存遗留。

全部正负折/逐变体、完整DD、spec/report/archive/数据/代码SHA、真实短窗及失败证据保留。main非强制push、完整远端tree/blob及实际终态/解锁凭据见.git/automation_proofs/20261104T181839Z.json。
