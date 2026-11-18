# 20261118T122939Z ETH退出恢复缓冲研究

预先固定ETH退出E=[0.00625,0.0075旧只读,0.00875] × 旧BTC H=[0.03,0.0325]，代表E0.00625/H0.03不随结果改变。6项新配置（2组件、4完整银行组合）逐项先reserve，实际执行一次并finish。历史门槛通过组合4/4；ETH组件通过0/2、淘汰2/2。严格同时改善收益、整体DD、Sharpe及Calmar为0/4。历史正收益不代表稳定实盘盈利，独立未来资格不足。

完整读取37988条事件、18855个ID、463份既往结论和27份附加材料；初始16项实际结果缺口0，legacy标记和真实原ZIP证据分别保留。规范研究定义11497→11503，正式有结果11290；定义数不是独立试验数，无DSR/PBO显著性证明。

经济假设：较窄/较宽的反转恢复退出缓冲可能改变持有时间、交易成本与回撤。仅exit_buffer_fraction与描述字段改变，E是5日收益的严格保持阈值（0.625%/0.75%/0.875%），等于阈值即退出；不是手续费、趋势斜率K或资金权重。固定L5/H2%、有限EWM S16/beta15/17/D3/K0.75%、入场风险V6/cap5.625%、M4/R0.0075/VW9。完整金融引擎与核算源码原字节保持。

完整规则：ETH longonly L5/H.02,exitE[.00625,.0075readonly,.00875]. Fast r=lastcompletedclose/close5completeddaysearlier-1;contrarianbase=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<E)or(actual==-1 and r>-E),else0;strict E equality exits. Finite normalized EWM fixedS16,beta15/17,latest16completedcloses; slope=currentlevel/samefinitelevel3completeddaysearlier-1,strictabsoluteK.0075 over3days,notdailyized. Gate=+1 if slope>.0075,-1 if slope<-.0075,else0;acceptbase ifbase==actual or base==gate,else0. Entryrisk samplelogvol V6/cap.05625 onlynew/reversed,equalitypasses. LatestM4actual signedfundingmedian mature1to36hinclusive/available<=signal;outgoingcost<=min(.0002,.0075*past9completedunbiasedsamplelogvol*latesteligibleactualintervalhours/24),equalitypasses,missingblocksnewentryonly;entrygatesdo_not_resize_actualq;normalexitusesregisteredE;finallymax(desired,0). BTCreadonly L29 mainH[.03,.0325],exitE.005,V10cap.0275,recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. ExitE,fastH,trendK,lagD,entryriskV6,carryVW9,impactV20distinct.

原始完整银行权重[1,1]：BTC C3750/N1000、ETH C15000/N4000，总初始18750USDT；20/80仅为初始资金占比，不归一化、缩放旧NAV、转移、再平衡、创建父订单或跨银行抵消保证金。组合对齐真实事件轴后相加完整美元NAV。

Walk-forward：2025-10-19 00:01→2026-11-14 00:01，391日复用开发历史、33日闭合上下文；无拟合/标签，仅过去可得前缀，下一分钟开盘执行。13个完整30日折+1日尾段、近40日8×5日、扩展21日5/5/5/6日；跨折继承现金/持仓，终点计费平仓，整体DD取连续全NAV。反复使用日期不是未触碰最终测试集。

成本1/2/3倍：每边手续费5bp、半价差1bp、滑点2bp、0.5×过去20日波动×sqrt(订单额/过去20日quoteADV)冲击；不利tick/LOT/minnotional、参与率≤0.001、1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流随倍率放大、收入不放大；USDT线性永续无现货借币。缺L2/TCA、完整阶梯、tick清算和容量实证，成本/风险为估计。

|配置|状态|净收益1x/2x/3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，E=0.625%|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|ETH组件，E=0.875%|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|组合BTCH=0.03，E=0.625%|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|组合BTCH=0.0325，E=0.625%|passed|9.181407 / 8.635555 / 8.089884|1.357834|2.313647|5.547208|12/13|6/6/6（各/8）|
|组合BTCH=0.03，E=0.875%|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|组合BTCH=0.0325，E=0.875%|passed|9.181407 / 8.635555 / 8.089884|1.357834|2.313647|5.547208|12/13|6/6/6（各/8）|

六个新参数定义的完整1/2/3倍成本NAV都与各自旧E0.0075对照相同；两新ETH组件的逐笔成交、资金费和全部desired也相同，见exit_path_equivalence.json。因此本批没有新增收益路径或增量alpha，不把不同参数名当独立盈利证据；本轮预注册仍实际执行且全部结果/负折保留。

双轴敏感性保存42个新旧成本场景、588逐折、336近40日折、168扩展折、16464日NAV、10相邻边和六面热图。启发式跳变标记1/10条，批内不同完整成本路径3条，匹配旧参考3条；别名、边界、平台均保留，不当独立alpha，不在看结果后扩大网格或换代表。

失败判据预先固定：各成本全期/近期正收益、1x≥10/13正月、各成本近期≥6/8正折、扩展≥3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、≥4平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规、终点flat。
ETH_longonly_L5H0p02E0p00625_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p00875_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHE0p00625_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHE0p00625_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHE0p00875_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHE0p00875_EWMS16D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。

