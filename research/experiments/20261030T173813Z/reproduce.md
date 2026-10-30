# 复现与只读核验

固定目录/home/desktop/Documents/Codex/EquiTide、main only、持有research/automation/branch.lock。解释器/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python，环境PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1，版本见runtime.json。

实际命令、时间、退出和stdout/stderr日志见all_command_receipts：bootstrap→initial（数据、1485票数/1485未来扰动、冻结、定义）→reserve_batch_0..3（8/8/8/3）→evaluate一次→audit→summary/exports/comparison→finish_batch_0..3/finish→forward→candidate。candidate原账户执行和独审exit0，后补充risk_carry检查因严格递增假设exit1，失败原样保留。只执行candidate_checks_retry1复查/索引现有3ID，未重新GET/执行账户/登记；其后observer_status/review/gates/feed全部exit0。

完整规则和27spec见plan.json/specs。E5/6/7×H2/3/4，中心6/3；源N20/25/30×M5/10/15九格的pre-OPEN方向三成本一致且独立因果核验，排除被测收盘，无源当次OPEN/fill/PnL/funding特征。原交易/资金费/风险/数据/统计函数AST保持，完整代码在计算前绑定。BTC/ETH银行各10000，固定名义1000/2000；父raw[1,1]总20000，不归一化或缩放旧NAV。18新native真实执行，9父组合复用新NAV；18源信号与3旧常持只读，均未重新金融回测。

已有结果只读复核，不重复reserve或evaluate：

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T173813Z/audit.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T173813Z/check_exports.py
env PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261030T173813Z/forward.py --reproduce
```

独审整数源信号/Fraction数量/Decimal成交费用、实际纳秒资金费、小时状态风险/完整NAV与逐折。84场景45,781,092点、6CSV逐值、3图18面板实际查看。数据清单保留8真实Parquet/16来源输入与公共原响应SHA，缺数据即停止，不合成。原始行情留ignoreddata，必要账本/规格/代码/实际失败证据保留。

原冻结SMA65/singleS28从14:30至16:30续接，原规则/本金/数量/entry保持。本窗原singleS28实际16:00整点funding每成本BTC+.093099965652168、ETH0，6流水/124新增NAV点，累计135ID/5432点/5309分钟；6闭合小时风险检查0违规。原core保留同纳秒pre/postfund状态，只有正持续区间计风险；失败补充检查改为验证这种实际语义，未改core/状态/报告。下一窗16:30至18:30按真实packet续接，16资金费已计入不重记，次日00:01决策与180日终点保持；SMA65旧日上下文在next_research_state保留。两旧延迟shadow不称十策略实时报价模拟。

33新完成ID/66追加事件，全部正收益/负折/淘汰保存。27配置全期三成本净正仍全部月折/近期5日折/邻域严格门槛失败；新参数重复旧/本批NAV不构成独立市场证据，见path_diversity。21旧结果与17975保护文件哈希不变。next_direction_proposal仅未测试价差假设，零新reserve/计算，下一轮先查重、补全双腿执行/失败规则、冻结和登记，不能据此称协整/盈利。

所有必要登记/只读snapshot/monitor检查在同main锁内实际执行，paper10仅汇总已有10账户190观察，网页读取main不重部署。publish.py提交推送main，再fetch/独立lsremote/全递归tree及所有必要blob与原输入哈希核验；发布进程实际exit0后释放本人锁。实际SHA、进程退出、解锁和发布后核验见.git/automation_proofs/20261030T173813Z.json。以后其他任务正常推进按保存pointer/本轮commit核验，不回滚共享账户或main。
