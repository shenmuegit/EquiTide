固定工作目录 /home/desktop/Documents/Codex/EquiTide，同main排他锁；完整定义见spec.json、plan.json、specs/。所有真实命令、起止时间、退出码和stdout/stderr见 *_commands.json、reserve_batches、finish_batches及all_command_receipts.json。

实际运行时 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B，PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。每配置成功reserve先于计算；完整相同已完成配置只读，不重复reserve/evaluate。8份真实年bars/mark/funding/metadata留在忽略data/，hash/字节/边界在data_manifest。

保存结果核验命令：
```bash
cd /home/desktop/Documents/Codex/EquiTide
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261102T160054Z/audit.py
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```
审计从保存账本及原行情独立重建核算与NAV，不调用策略simulate/decide/trade；只重写相同派生摘要，封存后通常无需运行。策略仅将V==10接纳范围扩展至预设V5/10/20，样本std与入场过滤公式/会计复用；成本仍前20完整日。旧对照先补齐VW元数据再计算邻域。原3冻结账户不注入新VW或规则，不从现金重开，不重复00/08/16资金费。上轮13:59无金融配置已如实中断留档并推送2bf85e09，9个真实遗漏账户观察已补齐；本轮从这些实际状态连续续接。
