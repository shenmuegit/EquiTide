BTC/ETH 原生银行资金与敞口组合验证

宽/窄ETH回看参数均缺近期邻域稳健性，本轮改变原生银行的资金/敞口组合：从BTC3750/N750+ETH15000/N4500变为各15000本金、N1500/4500，raw[1,1]。增加BTC相对ETH的实际名义预算，检验既有ETH宽L/H面能否获得更广近期支持。所有组件已真实执行，本轮只生成九个新组合，不重跑原生、不缩放旧净值。资本与敞口同时变化，不能把收益/DD变化称同资本alpha改进；原20/80组合的rejected资格和历史选择偏差保留。

读取完整26844事件/13300ID、293份既往结论；初始16实际证据完整，缺结果0。此前研究定义9687，标实际9474、未标213；不把全部登记当全部回测，历史多重选择偏差保留。

事前固定新的资金/敞口组合：完整BTC15000/N1500银行+完整ETH15000/N4500银行，raw权重[1,1]，总本金30000，资本份额50/50%、初始名义敞口份额5/15%。旧组合BTC3750/N750+ETH15000/N4500总本金18750、资本份额20/80%、名义4/24%。资本与实际敞口同时改变，百分比收益/DD差异不能称同资本alpha改善。没有归一化、缩放旧NAV/数量、平均Sharpe/DD、调仓/跨银行转移/交叉保证金或父订单。

BTC源政策固定L31/H4%/退出E1%，ETH源固定SMA32门槛、快反转L3/5/7×对称H1.5/2/2.5%、E0.5%、entry-onlyV10/cap4.5%。所有13个原生组件均有真实既往账本；本轮零新原生信号/成交，仅先reserve九个组合后对齐共同事件轴相加完整美元净值。旧20/80组合九格原rejected资格不改；同资本/同预算常多持有基准亦已有实际结果，只读复用，现金0%另列。

Walk-forward：2025-10-19UTC00:01→2026-10-24UTC00:01，连续370日、12×30日完整折+10日尾折，逐折不重置持仓/现金。整体DD来自完整分钟/事件净值，近期40日继承day330状态、8×5日。固定源规则无训练/标签，purge0；所有源过去完整信号在下一00:01原生OPEN执行并于终点计成本平仓。这里是多轮复用的开发历史，不是未触碰最终测试或独立未来。

各组件原生执行预算已实际测试，按真实过去收盘/LOT数量、原5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20quoteADV)，1/2/3倍执行支出和资金费支出、收入不放大。实际settlement ns/rate/mark/heldq；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、1%闭合小时不利mark风险代理完整复核。永续空头无现货借币，不虚构借币费。缺盘口/TCA、完整历史层级/最大量、逐tick强平与容量证明，不把回测正收益称稳定实盘盈利。

沿用失败门槛：各成本全年净正、1倍>=9/12正完整月；各成本近期总收益正且>=6/8正5日折；3倍整体DD<=25%；L/H索引半径1含中心邻域，3倍正与严格近期合格比例均>=60%；>=4底层平仓、毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat、>=180日。不在看到结果后改门槛或扩格。

|新组合|L|H比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|bankmix370_BTC1500_ETHL3_H150bp|3|0.015|8.611795|7.383692|6.155420|4.031406|9|5/5/5|rejected|
|bankmix370_BTC1500_ETHL3_H200bp|3|0.02|9.699124|8.557354|7.415590|3.755596|9|5/5/5|rejected|
|bankmix370_BTC1500_ETHL3_H250bp|3|0.025|9.168473|8.234562|7.300554|3.087425|9|5/5/5|rejected|
|bankmix370_BTC1500_ETHL5_H150bp|5|0.015|11.342887|10.239643|9.136855|2.611453|12|5/5/5|rejected|
|bankmix370_BTC1500_ETHL5_H200bp|5|0.02|10.254830|9.289364|8.324010|2.590933|12|5/5/5|rejected|
|bankmix370_BTC1500_ETHL5_H250bp|5|0.025|6.791316|6.006767|5.222226|2.424343|10|4/4/4|rejected|
|bankmix370_BTC1500_ETHL7_H150bp|7|0.015|10.039488|9.139405|8.239435|2.514224|11|5/5/5|rejected|
|bankmix370_BTC1500_ETHL7_H200bp|7|0.02|9.575872|8.712762|7.849685|2.521685|10|5/5/5|rejected|
|bankmix370_BTC1500_ETHL7_H250bp|7|0.025|9.058888|8.273920|7.489047|2.131617|10|4/4/4|rejected|

