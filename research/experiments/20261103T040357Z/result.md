BTC实际入场额与ETH回看双轴研究

前三轮S24/32、S26/30及S27/29的慢窗口扰动未达到近期/邻域门槛，本轮换成资金敞口方向：固定真实银行3750/15000，BTC固定入场N250/375/500 × ETH快回看L3/4/5。BTC信号ROC31/H4%/E1%、ETH的HL1.5%/HS2.5%/S28/E0.5%/V10/cap4.5%固定。经济假设是改变BTC相对ETH的实际交易敞口，检验近期组合覆盖是否对一档BTC入场量稳健，不以降低总本金掩饰亏损。原始[1,1]完整银行净值相加，不归一化。两个BTC新N必须实算原生LOT、成交量冲击和资金费，ETH与N375旧结果只读；每档同本金同N的恒定持有基准也分别真实核算。属于反复开发历史上的参数诊断，不能称独立最终测试或实盘稳定利润。

完整读取26220事件/12988ID、283份既往结论；初始16均有原档真实证据。此前完整研究定义9565，登记有结果9354、未标结果213，不能把全部登记当完成回测。大量历史搜索存在多重选择偏差。

预设BTC入场N=[250,375,500]USDT × ETH快L=[3,4,5]，固定真实银行3750/15000与ETH入场4500。N是每次开仓名义敞口，不是本金重配；BTC初始资本占比20%、ETH80%，raw[1,1]只把两个完整银行净值相加，不重复乘资本比例、不归一化。不线性缩放旧BTC净值，两个新N逐项实际LOT/手续费/冲击/资金费计算。4新BTC原生（2动量、2恒定持有）和8新父（6候选、2匹配持有）共12/36场景，10旧结果只读。

Walk-forward：真实2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30日完整折+10日尾折。现金/数量/成本跨折连续，完整分钟/事件OOS NAV算整体DD。近期40日继承day330状态、8×5日折，固定信号不拟合、无标签，purge0，30日预热+3日间隔，仅当时已完成收盘和past20成本输入，次日00:01原生OPEN。反复开发历史不称未触碰最终测试、独立未来或DSR/PBO显著。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际订单q×OPEN/past20完整日quoteADV)，LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark维持保证金代理。真实settlement ns/rate/mark/heldq资金费，1/2/3倍压力放大支出、收入不放大。永续空头不借现货，不虚构借币费；缺盘口/TCA/历史全层级/逐tick强平和真实容量证据。三个BTC N均用同本金、同入场N的恒定持有对照，现金0%另列。

判据不放宽：各成本全年净收益>0；1倍至少9/12正完整月；各成本近期40日>0且至少6/8正5日折；3倍整体DD<=25%；索引半径1含中心的局部3倍正收益与严格近期支持均>=60%；至少4原生成交平仓、毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat。组合双轴L/N，BTC源模型仅N单轴，不能冒充两种信号参数同时扰动。4实际持有基准只作参照，rejected表示不是策略候选，不是没有实际结果。

|配置|角色|L|BTC N|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|entrysize370_BTC_N250_momentum|component|31|250|1.713203|1.434598|1.155982|1.510510|9|4/4/4|rejected|
|entrysize370_BTC_N500_momentum|component|31|500|3.474602|2.839155|2.203659|3.535793|9|4/4/4|rejected|
|entrysize370_BTC_N250_constantlong|benchmark_native|0|250|-1.542889|-1.733401|-1.923914|3.381338|6|4/4/4|rejected|
|entrysize370_BTC_N500_constantlong|benchmark_native|0|500|-3.085789|-3.466813|-3.847859|6.731831|6|4/4/4|rejected|
|entrysize370_parent_L3_BTCN250|candidate|3|250|13.391373|11.775119|10.158075|3.259824|10|6/6/5|rejected|
|entrysize370_parent_L3_BTCN500|candidate|3|500|13.743653|12.056030|10.367611|3.360929|10|6/6/6|passed|
|entrysize370_parent_L4_BTCN250|candidate|4|250|9.395340|7.932938|6.469723|4.769160|10|6/6/5|rejected|
|entrysize370_parent_L4_BTCN500|candidate|4|500|9.747620|8.213850|6.679258|4.775981|10|6/6/6|passed|
|entrysize370_parent_L5_BTCN250|candidate|5|250|14.771110|13.146037|11.521952|3.937692|11|3/3/2|rejected|
|entrysize370_parent_L5_BTCN500|candidate|5|500|15.123390|13.426949|11.731487|3.886366|11|4/4/3|rejected|
|entrysize370_parent_L0_BTCN250_constantlong|benchmark_parent|0|250|-10.053750|-10.737949|-11.422152|18.121280|6|3/3/3|rejected|
|entrysize370_parent_L0_BTCN500_constantlong|benchmark_parent|0|500|-10.362330|-11.084632|-11.806942|18.756541|6|4/3/3|rejected|

