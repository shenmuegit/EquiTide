# 20261118T142910Z ETH快速回看期研究

预先固定ETH快回看L=[4,5旧只读,6]天 × 旧BTC H=[0.03,0.0325]，代表L4/H0.03不随结果改变。6项新配置（2组件、4完整银行组合）逐项先reserve，实际执行一次并finish。历史门槛通过组合4/4；ETH组件通过0/2、淘汰2/2。严格同时改善收益、整体DD、Sharpe及Calmar为0/4。历史正收益不代表稳定实盘盈利，独立未来资格不足。

完整读取38044条事件、18883个ID、464份既往结论和29份附加材料。初始16项实际结果缺口0，legacy标记和原ZIP证据分别保留。规范研究定义11503→11509，正式有结果11296；定义数不是独立试验数，无DSR/PBO显著性证明。

经济假设：较短/较长的反转记忆可能改变信号时机、换手成本与回撤。仅lookback_days及描述字段改变，当前已闭合价格除以L天前已闭合价格减一；L是天数，不是资金权重、EWM跨度或斜率滞后。固定H2%/exitE0.75%、有限EWM S16/beta15/17/D3/K0.75%、入场风险V6/cap5.625%、M4/R0.0075/VW9。完整金融引擎和原生核算源码字节相同。

完整规则：ETH longonly fastL[4,5readonly,6]/H.02,exitE.0075. Fast r=lastcompletedclose/closeLcompleteddaysearlier-1;contrarianbase=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0;strict E equality exits. Finite normalized EWM fixedS16,beta15/17,latest16completedcloses; slope=currentlevel/samefinitelevel3completeddaysearlier-1,strictabsoluteK.0075 over3days,notdailyized. Gate=+1 if slope>.0075,-1 if slope<-.0075,else0;acceptbase ifbase==actual or base==gate,else0. Entryrisk samplelogvol V6/cap.05625 onlynew/reversed,equalitypasses. LatestM4actual signedfundingmedian mature1to36hinclusive/available<=signal;outgoingcost<=min(.0002,.0075*past9completedunbiasedsamplelogvol*latesteligibleactualintervalhours/24),equalitypasses,missingblocksnewentryonly;entrygatesdo_not_resize_actualq;finallymax(desired,0). BTCreadonly L29 mainH[.03,.0325],exitE.005,V10cap.0275,recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. FastL,exitE,fastH,trendK,lagD,entryriskV6,carryVW9,impactV20distinct.

原始完整银行权重[1,1]：BTC C3750/N1000、ETH C15000/N4000，总初始18750USDT；20/80仅初始资金占比，不归一化、缩放旧NAV、转移、再平衡、创建父订单或跨银行抵消保证金。对齐真实事件轴后相加完整美元NAV。

Walk-forward：2025-10-19 00:01→2026-11-14 00:01，391日复用开发历史、33日闭合上下文；无拟合/标签，仅过去可得前缀，下一分钟开盘执行。13个完整30日折+1日尾段、近40日8×5日、扩展21日5/5/5/6日。跨折继承现金/持仓，终点计费平仓，整体DD取连续全NAV。反复使用日期不是未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日波动×sqrt(订单额/过去20日quoteADV)冲击；不利tick/LOT/minnotional、参与率≤0.001、1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流随倍率放大、收入不放大；USDT线性永续无现货借币。缺L2/TCA、完整阶梯、tick清算和容量实证，成本/风险为估计。

|配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，L=4天|rejected|4.111931 / 3.601113 / 3.090056|3.978991|0.800748|0.724216|6/13|0/0/0（各/8）|
|ETH组件，L=6天|rejected|3.115522 / 2.852853 / 2.590193|1.119328|1.528496|2.158340|3/13|0/0/0（各/8）|
|组合BTCH=0.03，L=4天|passed|6.935586 / 6.281202 / 5.626640|4.346063|1.387157|1.206346|10/13|6/6/6（各/8）|
|组合BTCH=0.0325，L=4天|passed|6.827986 / 6.174299 / 5.520433|4.346063|1.361369|1.183615|10/13|6/6/6（各/8）|
|组合BTCH=0.03，L=6天|passed|6.138459 / 5.682594 / 5.226749|1.215308|1.965366|4.007928|10/13|6/6/6（各/8）|
|组合BTCH=0.0325，L=6天|passed|6.030859 / 5.575691 / 5.120542|1.215308|1.926400|3.926621|10/13|6/6/6（各/8）|

双轴敏感性保存42成本场景、588逐折、336近40日折、168扩展折、16464日NAV、10相邻边和六面热图。启发式跳变标记3/10；6项新配置有6条不同完整成本路径，其中0条匹配旧参考。保留边界和变差结果，不在看结果后扩网格或换代表。

失败判据预先固定：各成本全期/近期正收益、1x≥10/13正月、各成本近期≥6/8正折、扩展≥3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、≥4平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规、终点flat。
ETH_longonly_L4H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L6H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHL4E0p0075_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHL4E0p0075_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHL6E0p0075_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHL6E0p0075_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。

