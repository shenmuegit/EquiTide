本轮实际完成11个390日配置、33个1/2/3倍成本场景：4个策略组件、2个匹配持有组件、4个策略组合及1个持有组合。4个策略组合历史通过，4个策略组件与3个持有基准淘汰；每项先成功reserve后计算、独立核算后finish，全部负收益与负折保留。原report.summary的rejected_source_components字段沿用“全部拒绝原生行”含2个持有腿，明确角色核对见classification_verification，不改财务报告原字节。

经济假设与预设：将既有BTC波动门控动量、ETH资金费预算反转的相同规则延长一个实际闭合日，检查成本与近期资格。预设BTC V10无偏samplelogvol上限BVC=[3%,4%]×ETH VW8资金费预算比R=[0.00875,0.01]，2×2网格；代表固定BVC4%/R0.01，未按结果更换或扩展网格。参数选自已有规则，新增时间边界与真实输入哈希构成新配置，非改名绕过查重。

BTC C3750/N1000，L29/H3%/E1%严格ROC动量；ETH C15000/N4000，L5/H2%/E0.75%反转，有限归一化EWMS16 beta15/17、D3严格K0.75%、V6cap5.625%，最近4笔1–36小时成熟实际资金费有符号中位数，预算min(.0002,R×VW8无偏samplelogvol×最新合格实际结算间隔小时/24)，最后long-only。只挡新仓/反手，同向q保留；前完成收盘算N/LOT向下取整，下一00:01真实OPEN执行。全部政策、交易、资金费、统计与保证金公式AST与旧版一致；只变研究日历和事前阈值。

父组合本金18750，raw[1,1]相加完整独立银行美元NAV，20/80仅本金占比，不自动归一化或对NAV二次加权；不转账、再平衡、父订单、跨保证金。旧389日归档在旧终点强平，不能直接拼接为390日；本轮6个390日原生配置全部预登记后真实执行，组件一旦生成即复用于5个父组合，未重跑任何已完成的389日配置。

完整读取35036登记事件/17396ID、412份结论、三技能/task/README/OOS脚本及原ZIP。初始16项仍有11份正式实际结果与5份原ZIP证据，保留历史false和全部旧记录；没有缺实际历史配置可补，不补跑其他所有者paper失败报价窗口。保护72836份旧文件。

新数据：官方/fapi/v1闭合K线、小时mark与实际fundingTime/rate/mark；每币新增1440分钟、24小时mark及3笔已实际核验结算。旧1442根重叠分钟、24根小时和10笔重叠资金费逐字段相等，规范化新文件保留所有旧行。每币609122分钟、10152小时、1270实际资金费，完整423日背景+研究数据及2根终点参考分钟。原始GET、body/文件SHA、bundles、规范化新旧输入哈希均保存；大parquet留忽略data。

三项验证已实际执行：连续390日2025-10-19T00:01Z→2026-11-13T00:01Z，33日背景、13个完整30日折；1倍至少10/13正月，沿用事前至少75%比例，不在结果后改门槛。近期40日day350继承真实cash/q，8×5日；扩展20日day370继承，4×5日。全路径事件NAV计算整体回撤，不用折内最大值或平均单策略指标。无训练、标签或拟合，purge0，信号只用当时已完成数据，跨折不重置，只有新终点成本平仓；旧389日终点不插入额外退出。

全部历史反复用于开发，新增一天也已在其他观察中可见，不能称未触碰最终测试集或独立未来。多重选择偏差仍在；2×2面仅为局部检验，最高收益落边界已标记，不据此结果后扩网格。不同定义/不同完整路径不等于独立alpha；未声称统计显著性或稳定实盘盈利。此前389日L31近期失效证据原样保留，本轮未检验L31新390日结果。

成本逐边5bp费+1bp半价差+2bp滑点+0.5×过去20日samplelogvol×sqrt(abs(q)×真实OPEN/过去20日quoteADV)冲击，不利tick取整；1/2/3倍执行成本和资金费支出，收入不放大。线性永续无需现货借币，核对LOT/tick/minnotional、参与率≤0.1%、费后1倍抵押及已闭合小时不利high/low的1%保证金代理。缺历史L2/TCA、完整风险档位/tick强平与独立容量实证，估计成本不保证真实成交。

