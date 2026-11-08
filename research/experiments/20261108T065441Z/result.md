本轮6新ETH快周期配置＋6新组合，共36成本场景实际回测；组合历史通过6/6、淘汰0/6。旧L5三格原生和父组合只读。

上轮退出缓冲E1%已成为D/E网格内部峰，所有新退出配置收益低于旧E1%，故停止扩退出轴。本轮检验快反转信号时间尺度：固定退出E1%、入场H2%、finiteEWM24/K1.5%、entry-only V10cap4.5%及原银行，预设快ROC周期L4/5/6日×慢斜率间隔D6/7/8日。较短L可能改善反转时机也可能增交易噪音，较长L可能减换手但延迟平反转；所有真实成本/资金费/风险及近期折按原门槛检验。L5三旧组件和组合只读；6新ETH/6新父组合逐个reserve后计算。事前代表D6/L4/E1%，不依据结果换代表/扩网格/改门槛。全部正负与同路径保留，重复开发历史不是独立最终/未来或稳定实盘盈利。

完整读取30188登记事件/14972ID、344份既往结论。初始16项真实历史证据齐全，缺0；此前研究定义10273、标实际10060、未标实际213，不称全部登记均有结果。

固定BTC signedROC29日/H3%/E1%，只读C3750/N1000。ETH C15000/N4500、反向ROC4/5/6日/H2%、finiteEWM24 beta23/25、固定严格斜率K1.5%，D6/7/8日×快周期L4/5/6，退出E1%固定。入场strictH优先；阈值内原long在ROC<E保留、原short在ROC>-E保留，等于退出边界平仓。慢趋势与V10样本logvol上限4.5%只过滤新开/反手；同向留实际q、反手先平后开，无日再平衡。新参数均实际核算数量、LOT、成交量冲击、费用、资金费、风险和完整NAV。

Raw[1,1]直接相加两个独立完整银行NAV，总本金18750，资金占比20/80%不重复乘、不归一化、不缩放旧q/NAV/成本。BTC初始名义为本银行26.666667%/总本5.333333%，ETH为本银行30%/总本24%；无父订单、转账、再平衡或交叉保证金。

370日连续开发OOS：2025-10-19UTC00:01至2026-10-24UTC00:01，12×30完整折＋10日尾。近期40日继承day330现金/q，划8×5日，不折间重开。BTC需30、ETH最大32过去完整收盘，来源33日；仅完整过去收盘发信号，下一UTC00:01 OPEN执行，终点计成本平仓。固定规则无fit/labels，purge/embargo0；逐折及连续整体DD留档。重复开发历史和多轮参数选择不是未触碰最终留出、独立未来或稳定实盘收益。

每边5bp手续费＋1bp半价差＋2bp滑点；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本与资金费支出压力，收入不放大；真实fundingTime/rate/mark/当时q。线性永续无现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理；缺L2/TCA/历史完整层级/逐tick强平与真实容量证据。

原生和父组合D/L各9格、旧L5列只读；索引半径1含中心，全部变体收益/整体DD/Sharpe/Calmar及72邻接边、边界/跳变留档。门槛原样：全期和近期各成本净正、1倍≥9/12正30日折、各成本近期≥6/8正5日、3倍DD≤25%、局部三倍净正与严格近期合格率≥60%、至少4原生平仓、毛PnL＋资金费/1倍成本≥2.5、无抵押/订单/风险违规、终点flat、≥180日。与同C/N真实常持有及现金0%只读比较，不据结果改变门槛。

