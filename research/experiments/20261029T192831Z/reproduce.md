# 复现与只读核验

固定目录 `/home/desktop/Documents/Codex/EquiTide`；解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`；环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。24金融及6partial实际独立reserve/finish，全部结果保留。正式登记不得重跑已完成精确配置或重开账户。

每个真实命令/退出、失败及恢复见all_command_receipts与read_failures；reserve_batches/finish_batches有逐ID完整stdout/actualexit。最初engine不接纳S30/31，plan_initial保留；extend_guard只扩白名单，engine_change_verification及两版code_binding证明旧规则不变。第二次执行已完成24账本，run_executed是真实执行版本；原生只读对照元数据遗漏由recover_report只读恢复，未重算任何已完成曲线。

8行情合并Parquet、16原始/近期来源、每个源spec/report/archive、算法/冻结规则SHA见data_manifest。原公共HTTP响应与失败响应在ignoreddata、纳秒实际价格/资金费/成交完整账本留存；缺匹配输入需停止，不可合成。旧ETHhold近期五日折日期缺元数据，CSV仅按冻结第330日8×5日边界补足时间标签，不改任何旧收益或资格。

封存版本只读核验：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T192831Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T192831Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T192831Z/forward.py --reproduce
```

独审用有理数独立重建原生决策、Decimal独立成交/资金费/风险和全部完整NAV，以结构化(ns,eventcode)独立合并原值所有权组合，不调用simulate/target/trade。后续共享账户正常推进后，保护断言所绑共享版本会变；应读取本轮提交blob/保存pointer/完整账本核验，不回滚main或账户，不切分支。只读monitor不产生新模拟成交。历史正收益不代表稳定实盘盈利。
