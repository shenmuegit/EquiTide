固定执行目录 `/home/desktop/Documents/Codex/EquiTide`，main，同一排他锁。完整原生argv/cwd/UTC/退出码见reproduction_history、*_commands.json及review/native_*_receipt。顺序：完整查重/冻结V[5,6,7]×VW[8,10,12]→36数量成本合成例/27完整政策例/7错误变体→绑定金融源→16项reserve→一次真实evaluate→独立audit/导出→16项finish→四原账户续接与完整链核验→登记片段/monitor gates→collect/final checks→暂存/封存→push/独立tree/blob核验→释放锁与私有postrelease。

已有完成配置不得重reserve/重回测。以下为本轮已执行的只读重建核验；需真实本地行情文件与plan哈希一致。账户共享指针后来推进时仅查本轮原始文件，不回退/覆盖指针或账本：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261111T212846Z/audit.py
PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261111T212846Z/forward.py --reproduce
python3 -B checks/strategy_registry.py
```

逐项spec/plan固定全部规则、两个适用窗口、时间和失败门槛；results归档/report/registry_records保留所有真实结果，CSV/图不替代原始精度。大行情留忽略data，仅保留数据哈希/必要原始公共响应和完整账户。当前所有账户仅marks/risk、旧Nov11_16已各记一次；后续跨Nov12_00需真正新字段和00:11闭合参考，不使用旧率或提前执行。封存后无追写；真实commit/push/ref/tree/blob/锁释放证据保存在 `.git/automation_proofs/20261111T212846Z.json`。
