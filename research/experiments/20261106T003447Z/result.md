本轮9个新组合通过6/9、淘汰3/9。9定义/27成本场景实际完成，13个原生银行/39成本路径只读，0原生策略重跑。连续370日walk-forward、D/K两轴敏感性和1/2/3倍成本压力测试完成；组合3倍净收益6.913837%～12.605815%，完整整体回撤1.961898%～5.018148%。不把正收益回测称独立前向或稳定实盘盈利。

此前BTC750与ETH4500组合在D6/7/8、K1/2/3%网格有历史通过，但存在边界与陡变。本轮事前固定BTC入场1000/银行3750、ETH4500/15000，检验更高BTC名义敞口是否改善组合近期一致性，也可能增加回撤或降低全期收益。9个D6/7/8×K1/2/3%新组合全部先reserve；原生银行全只读、不缩放NAV/数量/成本。逐D/K对照旧BTC750、同本金/N1000持有与现金，原门槛不变，全部正负结果留档。复用历史及多重选择不构成独立最终或未来证据。

完整读取28382登记事件/14069ID、317既往结论、三技能/README/OOS/freqtradeZIP。初始16项均有实际证据、缺0；此前独立研究定义9964、标实际9751、未标213。保留多重选择偏差，重复开发历史不是未触碰最终测试集。

BTC固定ROC31/H4%/E1%、入场1000/银行3750；ETH固定contrarianROC5/H2%/E0.5%、有限归一化EWM24 beta23/25、入场4500/银行15000。本轮仅变D6/7/8×严格K1/2/3%。斜率M(i,24)/M(i-D,24)-1只使用过去完整收盘；仅新开仓/反手检查趋势和V10样本logvol上限4.5%，同向现仓保留；失败反转先平旧仓、不新开。下一UTC00:01 OPEN执行，原生N/priorclose/LOT下取整；终点计成本平仓。

raw[1,1]相加完整独立银行，总本金18750，不归一化、不重复乘20/80%资本份额。BTC名义占自身26.666667%、总5.333333%；ETH占自身30%、总24%。所有13个原生银行均已有真实结果，按原数量/LOT/成交量冲击/资金费/风险账本恢复净值并核对SHA；23旧结果/39成本路径只读，0原生策略或订单重跑，不缩放旧NAV/数量/成本，不产父订单、转移、再平衡或交叉保证金。

全部9新组合先reserve后计算，分8+1预留/finish。旧BTC750对照逐D/K匹配完全相同ETH子账户与本金，BTC预算1000与750有意不同；原canonical状态/criteria/sensitivity不改。9个同本金/预算BTC1000+ETH4500持有组合及现金0%只读。

2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30日完整折+10日尾折；近期40日继承day330实有状态、8×5日，无折间重开。共同事件轴545013点。无拟合或标签，purge0；最大S+D32与BTC32个过去收盘在33日上下文内。整体回撤从完整连续分钟/事件NAV计算，不平均组件Sharpe/收益/回撤。

敏感性D/K索引半径1含中心，父组合与只读原生分别完整9格×3成本，保留Sharpe、Calmar、整体DD、全期/近期收益、72条邻接边、描述性cliff与最高Sharpe边界。不得依据新结果扩网格或放宽门槛；未把依赖邻域当DSR/PBO显著性。

费用每边5bp、半价差1bp、滑点2bp；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行成本和资金费支出，资金费收入不放大；真实结算ns/rate/mark/当时持仓，费率不作信号。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理均核对。线性永续无现货借币；缺历史L2/TCA、完整层级/最大量/逐tick强平证据，未证明真实容量。

门槛固定：每成本全期净正；1倍>=9/12正月；每成本近期净正且>=6/8正五日折；3倍整体DD<=25%；邻域3倍正收益及严格近期合格率均>=60%；>=4原生平仓；毛参考PnL+资金费/执行成本>=2.5；0现金/订单/风险代理违规、终点flat、>=180日。

|新配置|类型|D|K|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|uppermix370_parent_BTCN1000_ETHentryGateK10000ppm_D6|parent|6|0.01|14.013573|12.622690|11.232139|5.018148|12|6/6/6|passed|
|uppermix370_parent_BTCN1000_ETHentryGateK20000ppm_D6|parent|6|0.02|12.817933|11.767720|10.717735|3.747309|11|6/6/6|passed|
|uppermix370_parent_BTCN1000_ETHentryGateK30000ppm_D6|parent|6|0.03|8.189769|7.551612|6.913837|1.961898|10|5/5/5|rejected|
|uppermix370_parent_BTCN1000_ETHentryGateK10000ppm_D7|parent|7|0.01|13.282576|11.845682|10.409213|5.018148|11|5/5/5|rejected|
|uppermix370_parent_BTCN1000_ETHentryGateK20000ppm_D7|parent|7|0.02|13.750467|12.578266|11.406398|3.699500|11|6/6/6|passed|
|uppermix370_parent_BTCN1000_ETHentryGateK30000ppm_D7|parent|7|0.03|9.491815|8.591320|7.691129|4.825362|11|6/6/6|passed|
|uppermix370_parent_BTCN1000_ETHentryGateK10000ppm_D8|parent|8|0.01|15.149726|13.662506|12.175614|5.018148|12|5/5/5|rejected|
|uppermix370_parent_BTCN1000_ETHentryGateK20000ppm_D8|parent|8|0.02|15.210379|13.907930|12.605815|3.886201|12|6/6/6|passed|
|uppermix370_parent_BTCN1000_ETHentryGateK30000ppm_D8|parent|8|0.03|8.888705|7.948801|7.009202|4.825362|11|6/6/6|passed|

