本轮工作目录固定为 /home/desktop/Documents/Codex/EquiTide，仅 main。运行环境为原研究虚拟环境，PYTHONDONTWRITEBYTECODE=1、OPENBLAS_NUM_THREADS=1、OMP_NUM_THREADS=1。原始行情路径与 SHA256 在 plan.json/data_manifest.json；全部原生实际执行命令、时间、退出码和日志在 *_commands.json、review/native_*_receipt.json。每个具体定义的 reserve/finish 凭据在 reserve_batches/finish_batches，账户定义另有各自原登记凭据。完整计算只执行一次，已完成同配置不得直接重跑 evaluate 或观察窗口。

以下命令只复核已保存真实结果，不发新数据请求、不生成交易、不修改账户：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261113T134318Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261113T134318Z/audit_candidate.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261113T134318Z/audit_l4h02.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261113T134318Z/audit_fewm.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B /home/desktop/Documents/Codex/EquiTide/research/experiments/20261113T134318Z/forward.py --reproduce
python3 -B /home/desktop/Documents/Codex/EquiTide/checks/strategy_registry.py
```

其中审计器会写自己的核验JSON；封存后如需复核必须先核对输出字节不变，不能改写已经绑定的旧证据。用于本轮所有图表/归因/报表的输入仅为上述已完成实际结果；合成 primitive 明确标为 synthetic_only，未冒充市场回测。新的策略参数必须另存新轮 spec、先成功 reserve 后计算。现存8个新BTC组件、8个新父组合与旧锚使用完全相同的真实389日历史，非独立最终测试集。当前原账户和十策略执行器冻结规则不受本研究改变。