其余冻结判据：全期和近期各成本净正，近期各成本≥6/8正折，3倍整体DD≤25%，局部3倍净正和严格近期资格邻居比例≥60%，底层≥4次平仓，(毛价格PnL+净资金费)/1倍执行成本≥2.5，无拒单/负抵押/保证金代理违规，期末平仓且≥180日；扩展20日各成本净正且≥3/4正折。父组合同时变化两个适用参数；每个单币组件只检验自己的适用轴，基准无调参。

|BVC%|ETH预算R|1x净%|2x净%|3x净%|3x整体DD%|正月/13|近期正折1/2/3|状态|
|---:|---:|---:|---:|---:|---:|---:|---|---|
|3|0.00875|8.988288|8.415145|7.842196|1.484207|12|6/6/6|passed|
|3|0.01|8.926692|8.349711|7.772923|1.484207|12|6/6/6|passed|
|4|0.00875|8.747090|8.154638|7.562364|1.488161|11|6/6/6|passed|
|4|0.01|8.685495|8.089204|7.493091|1.488161|11|6/6/6|passed|


预设代表指纹ff7714578c7c8a2e9ae5e8612d676c6e3f7d2f8f729ef92d2955ddcb978d1ead，三倍净7.493091158%、整体回撤1.488160521%，11/13正月，各成本近期6/8正折，局部严格资格比例1。四组合三倍净7.493091%–7.842196%，最高值在网格边界，未重选代表。同390日期间匹配持有三倍净-14.165005961%、整体DD18.454766592%，负收益及所有失败项保留；现金基准0%。

各淘汰行（完整逐成本数值见exports/costs.csv、report.json）：

extend390_BTC_V10cap300bp，role=component，3倍净13.657136%；recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct

extend390_BTC_V10cap400bp，role=component，3倍净12.257975%；ten_of_thirteen_positive_complete30d_1x_folds,recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct

extend390_ETH_longonly_R0p00875，role=component，3倍净6.388461%；ten_of_thirteen_positive_complete30d_1x_folds,recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct,extension20_positive_all_costs,extension20_three_of_four_positive_folds_all_costs

extend390_ETH_longonly_R0p01，role=component，3倍净6.301870%；ten_of_thirteen_positive_complete30d_1x_folds,recent40_six_of_eight_positive5d_all_costs,local_recent6of8_allcost_gte60pct,extension20_positive_all_costs,extension20_three_of_four_positive_folds_all_costs

extend390_hold_BTC，role=benchmark，3倍净-11.232418%；positive_all_costs,ten_of_thirteen_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,extension20_positive_all_costs,extension20_three_of_four_positive_folds_all_costs

extend390_hold_ETH，role=benchmark，3倍净-14.898153%；positive_all_costs,ten_of_thirteen_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,extension20_positive_all_costs,extension20_three_of_four_positive_folds_all_costs

extend390_parent_matched_hold，role=benchmark，3倍净-14.165006%；positive_all_costs,ten_of_thirteen_positive_complete30d_1x_folds,recent40_positive_all_costs,recent40_six_of_eight_positive5d_all_costs,local_positive3_gte60pct,local_recent6of8_allcost_gte60pct,four_underlying_native_closes1,gross_plus_funding_to_cost1_gte2_5,extension20_positive_all_costs,extension20_three_of_four_positive_folds_all_costs

独立核算18条新原生/15条新父曲线、7020条因果决策；计数{"funding": 21060, "fills": 324, "rejects": 0, "metric_checks": 462, "margin_checks": 123408}。Fraction政策、Decimal现金/LOT/tick/费用/实际资金费、小时风险、完整NAV、13逐折/近期/扩展与判据均核验。保存33场景、429逐折、264近期折、132扩展折、12903每日净值点、6邻接边、热力图及1条Sharpe突变标记。单独的合成严格边界/未来后缀、收入不放大/支出压力与390日日历测试不是市场回测。

