# 实际检查、资金账本与发布核验

固定目录`/home/desktop/Documents/Codex/EquiTide`，分支codex/strategy-research。启动SSH fetch实际exit0，HEAD/origin均`1ff4b462607c1897cdf94cd8736ae4b077201db7`。自身broker PID1541238持有排他FLOCK；普通SSH非强推、fresh fetch/独立ls-remote/完整tree及证据SHA核验后才release。

|命令|实际exit|完整回执|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/check_money.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/run.py freeze|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/forward_registry.py reserve|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/benchmark_prepare.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/run.py evaluate|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/audit.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/summarize.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/audit.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/run.py finish|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/audit_forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/forward_registry.py finish|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/forward.py --reproduce|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T124125Z/forward.py --reproduce|0|final_gates.json|
|python3 checks/strategy_registry.py|0|final_gates.json|
|python3 research/monitor/snapshot.py|0|final_gates.json|
|python3 checks/monitor_snapshot.py|0|final_gates.json|
|python3 research/experiments/20261023T124125Z/check_feed.py|0|final_gates.json|
|git diff --check|0|final_gates.json|

金融报告SHA256`2c279d98f257c6a03202feb86168828e950046dc895cb4ed40a24da3b9704b84`，原SMA完整报告SHA256`85e313599f842f303b6c23b5699686054485d63f2078dce532fe592aa684f786`。18候选＋2真实恒多参考＋3原SMA截止分别reserve→finish，主登记仅追加46事件。18候选全rejected，2参考仅参考但有完整实际结果而rejected，3有真实partial结果而rejected不取消原SMA长期计划。

在任何金融计算前追加2同预算参考并单独reserve；主计划原字节/18候选规则未改。benchmark_plan.json与日志记录先后，20金融定义/60成本场景/660逐折全留。合成检查先证明线性永续开仓只扣费、多空价格盈亏方向、资金费支出压力、不可变交易历史、初始抵押上限和参与率拒单。

独立审核60×486093=29165580点、720整体/逐折指标、19800因果日决策、5244实际填单、59400实际资金费结算含空仓0、401427个状态/小时不利标记边界检查；均实测exit0。资金费率真实available_ts延迟保留，不进入信号/固定数量；现金/带符号数量/价格盈亏/资金费/五项费用守恒验证。初审后仅补报告描述元数据，最终再审以最终SHA finish，不重写已finish结果。

原值20%是10000抵押中的2000入场名义额，不自动归一化或按已用名义额放大收益。同向不缩放数量、反向先平后开，两腿各收费；永续空头不借现货，无借币费虚构。1/2/3倍费用和负资金费压力，正收入不增；5个候选3倍净正，但全部邻域不足60%，BTC20/1%虽8/11正折、3倍+3.933954%，仍rejected。

全NAV是分钟成交价代理、真实小时mark/结算mark及成交前后参考的混合采样轴，另报mark观察和成交代理DD；不冒充真实分钟mark权益或逐tick强平。1%维护率是声明代理，缺历史完整阶梯和L2/TCA；不利整小时最低余量约7979.92USDT仅是此采样模型安全，不是实盘保证。

监控实际4031配置/104观察/10账户，20新FP/60场景/660折六位收益、DD、Sharpe、执行成本、NAV哈希与原报告一致。11折/10000抵押/330日周期准确，未把20%敞口伪装100%权重。旧exclusive-end别名回归仍可见，4受保护输入/paper10冻结计划状态不变；snapshot只读无新交易。

本轮全部记录命令真实returncode0，无读取或金融失败；read_failures.json保留空清单，不虚构阻碍。官方作者时序动量页、Binance资金费与Mark/Last/保证金说明实际打开，本文不把研究论文或当前规则作历史盈利背书。敏感性图已实际打开核验，两3×3面及预设中心/同资金参考/现金线完整可读。

原SMA10:30→12:30仅120闭合分钟，旧30892点完整前缀保留、各场景31012点；无新日决策/参考点/成交/费用，下个日事件Oct24 00:01UTC，原终点不变。保持原Float与BTC1500/ETH500，不受本永续研究替换。

本轮没有磁盘NPY/checkpoint或重复下载；保留20完整正负archive、完整有符号成交/资金费/状态/折与日NAV、原SMA累计完整报告/状态/输入及2原始HTTP响应。8份原始永续/mark/资金费/元数据留忽略data、路径/字节数/SHA及复现命令记录在清单。已finish报告原字节优先，不另压缩迁移。

仅stage本轮目录、主登记和两个监控feed，不改main或外部开发目录；普通SSH push后fresh fetch/ls-remote、含原Freqtrade gitlink的完整tree/索引/工作树及全证据/数据哈希核验后释放自身broker。真实commit/push/release由随后实际命令和最终通知给出，本文不提前声称发布完成。

未验证：独立最终测试、365完整年度、DSR/PBO、完整历史阶梯/逐tickmark强平、真实L2/成交/TCA；本330日历史已重复研究。
