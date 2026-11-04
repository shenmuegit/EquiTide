本轮9新候选组合通过0/9，3个BTC金额组件通过0/3。另6个同金额持有组件/组合仅作基准，登记rejected不表示统一亏损。18金融配置/54成本场景全部实际执行。连续370日walk-forward、BTC金额/ETH间隔敏感性、1/2/3倍成本验证完成；组合3倍净收益9.409508%～17.881964%，整体DD3.689721%～6.030732%。严格近期组合通过1/9，BTC组件0/3。复用历史回测不是稳定实盘盈利。

上轮entry-only趋势门槛网格全期净正但近期未过，本轮不继续微调K或ETH规则。预设BTC实际入场预算1000/2000/3000USDT × 旧ETH斜率间隔D1/3/5，K.0005固定，检验增加BTC相对ETH敞口能否改善近期组合覆盖，且对相邻金额/间隔稳健。资本始终3750/15000、总18750，raw1/1不归一化；BTC自己实际重新LOT/冲击/资金费/抵押，ETH三个组件只读。每档同金额持有基准同批先登记。属于复用开发历史与多重选择后的新组合诊断，不是独立最终/未来或稳定实盘盈利。

完整读取27396事件/13576ID、301既往结论及三技能/README/OOS检查/原freqtradeZIP。初始16项都有真实证据、缺结果0。此前研究定义9811、标实际9598、未标213；不把全部登记称实际回测，重复开发存在多重选择偏差。

固定BTC原ROC31/H4%/E1%动量信号，仅变实际入场N1000/2000/3000；ETH复用上轮K0.05%、S24、L5/H2%/E0.5%、仅开仓/反手趋势门槛、V10/cap4.5%，D1/3/5三条原生净值。ETH不重新计算。BTC新金额与同金额恒定持有的LOT、成交量冲击和资金费独立实算；不会线性缩放旧NAV/数量。整个原生engine与上轮字节相同。

实际独立银行BTC3750+ETH15000、总18750，资本20/80%，原始权重[1,1]是两完整银行倍数，不归一化。BTC名义额占总本金5.333333/10.666667/16%，占BTC银行26.666667/53.333333/80%；ETH固定4500/18750=24%。以过去完整日收盘定LOT数量，下一UTC00:01原生OPEN成交，反手先平后开，同方向数量保持，终点计成本平仓。没有父级订单、资金转移、克隆银行、调仓或交叉保证金。

新6个BTC原生、9候选父组合、3匹配持有父组合全部18次reserve成功后才估值。10旧真实结果/6原生/18成本路径只读，包含旧BTCN500与相同ETHD/K候选；比较时明确BTC金额不同。每档N的BTC+ETH同本金/同入场金额持有对照和现金0%都报告。

时间2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日、12×30完整折+10尾折；近期40日从day330真实状态续接、8×5日，无折重开。过去上下文33日，BTC最大32、ETH最多29日；无拟合/标签，purge0，没有在测试期拟合权重。原历史已反复研究，不是未触碰最终测试或独立未来。全净值分钟/事件轴计算整体DD，逐折收益不平均代替整体。

成本5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍执行支出及资金费支出，收入不放大。实际结算ns/rate/mark/heldq；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押及1%闭合小时不利mark风险代理逐笔核验。线性永续无现货借币，不编造借币费；缺L2/TCA、完整历史层级/最大量、逐tick强平与真实容量证明。

预设判据不变：所有成本全期净正、1倍>=9/12正月；各成本近期净正且>=6/8正五日折；3倍整体DD<=25%；N/D索引半径1含中心，邻域3倍正与严格近期合格比例均>=60%；>=4原生平仓、毛参考PnL+资金费/执行成本>=2.5；0现金/订单/保证金代理违规、终点flat、>=180日。BTC新组件只按N一维敏感性，组合联合N/D二维；持有基准不属于候选。

