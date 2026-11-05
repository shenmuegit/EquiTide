本轮6个新组合通过0/6，淘汰6/6。连续370日walk-forward、ETH D/K两轴敏感性和1/2/3倍成本测试完成。3倍净收益12.912095%～15.911897%，完整连续回撤4.501608%～4.501608%。资格逐项见表与失败项；历史通过不代表独立前向或稳定实盘盈利。

事前固定BTC入场1250、3750独立银行，ETH4500/15000、D1/3/5×K250/500/750ppm。检验较高BTC实际敞口与ETH斜率时间/门槛的联合敏感性，完整保留近期失败可能；只补6个新D3/5组合，旧D1、原生银行和同N持有只读。已复用历史和既往选择，不能把全期正收益称稳健合格，不据本轮结果改批次/门槛。

完整读取27676登记事件/13716ID、306既往结论及三技能/README/OOS/freqtradeZIP。初始16项均有实际证据、缺0；此前独立研究定义9853，标实际9640，未标213。保留多重选择偏差，反复开发历史不是未触碰最终留出。

固定BTC入场1250、银行3750，ETH入场4500、银行15000，总18750；raw[1,1]相加完整银行，不归一化或重复乘20/80%资本份额。BTC名义占自身1/3、总6.666667%；ETH占自身30%、总24%。无NAV/数量/成本缩放、父订单、克隆、转移、再平衡或交叉保证金。

BTC ROC31/H4%/E1%固定；ETH contrarianROC5/H2%/E0.5%，有限归一化EWM24 beta23/25，D1/3/5与严格K0.025/0.05/0.075%。仅新开仓/反手检查趋势及V10样本logvol上限4.5%，同向现仓保留；失败反转先平旧仓、不新开。所有信号只读过去完整收盘，下一UTC00:01OPEN，原生数量按N/priorclose/LOT取整，终点计成本平仓。

26旧结果/13原生银行/39成本路径只读恢复完整净值与SHA，0原生策略重跑；6个新D3/5父组合/18场景全部先reserve。3个旧D1组合canonical状态/criteria/sensitivity不改，当前D/K诊断单列。所有候选逐格匹配旧同N1250、同本金BTC+ETH4500持有及现金0%；另有9个旧BTC1000、相同ETHD/K基线，BTC预算有意不同。

共同事件轴545013点，2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30完整折+10日尾折；近期40日从day330真实状态延续、8×5日，无折间重开。无拟合或标签，purge0，33日上下文覆盖最大32日信号。整体DD从完整连续分钟/事件NAV计算，不平均组件Sharpe或回撤。

敏感性D/K索引半径1含中心，父组合与只读ETH源均两轴，所有9格×3成本及72相邻边、最高Sharpe边界/cliff完整报告。依赖邻域只是描述性诊断，不作DSR/PBO显著性，不据结果扩网格或放宽门槛。

费用5bp/边，半价差1bp、滑点2bp，冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行费用和资金费支出、收入不放大；实际结算ns/rate/mark/当时持仓，不把费率用于信号。保留LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押及1%闭合小时不利mark风险代理。线性永续无现货借币；缺L2/TCA/完整历史层级/最大量/逐tick强平与真实容量证明。

资格固定：每成本全期净正；1倍>=9/12正月；每成本近期净正且>=6/8正五日折；3倍整体DD<=25%；邻域3倍正和严格近期合格率均>=60%；>=4原生平仓；毛参考PnL+资金费/执行成本>=2.5；0现金/订单/风险代理违规、终点flat、>=180日。

|新组合|D|K|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|lagmix370_parent_BTCN1250_ETHentryGateK250ppm_D3|3|0.00025|16.106395|14.509002|12.912095|4.501608|12|5/5/5|rejected|
|lagmix370_parent_BTCN1250_ETHentryGateK500ppm_D3|3|0.0005|16.106395|14.509002|12.912095|4.501608|12|5/5/5|rejected|
|lagmix370_parent_BTCN1250_ETHentryGateK750ppm_D3|3|0.00075|16.106395|14.509002|12.912095|4.501608|12|5/5/5|rejected|
|lagmix370_parent_BTCN1250_ETHentryGateK250ppm_D5|5|0.00025|19.290643|17.601137|15.911897|4.501608|12|5/5/5|rejected|
|lagmix370_parent_BTCN1250_ETHentryGateK500ppm_D5|5|0.0005|19.290643|17.601137|15.911897|4.501608|12|5/5/5|rejected|
|lagmix370_parent_BTCN1250_ETHentryGateK750ppm_D5|5|0.00075|17.423493|15.784312|14.145496|4.501608|12|5/5/5|rejected|

