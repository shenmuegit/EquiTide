本轮完整冻结定义见 spec.json、plan.json 和 specs/；所有实际执行命令、起止时间、真实退出码与stdout/stderr保留在各 *_commands.json、reserve_batches、finish_batches和all_command_receipts.json。固定工作目录为 /home/desktop/Documents/Codex/EquiTide，使用同main排他锁。

实际研究运行时：/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。每个新配置成功reserve先于金融计算；已完成相同配置只能读结果，不重复reserve/evaluate。

保存结果的核验命令：
```bash
cd /home/desktop/Documents/Codex/EquiTide
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T095853Z/audit.py
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```
审计仅从保存的实际账本和原行情重建独立核算/NAV，不调用策略simulate/decide/trade；audit会重写相同派生核验摘要，封存后一般无需再执行。年度8份真实数据留在忽略data/，边界、路径、字节与SHA256见data_manifest。原SMA及两个独立永续冻结账户均必须延续原cash/q/risk/上下文，不可从现金重开，不能重复观察或重复08资金费。所有本轮短窗原始响应、完整增量及账本保留。

实际初次evaluate在所有12归档/36场景计算完成后，旧对照元数据HL关键字误代HS而失败；原始run.py与初始代码绑定保持原字节。report_recovery_plan/binding/regression/verification记录纯汇总恢复；recover_report.py明确禁止simulate/decide/trade、market.load/recover和evaluate，未重跑金融或参数。报告的evaluation_started_utc是原命令真实启动时间，早于内部金融计算，仅用于证明登记先行，不虚构未持久化的内部首条计算时间。counter先于audit结束触发的真实文件缺失另存count_dependency_failure，审计完成后仅重跑只读计数。两个失败的原始退出和stderr均永久保留。
