# 复现与核验

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，Python `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。每个spec先成功reserve；40金融及6partial均已finish，禁止对正式登记重复reserve/evaluate/finish或重开账户。

实际命令/原始exit/log在各 `*_commands.json`、reserve_batches及finish_batches；失败与恢复均保留。required_command_receipts选取实际有效完成凭据，不表示原始运行从未失败。finish_interruption_reconciliation.json绑定那个已完成但未收到进程回执的terminal事件。

本轮封存版本可执行：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T152659Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T152659Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T152659Z/forward.py --reproduce
```

审计从已保存真实成交/资金费独立回放原生NAV，按结构化(ns,eventcode)逐点归属加权；不调用源信号/交易模型。所有Parquet、16年度/近期源、源spec/report/archive及代码SHA见data_manifest。未进Git的大行情及公开HTTPpacket原字节留ignoreddata；缺失任何SHA匹配输入必须停止，不可合成替代。

审计保护当轮账户快照：未来paper10或候选正常继续后，共享状态/监控可能不同，防护应阻止混入未来账户。读取本轮提交blob与完整只读代码/账本核验历史，不为通过旧审计回滚正式main、共享账户或切分支；当时候选pointer原字节另存candidate_current_pointer.json。原候选独审实际命令见candidate_commands.json，原SMA精确回放实际exit0见forward_commands.json。

这是原固定规模银行净值的静态所有权，复现不得归一化、重设N、线性缩放订单解释非线性冲击、重算源模型或新增父层成交。旧资格不变，完整正负结果均在report及results归档。

CSV固定LF。publication_newline_recovery.json绑定修复前后每个CSV SHA、相同解析单元格及原始Git失败诊断；exports_recovery/monitor_recovery/feed_recovery命令均实际exit0。首次publisher在commit前停止，正式报告及账本未变。