相对同BTC旧ETH E0.0075/S16/D3的三倍成本配对增量：
E=0.00625/BTC H=0.03：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
E=0.00625/BTC H=0.0325：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
E=0.00875/BTC H=0.03：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
E=0.00875/BTC H=0.0325：收益0.000000个百分点，整体DD0.000000个百分点，Sharpe0.000000，Calmar0.000000，完整成本路径相同=True。
E=0.00625 cost=1：退出阈值变化391次，固定滞后变化0、固定跨度变化0，最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。这是已保存真实路径逐决策差异，不视为同状态单步反事实。
E=0.00625 cost=2：退出阈值变化391次，固定滞后变化0、固定跨度变化0，最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。这是已保存真实路径逐决策差异，不视为同状态单步反事实。
E=0.00625 cost=3：退出阈值变化391次，固定滞后变化0、固定跨度变化0，最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。这是已保存真实路径逐决策差异，不视为同状态单步反事实。
E=0.00875 cost=1：退出阈值变化391次，固定滞后变化0、固定跨度变化0，最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。这是已保存真实路径逐决策差异，不视为同状态单步反事实。
E=0.00875 cost=2：退出阈值变化391次，固定滞后变化0、固定跨度变化0，最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。这是已保存真实路径逐决策差异，不视为同状态单步反事实。
E=0.00875 cost=3：退出阈值变化391次，固定滞后变化0、固定跨度变化0，最终desired变化0，成交相同=True，资金费相同=True，NAV相同=True。这是已保存真实路径逐决策差异，不视为同状态单步反事实。

独立核验2346个新决策和5865个只读决策、完整现金/数量、真实资金费、执行成本、风险和逐折/整体NAV。市场模型只执行一次，未重跑完成配置或账户窗口。匹配持有3x收益-14.782911%/DD18.454767%，现金0。所有成本/成交数/执行费用/费用安全比、逐折和完整日NAV见report.json、results/与exports/各CSV。

本轮SMA/single Nov17_22:30→Nov18_00:30跨原00:01日决策。SMA真实70日现货背景与原69日前缀一致，按原SMA65/对称1%/Float/10bp内核执行；独立原信号、成本、持仓、完整NAV审计通过。Single按自身原日背景与冻结内核处理，只记自己的00资金费。L4/FEWM00:10→02:10仅新闭合mark，不重复此前00结算或00:01日决策。实际资金费记录{'SMA': 0, 'candidate': 6, 'l4h02': 0, 'fewm': 0}、日事件{'SMA': 1, 'candidate': 1, 'l4h02': 0, 'fewm': 0}、新成交{'SMA': 0, 'candidate': 3, 'l4h02': 0, 'fewm': 0}；三永续00每资产/每成本键各一次，四原账户日决策各一次，全部旧链和18账本保留。首00公共来源UTC仍2026-11-18T10:35:18.941062Z，新查询另存、原字节SHA不改。下一SMA/single00:30→02:30，L4/FEWM02:10→04:10，均无日决策；四账户下一日决策Nov19_00:01，继续使用当前原账户现金/数量/desired与费用、实际70日权威和mark-only适配器，不能重用本轮one-daily-only门禁。完整新查实际资金费，仅记各自窗口新事件，不假定8小时、不预记未来、不采用研究E、不重启或强平。

原SMA三倍成本累计收益-7.468958%保留。各原账户是晚于参考时刻取得数据的延迟shadow，和十策略真实报价模拟分开；180日/六折未成熟不取消原冻结长期计划。
保存20份唯一公共GET回执（本轮20，复用旧成功响应0，真实运输失败0），含4份SMA70日/分钟原始响应。首00来源UTC/SHA保持，当前新查询另存。
只读监控生成成功=True；11062研究行，11056旧行完整字典保持；不新建模拟成交或修改paper冻结规则。

实际命令（已完成目录禁止重新评估；仅核验读取既有证据）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261118T122939Z/commands.py prefetch
python3 -B research/experiments/20261118T122939Z/commands.py prepare
python3 -B research/experiments/20261118T122939Z/commands.py freeze
python3 -B research/experiments/20261118T122939Z/commands.py units
python3 -B research/experiments/20261118T122939Z/commands.py bind
python3 -B research/experiments/20261118T122939Z/commands.py reserve_0
python3 -B research/experiments/20261118T122939Z/commands.py evaluate
python3 -B research/experiments/20261118T122939Z/commands.py audit
python3 -B research/experiments/20261118T122939Z/commands.py exports
python3 -B research/experiments/20261118T122939Z/commands.py finish_0
python3 -B research/experiments/20261118T122939Z/commands.py research_check
python3 -B research/experiments/20261118T122939Z/commands.py l4h02
python3 -B research/experiments/20261118T122939Z/commands.py fewm
python3 -B research/experiments/20261118T122939Z/commands.py candidate
python3 -B research/experiments/20261118T122939Z/commands.py forward
python3 -B research/experiments/20261118T122939Z/commands.py accounts_check
python3 -B research/experiments/20261118T122939Z/commands.py journal
python3 -B research/experiments/20261118T122939Z/commands.py sources_check
python3 -B research/experiments/20261118T122939Z/commands.py gates
python3 -B research/experiments/20261118T122939Z/commands.py feed
python3 -B research/experiments/20261118T122939Z/commands.py collect
python3 -B research/experiments/20261118T122939Z/commands.py final_checks
```

逐项native退出码、stdout/stderr、数据SHA、spec、成本/折/变体结果与账本同目录保留。

来源：[Binance官方USD-M市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[公共数据作者README](https://github.com/binance/binance-public-data/blob/master/README.md)、[pandas官方EWM](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)。当日已读取官方REST v1/README master/pandas3.1.1文档，有限支持与固定D3比值为明确自定义规则，不是pandas默认无限历史；源版本、规范化可得时间延迟和模型估计限制均保留。
