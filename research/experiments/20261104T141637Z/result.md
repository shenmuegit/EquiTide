本轮新组合通过0/9，9个原生通过0/9。三项验证已完成：连续370日walk-forward；K/D二维敏感性；1/2/3倍成本压力。54场景全期净正54/54。组合3倍净收益8.304645%～15.021479%，连续整体DD3.437378%～3.899731%。严格近期条件通过组合0/9、原生0/9；最终裁定逐项见下。已知开发历史的正收益不能称稳定实盘盈利。

有限指数均值趋势门槛仅作用新开仓/反手，K 与 D 联合验证

上轮相同K/D的全持仓趋势门槛在中性或反向斜率时立即退出，近期未过关。本轮事前只改门槛作用范围：仅新开仓或反手检查严格趋势门槛，已有仓位只按原快ROC退出/反转规则决定。K=.00025/.0005/.00075 × D1/3/5固定，S24/L5/H.02/E.005/V10/cap.045、本金预算和成本不变。9新原生+9组合先reserve，9个相同K/D旧全持仓门槛逐格只读。检验减少门槛诱发退出是否改善连续性与近期稳定；不在本批结果后调网格/门槛，不将复用历史称独立最终/未来。

完整读取27322事件/13539ID、300份既往结论，另完整读取三技能/README/既有OOS检查及原始freqtrade ZIP。初始16项均有实际证据、缺结果0。此前研究定义9793、标实际9580、未标213；不把全部登记当已有回测。反复使用开发历史存在多重选择偏差。

预先固定S24、快L5/H2%、退出E0.5%、entry-only V10/cap4.5%；K=0.025/0.05/0.075% × D1/3/5九格。r=C[i−1]/C[i−6]−1，严格r>H空、r<−H多，否则实际多仓只在r<E保留、空仓只在r>−E保留；等号不触发新入场；r=E时多仓退出、r=−E时空仓退出。M(i,24)=sum(beta^j×C[i−1−j])/sum(beta^j)，j0..23、beta23/25；s=M(i,24)/M(i−D,24)−1。gate仅s>K为+1、s<−K为−1，其余及等号0。仅base非零且不同于实际持仓时检查base==gate，覆盖新开仓及反手；不匹配则flat。base等于已有实际方向时，保留原仓，独立于中性/反向趋势；base为0仍按快ROC退出。失败反手先平旧仓且不开新仓。波动过滤仅用于新增/反向仓，原方向不因单独高波动退出。

最多29个完整过去日足够本批窗口，源已有33日上下文；两有限均值、快ROC和vol都不看当前/未来数据。独立整数权重核与不同Horner递推核交叉验证，含K正负等号/微扰、入退等号、未来/窗口外不可见。18新配置全部8+8+2预留成功才估值，不重跑旧结果。

原生ETH本金15000/预算4500。组合完整BTC3750/N500旧银行+ETH15000/N4500新银行，raw[1,1]、总本金18750、资本20/80%、初始名义占比2.6666666667/24%。组合权重不归一化，不缩放旧NAV/数量，不平均指标，不设父订单、调仓、转移或交叉保证金。22旧实际结果含12原生/36成本路径只读；9个全持仓门槛参考的S24/K/D逐格匹配。常多持有同本金/预算、现金0%另列。仅门槛作用范围不同的历史差异为描述性对照，不是独立alpha证明。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30完整日折+10日尾折，逐折不重置现金或持仓。近期40日继承day330实际状态、8×5日；整体DD从完整分钟/事件净值计算。固定规则无拟合/标签、purge0；过去信号下一00:01原生OPEN、LOT数量取整、反手先平后开、终点计成本平仓。反复研究历史不是未触碰最终留出，也不是独立未来。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍执行与资金费支出，资金费收入不放大；实际结算ns/rate/mark/heldq。逐笔检查LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押，及独立1%闭合小时不利mark风险代理。线性永续空头无现货借币，不虚构借币费。缺盘口/TCA、完整历史层级/最大量、逐tick强平与容量证明。

