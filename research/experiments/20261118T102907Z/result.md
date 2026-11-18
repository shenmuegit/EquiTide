# 20261118T102907Z ETH有限EWM斜率滞后期研究

预先固定D=[1,3旧只读,5]与旧BTC主入场H=[0.03,0.0325]；代表D1/BTC H0.03。共6项新配置（2个ETH组件、4个整银行组合）均先reserve、实际计算一次并finish。历史门槛通过组合4/4，ETH组件通过0/2，淘汰2/2。严格同时改善净收益、整体DD、Sharpe及Calmar的组合0/4。全部负收益折、未通过和实际失败保留；历史正收益不能称稳定实盘盈利。

完整读取37932条登记事件、18827个ID、462份既往结论和27份附加完整材料。初始16项实际回测缺口为0，legacy状态及原ZIP真实证据保留；没有把paper失败观察当缺历史回测。规范研究定义从11491至11497，正式有结果定义11284。多重选择、旧历史复用和路径别名限制均保留，定义数不是独立试验数，无DSR/PBO显著性证明。

经济假设：改变趋势斜率测量期限D可能改变入场时机。有限归一化EWM跨度固定16、beta=15/17；当前最新16个已闭合价格的EWM与D个闭合日前的同样有限EWM之比减1，以严格绝对门槛0.75%判断方向，不除以D、不日均化。D1/D5相对旧D3是实际参数变化，完整引擎与资金核算源码原字节保持。其余ETH L5/H2%/E0.75%、风险V6/cap5.625%、M4/R0.0075/预算VW9与BTC旧规则均固定。

完整信号：ETH longonly L5/H.02/E.0075. Fast r=lastcompletedclose/close5completeddaysearlier-1;contrarianbase=-1 if r>.02,+1 if r<-.02,else actual if(actual==1 and r<.0075)or(actual==-1 and r>-.0075),else0. Finite normalized EWM fixedspan16,beta15/17,latest16completedcloses. Slope=currentfinitelevel/samefinitelevelDcompleteddaysearlier-1,D[1,3readonly,5];strictabsoluteK.0075 over Ddays,not dividedbyD or dailyized. Direction=+1 if slope>.0075,-1 if slope<-.0075,else0;acceptbase ifbase==actual or base==direction,else0. Entryrisk samplelogvol V6/cap.05625 onlynew/reversed,equalitypasses. LatestM4actual signedfundingmedian mature1to36hinclusive/available<=signal;outgoingcost<=min(.0002,.0075*past9completedunbiasedsamplelogvol*latesteligibleactualintervalhours/24);equalitypasses,missingblocksnewentryonly;heldq/normalexitunchanged;finallymax(desired,0). BTCreadonly L29 mainH[.03,.0325],exitE.005,V10cap.0275,recent5directionalROCstrictly>.0025,newentrygatesonly,retainactualq. No fit/labels/futurevalues. FixedS16/fastL5/H.02,lagD,entryriskV6,carryVW9,impactV20distinct.

原始整银行权重[1,1]，BTC C3750/N1000、ETH C15000/N4000，相加完整USDT净值，总初始18750；20/80仅是初始银行资金占比，无归一化、缩放、转移、再平衡、父订单或跨银行保证金抵消。

Walk-forward：2025-10-19 00:01至2026-11-14 00:01，共391日真实复用开发历史、33日上下文。无拟合或标签，只用已可得闭合前缀和成熟资金费，下一分钟开盘执行；13个完整30日折加1日尾段，近40日8×5日及扩展21日5/5/5/6日。跨折继承现金/数量，终点计费平仓，整体DD用完整连续事件NAV计算；这些反复使用的日期不是未触碰最终测试集或独立未来。

成本1/2/3倍压力：每边手续费5bp、半价差1bp、滑点2bp，冲击0.5×过去20日波动×sqrt(实际订单额/过去20日quoteADV)，含不利tick/LOT/minnotional、参与率≤0.001、费用后1倍抵押及小时不利价1%维持保证金代理。真实永续资金费出流按倍率放大、收入不放大；USDT线性永续不借现货。缺L2/TCA、完整阶梯、tick清算和容量实证，成本/成交风险模型为估计。

