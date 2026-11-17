# 20261117T202125Z ETH资金费预算波动率窗口研究

本轮预登记并实际执行2个ETH组件和4个被动整银行组合，共6项新配置；每项均先reserve、完整计算一次并finish。历史门槛通过父组合4/4，未达门槛ETH组件2/2。严格同时改善收益、整体DD、Sharpe、Calmar的父组合0/4。所有负收益、未达门槛和失败均保留；历史正收益不能称稳定实盘盈利。

经济假设：较长的预算波动率窗口可能改变风险和资金费预算的适应速度。结果前固定VW=[9只读,10,12]，固定R=0.0075、M4及入场风险V6/cap0.05625，交叉旧BTC主入场H=[0.03,0.0325]；代表固定VW10/BTCH0.03，无结果后扩网格、换代表或重算已完成窗口。入场风险V6、预算VW9/10/12和执行冲击V20相互独立，VW不是权重。旧VW9及BTC银行已有真实结果，本轮只读复用，不精确重跑。

完整读取37612条登记事件、18667个ID、457份既往结论和27份附加完整材料。初始16项实际回测缺口为0，原legacy状态和ZIP实际证据保留，未把paper失败观察当策略缺测。规范研究定义由11461至11467，正式result_available研究定义11254。反复开发、多重选择与重复路径仍在，定义数不等于独立试验数，没有DSR/PBO显著性证明。

ETH固定L5/H2%/E0.75%、有限归一化EWM16(beta15/17)/lag3/严格斜率K0.75%，闭合日log收益样本波动V6/cap5.625%仅过滤新开或反转，等号通过。最近4个实际资金费有符号中位数须成熟1–36小时且available不晚于信号，出流门槛min(0.0002,0.0075×过去VW日样本log波动×最新可用实际结算间隔小时/24)，缺记录只阻止新入场，持仓和正常退出保留，最后long-only。BTC旧银行固定L29/H3%或3.25%/E0.5%、V10cap2.75%、5日同方向ROC严格大于0.25%，只读复用。完整规则、失败判据、边界、数据SHA均在spec/plan。

BTC C3750/N1000、ETH C15000/N4000，父层原始整银行权重[1,1]，相加各自完整USDT净值，总初始本金18750；20/80仅为初始资金占比，无自动归一化、账本缩放、转移、再平衡、父层订单或跨银行保证金抵消。

Walk-forward完成：2025-10-19 00:01至2026-11-14 00:01共391日真实复用开发历史、33日预热；无拟合和标签，只用可得闭合前缀、成熟实际资金费，信号后下一分钟开盘执行。13个完整30日折加1日尾段，近40日8×5日、扩展21日5/5/5/6日；跨折继承实际现金与数量，终点计费平仓，整体DD基于连续完整事件NAV。该历史已反复开发，不是未触碰最终测试集或独立未来。

成本1/2/3倍压力完成：每边手续费5bp、半价差1bp、滑点2bp，冲击0.5×过去20日波动×sqrt(实际订单金额/过去20日quoteADV)，含不利tick/LOT/minnotional、参与率≤0.001、费用后1倍抵押和小时不利价1%维持保证金代理。实际永续资金费出流按倍率放大，收入不放大；USDT线性永续不借现货。缺L2/TCA、完整保证金阶梯、tick清算和容量实证，费用及成交风险模型为估计。

|配置|状态|净收益1x / 2x / 3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，VW=10|rejected|7.053708 / 6.677684 / 6.301870|1.528984|1.860974|3.839649|7/13|0/0/0（各/8）|
|ETH组件，VW=12|rejected|6.715796 / 6.335002 / 5.954418|1.528984|1.738908|3.628353|7/13|0/0/0（各/8）|
|父组合BTCH=0.03，VW=10|passed|9.289007 / 8.742459 / 8.196091|1.357834|2.342950|5.619846|12/13|6/6/6（各/8）|
|父组合BTCH=0.0325，VW=10|passed|9.181407 / 8.635555 / 8.089884|1.357834|2.313647|5.547208|12/13|6/6/6（各/8）|
|父组合BTCH=0.03，VW=12|passed|9.018678 / 8.468313 / 7.918129|1.357834|2.244814|5.429731|12/13|6/6/6（各/8）|
|父组合BTCH=0.0325，VW=12|passed|8.911078 / 8.361410 / 7.811922|1.357834|2.215712|5.357081|12/13|6/6/6（各/8）|

