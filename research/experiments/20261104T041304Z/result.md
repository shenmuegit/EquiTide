本轮无合格新候选：有限 EWM32 的9个ETH原生策略与9个BTC/ETH组合全部rejected。三项验证均实际完成：连续370日walk-forward及逐折/近期核验；原生与组合两个L/H敏感性面均因严格近期邻域合格比例0%未通过；1/2/3倍成本下54/54全期净收益为正。九个组合三倍收益4.1943%～10.5770%、连续整体DD2.4236%～4.2859%，但近期仅4–5/8个盈利五日折；原生仅0–3/8，另6项未达9/12盈利完整月，1项近期全成本净正门槛失败。全部正负折保留，不把历史正收益称稳定实盘盈利。

有限窗口 EWM32 趋势门槛与快反转 L/H 联合验证

此前简单均值SMA32与资金敞口分配变化仍未满足近期稳健性。本轮固定实际资本18750、BTC500/ETH4500预算、E0.5%、V10/cap4.5%，仅把ETH慢门槛换为有限32日归一化指数加权均值(beta31/33)，让近期完整收盘权重更高，检验趋势识别时滞变化能否改善近期分布。事前L3/5/7×H1.5/2/2.5%九格，9新原生+9新组合先reserve。BTC及同格SMA32对照真实账本只读。已知开发历史中的假设探索，非独立最终或未来验证。

完整读取26956事件/13356ID、295份既往结论；初始16项实际证据完整，缺结果0。此前研究定义9705，标实际9492、未标213。不将全部登记当全部实际回测；反复使用历史的多重选择偏差保留。

事前固定 ETH 快反转 L3/5/7×对称入场 H1.5/2/2.5%，E0.5%、entry-only V10/cap4.5%。r=C[i−1]/C[i−1−L]−1；严格r>H做空、r<−H做多，入场等号不触发。否则实际多仓仅在r<E保留、实际空仓仅在r>−E保留，退出等号flat。EWM32=sum((31/33)^j×C[i−1−j],j=0..31)/sum((31/33)^j,j=0..31)，只取此前32个完整收盘，最新完整收盘权重最大；gate=sign(C[i−1]/EWM32−1)，零或相反方向强制flat。它是每天重新限定32日窗口的归一化指数加权均值，不是无限历史递推EMA。仅新增/反向仓位应用过去10日样本logvol门槛，原方向仓位不因单独高波动退出。

九个新ETH原生各本金15000/N4500，真实数量/费用/资金费/风险从冻结日历执行；九个新组合拥有完整BTC3750/N500旧银行+对应ETH15000/N4500新银行。raw[1,1]、总本金18750、资本份额20/80%、初始名义敞口份额2.6666666667/24%。没有组合权重归一化、旧NAV/数量缩放、平均指标、父订单、调仓/转移或交叉保证金。信号内的时间权重归一化属于预先规定的均值公式。22个旧实际结果中12个原生账本/36成本路径只读复用，包含同格L/H、同资本与预算的SMA32原生和组合，以及同资本/预算的常多持有基准，所有旧资格保持。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日，12×30日完整折+10日尾折，逐折不重置现金和持仓，整体DD使用完整分钟/事件净值。近期40日继承day330状态、8×5日。固定规则无拟合/标签、purge0，33日线上下文足够；信号来自完整过去收盘，下一UTC00:01原生OPEN执行，数量按过去收盘/LOT取整，反手先平后开，终点计成本平仓。已反复使用的开发历史不能称未触碰最终测试或独立未来。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍放大执行支出与资金费支出，资金费收入不放大。使用真实settlement ns/rate/mark和结算时自身持仓；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押与独立1%闭合小时不利mark风险代理均核验。永续空头无现货借币，不虚构借币费用。基准为同资本/预算常多持有及现金0%。缺盘口/TCA、完整历史最大量/保证金层级、逐tick强平及容量证明，正回测不代表稳定实盘盈利。

