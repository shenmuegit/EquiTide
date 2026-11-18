# 20261118T002327Z ETH有限EWM趋势跨度研究

本轮预登记并实际执行2个ETH组件和4个被动整银行组合，共6项新配置；每项均先reserve、完整计算一次并finish。历史门槛通过父组合4/4，ETH组件通过0/2、淘汰2/2。严格同时改善收益、整体DD、Sharpe、Calmar的父组合0/4。所有负收益、未达门槛和失败均保留；历史正收益不能称稳定实盘盈利。

经济假设：较快或较慢的有限EWM可能改变趋势响应与价格回撤入场的质量。结果前固定ETH S=[12,16旧只读,20]，并令trend_lookback_days=trend_window_days=S、decay_numerator=S−1、decay_denominator=S+1，交叉旧BTC主入场H=[0.03,0.0325]。代表固定S12/BTCH0.03，无结果后扩网格、换代表或重算已完成窗口。ETH L5/H2%/E0.75%、lag3/K0.75%、风险V6/cap5.625%、M4/R0.0075/VW9及原生资金核算固定；W只是继承的S坐标名，不是H、预算窗口或权重。旧S16与BTC银行只读复用。

完整读取37724条登记事件、18723个ID、459份既往结论和27份附加完整材料。初始16项实际回测缺口为0，原legacy状态和ZIP实际证据保留，未把paper失败观察当缺历史回测。规范研究定义由11473至11479，正式有真实结果定义11266。反复开发、多重选择与重复路径仍在，定义数不等于独立试验数，没有DSR/PBO显著性证明。

完整信号：r=最新闭合价/5个闭合日前价−1；base在r>H时−1、r<−H时+1，否则实际long在r<0.0075保留、实际short在r>−0.0075保留，其余0。有限归一化EWM S12/16/20、beta=(S−1)/(S+1)，最新S个闭合价与其3个闭合日前的同样有限EWM之比−1，严格斜率K0.75%方向过滤，base等于实际持仓或等于趋势方向才接受。闭合日log收益样本波动V6/cap5.625%只过滤新开/反转，等号通过。最近4个成熟1–36小时且available不晚于信号的实际资金费有符号中位数，出流门槛min(0.0002,0.0075×过去9日样本log波动×最新可用实际结算间隔小时/24)，缺记录只阻止新入场，持仓和正常退出保留，最后long-only。BTC固定L29/H3%或3.25%/E0.5%、V10cap2.75%、5日同方向ROC严格大于0.25%，只读复用。完整规则/失败判据/边界/数据SHA在spec/plan。

BTC C3750/N1000、ETH C15000/N4000；原始整银行权重[1,1]，相加完整USDT净值，总初始本金18750，20/80仅为初始资金占比，无自动归一化、缩放、转移、再平衡、父订单或跨银行保证金抵消。

Walk-forward完成：2025-10-19 00:01至2026-11-14 00:01共391日真实复用开发历史、33日预热；无拟合和标签，只用已可得闭合前缀与成熟实际资金费，信号后下一分钟开盘执行。13个完整30日折加1日尾段，近40日8×5日、扩展21日5/5/5/6日；跨折继承实际现金/数量，终点计费平仓，整体DD基于连续完整事件NAV。不是未触碰最终测试集或独立未来。

成本1/2/3倍压力完成：每边手续费5bp、半价差1bp、滑点2bp，冲击0.5×过去20日波动×sqrt(实际订单金额/过去20日quoteADV)，含不利tick/LOT/minnotional、参与率≤0.001、费用后1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流按倍率放大，收入不放大；USDT线性永续不借现货。缺L2/TCA、完整保证金阶梯、tick清算与容量实证，费用及成交风险模型为估计。

|配置|状态|净收益1x / 2x / 3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，ETH S=12|rejected|5.459243 / 5.180903 / 4.902772|1.528984|1.565567|2.988535|5/13|0/0/0（各/8）|
|ETH组件，ETH S=20|rejected|4.020559 / 3.629832 / 3.239312|3.470060|0.789538|0.870501|6/13|0/0/0（各/8）|
|父组合BTCH=0.03，ETH S=12|passed|8.013435 / 7.545034 / 7.076813|1.357834|2.171703|4.854104|11/13|6/6/6（各/8）|
|父组合BTCH=0.0325，ETH S=12|passed|7.905836 / 7.438130 / 6.970606|1.357834|2.140452|4.781416|11/13|6/6/6（各/8）|
|父组合BTCH=0.03，ETH S=20|passed|6.862488 / 6.304177 / 5.746045|3.918231|1.378277|1.366410|11/13|6/6/6（各/8）|
|父组合BTCH=0.0325，ETH S=20|passed|6.754888 / 6.197273 / 5.639838|3.918231|1.353760|1.341200|11/13|6/6/6（各/8）|

