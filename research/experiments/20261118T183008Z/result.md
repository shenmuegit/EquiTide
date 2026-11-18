# 20261118T183008Z ETH趋势强度门槛研究

预先固定ETH绝对三日趋势门槛K=[0.00625,0.0075旧只读,0.00875] × 旧BTC H=[0.03,0.0325]，代表ETHK0.00625/BTCH0.03不随结果改变。6项新配置（2组件、4完整银行组合）逐项先reserve，实际执行一次并finish。历史门槛通过组合4/4；ETH组件通过0/2、淘汰2/2。严格同时改善收益、整体DD、Sharpe及Calmar为0/4。历史正收益不代表稳定实盘盈利，独立未来资格不足。

完整读取38156条事件、18939个ID、466份既往结论和29份附加材料。初始16项实际结果缺口0，legacy标记和原ZIP证据分别保留。规范研究定义11515→11521，正式有结果11308；定义数不是独立试验数，无DSR/PBO显著性证明。

经济假设：较低/较高的趋势确认门槛可能接纳较弱趋势或要求更强确认，从而改变换手、成本和回撤。仅trend_slope_hurdle_fraction及描述字段改变。门槛比较当前16项有限归一化EWM与3日前同有限EWM的比值减一；K为绝对三日变化0.625%/0.75%/0.875%，不是日化值。严格大于K为正、严格小于-K为负，等于边界中性；只过滤新建/反转，已有数量不缩放。固定L5/H2%/exitE0.75%、S16/beta15/17/D3、入场V6/cap5.625%、M4/R0.0075/VW9，整个金融引擎与核算源码字节相同。

完整规则：ETH longonly fixedfastL5/H.02,exitE.0075. Fast r=lastcompletedclose/closeLcompleteddaysearlier-1;contrarianbase=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0;strict E equality exits. Finite normalized EWM fixedS16,beta15/17,latest16completedcloses; slope=currentlevel/samefinitelevel3completeddaysearlier-1,strictabsoluteK[.00625,.0075readonly,.00875] over3days,notdailyized. Gate=+1 if slope>K,-1 if slope<-K,else0;acceptbase ifbase==actual or base==gate,else0. Entryrisk samplelogvol V6/cap.05625 onlynew/reversed,equalitypasses. LatestM4actual signedfundingmedian mature1to36hinclusive/available<=signal;outgoingcost<=min(.0002,.0075*past9completedunbiasedsamplelogvol*latesteligibleactualintervalhours/24),equalitypasses,missingblocksnewentryonly;entrygatesdo_not_resize_actualq;finallymax(desired,0). BTCreadonly L29 mainH[.03,.0325],exitE.005,V10cap.0275,recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. FastL,exitE,fastH,trendK,lagD,entryriskV6,carryVW9,impactV20distinct.

原始完整银行权重[1,1]：BTC C3750/N1000、ETH C15000/N4000，总初始18750USDT；20/80仅初始资金占比，不归一化、缩放旧NAV、转移、再平衡、创建父订单或跨银行抵消保证金。对齐真实事件轴后相加完整美元NAV。

Walk-forward：2025-10-19 00:01→2026-11-14 00:01，391日复用开发历史、33日闭合上下文；无拟合/标签，仅过去可得前缀，下一分钟开盘执行。13个完整30日折+1日尾段、近40日8×5日、扩展21日5/5/5/6日。跨折继承现金/持仓，终点计费平仓，整体DD取连续全NAV。反复使用日期不是未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日波动×sqrt(订单额/过去20日quoteADV)冲击；不利tick/LOT/minnotional、参与率≤0.001、1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流随倍率放大、收入不放大；USDT线性永续无现货借币。缺L2/TCA、完整阶梯、tick清算和容量实证，成本/风险为估计。