相对同BTC旧ETH L5/S16/D3的三倍成本配对增量：
L=4/BTC H=0.03：收益-2.569451个百分点，整体DD2.988229个百分点，Sharpe-0.955794，Calmar-4.413500，完整成本路径相同=False。
L=4/BTC H=0.0325：收益-2.569451个百分点，整体DD2.988229个百分点，Sharpe-0.952278，Calmar-4.363593，完整成本路径相同=False。
L=6/BTC H=0.03：收益-2.969342个百分点，整体DD-0.142526个百分点，Sharpe-0.377584，Calmar-1.611918，完整成本路径相同=False。
L=6/BTC H=0.0325：收益-2.969342个百分点，整体DD-0.142526个百分点，Sharpe-0.387247，Calmar-1.620587，完整成本路径相同=False。
L=4 cost=1：快回看参数变化391次，快ROC变化391次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化28，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
L=4 cost=2：快回看参数变化391次，快ROC变化391次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化28，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
L=4 cost=3：快回看参数变化391次，快ROC变化391次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化28，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
L=6 cost=1：快回看参数变化391次，快ROC变化391次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化11，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
L=6 cost=2：快回看参数变化391次，快ROC变化391次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化11，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
L=6 cost=3：快回看参数变化391次，快ROC变化391次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化11，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。

独立核验2346个新决策、5865个只读决策及完整账本/成本/资金费/风险/NAV。匹配持有3x收益-14.782911%、DD18.454767%，现金0。全部成本、逐折、敏感性和完整日NAV见report.json、results与exports。

本轮SMA/single 2026-11-18T00:30:00Z→2026-11-18T02:30:00Z、L4/FEWM 2026-11-18T02:10:00Z→2026-11-18T04:10:00Z均仅续接闭合盯市。真实新查资金费{'BTC': [], 'ETH': []}；实际资金费行{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}均来自已执行审计。18份原永续账本现金/数量/入场/费用全部保持，single ETH空头{'1': '-1.644000000000000000', '2': '-1.644000000000000000', '3': '-1.644000000000000000'}继续持有，未重启或强平；完整旧NAV前缀、原70日SPOT权威及69日前缀保留。首Nov18_00资金费来源UTC仍2026-11-18T10:35:18.941062Z且字节不改。下一SMA/single ['2026-11-18T02:30:00Z', '2026-11-18T04:30:00Z']、L4/FEWM ['2026-11-18T04:10:00Z', '2026-11-18T06:10:00Z']仍mark-only，四账户下一日决策Nov19_00:01。先reserve新窗口，新查实际资金费，只记各自新事件，不采用研究L、不重复00或日决策。

原SMA3x累计收益-7.468958%。四原账户为延迟shadow；十策略真实报价模拟只读保留，未创建paper新成交或改规则。原180日/六折观察计划未成熟，继续原计划。
保存18份唯一公共GET回执，本轮18、复用旧0、真实运输失败0。未新下载SPOT日线，原完整70日权威另保留；首00来源时间/SHA不变，新查询另存。
只读监控生成成功=True；11068研究配置、11062旧行完整字典不变。

实际复现命令（已完成目录禁止重评；读取既有证据核验）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261118T142910Z/commands.py prepare
python3 -B research/experiments/20261118T142910Z/commands.py freeze
python3 -B research/experiments/20261118T142910Z/commands.py units
python3 -B research/experiments/20261118T142910Z/commands.py bind
python3 -B research/experiments/20261118T142910Z/commands.py reserve_0
python3 -B research/experiments/20261118T142910Z/commands.py evaluate
python3 -B research/experiments/20261118T142910Z/commands.py audit
python3 -B research/experiments/20261118T142910Z/commands.py exports
python3 -B research/experiments/20261118T142910Z/commands.py finish_0
python3 -B research/experiments/20261118T142910Z/commands.py research_check
python3 -B research/experiments/20261118T142910Z/commands.py l4h02
python3 -B research/experiments/20261118T142910Z/commands.py fewm
python3 -B research/experiments/20261118T142910Z/commands.py candidate
python3 -B research/experiments/20261118T142910Z/commands.py forward
python3 -B research/experiments/20261118T142910Z/commands.py accounts_check
python3 -B research/experiments/20261118T142910Z/commands.py journal
python3 -B research/experiments/20261118T142910Z/commands.py sources_check
python3 -B research/experiments/20261118T142910Z/commands.py gates
python3 -B research/experiments/20261118T142910Z/commands.py feed
python3 -B research/experiments/20261118T142910Z/commands.py collect
python3 -B research/experiments/20261118T142910Z/commands.py final_checks
```

每个native退出码、stdout/stderr、spec、数据SHA、负折、实际账本和失败记录均保留。

本轮实际读取[Binance官方资金费历史接口](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)确认资金费与时间/标记价字段；以实际事件为准，不固定8小时。使用原始数据格式及来源时间说明见[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。衰减定义参考[pandas3.1.1 EWM](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)；有限16项支持与D3比值为预先明确的自定义规则。访问记录见primary_source_access.json。