|配置|角色|BTC N|ETH D|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
|mixbudget370_BTC_N1000_momentum|component|1000|None|7.984379|6.660050|5.335719|7.231400|9|4/4/4|rejected|
|mixbudget370_BTC_N2000_momentum|component|2000|None|16.234841|13.551979|10.869178|14.073445|9|4/4/4|rejected|
|mixbudget370_BTC_N3000_momentum|component|3000|None|24.667707|20.587143|16.506084|20.773534|9|4/4/4|rejected|
|mixbudget370_BTC_N1000_constantlong|benchmark_native|1000|None|-6.943073|-7.800425|-8.657804|14.975864|6|4/4/4|rejected|
|mixbudget370_BTC_N2000_constantlong|benchmark_native|2000|None|-13.886194|-15.601043|-17.315896|29.356064|6|4/4/4|rejected|
|mixbudget370_BTC_N3000_constantlong|benchmark_native|3000|None|-21.600895|-24.268513|-26.936137|44.677787|6|4/4/4|rejected|
|mixbudget370_parent_BTCN1000_ETHentryGateK500ppm_D1|candidate|1000|1|11.811563|10.610556|9.409508|3.689721|12|6/6/6|rejected|
|mixbudget370_parent_BTCN1000_ETHentryGateK500ppm_D3|candidate|1000|3|15.703088|14.175315|12.648089|4.247345|11|5/5/5|rejected|
|mixbudget370_parent_BTCN1000_ETHentryGateK500ppm_D5|candidate|1000|5|18.887336|17.267449|15.647891|4.247345|12|5/5/5|rejected|
|mixbudget370_parent_BTCN2000_ETHentryGateK500ppm_D1|candidate|2000|1|13.461655|11.988942|10.516200|4.215307|11|5/5/5|rejected|
|mixbudget370_parent_BTCN2000_ETHentryGateK500ppm_D3|candidate|2000|3|17.353180|15.553700|13.754781|5.118948|12|5/5/5|rejected|
|mixbudget370_parent_BTCN2000_ETHentryGateK500ppm_D5|candidate|2000|5|20.537429|18.645835|16.754583|5.118948|12|5/5/5|rejected|
|mixbudget370_parent_BTCN3000_ETHentryGateK500ppm_D1|candidate|3000|1|15.148228|13.395975|11.643581|4.904551|10|5/5/5|rejected|
|mixbudget370_parent_BTCN3000_ETHentryGateK500ppm_D3|candidate|3000|3|19.039754|16.960733|14.882162|6.030732|12|5/5/5|rejected|
|mixbudget370_parent_BTCN3000_ETHentryGateK500ppm_D5|candidate|3000|5|22.224002|20.052868|17.881964|6.030732|12|5/5/5|rejected|
|mixbudget370_parent_BTCN1000_constantlong|benchmark_parent|1000|None|-11.133786|-11.951354|-12.768930|20.340098|6|4/4/4|rejected|
|mixbudget370_parent_BTCN2000_constantlong|benchmark_parent|2000|None|-12.522411|-13.511478|-14.500549|23.185236|6|4/4/4|rejected|
|mixbudget370_parent_BTCN3000_constantlong|benchmark_parent|3000|None|-14.065351|-15.244972|-16.424597|26.335099|6|4/4/4|rejected|

