本轮完整冻结定义见spec.json、plan.json和specs/；实际命令、起止时间、真实退出码、stdout/stderr保留在各 *_commands.json、reserve_batches、finish_batches与all_command_receipts.json。固定工作目录 /home/desktop/Documents/Codex/EquiTide，同main排他锁。

实际研究运行时 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。逐定义reserve先于金融计算；有结果的完全相同配置只读，不重复reserve/evaluate。

保存结果核验命令：
```bash
cd /home/desktop/Documents/Codex/EquiTide
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T115954Z/audit.py
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```
审计从保存账本和对应原行情独立重建核算/NAV，不调用策略simulate/decide/trade；只会重写相同派生核验摘要，封存后通常无需再运行。8份年度真实数据在忽略data/，路径、边界、字节、SHA256见data_manifest。三个账户必须从原现金/数量/desired/risk/context续接，不能从现金重开或重记00/08资金费。本轮短窗原始响应和完整增量/账本全部保存。

新参数的唯一策略接纳修改为cap==.045扩展至预先固定[.04,.045,.05]；入场过滤公式及会计复用。当前网格使用current_grid_row补足旧对照缺少的VC字段，18个旧行fixture在首次金融登记前已验证。审计退出0后再计数/判断资格，summary退出0后再网格/导出检查；不继承上轮汇总/计数失败或用其代替本轮实际结果。
