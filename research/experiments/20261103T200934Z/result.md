SMA32 慢门槛下快反转回看与入场阈值的联合验证

上一批SMA慢门槛组合全年和逐月表现为正，但近期仅5/8正折，全部淘汰。本轮保持SMA32、E0.5%、V10/cap4.5%及实际资金规模，事前改变快逆势回看L3/5/7和对称入场H1.5/2/2.5%，检验入场频率变化能否改善近期分布。所有旧L4控制只读，九新原生+九新组合先reserve；重复开发历史上的继续研究不称未触碰最终/独立未来，不因本轮结果再扩网格或放宽门槛。

完整读取26696事件/13226ID、291份既往结论；初始16有原档实际证据、缺结果0。此前研究定义9651，标实际9438、未标213，不将全部登记当全部实际回测；大量反复历史研究存在多重选择偏差。

事前固定快反转 L3/5/7 日×对称入场 H1.5/2/2.5%，SMA32、退出E0.5%、entry-onlyV10/cap4.5%固定。r=C[i−1]/C[i−1−L]−1；r>H做空、r<−H做多，入场等号不触发。否则实际多仓只在r<E保留、空仓只在r>−E保留，退出等号平仓。慢门槛为sign(C[i−1]/mean(C[i−32:i])−1)，包含最新完整收盘，零/相反方向flat；仅对新增/反转仓应用波动门槛，原方向仓位不因单独高波动退出。

九个新ETH原生各本金15000/N4500；九个新组合持有完整BTC3750/N750旧银行+对应ETH15000/N4500新银行，raw[1,1]、总本金18750、资金份额20/80%、名义入场占比4/24%。保持原权重，不归一化、不缩放旧净值/真实数量、不平均收益/Sharpe/DD、不跨银行调仓/交叉保证金或转移，0父订单。三项旧SMA32/L4/H2%控制E0.375/0.5/0.625%在网格外只读，其中同E0.5%为预定主控制；三者原rejected资格不改，不能混入本轮L/H邻域。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日，12×30日完整折+10日尾折；逐折不重置现金/仓位，整体DD来自完整分钟/事件OOS净值。近期40日承接day330实际状态，8×5日。固定规则无拟合/标签、purge0、事前33日线足够SMA32；下一UTC00:01原生OPEN执行，数量按过去完整收盘/LOT算，反手先平后开，终点计成本平仓。属于反复使用的开发历史，不是未触碰最终测试或独立未来验证。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍放大执行和资金费支出，资金费收入不放大；实际settlement ns/rate/mark/heldq。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark风险代理；永续空头无需现货借币，不虚构借币费用。同资本/N750/4500持有和现金0%对照只读。缺盘口/TCA、历史完整保证金层级/最大量、逐tick强平和容量证明。

固定失败门槛：各成本全年净正；1倍至少9/12正完整月；近期各成本总收益正且>=6/8正5日折；3倍整体DD<=25%；含中心L/H索引半径1邻域，3倍正和严格近期合格比例均>=60%；>=4底层平仓；毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规，终点flat、至少180日。全部18项按同一事前标准裁定，不据结果增格/改门槛。

