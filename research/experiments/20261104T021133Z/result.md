本轮无合格新候选：9项全部rejected。三项验证均已实际执行：连续walk-forward完成；参数敏感性未达近期邻域门槛；1/2/3倍成本下27/27全期净收益为正。三倍收益7.2243%～13.4878%，连续整体回撤2.7797%～5.4892%。2项少于9个盈利完整月，9项均因三倍近期只有4–5/8个盈利五日折、邻域严格近期合格比例0%淘汰。历史正收益不代表稳定实盘盈利。

BTC/ETH 原生银行资金与敞口组合验证

此前宽窄ETH参数和更大BTC银行组合均未通过近期稳健性。本轮固定总本金18750和BTC3750/ETH15000银行资本，将BTC实际预算750降至500，ETH仍4500；复用13个实际原生账本，raw[1,1]，检验ETH SMA32 L3/5/7×H1.5/2/2.5%九格的近期支持是否改善。九个新父组合先reserve，零新原生信号/成交、零旧NAV/数量缩放，旧750对照资格和多重历史选择偏差保留。

读取完整26900事件/13328ID、294份既往结论；初始16实际证据完整，缺结果0。此前研究定义9696，标实际9483、未标213；不把全部登记当全部回测，历史多重选择偏差保留。

事前固定新的资金/敞口组合：完整BTC3750/N500银行+完整ETH15000/N4500银行，raw权重[1,1]，总本金18750，资本份额20/80%、初始名义敞口份额2.6666666667/24%。旧组合BTC3750/N750+ETH15000/N4500总本金18750、资本份额20/80%、名义4/24%。总本金及两银行资本不变，只将BTC实际预算750降至500；收益/DD差异反映敞口组合变化，不能称新信号alpha。没有归一化、缩放旧NAV/数量、平均Sharpe/DD、调仓/跨银行转移/交叉保证金或父订单。

BTC源政策固定L31/H4%/退出E1%，ETH源固定SMA32门槛、快反转L3/5/7×对称H1.5/2/2.5%、E0.5%、entry-onlyV10/cap4.5%。所有13个原生组件均有真实既往账本；本轮零新原生信号/成交，仅先reserve九个组合后对齐共同事件轴相加完整美元净值。旧20/80组合九格原rejected资格不改；同资本/同预算常多持有基准亦已有实际结果，只读复用，现金0%另列。

Walk-forward：2025-10-19UTC00:01→2026-10-24UTC00:01，连续370日、12×30日完整折+10日尾折，逐折不重置持仓/现金。整体DD来自完整分钟/事件净值，近期40日继承day330状态、8×5日。固定源规则无训练/标签，purge0；所有源过去完整信号在下一00:01原生OPEN执行并于终点计成本平仓。这里是多轮复用的开发历史，不是未触碰最终测试或独立未来。

各组件原生执行预算已实际测试，按真实过去收盘/LOT数量、原5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20quoteADV)，1/2/3倍执行支出和资金费支出、收入不放大。实际settlement ns/rate/mark/heldq；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理完整复核。永续空头无现货借币，不虚构借币费。缺盘口/TCA、完整历史层级/最大量、逐tick强平与容量证明，不把回测正收益称稳定实盘盈利。

沿用失败门槛：各成本全年净正、1倍>=9/12正完整月；各成本近期总收益正且>=6/8正5日折；3倍整体DD<=25%；L/H索引半径1含中心邻域，3倍正与严格近期合格比例均>=60%；>=4底层平仓、毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat、>=180日。不在看到结果后改门槛或扩格。

|新组合|L|H比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|bankmix370_BTC500_ETHL3_H150bp|3|0.015|12.101703|10.409752|8.717458|5.489160|8|5/5/5|rejected|
|bankmix370_BTC500_ETHL3_H200bp|3|0.02|13.841430|12.287611|10.733729|5.051174|8|5/5/5|rejected|
|bankmix370_BTC500_ETHL3_H250bp|3|0.025|12.992389|11.771143|10.549672|3.894822|9|5/5/5|rejected|
|bankmix370_BTC500_ETHL5_H150bp|5|0.015|16.471450|14.979274|13.487753|3.329941|11|6/6/5|rejected|
|bankmix370_BTC500_ETHL5_H200bp|5|0.02|14.730559|13.458827|12.187202|3.297605|11|6/6/5|rejected|
|bankmix370_BTC500_ETHL5_H250bp|5|0.025|9.188937|8.206673|7.224346|2.788370|10|5/5/4|rejected|
|bankmix370_BTC500_ETHL7_H150bp|7|0.015|14.386012|13.218893|12.051881|3.445853|11|5/5/5|rejected|
|bankmix370_BTC500_ETHL7_H200bp|7|0.02|13.644227|12.536263|11.428281|3.461840|11|5/5/5|rejected|
|bankmix370_BTC500_ETHL7_H250bp|7|0.025|12.817051|11.834117|10.851260|2.779653|11|4/4/4|rejected|