敏感性完成：3×2两轴网格含旧对照，保存42个新旧成本场景、588行逐折、336行近40日折、168行扩展折、16464行日NAV、10条相邻边与六面热图。按预设2倍相邻绝对Sharpe变化样本标准差启发式标记3/10条边；6个新定义有6条批内不同全成本路径，其中0条匹配本轮只读旧对照。所有边界、相同路径和失败保留，不把重复路径当独立alpha，不事后延网格。

通过标准：各成本全期/近期正收益、1x至少10/13正月、近期各成本至少6/8正折、扩展各成本至少3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、至少4次平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规且终点flat。实际结论：
ETH_longonly_L5H0p02E0p0075_EWMS12D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS20D3K0p0075_EntryRiskV6Cap0p05625_M4BudgetVW9R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHEWMS12D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEWMS12D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEWMS20D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p03Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEWMS20D3K0p0075V6Cap0p05625BudgetVW9R0p0075_BTCH0p0325Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。

相对旧ETH EWM跨度16（H2%、VW9固定）父组合，三倍成本完整连续OOS配对比较：
ETH S=12/BTCH=0.03：收益变化-1.119278个百分点，整体DD变化0.000000个百分点，Sharpe变化-0.171247，Calmar变化-0.765742，全成本NAV相同=False。
ETH S=12/BTCH=0.0325：收益变化-1.119278个百分点，整体DD变化0.000000个百分点，Sharpe变化-0.173195，Calmar变化-0.765793，全成本NAV相同=False。
ETH S=20/BTCH=0.03：收益变化-2.450047个百分点，整体DD变化2.560398个百分点，Sharpe变化-0.964673，Calmar变化-4.253436，全成本NAV相同=False。
ETH S=20/BTCH=0.0325：收益变化-2.450047个百分点，整体DD变化2.560398个百分点，Sharpe变化-0.959887，Calmar变化-4.206009，全成本NAV相同=False。

独立审计重算2346个新决策及5865个只读决策，核对现金、数量、成本、实际资金费、风险、全NAV和折指标；6条新native/12条父曲线及15条旧native/9条旧父曲线均核验，未重跑金融模型。匹配持有3x收益-14.782911%、整体DD18.454767%，现金收益和DD为0。

逐决策差异读取已保存的各自真实路径；持仓及后续阻止状态可能随路径改变，不宣称同状态单步反事实：
ETH S=12 cost=1：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化41、固定H变化0、ungated desired变化0、入场风险前desired变化6、资金费前desired变化6、资金费阻止状态变化1、最终desired变化2；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。
ETH S=12 cost=2：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化41、固定H变化0、ungated desired变化0、入场风险前desired变化6、资金费前desired变化6、资金费阻止状态变化1、最终desired变化2；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。
ETH S=12 cost=3：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化41、固定H变化0、ungated desired变化0、入场风险前desired变化6、资金费前desired变化6、资金费阻止状态变化1、最终desired变化2；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。
ETH S=20 cost=1：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化41、固定H变化0、ungated desired变化1、入场风险前desired变化11、资金费前desired变化11、资金费阻止状态变化0、最终desired变化9；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。
ETH S=20 cost=2：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化41、固定H变化0、ungated desired变化1、入场风险前desired变化11、资金费前desired变化11、资金费阻止状态变化0、最终desired变化9；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。
ETH S=20 cost=3：EWM跨度变化391、当前有限EWM变化391、历史有限EWM变化391、斜率变化391、趋势方向变化41、固定H变化0、ungated desired变化1、入场风险前desired变化11、资金费前desired变化11、资金费阻止状态变化0、最终desired变化9；固定风险波动变化0、预算波动变化0、预算上限变化0；成交相同=False，资金费相同=False，NAV相同=False。

增量结论：相对旧S16，同BTC门槛的S12组合三倍成本收益各低约1.119278个百分点，整体DD相同；S20各低约2.450047个百分点、整体DD各高约2.560398个百分点。四组合的Sharpe和Calmar均下降，0/4严格四指标改善；旧16只是这三点网格的局部高点，不能称宽参数平台。本轮未发现增量收益，保留预设S12代表而不事后择优或扩网格，独立未来资格仍不足。