固定失败门槛：所有成本全期净正；1倍>=9/12盈利完整月；各成本近期净正且>=6/8盈利五日折；3倍整体DD<=25%；L/H索引半径1含中心，邻域3倍净正与严格近期合格比例均>=60%；>=4底层平仓；毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat、>=180日。native和parent分别用预定九格邻域；看到结果后不改门槛或扩本批网格。

|新配置|scope|L日数|H比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|fewm32_ETH_L3_H150bp_E5000ppm|native|3|0.015|9.006980|7.348173|5.688867|4.421961|8|3/3/3|rejected|
|fewm32_ETH_L3_H200bp_E5000ppm|native|3|0.02|11.590139|10.149168|8.708206|3.751440|9|3/3/3|rejected|
|fewm32_ETH_L3_H250bp_E5000ppm|native|3|0.025|9.431935|8.348671|7.265114|4.078743|8|2/2/2|rejected|
|fewm32_ETH_L5_H150bp_E5000ppm|native|5|0.015|15.913801|14.291866|12.670336|2.834389|10|2/2/2|rejected|
|fewm32_ETH_L5_H200bp_E5000ppm|native|5|0.02|14.683403|13.335614|11.987976|2.801219|10|2/2/2|rejected|
|fewm32_ETH_L5_H250bp_E5000ppm|native|5|0.025|6.565134|5.628590|4.691985|3.213283|8|1/1/1|rejected|
|fewm32_ETH_L7_H150bp_E5000ppm|native|7|0.015|11.299634|10.040172|8.780871|5.048556|8|3/3/2|rejected|
|fewm32_ETH_L7_H200bp_E5000ppm|native|7|0.02|10.366070|9.375216|8.384273|5.084304|8|2/2/1|rejected|
|fewm32_ETH_L7_H250bp_E5000ppm|native|7|0.025|9.332101|8.497533|7.662997|4.134735|8|1/1/0|rejected|
|fewm32_parent_BTC500_ETHL3_H150bp|parent|3|0.015|7.900504|6.446370|4.991825|3.963082|9|5/5/5|rejected|
|fewm32_parent_BTC500_ETHL3_H200bp|parent|3|0.02|9.967031|8.687165|7.407296|3.425339|10|5/5/5|rejected|
|fewm32_parent_BTC500_ETHL3_H250bp|parent|3|0.025|8.240469|7.246768|6.252823|3.725062|9|5/5/5|rejected|
|fewm32_parent_BTC500_ETHL5_H150bp|parent|5|0.015|13.425961|12.001324|10.577000|2.501005|11|6/6/5|rejected|
|fewm32_parent_BTC500_ETHL5_H200bp|parent|5|0.02|12.441642|11.236322|10.031112|2.423574|11|6/6/5|rejected|
|fewm32_parent_BTC500_ETHL5_H250bp|parent|5|0.025|5.947027|5.070703|4.194320|2.503935|9|5/5/4|rejected|
|fewm32_parent_BTC500_ETHL7_H150bp|parent|7|0.015|9.734628|8.599969|7.465429|4.261409|9|5/5/5|rejected|
|fewm32_parent_BTC500_ETHL7_H200bp|parent|7|0.02|8.987776|8.068004|7.148150|4.285924|9|5/5/5|rejected|
|fewm32_parent_BTC500_ETHL7_H250bp|parent|7|0.025|8.160601|7.365857|6.571129|3.505682|9|4/4/4|rejected|