新组合通过0、淘汰9，逐项失败{'bankmix370_BTC500_ETHL3_H150bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC500_ETHL3_H200bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC500_ETHL3_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC500_ETHL5_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC500_ETHL5_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC500_ETHL5_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC500_ETHL7_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC500_ETHL7_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC500_ETHL7_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。正负场景/折完整保存；同网格NAV别名和与旧配置实际BTC预算差异另存，不把重复/现金稀释当独立收益来源。

10CSV保存27新场景、351月/尾折、216近期折、10017日NAV、九格L/H面、27旧配置场景、36相邻边、27匹配持有/现金比较、39只读原生成本路径、10资金分配。相邻cliff为依赖样本描述性诊断，不是DSR/PBO显著性或新增裁定条件；边界按真实L/H端点核对。

一手[SMA论文入口](https://mebfaber.com/white-papers/)和[Binance USD-M市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)于2026-11-04UTC访问。仅参考均线趋势估计器与实际字段，不能移植原10月长仓论文收益。所有价格/资金费/mark/约束文件字节/SHA和组件spec/report/archive版本见plan/data_manifest。

本轮single及原SMA65续Nov3UTC22:30→Nov4UTC00:30，分别按各自冻结规则处理00:01日决策；single另按真实00结算时刻/rate/mark及自身持仓计算资金费，不复制L4金额。SMA65采用原Float日决策与65日完整上下文、过去20日成本及实际00:01执行参考。L4续Nov4UTC00:10→02:10，其00资金费和日决策已由上轮处理，完整前缀保留且不重复结算。所有本金、冻结规则、风险和完整NAV前缀保持，partial不冒充180日/六折，旧shadow与十策略报价模拟分开。

本轮single索引直接读取common元数据，不依赖省略的原生engine。所有实际HTTP/命令终态如实保存；只读文档旧地址不可访问后已改读官方当前目录，读取诊断的语法错误修复记录保留。不重跑已完成的观察/金融结果，不为监控改历史。32来源文件在首个金融reserve前绑定，原生交易函数无新调用，合成检查验证完整18750银行资本、非平均DD、错误旧BTC缩放及错位事件轴拒绝。

本轮仅清理可重建中间物，保留完整源/账户账本、冻结规则、登记、全部正负结果、原始短窗/失败响应及必要代码。同main排他锁更新只读监控并非强制push，远端完整tree/哈希、实际终态和解锁凭据见.git/automation_proofs/20261104T021133Z.json。

封存：9新组合/27成本场景逐项finish，通过0、淘汰9；0新原生信号/订单，13旧原生/39成本账本只读复核。旧资金费43290条、成交1638笔均是旧源记录。新组合NAV14715351点，独立核验{'funding': 43290, 'fills': 1638, 'rejects': 0, 'metric_checks': 924, 'margin_checks': 163593}，无父订单。18新ID/36追加事件，31031旧保护文件不变。

新旧组合均为本金18750、银行资本3750/15000，BTC实际预算500对旧750，ETH4500不变。matched_hold采用同本金和预算500/4500的既有真实账本。收益/DD变化属于实际敞口分配效应，不称新信号alpha；本轮calendar及causality文字已在首个reserve前修正为9父组合、0新原生、L3/5/7。

原SMA续2026-11-03T22:30:00Z至2026-11-04T00:30:00Z，NAV47463+121=47584，累计47549分钟；实际日决策2、逐成本新成交0。single续2026-11-03T22:30:00Z至2026-11-04T00:30:00Z，午夜日事件1、原规则决策6、新成交0，NAV11690+127=11817，累计291ID，真实资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0.09293004000000000000000000000', 'amount_usdt': '0.09293004000000000000000000000', 'mark': '77441.70000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0.09293004000000000000000000000', 'amount_usdt': '0.09293004000000000000000000000', 'mark': '77441.70000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0.09293004000000000000000000000', 'amount_usdt': '0.09293004000000000000000000000', 'mark': '77441.70000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2273.85000000', 'rate': '0.00008833'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2273.85000000', 'rate': '0.00008833'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2273.85000000', 'rate': '0.00008833'}]。L4续2026-11-04T00:10:00Z至2026-11-04T02:10:00Z，新日事件0、资金费0、成交0，NAV4554，累计114ID。所有原账户完整NAV前缀/规则/本金保留，partial不冒充180日/六折。

监控通过：9264研究行，9255旧完整行不变；10报价账户/242观察，gzip4232730字节。必要实际命令均退出0；公共HTTP/传输失败1次及初始只读访问/诊断错误如实留档。0已完成回测或观察重跑。清理0真实结果/账本，零可重建缓存遗留。

全部正负折、连续整体DD、spec/report/archive/数据/源码哈希、真实短窗与失败证据保留。main非强制push、远端完整tree/blob及实际终态/解锁凭据见.git/automation_proofs/20261104T021133Z.json。