固定门槛保持：所有成本全期净正；1倍>=9/12盈利完整月；各成本近期净正且>=6/8盈利五日折；3倍整体DD<=25%；K/D索引半径1含中心、邻域3倍正与严格近期比例均>=60%；>=4原生平仓、毛参考PnL+资金费/执行成本>=2.5；0现金/订单/保证金代理违规、终点flat、>=180日。原生和组合分开裁定，不按本批结果放宽门槛或扩网格。

|新配置|scope|K比例|D日数|1x净收益%|2x净收益%|3x净收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|fewmEntryOnly_ETH_S24_K250ppm_D1_L5_H200bp_E5000ppm|native|0.00025|1|12.500989|11.165416|9.829892|4.563073|11|2/2/2|rejected|
|fewmEntryOnly_ETH_S24_K250ppm_D3_L5_H200bp_E5000ppm|native|0.00025|3|17.632765|16.054131|14.476182|4.446411|10|2/2/2|rejected|
|fewmEntryOnly_ETH_S24_K250ppm_D5_L5_H200bp_E5000ppm|native|0.00025|5|21.613076|19.919299|18.225934|4.446411|11|3/3/3|rejected|
|fewmEntryOnly_ETH_S24_K500ppm_D1_L5_H200bp_E5000ppm|native|0.0005|1|12.768359|11.598182|10.427955|3.940555|10|2/2/2|rejected|
|fewmEntryOnly_ETH_S24_K500ppm_D3_L5_H200bp_E5000ppm|native|0.0005|3|17.632765|16.054131|14.476182|4.446411|10|2/2/2|rejected|
|fewmEntryOnly_ETH_S24_K500ppm_D5_L5_H200bp_E5000ppm|native|0.0005|5|21.613076|19.919299|18.225934|4.446411|11|3/3/3|rejected|
|fewmEntryOnly_ETH_S24_K750ppm_D1_L5_H200bp_E5000ppm|native|0.00075|1|12.748343|11.578713|10.409032|3.940555|10|2/2/2|rejected|
|fewmEntryOnly_ETH_S24_K750ppm_D3_L5_H200bp_E5000ppm|native|0.00075|3|17.632765|16.054131|14.476182|4.446411|10|2/2/2|rejected|
|fewmEntryOnly_ETH_S24_K750ppm_D5_L5_H200bp_E5000ppm|native|0.00075|5|19.279139|17.648268|16.017934|4.446411|10|2/2/2|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K250ppm_D1|parent|0.00025|1|10.695712|9.500164|8.304645|3.899731|12|6/6/5|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K250ppm_D3|parent|0.00025|3|14.801133|13.411136|12.021677|3.819103|11|5/5/4|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K250ppm_D5|parent|0.00025|5|17.985381|16.503270|15.021479|3.819103|12|5/5/4|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K500ppm_D1|parent|0.0005|1|10.909607|9.846377|8.783096|3.437378|11|6/6/5|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K500ppm_D3|parent|0.0005|3|14.801133|13.411136|12.021677|3.819103|11|5/5/4|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K500ppm_D5|parent|0.0005|5|17.985381|16.503270|15.021479|3.819103|12|5/5/4|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K750ppm_D1|parent|0.00075|1|10.893595|9.830801|8.767957|3.437378|11|6/6/5|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K750ppm_D3|parent|0.00075|3|14.801133|13.411136|12.021677|3.819103|11|5/5/4|rejected|
|fewmEntryOnly_parent_BTC500_ETHS24_K750ppm_D5|parent|0.00075|5|16.118231|14.686446|13.255079|3.819103|11|5/5/4|rejected|