九个新组合通过0、淘汰9；九个新原生的独立资格见上表。逐项失败：{'fewm32_ETH_L3_H150bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_ETH_L3_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_ETH_L3_H250bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_ETH_L5_H150bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_ETH_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_ETH_L5_H250bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_ETH_L7_H150bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_ETH_L7_H200bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_ETH_L7_H250bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL3_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL3_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL3_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL5_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL5_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL5_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL7_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL7_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewm32_parent_BTC500_ETHL7_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。匹配SMA32对照与同格新旧原生比较另存；同格全成本NAV相同0/9，网格内别名另存，不把相同净值当独立收益路径。

11CSV完整保留54成本场景、702月/尾折、432近期折、20034日NAV、原生和组合两个九格L/H面、27旧SMA组合场景、72相邻边、27匹配持有/现金比较、63新旧原生成本路径和10组资金配置。正负收益折、完整DD/Sharpe/Calmar、费用与实际成交数均保留。边界最高Sharpe与相邻cliff均如实记录，只是依赖样本的描述性诊断，不是DSR/PBO显著性或新增裁定条件。

来源：2026-11-04UTC阅读 [Pandas官方EWM公式](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html) 和 [Binance USD-M官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。有限32日窗口是本项目预定研究变体；不移植文档之外的收益或成交能力。8个行情/mark/资金费/约束文件、spec/report/archive/实现和数据SHA见plan/data_manifest。

首个实际金融reserve之前绑定33份研究源码，旧simulate函数AST保持，仅改ETH门槛；合成检查以独立整数权重核对有限EWM、时序、等号和波动过滤。所有18配置分三批reserve成功后，实际计算27原生+27父成本路径；独立信号审计用相反遍历方向的Fraction Horner公式，独立复核Decimal现金/LOT/tick/冲击/资金费、小时风险和完整NAV，再逐配置finish。

原SMA65与single续Nov4UTC00:30→02:30，原L4续02:10→04:10，均在所需参考闭合后采集；延续原本金、冻结规则、逐成本状态和完整NAV前缀，不重复已处理的Nov4午夜决策/资金费。原SMA65保留最新65日上下文源20261104T021133Z/forward_inputs.json.gz。真实事件以各自响应为准，不预设资金费/成交结果；本批EWM研究不写入冻结账户。partial不冒充180日/六折，旧延迟shadow与十策略真实报价模拟分开。

只清理本轮可重建中间物；完整账户账本、冻结规则、登记、正负结果、必要代码和原始短窗/失败证据均保留。同main排他锁内更新只读监控、普通非强制push；实际发布终态/完整远端tree与blob哈希/解锁凭据见.git/automation_proofs/20261104T041304Z.json。

封存：18新金融配置/54成本场景逐项finish，组合通过0、淘汰9；原生通过0。新原生信号9990次、资金费29970条、成交1254笔均为实际新账本；旧36成本账本的资金费39960条、成交1536笔属于旧记录。独立核验{'funding': 69930, 'fills': 2790, 'rejects': 0, 'metric_checks': 1260, 'margin_checks': 176895}，无父订单。27新ID/54追加事件，31302旧保护文件不变。

原SMA续2026-11-04T00:30:00Z至2026-11-04T02:30:00Z，NAV47584+120=47704，累计47669分钟。single续2026-11-04T00:30:00Z至2026-11-04T02:30:00Z，NAV11817+122=11939，累计294ID。L4续2026-11-04T02:10:00Z至2026-11-04T04:10:00Z，NAV4676，累计117ID。三账户本轮新日决策/成交分别为SMA 0/0、single 0/0、L4 0/0；资金费single []、L4 []。原规则/本金和完整NAV前缀保留，partial不冒充180日/六折，不采纳EWM研究。

监控通过：9282研究行，9264旧完整行不变，10报价账户/243观察，gzip4243680字节。必要实际命令均退出0；公共HTTP/传输失败0次及其他实际错误如实留档，0已完成金融/观察重跑。清理0真实结果/账本，零可重建缓存遗留。

全部正负折/逐变体、完整DD、spec/report/archive/数据/源码SHA、真实短窗与失败证据保留。main非强制push和远端完整tree/blob及实际终态/解锁凭据见.git/automation_proofs/20261104T041304Z.json。