实际失败项：{'uppermix370_parent_BTCN1000_ETHentryGateK10000ppm_D6': [], 'uppermix370_parent_BTCN1000_ETHentryGateK20000ppm_D6': [], 'uppermix370_parent_BTCN1000_ETHentryGateK30000ppm_D6': ['recent40_six_of_eight_positive5d_all_costs'], 'uppermix370_parent_BTCN1000_ETHentryGateK10000ppm_D7': ['recent40_six_of_eight_positive5d_all_costs'], 'uppermix370_parent_BTCN1000_ETHentryGateK20000ppm_D7': [], 'uppermix370_parent_BTCN1000_ETHentryGateK30000ppm_D7': [], 'uppermix370_parent_BTCN1000_ETHentryGateK10000ppm_D8': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'uppermix370_parent_BTCN1000_ETHentryGateK20000ppm_D8': [], 'uppermix370_parent_BTCN1000_ETHentryGateK30000ppm_D8': []}。

11CSV保留27新成本场景、351月/尾折、216近期折、10017日NAV、27父/27原生网格、27旧对照成本场景、72相邻边、27匹配持有/现金比较、39旧原生成本路径、10资金配置。全部正负结果保留；归档原生账本/逐决策、独立Fraction信号和Decimal账本重建、完整净值SHA可核验。

原SMA65/single各自Nov5_20:30→22:30，只追加闭合mark；L4/FEWM各自Nov5_22:10→Nov6_00:10，先用各自旧持仓核算真实00资金费，再执行各自冻结规则00:01目标及允许的成交，随后追加mark并核验完整NAV/风险。不重开现金、不重复00或16/08结算、不复制另一账户现金流。SMA完整65日spot上下文仍20261105T022141Z。FEWM累计1449分钟/39观察ID，固定N750/4500、D1/K.0005，不采纳本轮BTC1000研究。预先只复用公开响应：single复用L4元数据/时间，自己取分钟/hour/funding；FEWM同窗公共数组及provenance相同，但账本、目标、成交、资金费、NAV各自独立计算。均为未成熟延迟shadow，不作180日/六折或十策略真实报价模拟业绩结论。

2026-11-06UTC实际读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对资金费字段与单位；返回行情/资金费只取真实parquet/API。缺真实盘口/TCA时成本仍为明确模型。

同main排他锁内完成登记、只读snapshot与monitor检查；不回测监控、不造模拟成交、不改冻结规则/本金/持仓，不重部署网页或新增定时任务。仅清理可重建中间物；完整账本、冻结规则、登记及核验必要证据、原始warmup/行情均保留。实际push、远端完整tree/blob和解锁终态留.git/automation_proofs/20261106T003447Z.json。

事前代表配置为D7/K2%、BTC入场1000/3750银行，非事后最高收益选择；其3倍净收益11.406398%、整体DD3.699500%，近期各成本6/8正折、严格近期邻域6/9。全部D/K网格仍有描述性Sharpe陡变，最高Sharpe部分在D边界，不能据此称独立稳健或稳定实盘盈利。新候选独立未来计划本轮尚未冻结/开户/观测，原四账户保持原规则。

初始16项口径保持：11个已恢复ID有正式实际报告，5个legacy-tested ID沿用原ZIP/walk-forward实际证据、原先缺失的result_available字段未重写。未把其他213个未标实际的研究定义或paper失败观察宣称全部有结果。

封存：9新组合/27成本场景，组合通过6、组合淘汰3。21新ID/42事件全部finish，38023旧保护文件保持；全部原生组件均只读复用，39旧成本路径核验、0原生策略重跑。

SMA NAV50225→50345，120分钟mark；single NAV14514→14636，本窗新资金费0条成本副本，以真实时间/费率/mark和各自旧持仓独立入账。L4 NAV7251→7378，本窗新资金费6；FEWM NAV1359→1486，累计1449分钟/39观察ID，本窗新资金费6，收益{'1': 0.20536246608811037, '2': 0.202264906088101, '3': 0.1991637196880891}。single从自身post16账本续接；L4/FEWM真实00资金费均先于各自原00:01日目标/成交，不重复00或16/08；SMA/single无新日目标/成交，L4/FEWM各有一次日决策事件，实际新成交分别3/0，按各自原规则和原账本核验，不重置现金、本金、持仓、规则或完整NAV前缀。

仅复用真实公开行情/元数据/服务器时间，未复制任何另一账户的状态、现金、单位、交易、资金费金额或净值。SMA完整65日spot上下文保留20261105T022141Z。全部partial，不作180日/六折或稳定实盘盈利结论。

只读监控9532行，原9523行完整不变，10报价账户/265观察；gzip4353731字节。实际HTTP失败0次留档。全部参数/金额/权重/边界/门槛预登记前固定，无实际结果重复计算。完整账本/冻结规则/登记/真实输入及核验必需证据保留，清理只限可重建中间物；非强制push/完整远端tree/blob与解锁终态见.git/automation_proofs/20261106T003447Z.json。
