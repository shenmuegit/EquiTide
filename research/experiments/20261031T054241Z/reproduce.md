# 复现与核验

所有命令在 `/home/desktop/Documents/Codex/EquiTide`、main及branch.lock排他锁内执行。解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。

已登记有实际结果的定义只读，不再次reserve或回测。原始同轮执行顺序和actual exit见 `*_commands.json`、reserve_batches及finish_batches；下列核验仅读取现有真实结果，不产生新交易：

```bash
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T054241Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T054241Z/check_exports.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T054241Z/forward.py --reproduce
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261031T054241Z/audit_candidate.py
python3 checks/strategy_registry.py
```

金融实际只执行一次：bootstrap完整读取→capture_warmup真实响应→freeze完整spec/plan→initial合成与定义核验→reserve_batch_0/1共10次成功→evaluate30场景→audit→summary_retry2/export→finish_batch_0/1及finish核对。汇总SyntaxError两次失败未计算或修改金融结果，正确导出只读原报告。

原SMA：forward reserve→实际闭合分钟续接→独审→finish→无HTTP精确重放。原singleS28：8实际HTTP200后packet目录缺失，0spec/0reserve/0advance；原失败目录留档，candidate_retry1以准确URL/SHA复用8真实响应、原normalize后reserve3→advance一次→finish，extraHTTP0。不直接再次运行已经完成的observer/run evaluate。

8原始Parquet、16上游年/近期输入、warmup原始response/ overlap、所有源码/账本和旧资格SHA见plan、context及data_manifest。历史完整状态段可重建545013点净值，无需提交可重建大数组。正负净值/折/成本均已保留，临时缓存清理不删除账本或冻结规则。

同锁、完成真实登记及必要检查后执行：

```bash
python3 research/monitor/snapshot.py
python3 checks/monitor_snapshot.py
```

只读汇总10策略已有账户/报价及研究报告；不产生新回测/模拟成交，main更新由网页自动读取。普通SSH非force推送，完整tree/blob及实际publisher进程退出0证明保存在.git/automation_proofs/20261031T054241Z.json。
