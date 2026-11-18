# 20261118T162941Z ETH入场波动窗口研究

预先固定ETH入场波动窗口V=[5,6旧只读,7]天 × 旧BTC H=[0.03,0.0325]，代表V5/H0.03不随结果改变。6项新配置（2组件、4完整银行组合）逐项先reserve，实际执行一次并finish。历史门槛通过组合4/4；ETH组件通过0/2、淘汰2/2。严格同时改善收益、整体DD、Sharpe及Calmar为0/4。历史正收益不代表稳定实盘盈利，独立未来资格不足。

完整读取38100条事件、18911个ID、465份既往结论和29份附加材料。初始16项实际结果缺口0，legacy标记和原ZIP证据分别保留。规范研究定义11509→11515，正式有结果11302；定义数不是独立试验数，无DSR/PBO显著性证明。

经济假设：短/长入场波动估计窗口对暂时与持续风险反应不同，可能改变入场、换手成本与回撤。仅entry_volatility_window_days及描述字段改变，过去V条已闭合日对数收益的样本标准差采用V-1分母，需要V+1个过去闭合价格；超过5.625%才阻挡新建或反转，等于阈值通过，已有数量不缩放。V不是快速ROC回看L、EWM跨度、资金费预算VW9或冲击窗口20。固定L5/H2%/exitE0.75%、有限EWM S16/beta15/17/D3/K0.75%、入场cap5.625%、M4/R0.0075/VW9。这里V-1是样本方差的Bessel校正，开方后的样本标准差不宣称总体波动的无偏估计。完整金融引擎与核算源码字节相同。

完整规则：ETH longonly fixedfastL5/H.02,exitE.0075. Fast r=lastcompletedclose/closeLcompleteddaysearlier-1;contrarianbase=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0;strict E equality exits. Finite normalized EWM fixedS16,beta15/17,latest16completedcloses; slope=currentlevel/samefinitelevel3completeddaysearlier-1,strictabsoluteK.0075 over3days,notdailyized. Gate=+1 if slope>.0075,-1 if slope<-.0075,else0;acceptbase ifbase==actual or base==gate,else0. Entryrisk unbiasedsamplelogvol V[5,6readonly,7]/cap.05625 onlynew/reversed,equalitypasses. LatestM4actual signedfundingmedian mature1to36hinclusive/available<=signal;outgoingcost<=min(.0002,.0075*past9completedunbiasedsamplelogvol*latesteligibleactualintervalhours/24),equalitypasses,missingblocksnewentryonly;entrygatesdo_not_resize_actualq;finallymax(desired,0). BTCreadonly L29 mainH[.03,.0325],exitE.005,V10cap.0275,recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. FastL,exitE,fastH,trendK,lagD,entryriskV5/6/7,carryVW9,impactV20distinct.

原始完整银行权重[1,1]：BTC C3750/N1000、ETH C15000/N4000，总初始18750USDT；20/80仅初始资金占比，不归一化、缩放旧NAV、转移、再平衡、创建父订单或跨银行抵消保证金。对齐真实事件轴后相加完整美元NAV。

Walk-forward：2025-10-19 00:01→2026-11-14 00:01，391日复用开发历史、33日闭合上下文；无拟合/标签，仅过去可得前缀，下一分钟开盘执行。13个完整30日折+1日尾段、近40日8×5日、扩展21日5/5/5/6日。跨折继承现金/持仓，终点计费平仓，整体DD取连续全NAV。反复使用日期不是未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日波动×sqrt(订单额/过去20日quoteADV)冲击；不利tick/LOT/minnotional、参与率≤0.001、1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流随倍率放大、收入不放大；USDT线性永续无现货借币。缺L2/TCA、完整阶梯、tick清算和容量实证，成本/风险为估计。

|配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，V=5天|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|ETH组件，V=7天|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|组合BTCH=0.03，V=5天|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|组合BTCH=0.0325，V=5天|passed|9.181407 / 8.635555 / 8.089884|1.357834|2.313647|5.547208|12/13|6/6/6（各/8）|
|组合BTCH=0.03，V=7天|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|组合BTCH=0.0325，V=7天|passed|9.181407 / 8.635555 / 8.089884|1.357834|2.313647|5.547208|12/13|6/6/6（各/8）|

与旧V6同BTC对照比较，6/6项完整1/2/3倍成本路径相同。逐成本原生成交、实际资金费和desired是否相同见parameter_path_equivalence.json；波动估计数值变化不自动形成新收益路径，不把定义数当独立盈利证据。

固定5.625%上限和本批其余规则下，V5/6/7的已保存完整成本路径呈条件平台；这是参数变动未产生新增收益路径的证据，不外推为所有波动上限、资金规模或市场状态的宽泛稳健性。
启发式跳变边：[{"scope": "native", "from": "BTC_L29_H3_E0p005_V10cap0p0275_RecentConfirm5_Min0p0025_391d", "to": "BTC_L29_H0p0325_E0p005_V10cap0p0275_RecentConfirm5_Min0p0025_391d", "delta_net_pp": -0.5310350827707264, "delta_sharpe": -0.04858481063530795, "delta_DD_pp": 0.0, "delta_Calmar": -0.08500611923548096}]

双轴敏感性保存42成本场景、588逐折、336近40日折、168扩展折、16464日NAV、10相邻边和六面热图。启发式跳变标记1/10；6项新配置有3条不同完整成本路径，其中3条匹配旧参考。保留边界和变差结果，不在看结果后扩网格或换代表。

