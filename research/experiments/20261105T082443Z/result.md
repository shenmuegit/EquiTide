本轮6个新组合通过0/6，淘汰6/6。连续370日walk-forward、ETH D/K两轴敏感性和1/2/3倍成本测试完成。3倍净收益11.165131%～17.881964%，完整连续回撤4.904551%～6.296950%。资格逐项见表与失败项；历史通过不代表独立前向或稳定实盘盈利。

事前固定BTC入场3000、3750独立银行，ETH4500/15000、D1/3/5×K250/500/750ppm。检验BTC预算3000与ETH固定4500的实际敞口与ETH斜率时间/门槛的联合敏感性，完整保留近期失败可能；只补6个新K250/750组合，旧K500、原生银行和同N持有只读。已复用历史和既往选择，不能把全期正收益称稳健合格，不据本轮结果改批次/门槛。

完整读取27844登记事件/13800ID、309既往结论及三技能/README/OOS/freqtradeZIP。初始16项均有实际证据、缺0；此前独立研究定义9871，标实际9658，未标213。保留多重选择偏差，反复开发历史不是未触碰最终留出。

固定BTC入场3000、银行3750，ETH入场4500、银行15000，总18750；raw[1,1]相加完整银行，不归一化或重复乘20/80%资本份额。BTC名义占自身80%、总16%；ETH占自身30%、总24%。无NAV/数量/成本缩放、父订单、克隆、转移、再平衡或交叉保证金。

BTC ROC31/H4%/E1%固定；ETH contrarianROC5/H2%/E0.5%，有限归一化EWM24 beta23/25，D1/3/5与严格K0.025/0.05/0.075%。仅新开仓/反手检查趋势及V10样本logvol上限4.5%，同向现仓保留；失败反转先平旧仓、不新开。所有信号只读过去完整收盘，下一UTC00:01OPEN，原生数量按N/priorclose/LOT取整，终点计成本平仓。

26旧结果/13原生银行/39成本路径只读恢复完整净值与SHA，0原生策略重跑；6个新K250/750父组合/18场景全部先reserve。3个旧K500组合canonical状态/criteria/sensitivity不改，当前D/K诊断单列。所有候选逐格匹配旧同N3000、同本金BTC+ETH4500持有及现金0%；另有9个旧BTC2000、相同ETHD/K基线，BTC预算有意不同。

共同事件轴545013点，2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30完整折+10日尾折；近期40日从day330真实状态延续、8×5日，无折间重开。无拟合或标签，purge0，33日上下文覆盖最大32日信号。整体DD从完整连续分钟/事件NAV计算，不平均组件Sharpe或回撤。

敏感性D/K索引半径1含中心，父组合与只读ETH源均两轴，所有9格×3成本及72相邻边、最高Sharpe边界/cliff完整报告。依赖邻域只是描述性诊断，不作DSR/PBO显著性，不据结果扩网格或放宽门槛。

费用5bp/边，半价差1bp、滑点2bp，冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行费用和资金费支出、收入不放大；实际结算ns/rate/mark/当时持仓，不把费率用于信号。保留LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押及1%闭合小时不利mark风险代理。线性永续无现货借币；缺L2/TCA/完整历史层级/最大量/逐tick强平与真实容量证明。

资格固定：每成本全期净正；1倍>=9/12正月；每成本近期净正且>=6/8正五日折；3倍整体DD<=25%；邻域3倍正和严格近期合格率均>=60%；>=4原生平仓；毛参考PnL+资金费/执行成本>=2.5；0现金/订单/风险代理违规、终点flat、>=180日。

|新组合|D|K|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|lagmix370_parent_BTCN3000_ETHentryGateK250ppm_D1|1|0.00025|14.934333|13.049761|11.165131|6.296950|10|5/5/5|rejected|
|lagmix370_parent_BTCN3000_ETHentryGateK750ppm_D1|1|0.00075|15.132216|13.380399|11.628442|4.904551|10|5/5/5|rejected|
|lagmix370_parent_BTCN3000_ETHentryGateK250ppm_D3|3|0.00025|19.039754|16.960733|14.882162|6.030732|12|5/5/5|rejected|
|lagmix370_parent_BTCN3000_ETHentryGateK750ppm_D3|3|0.00075|19.039754|16.960733|14.882162|6.030732|12|5/5/5|rejected|
|lagmix370_parent_BTCN3000_ETHentryGateK250ppm_D5|5|0.00025|22.224002|20.052868|17.881964|6.030732|12|5/5/5|rejected|
|lagmix370_parent_BTCN3000_ETHentryGateK750ppm_D5|5|0.00075|20.356852|18.236043|16.115564|6.030732|12|5/5/5|rejected|

