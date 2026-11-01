# 本轮实际复现与核验入口

固定执行目录 `/home/desktop/Documents/Codex/EquiTide`，main，排他锁。实际命令与退出码见各 `*_commands.json`、reserve_batches、finish_batches 和 bootstrap/freeze/decision/grid/collect 回执。全部命令调用同一现有虚拟环境，不安装依赖。

```bash
cd /home/desktop/Documents/Codex/EquiTide
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
R=research/experiments/20261101T095117Z
$PY $R/bootstrap.py
$PY $R/freeze.py
$PY $R/commands.py initial
$PY $R/commands.py reserve_batch_0
$PY $R/commands.py evaluate
$PY $R/commands.py audit
$PY $R/check_decisions.py
$PY $R/commands.py summary
$PY $R/commands.py exports
$PY $R/check_grid_diagnostics.py
$PY $R/commands.py finish_batch_0
$PY $R/commands.py finish
$PY $R/commands.py forward
$PY $R/commands.py candidate
$PY $R/commands.py l4h02
$PY $R/commands.py observer_status
$PY $R/commands.py review
$PY $R/commands.py gates
$PY $R/commands.py feed
$PY $R/collect_evidence.py
$PY $R/finalize.py
$PY $R/publish.py publish
```

上列是本轮真实执行顺序，不能在完成目录原地重跑：保留 sealed report/archive/完整账本和 reserve/finish 历史，驱动会拒绝已存在结果。年度模拟只消费 plan.json 的8份真实Parquet，8份全部哈希核验；旧原生状态段恢复净值并核对完整NAV哈希，只有BTC2500/N250的2个策略定义重新模拟，父组合直接相加各自原生美元净值。所有6项预先reserve完成才计算，18成本场景含负收益。独立audit不调用策略simulate/decide/trade，仅重建信号、账务和指标；核验用代码与输入版本由 code_binding_before_evaluation.json/data_manifest.json 固定。

历史行情不进Git，保留原data路径和哈希；轻量的新原生逐笔/状态段、新父归档、全部CSV/图、当前真实HTTP完整响应和packet副本、冻结账户全账本和下一轮必要状态进Git。重复开发历史不是未触碰最终测试集；三个候选虽全年净正，严格近期与邻域失败，不能称稳定实盘盈利。原生动量component、两个benchmark与3个parent候选分别计数，不把控制角色当合格候选。

观察原SMA65、原singleS28与独立未过滤L4/H2分别保留规则/本金/持仓/成本/全NAV前缀。L4本轮必须参考分钟10:11 UTC闭合后启动，真实launch在l4h02_reference_closure.json；资金费不能重复记账，跨资金费风险状态不能压平成最终现金状态。三观察各3个新截止ID，实际登记并finish；未成熟不取消原180日计划。快照只读已有研究/账户，不执行策略、产生成交、改冻结规则或重新部署网站。

publish实际SSH非强制推main，完整远端tree和每个必要blob重新逐字节哈希，proof写.git/automation_proofs。必须看到publisher实际终态exit0，再释放本轮锁并单独核验封存文件/共享快照/main/账户链。所有日志是真实命令回执，未预写成功或commit SHA。

核验后清理：仅删除本轮可重建的语义元数据全量清单，不含回测结果；原SHA/字节数/定义数/恢复基准见cleanup_verification.json。实际spec/ledger/report/archive/账户全账本、原始响应和必要代码均保留。
