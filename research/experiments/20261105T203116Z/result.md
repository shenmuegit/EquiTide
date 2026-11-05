本轮9个新组合通过2/9、淘汰7/9。9定义/27成本场景实际完成，13个原生银行/39成本路径只读，0原生策略重跑。连续370日walk-forward、D/K两轴敏感性和1/2/3倍成本压力测试完成；组合3倍净收益10.084488%～14.089764%，完整整体回撤3.549877%～4.744853%。不把正收益回测称独立前向或稳定实盘盈利。

事前固定BTC入场750、3750独立银行，ETH4500/15000、D6/7/8×K5000/10000/20000ppm。检验BTC预算750与ETH固定4500的实际敞口与ETH斜率时间/门槛的联合敏感性，完整保留近期失败可能；补齐全部9个新D/K组合；原生银行、BTC500对照和同N持有只读。已复用历史和既往选择，不能把全期正收益称稳健合格，不据本轮结果改批次/门槛。

完整读取28264登记事件/14010ID、315既往结论、三技能/README/OOS/freqtradeZIP。初始16项均有实际证据、缺0；此前独立研究定义9949、标实际9736、未标213。保留多重选择偏差，重复开发历史不是未触碰最终测试集。

BTC固定ROC31/H4%/E1%、入场750/银行3750；ETH固定contrarianROC5/H2%/E0.5%、有限归一化EWM24 beta23/25、入场4500/银行15000。本轮仅变D6/7/8×严格K0.5/1/2%。斜率M(i,24)/M(i-D,24)-1只使用过去完整收盘；仅新开仓/反手检查趋势和V10样本logvol上限4.5%，同向现仓保留；失败反转先平旧仓、不新开。下一UTC00:01 OPEN执行，原生N/priorclose/LOT下取整；终点计成本平仓。

raw[1,1]相加完整独立银行，总本金18750，不归一化、不重复乘20/80%资本份额。BTC名义占自身20%、总4%；ETH占自身30%、总24%。所有13个原生银行均已有真实结果，按原数量/LOT/成交量冲击/资金费/风险账本恢复净值并核对SHA；23旧结果/39成本路径只读，0原生策略或订单重跑，不缩放旧NAV/数量/成本，不产父订单、转移、再平衡或交叉保证金。

全部9新组合先reserve后计算，分8+1预留/finish。旧BTC500对照逐D/K匹配完全相同ETH子账户与本金，BTC预算750与500有意不同；原canonical状态/criteria/sensitivity不改。9个同本金/预算BTC750+ETH4500持有组合及现金0%只读。

2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30日完整折+10日尾折；近期40日继承day330实有状态、8×5日，无折间重开。共同事件轴545013点。无拟合或标签，purge0；最大S+D32与BTC32个过去收盘在33日上下文内。整体回撤从完整连续分钟/事件NAV计算，不平均组件Sharpe/收益/回撤。

敏感性D/K索引半径1含中心，父组合与只读原生分别完整9格×3成本，保留Sharpe、Calmar、整体DD、全期/近期收益、72条邻接边、描述性cliff与最高Sharpe边界。不得依据新结果扩网格或放宽门槛；未把依赖邻域当DSR/PBO显著性。

费用每边5bp、半价差1bp、滑点2bp；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本和资金费支出，资金费收入不放大；真实结算ns/rate/mark/当时持仓，费率不作信号。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理均核对。线性永续无现货借币；缺历史L2/TCA、完整层级/最大量/逐tick强平证据，未证明真实容量。

门槛固定：每成本全期净正；1倍>=9/12正月；每成本近期净正且>=6/8正五日折；3倍整体DD<=25%；邻域3倍正收益及严格近期合格率均>=60%；>=4原生平仓；毛参考PnL+资金费/执行成本>=2.5；0现金/订单/风险代理违规、终点flat、>=180日。

