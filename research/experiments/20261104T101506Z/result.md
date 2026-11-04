本轮新组合通过0/9，9个原生通过0/9。三项验证已完成：连续370日walk-forward；K/D二维敏感性；1/2/3倍成本压力。54场景全期净正54/54。组合3倍净收益2.301183%～10.595769%，连续整体DD1.773982%～3.647270%。严格近期条件通过组合0/9、原生0/9；最终裁定逐项见下。已知开发历史的正收益不能称稳定实盘盈利。

有限指数均值斜率强度 K 与间隔 D 联合验证

上轮仅按有限指数均值斜率正负过滤仍近期失败。本轮固定S24及其他交易规则，预先给斜率增加0.1/0.2/0.3%的最小强度K，并联合D1/3/5，检验过滤弱趋势是否减少反复进出与成本、以及是否丢失收益。九格9新原生+9新组合先reserve；相同D的旧K0斜率结果只读。门槛和网格事前冻结，不按本批结果调节。已知开发历史探索，不是独立未来/最终测试。

完整读取27174事件/13465ID、298份既往结论，另完整读取三技能/README/既有OOS检查及原始freqtrade ZIP。初始16项均有实际证据、缺结果0。此前研究定义9757、标实际9544、未标213；不把全部登记当已有回测。反复使用开发历史存在多重选择偏差。

预先固定S24、快L5/H2%、退出E0.5%、entry-only V10/cap4.5%；K=0.1/0.2/0.3% × D1/3/5九格。r=C[i−1]/C[i−6]−1，严格r>H空、r<−H多，否则实际多仓只在r<E保留、空仓只在r>−E保留；入场/退出等号flat。M(i,24)=sum(beta^j×C[i−1−j])/sum(beta^j)，j0..23、beta23/25；s=M(i,24)/M(i−D,24)−1。gate仅s>K为+1、s<−K为−1，其余及等号0。raw逆势方向与gate不等即flat，含已有仓。波动过滤仅用于新增/反向仓，原方向不因单独高波动退出。

最多29个完整过去日足够本批窗口，源已有33日上下文；两有限均值、快ROC和vol都不看当前/未来数据。独立整数权重核与不同Horner递推核交叉验证，含K正负等号/微扰、入退等号、未来/窗口外不可见。18新配置全部8+8+2预留成功才估值，不重跑旧结果。

原生ETH本金15000/预算4500。组合完整BTC3750/N500旧银行+ETH15000/N4500新银行，raw[1,1]、总本金18750、资本20/80%、初始名义占比2.6666666667/24%。组合权重不归一化，不缩放旧NAV/数量，不平均指标，不设父订单、调仓、转移或交叉保证金。10旧实际结果含6原生/18成本路径只读；3个K0斜率参考的S24与D1/3/5逐格匹配。常多持有同本金/预算、现金0%另列。仅K不同的历史差异为描述性对照，不是独立alpha证明。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30完整日折+10日尾折，逐折不重置现金或持仓。近期40日继承day330实际状态、8×5日；整体DD从完整分钟/事件净值计算。固定规则无拟合/标签、purge0；过去信号下一00:01原生OPEN、LOT数量取整、反手先平后开、终点计成本平仓。反复研究历史不是未触碰最终留出，也不是独立未来。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍执行与资金费支出，资金费收入不放大；实际结算ns/rate/mark/heldq。逐笔检查LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押，及独立1%闭合小时不利mark风险代理。线性永续空头无现货借币，不虚构借币费。缺盘口/TCA、完整历史层级/最大量、逐tick强平与容量证明。

固定门槛保持：所有成本全期净正；1倍>=9/12盈利完整月；各成本近期净正且>=6/8盈利五日折；3倍整体DD<=25%；K/D索引半径1含中心、邻域3倍正与严格近期比例均>=60%；>=4原生平仓、毛参考PnL+资金费/执行成本>=2.5；0现金/订单/保证金代理违规、终点flat、>=180日。原生和组合分开裁定，不按本批结果放宽门槛或扩网格。

