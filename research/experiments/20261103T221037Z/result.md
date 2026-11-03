SMA32 慢门槛下快反转回看与入场阈值的联合验证

上一轮宽L3/5/7与H1.5/2/2.5%网格中，L5/H1.5与2%虽近期6/8，却因邻域支持33%/22%淘汰。本轮预设较近回看L4/5/6及交错阈值H1.25/1.75/2.25%，保持SMA32、E0.5%、V10/cap4.5%、真实资本/入场规模，检验更近参数区间的结果分布。九新原生+九新组合先reserve。窄网格由已见开发历史启发，局部合格也不替代旧宽网格失败、独立未来或广泛稳健性，旧L4/L5控制原rejected资格不改；不据本轮结果扩格或改门槛。

完整读取26770事件/13263ID、292份既往结论；初始16有原档实际证据、缺结果0。此前研究定义9669，标实际9456、未标213，不将全部登记当全部实际回测；大量反复历史研究存在多重选择偏差。

事前固定较近快反转 L4/5/6 日×交错对称入场 H1.25/1.75/2.25%，SMA32、退出E0.5%、entry-onlyV10/cap4.5%固定。r=C[i−1]/C[i−1−L]−1；r>H做空、r<−H做多，入场等号不触发。否则实际多仓只在r<E保留、空仓只在r>−E保留，退出等号平仓。慢门槛为sign(C[i−1]/mean(C[i−32:i])−1)，包含最新完整收盘，零/相反方向flat；仅对新增/反转仓应用波动门槛，原方向仓位不因单独高波动退出。

九个新ETH原生各本金15000/N4500；九个新组合持有完整BTC3750/N750旧银行+对应ETH15000/N4500新银行，raw[1,1]、总本金18750、资金份额20/80%、名义入场占比4/24%。保持原权重，不归一化、不缩放旧净值/真实数量、不平均收益/Sharpe/DD、不跨银行调仓/交叉保证金或转移，0父订单。三项旧SMA32/E0.5%控制L5/H1.5%、L5/H2%、L4/H2%在网格外只读；预定主控制是上轮事前中心L5/H2%。三者原rejected资格及旧宽网格支持33%/22%失败不改，不能混入本轮局部L/H邻域。较窄网格由已见结果启发，即使本轮局部通过也不代替宽网格或独立未来验证。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日，12×30日完整折+10日尾折；逐折不重置现金/仓位，整体DD来自完整分钟/事件OOS净值。近期40日承接day330实际状态，8×5日。固定规则无拟合/标签、purge0、事前33日线足够SMA32；下一UTC00:01原生OPEN执行，数量按过去完整收盘/LOT算，反手先平后开，终点计成本平仓。属于反复使用的开发历史，不是未触碰最终测试或独立未来验证。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍放大执行和资金费支出，资金费收入不放大；实际settlement ns/rate/mark/heldq。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark风险代理；永续空头无需现货借币，不虚构借币费用。同资本/N750/4500持有和现金0%对照只读。缺盘口/TCA、历史完整保证金层级/最大量、逐tick强平和容量证明。

固定失败门槛：各成本全年净正；1倍至少9/12正完整月；近期各成本总收益正且>=6/8正5日折；3倍整体DD<=25%；含中心L/H索引半径1邻域，3倍正和严格近期合格比例均>=60%；>=4底层平仓；毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规，终点flat、至少180日。全部18项按同一事前标准裁定，不据结果增格/改门槛。