|配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，ETH K=0.625%|rejected|5.632508 / 5.191694 / 4.751173|4.103613|1.077719|1.079134|7/13|0/0/0（各/8）|
|ETH组件，ETH K=0.875%|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|组合BTCH=0.03，ETH K=0.625%|passed|8.152047 / 7.553666 / 6.955534|3.820753|1.609138|1.695572|11/13|6/6/6（各/8）|
|组合BTCH=0.0325，ETH K=0.625%|passed|8.044448 / 7.446763 / 6.849327|3.820753|1.585551|1.669738|11/13|6/6/6（各/8）|
|组合BTCH=0.03，ETH K=0.875%|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|组合BTCH=0.0325，ETH K=0.875%|passed|9.181407 / 8.635555 / 8.089884|1.357834|2.313647|5.547208|12/13|6/6/6（各/8）|

与旧ETH K0.0075同BTC对照比较，3/6项完整1/2/3倍成本路径相同。逐成本原生成交、实际资金费和desired是否相同见parameter_path_equivalence.json；波动估计数值变化不自动形成新收益路径，不把定义数当独立盈利证据。

本批仅检验固定S16/D3及其他规则下的三个ETH绝对趋势门槛，与两BTC门槛交叉。完整路径是否相同、各相邻跳变和边界均如实列出，不因参数数目推断独立收益证据，不外推为所有趋势跨度、风险上限或市场状态的宽泛稳健性。
启发式跳变边：[{"scope": "native", "from": "ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00625_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d", "to": "ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4_BudgetVW9R0p0075_391d", "delta_net_pp": 1.5506973833481874, "delta_sharpe": 0.7832554162071368, "delta_DD_pp": -2.574629397250861, "delta_Calmar": 2.7605148865453977}, {"scope": "parent", "from": "parent_ETHK0p00625L5E0p0075_EWMS16D3V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d", "to": "parent_ETHEntryRiskV6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d", "delta_net_pp": 1.2405579066785402, "delta_sharpe": 0.7338124205796712, "delta_DD_pp": -2.462918900633604, "delta_Calmar": 3.924274378523717}, {"scope": "parent", "from": "parent_ETHK0p00625L5E0p0075_EWMS16D3V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d", "to": "parent_ETHEntryRiskV6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d", "delta_net_pp": 1.2405579066785632, "delta_sharpe": 0.7280960959417755, "delta_DD_pp": -2.462918900633604, "delta_Calmar": 3.8774707659214256}]

双轴敏感性保存42成本场景、588逐折、336近40日折、168扩展折、16464日NAV、10相邻边和六面热图。启发式跳变标记3/10；6项新配置有6条不同完整成本路径，其中3条匹配旧参考。保留边界和变差结果，不在看结果后扩网格或换代表。

失败判据预先固定：各成本全期/近期正收益、1x≥10/13正月、各成本近期≥6/8正折、扩展≥3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、≥4平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规、终点flat。
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00625_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p00875_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHK0p00625L5E0p0075_EWMS16D3V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHK0p00625L5E0p0075_EWMS16D3V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHK0p00875L5E0p0075_EWMS16D3V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHK0p00875L5E0p0075_EWMS16D3V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。

相对同BTC旧ETH K0.0075/L5/S16/D3的三倍成本配对增量：
ETH K=0.00625/BTC H=0.03：收益-1.240558个百分点，整体DD2.462919个百分点，Sharpe-0.733812，Calmar-3.924274，完整成本路径相同=False。
ETH K=0.00625/BTC H=0.0325：收益-1.240558个百分点，整体DD2.462919个百分点，Sharpe-0.728096，Calmar-3.877471，完整成本路径相同=False。
ETH K=0.00875/BTC H=0.03：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
ETH K=0.00875/BTC H=0.0325：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
ETH K=0.00625 cost=1：趋势门槛变化391次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化8，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH K=0.00625 cost=2：趋势门槛变化391次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化8，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH K=0.00625 cost=3：趋势门槛变化391次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化8，成交相同=False，资金费相同=False，NAV相同=False。保存路径差异不视为同状态反事实。
ETH K=0.00875 cost=1：趋势门槛变化391次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
ETH K=0.00875 cost=2：趋势门槛变化391次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
ETH K=0.00875 cost=3：趋势门槛变化391次，固定入场波动窗口变化0次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。

