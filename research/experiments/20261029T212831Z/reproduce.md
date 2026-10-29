# 复现与只读核验

固定目录 `/home/desktop/Documents/Codex/EquiTide`，解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。18金融配置先各reserve，首轮无效实现被独审发现后全部finish blocked；同一18份spec成功重新reserve后才计算有效结果并finish。另6partial独立reserve/finish，共24新ID、84追加事件。不得在正式登记中重跑已完成有效精确配置或重开账户。

全部命令/退出见all_command_receipts、reserve_batches/invalid_finish_batches/finish_batches。初始计算虽完成，但缺预热资金费特征不符合完整规则；invalid_attempt保存原report/18全账本、原代码绑定与路径映射，原报告内旧路径按invalid_spec_report映射到其快照，不指向后来有效结果。同一预登记参数、数据边界和费用不变，仅修正full1212特征输入与1110OOS结算入账的区分；首轮暂pass/reject无效，未计正式资格。原始快照代码为取证，不能直接在其更深目录当正式账户运行。

数据/所有源spec/report/archive、算法版本/冻结规则SHA见data_manifest；8合并Parquet、16原始/近期源和公共HTTP原响应留ignoreddata并绑定SHA。缺真实匹配输入停止，不可合成。每次特征严格按available_ts和settlement_ts过滤、原始均值有理数计算；成本场景不改变资金费信号。旧ETHhold部分近期折缺日期，CSV仅按冻结day330/5日调度补足标签，不改旧收益与资格。

封存版本只读核验：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T212831Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T212831Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T212831Z/forward.py --reproduce
```

独审以独立有理数重建价格与可得资金费开仓信号、Decimal重算成交/资金费/风险、完整NAV与逐折，结构化(ns,eventcode)重建组合，不调用策略simulate/target/trade。所有权0.5/1.5不是新规模500/4500下单证明。后续共享账户正常推进后，共享文件保护断言会变；读取本轮提交blob、保存pointer和完整账本核验，不回滚main/账户，不切分支。历史通过仅限预设资金费网格，未独立未来验证。只读monitor不产生新模拟成交。
