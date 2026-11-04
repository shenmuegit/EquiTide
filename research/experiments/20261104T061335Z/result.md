本轮无合格新候选：S16/24/32×退出缓冲0.375/0.5/0.625%批次中，8个新ETH原生与8个新组合全部rejected；两个已有S32/E0.5%格只读、原资格不变。三项验证均实际完成：连续370日walk-forward；S/E敏感性严格近期邻域合格比例均0%，未通过；1/2/3倍成本48/48全期净正。新组合三倍收益2.9203%～10.3510%、整体DD2.1650%～2.4236%，近期仅3–5/8个盈利五日折；原生0或2/8，S16三个配置的近期总收益也未通过净正门槛。全部正负折及别名保留，不把重复开发历史的正收益称稳定实盘盈利。

有限指数加权窗口 S 与退出缓冲 E 联合验证

上轮EWM32快L/H变化全年净正但近期失败。本轮固定快L5/H2%、本金与预算，联合改变有限指数加权窗口S16/24/32和退出E0.375/0.5/0.625%，检验反应速度与持仓持续性变化；33日上下文足够最大窗口。已有S32/E0.5%原生及组合仅只读，不重测或重评旧资格，其他8原生+8组合先reserve。已知开发历史的继续假设探索，不称未触碰最终或独立未来，不按本批结果扩格/改门槛。

完整读取27030事件/13393ID、296份结论；初始16项实际证据完整、缺结果0。此前研究定义9723、标实际9510、未标213；不把全部登记当全部回测。多轮使用同一历史存在多重选择偏差。

事前固定L5/H2%、entry-only V10/cap4.5%，变更S16/24/32×E0.375/0.5/0.625%。r=C[i−1]/C[i−6]−1，r>2%做空、r<−2%做多，入场等号不触发；否则实际多仓仅r<E保留、空仓仅r>−E保留，退出等号flat。有限EWM(S)=sum(beta^j×C[i−1−j])/sum(beta^j)，j=0..S−1，beta=(S−1)/(S+1)，严格使用最后S个完整收盘。gate=sign(最新完整收盘/EWM−1)，零或相反方向flat；不是无限递推EMA。波动过滤只作用于新增/反向仓，原方向仓不因单独高波动退出。

两个九格面各含8新配置+1只读旧S32/E0.5%格。旧格的完整结果、状态、criteria与原敏感性不改，仅保存新S/E邻域的描述诊断，不重测、不重新finish旧格。16个新配置分8+8预留全部成功后实际计算。旧格已实际rejected，不因进入新邻域恢复资格。

ETH原生本金15000/预算4500；组合拥有完整BTC3750/N500旧银行+ETH15000/N4500银行，raw[1,1]、本金18750、资本20/80%、初始名义2.6666666667/24%。保留原权重，不归一化组合、不缩放旧NAV或数量、不平均指标、不设父订单/跨银行调仓/转移/交叉保证金。信号的时间权重归一化属于公式。6个旧实际结果中4个原生/12成本路径只读，包含旧EWM32格及同本金/预算常多持有，现金0%另列。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30完整日折+10日尾折，逐折不重置现金/仓位；整体DD使用完整分钟/事件净值。近期40日继承day330状态、8×5日。固定规则无拟合/标签、purge0，33日线上下文足够最大S32，下一00:01原生OPEN、数量按过去收盘/LOT取整、反手先平后开、终点计成本平仓。反复使用的开发历史不是未触碰最终测试或独立未来。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)，1/2/3倍执行及资金费支出、资金费收入不放大；实际settlement ns/rate/mark/heldq。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押和独立1%闭合小时不利mark保证金代理逐笔核验。永续空头无现货借币，不虚构借币费。缺盘口/TCA、完整历史层级/最大量、逐tick强平及容量证明，回测净正不能称稳定实盘盈利。