实际失败项：{'lagmix370_parent_BTCN1250_ETHentryGateK250ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN1250_ETHentryGateK500ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN1250_ETHentryGateK750ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN1250_ETHentryGateK250ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN1250_ETHentryGateK500ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN1250_ETHentryGateK750ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

11CSV保留18新成本场景、234月/尾折、144近期折、6678日NAV、27父网格/27旧ETH网格、27旧BTC1000匹配D/K基线场景、72相邻边、27同N1250持有/现金比较、39旧原生成本路径与10资金配置；全部正负结果永久保留。

原SMA65与single从Nov4_22:30续至Nov5_00:30，跨各自00:01日决策；single使用自己的实际00资金费。SMA补齐真实现货65日与既有64日逐行重叠、分钟日线收盘核对，保留原Float单位及10bp手续费，不把perp日线/LOT或FEWM状态套入。旧银行/仓位/成本/完整NAV前缀延续，不在窗口末强平。新完整SMA日线上下文为本轮forward_inputs.json.gz。

FEWM从自己的首窗pointer/完整账本继续00:10→02:10，累计129分钟，原冻结BTC3750/N750、ETH15000/N4500、D1/K0.0005与Nov5至May4计划不变；不重复首笔订单、不重新下载33日warmup、不采纳本轮BTC1250。旧L4也单独续00:10→02:10，自己的午夜资金费/日决策已在上轮完成，不重复。全部为真实闭合数据的延迟shadow，独立于十策略真实报价观察；partial不作180日/六折或稳定盈利结论，短窗年化不解释。

2026-11-05UTC实际读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对fundingTime/fundingRate/markPrice及单位。实际数值只用真实parquet/API；文档不提供盈利结论。原始行情保留忽略data，提交轻量账本/上下文/URL/SHA和复现代码，不提交大行情。

同main排他锁内完成登记、只读snapshot与monitor检查，snapshot不执行回测或成交，不改账户/本金/规则，不重部署网页或新建定时任务。只清理可重建中间物，保留完整账本、冻结规则、登记和结果核验所需证据。实际push、完整远端tree/blob与解锁终态见.git/automation_proofs/20261105T022141Z.json。

封存：6新金融配置/18成本场景，历史通过0、淘汰6。18新ID/36事件全部finish，34556旧保护文件不变。0原生策略重跑；39旧成本路径资金费43290条、成交1650笔仅只读审计。

原SMA跨午夜完成每资产1次、成本副本共6个日目标，0新模拟成交；NAV48904+121=49025，累计34完整日，完整真实65日spot上下文为本轮forward_inputs.json.gz。single自己的午夜资金费6条、日目标6个、新模拟成交3笔；NAV13163+127=13290，累计327ID。资金费在00:01目标之前以自己的旧持仓入账，不复制其他账户。

FEWM续2026-11-05T00:10:00Z→2026-11-05T02:10:00Z，累计129分钟，NAV13+122=135，累计6个实际观察ID。本窗日目标0、模拟成交0、资金费0；组合1/2/3倍成本收益{'1': -0.01567952639999204, '2': -0.01877708640000142, '3': -0.02187827280001331}、完整回撤{'1': 0.029382141230238634, '2': 0.029383051280773564, '3': 0.029383962453166657}。初始账本和13点NAV严格保留，无首笔订单重下/现金重开/33日warmup重取。

旧L4续2026-11-05T00:10:00Z→2026-11-05T02:10:00Z，本窗日目标0、模拟成交0、资金费0，NAV5905+122=6027，累计150ID。上轮00资金费与00:01决策均未重复。四账户仍是partial，均不作180日/六折或稳定盈利结论。

监控通过：9418研究行，9412旧完整行不变，10报价账户/254观察，gzip4311438字节。预留前仅校正继承的组件复用说明标志并重新绑定，无策略/参数/权重/边界/门槛变化，无实际金融或观察重跑。HTTP失败1次均留档；完整账本、冻结规则、登记与真实原始数据保留，可重建中间物已核验。真实非强制push、远端完整tree/blob及解锁终态见.git/automation_proofs/20261105T022141Z.json。