新组合通过0、淘汰9，逐项失败{'bankmix370_BTC1500_ETHL3_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC1500_ETHL3_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC1500_ETHL3_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC1500_ETHL5_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC1500_ETHL5_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC1500_ETHL5_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC1500_ETHL7_H150bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC1500_ETHL7_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'bankmix370_BTC1500_ETHL7_H250bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。正负场景/折完整保存；同网格NAV别名和与旧配置资本差异另存，不把重复/现金稀释当独立收益来源。

10CSV保存27新场景、351月/尾折、216近期折、10017日NAV、九格L/H面、27旧配置场景、36相邻边、27匹配持有/现金比较、39只读原生成本路径、10资金分配。相邻cliff为依赖样本描述性诊断，不是DSR/PBO显著性或新增裁定条件；边界按真实L/H端点核对。

一手[SMA论文入口](https://mebfaber.com/white-papers/)和[Binance USD-M市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)于2026-11-04UTC访问。仅参考均线趋势估计器与实际字段，不能移植原10月长仓论文收益。所有价格/资金费/mark/约束文件字节/SHA和组件spec/report/archive版本见plan/data_manifest。

原L4冻结账户本轮跨Nov3UTC22:10→Nov4UTC00:10，独立核验整日Nov3volume/close/context、实际00资金费以及00:01原规则决策/潜在成交；不预设收益、仓位或零资金费，不重复Nov3结算。single与原SMA65续Nov3UTC20:30→22:30，尚未处理各自Nov4日决策；下一窗口必须使用原规则完成实际00资金费/日线/执行参考，不能复制L4金额或继续mark-only跳过决策。所有本金、冻结规则、风险和完整NAV前缀保持，partial不冒充180日/六折，旧shadow与十策略报价模拟分开。

single索引依赖旧run导入已省略的原生engine而失败，改为直接读取common元数据后仅重试投影索引；观察与完整账户审计均已退出0，没有重跑观察。失败命令/HTTP首次TLS失败及已恢复事实保留；不会为监控改历史。32来源文件在首个金融reserve前绑定，原生交易函数无新调用，合成检查验证完整30000银行资本、非平均DD、错误旧BTC缩放及错位事件轴拒绝。

本轮仅清理可重建中间物，保留完整源/账户账本、冻结规则、登记、全部正负结果、原始短窗/失败响应及必要代码。同main排他锁更新只读监控并非强制push，远端完整tree/哈希、实际终态和解锁凭据见.git/automation_proofs/20261104T001133Z.json。

封存：9新组合/27成本场景逐项finish，通过0、淘汰9；0新原生/信号/订单，13旧原生/39成本账本只读复核，旧资金费43290条、成交1638笔是旧回测记录。新组合NAV14715351点，独立核验{'funding': 43290, 'fills': 1638, 'rejects': 0, 'metric_checks': 924, 'margin_checks': 163593}，无父订单。18新ID/36追加事件，30760旧保护文件不变。

本轮组合按实际资本30000统计，旧18750配置资本/敞口不同；matched_hold为同30000/入场1500+4500的旧真实持有基准。不能以现金稀释DD或不同本金百分比差异声称同资本alpha，也不能把旧源操作次数当新成交。原time_boundaries.calendar继承源实验日期，旧causality说明的原生18/L4/5/6文字仅为旧源描述；本轮权威rules/grid和九份已登记spec明确L3/5/7、9组合、0新原生，原文与注记均保留。

原SMA续2026-11-03T20:30:00Z至2026-11-03T22:30:00Z，NAV47343+120=47463，累计47429分钟；single续2026-11-03T20:30:00Z至2026-11-03T22:30:00Z，NAV11690、累计288ID，尚未执行自己的Nov4日决策。L4续2026-11-03T22:10:00Z至2026-11-04T00:10:00Z，真实午夜日事件1、独立决策6、新成交0；NAV4305+127=4432，累计111ID，完整日线36/36、资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0.04646502000000000000000000000', 'amount_usdt': '0.04646502000000000000000000000', 'mark': '77441.70000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0.04646502000000000000000000000', 'amount_usdt': '0.04646502000000000000000000000', 'mark': '77441.70000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0.04646502000000000000000000000', 'amount_usdt': '0.04646502000000000000000000000', 'mark': '77441.70000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2273.85000000', 'rate': '0.00008833'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2273.85000000', 'rate': '0.00008833'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793750400000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2273.85000000', 'rate': '0.00008833'}]。原冻结规则/本金/持仓续接、risk/context/fullNAV前缀不变，原始计划不取消；partial不冒充180日/六折。

监控通过：9255研究行、9246旧完整行不变，10报价账户/241观察，gzip4227375字节。原索引导入失败1次和公共HTTP/传输失败1次留档，恢复后的必要检查均实际退出0。0已完成回测/观察重跑。清理0真实结果/账本，零可重建缓存遗留。

全部正负折、完整DD、源/新spec/report/archive/数据哈希及代码、真实短窗/失败响应保留。main非强制push、远端完整tree/blob内容与实际终态/解锁凭据见.git/automation_proofs/20261104T001133Z.json。
