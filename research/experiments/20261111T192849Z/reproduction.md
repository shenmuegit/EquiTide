所有执行目录固定为 `/home/desktop/Documents/Codex/EquiTide`，main，同一排他锁。原生完整 argv/cwd/UTC/退出码/日志见 `reproduction_history.json`、`*_commands.json` 及 `review/native_*_receipt.json`。本轮先完整查重和冻结，再合成数量成本36例、政策48例和7错误变体，绑定金融源，10项分别reserve，真实evaluate仅一次，独立audit/导出、10项finish；继续四原账户后核验完整链和登记片段、监控、收集、检查、封存、push和远端blob核验、释放锁。

已有真实配置不能重新reserve或回测。以下为已实际执行的只读重建核验命令；须保持本地数据哈希一致，账户共享指针后来推进时只读本轮原始文件，不回退指针或覆盖账本：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261111T192849Z/audit.py
PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261111T192849Z/forward.py --reproduce
python3 -B checks/strategy_registry.py
```

全部参数/轴/原权重、时间与失败门槛在plan和逐项spec，真实结果在results归档及不可改写report，全部登记在registry_records.jsonl。大行情仍留忽略的data，保存必要数据哈希、完整账户和真实公共响应。Nov11_16公共字段复用172818原捕获，不能把17:33 UTC改成新获取时间，不能复制其他账户金额。封存后没有产物追加；真实提交/push/ref/tree/blob/释放锁终态保存在 `.git/automation_proofs/20261111T192849Z.json`。
