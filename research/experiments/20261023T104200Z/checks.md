# 实际门禁、保真留档与发布核验

固定目录`/home/desktop/Documents/Codex/EquiTide`，分支codex/strategy-research。启动SSH fetch实际exit0，HEAD/origin均`1ded390907a5d3327044add4056cfd554f7ac5f9`。自身broker PID1520654持有排他FLOCK，普通SSH非强推、fresh fetch/ls-remote及完整tree/结果SHA核验后才release。

|命令|实际exit|完整回执|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/check_signals.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/run.py freeze|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/forward_registry.py reserve|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/run.py evaluate|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/summarize.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/audit.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/run.py finish|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/audit_forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/forward_registry.py finish|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/forward.py --reproduce|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/forward.py --reproduce|0|final_gates.json|
|python3 checks/strategy_registry.py|0|final_gates.json|
|python3 research/monitor/snapshot.py|0|final_gates.json|
|python3 checks/monitor_snapshot.py|0|final_gates.json|
|python3 research/experiments/20261023T104200Z/check_feed.py|0|final_gates.json|
|git diff --check|0|final_gates.json|

金融报告SHA256`062308cf1e650bcf8faa59c55203dc7cff2021bfb93cb744ff1321c4b819ed1d`；原SMA完整报告SHA256`0cae98c1cbdef05bb1118551218dd3f219c7a766446c055a2ba32af29c3cd2f5`。18候选＋3真实部分观察分别reserve→finish，只追加42登记事件。18候选全部rejected，少数正收益也保留；3部分观察rejected不取消长期SMA冻结计划。

独立审核54×519123=28032642点、702整体/逐折指标、19440日决策、2160实际填单；18位整数边界/冻结A/B半收复/实际成交年龄与生产Fraction一致。终点退出6次，target/timeout可同时触发，完整原因与重叠计数保留holding_outcomes.csv。全NAV从实际现金/数量账本重建，禁止同日退出再入，手续费/价差/滑点/成交量冲击/tick守恒。

18定义/18不同三成本NAV路径仍是同一重复历史，不称独立样本。1/2/3倍净正4/3/1，最高3倍+5.682977%的BTC9%/H2仅2正折、4往返、邻域25%，按原门槛淘汰；预设D6%/H4两个中心3倍为负。不能用正折数量代替全局PnL，ETH3%/H2即使8正折仍严重亏损。

监控实际4011配置/103观察/10账户，本轮18新FP/54场景/648逐折的六位收益、DD、Sharpe、成本、NAV哈希与原报告逐项一致。旧exclusive-end别名回归仍可见；原paper10计划/状态、前轮SMA源状态/报告四受保护输入不变。snapshot只读，不产生交易。

本轮实际执行命令均returncode0；另有出版方网页直接open HTTP403，不是回测或shell失败。read_failures.json保留真实403，引用仅基于官方索引摘要；DeNicola作者期刊摘要和官方过滤器实际打开。没有用cat或管道外层exit0替代内层门禁，没有改历史收益。

敏感性图已实际打开核对，两币各3×3及预设中心连续日NAV/现金线完整可读。原SMA08:30→10:30只追加120闭合分钟，旧30772点原样前缀、各场景30892点；无新日决策/参考点/成交/费用，下个日事件Oct24 00:01UTC，原终点不变。

未生成磁盘NPY/checkpoint/重复下载页；保留18完整archive、全部正负结果/决策/成交/持仓/逐折/日NAV、原SMA完整累计账本/状态/输入及2原始HTTP响应。已finish报告原字节与登记SHA优先，必要的大JSON保留，不另迁移格式。114MB真实行情留忽略data，路径/字节数/SHA及复现命令见data_manifest.json。

只stage本轮目录、主登记和两个监控feed。普通SSH push后fresh fetch、独立ls-remote、含原Freqtrade gitlink的完整tree、索引/工作树及全部证据/源输入哈希核验，通过后release自身broker。真实commit/push/释放由随后命令和最终通知报告，本文不提前声称发布完成。

未验证：独立最终测试、完整365日、DSR/PBO、历史L2与实盘成交/TCA；原SMA仅21日部分观察。