|新配置|scope|K比例|D日数|1x净收益%|2x净收益%|3x净收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|fewmStrength_ETH_S24_K1000ppm_D1_L5_H200bp_E5000ppm|native|0.001|1|14.582278|13.555406|12.528659|2.041551|11|2/2/2|rejected|
|fewmStrength_ETH_S24_K1000ppm_D3_L5_H200bp_E5000ppm|native|0.001|3|9.120282|7.581557|6.043552|3.715970|8|1/1/1|rejected|
|fewmStrength_ETH_S24_K1000ppm_D5_L5_H200bp_E5000ppm|native|0.001|5|15.836914|14.265014|12.693797|4.023287|9|1/1/1|rejected|
|fewmStrength_ETH_S24_K2000ppm_D1_L5_H200bp_E5000ppm|native|0.002|1|5.554861|4.996797|4.438879|2.041551|6|0/0/0|rejected|
|fewmStrength_ETH_S24_K2000ppm_D3_L5_H200bp_E5000ppm|native|0.002|3|12.602141|11.258907|9.915991|3.071782|9|2/2/2|rejected|
|fewmStrength_ETH_S24_K2000ppm_D5_L5_H200bp_E5000ppm|native|0.002|5|15.663848|14.145744|12.628161|4.023287|9|1/1/1|rejected|
|fewmStrength_ETH_S24_K3000ppm_D1_L5_H200bp_E5000ppm|native|0.003|1|2.999611|2.662421|2.325564|2.050018|4|0/0/0|rejected|
|fewmStrength_ETH_S24_K3000ppm_D3_L5_H200bp_E5000ppm|native|0.003|3|12.341498|11.046675|9.752171|3.076436|9|2/2/2|rejected|
|fewmStrength_ETH_S24_K3000ppm_D5_L5_H200bp_E5000ppm|native|0.003|5|15.663848|14.145744|12.628161|4.023287|9|1/1/1|rejected|
|fewmStrength_parent_BTC500_ETHS24_K1000ppm_D1|parent|0.001|1|12.360742|11.412156|10.463659|1.773982|11|6/6/5|rejected|
|fewmStrength_parent_BTC500_ETHS24_K1000ppm_D3|parent|0.001|3|7.991146|6.633076|5.275573|3.199004|9|5/5/3|rejected|
|fewmStrength_parent_BTC500_ETHS24_K1000ppm_D5|parent|0.001|5|13.364451|11.979842|10.595769|3.647270|11|5/5/3|rejected|
|fewmStrength_parent_BTC500_ETHS24_K2000ppm_D1|parent|0.002|1|5.138809|4.565268|3.991835|1.773982|9|3/3/3|rejected|
|fewmStrength_parent_BTC500_ETHS24_K2000ppm_D3|parent|0.002|3|10.776633|9.574956|8.373525|2.683949|10|6/6/5|rejected|
|fewmStrength_parent_BTC500_ETHS24_K2000ppm_D5|parent|0.002|5|13.225998|11.884426|10.543261|3.647270|11|5/5/3|rejected|
|fewmStrength_parent_BTC500_ETHS24_K3000ppm_D1|parent|0.003|1|3.094609|2.697768|2.301183|1.779863|9|3/3/3|rejected|
|fewmStrength_parent_BTC500_ETHS24_K3000ppm_D3|parent|0.003|3|10.568118|9.405171|8.242468|2.687248|10|6/6/5|rejected|
|fewmStrength_parent_BTC500_ETHS24_K3000ppm_D5|parent|0.003|5|13.225998|11.884426|10.543261|3.647270|11|5/5/3|rejected|

