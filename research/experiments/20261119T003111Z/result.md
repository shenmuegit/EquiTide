# 20261119T003111Z ETH成熟资金费样本数研究

预先固定ETH成熟资金费中位数样本数M=[2,3,4旧只读] × 旧BTC H=[0.03,0.0325]，代表ETHM3/BTCH0.03不随结果改变。6项新配置（2组件、4完整银行组合）逐项先reserve，实际执行一次并finish。历史门槛通过组合4/4；ETH组件通过0/2、淘汰2/2。严格同时改善收益、整体DD、Sharpe及Calmar为0/4。历史正收益不代表稳定实盘盈利，独立未来资格不足。

完整读取38324条事件、19023个ID、469份既往结论和29份附加材料。初始16项实际结果缺口0，legacy标记和原ZIP证据分别保留。规范研究定义11533→11539，正式有结果11326；定义数不是独立试验数，无DSR/PBO显著性证明。

经济假设：较短的成熟资金费中位数样本M=2或3可能更快响应费率状态变化，改变新建/反转机会、换手、持仓和成本，同时可能放大噪声。仅entry_funding_settlement_count及描述字段改变。每次信号先选实际已结算、距信号1–36小时且当时已可得的最新M条有符号费率；奇数M取排序中间值，偶数M取中间两值均值。M是整数记录数，不是小时数、日数、仓位权重或预算比例，不假设固定8小时结算。沿用预期支出max(direction×median,0)≤min(0.0002,0.0075×过去9日闭合对数收益样本标准差×最近合格实际结算间隔小时数/24)，相等通过、缺数据只拒绝新建/反转，已有同向数量不缩放。固定L5/H2%/exitE0.75%、有限S16/beta15/17/D3/K0.75%、入场V6/cap5.625%、R0.0075/VW9和全部银行规模，引擎与核算源码字节相同。

完整规则：ETH longonly fixedfastL5/H.02,exitE.0075. Fast r=lastcompletedclose/closeLcompleteddaysearlier-1;contrarianbase=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0;strict E equality exits. Finite normalized EWM fixedS16,beta15/17,latest16completedcloses; slope=currentlevel/samefinitelevel3completeddaysearlier-1,strictabsoluteK.0075 over3days,notdailyized. Gate=+1 if slope>.0075,-1 if slope<-.0075,else0;acceptbase ifbase==actual or base==gate,else0. Entryrisk Bessel-corrected samplelogvol fixedV6/cap.05625 onlynew/reversed,equalitypasses. LatestM[2,3,4readonly]actual signedfundingmedian;selectMmostrecentsettlementsage1to36hinclusive/available<=signal;oddMusesmiddleofsortedrates,evenMmeanofmiddletwo;no8hscheduleassumed;outgoingcost<=min(.0002,fixedR.0075*past9completedBessel-correctedsamplelogvol*latesteligibleactualintervalhours/24),equalitypasses,missingblocksnewentryonly;entrygatesdo_not_resize_actualq;finallymax(desired,0). BTCreadonly L29 mainH[.03,.0325],exitE.005,V10cap.0275,recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. FastL,exitE,fastH,trendK,lagD,entryriskV6,carryVW9,impactV20distinct.

原始完整银行权重[1,1]：BTC C3750/N1000、ETH C15000/N4000，总初始18750USDT；20/80仅初始资金占比，不归一化、缩放旧NAV、转移、再平衡、创建父订单或跨银行抵消保证金。对齐真实事件轴后相加完整美元NAV。

Walk-forward：2025-10-19 00:01→2026-11-14 00:01，391日复用开发历史、33日闭合上下文；无拟合/标签，仅过去可得前缀，下一分钟开盘执行。13个完整30日折+1日尾段、近40日8×5日、扩展21日5/5/5/6日。跨折继承现金/持仓，终点计费平仓，整体DD取连续全NAV。反复使用日期不是未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日波动×sqrt(订单额/过去20日quoteADV)冲击；不利tick/LOT/minnotional、参与率≤0.001、1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流随倍率放大、收入不放大；USDT线性永续无现货借币。缺L2/TCA、完整阶梯、tick清算和容量实证，成本/风险为估计。

