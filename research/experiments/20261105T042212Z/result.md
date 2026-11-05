本轮6个新组合通过0/6，淘汰6/6。连续370日walk-forward、ETH D/K两轴敏感性和1/2/3倍成本测试完成。3倍净收益12.268486%～15.268288%，完整连续回撤3.920636%～3.920636%。资格逐项见表与失败项；历史通过不代表独立前向或稳定实盘盈利。

事前固定BTC入场625、3750独立银行，ETH4500/15000、D1/3/5×K250/500/750ppm。检验较高BTC实际敞口与ETH斜率时间/门槛的联合敏感性，完整保留近期失败可能；只补6个新D3/5组合，旧D1、原生银行和同N持有只读。已复用历史和既往选择，不能把全期正收益称稳健合格，不据本轮结果改批次/门槛。

完整读取27732登记事件/13744ID、307既往结论及三技能/README/OOS/freqtradeZIP。初始16项均有实际证据、缺0；此前独立研究定义9859，标实际9646，未标213。保留多重选择偏差，反复开发历史不是未触碰最终留出。

固定BTC入场625、银行3750，ETH入场4500、银行15000，总18750；raw[1,1]相加完整银行，不归一化或重复乘20/80%资本份额。BTC名义占自身1/6、总3.333333%；ETH占自身30%、总24%。无NAV/数量/成本缩放、父订单、克隆、转移、再平衡或交叉保证金。

BTC ROC31/H4%/E1%固定；ETH contrarianROC5/H2%/E0.5%，有限归一化EWM24 beta23/25，D1/3/5与严格K0.025/0.05/0.075%。仅新开仓/反手检查趋势及V10样本logvol上限4.5%，同向现仓保留；失败反转先平旧仓、不新开。所有信号只读过去完整收盘，下一UTC00:01OPEN，原生数量按N/priorclose/LOT取整，终点计成本平仓。

26旧结果/13原生银行/39成本路径只读恢复完整净值与SHA，0原生策略重跑；6个新D3/5父组合/18场景全部先reserve。3个旧D1组合canonical状态/criteria/sensitivity不改，当前D/K诊断单列。所有候选逐格匹配旧同N625、同本金BTC+ETH4500持有及现金0%；另有9个旧BTC750、相同ETHD/K基线，BTC预算有意不同。

共同事件轴545013点，2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30完整折+10日尾折；近期40日从day330真实状态延续、8×5日，无折间重开。无拟合或标签，purge0，33日上下文覆盖最大32日信号。整体DD从完整连续分钟/事件NAV计算，不平均组件Sharpe或回撤。

敏感性D/K索引半径1含中心，父组合与只读ETH源均两轴，所有9格×3成本及72相邻边、最高Sharpe边界/cliff完整报告。依赖邻域只是描述性诊断，不作DSR/PBO显著性，不据结果扩网格或放宽门槛。

费用5bp/边，半价差1bp、滑点2bp，冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行费用和资金费支出、收入不放大；实际结算ns/rate/mark/当时持仓，不把费率用于信号。保留LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押及1%闭合小时不利mark风险代理。线性永续无现货借币；缺L2/TCA/完整历史层级/最大量/逐tick强平与真实容量证明。

资格固定：每成本全期净正；1倍>=9/12正月；每成本近期净正且>=6/8正五日折；3倍整体DD<=25%；邻域3倍正和严格近期合格率均>=60%；>=4原生平仓；毛参考PnL+资金费/执行成本>=2.5；0现金/订单/风险代理违规、终点flat、>=180日。

|新组合|D|K|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|lagmix370_parent_BTCN625_ETHentryGateK250ppm_D3|3|0.00025|15.119514|13.693723|12.268486|3.920636|11|5/5/4|rejected|
|lagmix370_parent_BTCN625_ETHentryGateK500ppm_D3|3|0.0005|15.119514|13.693723|12.268486|3.920636|11|5/5/4|rejected|
|lagmix370_parent_BTCN625_ETHentryGateK750ppm_D3|3|0.00075|15.119514|13.693723|12.268486|3.920636|11|5/5/4|rejected|
|lagmix370_parent_BTCN625_ETHentryGateK250ppm_D5|5|0.00025|18.303762|16.785857|15.268288|3.920636|12|5/5/4|rejected|
|lagmix370_parent_BTCN625_ETHentryGateK500ppm_D5|5|0.0005|18.303762|16.785857|15.268288|3.920636|12|5/5/4|rejected|
|lagmix370_parent_BTCN625_ETHentryGateK750ppm_D5|5|0.00075|16.436612|14.969033|13.501888|3.920636|11|5/5/4|rejected|

实际失败项：{'lagmix370_parent_BTCN625_ETHentryGateK250ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN625_ETHentryGateK500ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN625_ETHentryGateK750ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN625_ETHentryGateK250ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN625_ETHentryGateK500ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN625_ETHentryGateK750ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

11CSV保留18新成本场景、234月/尾折、144近期折、6678日NAV、27父网格/27旧ETH网格、27旧BTC750匹配D/K基线场景、72相邻边、27同N625持有/现金比较、39旧原生成本路径与10资金配置；全部正负结果永久保留。

原SMA65与single各自从Nov5_00:30续至02:30；FEWM与旧L4各自从02:10续至04:10。四账户各自携带真实现金、单位、desired、成本、风险和完整NAV前缀，本窗无日决策，实际资金费/成交事件独立核验。SMA完整65日spot上下文仍为20261105T022141Z/forward_inputs.json.gz；本轮只追加闭合分钟mark。FEWM累计249分钟、9个实际观察ID，仍固定BTC3750/N750、ETH15000/N4500、D1/K.0005，不重复首笔、不重取warmup、不采纳研究BTC625。四账户均为partial延迟shadow，不作为180日/六折、稳定实盘或十策略真实报价模拟结果。

2026-11-05UTC实际读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对fundingTime/fundingRate/markPrice及单位。实际数值只用真实parquet/API；文档不提供盈利结论。原始行情保留忽略data，提交轻量账本/上下文/URL/SHA和复现代码，不提交大行情。

同main排他锁内完成登记、只读snapshot与monitor检查，snapshot不执行回测或成交，不改账户/本金/规则，不重部署网页或新建定时任务。只清理可重建中间物，保留完整账本、冻结规则、登记和结果核验所需证据。实际push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261105T042212Z.json。

封存：6新金融配置/18成本场景，通过0、淘汰6。18新ID/36事件全部finish，34857旧保护文件不变。39旧原生成本路径仅只读审计，新原生策略重跑0。

原SMA本窗增加120个分钟NAV：49025→49145，累计34完整日。现金、单位、desired、成本和成交不变，65日spot上下文保留上一轮文件。single NAV13290→13412，累计330观察ID。

FEWM续2026-11-05T02:10:00Z→2026-11-05T04:10:00Z，累计249分钟，NAV135→257，累计9观察ID；1/2/3倍累计收益{'1': 0.0026564736000045386, '2': -0.0004410863999937398, '3': -0.003542272799994528}。L4 NAV6027→6149，累计153观察ID。四账户均保留各自原规则/本金/持仓/完整账本；本窗各自日目标、成交、资金费的实际新增数见current_window_event_verification.json，不复制或重复午夜事件。均不足长期资格，不作为稳定实盘盈利。

只读监控：9424研究行，9418旧完整行不变，10报价账户/255观察，gzip4313109字节。HTTP失败11次均留档；真实行情/账本/冻结规则/登记及核验必需证据保留，仅清理可重建中间文件。非强制push、远端完整tree/blob和解锁终态见.git/automation_proofs/20261105T042212Z.json。