本轮SMA/single Nov17_14:30→16:30；L4/FEWM16:10→18:10。新查完整实际资金费与首次16源一致，单账户用自己的−0.012 BTC持仓逐成本入账，L4/FEWM已各记16而不重复；记录分配SMA0/single6/L4_0/FEWM0，零新日决策与成交。08与16结算三永续现各一次。下一轮SMA/single16:30→18:30（18:31闭合），L4/FEWM18:10→20:10（20:11闭合），须各自新查完整实际fundingTime/rate/mark并按自有现金/数量计账，不预设名义8小时；禁止重复08/16。首16捕获UTC仍Nov17_22:30:12.515145Z、原字节SHA保留，本轮新查询另存，不重标首捕获时间。SMA完整69日权威仍082021轮输入，分钟包不能当日背景；冻结账户自身尚未跨过下一日决策Nov18_00:01，未来跨日调用原SMA65/对称1%/Float/10bp内核并补真实闭合日。原SMA终止2027-03-31及其他终止日不变；不采用研究S、不重启、不强平。

本轮16:00真实BTC资金费率=0.00003565、mark=64090.69218141；ETH费率=-0.00001778、mark=1784.96239374。首次16公共捕获UTC=2026-11-17T22:30:12.515145Z、原字节SHA与首次08捕获UTC=2026-11-17T14:32:50.138522Z均保留。以下为实际原账户逐成本入账，非共享收益或新策略回测：
candidate BTC cost=1，结算ns=1794931200000000000，自有q=-0.012000000000000000，资金费现金流USDT=0.02741799811520719800000000000。
candidate BTC cost=2，结算ns=1794931200000000000，自有q=-0.012000000000000000，资金费现金流USDT=0.02741799811520719800000000000。
candidate BTC cost=3，结算ns=1794931200000000000，自有q=-0.012000000000000000，资金费现金流USDT=0.02741799811520719800000000000。
candidate ETH cost=1，结算ns=1794931200000000000，自有q=0，资金费现金流USDT=-0E-16。
candidate ETH cost=2，结算ns=1794931200000000000，自有q=0，资金费现金流USDT=-0E-16。
candidate ETH cost=3，结算ns=1794931200000000000，自有q=0，资金费现金流USDT=-0E-16。

原SMA三倍成本累计收益-7.468958%如实保留。原账户为取得行情晚于参考时刻的延迟shadow，不称同步实盘；十策略真实报价模拟仅只读汇总。各原账户180日/六折资格不足，冻结长期收集继续。

保存18份独立公共GET回执，本轮18，复用先前相同URL成功响应0，实际运输失败0；完整金融模型执行1次、完成账户窗口未重跑。所有真实失败原字节、UTC、URL、哈希与恢复证据均保留，详见read_failures.json。

只读监控生成成功=True，研究配置11038，11032旧行完整字典保持。生成失败则恢复上次有效汇总并保存本轮失败证据，不修改账户或删负收益。18个实际配置与36事件已finish，从next_research_state.json续接。

复现顺序（已完成目录禁止重新计算，保留全部stdout/退出码/数据哈希）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261118T002327Z/commands.py freeze
python3 -B research/experiments/20261118T002327Z/commands.py units
python3 -B research/experiments/20261118T002327Z/commands.py bind
python3 -B research/experiments/20261118T002327Z/commands.py reserve_0
python3 -B research/experiments/20261118T002327Z/commands.py evaluate
python3 -B research/experiments/20261118T002327Z/commands.py audit
python3 -B research/experiments/20261118T002327Z/commands.py exports
python3 -B research/experiments/20261118T002327Z/commands.py finish_0
python3 -B research/experiments/20261118T002327Z/commands.py research_check
```

只读核验：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261118T002327Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261118T002327Z/forward.py --reproduce
python3 -B checks/strategy_registry.py
python3 -B checks/monitor_snapshot.py
```

来源：[Binance官方USD-M市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[Binance公共数据作者README](https://github.com/binance/binance-public-data/blob/master/README.md)，访问UTC日2026-11-18，REST API v1/README master于访问日。行情和资金费均真实公共数据；历史funding available延迟为规范化假设，费用/价差/滑点/保证金代理为估计。完整spec、report、数据SHA、逐折/变体/成本、账本及实际命令回执同目录保留。

只读监控修复：本轮默认gzip为5,000,071字节，原5,000,000字节门禁实际失败，已先恢复上次有效汇总并保存原错误与旧源码。随后仅把标准gzip的deflate内存参数8改为9，生成和检查共用同一函数；压缩级别9、5MB预算及全部解压JSON字节不变。完整28,774,093字节的SHA保持，新gzip为4,997,629字节，11,032旧行完整字典与6个新结果均保留；原检查器与原生DecompressionStream验证通过。另有补充核验脚本误把st_size字段当函数的真实TypeError，触发回退后已修正重验，所有原失败回执保留。金融报告、策略与原账户窗口未重跑，无网页重部署或重复定时任务。
