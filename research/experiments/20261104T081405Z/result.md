本轮无合格新候选：有限指数均值斜率S16/24/28×间隔D1/3/5的9个ETH原生与9个BTC/ETH组合全部rejected。三项验证均完成：连续370日walk-forward与逐折/近期核验；S/D敏感性严格近期邻域合格比例全部0%，未通过；1/2/3倍成本下54/54全期净正。组合三倍收益3.8770%～10.7503%、连续整体DD2.2933%～4.1489%，近期仅3–5/8个盈利五日折；原生仅1–3/8，部分完整月/近期净正门槛也失败。所有正负折保留，已知开发历史正收益不代表稳定实盘盈利。

有限指数均值斜率门槛 S/D 联合验证

先前价格相对均值水平门槛及退出缓冲变化仍近期失败。本轮用有限指数均值过去D日斜率方向替代价格/均值水平：期望在较大趋势仍上升的回落中保留逆势入场，检验过早过滤问题。固定快L5/H2%、E0.5%、V10/cap4.5%及本金/预算，事前S16/24/28×D1/3/5九格，9新原生+9新组合先reserve。旧水平S16/24门槛只读，S28与S24参考有窗口差异，不作孤立斜率因果声称；已知开发历史探索，不是独立未来/最终测试。

完整读取27100事件/13428ID、297份结论；初始16项有原始实际证据、缺结果0。此前研究定义9739、标实际9526、未标213，不把全部登记当全部回测。反复使用开发历史存在多重选择偏差。

事前固定S16/24/28×斜率间隔D1/3/5，快L5/H2%、退出E0.5%、entry-only V10/cap4.5%。r=C[i−1]/C[i−6]−1，r>2%做空、r<−2%做多，入场等号不触发；否则实际多仓仅r<E保留、空仓仅r>−E保留，退出等号flat。M(i,S)=sum(beta^j×C[i−1−j])/sum(beta^j)，j=0..S−1、beta=(S−1)/(S+1)；gate=sign(M(i,S)/M(i−D,S)−1)。两窗口都严格来自完整过去日收盘，历史窗口结束于i−1−D。它是有限均值斜率，不是价格/均值水平或ROC端点。零/相反方向flat；波动过滤只作用于新增/反向仓，不单独退出同方向已有仓。

最大S28+D5需要33个完整历史日，现有起点上下文恰好足够，最早旧窗口用到index0；合成测试核对该边界及未来/窗口外价格不可见。所有18新配置在任何行情估值前分8+8+2预留成功。9新ETH原生+9新组合，旧BTC和水平门槛只读，不重跑既有政策或改变旧资格。

原生ETH本金15000/预算4500；父组合完整BTC3750/N500旧银行+ETH15000/N4500新银行，raw[1,1]、总本金18750、资本20/80%、初始名义2.6666666667/24%。不归一化组合权重、不缩放旧NAV/数量、不平均指标、不设父订单、调仓、转移或交叉保证金。8旧实际结果含5个原生/15成本路径只读，水平S16/24控制和同资本/预算常多持有基准保存，现金0%另列。S16/24窗口匹配；S28只能对比S24参考，窗口同时变化，不能把差异单独归因于斜率门槛或称alpha证明。

Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30完整日折+10日尾折，逐折不重置现金/持仓，整体DD使用完整分钟/事件净值。近期40日继承day330实际状态、8×5日。固定规则无拟合/标签、purge0，过去完整信号下一00:01原生OPEN执行，数量按过去收盘/LOT取整、反手先平后开、终点计成本平仓。已反复使用的开发历史不是未触碰最终测试或独立未来。

成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)，1/2/3倍执行与资金费支出，资金费收入不放大；实际settlement ns/rate/mark/heldq。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押和独立1%闭合小时不利mark风险代理核验。线性永续空头无需现货借币，不虚构借币费用。缺盘口/TCA、历史完整最大量/保证金层级、逐tick强平及容量证明，正回测不能称稳定实盘盈利。

固定门槛：所有成本全期净正；1倍>=9/12盈利完整月；各成本近期净正且>=6/8盈利五日折；3倍整体DD<=25%；S/D索引半径1含中心，邻域3倍正与严格近期合格比例均>=60%；>=4底层平仓、毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat、>=180日。原生与父组合分开裁定，看到结果后不改门槛或扩本批网格。

