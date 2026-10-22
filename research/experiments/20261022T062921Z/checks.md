固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，分支 `codex/strategy-research`。锁内fetch核验起点 `f334756fb999cf95989cfdd4ba0430cdb4666360` 与远端一致，只有既有未跟踪data软链接。用户固定目录要求优先于task.md中的旧工作区路径。完整读取登记/片段10676事件、5234条登记、141份既往结论及现有freqtrade结果/OOS检查；初始16项均有真实结果，无待恢复登记。采用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs。

18个HMA斜率配置均先reserve成功再计算，完成54成本场景/648逐折结果后分别finish rejected。两参数同时变化：HMA周期40/80/160日、比较间隔1/3/5日；半周期向下取整、根周期isqrt、完整窗口、零斜率保持实际持仓状态。每配置独立2000USDT，原始单资产资金占比1，不归一化。指标由作者原文公式定义，方向规则与过去KAMA价格缓冲不同，登记新颖性不依赖名称。

1/2/3倍净正配置4/4/3，但0通过。最佳ETH N80/M5为+5.828614%/+4.721496%/+3.622675%，仅5/12正折、4次往返，三倍连续OOS分钟回撤33.298559%、邻域盈利16.7%。所有18项未达到8正折及60%邻域门槛，15项未过25%回撤门槛，完整失败项在原报告保留。全部负收益、负折、正收益未合格与边界格点均留档，不根据结果扩网格或放宽门槛。18种三成本NAV路径不同，但不是独立市场样本。

指标自检包括WMA权重方向、完整窗口预热、整数半/根周期、恒价/线性序列、未来前缀不变、尺度/平移和零斜率状态边界。独立检查用整数卷积核及Fraction精确有理数重建HMA，替代生产代码的逐层Decimal WMA，核对19440个决策状态/时间；732笔成交余额、54条本金锚定完整分钟回撤、648折及19494日净值点通过。四个真实Parquet的UTC纳秒、闭合/连续性、大小和SHA核验；沿用已核验的Decimal成交、前20完整日波动率/quote ADV及参与率成本限制。无新依赖、共享会计引擎或监控代码改动，敏感性图已实际查看，两轴和18格数值对应原报告。

原冻结SMA由UTC04:00追加120闭合分钟至06:00，九场景完整29061点旧前缀保留至29181点，累计29159分钟/20完整天。0新日决策、参考点或模拟成交，现金、数量、desired、交易和费用保持；BTC继续持仓、ETH继续现金。两份原始响应各121条（含重叠bar）及重放输入保留，分钟源结构按真实类型处理。forward.py/audit_forward.py与上轮源码字节相同；续接、独立审计与离线精确重放实际exit0。3项部分观察finish rejected源于180天/六折尚未成熟，原长期计划继续；下一日决策仍为2026-10-23T00:01:00Z，不重复Oct22、不越过下一事件只mark。

initial_commands.json、research_commands.json、forward_commands.json和final_gates.json保留实际退出码及原stdout/stderr，本轮无失败命令。final_gates的五个命令均实际exit0，日志与保存输出一致，不用cat退出码代替门禁结果：

- `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T062921Z/forward.py --reproduce`
- `python3 checks/strategy_registry.py`
- `python3 research/monitor/snapshot.py`
- `python3 checks/monitor_snapshot.py`
- `git diff --check`

监控3757配置、10账户、89观察；18新配置/54成本场景的收益、整体分钟回撤、逐折收益、往返、NAV哈希及OOS边界与原报告逐项一致，详见feed_verification.json。旧exclusive-end指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e保留可见。四个受保护输入等于冻结前SHA；未来paper10状态可由独立任务合法推进，重放仍要求单次调用前后不变及所有冻结来源哈希严格一致。

21项完成登记的report_sha256均匹配原始字节：研究报告309d590f18fc2d707c80c37b5f7e7f87b430d9e67fb94549cf965a1f87257a69，SMA报告92b8ee7fecde435d6af0cd2ef0a2792386821298acb49dcc98fd5427595c1c31。核验后只清理54个可重建checkpoint和本轮字节码；完整结果、原始响应、完整净值、连续状态、冻结规则、账本及下轮输入保留，不迁移或重写已finish结果。大行情保持忽略data，并保留哈希及复现路径。提交仅限本轮目录、登记和两个feed；普通SSH非强推后通过fetch、ls-remote与完整tree核验，再释放分支锁。

未下真实订单、重置账户、创建定时任务、重部署网页或委派子代理。2025–2026为反复使用的开发历史；20完整天延迟shadow不证明180天资格、当时可成交或稳定实盘盈利。
