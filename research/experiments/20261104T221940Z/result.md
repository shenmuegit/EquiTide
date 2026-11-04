本轮6个新组合通过0/6，淘汰6/6。连续370日walk-forward、ETH D/K两轴敏感性和1/2/3倍成本测试完成。3倍净收益范围12.323364%～15.323165%，完整连续回撤4.004215%～4.004215%。资格逐项见表和失败项；历史通过也不代表独立前向或稳定实盘盈利。

固定BTC真实入场N750，ETH有限EWM斜率间隔D1/3/5与门槛K250/500/750ppm联合，检验较长斜率时间差是否改善近期折一致性或反而延迟。上轮低BTC金额邻域未过，不能靠正收益下结论；本轮只补6个未测试父组合，3个旧D1组合与全部组件/匹配基准只读。先定完整批次/门槛再估值，不事后增减；仍为反复使用的开发历史，非独立最终/未来证据。

读完27574事件/13665ID、304既往结论及三技能/README/OOS/freqtradeZIP。初始16项缺实际结果0。此前独立研究定义9843，标实际9630，未标213。保留多重选择偏差，重复开发历史非未触碰最终留出。

固定BTC入场750、资金银行3750；ETH入场4500、银行15000，总18750，raw[1,1]相加完整银行，不归一化，不重复乘20/80%资本份额。BTC名义占自身20%、总4%；ETH占自身30%、总24%。无NAV/数量/成本缩放、父订单、克隆、转移、再平衡或交叉保证金。

BTC ROC31/H4%/E1%固定。ETH contrarianROC5/H2%/E0.5%，有限归一化EWM24 beta23/25、斜率D1/3/5、严格门槛K0.025/0.05/0.075%。只在新开仓/反手检查趋势和V10样本logvol上限4.5%，同向现仓保留；失败反转先平旧仓、不新开。原生数量按过去完整收盘/LOT取整，下一UTC00:01OPEN，终点计成本平仓。13旧原生银行/39成本路径只读恢复并核对完整SHA，0原生策略重跑；仅计算6个新父组合/18场景，3个旧D1组合原canonical资格不变。

共同分钟/事件轴545013点。时间2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30完整折+10日尾折；近期40日从day330实际账本延续、8×5日，无折间现金重开。无模型拟合/标签，purge0，33日上下文覆盖最大32日信号。逐折及完整连续NAV的整体DD、Sharpe/Calmar均报告，不平均组件指标。

敏感性D/K索引半径1含中心，父组合和旧ETH组件均两轴。9格各3成本，最高Sharpe边界和72相邻边描述性cliff全部留档；不是DSR/PBO统计显著性，不据结果扩批或改门槛。旧D1状态/criteria/sensitivity保留，新邻域诊断单列。

费用5bp/边、半价差1bp、滑点2bp、冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。1/2/3倍执行和资金费支出、收入不放大，资金费按实际ns/rate/mark/当时持仓；持有/现金0%逐格同资金和同N750匹配。保留LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押和1%闭合小时不利mark风险代理。线性永续无现货借币；缺L2/TCA/完整层级/最大量/逐tick强平/容量证明。

冻结资格不变：所有成本全期净正；1倍>=9/12正月；每成本近期净正且>=6/8正五日折；3倍连续整体DD<=25%；邻域3倍正及严格近期合格率均>=60%；>=4原生平仓；毛参考PnL+资金费/执行成本>=2.5；0现金/订单/风险代理违规、终点flat、>=180日。

|新组合|D|K|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|lagmix370_parent_BTCN750_ETHentryGateK250ppm_D3|3|0.00025|15.234707|13.778757|12.323364|4.004215|11|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK500ppm_D3|3|0.0005|15.234707|13.778757|12.323364|4.004215|11|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK750ppm_D3|3|0.00075|15.234707|13.778757|12.323364|4.004215|11|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK250ppm_D5|5|0.00025|18.418955|16.870891|15.323165|4.004215|12|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK500ppm_D5|5|0.0005|18.418955|16.870891|15.323165|4.004215|12|5/5/5|rejected|
|lagmix370_parent_BTCN750_ETHentryGateK750ppm_D5|5|0.00075|16.551805|15.054067|13.556765|4.004215|11|5/5/5|rejected|