|新配置|scope|L日数|H比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|smalh370_ETH_L3_H150bp_S32_E5000ppm|native|3|0.015|14.258478|12.302401|10.345908|6.399955|8|4/4/4|rejected|
|smalh370_ETH_L3_H200bp_S32_E5000ppm|native|3|0.02|16.433136|14.649725|12.866247|5.855189|9|4/4/4|rejected|
|smalh370_ETH_L3_H250bp_S32_E5000ppm|native|3|0.025|15.371835|14.004140|12.636175|4.374775|9|3/3/3|rejected|
|smalh370_ETH_L5_H150bp_S32_E5000ppm|native|5|0.015|19.720662|18.014303|16.308776|3.714541|10|3/3/3|rejected|
|smalh370_ETH_L5_H200bp_S32_E5000ppm|native|5|0.02|17.544548|16.113744|14.683088|3.674503|10|3/3/3|rejected|
|smalh370_ETH_L5_H250bp_S32_E5000ppm|native|5|0.025|10.617521|9.548552|8.479518|3.356274|10|2/2/2|rejected|
|smalh370_ETH_L7_H150bp_S32_E5000ppm|native|7|0.015|17.113865|15.813827|14.513937|4.026221|10|3/3/2|rejected|
|smalh370_ETH_L7_H200bp_S32_E5000ppm|native|7|0.02|16.186633|14.960540|13.734436|4.049222|10|3/3/2|rejected|
|smalh370_ETH_L7_H250bp_S32_E5000ppm|native|7|0.025|15.152664|14.082857|13.013160|3.246696|10|2/2/1|rejected|
|smalh370_parent_BTC750_ETHL3_H150bp|parent|3|0.015|12.535277|10.777373|9.019144|5.638903|8|5/5/5|rejected|
|smalh370_parent_BTC750_ETHL3_H200bp|parent|3|0.02|14.275004|12.655232|11.035415|5.200848|8|5/5/5|rejected|
|smalh370_parent_BTC750_ETHL3_H250bp|parent|3|0.025|13.425963|12.138764|10.851358|4.084962|8|5/5/5|rejected|
|smalh370_parent_BTC750_ETHL5_H150bp|parent|5|0.015|16.905024|15.346895|13.789439|3.478553|11|6/6/6|rejected|
|smalh370_parent_BTC750_ETHL5_H200bp|parent|5|0.02|15.164133|13.826448|12.488888|3.446224|11|6/6/6|rejected|
|smalh370_parent_BTC750_ETHL5_H250bp|parent|5|0.025|9.622511|8.574294|7.526033|2.942892|10|5/5/5|rejected|
|smalh370_parent_BTC750_ETHL7_H150bp|parent|7|0.015|14.819586|13.586514|12.353568|3.504178|11|5/5/5|rejected|
|smalh370_parent_BTC750_ETHL7_H200bp|parent|7|0.02|14.077801|12.903884|11.729967|3.520414|11|5/5/5|rejected|
|smalh370_parent_BTC750_ETHL7_H250bp|parent|7|0.025|13.250625|12.201738|11.152946|2.887224|11|4/4/4|rejected|

