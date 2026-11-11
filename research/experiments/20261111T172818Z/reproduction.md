本轮所有命令均在 `/home/desktop/Documents/Codex/EquiTide`、同一 main 排他锁内执行。原生 argv、cwd、开始/结束 UTC、退出码、stdout/stderr 路径见 `reproduction_history.json`、`*_commands.json` 和 `review/native_*_receipt.json`；实际中断见 `orchestration_interruption.json`。

已有完成配置禁止重复 reserve/回测；原始执行顺序为 bootstrap → fresh funding16 public capture → freeze → synthetic units + four mutants → source binding → eight reserves → one evaluation → independent audit → exports → eight finishes → read-only research check → archived midnight regression → L4/FEWM/single original account continuations → original SMA continuation → accounts fullchain check → journal fragment → sources check → registry/monitor gates → feed → collect → final checks → staged whitespace → seal → publish/remote verify → release lock → private postrelease audit。

只读核验可运行以下实际使用的命令（前提是本地真实市场文件哈希与 plan 一致，账户指针仍指向本轮；指针后来推进时先只读旧 round 的原始文件，不能退回或覆盖共享指针）。这些审计只重建已保存账本及指标，不调用原策略交易函数、不 reserve、不模拟新成交：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261111T172818Z/audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261111T172818Z/forward.py --reproduce
python3 -B checks/strategy_registry.py
```

`plan.json` 固定真实数据文件、SHA256、完整规则、轴、时间边界和门槛；每配置 `specs/*.json`、真实登记 `registry_records.jsonl`、一次计算的 `results/*.json.gz` 以及未经重写的 `report.json` 共同保留重建依据。CSV/图为只读导出，不能代替原始报告精度。多年大行情保持 data/ 忽略状态，公共 HTTP 原始响应/失败和独立账户完整账本均保留。提交与真实推送最终 SHA、全 tree/blob 及锁释放证据位于 `.git/automation_proofs/20261111T172818Z.json`，不为追写 commit SHA 修改已封存产物。
