# 20261117T142055Z ETH入场风险上限研究

本轮预登记并实际执行2个ETH组件和4个被动整银行组合，共6项新配置；每项均先reserve、完整计算一次并finish。历史门槛通过父组合4/4，未达门槛ETH组件2/2。严格同时改善收益、整体DD、Sharpe、Calmar的父组合0/4。所有负收益和未达门槛结果保留。历史正收益不代表稳定实盘盈利。

经济假设：更紧或更松的入场波动上限可能改变不利入场及交易成本。结果前固定ETH cap=[0.0525,0.05625只读,0.06]、样本窗口V6，交叉旧BTC主入场H=[0.03,0.0325]；代表固定cap0.0525/BTCH0.03，无结果后扩网格、换代表或重算已完成窗口。

完整读取37444条登记事件、18583个ID、454份既往结论和27份附加完整材料。初始16项实际回测缺口为0，原legacy状态和ZIP实际证据保留，未把paper失败观察当策略缺测。规范研究定义由11443至11449，正式result_available研究定义11236。定义数不等于独立试验数，重复开发和多重选择偏差仍在，没有DSR/PBO显著性证明。

ETH完整固定规则为L5/H2%/E0.75%、有限归一化EWM16(beta15/17)/lag3/严格斜率K0.75%，固定V6的闭合日log收益样本波动仅在sigma>cap时阻止新开或反转，等号通过，实际持仓与正常退出保留。最近4次实际资金费有符号中位数须成熟1–36小时且available不晚于信号，出流门槛min(0.0002,0.0075×过去8日样本log波动×最新可用实际结算间隔小时/24)，最后long-only。BTC旧银行为L29/H3%或3.25%/E0.5%、V10cap2.75%、5日同方向ROC严格大于0.25%，只读复用。spec/plan保存完整规则、时间、数据SHA及失败判据。

资金与权重：BTC C3750/N1000、ETH C15000/N4000，父层原始整银行权重[1,1]，相加各自完整USDT净值，总初始本金18750；20/80仅是初始资金占比。没有自动归一化、账本缩放、转移、再平衡、父层订单或跨银行保证金抵消。

Walk-forward完成：2025-10-19 00:01至2026-11-14 00:01共391日真实复用开发历史，33日预热；无拟合与标签，信号只用可得闭合前缀和成熟实际资金费，下一分钟开盘执行。13个完整30日折加1日尾段，近40日8×5日、扩展21日5/5/5/6日；跨折继承实际现金与数量，只在完整终点计费平仓。整体DD基于连续完整事件NAV。该历史已反复开发，不能称未触碰最终测试集或独立未来。

成本1/2/3倍压力完成：每边手续费5bp、半价差1bp、滑点2bp，冲击0.5×过去20日波动×sqrt(实际订单金额/过去20日quoteADV)，不利tick/LOT/minnotional、参与率≤0.001、费用后1倍抵押及小时不利价1%维持保证金代理。实际永续资金费出流按倍率放大，收入不放大；USDT线性永续无现货借币。缺真实L2/TCA、完整保证金阶梯、tick清算和容量实证，成本模型为估计。

|配置|状态|净收益1x / 2x / 3x %|整体DD3 %|Sharpe3|Calmar3|正30日折1x|近5日正折1/2/3|
|---|---|---|---|---|---|---|---|
|ETH组件，cap=0.0525|rejected|6.842224 / 6.541435 / 6.240856|1.528984|1.875200|3.802547|6/13|0/0/0（各/8）|
|ETH组件，cap=0.06|rejected|6.842224 / 6.541435 / 6.240856|1.528984|1.875200|3.802547|6/13|0/0/0（各/8）|
|父组合BTCH=0.03，cap=0.0525|passed|9.119820 / 8.633459 / 8.147280|1.357834|2.365156|5.586463|12/13|6/6/6（各/8）|
|父组合BTCH=0.0325，cap=0.0525|passed|9.012220 / 8.526556 / 8.041073|1.357834|2.335453|5.513824|12/13|6/6/6（各/8）|
|父组合BTCH=0.03，cap=0.06|passed|9.119820 / 8.633459 / 8.147280|1.357834|2.365156|5.586463|12/13|6/6/6（各/8）|
|父组合BTCH=0.0325，cap=0.06|passed|9.012220 / 8.526556 / 8.041073|1.357834|2.335453|5.513824|12/13|6/6/6（各/8）|

敏感性完成：3×2两轴网格含旧对照；保存42个新旧成本场景、588行逐折、336行近40日折、168行扩展折、16464行日NAV、10条相邻边及六面热图。预设2倍相邻绝对Sharpe变化样本标准差启发式标记1/10条边。新配置共有3条批内不同全成本路径，其中3条匹配只读旧对照。所有边界、相同路径和未通过项保留，不把重复净值当新增独立alpha。