|配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，M=2|rejected|5.831403 / 5.507230 / 5.183267|1.528984|1.642651|3.159229|6/13|0/0/0（各/8）|
|ETH组件，M=3|rejected|5.459243 / 5.180903 / 4.902772|1.528984|1.565567|2.988535|5/13|0/0/0（各/8）|
|组合BTCH=0.03，M=2|passed|8.311163 / 7.806096 / 7.301209|1.357834|2.230073|5.007665|12/13|6/6/6（各/8）|
|组合BTCH=0.0325，M=2|passed|8.203563 / 7.699192 / 7.195002|1.357834|2.198969|4.934987|12/13|6/6/6（各/8）|
|组合BTCH=0.03，M=3|passed|8.013435 / 7.545034 / 7.076813|1.357834|2.171703|4.854104|11/13|6/6/6（各/8）|
|组合BTCH=0.0325，M=3|passed|7.905836 / 7.438130 / 6.970606|1.357834|2.140452|4.781416|11/13|6/6/6（各/8）|

与旧ETH M4同BTC对照比较，0/6项完整1/2/3倍成本路径相同。逐成本原生成交、实际资金费和desired是否相同见parameter_path_equivalence.json；参数数值变化不自动形成新收益路径，不把定义数当独立盈利证据。

本批仅检验固定S16/D3/K0.0075、R0.0075/VW9、入场V6/cap0.05625及其他规则下的三个ETH成熟资金费样本数，与两BTC门槛交叉。完整路径是否相同、各相邻跳变和边界均如实列出，不因参数数目推断独立收益证据，不外推为所有趋势跨度、风险上限或市场状态的宽泛稳健性。
启发式跳变边：[{"scope": "native", "from": "ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M3BudgetVW9R0p0075_391d", "to": "ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4_BudgetVW9R0p0075_391d", "delta_net_pp": 1.3990980188089086, "delta_sharpe": 0.2954077833653186, "delta_DD_pp": 0.0, "delta_Calmar": 0.8511131705208221}]
启发式标记由10条相邻边的实际指标差计算，逐边保留来源、方向与变化值；只读BTC边与新ETH样本数边分别辨认，既不隐去参数断崖，也不把混合尺度提示当统计显著性或广泛稳健性证明。
旧M4对照位于已测样本数域边界且本批表现较好；代表M3/H0.03仍按事前约定保留。当前仅核验既有2/3/4样本域和1–36小时成熟条件，不根据本批结果扩网格、更改成熟范围或将边界当作全局最优证明。

双轴敏感性保存42成本场景、588逐折、336近40日折、168扩展折、16464日NAV、10相邻边和六面热图。启发式跳变标记1/10；6项新配置有6条不同完整成本路径，其中0条匹配旧参考。保留边界和变差结果，不在看结果后扩网格或换代表。

失败判据预先固定：各成本全期/近期正收益、1x≥10/13正月、各成本近期≥6/8正折、扩展≥3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、≥4平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规、终点flat。
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M2BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M3BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHFundingM2L5E0p0075_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHFundingM2L5E0p0075_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHFundingM3L5E0p0075_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHFundingM3L5E0p0075_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。

相对同BTC旧ETH M4/L5/S16/D3的三倍成本配对增量：
ETH M=2/BTC H=0.03：收益-0.894882个百分点，整体DD0.000000个百分点，Sharpe-0.112878，Calmar-0.612182，完整成本路径相同=False。
ETH M=2/BTC H=0.0325：收益-0.894882个百分点，整体DD0.000000个百分点，Sharpe-0.114678，Calmar-0.612222，完整成本路径相同=False。
ETH M=3/BTC H=0.03：收益-1.119278个百分点，整体DD0.000000个百分点，Sharpe-0.171247，Calmar-0.765742，完整成本路径相同=False。
ETH M=3/BTC H=0.0325：收益-1.119278个百分点，整体DD0.000000个百分点，Sharpe-0.173195，Calmar-0.765793，完整成本路径相同=False。
ETH M=2 cost=1：成熟资金费计数变化391次、选择记录变化391次、中位费率变化333次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化1，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH M=2 cost=2：成熟资金费计数变化391次、选择记录变化391次、中位费率变化333次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化1，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH M=2 cost=3：成熟资金费计数变化391次、选择记录变化391次、中位费率变化333次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化1，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH M=3 cost=1：成熟资金费计数变化391次、选择记录变化391次、中位费率变化381次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化2，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH M=3 cost=2：成熟资金费计数变化391次、选择记录变化391次、中位费率变化381次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化2，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH M=3 cost=3：成熟资金费计数变化391次、选择记录变化391次、中位费率变化381次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化2，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。

