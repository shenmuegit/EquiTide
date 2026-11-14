本轮完成11个391日真实配置、33个1/2/3倍成本场景，4个策略组合历史通过，策略组件通过1个、淘汰3个，3个匹配持有基准全部淘汰。结果均先reserve后执行、独立核算后finish，保留全部负收益和负折；未新设前向账户、未采用新规则。

经济假设：既有BTC波动门控动量与ETH资金费预算反转组合，在新增一个实际闭合日后仍能保留成本及近期资格。批次事前固定BTC V10无偏samplelogvol上限[3%,4%]×ETH VW8预算比R[0.00875,0.01]；固定代表4%/0.01，没有按收益更换代表或扩网格。

BTC C3750/N1000，L29/H3%/E1%严格ROC动量；ETH C15000/N4000，L5/H2%/E0.75%反转，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6上限5.625%、最近4笔1–36小时已成熟实际资金费有符号中位数，预算min(.0002,R×VW8无偏samplelogvol×最新合格实际结算间隔小时/24)，最后限制long-only。只挡新仓/反手，同向q保留；信号用上一完整收盘，按N/close和LOT向下取整，下一00:01真实OPEN成交。

父组合本金18750，raw[1,1]相加BTC/ETH完整独立银行美元NAV；20/80只是本金占比，不归一化、不二次加权、不转账/再平衡/父订单/跨保证金。旧390日归档含终点退出，不能直接拼接。本轮6个391日原生配置重新计算新期间，生成后复用于5个父组合；未重跑任何已完成的390日配置。18条新原生曲线前390日所有决策、资金费和非终止成交均与旧归档完全相等，证据见calendar_prefix_verification.json。

完整读取登记35102事件/17429ID、413份旧结论、三技能、task/README/OOS脚本及原始ZIP。初始16项都有实际证据：11份正式报告、5份原ZIP；保留旧false/legacy记录，没有缺实际配置可补，不补跑paper10失败报价窗口。保护73191份旧文件。

数据范围2025-10-19T00:01Z→2026-11-14T00:01Z，33日背景。官方/fapi/v1每币610562分钟、10176小时mark、1273笔实际资金费；新增1440分钟、24小时和3笔真实结算。1442根重叠分钟、24根小时、10笔重叠资金费逐字段一致，所有旧规范化行保留。原采集止于00:00，漏掉实际00:00:00.004资金费，被规范化门禁拦下；使用覆盖完整账户窗口的新公开响应补齐，原包、失败回执、修复前后bundles和SHA均保留，无金融结果在补齐前产生。

Walk-forward完成：13个完整30日折加1日尾折，共14折；完整月折要求1倍≥10/13正，尾折不参与月度通过率。近期40日day351继承cash/q，8×5日；扩展21日day370继承，5+5+5+6日四折，要求各成本净正且≥3/4正折。全部折连续继承状态，只有新终点成本退出；以完整事件NAV算整体回撤，无拟合/标签，purge0，不用未来收盘或未成熟资金费。1日尾折Sharpe无定义，保存null；尾折年化量不作为稳健资格。

敏感性完成：父组合同时变化两个适用参数，单币各检验自己的适用轴，持有基准无调参。每个具体配置独立spec/reserve/finish。表中全期净收益、整体DD和月/近期折数由保存结果读取；全变体Sharpe、Calmar、逐折和成本明细见CSV。最高收益位于网格边界，保留1条Sharpe突变标记，不能外推为广泛参数平台。

成本完成：逐边5bp手续费+1bp半价差+2bp滑点+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)冲击，不利tick取整；执行成本及资金费支出1/2/3倍，收入不放大。核对LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押和闭合小时不利high/low的1%维持保证金代理。线性永续无现货借币需求。缺历史L2/TCA、完整风险档位/tick强平和独立容量实证，估计不保证真实成交。

其余冻结门槛：全期和近期各成本净正、近期各成本≥6/8正折、3倍整体DD≤25%、局部净正和严格近期邻居比例≥60%、底层≥4次平仓、(毛价格PnL+净资金费)/1倍执行成本≥2.5、无拒单/负抵押/保证金代理违规、期末平仓、至少180日。

