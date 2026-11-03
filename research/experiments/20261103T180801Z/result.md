ETH 收盘价相对 SMA 慢门槛的逆势策略验证

此前端点ROC慢门槛在S27/28/29间不稳健，顺势入场L/H又未达近期/逐月门槛。本轮改用最新完整收盘相对过去S日SMA估计慢趋势，保留L4/H2%逆势入场、entry-onlyV10/cap4.5%、真实原生资金规模。事前固定S24/28/32×E0.375/0.5/0.625%，九个新原生+九个新组合全部先reserve；不用看结果后扩网格或放宽门槛。此为不同慢趋势估计器的实验，不声称作者原10月模型在ETH永续有效。

完整读取26622事件/13189ID、290份既往结论；初始16已有原档实际证据、缺真实结果0。此前研究定义9633，标实际9420、未标213；大量历史搜索存在多重选择偏差。

事前固定 SMA S24/28/32 日×退出 E0.375/0.5/0.625%。快反转 L4、对称 H2%、entry-only V10/cap4.5%固定。SMA=mean(C[i-S:i])，包含最新完整 i−1 收盘；gate=sign(C[i−1]/SMA−1)。fastROC>2%做空、<−2%做多，入场等号不触发；否则实际多仓仅r<E保留，空仓仅r>−E保留，退出等号平仓；与SMA方向不符或均值相等强制flat。只过滤新增/转向持仓，高波动不单独退出同方向实仓。

九个ETH新原生各本金15000、固定N4500。九个组合逐一持有完整BTC3750/N750旧银行+对应ETH15000/N4500新银行，raw[1,1]、总本金18750、资金占比20/80%、入场名义占比4/24%。不归一化、不缩放旧净值/数量、不平均收益/Sharpe/DD、不跨银行调仓/转移/交叉保证金，0父订单。三项旧endpointROC逆势S28控制E0.375/0.5/0.625%在网格外只读；主控制E0.375%在新结果前固定，同E对照另存matched_gate_comparisons.json。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30日完整折+10日尾折；逐折不重置现金/持仓，整体DD来自完整分钟/事件净值。近期40日承接day330真实状态，8×5日。固定规则无拟合/标签、purge0，事前33根日线足够maxS32，下一UTC00:01原生OPEN执行，数量以前一完整close/LOT算；反手先平后开，终点计成本平仓。这是反复使用的开发历史，不是未触碰最终测试或独立未来。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍放大执行和资金费支出，资金费收入不放大。实际结算ns/rate/mark/heldq；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark风险代理。永续空头无需借入现货，不虚构借币费用。匹配同资本/入场N750/4500持有与现金0%对照。缺真实盘口/TCA、历史完整层级/最大量、逐tick强平及容量证明。

冻结失败判据：各成本全年净正，1倍至少9/12正完整月；各成本近期总收益正且>=6/8正5日折；3倍整体DD<=25%；S/E索引半径1含中心邻域3倍正和严格近期合格比例均>=60%；>=4底层平仓，毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规，终点flat、>=180日。全部18项按同一预定门槛裁定。旧ROC控制canonical资格/判据/敏感性不改，不能混进SMA邻域。

