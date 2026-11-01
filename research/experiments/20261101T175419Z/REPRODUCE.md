# 本轮复核与真实执行命令

工作目录固定：`/home/desktop/Documents/Codex/EquiTide`；仅main。基准提交`c3b551aec151f93d7ba607f76d145c3ba14c60b3`已包含paper10的17UTC真实观察，完整保留。先核对`git rev-parse --show-toplevel`和AGENTS/task，不切换其他工作区，不新建分支/工作树，不读取凭据。

本轮解释器`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`仅作为已有Python环境，所有进程cwd都是固定仓库目录；版本见runtime.json。标准库Decimal28、numpy2.3.5、polars1.44.2等，没有为本轮安装依赖。原8个真实Parquet和16个来源输入的文件字节数/SHA、原始API响应、UTC单位和代码哈希见data_manifest.json。大行情保留在忽略data路径，未提交。初始16项真实证据与完整25190事件/12473ID及266份结论读取记录在context.json。

预登记顺序：完整spec/plan和源码合成检查通过；每个新配置单独调用registry.py reserve，实际exit0回执保存在reserve_batches/。两批8+4之后才运行估值：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T175419Z/commands.py evaluate
```

上面是已实际执行的命令记录，不应在当前已完成定义上重跑。run.py拒绝覆盖已有report；12定义已全部独立finish rejected，旧K1/BTC/hold的10唯一结果仅复用状态段重建NAV并验证原哈希，未重新执行旧策略。参数/失败判据在结果前固定。代码绑定、所有36场景和报告原字节均封存，report SHA为`43e42637b267571af66920bb5bc882430cc85ed268f325a63323c336ca384d12`。

以下为只读独立核验命令；从保存的必要逐笔/资金费/状态段和真实行情重建账务与净值，不调用simulate/decide/trade、不写账户或登记、不作新参数试验：

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T175419Z/audit.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T175419Z/check_decisions.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T175419Z/check_grid_diagnostics.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T175419Z/check_exports.py
```

这些命令可能重写相同核验输出；封存仓库日常应只读其已有回执，不改已finish报告。实际命令、cwd、开始结束时间、stdout/stderr和进程exit_code分别保存在各phase_commands.json及日志；data_manifest记录全部哈希。audit总计含旧来源与新原生，research_evidence_counts.json分开统计，避免把父复用操作当新成交。

新机制仅对fresh entry/flip要求K连续已完成日快ROC同向严格极值，slowS28和vol10 cap当前检查；退出/同向保留不被确认拦截。lookback L3/4/5×K1/2/3，K1等价旧规则只读；L4/K2为内部Sharpe峰值，但新父近期3–4/8不满足6/8，局部严格支持低于60%。370天历史已反复开发，不称未触碰最终OOS或稳定实盘正收益。

三个冻结账户实际执行并核验：SMA65和singleS28从Nov1UTC14:30到16:30，L4/H2从16:10到18:10且在18:11参考闭合后启动。延续完整现金/数量/desired/risk/NAV及成本。singleS28新增16资金费基于q=-.012，L4已有16资金费不重复；均0新成交。原计划/本金/参数/终止边界不改，partial rejected继续原180天计划。已有截止绝不重新reserve/advance；源HTTP/packet、增量journal和完整指针链保留。

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T175419Z/audit_forward.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T175419Z/audit_candidate.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261101T175419Z/audit_l4h02.py
```

后续账户指针继续前进后，当前审计器针对本轮结束指针的assert会按设计失败，不得将指针回退；使用本轮封存回执与完整链核验。SMA来源输入旧段可为资产1d/1m字典，本轮续接是minute数组，原65日上下文另有nextstate指向。

registry/monitor在同一排他锁内实际运行：`python3 checks/strategy_registry.py`、`python3 research/monitor/snapshot.py`、`python3 checks/monitor_snapshot.py`；只读快照8944行，全部8932旧行字典一致，10固定报价账户/214既有观察，压缩4040595字节沿用5MB预算。既有paper10计划/执行器/状态不改，不重部署网页或建立定时任务。

TDD预期红灯、rg缺失及可选pyarrow元数据探测失败均保留，均未造成金融重跑。SMA curl有一次可确认TLS35 stderr并内部恢复；原传输器未逐次输出失败响应体，不补造尝试次数。所有真实成功响应、日志与本轮原生结果/负收益期间均保存。

只删除22027字节可重建语义查重材料，原哈希/字节数/依据在cleanup_verification.json；金融档案、冻结账本/计划和必要输入删除0。提交与push成功不能预写：实际main SHA、远端完整tree/必要blob核验及进程终态/解锁证明见`.git/automation_proofs/20261101T175419Z.json`。
