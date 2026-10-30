# 复现及只读核验

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，main only，持有research/automation/branch.lock。解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`，实际版本见runtime.json。

先读task.md/三技能/完整登记与239结论并验证main远端/目录，保护旧结果和账户。引擎仅majority_target允许S26，54合成未来扰动与36旧参数精确检查，真实33天上下文覆盖25/26/27ROC，费用/资金费/账本/风险公式原字节不变；前置检查无真实PNL。看结果前固定L3/4/5×S26/27/28，H.025/E−.01,N6/C.00005,独立本金5000/7500/7500,N500/2250/750,raw[1,1,1]及全部原严格门槛。四精确旧格只读，新五ETH+五父组合完整spec先reserve_batch_0/1成功才evaluate一次30场景，audit/summary/exports/comparison，finish_batch_0/1/finish全部实际正负结果；不改名重跑旧格。旧四格新邻域诊断不覆盖原登记/曲线。

实际命令、时间、退出、stdout/stderr见all_command_receipts及reserve/finish_batches。10真实金融+6冻结观察共16新ID/32追加事件。forward和candidate各一次，原账户08:30至10:30承接08:00:00.001资金费前1ms正暴露，两风险状态在09闭合08小时均检查，共9风险检查，无资金费重记/新成交/决策。原SMA公开GET一次TLS失败自动重试后成功，仅实际stderr/成功响应已捕获，未编造失败body；候选GET另一次失败空body/状态单独留档，独立有界重试后窗口成功。所有最终命令实际exit0。

已有精确结果只读核验，不新登记计算：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T113406Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T113406Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T113406Z/forward.py --reproduce
```

独立审计Fraction信号/Decimal每笔成本资金费/完整NAV/风险，不调用simulate/target/trade。45审计场景=30新+15旧父组合；6CSV逐数值和实际6面板查看。源8真实Parquet/16来源及全部公共原响应路径/SHA见data_manifest，缺匹配输入停止不合成，大行情留ignoreddata。14旧结果原资格/完整源账本保留。读取以后共享账户状态时，不回滚正常推进；按本轮commit/保存pointer核验。

当前中心L4/S27进入完整9邻域后严格率5/9失败；新两S26边界候选仅局部通过，不是宽平台。峰值L5/S27虽全期收益/DD更好却近期负收益，仍淘汰。下一S25扩网需重新预登记六个新配置并复用六旧格，固定内部中心L4/S26；若仍失败，应记录方向脆弱性并换假设，不连续追逐边界自称稳健。所有历史反复开发，未作独立未来/未触碰留出/DSR/PBO，不称稳定实盘盈利或真实容量。

冻结SMA65/singleS28原计划/本金/q/entry/desired/成本保留，当前10小时risk栈单postfund状态；下窗10:30至12:30按真实packet事件续接，下一资金费16UTC、日决策次日00:01。旧两观察是延迟真实闭合bar/资金费重建，不是十策略实时报价模拟。只读monitor只汇总已有账户/报告，无新回测/成交/部署。

main实际push/fetch/lsremote/全tree/blob证明与发布进程exit0在.git/automation_proofs/20261030T113406Z.json，全部成功后才释放本人锁。