实际失败项：{'lagmix370_parent_BTCN750_ETHentryGateK250ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK500ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK750ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK250ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK500ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'lagmix370_parent_BTCN750_ETHentryGateK750ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。

11CSV保存18新成本场景、234月/尾折、144近期折、6678日NAV、27父网格/27旧ETH原生网格、27旧N500匹配D/K基线场景、72相邻边、27同N750持有/现金比较、39旧原生成本路径、10资金配置。所有正负结果都保留。

原SMA65/single续Nov4UTC18:30→20:30，原L4续20:10→22:10，无新日决策时完整保留规则/资金/数量/成本/risk/context/NAV前缀；资金费只按本窗真实记录，不重复16:00。SMA日线仍为20261104T021133Z完整上下文。延迟shadow与十策略真实报价观察分开，partial不作180日/六折资格。

R20的独立FEWM前向计划仍从2026-11-05UTC00:01开始、2027-05-04UTC00:01结束，N750/K0.0005/D1规则和哈希不改。本轮仅只读status，0新账户/HTTP/登记/前向结果；不因本轮历史结果采纳D3/5或修改冻结计划。起点后真实闭合首窗仍须独立预登记、真实warmup和新策略账本审计。

2026-11-04UTC实际读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对fundingTime/fundingRate/markPrice和数量/价格单位。文档不提供盈利结论；实际数值来自已有真实parquet/API，源数据及spec/report/archive/code SHA随本轮保存。

同main排他锁内登记、只读snapshot/monitor核验后提交push；无新订单、重部署或定时任务。只清理可重建中间物，完整账本/冻结规则/登记/真实输入/失败留档。实际提交/完整远端tree/blob与解锁凭据在.git/automation_proofs/20261104T221940Z.json。

封存：6新金融配置/18成本场景逐项finish，组合通过0、淘汰6，0个新原生组件，通过0；持有对照全部只读。新原生决策0次、资金费0条、成交0笔；旧39成本账本资金费43290条、成交1650笔均是旧记录。独立审计{'funding': 43290, 'fills': 1650, 'rejects': 0, 'metric_checks': 798, 'margin_checks': 183201}，0父订单。15新ID/30追加事件，33993旧保护文件不变。

原SMA续2026-11-04T18:30:00Z至2026-11-04T20:30:00Z，NAV48664+120=48784，累计48749分钟。single续2026-11-04T18:30:00Z至2026-11-04T20:30:00Z，NAV12919+122=13041，累计321ID；本窗实际新增资金费[]。L4续2026-11-04T20:10:00Z至2026-11-04T22:10:00Z，NAV5656+122=5778，累计144ID，本窗资金费[]，不重复上轮08结算。三者新日决策/成交SMA 0/0、single 0/0、L4 0/0。原规则/本金与完整前缀保留，partial不冒充180日/六折，不采纳本批研究。

监控通过：9408研究行，9402旧完整行不变，10报价账户/252观察，gzip4308179字节。本轮必要正式管线均实际退出0。HTTP/传输失败0次全部保留；取得共用锁后写入，官方文档本轮读取成功，实际资金费字段/现金流已核验。0已完成金融/观察重跑，清理0真实结果/账本，零可重建缓存遗留。

全部正负折/逐变体、完整DD、spec/report/archive/数据/代码SHA、真实短窗及失败证据保留。main非强制push、完整远端tree/blob及实际终态/解锁凭据见.git/automation_proofs/20261104T221940Z.json。

原R20 FEWM前向计划本轮只读status实际退出0：仍waiting_for_planned_start，0网络/0写入/0登记，原计划/绑定/核心/执行器哈希不变；没有重复工程测试、创建账户或实际前向结果。6配置只形成3种不同完整三成本NAV组，D3三个K同路径、D5两个K同路径，不作独立alpha。下一L4窗口22:10→Nov5_00:10跨资金费和00:01日决策，必须用原账户自己的实际输入/仓位执行，不能复制新FEWM账户。
