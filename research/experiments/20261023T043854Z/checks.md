# 实际检查、失败事实与发布约束

目录`/home/desktop/Documents/Codex/EquiTide`，研究分支`codex/strategy-research`。启动SSH fetch实际exit0，broker PID1449023持有排他flock；非强制SSH推送及远端完整tree/结果SHA核验后才释放。

|阶段|实际returncode|完整回执|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T043854Z/check_math.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T043854Z/run.py freeze|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T043854Z/forward_registry.py reserve|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T043854Z/run.py evaluate|1|research_commands.json|
|math_checks_after_fix|0|research_commands.json|
|evaluate_retry|0|research_commands.json|
|summarize|0|research_commands.json|
|audit|0|research_commands.json|
|finish|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T043854Z/forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T043854Z/audit_forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T043854Z/forward_registry.py finish|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T043854Z/forward.py --reproduce|0|forward_commands.json|
|forward_replay|0|final_gates.json|
|registry_gate|0|final_gates.json|
|snapshot|0|final_gates.json|
|monitor_check_final|0|final_gates.json|
|feed_attribution|0|final_gates.json|
|diff_check|0|final_gates.json|

金融报告`4abc0832fc281991676d01612a7e41848c95717ce1af1cc0848978a53aa85e7f`，前向报告`07b35333f1e9bbc36f72bad8618d4642ab8fcfdf6e150b16cf2c143cc2773fa0`。18个父组合与3个partial真实reserve→finish配对，主登记只追加42事件；12个旧组件状态/报告/archive保持。

初次evaluate实际exit1，失败发生于旧源NAV哈希恢复，未产生任何父配置结果；这不是最终成功记录。原失败evaluate.log与research_commands第一项保留。另一个只读诊断在序列化NumPy布尔值时异常，随后grep使外层shell exit0；其个别Python退出码当时未单独捕获，不能把该外层0当诊断通过。事实在diagnostic_serialization_failure.json，修正诊断另以独立exec实际exit0。

根因为OPEN在Decimal→Polars Float64→str→Decimal间丢末位，修复仅本轮读取器，以原生Decimal OPEN计算后再一次转float。闭合分钟编码保持原值，三个原始成本SHA和36条源曲线全吻合。随后成功evaluate_retry、独立账本/风险审核、18配置finish及所有指定最终gate实际exit0，不重写历史或已finish收益。

独立审核包括：36源曲线用保存持仓段/保存旧成交账本两条路径恢复并匹配原SHA，240源余额事件，54父成本场景全量重放，14006628向量点，378整体/逐折指标；权重75/25只代表初始1500/500分仓，不二次乘已经分好资金的NAV，不平均组件指标。

最终监控3957配置/100观察/10账户，新18FP/54场景与JSON六位小数显示一致，两期资格和原权重匹配；原绝对路径/别名回归配置仍可见，四个受保护源及paper10执行器不变。snapshot只读汇总，不产生交易。

不存在本轮磁盘NPY/重复checkpoint，保留18完整父archive及完整源证据、失败事实、原SMA状态/累计NAV/原响应。价格原始大数据仍在忽略data路径，SHA/复现路径记录。

只stage本轮轻量目录、主登记及两监控feed；普通SSH push后fresh fetch/独立ls-remote/完整tree及全部报告/清单/输入哈希一致才释放自身broker。真实commit及推送/锁释放状态由随后的命令回执和最终通知报告，本文不提前声称发布完成。

未做独立前向、连续全年或实盘/TCA验证；两段春夏历史反复使用，原SMA仅21日partial，没有稳定实盘盈利结论。