|新配置|scope|L日数|H比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|smalocal370_ETH_L4_H125bp_S32_E5000ppm|native|4|0.0125|13.363472|11.592183|9.819686|5.213868|9|3/3/3|rejected|
|smalocal370_ETH_L4_H175bp_S32_E5000ppm|native|4|0.0175|12.758285|11.163633|9.567915|5.140634|10|3/3/3|rejected|
|smalocal370_ETH_L4_H225bp_S32_E5000ppm|native|4|0.0225|16.028672|14.591484|13.153759|3.490012|9|3/3/3|rejected|
|smalocal370_ETH_L5_H125bp_S32_E5000ppm|native|5|0.0125|18.064269|16.355409|14.647284|4.345180|10|3/3/3|rejected|
|smalocal370_ETH_L5_H175bp_S32_E5000ppm|native|5|0.0175|15.950498|14.412045|12.874071|3.714541|10|3/3/3|rejected|
|smalocal370_ETH_L5_H225bp_S32_E5000ppm|native|5|0.0225|10.958612|9.792493|8.626311|4.550421|10|2/2/2|rejected|
|smalocal370_ETH_L6_H125bp_S32_E5000ppm|native|6|0.0125|16.256788|14.569987|12.884041|4.092142|9|3/3/3|rejected|
|smalocal370_ETH_L6_H175bp_S32_E5000ppm|native|6|0.0175|13.883810|12.412378|10.941414|4.278812|9|2/2/2|rejected|
|smalocal370_ETH_L6_H225bp_S32_E5000ppm|native|6|0.0225|12.564511|11.252636|9.941425|4.102225|9|2/2/2|rejected|
|smalocal370_parent_BTC750_ETHL4_H125bp|parent|4|0.0125|11.819272|10.209198|8.598167|4.697781|10|5/5/5|rejected|
|smalocal370_parent_BTC750_ETHL4_H175bp|parent|4|0.0175|11.335122|9.866359|8.396750|4.639073|10|5/5/5|rejected|
|smalocal370_parent_BTC750_ETHL4_H225bp|parent|4|0.0225|13.951432|12.608639|11.265425|3.039655|10|5/5/5|rejected|
|smalocal370_parent_BTC750_ETHL5_H125bp|parent|5|0.0125|15.579910|14.019779|12.460246|3.987775|11|6/6/6|rejected|
|smalocal370_parent_BTC750_ETHL5_H175bp|parent|5|0.0175|13.888893|12.465088|11.041675|3.478553|11|6/6/6|rejected|
|smalocal370_parent_BTC750_ETHL5_H225bp|parent|5|0.0225|9.895384|8.769447|7.643467|4.211768|10|5/5/5|rejected|
|smalocal370_parent_BTC750_ETHL6_H125bp|parent|6|0.0125|14.133925|12.591442|11.049650|3.845088|10|5/5/5|rejected|
|smalocal370_parent_BTC750_ETHL6_H175bp|parent|6|0.0175|12.235543|10.865355|9.495549|4.071552|10|4/4/4|rejected|
|smalocal370_parent_BTC750_ETHL6_H225bp|parent|6|0.0225|11.180103|9.937560|8.695558|3.528628|10|4/4/4|rejected|