固定门槛：所有成本全期净正；1倍>=9/12正完整月；各成本近期净正且>=6/8正五日折；3倍整体DD<=25%；S/E索引半径1含中心，3倍正与严格近期合格比例均>=60%；>=4底层平仓，毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat、>=180日。只裁定新16项，不据本批结果扩格或放宽门槛。

|新配置|scope|S日数|E比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|fewmSE_ETH_S16_E3750ppm_L5_H200bp|native|16|0.00375|4.919813|4.009593|3.099471|2.629305|7|0/0/0|rejected|
|fewmSE_ETH_S16_E5000ppm_L5_H200bp|native|16|0.005|4.919813|4.009593|3.099471|2.629305|7|0/0/0|rejected|
|fewmSE_ETH_S16_E6250ppm_L5_H200bp|native|16|0.00625|5.052158|4.137080|3.221928|2.629305|7|0/0/0|rejected|
|fewmSE_ETH_S24_E3750ppm_L5_H200bp|native|24|0.00375|14.539102|13.393938|12.248898|2.512789|11|2/2/2|rejected|
|fewmSE_ETH_S24_E5000ppm_L5_H200bp|native|24|0.005|14.539102|13.393938|12.248898|2.512789|11|2/2/2|rejected|
|fewmSE_ETH_S24_E6250ppm_L5_H200bp|native|24|0.00625|14.687895|13.537879|12.387816|2.512789|11|2/2/2|rejected|
|fewmSE_ETH_S32_E3750ppm_L5_H200bp|native|32|0.00375|14.683403|13.335614|11.987976|2.801219|10|2/2/2|rejected|
|fewmSE_ETH_S32_E6250ppm_L5_H200bp|native|32|0.00625|14.843223|13.486738|12.130101|2.801219|10|2/2/2|rejected|
|fewmSE_parent_BTC500_ETHS16_E3750ppm|parent|16|0.00375|4.630770|3.775506|2.920309|2.245860|9|3/3/3|rejected|
|fewmSE_parent_BTC500_ETHS16_E5000ppm|parent|16|0.005|4.630770|3.775506|2.920309|2.245860|9|3/3/3|rejected|
|fewmSE_parent_BTC500_ETHS16_E6250ppm|parent|16|0.00625|4.736646|3.877495|3.018275|2.245860|9|3/3/3|rejected|
|fewmSE_parent_BTC500_ETHS24_E3750ppm|parent|24|0.00375|12.326202|11.282981|10.239850|2.165000|12|6/6/5|rejected|
|fewmSE_parent_BTC500_ETHS24_E5000ppm|parent|24|0.005|12.326202|11.282981|10.239850|2.165000|12|6/6/5|rejected|
|fewmSE_parent_BTC500_ETHS24_E6250ppm|parent|24|0.00625|12.445236|11.398135|10.350985|2.165000|12|6/6/5|rejected|
|fewmSE_parent_BTC500_ETHS32_E3750ppm|parent|32|0.00375|12.441642|11.236322|10.031112|2.423574|11|6/6/5|rejected|
|fewmSE_parent_BTC500_ETHS32_E6250ppm|parent|32|0.00625|12.569499|11.357222|10.144813|2.423574|11|6/6/5|rejected|