独立核验2346个新决策、5865个只读决策及完整账本/成本/资金费/风险/NAV。匹配持有3x收益-14.782911%、DD18.454767%，现金0。全部成本、逐折、敏感性和完整日NAV见report.json、results与exports。

本轮SMA/single 2026-11-18T10:30:00Z→2026-11-18T12:30:00Z、L4/FEWM 2026-11-18T12:10:00Z→2026-11-18T14:10:00Z均无日决策。实际资金费行{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}来自已执行独立审计。本轮四账户均未重复已计入的08资金费，现金按本窗实际事件核对。持仓/入场/desired/执行费用保持，资金费后的现金不重置；single ETH空头{'1': '-1.644000000000000000', '2': '-1.644000000000000000', '3': '-1.644000000000000000'}保留。首08来源UTC仍2026-11-18T18:34:09.827345Z且字节SHA不改，新查来源UTC为2026-11-19T00:36:23.249328Z另存。下一SMA/single ['2026-11-18T12:30:00Z', '2026-11-18T14:30:00Z']、L4/FEWM ['2026-11-18T14:10:00Z', '2026-11-18T16:10:00Z']都不得重复08，仍须完整查询实际特殊事件。四账户下一日决策Nov19_00:01，full70SPOT与69日前缀保留，不采用研究资金费样本数、不重启或强平。本轮已使用按事件覆盖核对的门禁，后续仅在查询覆盖相同已知08事件时核对原字段，不要求不重叠查询的完整响应相同。

原SMA3x累计收益-7.468958%。四原账户为延迟shadow；十策略真实报价模拟只读保留，未创建paper新成交或改规则。原180日/六折观察计划未成熟，继续原计划。
保存18份唯一公共GET回执，本轮18、复用旧0、真实运输失败0。未新下载SPOT日线，原完整70日权威另保留；首00来源时间/SHA不变，新查询另存。
只读监控生成成功=True；11098研究配置、11092旧行完整字典不变。

实际复现命令（已完成目录禁止重评；读取既有证据核验）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261119T003111Z/commands.py prepare
python3 -B research/experiments/20261119T003111Z/commands.py freeze
python3 -B research/experiments/20261119T003111Z/commands.py units
python3 -B research/experiments/20261119T003111Z/commands.py bind
python3 -B research/experiments/20261119T003111Z/commands.py reserve_0
python3 -B research/experiments/20261119T003111Z/commands.py evaluate
python3 -B research/experiments/20261119T003111Z/commands.py audit
python3 -B research/experiments/20261119T003111Z/commands.py exports
python3 -B research/experiments/20261119T003111Z/commands.py finish_0
python3 -B research/experiments/20261119T003111Z/commands.py research_check
python3 -B research/experiments/20261119T003111Z/commands.py l4h02
python3 -B research/experiments/20261119T003111Z/commands.py fewm
python3 -B research/experiments/20261119T003111Z/commands.py candidate
python3 -B research/experiments/20261119T003111Z/commands.py forward
python3 -B research/experiments/20261119T003111Z/commands.py accounts_check
python3 -B research/experiments/20261119T003111Z/commands.py journal
python3 -B research/experiments/20261119T003111Z/commands.py sources_check
python3 -B research/experiments/20261119T003111Z/commands.py gates
python3 -B research/experiments/20261119T003111Z/commands.py feed
python3 -B research/experiments/20261119T003111Z/commands.py collect
python3 -B research/experiments/20261119T003111Z/commands.py final_checks
```

每个native退出码、stdout/stderr、spec、数据SHA、负折、实际账本和失败记录均保留。

本轮实际读取[Binance官方资金费历史接口](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)确认资金费与时间/标记价字段；以实际事件为准，不固定8小时。使用原始数据格式及来源时间说明见[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。衰减定义参考[pandas3.1.1 EWM](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)；有限16项支持与D3比值为预先明确的自定义规则。资金费样本数、成熟范围、预算公式、三日趋势门槛及有限支持为预先固定的自定义规则；中位数奇偶定义见[Python官方statistics.median](https://docs.python.org/3/library/statistics.html#statistics.median)。本轮实际文档访问与版本记录见primary_source_access.json。