逐项失败：{'fewmStrength_ETH_S24_K1000ppm_D1_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_ETH_S24_K1000ppm_D3_L5_H200bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_ETH_S24_K1000ppm_D5_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_ETH_S24_K2000ppm_D1_L5_H200bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_ETH_S24_K2000ppm_D3_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_ETH_S24_K2000ppm_D5_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_ETH_S24_K3000ppm_D1_L5_H200bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_ETH_S24_K3000ppm_D3_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_ETH_S24_K3000ppm_D5_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K1000ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K1000ppm_D3': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K1000ppm_D5': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K2000ppm_D1': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K2000ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K2000ppm_D5': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K3000ppm_D1': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K3000ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmStrength_parent_BTC500_ETHS24_K3000ppm_D5': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。旧K0参考的criteria、sensitivity与status原样保留；本批同路径别名另存，不将相同实现路径当独立收益来源。

11CSV保留54成本场景、702月/尾折、432近期折、20034日NAV、两个九格K/D面、9旧K0参考场景、72相邻边、27持有/现金比较、45新旧原生成本路径与10资金配置。全部正负折、整体DD/Sharpe/Calmar、成本和成交数保留；边界最高Sharpe与相邻cliff为依赖样本描述，不是DSR/PBO显著性或新增资格门槛。

2026-11-04UTC读取 [Pandas官方EWM公式](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)（3.1.0）与 [Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。本轮资金费文档访问已恢复，核对fundingTime/fundingRate/markPrice定义；数值仍只能来自实际公开API响应。有限窗口与K门槛是项目预先假设，文档不提供盈利结论。8源行情/mark/资金费/约束文件与全部spec/report/archive/code SHA见plan/data_manifest。

33源码在首个reserve前绑定。原生simulate函数AST保持，只有ETH的最小斜率强度门槛改变。独立Fraction信号、Decimal逐笔现金/成交/成本/资金费/小时风险、完整NAV及组合对齐守恒审计后逐配置finish。

原SMA65和single延续Nov4UTC06:30→08:30，L4延续08:10→10:10。single窗口跨实际08资金费：取自身响应与q核算，不复制L4金额；L4的08结算已于上轮处理，不重复。三者没有新日决策，完整NAV前缀和原规则/本金/持仓/risk/context保持，不采纳本轮研究、不截点强平。SMA65完整日线上下文仍为20261104T021133Z/forward_inputs.json.gz。partial不冒充180日/六折，旧延迟shadow不冒充十策略报价模拟。

只清理本轮可重建中间物，完整结果/账本/冻结规则/登记/短窗原始响应及失败证据保留。锁等待保留真实失败后由原owner释放，未抢锁；同main锁内更新只读监控，不新建部署或定时任务。真实发布终态见.git/automation_proofs/20261104T101506Z.json。

元数据说明：report内current_grid_diagnostic_sensitivity.scope继承了旧“CurrentL/H”标签；实际变动轴由冻结plan及独立检查确认是K/D，L5/H2%固定，原report与已finish结果字节保留。完整指针链核验的实际累计观察single303、L4为126，原immutable observer的只读预检计数字段不作累计观测数。

封存：18新金融配置/54成本场景逐项finish，组合通过0、淘汰9，原生通过0。新原生决策9990次、资金费29970条、成交1188笔；旧18成本账本资金费19980条、成交618笔均是旧记录。独立审计{'funding': 49950, 'fills': 1806, 'rejects': 0, 'metric_checks': 1008, 'margin_checks': 139548}，0父订单。27新ID/54追加事件，32188旧保护文件不变。

原SMA续2026-11-04T06:30:00Z至2026-11-04T08:30:00Z，NAV47944+120=48064，累计48029分钟。single续2026-11-04T06:30:00Z至2026-11-04T08:30:00Z，NAV12183+124=12307，累计303ID；本轮实际08资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0.09374375356521600000000000000', 'amount_usdt': '0.09374375356521600000000000000', 'mark': '78119.79463768', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0.09374375356521600000000000000', 'amount_usdt': '0.09374375356521600000000000000', 'mark': '78119.79463768', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0.09374375356521600000000000000', 'amount_usdt': '0.09374375356521600000000000000', 'mark': '78119.79463768', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2303.08556589', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2303.08556589', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2303.08556589', 'rate': '0.00010000'}]。L4续2026-11-04T08:10:00Z至2026-11-04T10:10:00Z，NAV4922+122=5044，累计126ID，本窗资金费[]，不重复上轮08结算。三者新日决策/成交SMA 0/0、single 0/0、L4 0/0。原规则/本金与完整前缀保留，partial不冒充180日/六折，不采纳本批研究。

监控通过：9334研究行，9316旧完整行不变，10报价账户/246观察，gzip4270227字节。必要管线命令均实际退出0，HTTP/传输失败2次全部保留；初始锁忙等待后恢复，文档访问本轮已恢复，实际资金费字段/现金流已核验。0已完成金融/观察重跑，清理0真实结果/账本，零可重建缓存遗留。

全部正负折/逐变体、完整DD、spec/report/archive/数据/代码SHA、真实短窗及失败证据保留。main非强制push、完整远端tree/blob及实际终态/解锁凭据见.git/automation_proofs/20261104T101506Z.json。
