# 核验与复现

固定目录 `/home/desktop/Documents/Codex/EquiTide`；运行时 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。每份完整spec先reserve，40金融+6partial均finish；不得在正式登记中重跑已完成精确配置或重开账户。

真实阶段命令、退出和日志在各 *_commands.json 与reserve_batches/finish_batches。数据/所有源spec/report/archive、算法版本/冻结规则SHA见data_manifest与code_binding_before_evaluation。输入8合并Parquet、16年度/近期源及原始公共HTTPpacket留ignoreddata并绑定SHA；缺真实匹配输入必须停止，不可合成。

封存证据版本上的只读金融核验命令：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T172700Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T172700Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261029T172700Z/forward.py --reproduce
```

独审只回放已保存原生回测成交/历史资金费及状态段，核对每一源NAV SHA，再用结构化(ns,eventcode)独立合并、加权和重算全部整体/逐折指标；不调用原生策略simulate/target/trade。原候选独审、16资金费纳秒/现金/风险栈检查见candidate_commands及risk_carry_verification。

保护断言绑定当轮账户快照；后续paper10或原候选正常继续后，实时共享文件会变，应读取本轮提交blob/保存pointer/完整报告账本做历史核验，不为通过旧审计回滚main或正式账户，不切分支。CSV固定LF。原值w是固定规模银行净值所有权，不可解释成归一化下单或忽略lot/非线性冲击的新规模执行。所有旧资格保留；独立未来与稳定实盘盈利尚未证明。
