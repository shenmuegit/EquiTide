# 20261118T042531Z ETH有限EWM趋势跨度研究

本轮预登记并实际执行2个ETH组件和4个被动整银行组合，共6项新配置；每项均先reserve、完整计算一次并finish。历史门槛通过父组合4/4，ETH组件通过0/2、淘汰2/2。严格同时改善收益、整体DD、Sharpe、Calmar的父组合0/4。所有负收益、未达门槛和失败均保留；历史正收益不能称稳定实盘盈利。

经济假设：较快或较慢的有限EWM可能改变趋势响应与价格回撤入场的质量。结果前固定ETH S=[14,16旧只读,18]，并令trend_lookback_days=trend_window_days=S、decay_numerator=S−1、decay_denominator=S+1，交叉旧BTC主入场H=[0.03,0.0325]。代表固定S14/BTCH0.03，无结果后扩网格、换代表或重算已完成窗口。ETH L5/H2%/E0.75%、lag3/K0.75%、风险V6/cap5.625%、M4/R0.0075/VW9及原生资金核算固定；W只是继承的S坐标名，不是H、预算窗口或权重。旧S16与BTC银行只读复用。

完整读取37800条登记事件、18761个ID、460份既往结论和27份附加完整材料。初始16项实际回测缺口为0，原legacy状态和ZIP实际证据保留，未把paper失败观察当缺历史回测。规范研究定义由11479至11485，正式有真实结果定义11272。反复开发、多重选择与重复路径仍在，定义数不等于独立试验数，没有DSR/PBO显著性证明。

完整信号：r=最新闭合价/5个闭合日前价−1；base在r>H时−1、r<−H时+1，否则实际long在r<0.0075保留、实际short在r>−0.0075保留，其余0。有限归一化EWM S14/16/18、beta=(S−1)/(S+1)，最新S个闭合价与其3个闭合日前的同样有限EWM之比−1，严格斜率K0.75%方向过滤，base等于实际持仓或等于趋势方向才接受。闭合日log收益样本波动V6/cap5.625%只过滤新开/反转，等号通过。最近4个成熟1–36小时且available不晚于信号的实际资金费有符号中位数，出流门槛min(0.0002,0.0075×过去9日样本log波动×最新可用实际结算间隔小时/24)，缺记录只阻止新入场，持仓和正常退出保留，最后long-only。BTC固定L29/H3%或3.25%/E0.5%、V10cap2.75%、5日同方向ROC严格大于0.25%，只读复用。完整规则/失败判据/边界/数据SHA在spec/plan。

BTC C3750/N1000、ETH C15000/N4000；原始整银行权重[1,1]，相加完整USDT净值，总初始本金18750，20/80仅为初始资金占比，无自动归一化、缩放、转移、再平衡、父订单或跨银行保证金抵消。

Walk-forward完成：2025-10-19 00:01至2026-11-14 00:01共391日真实复用开发历史、33日预热；无拟合和标签，只用已可得闭合前缀与成熟实际资金费，信号后下一分钟开盘执行。13个完整30日折加1日尾段，近40日8×5日、扩展21日5/5/5/6日；跨折继承实际现金/数量，终点计费平仓，整体DD基于连续完整事件NAV。不是未触碰最终测试集或独立未来。

成本1/2/3倍压力完成：每边手续费5bp、半价差1bp、滑点2bp，冲击0.5×过去20日波动×sqrt(实际订单金额/过去20日quoteADV)，含不利tick/LOT/minnotional、参与率≤0.001、费用后1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流按倍率放大，收入不放大；USDT线性永续不借现货。缺L2/TCA、完整保证金阶梯、tick清算与容量实证，费用及成交风险模型为估计。

|配置|状态|净收益1x / 2x / 3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，ETH S=14|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|ETH组件，ETH S=18|rejected|5.632508 / 5.191694 / 4.751173|4.103613|1.077719|1.079134|7/13|0/0/0（各/8）|
|父组合BTCH=0.03，ETH S=14|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|父组合BTCH=0.0325，ETH S=14|passed|9.181407 / 8.635555 / 8.089884|1.357834|2.313647|5.547208|12/13|6/6/6（各/8）|
|父组合BTCH=0.03，ETH S=18|passed|8.152047 / 7.553666 / 6.955534|3.820753|1.609138|1.695572|11/13|6/6/6（各/8）|
|父组合BTCH=0.0325，ETH S=18|passed|8.044448 / 7.446763 / 6.849327|3.820753|1.585551|1.669738|11/13|6/6/6（各/8）|

