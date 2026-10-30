# 复现与已有结果只读核验

工作目录 `/home/desktop/Documents/Codex/EquiTide`，main only；解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。先完整读取task.md/三技能/登记和历史，验证本地远端main与独占锁，保护旧未推送结果和账户。

看结果前冻结plan.json和66个完整spec，presentation_plan固定几何中心。a25/50/75%×慢动量L20/25/30×H2/4/6、E1%，fastL3/H2.5/E−1/S28majority-entryonly/N6/C.5bp固定。真实BTC5000/N500旧组件复用；新ETH本金15000a/N4500a反转、15000(1−a)/N1500(1−a)动量，各自lot/tick/冲击/现金/资金费/抵押重算；父组合raw[1,1,1]，不归一化、不共享资本。36原生组件/控制+30父组合，27为候选，39仅参考；每个reserve成功后run.py evaluate一次，实际198场景，再逐项finish，不能将已完成配置改名重测。

真实调用顺序及各命令实际exit/stdout/stderr见all_command_receipts.json和reserve_batches/finish_batches。commands.py initial；reserve_batch_0至8；evaluate；audit；summary；exports；comparison；finish_batch_0至8；finish；forward；candidate；observer_status；review；gates；feed。bootstrap_receipt记录全登记和237结论读取。独占锁持有至main实际push、fetch、lsremote/fullrecursiveblob证据核验且发布进程实际exit0，再释放。

新配置现已完成，复现优先只读独审记录账本：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T073235Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T073235Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T073235Z/forward.py --reproduce
```

audit_native用独立整数/Fraction信号、Decimal新数量与每笔成本/资金费/保证金/完整NAV，audit.py独立共同(ns,eventcode)时钟与组合净值，不调用simulate/target/trade。6CSV逐数值核验、3图18面板已实际打开。8真实合并Parquet、16来源及原始公共响应路径/SHA见data_manifest；缺真实匹配输入停止，不合成，不提交大行情。原生完整账本/全部正负结果gzip、冻结spec、登记与命令均保留。44旧结果原资格/完整账户/paper10文件不改。

重复开发历史370日、12完整30日+10尾日、day330继承近期8×5日；不是未触碰最终测试或独立未来。短反转价格参数本轮固定，其先前脆弱性尚未解决；执行通过不等于实盘容量或稳定盈利。成本估计和1%闭合小时风险代理非L2/TCA/逐tick清算证明。以后共享账户正常推进，核验本轮commit和保存pointer，不回滚共享状态。

原SMA65/singleS28仅延续04:30至06:30，原规则/本金/持仓/entry/成本不改。本窗0成交/决策/资金费、6闭合小时风险检查；下窗06:30至08:30跨实际08资金费，必须基于真实packet精确贷记一次并检查前后风险状态，不能套用本窗零事件假设。两个旧延迟shadow不称十策略实时盘。只读monitor汇总已有报告/账户，无新回测/成交/部署。