|新配置|scope|SMA日数|E比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|smagate370_ETH_L4_H200bp_S24_E3750ppm|native|24|0.00375|6.949062|5.480863|4.012856|5.085144|9|2/2/2|rejected|
|smagate370_ETH_L4_H200bp_S24_E5000ppm|native|24|0.005|6.372653|4.952544|3.532255|5.085144|9|2/2/2|rejected|
|smagate370_ETH_L4_H200bp_S24_E6250ppm|native|24|0.00625|8.376781|6.956898|5.536935|4.987976|10|2/2/2|rejected|
|smagate370_ETH_L4_H200bp_S28_E3750ppm|native|28|0.00375|11.916377|10.395691|8.875001|3.510330|10|2/2/2|rejected|
|smagate370_ETH_L4_H200bp_S28_E5000ppm|native|28|0.005|11.339967|9.867372|8.394399|3.510330|10|2/2/2|rejected|
|smagate370_ETH_L4_H200bp_S28_E6250ppm|native|28|0.00625|13.344096|11.871726|10.399080|3.443256|10|2/2/2|rejected|
|smagate370_ETH_L4_H200bp_S32_E3750ppm|native|32|0.00375|15.072449|13.485500|11.898457|3.796897|9|3/3/3|rejected|
|smagate370_ETH_L4_H200bp_S32_E5000ppm|native|32|0.005|15.123193|13.582617|12.041413|3.796897|9|3/3/3|rejected|
|smagate370_ETH_L4_H200bp_S32_E6250ppm|native|32|0.00625|17.127321|15.586971|14.046094|3.484628|9|3/3/3|rejected|
|smagate370_parent_BTC750_ETHS24_E3750ppm|parent|24|0.00375|6.687744|5.320142|3.952703|4.465980|10|5/5/5|rejected|
|smagate370_parent_BTC750_ETHS24_E5000ppm|parent|24|0.005|6.226616|4.897487|3.568222|4.465980|10|5/5/5|rejected|
|smagate370_parent_BTC750_ETHS24_E6250ppm|parent|24|0.00625|7.829919|6.500970|5.171966|4.397273|11|5/5/5|rejected|
|smagate370_parent_BTC750_ETHS28_E3750ppm|parent|28|0.00375|10.661596|9.252005|7.842419|3.057786|11|5/5/5|rejected|
|smagate370_parent_BTC750_ETHS28_E5000ppm|parent|28|0.005|10.200468|8.829350|7.457938|3.057786|11|5/5/5|rejected|
|smagate370_parent_BTC750_ETHS28_E6250ppm|parent|28|0.00625|11.803771|10.432833|9.061682|3.004890|11|5/5/5|rejected|
|smagate370_parent_BTC750_ETHS32_E3750ppm|parent|32|0.00375|13.186454|11.723852|10.261183|3.561853|10|5/5/5|rejected|
|smagate370_parent_BTC750_ETHS32_E5000ppm|parent|32|0.005|13.227048|11.801546|10.375549|3.561853|10|5/5/5|rejected|
|smagate370_parent_BTC750_ETHS32_E6250ppm|parent|32|0.00625|14.830351|13.405029|11.979293|3.335853|10|5/5/5|rejected|