敏感性完成：3×2两轴网格含旧对照，保存42个新旧成本场景、588行逐折、336行近40日折、168行扩展折、16464行日NAV、10条相邻边与六面热图。按预设2倍相邻绝对Sharpe变化样本标准差启发式标记3/10条边；6个新定义有6条批内不同全成本路径，其中3条匹配本轮只读旧对照。所有边界、相同路径和失败保留，不把重复路径当独立alpha，不事后延网格。

通过标准：各成本全期/近期正收益、1x至少10/13正月、近期各成本至少6/8正折、扩展各成本至少3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、至少4次平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规且终点flat。实际结论：
ETH_longonly_L5H0p02E0p0075_EWMS14D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS18D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHEWMS14D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEWMS14D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEWMS18D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEWMS18D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。

相对旧ETH EWM跨度16（H2%、VW9固定）父组合，三倍成本完整连续OOS配对比较：
ETH S=14/BTCH=0.03：收益变化0.000000个百分点，整体DD变化0.000000个百分点，Sharpe变化0.000000，Calmar变化0.000000，全成本NAV相同=True。
ETH S=14/BTCH=0.0325：收益变化0.000000个百分点，整体DD变化0.000000个百分点，Sharpe变化0.000000，Calmar变化0.000000，全成本NAV相同=True。
ETH S=18/BTCH=0.03：收益变化-1.240558个百分点，整体DD变化2.462919个百分点，Sharpe变化-0.733812，Calmar变化-3.924274，全成本NAV相同=False。
ETH S=18/BTCH=0.0325：收益变化-1.240558个百分点，整体DD变化2.462919个百分点，Sharpe变化-0.728096，Calmar变化-3.877471，全成本NAV相同=False。

独立审计重算2346个新决策及5865个只读决策，核对现金、数量、成本、实际资金费、风险、全NAV和折指标；已披露引擎与审计器仅扩展跨度允许列表14/18，掩去允许列表后的AST一致，资金核算源码原字节不变；6条新native/12条父曲线及15条旧native/9条旧父曲线均核验，未重跑金融模型。匹配持有3x收益-14.782911%、整体DD18.454767%，现金收益和DD为0。

逐决策差异读取已保存的各自真实路径；持仓及后续阻止状态可能随路径改变，不宣称同状态单步反事实：
ETH S=14 cost=1：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化23、固定H变化0、ungated desired变化0、入场风险前desired变化2、资金费前desired变化2、资金费阻止状态变化0、最终desired变化0；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=True，资金费相同=True，NAV相同=True。
ETH S=14 cost=2：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化23、固定H变化0、ungated desired变化0、入场风险前desired变化2、资金费前desired变化2、资金费阻止状态变化0、最终desired变化0；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=True，资金费相同=True，NAV相同=True。
ETH S=14 cost=3：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化23、固定H变化0、ungated desired变化0、入场风险前desired变化2、资金费前desired变化2、资金费阻止状态变化0、最终desired变化0；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=True，资金费相同=True，NAV相同=True。
ETH S=18 cost=1：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化23、固定H变化0、ungated desired变化1、入场风险前desired变化8、资金费前desired变化8、资金费阻止状态变化0、最终desired变化8；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。
ETH S=18 cost=2：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化23、固定H变化0、ungated desired变化1、入场风险前desired变化8、资金费前desired变化8、资金费阻止状态变化0、最终desired变化8；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。
ETH S=18 cost=3：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化23、固定H变化0、ungated desired变化1、入场风险前desired变化8、资金费前desired变化8、资金费阻止状态变化0、最终desired变化8；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。

增量结论：严格同时改善净收益、整体DD、Sharpe及Calmar的父组合为0/4；全部逐配置配对增量见上表及component_attribution.json。预设代表保持S14/BTC H0.03，无结果后扩网格或重新选择；此局部复用开发历史不构成独立未来或宽参数平台证明。

