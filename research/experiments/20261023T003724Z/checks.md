# 本轮实际检查

固定目录`/home/desktop/Documents/Codex/EquiTide`，分支`codex/strategy-research`，启动SSH fetch已实际exit0，HEAD及远端均为`b21cfc02b0e8dd418f758c09f6dc9fde7ee5ce07`。本轮持有broker PID1396990的排他flock；按授权普通SSH push及完整远端核验后才释放。

|命令类别|实际退出码|证据|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/signal_checks.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/check_nav.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/run.py freeze|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/forward.py reserve|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/run.py evaluate|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/summarize.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/audit_b1.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/run.py verify|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/run.py finish|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/forward.py capture|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/forward.py evaluate|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/audit_forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/forward.py finish|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T003724Z/forward.py verify|0|final_gates.json|
|python3 checks/strategy_registry.py|0|final_gates.json|
|python3 research/monitor/snapshot.py|0|final_gates.json|
|python3 checks/monitor_snapshot.py|0|final_gates.json|
|git diff --check|0|final_gates.json|
|python3 research/experiments/20261023T003724Z/check_feed.py|0|final_gates.json|
|python3 research/experiments/20261023T003724Z/check_feed.py|0|final_gates.json|

计划`cf430bde5e3bdb464aa109fcc488d32b3d2722e80e60b9920b9016b70abcfab8`；金融报告`9ddecd909ab00a6332663d18b6608a932ba9b78160462f650009ccc332fc13c5`；原SMA报告`87f6471ccf15d771e5ddf145af0897b45c25a61dcf6e40563bd3fbd8d03756dc`。21个reserve及21个finish均保留真实stdout。主登记只追加42行，未修改历史前缀；所有18项候选均有完整负收益结果。

本轮只读验证：54全量重放/648个逐折结果/54个分钟NAV哈希；18项二维网格和陡变表；389366条B1信号与8176686项历史可得资金费；独立事件资金费/账本/所有小时NAV、26127360分钟标记；日线65/20成本上下文和分钟重叠及前缀连续；十策略与旧账户源哈希不变。

监控门禁当前进程实际exit0，不以cat日志exit0代替。3921配置/98观察/10账户；逐项54场景收益、费用、完整分钟代理DD、Sharpe、执行数、往返、NAV哈希及12折指标与展示六位小数一致。历史exclusive-end/别名回归保留，20项只读对照不重登记、不改归属。

失败说明仅read_failures.json中的两项只读诊断，均已查明并更正；全部金融/网络获取/registry/监控命令实际exit0。本轮未改历史收益，也未为了减体积重写已finish JSON/gzip。

清理只删与已保留完整结果相同的54份checkpoint及本轮可重建字节码，完整源数据/结果/账户状态保留。未重算前轮18B0和2基准、未部署网页、未创建定时任务。缺历史L2/TCA与真实清算阶梯校准，复用历史存在多重选择偏差，SMA仅21日partial；没有实盘稳定盈利验证。

发布核验遵循原授权：只stage本轮目录与主登记/两监控feed，普通SSH非强推；再fresh SSH fetch、独立ls-remote、完整tree/全部轻量证据及输入哈希、报告登记SHA核验，最后释放自己的broker。实际提交SHA/推送/锁释放结果由该次命令回执及最终通知报告，本文不提前声称发布完成。