|新配置|scope|S日数|D日数|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|fewmSlope_ETH_S16_D1_L5_H200bp_E5000ppm|native|16|1|11.748039|10.650265|9.552747|2.699702|11|2/2/2|rejected|
|fewmSlope_ETH_S16_D3_L5_H200bp_E5000ppm|native|16|3|8.324894|6.975241|5.626680|4.322467|6|2/2/2|rejected|
|fewmSlope_ETH_S16_D5_L5_H200bp_E5000ppm|native|16|5|11.709906|10.055114|8.401379|4.184786|7|2/2/2|rejected|
|fewmSlope_ETH_S24_D1_L5_H200bp_E5000ppm|native|24|1|12.125867|10.832029|9.538063|3.119962|9|2/2/2|rejected|
|fewmSlope_ETH_S24_D3_L5_H200bp_E5000ppm|native|24|3|11.380252|9.779581|8.179534|3.708613|9|1/1/1|rejected|
|fewmSlope_ETH_S24_D5_L5_H200bp_E5000ppm|native|24|5|16.134852|14.510651|12.887008|4.023287|9|2/2/2|rejected|
|fewmSlope_ETH_S28_D1_L5_H200bp_E5000ppm|native|28|1|13.743820|12.238018|10.732572|3.569029|10|3/3/3|rejected|
|fewmSlope_ETH_S28_D3_L5_H200bp_E5000ppm|native|28|3|7.695858|5.995251|4.295288|4.692796|9|2/2/2|rejected|
|fewmSlope_ETH_S28_D5_L5_H200bp_E5000ppm|native|28|5|16.044737|14.406502|12.768806|4.287013|10|3/3/3|rejected|
|fewmSlope_parent_BTC500_ETHS16_D1|parent|16|1|10.093351|9.088043|8.082930|2.293277|12|6/6/5|rejected|
|fewmSlope_parent_BTC500_ETHS16_D3|parent|16|3|7.354836|6.148024|4.942076|3.324075|8|6/6/5|rejected|
|fewmSlope_parent_BTC500_ETHS16_D5|parent|16|5|10.062845|8.611922|7.161835|3.229900|8|6/6/5|rejected|
|fewmSlope_parent_BTC500_ETHS24_D1|parent|24|1|10.395614|9.233454|8.071182|2.768622|11|6/6/5|rejected|
|fewmSlope_parent_BTC500_ETHS24_D3|parent|24|3|9.799122|8.391496|6.984359|3.322284|10|5/5/3|rejected|
|fewmSlope_parent_BTC500_ETHS24_D5|parent|24|5|13.602802|12.176352|10.750338|3.647270|11|5/5/3|rejected|
|fewmSlope_parent_BTC500_ETHS28_D1|parent|28|1|11.689976|10.358246|9.026789|3.130656|11|6/6/5|rejected|
|fewmSlope_parent_BTC500_ETHS28_D3|parent|28|3|6.851607|5.364032|3.876962|4.148919|10|5/5/3|rejected|
|fewmSlope_parent_BTC500_ETHS28_D5|parent|28|5|13.530710|12.093033|10.655777|3.895882|11|5/5/4|rejected|

新组合通过0、淘汰9；新原生独立状态列上。逐项失败{'fewmSlope_ETH_S16_D1_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_ETH_S16_D3_L5_H200bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_ETH_S16_D5_L5_H200bp_E5000ppm': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_ETH_S24_D1_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_ETH_S24_D3_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_ETH_S24_D5_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_ETH_S28_D1_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_ETH_S28_D3_L5_H200bp_E5000ppm': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_ETH_S28_D5_L5_H200bp_E5000ppm': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS16_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS16_D3': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS16_D5': ['nine_of_twelve_positive_complete30d_1x_folds', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS24_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS24_D3': ['recent40_positive_all_costs', 'recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS24_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS28_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS28_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'fewmSlope_parent_BTC500_ETHS28_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct']}。同路径别名和相对预定水平参考的变化另存，不把相同路径当独立收益来源，S28参考窗口差异明确。

