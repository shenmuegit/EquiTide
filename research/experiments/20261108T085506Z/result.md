本轮6新ETH快周期配置＋6新组合，共36成本场景实际回测；组合历史通过0/6、淘汰6/6。旧L5三格原生和父组合只读。

上轮L4/D8提高历史收益但增加回撤且仍在快周期/慢间隔边界，最高Sharpe仍为旧L5/D7。本轮预设更宽快周期L3/5/7日×慢间隔D6/7/8日，固定E1%、H2%、finiteEWM24/K1.5%、entry-only V10cap4.5%和原银行，检验更短周期的噪音与更长周期滞后是否形成局部合格区域或性能悬崖。L5三旧组件/组合只读；6新ETH和6新组合逐个reserve后计算，旧L4结果只读描述性比较，不重跑。事前代表D6/L3，不因结果改代表/扩网格/改门槛。正负、失败、同路径均保留；重复开发历史不是未触碰最终/独立未来或稳定实盘盈利。

完整读取30256登记事件/15006ID、345份既往结论。初始16项真实历史证据齐全，缺0；此前研究定义10285、标实际10072、未标实际213，不称全部登记均有结果。

固定BTC signedROC29日/H3%/E1%，只读C3750/N1000。ETH C15000/N4500、反向ROC4/5/6日/H2%、finiteEWM24 beta23/25、固定严格斜率K1.5%，D6/7/8日×快周期L3/5/7，退出E1%固定。入场strictH优先；阈值内原long在ROC<E保留、原short在ROC>-E保留，等于退出边界平仓。慢趋势与V10样本logvol上限4.5%只过滤新开/反手；同向留实际q、反手先平后开，无日再平衡。新参数均实际核算数量、LOT、成交量冲击、费用、资金费、风险和完整NAV。

Raw[1,1]直接相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘、不归一化、不缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

370日连续开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30完整折＋10日尾。近期40日继承day330现金/q，划8×5日，不折间重开。BTC需30、ETH最大32过去完整收盘，来源33日；仅完整过去收盘发信号，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0；逐折及连续整体DD留档。重复开发历史和多轮参数选择不是未触碰最终留出、独立未来或稳定实盘收益。

每边5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出压力，收入不放大；真实fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理；缺L2/TCA/历史完整层级/逐tick强平与真实容量证据。

原生和父组合D/L各9格、旧L5列只读；索引半径1含中心，全部变体收益/整体DD/Sharpe/Calmar及72邻接边、边界/跳变留档。门槛原样：全期和近期各成本净正、1倍≥9/12正30日折、各成本近期≥6/8正5日、3倍DD≤25%、局部三倍净正与严格近期合格率≥60%、至少4原生平仓、毛PnL＋资金费/1倍成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。与同C/N真实常持有及现金0%只读比较，不据结果改变门槛。

|新配置|类别|ETH D|L|固定E|固定K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|fastperiod370_ETH_D6_L3_E10000ppm|native|6|3|0.01|0.015|15.786453|14.202822|12.619124|4.584025|3/3/3|rejected|
|fastperiod370_ETH_D6_L7_E10000ppm|native|6|7|0.01|0.015|11.208341|10.543042|9.877938|3.437549|2/2/2|rejected|
|fastperiod370_ETH_D7_L3_E10000ppm|native|7|3|0.01|0.015|16.504363|14.931270|13.358110|4.553552|3/3/3|rejected|
|fastperiod370_ETH_D7_L7_E10000ppm|native|7|7|0.01|0.015|16.877784|15.961152|15.044814|4.570324|2/2/2|rejected|
|fastperiod370_ETH_D8_L3_E10000ppm|native|8|3|0.01|0.015|18.889812|17.249423|15.608849|4.526040|3/3/3|rejected|
|fastperiod370_ETH_D8_L7_E10000ppm|native|8|7|0.01|0.015|21.163730|20.015635|18.867677|4.570324|3/3/3|rejected|
|fastperiod370_parent_BTC29H3_D6_L3_E10000ppm|parent|6|3|0.01|0.015|15.029063|13.466198|11.903282|4.311668|5/5/5|rejected|
|fastperiod370_parent_BTC29H3_D6_L7_E10000ppm|parent|6|7|0.01|0.015|11.366574|10.538373|9.710333|3.177528|6/6/5|rejected|
|fastperiod370_parent_BTC29H3_D7_L3_E10000ppm|parent|7|3|0.01|0.015|15.603391|14.048956|12.494470|3.883798|5/5/5|rejected|
|fastperiod370_parent_BTC29H3_D7_L7_E10000ppm|parent|7|7|0.01|0.015|15.902128|14.872861|13.843834|3.967173|6/6/5|rejected|
|fastperiod370_parent_BTC29H3_D8_L3_E10000ppm|parent|8|3|0.01|0.015|17.511751|15.903478|14.295062|3.864898|5/5/5|rejected|
|fastperiod370_parent_BTC29H3_D8_L7_E10000ppm|parent|8|7|0.01|0.015|19.330884|18.116448|16.902124|3.967173|6/6/5|rejected|