失败判据预先固定：各成本全期/近期正收益、1x≥10/13正月、各成本近期≥6/8正折、扩展≥3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、≥4平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规、终点flat。
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV5Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV7Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHV5L5E0p0075_EWMS16D3K0p0075Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHV5L5E0p0075_EWMS16D3K0p0075Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHV7L5E0p0075_EWMS16D3K0p0075Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHV7L5E0p0075_EWMS16D3K0p0075Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。

相对同BTC旧ETH V6/L5/S16/D3的三倍成本配对增量：
V=5/BTC H=0.03：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
V=5/BTC H=0.0325：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
V=7/BTC H=0.03：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
V=7/BTC H=0.0325：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
V=5 cost=1：入场波动窗口变化391次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
V=5 cost=2：入场波动窗口变化391次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
V=5 cost=3：入场波动窗口变化391次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
V=7 cost=1：入场波动窗口变化391次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
V=7 cost=2：入场波动窗口变化391次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。
V=7 cost=3：入场波动窗口变化391次，固定快回看变化0、快ROC变化0次；固定退出缓冲变化0、EWM滞后变化0、跨度变化0；最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。保存路径差异不视为同状态反事实。

独立核验2346个新决策、5865个只读决策及完整账本/成本/资金费/风险/NAV。匹配持有3x收益-14.782911%、DD18.454767%，现金0。全部成本、逐折、敏感性和完整日NAV见report.json、results与exports。

本轮SMA/single 2026-11-18T02:30:00Z→2026-11-18T04:30:00Z、L4/FEWM 2026-11-18T04:10:00Z→2026-11-18T06:10:00Z均仅续接闭合盯市。真实新查资金费{'BTC': [], 'ETH': []}；实际资金费行{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、日事件{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}均来自已执行审计。18份原永续账本现金/数量/入场/费用全部保持，single ETH空头{'1': '-1.644000000000000000', '2': '-1.644000000000000000', '3': '-1.644000000000000000'}继续持有，未重启或强平；完整旧NAV前缀、原70日SPOT权威及69日前缀保留。首Nov18_00资金费来源UTC仍2026-11-18T10:35:18.941062Z且字节不改。下一SMA/single ['2026-11-18T04:30:00Z', '2026-11-18T06:30:00Z']、L4/FEWM ['2026-11-18T06:10:00Z', '2026-11-18T08:10:00Z']仍mark-only，四账户下一日决策Nov19_00:01。先reserve新窗口，新查实际资金费，只记各自新事件，不采用研究L、不重复00或日决策。 下一L4/FEWM06:10→08:10没有日决策，但覆盖可能的08资金费边界；必须完整新查实际结算，按各自持仓与成本场景入账，并另存首次真实08来源UTC/原字节。不得把mark-only理解为忽略真实资金费，也不得本轮预记。Single下一窗口仍应完整查询特殊实际事件，自己的08结算须到自己的覆盖窗口处理。

原SMA3x累计收益-7.468958%。四原账户为延迟shadow；十策略真实报价模拟只读保留，未创建paper新成交或改规则。原180日/六折观察计划未成熟，继续原计划。
保存18份唯一公共GET回执，本轮18、复用旧0、真实运输失败0。未新下载SPOT日线，原完整70日权威另保留；首00来源时间/SHA不变，新查询另存。
只读监控生成成功=True；11074研究配置、11068旧行完整字典不变。

实际复现命令（已完成目录禁止重评；读取既有证据核验）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261118T162941Z/commands.py prepare
python3 -B research/experiments/20261118T162941Z/commands.py freeze
python3 -B research/experiments/20261118T162941Z/commands.py units
python3 -B research/experiments/20261118T162941Z/commands.py bind
python3 -B research/experiments/20261118T162941Z/commands.py reserve_0
python3 -B research/experiments/20261118T162941Z/commands.py evaluate
python3 -B research/experiments/20261118T162941Z/commands.py audit
python3 -B research/experiments/20261118T162941Z/commands.py exports
python3 -B research/experiments/20261118T162941Z/commands.py finish_0
python3 -B research/experiments/20261118T162941Z/commands.py research_check
python3 -B research/experiments/20261118T162941Z/commands.py l4h02
python3 -B research/experiments/20261118T162941Z/commands.py fewm
python3 -B research/experiments/20261118T162941Z/commands.py candidate
python3 -B research/experiments/20261118T162941Z/commands.py forward
python3 -B research/experiments/20261118T162941Z/commands.py accounts_check
python3 -B research/experiments/20261118T162941Z/commands.py journal
python3 -B research/experiments/20261118T162941Z/commands.py sources_check
python3 -B research/experiments/20261118T162941Z/commands.py gates
python3 -B research/experiments/20261118T162941Z/commands.py feed
python3 -B research/experiments/20261118T162941Z/commands.py collect
python3 -B research/experiments/20261118T162941Z/commands.py final_checks
```

每个native退出码、stdout/stderr、spec、数据SHA、负折、实际账本和失败记录均保留。

本轮实际读取[Binance官方资金费历史接口](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)确认资金费与时间/标记价字段；以实际事件为准，不固定8小时。使用原始数据格式及来源时间说明见[公共数据README](https://github.com/binance/binance-public-data/blob/master/README.md)。衰减定义参考[pandas3.1.1 EWM](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)；有限16项支持与D3比值为预先明确的自定义规则。样本波动采用[Python3.12官方statistics](https://docs.python.org/3.12/library/statistics.html)的V-1自由度定义；V日窗口、固定上限和仅作用新入场为预先固定规则。可选pandas rolling文档404及官方回退读取记录见primary_source_access.json。