九个新组合通过0、淘汰9；九个新原生独立状态列上。逐项失败{'smalh370_ETH_L3_H150bp_S32_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_ETH_L3_H200bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_ETH_L3_H250bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_ETH_L5_H150bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_ETH_L5_H200bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_ETH_L5_H250bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_ETH_L7_H150bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_ETH_L7_H200bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_ETH_L7_H250bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL3_H150bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL3_H200bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL3_H250bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL5_H150bp': ['local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL5_H200bp': ['local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL5_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL7_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL7_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smalh370_parent_BTC750_ETHL7_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。对同SMA32/同E0.5%旧L4/H2%主控制，全成本NAV同路径0/9，同网格别名另存；不将改名/相同净值当新收益路径。

11CSV保存54成本场景、702月/尾折、432近期折、20034日NAV、两个九格L/H面、9旧SMA控制场景、72相邻边、27持有/现金比较、45新旧原生成本路径及10资金分配。正负折、完整DD/Sharpe/Calmar/成本/成交数全部保留。边界按L3/7与H1.5/2.5%端点核对，相邻cliff仅描述依赖样本，非DSR/PBO显著性或新增裁定标准。

作者一手[SMA趋势估计器论文入口](https://mebfaber.com/white-papers/)与[Binance USD-M市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)均于2026-11-03UTC访问。SMA32、快逆势L/H、永续双向/退出/波动过滤是本项目实验，不能移植作者原10月长仓模型收益；官方字段不是成交、盈利或容量证明。8行情/mark/资金费/约束文件的边界/字节/SHA及新旧实现版本见plan/data_manifest。

全部18份spec先分三批reserve成功，才实际计算27原生+27父成本路径；33来源代码在首个reserve前绑定。合成检查覆盖错误双重加权负对照、非平均收益/DD、错位事件轴拒绝、18个L/H邻域、future价格不可见、L3/5/7精确回看、SMA32真实窗口及与ROC端点区分、双向反转、入退场等号与entry-only波动过滤。独立Fraction信号、Decimal真实q/费用/冲击/资金费/小时风险和完整NAV核验后逐项finish，负结果同样留档。

原SMA65和single续16:30→18:30，原L4/H2续18:10→20:10，仅20:11执行参考闭合后采集。原现金/q/desired/cost/risk/context/完整NAV前缀和终止日保持；00/08/16资金费已按各自实际q入账，不得重复；是否有新结算以真实响应/事件核验，不预设为零。无新日线决策，不强制截止平仓或采纳本批研究。原SMA65日线源20261103T020232Z保持，partial不冒充180日/六折；旧延迟shadow与十策略报价模拟分开。

仅清理本轮可重建中间物；保留真实结果/完整账本、登记、冻结规则、spec/代码、原始短窗响应和失败事实。同main排他锁内更新只读监控并非强制push；实际发布终态、远端完整tree/证据哈希和解锁凭据见.git/automation_proofs/20261103T200934Z.json。

封存：18新定义/54成本场景分别finish，9新组合通过0、淘汰9；9新原生通过0、淘汰9。独立核验9990新信号决策、27新原生成本曲线及27新父曲线，全部新NAV29430702点，核验计数{'funding': 49950, 'fills': 2046, 'rejects': 0, 'metric_checks': 1008, 'margin_checks': 156840}。18旧原生成本曲线只读核验，其资金费/成交是旧账本记录；新原生资金费29970条、成交1422笔来自本轮实际历史模拟。0新BTC/基准/父订单。27新ID/54追加事件；30176旧保护文件不变。

九个新组合对预定同SMA32/E0.5%的L4主控制全成本NAV同路径0/9。同网格别名另存；旧SMA32/L4/H2%控制E0.375/0.5/0.625%不混入新快反转L/H邻域，旧canonical rejected状态保持，前轮SMA S/E近期仅5/8的失败仍有效。没有因本批年度正收益而扩大参数、改门槛、修改实测账户或声称独立未来资格。

原SMA续2026-11-03T16:30:00Z至2026-11-03T18:30:00Z，NAV47103+120=47223、累计47189分钟/32完整日；single续2026-11-03T16:30:00Z至2026-11-03T18:30:00Z，NAV11446、累计282ID；L4/H2续2026-11-03T18:10:00Z至2026-11-03T20:10:00Z，仅20:11参考闭合后采集，NAV4183、累计105ID。新资金费single=[]、L4=[]，成交single=0、L4=0，0新日决策。所有book/risk/context/NAV前缀连续；single与L4此前16结算各按其自身-.012/-.006持仓入账，本轮不重复00/08/16，实际新资金费仍依照各自真实响应/事件核验。partial不冒充180日/六折，不采纳新研究规则。

监控通过：9228研究行、9210旧完整行不变，10报价账户/239观察，gzip4211146字节。实际HTTP/传输失败0次，一手作者SMA入口与官方USD-M页面实际访问记录保留。所有必要pipeline实际退出0。双重加权负对照exit1，正确资本/收益/DD与错位事件轴拒绝、未来价格不可见/双向逆势/入退场等号/L3/5/7精确回看/SMA32区间及18邻域检查通过。0已完成回测或观察重跑。清理0真实结果/完整账本，无本轮可重建缓存遗留。

完整正负场景、逐折/全曲线DD、spec/代码/数据和NAV哈希、完整账本、原始短窗响应及失败事实保留。main非强制push、完整远端tree与实际终态/解锁凭据见.git/automation_proofs/20261103T200934Z.json。