|配置|状态|净收益1x / 2x / 3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，D=1|rejected|0.000000 / 0.000000 / 0.000000|0.000000|未定义|未定义|0/13|0/0/0（各/8）|
|ETH组件，D=5|rejected|7.064394 / 6.468689 / 5.873014|4.905622|1.134798|1.115453|8/13|0/0/0（各/8）|
|组合BTCH=0.03，D=1|passed|3.646041 / 3.400311 / 3.154595|1.215308|1.540471|2.420599|10/13|6/6/6（各/8）|
|组合BTCH=0.0325，D=1|passed|3.538441 / 3.293408 / 3.048388|1.215308|1.490320|2.339185|10/13|6/6/6（各/8）|
|组合BTCH=0.03，D=5|passed|9.297556 / 8.575263 / 7.853007|4.669697|1.622367|1.565880|11/13|6/6/6（各/8）|
|组合BTCH=0.0325，D=5|passed|9.189956 / 8.468359 / 7.746800|4.669697|1.601413|1.544754|11/13|6/6/6（各/8）|

双轴为预设D1/3/5的两日间隔与BTC H0.03/0.0325；D2/D4既有结果保留在前轮，不当作本轮新计算。双轴敏感性保存42个新旧成本场景、588逐折行、336近40日折、168扩展折、16464日NAV、10条相邻边及六面热图。按预设启发式标记2/10条相邻边；6个新定义含6条批内不同全成本路径，0条匹配当前旧对照。所有平台、边界和相同路径都保留，不把别名当独立alpha，不看结果后扩网格或换代表。

失败判据固定：各成本全期/近期正收益、1x至少10/13正月、各成本近期至少6/8正折、扩展至少3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、至少4次平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规且终点flat。
ETH_longonly_L5H0p02E0p0075_EWMS16D1K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：positive_all_costs；ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_positive3_gte60pct；local_recent6of8_allcost_gte60pct；four_underlying_native_closes1；gross_plus_funding_to_cost1_gte2_5；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D5K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHEWMS16D1K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHEWMS16D1K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHEWMS16D5K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。
parent_ETHEWMS16D5K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：通过历史门槛，仍待独立未来。

相对同BTC旧ETH S16/D3的三倍成本配对增量：
D=1/BTC H=0.03：收益变化-5.041496个百分点，整体DD变化-0.142526个百分点，Sharpe变化-0.802479，Calmar变化-3.199247，全成本NAV相同=False。
D=1/BTC H=0.0325：收益变化-5.041496个百分点，整体DD变化-0.142526个百分点，Sharpe变化-0.823327，Calmar变化-3.208024，全成本NAV相同=False。
D=5/BTC H=0.03：收益变化-0.343085个百分点，整体DD变化3.311863个百分点，Sharpe变化-0.720583，Calmar变化-4.053966，全成本NAV相同=False。
D=5/BTC H=0.0325：收益变化-0.343085个百分点，整体DD变化3.311863个百分点，Sharpe变化-0.712234，Calmar变化-4.002454，全成本NAV相同=False。

独立审计核验2346个新决策、5865个只读决策及全部现金/数量、成本、真实资金费、风险、NAV与折指标；完整金融模型执行一次，无已完成模型或账户窗口重跑。匹配持有3x收益-14.782911%、整体DD18.454767%，现金收益/回撤为0。
D=1 cost=1：滞后期变化391，固定跨度变化0，当前EWM变化0、参考EWM变化391、斜率变化391、趋势方向变化151、最终desired变化20；固定H变化0、风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False、资金费相同=False、NAV相同=False。
D=1 cost=2：滞后期变化391，固定跨度变化0，当前EWM变化0、参考EWM变化391、斜率变化391、趋势方向变化151、最终desired变化20；固定H变化0、风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False、资金费相同=False、NAV相同=False。
D=1 cost=3：滞后期变化391，固定跨度变化0，当前EWM变化0、参考EWM变化391、斜率变化391、趋势方向变化151、最终desired变化20；固定H变化0、风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False、资金费相同=False、NAV相同=False。
D=5 cost=1：滞后期变化391，固定跨度变化0，当前EWM变化0、参考EWM变化391、斜率变化391、趋势方向变化64、最终desired变化22；固定H变化0、风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False、资金费相同=False、NAV相同=False。
D=5 cost=2：滞后期变化391，固定跨度变化0，当前EWM变化0、参考EWM变化391、斜率变化391、趋势方向变化64、最终desired变化22；固定H变化0、风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False、资金费相同=False、NAV相同=False。
D=5 cost=3：滞后期变化391，固定跨度变化0，当前EWM变化0、参考EWM变化391、斜率变化391、趋势方向变化64、最终desired变化22；固定H变化0、风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False、资金费相同=False、NAV相同=False。

