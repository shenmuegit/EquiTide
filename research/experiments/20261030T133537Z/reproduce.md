# 复现与只读核验

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，main only，持有research/automation/branch.lock。解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`，版本见runtime.json。

先验证目录/main远端，完整读task.md、三技能、登记与240结论，保护旧结果/账户。引擎仅majority_target断言添加S25，54未来价格扰动/36旧参数一致性检查，真实33天历史覆盖24/25/26 ROC；费用/资金费/账本/风险公式原字节保持。看结果前冻结L3/4/5×S25/26/27、中心L4/S26、H.025/E−.01、N6/C.00005、独立本金5000/7500/7500、N500/2250/750、raw[1,1,1]和原严格失败门槛及内点失败停止准则。六旧格只读，三个新S25ETH+三个父组合各reserve_batch_0成功后evaluate一次18场景，audit/summary/exports/comparison，再finish_batch_0及finish。所有新正负结果和失败稳健性都保留；六旧格新邻域诊断另存不覆盖原资格。

原冻结forward/candidate只续10:30至12:30，原账户/计划不改，现金/数量/entry连续，资金费不重记；6小时风险检查0违规。网络失败按实际日志/原响应保留，独立有界重试不导致观察重跑。实际命令/时间/退出/stdout/stderr见all_command_receipts和reserve/finish_batches。review、python3 registry/snapshot/monitor gates及feed实际执行，原paper10账户只读。

已有结果只读复核，不新登记重算：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T133537Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T133537Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T133537Z/forward.py --reproduce
```

独审Fraction整数信号/Decimal每笔fill/资金费/风险与完整NAV，无simulate/target/trade调用；39审计场景=18新+21旧父组合，6CSV逐数值和6面板实际查看。8真实Parquet、16来源、原公共响应路径/SHA见data_manifest，缺匹配输入停止，不合成。大行情留ignoreddata；完整账本、冻结规则、登记和必要代码保留。18旧结果及所有历史源保护哈希保持，共12新完成ID/24追加事件。

三新S25组合全期三档净正却全部近期/邻域不合格；预设L4/S26内点严格率4/9失败，direction_stop_decision触发，不继续追逐S24/S23。旧canonicalpassed保留历史范围，不等于本轮完整内点通过。next_direction_proposal仅拟研究收盘通道突破N20/25/30×M5/10/15、中心25/10，本轮未计算/未登记该新方向；下轮须完整查重和逐项reserve再计算。相同历史仍为开发验证，不是未触碰最终测试/独立未来/稳定实盘盈利或真实容量。

冻结SMA65/singleS28下一窗12:30至14:30按真实packet续接，当前12小时risk单postfund状态；下一资金费16UTC、日决策次日00:01。08:00:00.001资金费已入账，不得重记，不采用新研究参数/重启账户，不把两旧延迟shadow称十策略实时报价模拟。只读monitor不新回测/成交/部署。

实际main commit/push、fetch、lsremote和全tree/blob核验与发布进程exit0在.git/automation_proofs/20261030T133537Z.json；全部成功后才释放本人锁。共享账户以后正常推进按本轮commit/保存pointer核验，不回滚main或账户。
