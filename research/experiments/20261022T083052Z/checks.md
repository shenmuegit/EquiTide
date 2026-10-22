固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，分支 `codex/strategy-research`。锁内fetch核验起点 `4a2c048a52608d446da3f67e09eb18fcd3c85437` 与远端一致，只有既有未跟踪data软链接。用户固定目录要求优先于task.md中的旧工作区路径。完整读取登记/片段10738事件、5265条登记、142份既往结论及现有freqtrade结果/OOS检查；初始16项均有真实结果，无待恢复登记。使用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs。

18个Aroon高低点时间差配置均先reserve成功再计算，完成54成本场景/648逐折结果后分别finish rejected。回看20/40/80日与入场阈值20/40/60同时变化，退出0固定；N+1根完整日高低区间、并列极值取最近日、严格入场边界和零值保持多头均提前固定。每配置独立2000USDT，原始单资产资金占比1，不归一化；与旧收盘HMA斜率规则不同。StockCharts官方公式和TA-Lib v0.6.4原实现作为一手依据，Python公式实现独立，没有安装TA-Lib或复制C源码。

1/2/3倍净正数量为6/6/6，0通过。最佳ETH N40/E40为+27.639440%/+26.297240%/+24.970144%，三倍整体分钟回撤21.293194%，但仅5/12正折、4次往返、44.4%邻域三倍盈利；这些门槛未放宽。18项均未达到8正折，16项未过25%回撤、16项未过60%邻域、14项未过8往返，完整失败项在原报告。不同参数全部独立登记；18配置只有15组完整三成本NAV，BTC80的20/40阈值及ETH80的20/40/60阈值各组路径重合，详见path_equivalence.json，不当独立证据。全部负收益、负折、边界格点和未合格正收益保留，未按结果扩网格。

指标自检覆盖N+1窗口最旧端点、最近并列极值、恒价/上涨/下跌、未来前缀不变、尺度/平移、严格入场及零退出边界。新增读取真实分钟high/low列并核对区间包含open/close及正价格；Polars日极值聚合与NumPy分钟重排max/min独立核对，共2920个日高低值。信号用反向argmax/argmin重新求最近极值日期，并以整数分子比较阈值，核对19440个决策状态和时间。576笔成交余额、54条本金锚定完整分钟回撤、648折及19494日净值点均通过。四个Parquet的UTC纳秒、闭合/连续性、大小和SHA及日高/低/收盘数组哈希保留。成本及成交沿用已核验的Decimal核算、前20完整日波动率/quote ADV及参与率限制；共享会计引擎和监控代码未改，未新增依赖。敏感性图已实际查看，两轴及18格数值对应原报告。

原冻结SMA从UTC06:00追加120闭合分钟至08:00，九场景完整29181点旧前缀保留至29301点，累计29279分钟/20完整天。0新日决策、参考点或模拟成交，现金、数量、desired、交易和费用保持；BTC继续持仓、ETH继续现金。两份原始响应各121条（含重叠bar）及重放输入保留，分钟源结构按实际类型读取。forward.py/audit_forward.py与上轮源码字节相同；续接、独立审计与离线精确重放实际exit0。3项部分观察finish rejected是因为180天/六折尚未成熟，原长期计划继续；下一日决策仍为2026-10-23T00:01:00Z，不重复Oct22、不越过下一事件只mark。

initial_commands.json、research_commands.json、forward_commands.json和final_gates.json保留实际退出码及原stdout/stderr，本轮无失败命令。final_gates五个命令均真实exit0，日志与保存输出核对一致，不用cat退出码代替门禁结果：

- `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T083052Z/forward.py --reproduce`
- `python3 checks/strategy_registry.py`
- `python3 research/monitor/snapshot.py`
- `python3 checks/monitor_snapshot.py`
- `git diff --check`

监控3775配置、10账户、90观察；18新配置/54成本场景的收益、整体分钟回撤、逐折收益、往返、NAV哈希及OOS边界与原报告逐项一致，见feed_verification.json。旧exclusive-end指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e保留可见。四个受保护输入等于冻结前SHA；未来paper10状态可由独立任务合法推进，重放仍要求单次调用前后不变及所有冻结来源哈希严格一致。

21项完成登记的report_sha256均匹配原字节：研究报告0079a00f55d0cec32796f92ea833dccedc427a462d81aa55e1a64cb30f7e2c49，SMA报告32dc6585d9d30729ca5be49ed4c875b2cba4db3021e4fe9dacfbfd6cac5481e1。核验后只清理54个可重建checkpoint和本轮字节码；完整结果、原始响应、完整净值、连续状态、冻结规则、账本及下轮输入保留，不迁移或改写已finish结果。大行情保持忽略data，并保留哈希及复现路径。提交仅限本轮目录、登记和两个feed；普通SSH非强推后通过fetch、ls-remote与完整tree核验，再释放分支锁。

未下真实订单、重置账户、创建定时任务、重部署网页或委派子代理。2025–2026为反复使用的开发历史；20完整天延迟shadow不证明180天资格、当时可成交或稳定实盘盈利。
