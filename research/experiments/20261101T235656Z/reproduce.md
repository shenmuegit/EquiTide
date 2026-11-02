# 复核与复现命令

所有命令工作目录固定为 `/home/desktop/Documents/Codex/EquiTide`，分支 `main`。
Python 运行时为 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，仅使用该虚拟环境，不切换仓库或工作目录。

本轮原始执行顺序及每个真实退出码、起止时间、stdout/stderr在 `all_command_receipts.json`、各阶段 `*_commands.json` 与12条 reserve/finish独立回执中；bootstrap实际终态见 `bootstrap_receipt.json`。预期合成红灯与修复后绿灯另存，不计真实行情结果。

本轮实际金融计算命令：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T235656Z/commands.py evaluate
```

上述命令只在12项spec成功reserve后运行一次。已完成定义禁止再次评估，`run.py`存在报告与登记状态保护；需要核验时只重建已保存账本，不能删除报告或绕过登记。

只读合成/账本/导出复核：

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T235656Z/check_funding.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T235656Z/audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T235656Z/check_decisions.py
PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T235656Z/forward.py --reproduce
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```

审核程序不调用金融 simulate/decide/trade，不追加观察或交易。以上部分审核会重写自身核验JSON，已封存轮次应在受控环境只读比对；不要改动原封存证据。两份永续审核绑定的是本轮共享指针，下一轮指针推进后应从本轮保存的指针与完整历史链比对，不覆盖共享指针。

完整8份真实行情/mark/funding/交易约束文件在 `plan.json` 和 `data_manifest.json` 保存路径/字节/SHA256。大行情位于忽略的 `data/normalized`，未提交。新原生18条成本账本保存真实决策、资金费、成交及分段现金/数量；重建完整分钟/事件NAV后比对原hash。父18条成本路径只按原始[1,1]相加两银行NAV，与原生来源全曲线hash逐条对齐。原始HTTP及完整账户输入packet保存于 `raw_evidence`，原路径/副本hash见index。

新窗口仅可在同main排他锁内单独reserve后推进；原SMA和singleS28下一窗口跨Nov2日决策，原L4已完成午夜事件、下一窗口00:10至02:10必须02:11闭合参考后执行。冻结规则、实际资金/数量和历史登记不能重置。