|新配置|类型|D|K|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|lagmix370_parent_BTCN750_ETHentryGateK5000ppm_D6|parent|6|0.005|17.101856|15.595581|14.089764|4.004215|12|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK10000ppm_D6|parent|6|0.01|13.545191|12.226132|10.907413|4.744853|12|6/6/6|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK20000ppm_D6|parent|6|0.02|12.349551|11.371162|10.393009|3.595777|11|6/6/6|passed|
|lagmix370_parent_BTCN750_ETHentryGateK5000ppm_D7|parent|7|0.005|15.651178|14.189981|12.729243|4.744853|12|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK10000ppm_D7|parent|7|0.01|12.814195|11.449124|10.084488|4.744853|11|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK20000ppm_D7|parent|7|0.02|13.282086|12.181708|11.081672|3.549877|11|6/6/6|passed|
|lagmix370_parent_BTCN750_ETHentryGateK5000ppm_D8|parent|8|0.005|15.651178|14.189981|12.729243|4.744853|12|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK10000ppm_D8|parent|8|0.01|14.681344|13.265948|11.850888|4.744853|12|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK20000ppm_D8|parent|8|0.02|14.741997|13.511372|12.281089|3.610793|12|6/6/6|rejected|

实际失败项：{'lagmix370_parent_BTCN750_ETHentryGateK5000ppm_D6': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK10000ppm_D6': ['local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK20000ppm_D6': [], 'lagmix370_parent_BTCN750_ETHentryGateK5000ppm_D7': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK10000ppm_D7': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK20000ppm_D7': [], 'lagmix370_parent_BTCN750_ETHentryGateK5000ppm_D8': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK10000ppm_D8': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK20000ppm_D8': ['local_recent6of8_allcost_gte60pct']}。

11CSV保留27新成本场景、351月/尾折、216近期折、10017日NAV、27父/27原生网格、27旧对照成本场景、72相邻边、27匹配持有/现金比较、39旧原生成本路径、10资金配置。全部正负结果保留；归档原生账本/逐决策、独立Fraction信号和Decimal账本重建、完整净值SHA可核验。

原SMA65/single各自Nov5_16:30→18:30，L4/FEWM各自18:10→20:10，三个永续账户均从各自已结算16资金费的旧账本续接。本窗只追加真实闭合mark/小时风险核验，不重复16或08结算。保留原cash/units/desired/cost/risk/完整NAV前缀，不重开、无新日目标或成交。SMA65日spot完整上下文仍20261105T022141Z/forward_inputs.json.gz。FEWM累计1209分钟/33观察ID，固定BTC3750/N750、ETH15000/N4500、D1/K.0005，不采纳本轮BTC750新组合（原FEWM自身规则/预算保持）。预先声明只复用公开市场响应：single仅复用L4元数据/时间，其自身分钟/hour/funding另取；FEWM同窗公共数组及provenance相同，但自己的账本/资金费/完整NAV独立计算。均为未成熟延迟shadow，不能冒充180日/六折或十策略真实报价模拟业绩。

2026-11-05UTC实际读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对资金费字段与单位；返回行情/资金费只取真实parquet/API。缺真实盘口/TCA时成本仍为明确模型。

同main排他锁内完成登记、只读snapshot与monitor检查；不回测监控、不造模拟成交、不改冻结规则/本金/持仓，不重部署网页或新增定时任务。仅清理可重建中间物；完整账本、冻结规则、登记及核验必要证据、原始warmup/行情均保留。实际push、远端完整tree/blob和解锁终态留.git/automation_proofs/20261105T203116Z.json。

封存：9新组合/27成本场景，组合通过2、组合淘汰7。21新ID/42事件全部finish，37408旧保护文件保持；全部原生组件均只读复用，39旧成本路径核验、0原生策略重跑。

SMA NAV49985→50105，120分钟mark；single NAV14270→14392，本窗新资金费0条成本副本，以真实时间/费率/mark和各自旧持仓独立入账。L4 NAV7007→7129，本窗新资金费0；FEWM NAV1115→1237，累计1209分钟/33观察ID，本窗新资金费0，收益{'1': 0.21310940645113963, '2': 0.21001184645113025, '3': 0.20691066005114056}。三个永续账户均从各自post16账本续接，不重复16或08；四账户无日目标或新成交，不重置现金、本金、持仓、规则或完整NAV前缀。

仅复用真实公开行情/元数据/服务器时间，未复制任何另一账户的状态、现金、单位、交易、资金费金额或净值。SMA完整65日spot上下文保留20261105T022141Z。全部partial，不作180日/六折或稳定实盘盈利结论。

只读监控9517行，原9508行完整不变，10报价账户/263观察；gzip4345886字节。实际HTTP失败0次留档。全部参数/金额/权重/边界/门槛预登记前固定，无实际结果重复计算。完整账本/冻结规则/登记/真实输入及核验必需证据保留，清理只限可重建中间物；非强制push/完整远端tree/blob与解锁终态见.git/automation_proofs/20261105T203116Z.json。
