# 复现与只读核验

固定目录/home/desktop/Documents/Codex/EquiTide，main only，持有research/automation/branch.lock。解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python；环境PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。runtime.json保存版本。

完整实际命令/退出/日志见all_command_receipts：bootstrap→initial（族ID格式失败，0预留/计算，失败计划保留）→initial_retry1（真实8文件/570543点时钟、135合成边界/回滚、freeze9、代码绑定）→reserve_batch0/1（8+1）→evaluate一次27场景→audit失败bisect/audit_retry1失败hashlib→audit_retry2最终独审通过→summary/exports→finish_batch0/1、finish。金融规格参数/结果未因检查失败改动，所有原码绑定保持。

金融结果已完成，不再次reserve/evaluate。只读复核：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T194013Z/audit_complete.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T194013Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T194013Z/forward.py --reproduce
```

原始8Parquet与16只读来源路径/SHA在data_manifest，缺数据即停止，不合成或改历史。九规格明确720小时logETH~logBTC、24完整小时训练间隔、被测小时排除、E2/2.5/3×X.5/1/1.5、48h上限与双腿执行/拒绝/付费unwind/恢复规则；银行各10000/ETH名义2000/BTCbeta*2000，raw[1,1]不归一化、不NAV调仓。旧9ADF模型与3旧长持对象只读，旧标记时钟/暴露不同须保留比较范围。

独审不调用model.simulate/decide/open/close或trade：独立math.fsum拟合8880窗口、239760决策、Decimal每笔4752fill/59940fund/109170risk、81曲线46213983NAV点与全部折/近期指标。六CSV逐数值和一图六面板查看，9项全部成本/稳健性淘汰，不把1x边缘正收益或重复开发历史称未触碰最终测试、协整或稳定实盘盈利。

原冻结forward/candidate只续16:30至18:30，3+3观察分别reserve/finish，原资金/数量/entry/规则不变。最初候选TLS35和原目录保护失败都发生在0候选预留/计算；失败目录与原raw不覆盖，单独*_capture_retry目录做一次额外实际捕获，20秒/2次/验证TLS，首次metadata超时28后成功；随后8HTTP200、连续5554点/138ID/5429分钟、6风险0违规验证。当前18小时单postfund状态，16资金费已入账勿重记；下窗18:30至20:30按真实packet续，旧SMA65上下文路径保留，次日00:01日决策、180日终点不变。旧延迟shadow不当十策略实时报价模拟。

15新完成ID/30追加事件，18244保护文件、9旧配对和3旧比较结果不改。只读monitor已有10账户191观察，8708研究行，页面读取main不重新部署。next_direction_proposal仅未测试raw基金单位组合，零新reserve/结果，下轮完整查重/冻结/逐项预留后才能计算。所有负收益与失败保留，只清理可重建进度文件。

publish.py直接提交/push main，fetch/独立lsremote/全tree和必要blob/原输入哈希核验；发布进程实际exit0才释放锁。实际SHA、进程、锁释放与发布后证明见.git/automation_proofs/20261030T194013Z.json，其他任务以后可正常推进共享状态，按本轮commit/保存pointer复核，不回滚账户。