新组合历史通过2、淘汰4；逐项失败判据{'entrysize370_BTC_N250_momentum': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entrysize370_BTC_N500_momentum': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entrysize370_BTC_N250_constantlong': ['benchmark_control_not_strategy_candidate'], 'entrysize370_BTC_N500_constantlong': ['benchmark_control_not_strategy_candidate'], 'entrysize370_parent_L3_BTCN250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entrysize370_parent_L3_BTCN500': [], 'entrysize370_parent_L4_BTCN250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entrysize370_parent_L4_BTCN500': [], 'entrysize370_parent_L5_BTCN250': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entrysize370_parent_L5_BTCN500': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'entrysize370_parent_L0_BTCN250_constantlong': ['benchmark_control_not_strategy_candidate'], 'entrysize370_parent_L0_BTCN500_constantlong': ['benchmark_control_not_strategy_candidate']}。旧N375原canonical status/criteria/sensitivity/报告字节均保留，本轮L/N诊断单列；原S扰动失败不能被新的N邻域掩盖。

相对匹配旧N375，完整NAV全同0/12；对上一轮同L的S27/28/29父净值同路径数量见prior_grid_NAV_aliases。收益/DD/Sharpe/Calmar、全部逐折及成本、36场景、持有与现金、42相邻边见11CSV和8图。描述性悬崖不当显著性、边界峰不引发本轮事后扩参。

三个冻结账户只延续：SMA65和single从Nov3_00:30到02:30，L4/H2从02:10到04:10，仅04:11参考闭合后采集。Nov3午夜日决策和资金费以前已记不重复；现金/q/desired/累计成本/risk/完整NAV前缀不改，不采纳本批新N、不重置本金、不强制平仓。SMA真实65日上下文仍引用20261103T020232Z/forward_inputs.json.gz。部分延迟shadow与十策略真实报价模拟分开，短样本不作180天/六折资格。

一手资料2026-11-03实际访问：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。原始年行情/mark/资金费/约束8文件的单位/边界/SHA见plan和data_manifest；官方字段不证明盈利或实时执行。

全部实际定义先成功reserve再计算，所有正负结果及必要代码、数据哈希、实际命令留档并finish；同main排他锁内检查、只读snapshot、提交推送。真实push终态与解锁证据见.git/automation_proofs/20261103T040357Z.json。

封存：本轮12个真实配置/36场景均逐项finish，6候选通过2、淘汰4；2新BTC动量源和4实际持有基准单列。独立核对19620468新对齐NAV点、4440决策，funding/fills/风险检查计数{'funding': 33300, 'fills': 954, 'rejects': 0, 'metric_checks': 756, 'margin_checks': 218790}。新原生funding13320条、成交216笔；旧只读funding19980条、成交738笔。21新ID/42追加事件，27976旧文件不变。

entrysize370_parent_L3_BTCN500历史通过：1/2/3倍净收益13.743653%/12.056030%/10.367611%，完整DD3.085383%/3.222567%/3.360929%，1倍10/12正月、近期正折{'1': 6, '2': 6, '3': 6}、局部严格近期支持1.000000。相对同L旧N375收益差+0.060042/+0.025210/-0.009635个百分点，DD差+0.060391/+0.063758/+0.067164个百分点；3倍成本被旧N375在收益/DD上同时支配=True，各成本均联合改善=False。N500位于预设入场量上边界，不事后扩参；历史达标不等于优于原控制或独立未来。

entrysize370_parent_L4_BTCN500历史通过：1/2/3倍净收益9.747620%/8.213850%/6.679258%，完整DD4.482565%/4.628781%/4.775981%，1倍10/12正月、近期正折{'1': 6, '2': 6, '3': 6}、局部严格近期支持0.666667。相对同L旧N375收益差+0.060042/+0.025210/-0.009635个百分点，DD差+0.085777/+0.089569/+0.093395个百分点；3倍成本被旧N375在收益/DD上同时支配=True，各成本均联合改善=False。N500位于预设入场量上边界，不事后扩参；历史达标不等于优于原控制或独立未来。

完整NAV与匹配旧控制同路径0/12，2个新候选是否为新风险收益改善须看逐成本差异，不能仅按passed计数宣传。原N375下S24/32、S26/30、S27/29扰动失败记录均保留；N500与其他S交叉尚未实际评估，不能把本轮L/N局部资格外推。

原SMA65从2026-11-03T00:30:00Z续2026-11-03T02:30:00Z，原NAV46143+120=46263，累计46229分钟/32完整日，0新日决策/成交，Float现金/units/desired/成本/账本连续，65日源仍为20261103T020232Z。原single从2026-11-03T00:30:00Z续2026-11-03T02:30:00Z，NAV10466，累计10229分钟/258ID；新日事件0、决策0、成交0、资金费[]、小时检查9。L4/H2从2026-11-03T02:10:00Z续2026-11-03T04:10:00Z，NAV3203，累计3129分钟/81ID，新日事件0、决策0、成交0、资金费[]、小时检查6。Nov3午夜已经入账的资金费和决策不重复，三个冻结账户保持本金、规则、q/risk与终止计划；部分观察不冒充180日资格。

只读监控通过：9136研究行、9124旧行完整相同，10报价账户/231观察，gzip4155095字节。HTTP/传输失败实际观察0次，必要命令全部真实退出0；预期合成红灯单独保留，无金融或完成观察重跑。0真实结果/0完整账本删除，无遗留可重建缓存。main非强制push/完整远端tree与实际解锁终态见.git/automation_proofs/20261103T040357Z.json。

一个来源核验汇总字段遗留matchedhold=0，按真实batch修正为4并保留原证明字节/哈希；原绑定代码及金融结果不改。一次补充只读来源清单核验实际exit1：非空signal_mode过滤误排除3个ETH来源，改为只排除constant_long_reference后真实exit0验证7个旧来源及4个新原生身份；失败、修正和哈希记录保留，无金融或完成观察重跑。
