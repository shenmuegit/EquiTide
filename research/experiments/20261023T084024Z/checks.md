# 实际检查、失败事实与发布约束

固定目录`/home/desktop/Documents/Codex/EquiTide`，分支codex/strategy-research。启动SSH fetch实际exit0，HEAD/origin均`4508c29e8534d82f1c489c3579065e6030eb8f50`；自身broker PID1497023持有排他FLOCK，非强制SSH push及远端完整tree/结果SHA核验后才release。

|命令|实际exit|完整回执|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/check_signals.py|1|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/check_signals.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/run.py freeze|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/forward_registry.py reserve|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/run.py evaluate|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/summarize.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/audit.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/run.py finish|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/audit_forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/forward_registry.py finish|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/forward.py --reproduce|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/forward.py --reproduce|0|final_gates.json|
|python3 checks/strategy_registry.py|0|final_gates.json|
|python3 research/monitor/snapshot.py|0|final_gates.json|
|python3 checks/monitor_snapshot.py|0|final_gates.json|
|python3 research/experiments/20261023T084024Z/check_feed.py|0|final_gates.json|
|git diff --check|0|final_gates.json|

金融报告SHA256`b0c417d9734c2b8a05da1a4b1360fcb6794cdb790a323177d6d7ce51689e4a9c`，原SMA报告SHA256`47573ca940eb070d21b5ba0266ac09b37eafdea814b702f685df0879b02ee636`。18金融＋3真实部分观察各自reserve→finish，主登记只追加42事件，全部有实际结果而rejected；不因partial拒绝取消原SMA长期计划。

独立审计54×519483=28052082个向量点、702整体/逐折指标、19440日历/状态决策（其中2754周一整数排名）、720实际填单、90双腿换币。先卖后买、中间OPEN风险、手续费/价差/滑点/冲击/tick和共享现金守恒均验证；18定义仅12种三成本完整路径，2个全成本正定义实际同一路径，均未过稳健性。

第一轮合成检查实际exit1：输入150/100本来强于130/100，样例期望错误。修复仅ETH合成中间值150→120，生产规则/18参数完全未改；此前没有金融reserve或计算。原失败signal_checks.log、initial_commands第一项、样例和日志SHA见signal_fixture_failure.json；修正后的合成测试及全部金融、前向和最终必要gate实际exit0。另有NBER直接网页HTTP403，仅引用官方可读索引摘要，不声称读取全文。

监控实际3993配置/102观察/10账户。18新FP/54场景/648逐折的六位收益、DD、Sharpe、成本、NAV哈希及12折验证状态与原报告一致；共享单资产目标敞口1不伪装75/25分仓。旧exclusive-end别名回归配置仍可见，受保护4源及paper10冻结计划/状态未改。

图像sensitivity_surface.png已实际打开核对：两张3×3面及两预设中心连续3倍日NAV完整显示，标题、原参数和现金0收益线可读。原SMA06:30→08:30仅120闭合分钟，旧30652点完整前缀保留，各场景30772点；无新成交/费用/日决策/参考点，下个日事件Oct24 00:01UTC。

本轮无可清理磁盘NPY/checkpoint/重复下载页，所有必要18完整archive、正负结果、失败事实、原SMA完整报告/账户账本/输入及2原始响应保留；已finish报告原字节与登记SHA优先，不为压缩另迁移。原始大行情114MB留忽略data，路径/字节数/SHA及重放命令见data_manifest.json。

只stage本轮目录、主登记及两监控feed。普通SSH push后fresh fetch/独立ls-remote/完整tree（含原Freqtrade gitlink）/索引/工作树/全清单与输入哈希核验，通过后释放自身broker；不改外部GitNexus/Claude目录，不用目录级ls-files精确匹配实际文件。真实commit/push/release由随后实际命令和最终通知给出，不提前声称完成发布。

未验证：独立最终测试、完整365日、DSR/PBO、实盘L2/成交/TCA；18参数相关且只复用同一360日历史，原SMA仅21日部分观察。