|新配置|类别|ETH D|L|固定E|固定K|1x净%|2x净%|3x净%|3x整体DD%|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|fastperiod370_ETH_D6_L4_E10000ppm|native|6|4|0.01|0.015|14.079877|12.751576|11.422914|4.620627|2/2/2|rejected|
|fastperiod370_ETH_D6_L6_E10000ppm|native|6|6|0.01|0.015|7.987799|7.176440|6.365770|6.779770|1/1/1|rejected|
|fastperiod370_ETH_D7_L4_E10000ppm|native|7|4|0.01|0.015|14.796233|13.478097|12.159694|4.580977|2/2/2|rejected|
|fastperiod370_ETH_D7_L6_E10000ppm|native|7|6|0.01|0.015|10.106089|9.019508|7.933568|6.685281|1/1/1|rejected|
|fastperiod370_ETH_D8_L4_E10000ppm|native|8|4|0.01|0.015|18.973629|17.427605|15.881314|4.563889|3/3/3|rejected|
|fastperiod370_ETH_D8_L6_E10000ppm|native|8|6|0.01|0.015|10.469299|9.163681|7.859013|7.072699|2/2/2|rejected|
|fastperiod370_parent_BTC29H3_D6_L4_E10000ppm|parent|6|4|0.01|0.015|13.663802|12.305201|10.946314|4.476484|6/6/6|passed|
|fastperiod370_parent_BTC29H3_D6_L6_E10000ppm|parent|6|6|0.01|0.015|8.790140|7.845092|6.900599|5.647077|6/6/6|passed|
|fastperiod370_parent_BTC29H3_D7_L4_E10000ppm|parent|7|4|0.01|0.015|14.236887|12.886418|11.535738|4.169682|6/6/6|passed|
|fastperiod370_parent_BTC29H3_D7_L6_E10000ppm|parent|7|6|0.01|0.015|10.484772|9.319546|8.154837|5.583455|6/6/6|passed|
|fastperiod370_parent_BTC29H3_D8_L4_E10000ppm|parent|8|4|0.01|0.015|17.578804|16.046024|14.513034|4.169682|6/6/6|passed|
|fastperiod370_parent_BTC29H3_D8_L6_E10000ppm|parent|8|6|0.01|0.015|10.775340|9.434884|8.095193|5.718165|6/6/6|passed|

逐项失败判据：{'fastperiod370_ETH_D6_L4_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D6_L6_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D7_L4_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D7_L6_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D8_L4_E10000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_ETH_D8_L6_E10000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fastperiod370_parent_BTC29H3_D6_L4_E10000ppm': [], 'fastperiod370_parent_BTC29H3_D6_L6_E10000ppm': [], 'fastperiod370_parent_BTC29H3_D7_L4_E10000ppm': [], 'fastperiod370_parent_BTC29H3_D7_L6_E10000ppm': [], 'fastperiod370_parent_BTC29H3_D8_L4_E10000ppm': [], 'fastperiod370_parent_BTC29H3_D8_L6_E10000ppm': []}。

原四冻结账户独立延续原现金/q/desired/成本/风险/fullNAV，不采用研究快周期L。本轮SMA/single Nov8_02:30→04:30，L4/FEWM Nov8_04:10→06:10，均仅闭合mark，无新日决策/资金费/成交，不重复已完成的Nov8_00/00:01或旧16。SMA完整65日spot上下文保留R025309的1d/1m字典，本轮输入minute数组需核对重叠，所有原规则/本金/持仓与完整NAV前缀不变。所有账户partial延迟shadow，非十策略实时报价收益或180日资格。

finish和必要检查后，在同main排他锁内生成只读monitor并检查。保留全部正负、失败、冻结规则、完整账本、登记及必要真实输入，仅清理可重建中间物。无真实订单、页面重部署或新定时任务。真实main push/完整远端tree/blob核验及解锁终态见.git/automation_proofs/20261108T065441Z.json。


本轮实际完成并独立核验三项验证。ETH快周期L4/5/6×慢斜率D6/7/8，两轴九格，固定退出E1%、严格对称入场H2%、finiteEWM24/K1.5%、entry-only V10cap4.5%。L5三旧组件和组合、BTC29/H3/E1 C3750/N1000及匹配持有控制只读。6新ETH原生与6新组合共36成本场景，全期均净正；6组合满足原预登记门槛历史通过，6ETH组件近期各成本仅1–3/8正5日折而淘汰，其中D8/L6原生额外未达1倍≥9/12正30日折（实为8/12）。其余新原生9/12，组合9或10/12；86个实际负30日成本折和所有负/零近期折完整保留。

Walk-forward保留370日连续12×30完整折＋10日尾，以及继承day330实际现金/q的近期40日8×5。固定规则无fit/标签，purge/embargo0，最大32个过去完整日收盘、来源33日；快ROC准确取close[i-1]/close[i-1-L]-1，下一UTC00:01 OPEN执行，历史终点计成本平仓，无未来价格/测试段调参。多轮复用开发历史、此前大量配置选择和本轮12定义不构成未触碰最终留出或独立未来证据。

1/2/3倍成本下，事前代表D6/L4组合净收益13.663802%/12.305201%/10.946314%，3倍整体DD4.476484%，按原门槛通过，未换成事后最高点。最高新收益点D8/L4的1/2/3倍为17.578804%/16.046024%/14.513034%，3倍连续DD4.169682%；比同D旧L5的3倍收益13.090151%多约1.422883个百分点，但DD从3.737890%升高，不能只报收益改善。D8/L4仍处于两个网格轴边缘。最高Sharpe则仍是只读D7/L5内部点，不能混同收益峰与风险调整表现。