11CSV保留54新成本场景、702月/尾折、432近期折、20034日NAV、两个九格S/D面、6旧水平参考场景、72相邻边、27持有/现金比较、42新旧原生成本路径和10资金配置。全部正负折、完整DD/Sharpe/Calmar、成本及成交数保留。边界最高Sharpe和相邻cliff只是依赖样本的描述性诊断，不是DSR/PBO显著性或新增裁定门槛。

2026-11-04UTC读取 [Pandas官方EWM公式](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)。斜率门槛是本项目事前假设，不从文档移植收益。[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)当前网页抓取三次超时，失败留档；本日此前已核实其字段，本轮必须以实际公开API响应取得资金费/mark/闭合bar并独立验证，不推定任何数值。原始8行情/mark/资金费/约束文件及新旧spec/report/archive/code版本/字节/SHA见plan/data_manifest。

33研究源码首个reserve前绑定，native simulate函数AST保持，只有ETH信号门槛改为S/D斜率。独立整数权重合成检查分辨斜率与价格/均值水平，覆盖S28+D5最早上下文、未来/窗口外不可见、等号/波动过滤、18邻域及错位轴/错误权重拒绝；独立Fraction Horner双窗口与Decimal逐笔成本/资金费/风险、完整NAV审计后逐配置finish。

原SMA65与single续Nov4UTC04:30→06:30，L4续06:10→08:10并实际跨08资金费。L4需抓取真正结算ns/rate/mark和自身持仓派生现金流，不固定时间或复制single金额、不重复00资金费；无新日决策。三账户原规则/本金、risk/context/完整NAV前缀保留，不强制截点平仓、不采纳本批斜率研究。SMA65日线上下文源20261104T021133Z/forward_inputs.json.gz保留；下一single 06:30→08:30仍须独立处理自己的08资金费，不复制L4半份BTC现金流。partial不冒充180日/六折，旧延迟shadow与十策略报价模拟分开。

仅清理当前可重建中间物；真实结果、完整账本、冻结规则、登记、原始短窗/失败事实及必要代码保留。同main排他锁内更新只读监控并非强制push；真实发布终态/远端完整tree/blob哈希及解锁凭据见.git/automation_proofs/20261104T081405Z.json。

封存：18新金融配置/54成本场景逐项finish，组合通过0、淘汰9，原生通过0。新原生决策9990次、资金费29970条、成交1500笔；旧15成本账本资金费16650条、成交342笔是旧记录。独立核验{'funding': 46620, 'fills': 1842, 'rejects': 0, 'metric_checks': 966, 'margin_checks': 139566}，0父订单。27新ID/54追加事件，31885旧保护文件不变。

原SMA续2026-11-04T04:30:00Z至2026-11-04T06:30:00Z，NAV47824+120=47944，累计47909分钟。single续2026-11-04T04:30:00Z至2026-11-04T06:30:00Z，NAV12061+122=12183，累计300ID。L4续2026-11-04T06:10:00Z至2026-11-04T08:10:00Z，真实08资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0.04687187678260800000000000000', 'amount_usdt': '0.04687187678260800000000000000', 'mark': '78119.79463768', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0.04687187678260800000000000000', 'amount_usdt': '0.04687187678260800000000000000', 'mark': '78119.79463768', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0.04687187678260800000000000000', 'amount_usdt': '0.04687187678260800000000000000', 'mark': '78119.79463768', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2303.08556589', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2303.08556589', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793779200000000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2303.08556589', 'rate': '0.00010000'}]，NAV4798+124=4922，累计123ID。三账户新日决策/成交SMA 0/0、single 0/0、L4 0/0。原规则/本金和完整前缀保留，partial不冒充180日/六折，不采纳本批斜率研究。

监控通过：9316研究行，9298旧完整行不变，10报价账户/245观察，gzip4261003字节。恢复后必要检查实际退出0；公共HTTP/传输失败1次及文档网页三次超时均留档。文档抓取仍不可用，本日原已核实字段及本轮真正API响应完成数据依赖核验，未推定金额。一次画图轴索引失败及原脚本/traceback保留，saved-metric导出重试实际0；没有重新计算金融结果。0已完成金融/观察重跑，清理0真实结果/账本，零可重建缓存遗留。

全部正负折/逐变体、完整DD、spec/report/archive/数据/代码SHA、真实短窗与失败证据保留。main非强制push、完整远端tree/blob及真实终态/解锁凭据见.git/automation_proofs/20261104T081405Z.json。