逐项失败判据：{'fastperiod370_ETH_D6_L3_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D6_L7_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D7_L3_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D7_L7_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D8_L3_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D8_L7_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_parent_BTC29H3_D6_L3_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_parent_BTC29H3_D6_L7_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_parent_BTC29H3_D7_L3_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_parent_BTC29H3_D7_L7_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_parent_BTC29H3_D8_L3_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_parent_BTC29H3_D8_L7_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

原四冻结账户独立延续原现金/q/desired/成本/风险/fullNAV，不采用研究快周期L。本轮SMA/single Nov8_04:30→06:30仅闭合mark，L4/FEWM Nov8_06:10→08:10跨真实08:00:00.001资金费，按各自结算前q/rate/mark记账，均无新日决策/成交，不重复已完成的Nov8_00/00:01或旧16。SMA完整65日spot上下文保留R025309的1d/1m字典，本轮输入minute数组需核对重叠，所有原规则/本金/持仓与完整NAV前缀不变。所有账户partial延迟shadow，非十策略实时报价收益或180日资格。

finish和必要检查后，在同main排他锁内生成只读monitor并检查。保留全部正负、失败、冻结规则、完整账本、登记及必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。真实main push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261108T085506Z.json。


本轮实际完成并独立核验walk-forward、D/L两轴敏感性和1/2/3倍成本压力测试，12新配置全部淘汰，未改门槛、未追加选峰或补算批次。全部36成本场景全期净正，但6ETH原生近期仅2–3/8正5日折、局部严格比例0，D6/L7还仅8/12正30日折；6组合三倍近期均5/8正折、局部严格比例50%低于预登记60%，因此全部rejected。L3组合各成本均5/8，L7组合1/2倍6/8却在3倍降到5/8，显示成本能使近期折变号。78个真实负30日成本折及所有负/零近期折完整保留。

历史仍为370日连续12×30完整折＋10日尾，近期40日继承day330真实现金/q划8×5，不折间重开。固定无fit/标签，purge/embargo0，33日源覆盖最大32日过去完整收盘；快ROC精确使用close[i-1]/close[i-1-L]，下一UTC00:01 OPEN执行，历史终点计成本平仓。新L3/L7/D6/7/8逐项先reserve、实际计算后finish；L5三旧组件/组合、BTC29/H3/E1银行3750/N1000和匹配持有控制只读。Raw[1,1]完整银行相加，不归一化、重复乘20/80%、缩放旧ETH数量/NAV/成本或新建父订单。重复开发历史、多轮参数选择和本轮12定义不能称未触碰最终留出、独立未来或稳定实盘盈利。

最高新组合D8/L7的1/2/3倍净收益19.330884%/18.116448%/16.902124%，3倍连续整体DD3.967173%，仍因近期3倍5/8和局部50%淘汰；不能把高收益、最高Sharpe或较小整体回撤替代近期稳健性。事前代表D6/L3的3倍净收益11.903282%、DD4.311668%，各成本近期5/8，同样淘汰，未以D8/L7替换代表。D/L九格全部Sharpe正，最大收益/Sharpe在D8/L7边界，但组合严格近期仅旧L5三格3/9、原生0/9；六组描述性相邻Sharpe跳变仍true，未建立平坦可独立验证的合格平台。旧L5的canonical资格和旧报告字节保持，只加本轮邻域描述性诊断，不用新邻域改写旧资格。

新组合3倍净收益9.710333%–16.902124%，整体DD3.177528%–4.311668%。与同D旧L5及上轮L4的真实已保存收益/DD/Sharpe/Calmar分别比较，prior_L4_comparison.json保存36条各成本描述性对照；旧L4无策略/净值重跑，未据对照改变任何门槛。相同C/N/时间边界的353个旧ETH原生及63个旧父组合三成本完整NAV哈希比对，12新定义无旧三路径匹配；不同路径仍是同一复用市场，不构成独立样本。

独立审计18新ETH原生＋18新父组合＋18旧原生只读路径，6660新策略决策、39960新旧资金费、1350新旧成交、155727保证金检查，全部通过且无订单拒绝。费用、半价差、滑点、过去20日logvol×sqrt(实际成交名义/quoteADV)量相关冲击、真实资金费rate/mark/当时q及LOT/tick/minnotional/参与率≤0.1%/费后抵押与小时不利mark代理均保留，执行和资金费支出压力1/2/3倍、正收入不放大。缺L2/TCA、完整历史层级/逐tick强平和实盘容量证明，正全期回测不能称稳定实盘盈利。

本轮账户预先公开只读取08结算字段、未计算数量或现金；真实fundingTime=1794124800001ms，即UTC08:00:00.001/1794124800001000000ns，不能截断整秒。预检原始响应、HTTP回执及哈希固定进窗口；随后先reserve每个实际观察配置，再由原冻结观察器按自己账本推进。L4和FEWM各6条结算记录，BTC实际rate0.00007157、mark75939.00000000，L4旧q−0.006每成本收入0.03260972538，FEWM旧q−0.009每成本收入0.04891458807，正收入未乘2/3倍；ETH实际rate0.00010000、mark2240.24000000，但两户ETHq0，逐场景派生0资金费且保留结算记录，不是缺数据。actual08_funding_verification逐条核对12条真实时间/rate/mark/q/金额/cash_before/after，并全链每资产/成本仅一次；旧00/16没有重算或重复，未复制另一户现金流。

四原账户连续性：SMA NAV53588→53708、53669分钟/37完整日；single 17953→18075、17669分钟/444ID；L4 10690→10814、10569分钟/267ID；FEWM 4798→4922、4809分钟/123ID。所有账户无新日决策/成交；L4/FEWM各自post08现金已承接，数量/entry/原规则/risk/fullNAV连续。SMA/单策略本窗04:30→06:30尚不跨08，未给单策略提前记08；SMA累计三倍仍−7.468958%，负结果保存，原Float/SMA65/1%及2027-03-31终点不变，完整65日spot上下文仍R025309的1d/1m，当前输入minute-array按形状读取和核对重叠。

所有账户仍partial延迟shadow，非P01–P10实时报价执行业绩、180日/六折资格或新研究参数独立未来。下轮SMA/single06:30→08:30，single需按自己q与实际08.001 rate/mark结算，不复制L4/FEWM现金流；SMAspot无funding。L4/FEWM08已各结算一次，下一08:10→10:10仅marks，不重复08/00/16。下一日决策统一Nov9_00:01。冻结规则、本金、持仓、完整账本、登记、正负/淘汰/失败和必要输入保留，无真实订单、子代理、分支、网页重部署或重复定时任务。

封存：6新ETH快周期组件＋6新组合/36场景，组合通过0、淘汰6；24ID/48事件全部finish，47355旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV53588→53708，single 17953→18075，L4 10690→10814，FEWM 4798→4922。single/L4/FEWM实际新资金费0/6/6，日事件0/0/0，成交0/0/0；各自实际资金费时间戳/rate/mark/结算前q与本窗闭合mark独立核验，旧00/00:01仅保留已验证历史证明，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计4809分钟/123ID，所有账户partial非180日资格。
只读监控9856行，原9844行不变，10报价账户/293观察，gzip4526551字节。HTTP/传输失败3次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261108T085506Z.json。