实际失败项：{'lagmix370_parent_BTCN3000_ETHentryGateK250ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN3000_ETHentryGateK750ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN3000_ETHentryGateK250ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN3000_ETHentryGateK750ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN3000_ETHentryGateK250ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN3000_ETHentryGateK750ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

11CSV保留18新成本场景、234月/尾折、144近期折、6678日NAV、27父网格/27旧ETH网格、27旧BTC2000匹配D/K基线场景、72相邻边、27同N3000持有/现金比较、39旧原生成本路径与10资金配置；全部正负结果永久保留。

原SMA65与single分别从Nov5_04:30续至06:30；L4与FEWM分别从06:10续至08:10。各自沿用原现金/单位/desired/成本/risk/完整NAV前缀，不重开账户或重复午夜结算。本窗无日目标或新成交；L4与FEWM的08资金费须以实际fundingTime/rate/mark和各自旧持仓独立核验，single当前截止06:30不计入08资金费。SMA完整65日spot上下文仍为20261105T022141Z/forward_inputs.json.gz。FEWM累计489分钟/15实际观察ID，固定BTC3750/N750和ETH15000/N4500、D1/K.0005，不采纳历史N3000。预先声明只复用L4真实公开行情、元数据和时间，single另取自己的分钟/hour/funding；FEWM同时间窗完全复用公共市场数组，账户book和现金流各自独立计算，未复制其他账户结果。全部仍partial延迟shadow，不作为180日/六折、稳定实盘或十策略真实报价模拟业绩。

2026-11-05UTC实际读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对fundingTime/fundingRate/markPrice及单位。实际数值只用真实parquet/API；文档不提供盈利结论。原始行情保留忽略data，提交轻量账本/上下文/URL/SHA和复现代码，不提交大行情。

同main排他锁内完成登记、只读snapshot与monitor检查，snapshot不执行回测或成交，不改账户/本金/规则，不重部署网页或新建定时任务。只清理可重建中间物，保留完整账本、冻结规则、登记和结果核验所需证据。实际push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261105T082443Z.json。

封存：6新金融配置/18成本场景，历史通过0、淘汰6。18新ID/36事件全部finish，35492旧保护文件保持。0原生策略重跑，39旧原生成本路径只读审计。

原SMA NAV49265→49385，增加120闭合分钟；完整65日spot上下文保留20261105T022141Z。single NAV13534→13656，累计336观察ID。L4 NAV6271→6395，累计159ID。FEWM NAV379→503，累计489分钟/15ID，1/2/3成本累计收益{'1': -0.0019546132288716933, '2': -0.005052173228881074, '3': -0.008153359628859658}。四账户规则/本金/持仓/原完整NAV前缀与资金费游标保持，事件数量从实际packet推导，本窗无日目标或新成交，L4与FEWM各自完成真实08资金费入账；single截止06:30未计入08。具体资金费时间、费率、mark、自己旧持仓及金额见primary_funding_field_verification.json，不复制现金流。

已在任何新预留前声明公共市场响应复用：single只用L4当前真实公开元数据和时间，六个行情请求独立抓取；FEWM用同窗口L4真实市场数组和原provenance，但ownfrozenbinding/normalize/3reserve/advance/完整账本审计独立执行一次。没有复用其他账户状态、现金、仓位、资金费现金流、交易、净值或资格。各账户仍partial，不作180日/六折或稳定实盘结论。

只读监控9436行，原9430行完整不变，10报价账户/257观察；gzip4318675字节。实际HTTP失败0次留档。本轮参数、金额、权重、边界、门槛均在预登记前固定，未发生已完成回测或账户结果重跑；前置目录与main核对证据留档。完整账本/冻结规则/登记/真实输入及核验必需文件保留，清理只限可重建中间物。实际非强制push、完整远端tree/blob及解锁终态见.git/automation_proofs/20261105T082443Z.json。