九个新组合通过0、淘汰9；九个新原生状态另列。逐项失败{'smagate370_ETH_L4_H200bp_S24_E3750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_ETH_L4_H200bp_S24_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_ETH_L4_H200bp_S24_E6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_ETH_L4_H200bp_S28_E3750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_ETH_L4_H200bp_S28_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_ETH_L4_H200bp_S28_E6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_ETH_L4_H200bp_S32_E3750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_ETH_L4_H200bp_S32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_ETH_L4_H200bp_S32_E6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS24_E3750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS24_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS24_E6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS28_E3750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS28_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS28_E6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS32_E3750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS32_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'smagate370_parent_BTC750_ETHS32_E6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。对预设旧强控制全成本NAV同路径0/9，同网格别名组另存，不把不同名称当新收益路径。

11CSV含54新成本场景、702月/尾折、432近期折、20034日NAV、两个九格S/E面、9旧ROC控制场景、72相邻边、27匹配持有/现金比较、45新旧原生成本路径和10资金分配。全部正负折、净收益、完整DD、Sharpe、Calmar、成本及成交数保留；边界按真实S/E端点检查。相邻cliff只作依赖样本描述，不冒充DSR/PBO显著性或事后门槛。

SMA原始动机来自作者一手[2013年战术配置论文入口](https://mebfaber.com/white-papers/)，仅参考价格相对简单均线这一趋势估计器。这里的日线S24/28/32、逆势快入场、永续双向仓位和风险核算均为本项目新实验；不能移植原10月长仓模型的收益结论。2026-11-03UTC已访问该作者入口、更新说明及[Binance USD-M市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。官方字段不是成交/盈利/容量证据；数据边界、字节/SHA及实现哈希见plan/data_manifest。

预检family ID含大写导致freeze失败，依赖plan的initial检查随之失败；两次原始命令和无实际结果事实均保留，preflight_evidence保存无效spec/生成器。修正ID后freeze_retry1与initial_retry1实际退出0，再预登记。失败期间0reserve/0实际市场回测；合成负对照与SMA窗口、future不可见、两向反转、入退场等号、S/E18邻域、原始权重/非平均DD/错位轴拒绝检查通过。33来源文件在首个reserve前绑定。计数检查曾先于verification.json就绪，改为审计成功后counts_retry1；附加同E控制汇总曾假设旧report含E，改读原始spec已验证的ETH_exit_buffer_fraction。两次后处理失败及重试保留，不改金融report或重算净值。

全部18项分三批reserve成功才计算27原生+27组合成本路径，独立Fraction慢均值/快信号、Decimal真实q/费用/资金费/小时风险及完整NAV核验后逐项finish，完整负结果同样保存。没有已完成市场回测重跑、没有据结果扩网格或松判据。

原SMA65和single账户续14:30→16:30；原L4/H2续16:10→18:10，仅18:11参考闭合后采集。single本轮独立取得16资金费，按本账户BTC−0.012计算；L4此前已计16，本轮不得重复。原规则/本金/持仓、risk/context/完整账本前缀和终止日不变，不采纳新SMA研究。原SMA65上下文源20261103T020232Z保留，partial不冒充180日/六折资格。旧延迟shadow与十策略报价模拟分开。

只清理本轮可重建中间物；完整账本、登记、冻结规则、原始短窗响应、全部真实结果和核验代码保留。同main排他锁内生成只读监控并非强制push，远端完整tree/实际终态及解锁凭据见.git/automation_proofs/20261103T180801Z.json。

封存：18新定义/54成本场景分别finish，9新组合通过0、淘汰9；9新原生通过0、淘汰9。独立核验9990新信号决策、27新原生成本曲线及27新父曲线，全部新NAV29430702点，核验计数{'funding': 49950, 'fills': 2172, 'rejects': 0, 'metric_checks': 1008, 'margin_checks': 158928}。18旧原生成本曲线只读核验，其资金费/成交是旧账本记录；新原生资金费29970条、成交1476笔来自本轮实际历史模拟。0新BTC/基准/父订单。27新ID/54追加事件；29869旧保护文件不变。

九个新组合对预设旧强逆势控制全成本NAV同路径0/9。同网格别名另存；旧endpointROC逆势L4/S28控制E0.375/0.5/0.625%不混入新SMA门槛S/E邻域，旧canonical状态保持，前轮慢窗交叉不足仍有效。没有因本批年度正收益而扩大参数、改门槛、修改实测账户或声称独立未来资格。

原SMA续2026-11-03T14:30:00Z至2026-11-03T16:30:00Z，NAV46983+120=47103、累计47069分钟/32完整日；single续2026-11-03T14:30:00Z至2026-11-03T16:30:00Z，NAV11324、累计279ID；L4/H2续2026-11-03T16:10:00Z至2026-11-03T18:10:00Z，仅18:11参考闭合后采集，NAV4061、累计102ID。新资金费single=[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0.09319716000000000000000000000', 'amount_usdt': '0.09319716000000000000000000000', 'mark': '77664.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0.09319716000000000000000000000', 'amount_usdt': '0.09319716000000000000000000000', 'mark': '77664.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0.09319716000000000000000000000', 'amount_usdt': '0.09319716000000000000000000000', 'mark': '77664.30000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2298.67000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2298.67000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793721600001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2298.67000000', 'rate': '0.00010000'}]、L4=[]，成交single=0、L4=0，0新日决策。所有book/risk/context/NAV前缀连续；single本轮独立以其-.012持仓计算16资金费，L4此前已按-.006入账，两者都不重复00/08/16。partial不冒充180日/六折，不采纳新研究规则。

监控通过：9210研究行、9192旧完整行不变，10报价账户/238观察，gzip4200414字节。实际HTTP/传输失败1次，初次官方网页访问失败及成功重试均保留。两次预登记前freeze/initial工程失败与两次counts/summary后处理失败均留档，修正后必要pipeline实际退出0；金融report/净值不变且无市场回测重跑。双重加权负对照exit1，正确资本/收益/DD与错位事件轴拒绝、未来价格不可见/双向逆势/SMA窗口与ROC端点区分/入退场等号及18邻域检查通过。0已完成回测或观察重跑。清理0真实结果/完整账本，无本轮可重建缓存遗留。

完整正负场景、逐折/全曲线DD、spec/代码/数据和NAV哈希、完整账本、原始短窗响应及失败事实保留。main非强制push、完整远端tree与实际终态/解锁凭据见.git/automation_proofs/20261103T180801Z.json。
