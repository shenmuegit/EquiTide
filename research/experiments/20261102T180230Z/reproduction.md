# 复现与留档

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，main 分支；所有写入持有 `research/automation/branch.lock` 排他锁。Python运行时 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B`，PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。行情路径、SHA256、闭合边界见plan/data_manifest，源策略、原生会计及所有代码哈希见code_binding_before_evaluation。commands JSON保存每次实际命令、cwd、时间、exit code和完整日志。

严格按以下顺序运行，各命令前补上述runtime/env；路径前缀均为 `research/experiments/20261102T180230Z/`：

1. `bootstrap.py` 完整读取登记主簿及所有追加片段、278份历史结论、task/三个技能、原freqtrade结果JSON/ZIP、checks/*oos.py，核验初始16实际证据及旧文件。
2. `check_asymmetric.py --legacy-exit-range` 在旧源上合成检查，实际exit1为预期接纳红灯，日志与TDD_red_receipt保留，不是金融回测。
3. `commands.py freeze` 冻结完整spec/参数/权重/数据/失败判据；`commands.py initial` 验证144策略fixture及18旧行fixture并绑定源代码。补齐本轮观察审核时界后，`commands.py bind_account_window` 在任何reserve之前重新绑定；初始绑定原字节保留。
4. `commands.py reserve_batch_0`、`commands.py reserve_batch_1`，每项调用registry.py reserve，12项成功才 `commands.py evaluate`。已有实际结果和原0.25%中心均只读，禁止精确重跑已完成策略。
5. `commands.py audit` 独立Fraction/Decimal价格/信号/实际数量/成本/funding/风险/净值审核；`commands.py summary` 只读导出。audit成功后执行 `commands.py counts` 和 `commands.py decisions`；summary成功后执行 `commands.py grid` 和 `commands.py exports`。
6. 登记写操作串行：`commands.py forward` 先reserve原SMA新截止、追加闭合mark、独立审核、finish、离线精确重放；`commands.py candidate` 原singleS28延续新窗口；`commands.py l4h02` 原独立L4/H2延续新窗口（18:11参考必须已闭合）。两永续观察分别先reserve，保存原始公开GET、精确Decimal账本/NAV链并finish。它们是已有账户延续，不能用新历史参数替代。
7. `commands.py finish_batch_0`、`commands.py finish_batch_1`、`commands.py finish`；所有12实际结果含淘汰项逐个registry.py finish。`commands.py observer_status` 只读原账户状态。
8. `commands.py review` 核验源结果/登记前缀/21新ID和42追加事件及保护文件；`commands.py gates` 实际执行 `python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`，失败恢复上次有效快照。`commands.py feed` 核验新增12行/36场景和全部旧展示行完整字典保持；`commands.py collect` 保存全部真实短窗原始响应及必要下轮状态。
9. 实际view_image检视sensitivity.png，清理仅本轮可重建缓存/中间物，保留全部完整账本和结果。`finalize.py` 校验实际退出、reserve时序、独立审计、原哈希、数据hash、完整账户前缀与监控后封存。封存后不修改本轮文件。
10. `publish.py publish` 只stage本轮及五个必要共享文件、commit、SSH非强制push main、fetch和独立ls-remote，验证完整递归tree及全部必要远端blob SHA256。终态实际exit0后记录.git私有凭据，释放本轮broker并独立复查。

已完成配置只允许离线复核已有报告、完整实际账本和原始响应，不重跑策略、不对过去报价补下单。复核始终使用本固定工作目录及原spec/输入hash、registry历史，不向main重复reserve、不覆盖完成结果，不创建其他分支或worktree。本文的步骤是已执行流程/复现边界，不授权覆盖已完成的当前轮文件。
