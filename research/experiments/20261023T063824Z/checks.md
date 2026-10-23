# 实际门禁、完整证据与发布核验

固定目录`/home/desktop/Documents/Codex/EquiTide`；分支codex/strategy-research；启动普通SSH fetch实际exit0、HEAD/origin均`cbc240a9c7d1a173644fedc7f877b60fd31b0eeb`。自身broker PID1472319持有排他FLOCK，推送及fresh fetch/ls-remote/完整tree和证据哈希核验后释放。

|命令|实际exit|完整回执|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python /home/desktop/Documents/Codex/EquiTide/research/experiments/20261023T063824Z/check_signals.py|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python /home/desktop/Documents/Codex/EquiTide/research/experiments/20261023T063824Z/run.py freeze|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python /home/desktop/Documents/Codex/EquiTide/research/experiments/20261023T063824Z/forward_registry.py reserve|0|initial_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python /home/desktop/Documents/Codex/EquiTide/research/experiments/20261023T063824Z/run.py evaluate|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T063824Z/summarize.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T063824Z/audit.py|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T063824Z/run.py finish|0|research_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python /home/desktop/Documents/Codex/EquiTide/research/experiments/20261023T063824Z/forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python /home/desktop/Documents/Codex/EquiTide/research/experiments/20261023T063824Z/audit_forward.py|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python /home/desktop/Documents/Codex/EquiTide/research/experiments/20261023T063824Z/forward_registry.py finish|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python /home/desktop/Documents/Codex/EquiTide/research/experiments/20261023T063824Z/forward.py --reproduce|0|forward_commands.json|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T063824Z/forward.py --reproduce|0|final_gates.json|
|python3 checks/strategy_registry.py|0|final_gates.json|
|python3 research/monitor/snapshot.py|0|final_gates.json|
|python3 checks/monitor_snapshot.py|0|final_gates.json|
|python3 research/experiments/20261023T063824Z/check_feed.py|0|final_gates.json|
|git diff --check|0|final_gates.json|

金融报告SHA256`1afd0147a48f8d039de9364cf019d3bffc7f23951808ad737af754a049c9bede`，原SMA报告SHA256`2f25b1494c4a6584e98638b3224b0496539bd72a29a0500169b680f642544c5b`；21项真实reserve→finish，共追加42登记事件。金融18项中15研究候选全部rejected、3同资金持有参考仅作参考登记rejected，3SMA部分观察有实际结果而rejected，不停止原冻结计划。

独立核验54场景×518762点，合计28013148点、702整体/逐折指标、8640闭合先前决策、288真实叶填单。24叶曲线按实际成交重建，30父曲线只加同金额叶NAV一次，保留1500/500原资金含义。

图像sensitivity_surface.png已实际打开检查：9格均亏损、坐标与原值正确，预设中心和同资金持有曲线完整显示。

监控实际3975配置/101观察/10账户。18新FP/54成本场景/648逐折的收益、DD、Sharpe、成本、NAV哈希及原75/25权重均与不可变原报告一致；旧exclusive-end别名537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍可见。monitor最近轮new_configs=15表示研究候选数，另3个参考配置也完整展示，未丢失任何结果。

四个非金融只读诊断失败完整保留read_failures.json：不存在文件sed/cat各一次，其管道/后续命令的外层exit0不能视为读取成功；两个元数据探针分别values解包ValueError、缺少summary的KeyError，实际exit1。按实际文件/字段修正后继续，金融计算、登记、独立审计与最终所需gate均实测exit0。失败事实未覆写成通过，不重算历史收益。

原SMA04:30→06:30追加120闭合分钟，旧30532点前缀保持，每场景完整30652点；无新交易、费用、日决策或参考点。下轮从06:30继续，下一日决策Oct24 00:01UTC，长期终点不变。保留完整报告/账户/输入、两原始HTTP响应及源状态哈希；paper10计划与状态未改。

本轮未生成NPY/checkpoint或重复下载页，无可清理的磁盘中间产物。已finish报告原字节与登记SHA优先，必要5MB完整SMA报告保留；原始大行情留data，固定路径、字节数、SHA和重放命令均记data_manifest.json。

只stage本轮目录、主登记及两监控feed；不自动合并main。采用普通SSH push，成功后fresh fetch、独立ls-remote、完整tree列表/索引/工作树/清单/所有结果哈希核验，再release自身broker。真实commit/push/锁释放由随后实际命令及最终通知给出，本文不提前声称已发布。

未验证：独立最终测试、完整365日年度、DSR/PBO与实盘L2/TCA；此360日连续历史反证为负，原SMA仍仅21日部分观察。

提交前范围守卫曾实际exit1：ls-files --directory额外显示GitNexus/Claude开发目录，目录级精确匹配过严；在git add之前停止，没有提交或改写金融/账户。随后以NUL分隔git status逐个实际文件验证exit0，只允许本轮目录、三个共享变更与既有data/normalized；外部开发目录保留且不stage。失败与修正见precommit_scope_failure.json。