D1零波动/零回撤下Sharpe及Calmar未定义，保留JSON null而非填零。D1实际391个日决策全部desired=0、ETH全程15000USDT现金、零成交/费用/资金费，三倍成本收益和回撤均为0；对应组合正收益全部由既有BTC银行带动，独立逐段状态和父NAV相加核验见idle_ETH_attribution.json。保留真实完成的零收益结果为rejected，不把闲置ETH资金剔除或归一化，也不把组合通过当作新ETH alpha。

以上为各自已保存路径的逐决策差异；持仓与阻止状态可能随路径变化，不当作同状态单步反事实。
严格同时改善四指标为0/4；全部配对增量保留，预设代表D1/H0.03不变，独立未来资格不足。

本轮SMA/single Nov17_20:30→22:30仅闭合分钟mark；L4/FEWM22:10→Nov18_00:10完成原Nov18_00:01日决策，按各自原冻结背景拼成Nov17整日1440条分钟及精确收盘/成交额。新查实际00资金费，入账记录分配{'SMA': 0, 'candidate': 0, 'l4h02': 6, 'fewm': 6}，原日事件{'SMA': 0, 'candidate': 0, 'l4h02': 1, 'fewm': 1}，原实际成交{'SMA': 0, 'candidate': 0, 'l4h02': 0, 'fewm': 0}，所有完整NAV前缀与18账本独立核验。旧Nov17_08/16和Nov18_00首来源UTC/SHA保持，各账户只记自身窗口一次。下一轮SMA/single22:30→Nov18_00:30将跨原00:01；SMA须实际补足70日现货数据并保持69日前缀，调用原SMA65/对称1%/Float/10bp内核；single用自身原日背景及冻结信号，新查完整真实资金费并只记自己的00结算。下一L4/FEWM00:10→02:10无日决策，不重复已记00，下一日决策Nov19_00:01。不得把本轮SMA分钟包当70日权威，不提前计算未来成交或采用新研究D。各原终止日、本金、持仓和规则保持，不重启、不强平。

原SMA三倍成本累计收益-7.468958%如实保留；原账户是取得数据晚于参考时刻的延迟shadow，与十策略真实报价模拟分开。各原账户180日/六折资格不足，不取消其冻结长期计划。
保留18份独立公共GET回执，本轮18、复用旧成功响应0、真实运输失败0；完整原始响应/UTC/URL/SHA与所有真实错误保留。
只读监控生成成功=True，研究配置11056，11050旧行完整字典保持。监控失败按既定规则保留上次有效汇总，不删负收益或修改账户。

实际阶段命令（已完成目录禁止重新计算；完整退出码/stdout/数据SHA同目录保留）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261118T102907Z/commands.py prepare
python3 -B research/experiments/20261118T102907Z/commands.py freeze
python3 -B research/experiments/20261118T102907Z/commands.py units
python3 -B research/experiments/20261118T102907Z/commands.py bind
python3 -B research/experiments/20261118T102907Z/commands.py reserve_0
python3 -B research/experiments/20261118T102907Z/commands.py evaluate
python3 -B research/experiments/20261118T102907Z/commands.py audit
python3 -B research/experiments/20261118T102907Z/commands.py exports
python3 -B research/experiments/20261118T102907Z/commands.py finish_0
python3 -B research/experiments/20261118T102907Z/commands.py research_check
```

只读核验：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261118T102907Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261118T102907Z/forward.py --reproduce
python3 -B checks/strategy_registry.py
python3 -B checks/monitor_snapshot.py
```

来源：[Binance官方USD-M市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[公共数据作者README](https://github.com/binance/binance-public-data/blob/master/README.md)、[pandas官方EWM](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)。访问UTC日2026-11-18，REST v1/README master/pandas3.1.1文档；有限16日支持和滞后D比值是本策略明确规则，不声称为pandas默认无限历史。历史funding available延迟与成本/风险代理均为规范化估计。