独立核验2346个新决策、5865个只读决策及完整账本/成本/资金费/风险/NAV。匹配持有3x收益-14.782911%、DD18.454767%，现金0。全部成本、逐折、敏感性和完整日NAV见report.json、results与exports。

本轮SMA/single 2026-11-18T04:30:00Z→2026-11-18T06:30:00Z、L4/FEWM 2026-11-18T06:10:00Z→2026-11-18T08:10:00Z均无日决策。实际资金费行{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}、日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}均由独立已执行审计导出。L4/FEWM仅按各自原持仓/成本场景记自己的新结算，所有q/入场/desired/执行费保持，资金费后的现金不重置。Single ETH空头{'1': '-1.644000000000000000', '2': '-1.644000000000000000', '3': '-1.644000000000000000'}保留，未在其窗口预记08。首08来源UTC为2026-11-18T18:34:09.827345Z，原00来源UTC仍2026-11-18T10:35:18.941062Z，各原字节SHA保持。下一SMA/single ['2026-11-18T06:30:00Z', '2026-11-18T08:30:00Z']需新查并仅由single记自己的08一次；L4/FEWM ['2026-11-18T08:10:00Z', '2026-11-18T10:10:00Z']不得重复已入账08，仍须完整新查特殊实际结算。四账户下一日决策Nov19_00:01，full70SPOT及69日前缀不变，不采用研究K、不重启或强平。

原SMA3x累计收益-7.468958%。四原账户为延迟shadow；十策略真实报价模拟只读保留，未创建paper新成交或改规则。原180日/六折观察计划未成熟，继续原计划。
保存18份唯一公共GET回执，本轮18、复用旧0、真实运输失败0。未新下载SPOT日线，原完整70日权威另保留；首00来源时间/SHA不变，新查询另存。
只读监控生成成功=True；11080研究配置、11074旧行完整字典不变。

实际复现命令（已完成目录禁止重评；读取既有证据核验）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261118T183008Z/commands.py prepare
python3 -B research/experiments/20261118T183008Z/commands.py freeze
python3 -B research/experiments/20261118T183008Z/commands.py units
python3 -B research/experiments/20261118T183008Z/commands.py bind
python3 -B research/experiments/20261118T183008Z/commands.py reserve_0
python3 -B research/experiments/20261118T183008Z/commands.py evaluate
python3 -B research/experiments/20261118T183008Z/commands.py audit
python3 -B research/experiments/20261118T183008Z/commands.py exports
python3 -B research/experiments/20261118T183008Z/commands.py finish_0
python3 -B research/experiments/20261118T183008Z/commands.py research_check
python3 -B research/experiments/20261118T183008Z/commands.py l4h02
python3 -B research/experiments/20261118T183008Z/commands.py fewm
python3 -B research/experiments/20261118T183008Z/commands.py candidate
python3 -B research/experiments/20261118T183008Z/commands.py forward
python3 -B research/experiments/20261118T183008Z/commands.py accounts_check
python3 -B research/experiments/20261118T183008Z/commands.py journal
python3 -B research/experiments/20261118T183008Z/commands.py sources_check
python3 -B research/experiments/20261118T183008Z/commands.py gates
python3 -B research/experiments/20261118T183008Z/commands.py feed
python3 -B research/experiments/20261118T183008Z/commands.py collect
python3 -B research/experiments/20261118T183008Z/commands.py final_checks
```

每个native退出码、stdout/stderr、spec、数据SHA、负折、实际账本和失败记录均保留。

本轮实际读取[Binance官方资金费历史接口](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)确认资金费与时间/标记价字段；以实际事件为准，不固定8小时。使用原始数据格式及来源时间说明见[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。衰减定义参考[pandas3.1.1 EWM](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)；有限16项支持与D3比值为预先明确的自定义规则。三日绝对趋势门槛及有限支持为预先固定的自定义规则；本轮实际文档访问与版本记录见primary_source_access.json。
