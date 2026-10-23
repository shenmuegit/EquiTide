# 实际门禁、源证据保真与发布核验

固定目录`/home/desktop/Documents/Codex/EquiTide`、分支codex/strategy-research，启动SSH fetch实际exit0，HEAD/origin均`701ccc97656e9e2bc7b5587e0a82598d1462b41d`。自身broker PID1561443持有排他FLOCK，普通SSH非强推、fresh fetch/独立ls-remote/完整tree与证据SHA核验后才release。

|命令|实际exit|完整回执|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/check_alignment.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/run.py freeze|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/forward_registry.py reserve|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/run.py evaluate|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/audit.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/summarize.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/audit.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/run.py finish|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/audit_forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/forward_registry.py finish|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/forward.py --reproduce|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T144255Z/forward.py --reproduce|0|final_gates.json|
|python3 checks/strategy_registry.py|0|final_gates.json|
|python3 research/monitor/snapshot.py|0|final_gates.json|
|python3 checks/monitor_snapshot.py|0|final_gates.json|
|python3 research/experiments/20261023T144255Z/check_feed.py|0|final_gates.json|
|git diff --check|0|final_gates.json|

金融报告SHA256`6094397f3a0369905b4f152ebc558da9450fdda9628fcdabcf26a415575f6ad7`，原SMA完整报告SHA256`2b198dee41b557ac57fbfb9c110e119dc65578043eb8ea54b82fbd393b4e16b6`。82新父金融配置（81候选＋1真实参考）和3个真实部分截止分别reserve→finish，仅追加170登记事件。81候选全部rejected，源20配置的既有status/report/archive原样保持，3SMApartial rejected不取消原长期计划。

全部81组BTC/ETH L×H组合在计算前冻结；每个父/参考各自reserve成功才评估，源18动量和2恒多共60场景只读，不重跑源信号、撮合、资金费模型或重登记旧组件。原值1/1是各一份已投入10000抵押账本、总20000，一次相加，不再乘50%、不归一化或跨保证金净额。

独立审计用结构化时间键对齐，读取源5244成交/59400资金费事件恢复60曲线，再与state_segments另一条路径和原SHA逐点相符；246新父成本曲线各486093点，总119578878点，2952整体/逐折指标真实exit0。原 source simulate/trade/signal/funding函数未调用。两实际源轴本轮相同，合成回归独立验证毫秒错位时只沿最近完成观察、不会前视插值，relativeepochkey防int64溢出。

3倍净正13/81；20/20日条件阈值切片9/9正，但全4D邻域最高37.5%，81项全不过正折/四维邻域门槛。最高组合3倍+3.980671%、混合采样DD7.077547%、1倍7/11正折；回撤下降不足以替代收益分散和参数稳健性。未把正收益称合格或实盘稳定盈利。

监控实际4113配置/105观察/10账户；82新FP/246成本/2706折的六位收益、DD、Sharpe、执行费、NAV哈希与原报告匹配，raw权重1/1、capital20000、11折及330日期间准确。旧exclusive-end别名回归仍可见，源20状态/报告/归档SHA和4受保护输入不变，snapshot只读无新交易。

原SMA取真实bar时curl报告TLS35 unexpected EOF，内置重试后外层Python实际exit0且取得完整真实响应；未单独捕获具体失败资产/每次重试退出码。原stderr/forward.log及SHA、成功响应SHA留read_failures.json。该事实不是最终门禁通过的证据；独立时间轴/重叠/NAV前缀审计和离线重放另实测exit0，不用cat或管道外层0冒充检查。

两张图均实际打开核验：9个L组合面保留全部81阈值格，20/20全绿与其他回看负值对照清楚；另图区分预设中心、事后峰值（未合格）、同预算恒多与现金线。新组合风险曲线继承源混合采样/1%保证金代理，不是真实逐tickmark或完整强平证据。

原SMA12:30→14:30仅新增120闭合分钟，旧31012点完整前缀保留，各场景31132点；无新日决策/参考点/成交/费用，下一日事件Oct24 00:01UTC，原终点不变，原Float/BTC1500/ETH500未更改。paper10冻结计划与状态只读；旧shadow不是十策略真实报价模拟。

没有磁盘NPY/checkpoint/重复下载；82父archive保留新结果和源NAV引用，不复制旧大trade/funding账本，旧20完整archive仍原处可核验。全部正负结果、源哈希、原SMA累计报告/账户/输入及2原始响应保留。原始8行情/资金费/元数据留忽略data，已finish报告原字节优先，不压缩迁移。

只stage本轮目录、主登记及两个feed。普通SSH push后fresh fetch/ls-remote、含原Freqtrade gitlink的完整tree/索引/工作树/全结果源输入SHA核验，再释放自身broker；不改main、不覆盖别人修改。真实commit/push/release由随后实际命令和最终通知给出，本文不提前称发布完成。

未验证：独立最终测试、365完整年度、DSR/PBO、真实逐tickmark强平/历史完整阶梯/L2/成交/TCA。新父组合没有产生新的独立市场样本。