敏感性完成：3×2两轴网格含旧对照，保存42个新旧成本场景、588行逐折、336行近40日折、168行扩展折、16464行日NAV、10条相邻边和六面热图；预设2倍相邻绝对Sharpe变化样本标准差启发式标记3/10条边。6个新定义有6条批内不同全成本路径，其中3条匹配本轮只读旧对照。所有边界、相同路径和失败保留，不把重复路径当独立alpha，不事后延网格。

通过标准包括各成本全期/近期正收益、1x至少10/13正月、近期各成本至少6/8正折、扩展各成本至少3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、至少4次平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规及终点flat。实际配置结论：
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4_BudgetVW10R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p05625_M4_BudgetVW12R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHEntryRiskV6Cap0p05625BudgetVW10R0p0075_BTCH0p03Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEntryRiskV6Cap0p05625BudgetVW10R0p0075_BTCH0p0325Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEntryRiskV6Cap0p05625BudgetVW12R0p0075_BTCH0p03Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。
parent_ETHEntryRiskV6Cap0p05625BudgetVW12R0p0075_BTCH0p0325Confirm5Min0p0025_391d：达到历史门槛，仍待独立未来。

相对旧VW9父组合的配对比较（3倍成本，完整OOS整体指标）：
VW=10/BTCH=0.03：净收益变化0.000000个百分点，整体DD变化0.000000个百分点，Sharpe变化0.000000，Calmar变化0.000000，全成本净值路径相同=True。
VW=10/BTCH=0.0325：净收益变化0.000000个百分点，整体DD变化0.000000个百分点，Sharpe变化0.000000，Calmar变化0.000000，全成本净值路径相同=True。
VW=12/BTCH=0.03：净收益变化-0.277962个百分点，整体DD变化0.000000个百分点，Sharpe变化-0.098136，Calmar变化-0.190115，全成本净值路径相同=False。
VW=12/BTCH=0.0325：净收益变化-0.277962个百分点，整体DD变化0.000000个百分点，Sharpe变化-0.097935，Calmar变化-0.190128，全成本净值路径相同=False。

独立审计重算2346个新决策、5865个只读决策及现金/数量/成本/实际资金费/风险、全NAV和折指标，核验6条新native/12条父曲线及15条旧native/9条旧父曲线，未重跑金融模型。匹配持有3x收益-14.782911%、整体DD18.454767%，现金收益和DD为0。

以下逐决策差异直接读取已保存的各自真实路径；预算前desired和阻止状态可能随持仓路径改变，不宣称同一状态下的单步反事实：
VW=10 cost=1：预算窗口变化391，预算样本波动变化391，预算上限变化391，入场观测波动变化0，资金费过滤阻止状态变化0，预算前desired变化0，最终desired变化0；成交相同=True，资金费相同=True，NAV相同=True。
VW=10 cost=2：预算窗口变化391，预算样本波动变化391，预算上限变化391，入场观测波动变化0，资金费过滤阻止状态变化0，预算前desired变化0，最终desired变化0；成交相同=True，资金费相同=True，NAV相同=True。
VW=10 cost=3：预算窗口变化391，预算样本波动变化391，预算上限变化391，入场观测波动变化0，资金费过滤阻止状态变化0，预算前desired变化0，最终desired变化0；成交相同=True，资金费相同=True，NAV相同=True。
VW=12 cost=1：预算窗口变化391，预算样本波动变化391，预算上限变化391，入场观测波动变化0，资金费过滤阻止状态变化1，预算前desired变化0，最终desired变化1；成交相同=False，资金费相同=False，NAV相同=False。
VW=12 cost=2：预算窗口变化391，预算样本波动变化391，预算上限变化391，入场观测波动变化0，资金费过滤阻止状态变化1，预算前desired变化0，最终desired变化1；成交相同=False，资金费相同=False，NAV相同=False。
VW=12 cost=3：预算窗口变化391，预算样本波动变化391，预算上限变化391，入场观测波动变化0，资金费过滤阻止状态变化1，预算前desired变化0，最终desired变化1；成交相同=False，资金费相同=False，NAV相同=False。