|配置|角色/状态|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|
|---|---|---:|---:|---:|---:|---:|---|
|extend391_BTC_V10cap300bp|component/passed|17.406460|16.026464|14.646562|5.833563|10|6/6/6|
|extend391_BTC_V10cap400bp|component/rejected|16.200473|14.723928|13.247400|6.818098|9|6/6/6|
|extend391_ETH_longonly_R0p00875|component/rejected|7.130703|6.759477|6.388461|1.528984|7|0/0/0|
|extend391_ETH_longonly_R0p01|component/rejected|7.053708|6.677684|6.301870|1.528984|7|0/0/0|
|extend391_hold_BTC|benchmark/rejected|-10.088892|-11.031753|-11.974640|14.975864|6|1/1/1|
|extend391_hold_ETH|benchmark/rejected|-13.959387|-14.722181|-15.484979|19.393639|6|1/1/1|
|extend391_parent_BVC300bp_R0p00875|candidate/passed|9.185854|8.612874|8.040081|1.484207|12|6/6/6|
|extend391_parent_BVC300bp_R0p01|candidate/passed|9.124258|8.547440|7.970808|1.484207|12|6/6/6|
|extend391_parent_BVC400bp_R0p00875|candidate/passed|8.944657|8.352367|7.760249|1.488161|11|6/6/6|
|extend391_parent_BVC400bp_R0p01|candidate/passed|8.883061|8.286933|7.690976|1.488161|11|6/6/6|
|extend391_parent_matched_hold|benchmark/rejected|-13.185288|-13.984095|-14.782911|18.454767|6|1/1/1|


固定代表68db1fe0deec7b5a4d647570a2b7b04ef4d3c45eaf1ab5e0c0b25e2814dedcc0，三倍净7.690976214%、整体回撤1.488160521%。同期间匹配持有三倍净-14.782911083%、整体DD18.454766592%；现金0%。四个组合近期均6/8正折。BTC3%组件从旧390日不通过到391日历史通过，来自预设滚动40日区间移动，不能称独立前向晋级。ETH扩展21日零PnL：True，该段组合收益不可归因于ETH新贡献。

淘汰理由（完整逐判据布尔值见report.json）：

extend391_BTC_V10cap400bp：ten_of_thirteen_positive_complete30d_1x_folds

extend391_ETH_longonly_R0p00875：ten_of_thirteen_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct,extension21_positive_all_costs,extension21_three_of_four_positive_folds_all_costs

extend391_ETH_longonly_R0p01：ten_of_thirteen_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct,extension21_positive_all_costs,extension21_three_of_four_positive_folds_all_costs

extend391_hold_BTC：positive_all_costs,ten_of_thirteen_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,extension21_positive_all_costs,extension21_three_of_four_positive_folds_all_costs

extend391_hold_ETH：positive_all_costs,ten_of_thirteen_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,extension21_positive_all_costs,extension21_three_of_four_positive_folds_all_costs

extend391_parent_matched_hold：positive_all_costs,ten_of_thirteen_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,extension21_positive_all_costs,extension21_three_of_four_positive_folds_all_costs

全部历史反复用于开发，新增一天也已在别的观察可见，不是未触碰最终测试集或独立未来。多重选择偏差未消除，11个定义和11条不同三成本路径不等于独立alpha；未声称统计显著性、稳定实盘盈利。旧389日L31失效证据和390日所有结果原样保留。

独立核算18条原生/15条父曲线、7038条精确因果决策；资金费、Decimal现金/LOT/tick/成本、小时风险与完整NAV核验计数{"funding": 21114, "fills": 324, "rejects": 0, "metric_checks": 495, "margin_checks": 123732}。导出33成本场景、462逐折、264近期折、132扩展折、12936每日净值点、12匹配持有对照、6邻接边和热力图。