全部新组合3倍净收益6.900599%–14.513034%，整体DD4.169682%–5.718165%；9/9组合格近期各成本6/8及局部严格比例100%，原生0/9格达近期门槛。两轴完整收益/DD/Sharpe/Calmar、72邻接边均留档，六组描述性Sharpe跳变标记仍true，不声称平坦稳定平台、显著独立优势或实盘稳定盈利。新快周期不是对原L4/FEWM/SMA/单策略冻结账户的改参。

成本保留真实数量、LOT/tick/minnotional、费用/半价差/滑点、过去20日样本logvol×sqrt(实际成交名义/quoteADV)量相关冲击、真实资金费rate/mark/当时q，1/2/3倍支出压力而正资金费收入不放大。逐笔余额、抵押、参与率≤0.1%及1%闭合小时不利mark风险代理均核验；缺L2/TCA、完整历史保证金层级/逐tick强平及真实容量证明。独立审计18新原生＋18新父组合＋18旧原生只读路径，6660新策略决策、39960新旧资金费、1320新旧成交、159357保证金检查，均通过且无订单拒绝。没有重跑已完成配置或缩放旧ETH净值替代新数量/成本。

相同C/N/时间边界的347个旧ETH原生（覆盖不同快周期）与57个旧父组合三成本完整NAV哈希比较，12新定义没有旧三路径匹配；这不使同一市场历史成为独立样本。与同D旧L5的各成本收益/DD对照保留，原资格不改，不因事后相对表现另加淘汰门槛。

发现前轮research/experiments/20261108T045410Z/historical_pass_followup.json的派生说明沿用更早E0.625%批次“3通过组合重复旧净值”文字；前轮实际report.json、validation_status计数及same_bank_realized_NAV_alias_diagnostic.json均显示0重复，原回测和登记资格正确且字节未变。本轮prior_derived_metadata_correction.json保存原文/文件SHA及权威0重复核验SHA，更正派生说明，不重写历史/登记或重跑回测。当前historical_pass_followup/validation_status按实际字段生成，并已用derived_metadata_verification独立检查数量、D/L轴、代表点和更正依据。

原四账户实际续接：SMA NAV53468→53588、53549分钟/37完整日；single 17831→17953、17549分钟/441ID；L4 10568→10690、10449分钟/264ID；FEWM 4676→4798、4689分钟/120ID。本轮全部无新funding/日决策/成交，18子账本现金/q/entry/desired/费用和完整NAV前缀连续；旧Nov8_00及Nov7_16各按自己q/rate/mark结算一次，不复制现金流、不重开现金或采用研究L。SMA3倍累计仍−7.468958%，负结果完整保存；当前与前轮输入minute-array，完整65日spot上下文仍R025309的1d/1m字典，原Float/SMA65/1%及2027-03-31终点不变。

账户均partial延迟shadow，非十策略实时报价执行、180日/六折资格或新研究参数独立未来。下轮SMA/single Nov8_04:30→06:30仍marks；L4/FEWM Nov8_06:10→08:10只能在08:11参考闭合后推进，先reserve，按各自结算前持仓及实际08 rate/mark/时间戳独立核算，不复制另一账户现金流、不重复00/16。下一日决策统一Nov9_00:01。冻结规则、本金、持仓、完整账本/登记及必要输入保留，无真实订单/子代理/网页重部署或重复定时任务。

封存：6新ETH快周期组件＋6新组合/36场景，组合通过6、淘汰0；24ID/48事件全部finish，47003旧文件保持。18旧原生路径只读，18新ETH原生路径/6660实际决策及18新组合路径独立核验。
原SMA NAV53468→53588，single 17831→17953，L4 10568→10690，FEWM 4676→4798。single/L4/FEWM实际新资金费0/0/0，日事件0/0/0，成交0/0/0；各自rate/mark/结算前q和先funding后00:01决策独立核验，原现金/q/风险/fullNAV连续，不复制现金流或重复16/00。FEWM累计4689分钟/120ID，所有账户partial非180日资格。
只读监控9844行，原9832行不变，10报价账户/292观察，gzip4519677字节。HTTP/传输失败1次原证据保留，所有正负/淘汰结果、完整账本/冻结规则/登记/必要输入保留。真实main push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261108T065441Z.json。
