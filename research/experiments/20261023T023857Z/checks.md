# 本轮实际检查与发布约束

目录`/home/desktop/Documents/Codex/EquiTide`，分支`codex/strategy-research`。启动SSH fetch实际exit0，HEAD/远端`1e744cad27d772308f9666d6ba79df6297158399`，没有上轮未推送结果。broker PID1424493持有排他flock，普通SSH推送及完整远端核验后才释放。

|命令|实际exit|完整回执|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/signal_checks.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/run.py freeze|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/forward_registry.py reserve|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/run.py evaluate|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/summarize.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/run.py verify|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/run.py finish|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/audit_forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/forward_registry.py finish|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/forward.py --reproduce|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T023857Z/forward.py --reproduce|0|final_gates.json|
|python3 checks/strategy_registry.py|0|final_gates.json|
|python3 research/monitor/snapshot.py|0|final_gates.json|
|python3 checks/monitor_snapshot.py|0|final_gates.json|
|python3 research/experiments/20261023T023857Z/check_feed.py|0|final_gates.json|
|git diff --check|0|final_gates.json|

金融报告`31f27c96a31a272c811e6ad2ed485213c2a8fa387ee680e03afce9ed19b6e9bf`；原SMA报告`4f9d4f6cf1687141b29cac4b0fbcd607668d4776bcac5c5998518f0fb177e6d4`；冻结规则计划`f5dd0a3f2bf703a8df3ce8f93eb027e6d625d3fa45d5ff3c0c8610536a6669fb`。21个实际reserve/finish配对、全部负收益及partial保留；主登记只追加42事件，原历史前缀不改。

实际检查包括：54成本场景/648逐折重放、19440条有理数信号及持仓/60秒时序、1014成交守恒、54初始本金锚定分钟整体DD、1460日成交量独立聚合；下轮账户30389分钟/30412点完整NAV前缀及9场景离线重放；两公开原始分钟响应及过滤器响应源哈希；四个行情Parquet和所有关键源文件哈希。

门禁以实际运行进程returncode为准。strategy_registry和monitor_snapshot均exit0，snapshot成功，3939配置/99观察/10账户。新54场景六位小数、逐折日采样DD、全程分钟DD、NAV SHA、费用与执行数对应原报告；旧别名回归可见；只读持有基准原字节和来源哈希未改。四个受保护输入未变，paper10执行器额外固定哈希。

唯一失败为初始化两个错误文件名的只读读取（read_failures.json），不是回测。金融、前向、HTTP获取、登记、监控均无非零退出，未改历史收益或已finish报告。

清理54个重复checkpoint前，核对其全部标量/折与报告，并独立序列化五份CSV逐字节一致；完整结果、原始响应、源状态和原SMA累计NAV均保留。未重算既往精确配置、未重新部署网页、未创建定时任务或真实订单。

下一步发布只stage本轮目录、主登记和两监控feed；普通SSH非强推，再fresh fetch/独立ls-remote/完整tree及全部证据哈希核验，最后释放自己的broker。本文不提前声称新提交发布完成，真实SHA和推送/释放以随后的命令回执及最终通知为准。

未做实盘/L2/TCA校准；历史复用与多重选择偏差仍在，SMA仅21日partial。没有稳定实盘盈利结论。