九个新组合通过0、淘汰9；九个新原生独立状态列上。逐项失败{'smalocal370_ETH_L4_H125bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_ETH_L4_H175bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_ETH_L4_H225bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_ETH_L5_H125bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_ETH_L5_H175bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_ETH_L5_H225bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_ETH_L6_H125bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_ETH_L6_H175bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_ETH_L6_H225bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL4_H125bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL4_H175bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL4_H225bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL5_H125bp': ['local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL5_H175bp': ['local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL5_H225bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL6_H125bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL6_H175bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalocal370_parent_BTC750_ETHL6_H225bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。对同SMA32/同E0.5%旧L5/H2%主控制，全成本NAV同路径0/9，同网格别名另存；不将改名/相同净值当新收益路径。

11CSV保存54成本场景、702月/尾折、432近期折、20034日NAV、两个九格L/H面、9旧SMA控制场景、72相邻边、27持有/现金比较、45新旧原生成本路径及10资金分配。正负折、完整DD/Sharpe/Calmar/成本/成交数全部保留。边界按L4/6与H1.25/2.25%端点核对，相邻cliff仅描述依赖样本，非DSR/PBO显著性或新增裁定标准。

作者一手[SMA趋势估计器论文入口](https://mebfaber.com/white-papers/)与[Binance USD-M市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)均于2026-11-03UTC访问。SMA32、快逆势L/H、永续双向/退出/波动过滤是本项目实验，不能移植作者原10月长仓模型收益；官方字段不是成交、盈利或容量证明。8行情/mark/资金费/约束文件的边界/字节/SHA及新旧实现版本见plan/data_manifest。

全部18份spec先分三批reserve成功，才实际计算27原生+27父成本路径；33来源代码在首个reserve前绑定。合成检查覆盖错误双重加权负对照、非平均收益/DD、错位事件轴拒绝、18个L/H邻域、future价格不可见、L4/5/6精确回看、SMA32真实窗口及与ROC端点区分、双向反转、入退场等号与entry-only波动过滤。独立Fraction信号、Decimal真实q/费用/冲击/资金费/小时风险和完整NAV核验后逐项finish，负结果同样留档。

原SMA65和single续18:30→20:30，原L4/H2续20:10→22:10，仅22:11执行参考闭合后采集。下轮L4的22:10→Nov4UTC00:10会跨真实00资金费与00:01冻结日决策，须00:11参考闭合后取得本账户真实结算并完成整日上下文，不能事前假设资金费/持仓或重复00/08/16。原现金/q/desired/cost/risk/context/完整NAV前缀和终止日保持；00/08/16资金费已按各自实际q入账，不得重复；是否有新结算以真实响应/事件核验，不预设为零。无新日线决策，不强制截止平仓或采纳本批研究。原SMA65日线源20261103T020232Z保持，partial不冒充180日/六折；旧延迟shadow与十策略报价模拟分开。

仅清理本轮可重建中间物；保留真实结果/完整账本、登记、冻结规则、spec/代码、原始短窗响应和失败事实。同main排他锁内更新只读监控并非强制push；实际发布终态、远端完整tree/证据哈希和解锁凭据见.git/automation_proofs/20261103T221037Z.json。

封存：18新定义/54成本场景分别finish，9新组合通过0、淘汰9；9新原生通过0、淘汰9。独立核验9990新信号决策、27新原生成本曲线及27新父曲线，全部新NAV29430702点，核验计数{'funding': 49950, 'fills': 2118, 'rejects': 0, 'metric_checks': 1008, 'margin_checks': 161007}。18旧原生成本曲线只读核验，其资金费/成交是旧账本记录；新原生资金费29970条、成交1494笔来自本轮实际历史模拟。0新BTC/基准/父订单。27新ID/54追加事件；30468旧保护文件不变。

九个新组合对预定同SMA32/E0.5%的L4主控制全成本NAV同路径0/9。同网格别名另存；旧SMA32/E0.5%控制L5/H1.5%、L5/H2%、L4/H2%不混入当前较近L/H邻域，旧canonical rejected状态保持，前轮宽L/H近期合格但邻域仅33%/22%的失败仍有效；本轮窄域通过仅限已见历史局部范围。没有因本批年度正收益而扩大参数、改门槛、修改实测账户或声称独立未来资格。

原SMA续2026-11-03T18:30:00Z至2026-11-03T20:30:00Z，NAV47223+120=47343、累计47309分钟/32完整日；single续2026-11-03T18:30:00Z至2026-11-03T20:30:00Z，NAV11568、累计285ID；L4/H2续2026-11-03T20:10:00Z至2026-11-03T22:10:00Z，仅22:11参考闭合后采集，NAV4305、累计108ID。新资金费single=[]、L4=[]，成交single=0、L4=0，0新日决策。所有book/risk/context/NAV前缀连续；single与L4此前16结算各按其自身-.012/-.006持仓入账，本轮不重复00/08/16，实际新资金费仍依照各自真实响应/事件核验。partial不冒充180日/六折，不采纳新研究规则。

监控通过：9246研究行、9228旧完整行不变，10报价账户/240观察，gzip4222091字节。实际HTTP/传输失败0次，一手作者SMA入口与官方USD-M页面实际访问记录保留。所有必要pipeline实际退出0。双重加权负对照exit1，正确资本/收益/DD与错位事件轴拒绝、未来价格不可见/双向逆势/入退场等号/L4/5/6精确回看/SMA32区间及18邻域检查通过。0已完成回测或观察重跑。清理0真实结果/完整账本，无本轮可重建缓存遗留。

完整正负场景、逐折/全曲线DD、spec/代码/数据和NAV哈希、完整账本、原始短窗响应及失败事实保留。main非强制push、完整远端tree与实际终态/解锁凭据见.git/automation_proofs/20261103T221037Z.json。
