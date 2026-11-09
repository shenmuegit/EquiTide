本轮复现工作目录固定 /home/desktop/Documents/Codex/EquiTide，main。解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python，环境 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。

真实执行顺序和原生命令/退出码见各 *_commands.json、reserve_batches/、finish_batches/、reproduction_history.json；预登记时间、全部规则、实际数据路径/字节/SHA256见 plan.json/specs/、funding_signal_preflight.json、code_binding_before_evaluation.json。完整登记为主日志加全部 registry_records.jsonl 片段，必须用 registry.read_events/read_records。

本轮 H×F：H=[0.0175,0.02,0.0225]，F=[0,0.00005,Off]；Off 精确旧结果只读。E=0.0075、L5/S16/D3/K0.0075/V10/VC0.05固定。代表H0.02/F0.00005事前固定。任何参数/权重/数据边界都未在看结果后修改。

1. freeze、真实资金费源/暖启动可得时间检查、合成正确检查与3个故障注入反例；绑定36个根代码及immutable依赖。
2. reserve_batch_0（8项）、reserve_batch_1（4项）均原生0后 evaluate 一次；保存6个新ETH银行及6个真实父组合的三成本完整证据。无旧策略重跑、无NAV线性缩放。
3. audit 独立从真实输入和留存现金/数量/成交/资金费/状态片段重建所有新旧原生和新父组合曲线，并重算全期、逐折、近期统计；counts/summary/exports/decisions/grid通过后逐项finish。
4. 四原冻结账户只续接本轮已闭合窗口；每个新观察先reserve，再捕获实际公共输入、原状态advance、独立账本/风险/完整NAV前缀审计、finish。FEWM仅复用同窗真实公共数据，自己的账户独立计算，不复制L4现金流。不得重复已完成cutoff。
5. 24个配置共48个事件保留为本轮registry片段，旧主日志/片段字节不变、全事件多重集和逻辑索引一致。原生registry门禁与只读monitor/snapshot.py、checks/monitor_snapshot.py后封存提交main并普通非forcepush，独立HTTPS ref、完整远端tree和所有必要blob逐字节核验，真实终态见.git/automation_proofs/20261109T230923Z.json。

允许的验证命令（读取已保存真实证据，不重新评估策略配置）：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261109T230923Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261109T230923Z/check_decisions.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261109T230923Z/check_grid_diagnostics.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261109T230923Z/check_exports.py
```

这些旧审计脚本会写自己的派生核验JSON；本轮封存后不得在封存目录直接覆盖。复核时将输出定向到临时目录，保留原证据哈希。registry reserve 已有实际结果时返回3，必须读取旧结果，不通过改名或元数据制造“新”配置。全量原始大行情与公共响应仍保留忽略data/，Git只存轻量核验必要输入、账本、报告和代码。

normalized funding.available_ts=settlement_ts+1h 是保守冻结假设，不是交易所历史网络到达证明。00时最新结算未成熟，实际每日选前一日16时结算；只用settlement年龄1–12h且available<=signal的过去字段，缺失阻止新入场。真实现金流仍用实际fundingTime/rate/mark/当时q，1/2/3倍支出、收入不放大。反复开发历史，不是独立最终或未来收益证明。