已保存12个策略组合/成本场景的BTC/ETH美元PnL分解。ETH扩展20日全部净PnL为0：True；因此不将该段组合表现当ETH新期间贡献。相对预设组合，同390日三成本同时改善净收益与回撤的格数2，仍属同一重复历史上的比较。11个定义形成11种三成本路径，改变日期会改变路径长度，未拿旧389日哈希不匹配证明新alpha。

原账户SMA/single Nov13_18:30→20:30Z，L4/FEWM20:10→22:10Z，本轮日决策{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新资金费{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}。18本永续账簿各自cash/q/entry核对，旧Nov13_00/08/16各一次；没有提前计入Nov14_00资金费或00:01决策。全部全NAV前缀通过。SMA累计61709分钟/61753点，完整65日权威仍research/experiments/20261113T033939Z/forward_inputs.json.gz，SHA11c8a6e3a86280dab367f823d4cbf396f27c4f9ff576d8162ee39d0aa68b987e，当前minute-only不替代日背景；延迟shadow与paper10报价模拟分开，partial rejected不取消原长期计划。

下轮SMA/single Nov13_20:30→22:30Z，22:31后参考分钟闭合，无日决策。L4/FEWM Nov13_22:10→Nov14_00:10Z，00:11后参考分钟闭合，覆盖Nov14_00实际结算与00:01原日决策。先GET各自完整窗口真实fundingTime/rate/mark，按各自旧q/cash记一次，不假定整8小时；闭合Nov13完整日1440分钟及quoteVolume，延续各自daily/context/risk/NAV链。single未覆盖00，不提前记或复制L4/FEWM现金流。旧Nov13_00/08/16三组均已各记一次不重复。本轮没有任何Nov14_00资金费或日决策，不把研究新390日当账户实盘报价。SMA是SPOT不计永续费，完整65日权威仍033939截至Nov13_00；下一mark-only20:30→22:30可用，其后22:30→Nov14_00:30必须用原日适配器增补第66个完成日，不能以minute-only替代背景。保持冻结本金/cash/q/desired/终止计划，不重置、不窗口强平、不采用新研究参数。

全阶段已保存公开GET 28次，真实失败0次，含新增研究日采集、资金费预检、三原生账户及SMA，公共响应复用去重。各URL、时间、原包、退出码与stderr如有均留档；未重跑完成的金融模型/账户窗口。

工程证据：两次只读源码定位误把多层导入别名当本地def，ValueError与原生命令位置留read_failures，改为inspect实际绑定后解决；无策略/账户计算或旧文件改动。热力图沿用的389d面板标题已更正390d，原/重导出CSV与stdout逐字节相同，未改财务报告或重算模型。完整角色分类将4策略组件与3持有基准分开，保留财务报告原字节。

[Binance官方USD-M REST v1市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[官方公共K线字段与时间单位](https://github.com/binance/binance-public-data/blob/master/README.md)，本轮跨UTC午夜后2026-11-14再次核对。fundingTime取实际公开时间戳；源可得性设为结算后一小时仅是规范化假设，未测历史网络到达。

复现命令与实际stdout/退出码见commands.py、all_command_receipts.json及各*_commands.json；全部输入、源代码、冻结spec和结果SHA见data_manifest。注册器防止重复已完成精确配置。只提交本轮轻量真实证据及监控；大行情保留忽略data，清理可重建缓存，完整账户/冻结规则/登记和核验必需证据保留。最终push状态以原生发布和完整远端树核验回执为准。

另一次对已成功结束会话的重复只读查询被工具以Unknown process拒绝，原exit0完成回执保持；未重跑账户或策略，见read_failures。

提交格式核对留档：原实际执行run.py第16行仅一个空格。为保持预登记后实际执行源码字节及SHA不变，只将该绑定文件从Git空白样式检查中显式列为例外；白名单由原绑定SHA及唯一纯空白行双重断言约束，财务逻辑、原生核算、注册与完整本地/远端字节哈希检查不排除此文件。报告末尾空行已修正。首次格式/封存失败及成功重试均保留，未重算模型或账户。