逐项失败：{'fewmEntryOnly_ETH_S24_K250ppm_D1_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_ETH_S24_K250ppm_D3_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_ETH_S24_K250ppm_D5_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_ETH_S24_K500ppm_D1_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_ETH_S24_K500ppm_D3_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_ETH_S24_K500ppm_D5_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_ETH_S24_K750ppm_D1_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_ETH_S24_K750ppm_D3_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_ETH_S24_K750ppm_D5_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K250ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K250ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K250ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K500ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K500ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K500ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K750ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K750ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmEntryOnly_parent_BTC500_ETHS24_K750ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。旧全持仓门槛参考的criteria、sensitivity与status原样保留；本批同路径别名另存，不将相同实现路径当独立收益来源。

11CSV保留54成本场景、702月/尾折、432近期折、20034日NAV、两个九格K/D面、27旧全持仓门槛参考场景、72相邻边、27持有/现金比较、63新旧原生成本路径与10资金配置。全部正负折、整体DD/Sharpe/Calmar、成本和成交数保留；边界最高Sharpe与相邻cliff为依赖样本描述，不是DSR/PBO显著性或新增资格门槛。

2026-11-04UTC读取 [Pandas官方EWM公式](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)（3.1.0）与 [Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。本轮资金费文档访问已恢复，核对fundingTime/fundingRate/markPrice定义；数值仍只能来自实际公开API响应。有限窗口与K门槛是项目预先假设，文档不提供盈利结论。8源行情/mark/资金费/约束文件与全部spec/report/archive/code SHA见plan/data_manifest。

33源码在首个reserve前绑定。原生simulate函数AST保持，只有ETH趋势门槛作用范围改变。独立Fraction信号、Decimal逐笔现金/成交/成本/资金费/小时风险、完整NAV及组合对齐守恒审计后逐配置finish。

原SMA65和single延续Nov4UTC10:30→12:30，L4延续12:10→14:10。资金费事件集均从本轮真实响应推导，08结算已处理，不固定假设新的资金费间隔或重复计入。三者没有新日决策，完整NAV前缀和原规则/本金/持仓/risk/context保持，不采纳本轮研究、不截点强平。SMA65完整日线上下文仍为20261104T021133Z/forward_inputs.json.gz。partial不冒充180日/六折，旧延迟shadow不冒充十策略报价模拟。

只清理本轮可重建中间物，完整结果/账本/冻结规则/登记/短窗原始响应及失败证据保留。等待共用锁、原owner释放后取得本轮锁；同main锁内更新只读监控，不新建部署或定时任务。真实发布终态见.git/automation_proofs/20261104T141637Z.json。

预声明同K/D对照：9个组合3倍净收益差为-0.708869～7.393658个百分点，其中8/9提高；整体DD差为0.171833～1.131109个百分点。保存的新原生决策中933次在趋势中性/反向时依快退出规则保留原仓，285次反手未过趋势门槛只平旧仓，证明规则变化实际生效。全期收益改善没有解决严格近期条件，不能据此采纳到冻结账户。新网格存在两组完整NAV别名（D3三格、D5两格），不是独立alpha；最高Sharpe在预设D5边界，未扩网格。

封存：18新金融配置/54成本场景逐项finish，组合通过0、淘汰9，原生通过0。新原生决策9990次、资金费29970条、成交1434笔；旧36成本账本资金费39960条、成交1572笔均是旧记录。独立审计{'funding': 69930, 'fills': 3006, 'rejects': 0, 'metric_checks': 1260, 'margin_checks': 203409}，0父订单。27新ID/54追加事件，32822旧保护文件不变。

原SMA续2026-11-04T10:30:00Z至2026-11-04T12:30:00Z，NAV48184+120=48304，累计48269分钟。single续2026-11-04T10:30:00Z至2026-11-04T12:30:00Z，NAV12429+122=12551，累计309ID；本窗实际新增资金费[]。L4续2026-11-04T12:10:00Z至2026-11-04T14:10:00Z，NAV5166+122=5288，累计132ID，本窗资金费[]，不重复上轮08结算。三者新日决策/成交SMA 0/0、single 0/0、L4 0/0。原规则/本金与完整前缀保留，partial不冒充180日/六折，不采纳本批研究。

监控通过：9370研究行，9352旧完整行不变，10报价账户/248观察，gzip4286545字节。必要管线命令均实际退出0，HTTP/传输失败1次全部保留；取得共用锁后写入，官方文档本轮读取成功，实际资金费字段/现金流已核验。0已完成金融/观察重跑，清理0真实结果/账本，零可重建缓存遗留。

全部正负折/逐变体、完整DD、spec/report/archive/数据/代码SHA、真实短窗及失败证据保留。main非强制push、完整远端tree/blob及实际终态/解锁凭据见.git/automation_proofs/20261104T141637Z.json。
