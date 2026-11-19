# 20261119T023142Z ETH快周期入场门槛研究

预先固定ETH五日快ROC门槛H=[0.019,0.02旧只读,0.021] × 旧BTC H=[0.03,0.0325]，代表ETHH0.019/BTCH0.03不随结果改变。6项新配置（2组件、4完整银行组合）逐项先reserve，实际执行一次并finish。历史门槛通过组合4/4；ETH组件通过0/2、淘汰2/2。严格同时改善收益、整体DD、Sharpe及Calmar为0/4。历史正收益不代表稳定实盘盈利，独立未来资格不足。

完整读取38380条事件、19051个ID、470份既往结论和29份附加材料。初始16项实际结果缺口0，legacy标记和原ZIP证据分别保留。规范研究定义11539→11545，正式有结果11332；定义数不是独立试验数，无DSR/PBO显著性证明。

经济假设：较低/较高的五日快ROC反向入场门槛H=1.9%或2.1%可能改变反转时机、持仓、换手和成本。return_hurdle、long_entry_return_hurdle、short_entry_return_hurdle三字段保持同值，仅这些耦合数值及描述字段改变。r=最新已闭合日收盘/五个闭合日前收盘-1；严格r>H给原始空向目标，r<-H给原始多向目标；等于H不新触发，其他情形按固定E=0.75%的严格退出/续持规则处理。依次经过固定趋势、入场风险和成熟资金费过滤，再限制为long-only；已有同向实际数量不因入场过滤缩放。H是无量纲五日简单收益门槛，不是资金权重、日对数波动上限或资金费样本数。固定L5/E0.75%、有限S16/beta15/17/D3/K0.75%、入场V6/cap5.625%、成熟M4/R0.0075/VW9及全部银行规模。资金费仍只用信号前1–36小时成熟且可得的最新4条有符号费率中位数，不假设8小时固定结算；预算等于min(0.0002,0.0075×过去9日样本对数波动×实际最近结算间隔小时数/24)，相等通过。引擎及核算源码字节不变。

完整规则：ETH longonly fixedfastL5/H[.019,.02readonly,.021],exitE.0075. Fast r=lastcompletedclose/closeLcompleteddaysearlier-1;contrarianbase=-1 if r>H,+1 if r<-H,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0;strict E equality exits. Finite normalized EWM fixedS16,beta15/17,latest16completedcloses; slope=currentlevel/samefinitelevel3completeddaysearlier-1,strictabsoluteK.0075 over3days,notdailyized. Gate=+1 if slope>.0075,-1 if slope<-.0075,else0;acceptbase ifbase==actual or base==gate,else0. Entryrisk Bessel-corrected samplelogvol fixedV6/cap.05625 onlynew/reversed,equalitypasses. LatestfixedM4actual signedfundingmedian;select4mostrecentsettlementsage1to36hinclusive/available<=signal;meanofmiddletwosortedrates;no8hscheduleassumed;outgoingcost<=min(.0002,fixedR.0075*past9completedBessel-correctedsamplelogvol*latesteligibleactualintervalhours/24),equalitypasses,missingblocksnewentryonly;entrygatesdo_not_resize_actualq;finallymax(desired,0). BTCreadonly L29 mainH[.03,.0325],exitE.005,V10cap.0275,recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. FastL,exitE,fastH,trendK,lagD,entryriskV6,carryVW9,impactV20distinct.

原始完整银行权重[1,1]：BTC C3750/N1000、ETH C15000/N4000，总初始18750USDT；20/80仅初始资金占比，不归一化、缩放旧NAV、转移、再平衡、创建父订单或跨银行抵消保证金。对齐真实事件轴后相加完整美元NAV。

Walk-forward：2025-10-19 00:01→2026-11-14 00:01，391日复用开发历史、33日闭合上下文；无拟合/标签，仅过去可得前缀，下一分钟开盘执行。13个完整30日折+1日尾段、近40日8×5日、扩展21日5/5/5/6日。跨折继承现金/持仓，终点计费平仓，整体DD取连续全NAV。反复使用日期不是未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日波动×sqrt(订单额/过去20日quoteADV)冲击；不利tick/LOT/minnotional、参与率≤0.001、1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流随倍率放大、收入不放大；USDT线性永续无现货借币。缺L2/TCA、完整阶梯、tick清算和容量实证，成本/风险为估计。

