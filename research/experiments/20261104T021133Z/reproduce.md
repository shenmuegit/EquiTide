本轮复核与复现

固定目录：`/home/desktop/Documents/Codex/EquiTide`；只使用 main，遵守 research/automation/branch.lock。原始执行命令、cwd、UTC起止时间及真实退出码见各 `*_commands.json` 与 `reserve_batches/`、`finish_batches/`；汇总见 `all_command_receipts.json`。实际顺序为 freeze、initial、两批reserve、evaluate、audit，再逐配置finish。没有实际结果的工程检查不算金融回测。

数据版本由 plan.json、code_binding_before_evaluation.json 与 data_manifest.json 的字节/SHA限定。需要 ignored data/normalized 中原始8个parquet；不重新下载替代历史，不重跑已有原生模型。新9组合只复用23项既有真实结果中的13个原生账本，按共同事件轴将美元NAV相加，raw[1,1]，银行3750/15000、实际预算500/4500、总本金18750。所有源spec/report/archive版本和指纹见plan.read_only_references。

在本轮原始main提交状态、账户最新指针仍对应本轮时，可执行以下复核命令。后续轮次指针变化后，原观察审计会主动拒绝不匹配；应在本轮封存状态核对，不能改写最新指针、重新预留旧配置或重新采集替代数据。

```bash
cd /home/desktop/Documents/Codex/EquiTide
research_py=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
research_round=research/experiments/20261104T021133Z
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
"$research_py" -B "$research_round/audit.py"
"$research_py" -B "$research_round/check_decisions.py"
"$research_py" -B "$research_round/audit_forward.py"
"$research_py" -B "$research_round/forward.py" --reproduce
"$research_py" -B "$research_round/audit_candidate.py"
"$research_py" -B "$research_round/audit_l4h02.py"
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```

复核使用已保存实际响应与资金费/成交账本，不创建金融配置或模拟订单。原SMA65保持Float规则，原single保持L3/S28零退出规则，独立L4保持L4/S28零退出规则；三者不能套用研究SMA32参数。原观察partial状态未达到180日/六折，不取消冻结计划。独立原生账本审计里的旧操作条数不是本轮新成交；audit_scope_provenance_note.json解释继承scope文字的旧资本表述，权威资本与敞口断言均由本轮spec/plan核验。