新组合通过0、淘汰8；新原生独立状态列上。失败明细{'fewmSE_ETH_S16_E3750ppm_L5_H200bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_ETH_S16_E5000ppm_L5_H200bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_ETH_S16_E6250ppm_L5_H200bp': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_ETH_S24_E3750ppm_L5_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_ETH_S24_E5000ppm_L5_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_ETH_S24_E6250ppm_L5_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_ETH_S32_E3750ppm_L5_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_ETH_S32_E6250ppm_L5_H200bp': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_parent_BTC500_ETHS16_E3750ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_parent_BTC500_ETHS16_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_parent_BTC500_ETHS16_E6250ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_parent_BTC500_ETHS24_E3750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_parent_BTC500_ETHS24_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_parent_BTC500_ETHS24_E6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_parent_BTC500_ETHS32_E3750ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSE_parent_BTC500_ETHS32_E6250ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。旧S32/E0.5%格的原资格不变；同路径别名及相对预定参考的变化另存，S/E不同不能称参数匹配比较或独立收益来源。

11CSV保存48新场景、624月/尾折、384近期折、17808日NAV、两个九格S/E面(各含只读旧格)、3旧参考场景、72相邻边、27同资本持有/现金比较、36新旧原生成本路径与10资金配置。所有正负折、完整DD/Sharpe/Calmar和成本/成交数保留；边界峰值与相邻cliff仅为依赖样本描述，不是DSR/PBO显著性或新门槛。

2026-11-04UTC读取 [Pandas官方EWM公式](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html) 与 [Binance USD-M市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。有限窗口是项目预设变体，不从文档移植收益或成交能力。8行情/mark/资金费/约束文件、全部源与新spec/report/archive/code版本SHA见plan/data_manifest。

33研究源码在首个reserve前绑定。预登记前仅更正继承stdout的18→16数量文字，并保留初始与刷新绑定；无金融规则/参数改变或已完成回测重跑。合成检查覆盖独立整数EWM核、S/E等号、窗口外/未来数据不可见、18邻域、旧格元数据保留与错位轴/错误权重拒绝。独立Fraction Horner信号与Decimal成本/资金费/风险/完整NAV审计后逐配置finish。

原SMA65与single续Nov4UTC02:30→04:30，L4续04:10→06:10；延续原规则/本金、逐成本状态、risk/context及完整NAV前缀，不重复已处理的午夜决策/资金费，不采纳本批S/E。SMA65完整日线上下文源20261104T021133Z/forward_inputs.json.gz保留。下一L4窗口06:10→08:10将跨08资金费，须在08:11闭合后抓取实际结算ns/rate/mark及自身持仓入账，不在本轮预算或复制single金额。partial不冒充180日/六折；旧延迟shadow与十策略报价模拟分开。

只清理本轮可重建中间物；真实结果、完整账本、冻结规则、登记、原始短窗/失败事实与必要代码均保留。同main排他锁更新只读监控并非强制push；实际发布终态/远端完整tree和blob哈希/解锁凭据见.git/automation_proofs/20261104T061335Z.json。

封存：16新金融配置/48成本场景逐项finish，组合通过0、淘汰8，原生通过0。旧S32/E0.5%原生及组合只读，未再次reserve/finish/裁定。新原生决策8880次、资金费26640条、成交984笔；旧12成本账本资金费13320条、成交264笔均为旧记录。独立核验{'funding': 39960, 'fills': 1248, 'rejects': 0, 'metric_checks': 840, 'margin_checks': 119817}，0父订单。25新ID/50追加事件，31596旧保护文件不变。

原SMA续2026-11-04T02:30:00Z至2026-11-04T04:30:00Z，NAV47704+120=47824，累计47789分钟。single续2026-11-04T02:30:00Z至2026-11-04T04:30:00Z，NAV11939+122=12061，累计297ID。L4续2026-11-04T04:10:00Z至2026-11-04T06:10:00Z，NAV4798，累计120ID。三账户新日决策/成交SMA 0/0、single 0/0、L4 0/0；资金费single []、L4 []。原规则/本金与完整前缀保留，partial不冒充180日/六折，不采纳本批S/E。

监控通过：9298研究行，9282旧完整行不变，10报价账户/244观察，gzip4249785字节。必要实际命令均退出0；公共HTTP/传输失败1次及其他实际错误留档，0已完成金融/观察重跑。清理0真实结果/账本，零可重建缓存遗留。

全部正负折/逐变体、完整DD、spec/report/archive/数据/代码SHA、真实短窗/失败证据保留。main非强制push、完整远端tree/blob及实际终态/解锁凭据见.git/automation_proofs/20261104T061335Z.json。