本轮SMA/single Nov17_16:30→18:30；L4/FEWM18:10→20:10。新查完整实际资金费窗口，预期无新结算；三永续先前已各记08和16且本轮不重复，记录分配SMA0/single0/L4_0/FEWM0，零新日决策与成交。下一轮SMA/single18:30→20:30（20:31闭合），L4/FEWM20:10→22:10（22:11闭合），仍须新查完整实际fundingTime/rate/mark而不预设8小时。首16捕获UTC与原字节SHA保留，新查询另存。SMA完整69日权威仍082021轮输入，分钟包不能当日背景；账户自身尚未跨过下一日决策Nov18_00:01，未来跨日调用原SMA65/对称1%/Float/10bp内核并补真实闭合日。冻结终止日、本金、持仓和规则不变，不采用研究S、不重启、不强平。

既往Nov17_16:00真实BTC资金费率=0.00003565、mark=64090.69218141；ETH费率=-0.00001778、mark=1784.96239374。首次16公共捕获UTC=2026-11-17T22:30:12.515145Z、原字节SHA与首次08捕获UTC=2026-11-17T14:32:50.138522Z均保留。本轮仅在新查询出现未记实际事件时才入账；本次为零，不重复既往16现金流。

原SMA三倍成本累计收益-7.468958%如实保留。原账户为取得行情晚于参考时刻的延迟shadow，不称同步实盘；十策略真实报价模拟仅只读汇总。各原账户180日/六折资格不足，冻结长期收集继续。

保存18份独立公共GET回执，本轮18，复用先前相同URL成功响应0，实际运输失败0；完整金融模型执行1次、完成账户窗口未重跑。所有真实失败原字节、UTC、URL、哈希与恢复证据均保留，详见read_failures.json。

只读监控生成成功=True，研究配置11044，11038旧行完整字典保持。生成失败则恢复上次有效汇总并保存本轮失败证据，不修改账户或删负收益。18个实际配置与36事件已finish，从next_research_state.json续接。

复现顺序（已完成目录禁止重新计算，保留全部stdout/退出码/数据哈希）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261118T042531Z/commands.py freeze
python3 -B research/experiments/20261118T042531Z/commands.py units_retry1
python3 -B research/experiments/20261118T042531Z/commands.py bind
python3 -B research/experiments/20261118T042531Z/commands.py reserve_0
python3 -B research/experiments/20261118T042531Z/commands.py evaluate
python3 -B research/experiments/20261118T042531Z/commands.py audit
python3 -B research/experiments/20261118T042531Z/commands.py exports_retry1
python3 -B research/experiments/20261118T042531Z/commands.py finish_0
python3 -B research/experiments/20261118T042531Z/commands.py research_check
```

只读核验：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261118T042531Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261118T042531Z/forward.py --reproduce
python3 -B checks/strategy_registry.py
python3 -B checks/monitor_snapshot.py
```

来源：[Binance官方USD-M市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[Binance公共数据作者README](https://github.com/binance/binance-public-data/blob/master/README.md)，访问UTC日2026-11-18，REST API v1/README master于访问日。行情和资金费均真实公共数据；历史funding available延迟为规范化假设，费用/价差/滑点/保证金代理为估计。完整spec、report、数据SHA、逐折/变体/成本、账本及实际命令回执同目录保留。

只读监控：11,044行的首次生成稿为5,000,295字节，原5MB门禁实际失败并恢复上次有效汇总，原错误、checker和README归档保留。仅将文件大小预算提高到6MB；重新生成的configs完整SHA与首次失败生成稿一致，11,038个旧行及6个新结果原值保留，完整检查器与原生gzip解压校验通过。策略失败门槛、金融报告、原账户状态及规则均未改变；无网页重部署或重复定时任务。

准备阶段一次prepare分派KeyError和一次跨度允许列表合成检查失败均发生在首个reserve及市场计算之前，原失败回执和源码保留；修正后合成检查通过。首次热图误继承12/16/20标签，已保留原图并按冻结计划修正为14/16/18，全部数值CSV与金融报告SHA不变。监控门禁失败及原有效汇总回退另已完整留档；本轮金融模型及各已完成账户窗口均未重跑。