|配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，ETH H=0.019|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|ETH组件，ETH H=0.021|rejected|3.346056 / 3.123722 / 2.901512|1.835160|1.124937|1.474523|4/13|0/0/0（各/8）|
|组合BTCH=0.03，ETH H=0.019|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|组合BTCH=0.0325，ETH H=0.019|passed|9.181407 / 8.635555 / 8.089884|1.357834|2.313647|5.547208|12/13|6/6/6（各/8）|
|组合BTCH=0.03，ETH H=0.021|passed|6.322885 / 5.899289 / 5.475805|1.373603|1.841723|3.714724|12/13|6/6/6（各/8）|
|组合BTCH=0.0325，ETH H=0.021|passed|6.215286 / 5.792386 / 5.369597|1.373603|1.807304|3.642798|12/13|6/6/6（各/8）|

与旧ETH H0.02同BTC对照比较，3/6项完整1/2/3倍成本路径相同。逐成本原生成交、实际资金费和desired是否相同见parameter_path_equivalence.json；参数数值变化不自动形成新收益路径，不把定义数当独立盈利证据。

本批仅检验固定S16/D3/K0.0075、M4/R0.0075/VW9、入场V6/cap0.05625及其他规则下的三个ETH耦合快ROC门槛，与两BTC门槛交叉。完整路径是否相同、各相邻跳变和边界均如实列出，不因参数数目推断独立收益证据，不外推为所有趋势跨度、风险上限或市场状态的宽泛稳健性。
启发式跳变边：[{"scope": "native", "from": "ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4_BudgetVW9R0p0075_391d", "to": "ETH_longonly_L5H0p021E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d", "delta_net_pp": -3.40035870092108, "delta_sharpe": -0.7360372226057472, "delta_DD_pp": 0.3061763627789649, "delta_Calmar": -2.36512583061699}]
启发式标记由10条相邻边的实际指标差计算，逐边保留来源、方向与变化值；只读BTC边与新ETH快H边分别辨认，既不隐去参数断崖，也不把混合尺度提示当统计显著性或广泛稳健性证明。
H=1.75%/2.25%的同条件配置已有真实结果，本批不重算；仅评估预设的新H=1.9%/2.1%及只读2%对照。代表H=1.9%/BTCH=3%保持事前约定，保留所有边界、跳变与平局，不根据结果扩网格、换代表或宣称全局最优。

双轴敏感性保存42成本场景、588逐折、336近40日折、168扩展折、16464日NAV、10相邻边和六面热图。启发式跳变标记1/10；6项新配置有6条不同完整成本路径，其中3条匹配旧参考。保留边界和变差结果，不在看结果后扩网格或换代表。

失败判据预先固定：各成本全期/近期正收益、1x≥10/13正月、各成本近期≥6/8正折、扩展≥3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、≥4平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规、终点flat。
ETH_longonly_L5H0p019E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p021E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHFastH0p019L5E0p0075_EWMS16D3K0p0075V6Cap0p05625M4BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHFastH0p019L5E0p0075_EWMS16D3K0p0075V6Cap0p05625M4BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHFastH0p021L5E0p0075_EWMS16D3K0p0075V6Cap0p05625M4BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHFastH0p021L5E0p0075_EWMS16D3K0p0075V6Cap0p05625M4BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。

相对同BTC旧ETH H0.02/L5/S16/D3的三倍成本配对增量：
ETH H=0.019/BTC H=0.03：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
ETH H=0.019/BTC H=0.0325：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
ETH H=0.021/BTC H=0.03：收益-2.720287个百分点，整体DD0.015769个百分点，Sharpe-0.501227，Calmar-1.905122，完整成本路径相同=False。
ETH H=0.021/BTC H=0.0325：收益-2.720287个百分点，整体DD0.015769个百分点，Sharpe-0.506343，Calmar-1.904410，完整成本路径相同=False。
ETH H=0.019 cost=1：固定资金费计数变化0次、选择记录变化0次、中位费率变化0次，耦合快H的long/short字段变化391/391次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
ETH H=0.019 cost=2：固定资金费计数变化0次、选择记录变化0次、中位费率变化0次，耦合快H的long/short字段变化391/391次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
ETH H=0.019 cost=3：固定资金费计数变化0次、选择记录变化0次、中位费率变化0次，耦合快H的long/short字段变化391/391次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
ETH H=0.021 cost=1：固定资金费计数变化0次、选择记录变化0次、中位费率变化0次，耦合快H的long/short字段变化391/391次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化5，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH H=0.021 cost=2：固定资金费计数变化0次、选择记录变化0次、中位费率变化0次，耦合快H的long/short字段变化391/391次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化5，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH H=0.021 cost=3：固定资金费计数变化0次、选择记录变化0次、中位费率变化0次，耦合快H的long/short字段变化391/391次，固定入场波动上限变化0次，固定资金费预算比例变化0次，固定趋势门槛变化0次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化5，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。

