本轮完整定义见 spec.json、plan.json 和 specs/。实际执行命令、起止时间、退出码及 stdout/stderr 在各 *_commands.json、reserve_batches、finish_batches 和 all_command_receipts.json；均在固定仓库根目录执行。

研究运行时：/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，PYTHONDONTWRITEBYTECODE=1，OPENBLAS_NUM_THREADS=1，OMP_NUM_THREADS=1。本轮金融登记先于所有实际计算，重复的有结果配置不得再次 reserve 或 evaluate。

现有结果只读审计命令（审计只重建账本/NAV检验，不调用金融策略 simulate/decide/trade）：
```bash
cd /home/desktop/Documents/Codex/EquiTide
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T075753Z/audit.py
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```

封存后无需修改原始证据；以上 audit 只会重写相同核验摘要。8份年历史数据保存在忽略的 data/，路径、字节、SHA256 在 data_manifest.json；所有本轮短窗原始响应和完整账户增量已保留。冻结账户不可从现金重开，不能通过复现重下观测或重复08点资金费。