增量结论：VW10的ETH组件及两父组合在所有成本下与只读VW9的成交、资金费和完整NAV一致；VW12两父组合三倍成本收益各低约0.277962个百分点，整体DD相同且Sharpe/Calmar下降。四父达到历史门槛不等于本轮改进；0/4严格四指标改善，未获得新的独立alpha。保留预设VW10代表，不按结果另选最优；下一批应先查重并事前冻结不同的经济假设，原冻结账户不采用本轮研究规则。

本轮SMA/single Nov17_10:30→12:30；L4/FEWM12:10→14:10。新查完整实际资金费列表为空，资金费分配0/0/0/0，零新日决策与成交；三永续已各记Nov17_08一次，禁止重复。原现金/数量/desired/累计费用和完整NAV前缀按各自账户续接。下一轮SMA/single12:30→14:30（14:31闭合），L4/FEWM14:10→16:10（16:11闭合），后者可能包含新的实际结算，须先查完整实际记录后再按自有持仓计账，均须新查自己的完整实际fundingTime/rate/mark，不预设名义8小时。全部Nov17午夜及00:01日决策仍各一次。SMA完整69日权威仍082021轮输入，分钟包不能当日背景；未来跨日调用原SMA65/对称1%/Float/10bp日内核并补真实闭合日。下一日决策均Nov18_00:01，各自终止日保持，原SMA仍2027-03-31；不采用研究VW、不重启、不强平。

本轮完整实际资金费查询为空，四账户没有新资金费现金流；三永续的08结算各一次。首次08公共捕获UTC=2026-11-17T14:32:50.138522Z和原字节SHA保持，本轮另有新完整窗口查询UTC=2026-11-17T20:28:42.175626Z。原SMA3x累计收益-7.468958%如实保留。原账户为取得行情晚于参考时刻的延迟shadow，不称同步实盘；十策略真实报价模拟仅只读汇总。各原账户180日/六折资格仍不足，冻结长期收集继续。

保存18份独立公共GET回执，本轮18，按相同URL复用先前成功响应0，实际运输失败0；真实失败字节/UTC/URL/哈希及恢复全部保留。完整金融模型执行1次、完成账户窗口未重跑。环境、来源与检查实际失败见read_failures.json。

只读网页监控生成成功=True，研究配置11026，11020旧行逐项保持。若生成失败则恢复上次有效快照并保存本轮证据，不修改冻结账户或删负收益。18个实际配置及36事件已finish；从next_research_state.json续接。

复现顺序（仅记录，已完成目录禁止重新计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261117T202125Z/commands.py freeze
python3 -B research/experiments/20261117T202125Z/commands.py units
python3 -B research/experiments/20261117T202125Z/commands.py bind
python3 -B research/experiments/20261117T202125Z/commands.py reserve_0
python3 -B research/experiments/20261117T202125Z/commands.py evaluate
python3 -B research/experiments/20261117T202125Z/commands.py audit
python3 -B research/experiments/20261117T202125Z/commands.py exports
python3 -B research/experiments/20261117T202125Z/commands.py finish_0
python3 -B research/experiments/20261117T202125Z/commands.py research_check
```

只读核验：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261117T202125Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261117T202125Z/forward.py --reproduce
python3 -B checks/strategy_registry.py
python3 -B checks/monitor_snapshot.py
```

来源：[Binance官方USD-M市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[Binance公共数据作者README](https://github.com/binance/binance-public-data/blob/master/README.md)，访问UTC日2026-11-17。行情与资金费均为真实公共数据；历史funding available延迟是规范化假设，费用/价差/滑点/保证金代理是估计。spec、report、数据SHA、逐折/变体/成本、完整账本及真实命令回执同目录保存。