独立核验2346个新决策、5865个只读决策及完整账本/成本/资金费/风险/NAV。匹配持有3x收益-14.782911%、DD18.454767%，现金0。全部成本、逐折、敏感性和完整日NAV见report.json、results与exports。

本轮SMA/single 2026-11-18T12:30:00Z→2026-11-18T14:30:00Z、L4/FEWM 2026-11-18T14:10:00Z→2026-11-18T16:10:00Z均无日决策。实际资金费行{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}、日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}来自已执行独立审计。本轮L4/FEWM仅按自己的原持仓与成本场景记实际16一次；single窗结束14:30尚未覆盖16，不提前入账；08未重复。现金按本窗实际事件核对。持仓/入场/desired/执行费用保持，资金费后的现金不重置；single ETH空头{'1': '-1.644000000000000000', '2': '-1.644000000000000000', '3': '-1.644000000000000000'}保留。首08来源UTC仍2026-11-18T18:34:09.827345Z且字节SHA不改，新查来源UTC为2026-11-19T02:38:28.559917Z另存。下一SMA/single ['2026-11-18T14:30:00Z', '2026-11-18T16:30:00Z']须按自己BTC/ETH持仓将已知16记一次；L4/FEWM ['2026-11-18T16:10:00Z', '2026-11-18T18:10:00Z']不得重复16，仍须完整查询实际特殊事件。四账户下一日决策Nov19_00:01，full70SPOT与69日前缀保留，不采用研究快入场门槛、不重启或强平。本轮已使用按事件覆盖核对的门禁，后续仅在查询覆盖相同已知08事件时核对原字段，不要求不重叠查询的完整响应相同。

原SMA3x累计收益-7.468958%。四原账户为延迟shadow；十策略真实报价模拟只读保留，未创建paper新成交或改规则。原180日/六折观察计划未成熟，继续原计划。
保存18份唯一公共GET回执，本轮18、复用旧0、真实运输失败0。未新下载SPOT日线，原完整70日权威另保留；首00来源时间/SHA不变，新查询另存。
只读监控生成成功=True；11104研究配置、11098旧行完整字典不变。

实际复现命令（已完成目录禁止重评；读取既有证据核验）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261119T023142Z/commands.py prepare
python3 -B research/experiments/20261119T023142Z/commands.py freeze
python3 -B research/experiments/20261119T023142Z/commands.py units
python3 -B research/experiments/20261119T023142Z/commands.py bind
python3 -B research/experiments/20261119T023142Z/commands.py reserve_0
python3 -B research/experiments/20261119T023142Z/commands.py evaluate
python3 -B research/experiments/20261119T023142Z/commands.py audit
python3 -B research/experiments/20261119T023142Z/commands.py exports
python3 -B research/experiments/20261119T023142Z/commands.py finish_0
python3 -B research/experiments/20261119T023142Z/commands.py research_check
python3 -B research/experiments/20261119T023142Z/commands.py l4h02
python3 -B research/experiments/20261119T023142Z/commands.py fewm
python3 -B research/experiments/20261119T023142Z/commands.py candidate
python3 -B research/experiments/20261119T023142Z/commands.py forward
python3 -B research/experiments/20261119T023142Z/commands.py accounts_check
python3 -B research/experiments/20261119T023142Z/commands.py journal
python3 -B research/experiments/20261119T023142Z/commands.py sources_check
python3 -B research/experiments/20261119T023142Z/commands.py gates
python3 -B research/experiments/20261119T023142Z/commands.py feed
python3 -B research/experiments/20261119T023142Z/commands.py collect
python3 -B research/experiments/20261119T023142Z/commands.py final_checks
```

每个native退出码、stdout/stderr、spec、数据SHA、负折、实际账本和失败记录均保留。

本轮实际读取[Binance官方资金费历史接口](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)确认资金费与时间/标记价字段；以实际事件为准，不固定8小时。使用原始数据格式及来源时间说明见[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。衰减定义参考[pandas3.1.1 EWM](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)；有限16项支持与D3比值为预先明确的自定义规则。快ROC门槛、成熟范围、资金费预算公式、三日趋势门槛及有限支持为预先固定的自定义规则；本轮实际文档访问与版本记录见primary_source_access.json。