逐项未通过条件：{'mixbudget370_BTC_N1000_momentum': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_BTC_N2000_momentum': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_BTC_N3000_momentum': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_BTC_N1000_constantlong': ['benchmark_control_not_strategy_candidate'], 'mixbudget370_BTC_N2000_constantlong': ['benchmark_control_not_strategy_candidate'], 'mixbudget370_BTC_N3000_constantlong': ['benchmark_control_not_strategy_candidate'], 'mixbudget370_parent_BTCN1000_ETHentryGateK500ppm_D1': ['local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN1000_ETHentryGateK500ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN1000_ETHentryGateK500ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN2000_ETHentryGateK500ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN2000_ETHentryGateK500ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN2000_ETHentryGateK500ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN3000_ETHentryGateK500ppm_D1': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN3000_ETHentryGateK500ppm_D3': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN3000_ETHentryGateK500ppm_D5': ['recent40_six_of_eight_positive5d_all_costs', 'local_recent6of8_allcost_gte60pct'], 'mixbudget370_parent_BTCN1000_constantlong': ['benchmark_control_not_strategy_candidate'], 'mixbudget370_parent_BTCN2000_constantlong': ['benchmark_control_not_strategy_candidate'], 'mixbudget370_parent_BTCN3000_constantlong': ['benchmark_control_not_strategy_candidate']}。基准的benchmark_control_not_strategy_candidate是身份标记，所有正/负收益仍保留。旧criteria/sensitivity/status不重评。

11CSV保留54成本场景、702月/尾折、432近期折、20034日NAV、27父N/D网格行、9原生N网格行、9旧基线场景、42相邻边、27同N持有/现金比较、36新旧原生成本路径、12资金配置。最高Sharpe边界与相邻cliff只作依赖样本描述，不据此扩批/调资格门槛，不冒充DSR/PBO统计显著性。

2026-11-04UTC读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对fundingTime/fundingRate/markPrice与tickSize/stepSize；实际数值仅取真实parquet/公开API。配比盈利是假设，官方文档不给收益结论。8源行情与spec/report/archive/code SHA见plan/binding/data_manifest。

原SMA65与single延续Nov4UTC12:30→14:30；独立L4延续14:10→16:10，可能跨16:00资金费。各账户用自己真实响应和原持仓逐事件核算，不复制现金流、不假定零/固定间隔，不重复旧08结算；无新日决策前保留原规则/本金/数量/risk/context与完整NAV前缀。本批研究不采纳到冻结账户。SMA完整日上下文仍为20261104T021133Z/forward_inputs.json.gz；partial不冒充180日/六折，延迟shadow与十策略真实报价观察分开。

预登记准备的family大写格式错误已在任何reserve/估值前修正，失败源码/无效spec/退出1回执保留；所有正式金融估值仅一次。取得同main共用锁后写入；只清理可重建中间物，完整结果/账本/冻结规则/登记/真实HTTP及失败证据保留。只读监控不新回测/下单/部署/建定时任务。真实push终态与解锁凭据见.git/automation_proofs/20261104T161708Z.json。

独立复核：仅BTCN1000/ETHD1自身满足全部成本近期6/8，仍因邻域严格合格率1/4=25%低于60%而淘汰；其他8组合自身近期未达6/8。没有把这个孤立点当稳健方法，也没有扩展网格。新原生324笔真实回测成交中246笔LOT数量不等于旧N500数量按金额线性缩放，324笔冲击成本均不等于旧N500冲击线性缩放；金额变化确实通过原生核算，细节见native_sizing_behavior.json。6个持有基准的负收益全部保存。

封存：18新金融配置/54成本场景逐项finish，组合通过0、淘汰9，3个BTC金额组件通过0；6持有对照不作候选。新原生决策6660次、资金费19980条、成交324笔；旧18成本账本资金费19980条、成交588笔均是旧记录。独立审计{'funding': 39960, 'fills': 912, 'rejects': 0, 'metric_checks': 1008, 'margin_checks': 276504}，0父订单。27新ID/54追加事件，33125旧保护文件不变。

原SMA续2026-11-04T12:30:00Z至2026-11-04T14:30:00Z，NAV48304+120=48424，累计48389分钟。single续2026-11-04T12:30:00Z至2026-11-04T14:30:00Z，NAV12551+122=12673，累计312ID；本窗实际新增资金费[]。L4续2026-11-04T14:10:00Z至2026-11-04T16:10:00Z，NAV5288+124=5412，累计135ID，本窗资金费[{'asset': 'BTC', 'cost': '1', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0.04816458000000000000000000000', 'amount_usdt': '0.04816458000000000000000000000', 'mark': '80274.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '2', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0.04816458000000000000000000000', 'amount_usdt': '0.04816458000000000000000000000', 'mark': '80274.30000000', 'rate': '0.00010000'}, {'asset': 'BTC', 'cost': '3', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0.04816458000000000000000000000', 'amount_usdt': '0.04816458000000000000000000000', 'mark': '80274.30000000', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '1', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2425.77209302', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '2', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2425.77209302', 'rate': '0.00010000'}, {'asset': 'ETH', 'cost': '3', 'timestamp_ns': 1793808000001000000, 'base_usdt': '0E-16', 'amount_usdt': '0E-16', 'mark': '2425.77209302', 'rate': '0.00010000'}]，不重复上轮08结算。三者新日决策/成交SMA 0/0、single 0/0、L4 0/0。原规则/本金与完整前缀保留，partial不冒充180日/六折，不采纳本批研究。

监控通过：9388研究行，9370旧完整行不变，10报价账户/249观察，gzip4298266字节。采用的正式管线及freeze_retry1均退出0；首个freeze格式错误退出1完整保留、未产生reserve/估值。HTTP/传输失败1次全部保留；取得共用锁后写入，官方文档本轮读取成功，实际资金费字段/现金流已核验。0已完成金融/观察重跑，清理0真实结果/账本，零可重建缓存遗留。

全部正负折/逐变体、完整DD、spec/report/archive/数据/代码SHA、真实短窗及失败证据保留。main非强制push、完整远端tree/blob及实际终态/解锁凭据见.git/automation_proofs/20261104T161708Z.json。
