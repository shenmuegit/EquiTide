固定工作目录为 `/home/desktop/Documents/Codex/EquiTide`，分支 `codex/strategy-research`；锁内fetch核验起点 `57aa8f25849bad87caddef7c1c92e23b0cad88b5` 与远端一致，只有既有未跟踪data软链接。遵守用户固定目录要求，没有使用task.md中已过时的其他工作区路径。读取完整登记/片段10614事件、5203条登记、140份既往结论及已有freqtrade结果/OOS检查；初始16项均有真实结果，未处置他人观察登记。使用三个指定验证技能。

18个KAMA配置在任何行情收益计算前分别reserve成功，随后完成54成本场景、648逐折结果，全部为负收益并逐项finish rejected。效率窗口10/20/40日与慢平滑周期30/60/120日同时变化，快周期2日及对称1%价格缓冲固定，原始资产分仓权重1，不归一化。旧方向效率比直接交易指标，本轮用无方向ER适配累积价格锚，具体规则不同，不靠更名制造新颖性。

相对最好的BTC L10/S120仍为−3.058638%/−5.805260%/−8.481929%，只有4/12正折，三倍连续OOS分钟回撤32.907317%。所有18格未通过净正、8正折、25%回撤、60%邻域和2.5毛参考盈亏/成本门槛。所有负折、成本和边界格点保留；未按结果增补网格或放宽门槛。18条完整三成本NAV路径不同，但不表示独立样本。敏感性图已实际查看，两轴、18格和负收益颜色/数值对应完整报告。

指标自检覆盖SMA种子、单调/往返/恒价ER、平方平滑、未来前缀不变、尺度/平移、零噪声及严格缓冲边界。独立验证以math.fsum重建效率比，用变动权重的乘积展开代替生产递推，核对19440个日决策状态和时间；1242笔成交余额、54条本金锚定完整分钟回撤、648折及19494日净值点均通过。原始四份Parquet的UTC纳秒、闭合/连续性、大小和SHA均核验；成本沿用已核验Decimal核算、前20完整日波动率/quote ADV及参与率限制。公式来源和版本记录在plan/spec中，无新依赖或共享引擎改动。

原冻结SMA从UTC02:00追加120闭合分钟至04:00，九场景的完整28941点旧前缀保留至29061点，累计29039分钟/20完整天。0新决策、参考点和模拟成交，现金、数量、desired、账本和费用保持；BTC继续持仓、ETH继续现金。原始公开响应各121条（含重叠bar）及重放输入保留。forward.py及audit_forward.py与上轮源码逐字节一致；实际续接、独立审计与离线精确重放均exit0。三项部分观察分别finish rejected，原因是180天/六折尚未成熟，原长期计划继续；下一原日决策仍为2026-10-23T00:01:00Z，不重复Oct22，不越过下一事件只mark。

实际进程及stdout/stderr记录在initial_commands.json、research_commands.json、forward_commands.json和final_gates.json；本轮无失败命令。final_gates的五个命令均真实exit0，日志内容与保存输出核对一致，不用cat退出码代替检查结果：

- `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T042721Z/forward.py --reproduce`
- `python3 checks/strategy_registry.py`
- `python3 research/monitor/snapshot.py`
- `python3 checks/monitor_snapshot.py`
- `git diff --check`

监控3739配置、10账户、88观察；18新配置/54成本场景的收益、整体分钟回撤、逐折收益、往返、NAV哈希和OOS边界逐项匹配报告，见feed_verification.json。旧exclusive-end指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e保留可见。四个受保护输入严格等于冻结前SHA；重放允许未来paper10状态合法推进，同时保持单次调用前后不变及所有冻结来源哈希严格一致。

21个完成登记的report_sha256均匹配原始字节：研究报告354ef7139a328ffb0d290e24939d6ce455cfccd8886bd7ae0ad5275057a73a6d，SMA报告0cb57ddc16a80be81d48839dbc4672c7910cbf7ab3941f02941b5dd13a2f6c36。只在完成核验后删除54个可重建checkpoint和本轮字节码；所有负收益、原始响应、完整净值、连续状态、冻结规则、账本及下轮输入保留，不迁移或改写已finish结果格式。大行情保持忽略data，保留哈希和复现路径。只提交本轮目录、登记和两个feed；普通SSH非强推后用fetch、ls-remote及完整tree核验，再释放同一分支锁。

未下真实订单、重置账户、创建定时任务、重部署网页或委派子代理。反复使用的2025–2026历史不是未触碰最终测试集，20完整天的延迟shadow不能证明180天资格、当时可成交或稳定实盘盈利。
