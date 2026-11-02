# 复核与复现

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，仅main。Python运行时 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python` 仅提供既有解释器/依赖，不切换仓库。

各实际命令cwd、起止时间、退出码、stdout/stderr见all_command_receipts、各阶段*_commands及12项逐条reserve/finish。合成红/绿与完整spec冻结后，全部12定义reserve成功，金融计算仅执行一次：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T055753Z/commands.py evaluate
```

已有报告和完成登记禁止重测，不删报告/改名或绕过状态保护。复核已有账本命令如下：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T055753Z/check_asymmetric.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T055753Z/audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T055753Z/check_decisions.py
PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T055753Z/forward.py --reproduce
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```

审核不调用金融simulate/decide/trade，不产生新交易/观察/登记；部分审核会重写自身核验JSON，封存原证据应保持原字节，需复核在受控环境比对。两份永续审核绑定本轮共享指针，未来推进后使用本轮保存指针及完整历史链，不覆盖共享最新指针。

新18原生成本账本包含真实决策、成交、资金费及分段现金/数量，独立Fraction复算多侧HL和固定空侧2.5%及原退出，Decimal复算费用、冲击、数量、资金费、小时风险后重建全部NAV。18父成本路径直接按原[1,1]相加BTC3750与ETH15000美元NAV，不另造父成交。11CSV包含全部36场景、逐月/尾折/近期折、每日NAV和完整两轴网格。所有新配置与匹配旧对称基线完整NAV不同。

真实8份行情/mark/funding/约束文件路径、字节、SHA256在plan/data_manifest，大行情位于忽略的data/normalized，未提交。账户HTTP/packet/失败尝试及原路径/副本hash保存在raw_evidence和index；SMA当前为minute数组，65日daily上下文仍为20261102T015622Z/forward_inputs.json.gz。

下一SMA/single窗口04:30至06:30，仅06:31参考闭合后；L4下一06:10至08:10，仅08:11闭合后，需按真实08结算ns/rate/mark/heldq入账一次并核对正时长风险段。均持同main排他锁、3新观察reserve后延续原规则/cash/q/risk，不注入非对称参数，不重复00资金费。新组合仅历史通过，峰值处在HL低端且历史反复使用；未启动新账户/定时任务，尚无独立未来资格。