逐配置通过/失败条件包括：各成本全期和近期正收益、1x至少10/13正月、近期各成本至少6/8正折、扩展各成本至少3/4正折、DD3≤25%、局部正收益和严格近期比例≥60%、至少4次平仓、1x(毛价差收益+资金费)/执行费用≥2.5、无拒单/抵押/保证金代理违规、终点flat。以下为实际未通过条件：
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p0525_M4_BudgetVW8R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
ETH_longonly_L5H0p02E0p0075_EWMS16D3K0p0075_EntryRiskV6Cap0p06_M4_BudgetVW8R0p0075_391d：ten_of_thirteen_positive_complete30d_1x_folds；recent40_positive_all_costs；recent40_six_of_eight_positive5d_all_costs；local_recent6of8_allcost_gte60pct；extension21_positive_all_costs；extension21_three_of_four_positive_folds_all_costs
parent_ETHEntryRiskV6Cap0p0525BudgetVW8R0p0075_BTCH0p03Confirm5Min0p0025_391d：全部通过历史门槛，继续待独立未来。
parent_ETHEntryRiskV6Cap0p0525BudgetVW8R0p0075_BTCH0p0325Confirm5Min0p0025_391d：全部通过历史门槛，继续待独立未来。
parent_ETHEntryRiskV6Cap0p06BudgetVW8R0p0075_BTCH0p03Confirm5Min0p0025_391d：全部通过历史门槛，继续待独立未来。
parent_ETHEntryRiskV6Cap0p06BudgetVW8R0p0075_BTCH0p0325Confirm5Min0p0025_391d：全部通过历史门槛，继续待独立未来。

独立审计重算2346个新决策、5865个只读决策及原生现金/数量/成本/实际资金费/风险、完整NAV和折指标，核验6条新native、12条父曲线及15条旧native/9条旧父曲线，未重跑金融模型。同期同资金/名义金额持有3x收益-14.782911%、整体DD18.454767%，现金收益和DD为0。

逐决策实际差异（每行一个ETH组件成本场景）：
cap=0.0525 cost=1：上限变化391，观测波动数值变化0，入场风险阻止状态变化1，实际desired变化0，成交相同=True，资金费相同=True，NAV相同=True。
cap=0.0525 cost=2：上限变化391，观测波动数值变化0，入场风险阻止状态变化1，实际desired变化0，成交相同=True，资金费相同=True，NAV相同=True。
cap=0.0525 cost=3：上限变化391，观测波动数值变化0，入场风险阻止状态变化1，实际desired变化0，成交相同=True，资金费相同=True，NAV相同=True。
cap=0.06 cost=1：上限变化391，观测波动数值变化0，入场风险阻止状态变化1，实际desired变化0，成交相同=True，资金费相同=True，NAV相同=True。
cap=0.06 cost=2：上限变化391，观测波动数值变化0，入场风险阻止状态变化1，实际desired变化0，成交相同=True，资金费相同=True，NAV相同=True。
cap=0.06 cost=3：上限变化391，观测波动数值变化0，入场风险阻止状态变化1，实际desired变化0，成交相同=True，资金费相同=True，NAV相同=True。

本轮SMA/single Nov17_04:30→06:30；L4/FEWM06:10→08:10。新查真实08结算按各自账本入账，资金费记录分配0/0/6/6；各自结算前q、mark、rate和成本倍率独立核对，零新日决策与成交。下一轮SMA/single06:30→08:30（08:31闭合），single必须新查完整实际结算并计入自己的08资金费；L4/FEWM08:10→10:10（10:11闭合）已记08一次，禁止重复，仍须新查各自完整窗口。所有Nov17午夜及00:01日决策保持已记一次。SMA完整69日权威仍082021轮输入，当前分钟包不能当日背景；未来跨日执行原SMA65/对称1%/Float/10bp日内核并补真实闭合日。四账户下一日决策均Nov18_00:01，各自终止日保持，原SMA仍2027-03-31。原账户不采用研究cap、不重启、不强平。

新08资金费原始来源首次捕获UTC=2026-11-17T14:32:50.138522Z；本轮共12条资产×成本现金流独立核对并保存，BTC负费率使本轮两个BTC空头支付，ETH零仓位现金流为0；不复制账户现金流。原SMA3x累计收益-7.468958%如实保留。原账户为取得行情晚于参考时刻的延迟shadow，不能称同步实盘；十策略真实报价模拟仅只读汇总，各原账户180日/六折资格仍不足，冻结长期收集继续。

保存18份独立公共GET回执，本轮18，按完全相同URL复用先前成功响应0，实际运输失败0；真实失败原字节/UTC/URL/哈希与恢复保留。完整金融评估1次、完成账户窗口未重跑。初始读文件名错误和旧官方文档URL访问错误也已留档并使用正确来源解决。

只读网页监控生成成功=True，研究配置11008，旧行11002逐项保持。失败时恢复上次有效快照并保留真实证据。所有18个实际配置、36个登记事件完整finish，下一轮从next_research_state.json恢复，不重复精确配置。

复现顺序（历史记录，已完成目录禁止再次计算）：

```sh
cd /home/desktop/Documents/Codex/EquiTide
python3 -B research/experiments/20261117T142055Z/commands.py freeze
python3 -B research/experiments/20261117T142055Z/commands.py units
python3 -B research/experiments/20261117T142055Z/commands.py bind
python3 -B research/experiments/20261117T142055Z/commands.py reserve_0
python3 -B research/experiments/20261117T142055Z/commands.py evaluate
python3 -B research/experiments/20261117T142055Z/commands.py audit
python3 -B research/experiments/20261117T142055Z/commands.py exports
python3 -B research/experiments/20261117T142055Z/commands.py finish_0
python3 -B research/experiments/20261117T142055Z/commands.py research_check
```

只读核验：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261117T142055Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261117T142055Z/forward.py --reproduce
python3 -B checks/strategy_registry.py
python3 -B checks/monitor_snapshot.py
```

来源：[Binance官方USD-M市场数据](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)、[Binance公共数据作者README](https://github.com/binance/binance-public-data/blob/master/README.md)，访问日2026-11-17。数据、原响应、spec、report、逐变体/逐折/成本结果、完整账户链和核验SHA/实际命令同目录保存。历史资金费available延迟为规范化假设；费用和成交风险代理为估计。
