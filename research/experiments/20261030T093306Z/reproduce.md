# 复现及只读核验

固定工作目录 `/home/desktop/Documents/Codex/EquiTide`，main only，持有research/automation/branch.lock。解释器 `/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python`，环境 `PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`。实际版本见runtime.json。

先验证目录/main/远端，读task.md、三技能、完整登记与238结论，保护旧账户和结果。initial冻结L2/3/4×S27/28/29、H.025/E−.01、N6/C.00005、独立资本5000/7500/7500与N500/2250/750、raw[1,1,1]及全部失败门槛。只新增8ETH组件和8父组合；精确旧L3/S28中心、同本金常持和固定源只读，不重复reserve/模型/交易。reserve_batch_0/1各8成功后evaluate一次48场景，再audit、summary、exports、comparison；finish_batch_0/1及finish，所有正负实际结果留档。源8旧结果原资格/哈希保留，新邻域诊断另存不改中心旧passed。

原SMA及singleS28续06:30至08:30，forward/candidate各一次；资金费实际08:00:00.001，保留原始毫秒和先后状态。candidate原观察和独立审计成功，补充风险检查的整点假设失败；修复后缺Path导入再次失败；candidate_checks_retry2仅重跑补充检查和创建已有3观察的发布索引，最终exit0，未重跑观察/金融模型或改账本。完整失败代码、退出和log保留；all_command_receipts、read_failures、risk_check_recovery记录事实。随后observer_status只读、review、python3 registry/snapshot/monitor gates、feed核验；实际调用及时间/退出见各receipt。

已有精确结果只读审计，不新登记重算：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T093306Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T093306Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T093306Z/forward.py --reproduce
```

独立审计用Fraction整数信号和Decimal每笔现金/LOT/tick/冲击/资金费、完整NAV及风险，无simulate/target/trade调用。54审计场景包含48新与6只读旧父组合；6CSV逐数值和实际6面板查看。源8真实Parquet、16来源、全部公共原响应路径/SHA见data_manifest，缺匹配输入停止，不合成。大行情留ignoreddata；完整新正负账本、旧源/冻结规则/登记和必要代码保留。

370日重复开发历史，12完整30日+10尾日、day330继承近期8×5日，不是未触碰留出或独立未来。只有L4/S27角点通过，旧中心价格邻域严格率4/9失败，不能称宽平台或稳定盈利；旧中心原a/慢L/H资格仍原样保留。下一批边界扩网须独立预登记，精确旧格只读，不把同历史扩网叫最终验证。

当前singleS28风险栈在08整点旧现金和08:00:00.001新现金间有1ms正暴露。下窗09点闭合08小时须检查两状态，不能删成零时长；原始1%闭合小时极值代理不是真tick清算证明。下窗08:30至10:30按真实packet判定事件，16资金费/次日00:01前不主动换仓。继续原本金/数量/entry，不采用新研究组合，不拿旧延迟shadow当十策略实时报价模拟。只读monitor不新回测/成交/部署。

完整push/fetch/lsremote/tree/blob证明与发布进程实际exit0在.git/automation_proofs/20261030T093306Z.json；全部成功后释放本人锁。共享账户以后正常推进，读本轮commit和保存pointer核验，不回滚main或账户。