真实中断与恢复：旧统计函数对1日尾折调用样本stdev失败，首个成本场景尚未完成归档，完整曲线/实际结果数0。11项先finish blocked无结果，保存原代码绑定及源文件，再以单日Sharpe=null的最小统计边界修复，通过失败→成功的合成测试及多日公式逐值相等测试；原交易/资金费/风险政策AST不变，全部spec、参数、权重、数据、门槛字节不变，重新成功reserve后完整执行一次。两次执行尝试、一次完整结果，不把中断当rejected，也没有重跑已完成曲线。登记总计23ID/68事件，含11项恢复各额外blocked/reserve两事件。另一次只读源码定位ValueError已记录并解决，无金融计算。

原账户：SMA/single Nov13_20:30→22:30Z，L4/FEWM Nov13_22:10→Nov14_00:10Z。当前日事件{'SMA': 0, 'candidate': 0, 'l4h02': 1, 'fewm': 1}，成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，资金费记录{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}。L4/FEWM按各自旧q/cash在00:00:00.004记一次实际费，00:01执行各自原规则，重建完整Nov13日close及1440分钟quoteVolume；18本永续账簿及全部NAV前缀独立核对，无重开或强平。SMA累计61829分钟/61873点，当前仍使用65日完整背景research/experiments/20261113T033939Z/forward_inputs.json.gz，SHA11c8a6e3a86280dab367f823d4cbf396f27c4f9ff576d8162ee39d0aa68b987e。这些是延迟shadow，partial未达180日不取消原冻结计划，与paper10报价模拟分开。

下轮SMA/single Nov13_22:30→Nov14_00:30Z，00:31后参考分钟闭合；覆盖00实际结算和00:01原日决策。single按自己的q/cash记实际资金费，不能复制L4/FEWM现金流；SMA是现货不计永续费。SMA现有完整65日权威033939截至Nov13_00，下轮必须使用原日适配器增补第66个完成日Nov13，不可用minute-only替代背景。L4/FEWM下轮Nov14_00:10→02:10Z，02:11后参考闭合，无新日决策；各自00:00:00.004实际结算、00:01原日决策已在本轮记一次，不重复。每币窗口先GET实际fundingTime/rate/mark，不以8小时时刻代替真实记录。旧Nov13_00/08/16三永续账户均已各记一次。保持所有冻结本金、规则、cash/q/desired与终止计划；不采用本轮新研究参数、不重置、不窗口强平。原账户仍是延迟shadow，paper10报价模拟单独只读汇总。

本轮留档行情数据GET共29次，观察到真实传输失败1次，含研究新日、资金费预检、三原生账户和SMA，复用响应去重；保留URL、原包、body/压缩SHA、UTC、退出码和stderr，未因数据读取失败重算完成模型或账户窗口。

[Binance官方USD-M REST v1市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[官方公共数据字段与单位](https://github.com/binance/binance-public-data/blob/master/README.md)，2026-11-14访问。资金费按实际时间戳；信号可得性保守设结算后一小时，是规范化假设，并非历史网络到达实测。

复现顺序：review/capture_new_day.py（本轮已完成，不重下完成数据）→review/preflight.py→review/supplement_midnight_funding.py→review/normalize_new_day_retry1.py→review/configure.py→review/setup.py→commands.py freeze/units/bind/reserve_0/reserve_1；中断见evaluate.log，恢复见review/mark_interrupted.py、recovery_setup.py、test_tail_stats.py及绿色测试、bind_retry3、resume_recovery.py；成功评估见commands.py evaluate_retry3/audit/exports/finish_0/finish_1/research_check。原账户顺序midnight_archive/l4h02/fewm/candidate/forward/accounts_check，登记及提交前journal/sources_check/gates/feed/collect/final_checks。具体绝对命令、UTC、stdout与退出码见各*_commands.json和review/native_*_receipt.json；注册器阻止重复完成配置，纯核验不新生成成交。

输入、spec、代码、报告和充分复现证据SHA见data_manifest；全部旧账本/冻结计划/登记和失败证据保留。仅提交本轮轻量证据与只读监控，大parquet留忽略data。监控在同一锁内只读汇总已有账户和报告，不新回测/造报价/改规则或本金；无需部署网站。提交与push最终状态以原生发布、完整远端树/blob核验、实际释放锁回执为准。
