本轮实际结果复核与复现

固定cwd=/home/desktop/Documents/Codex/EquiTide，仅main，共用research/automation/branch.lock。当前37源码中33个在首条reserve前绑定；engine.simulate的AST保持，新的具体规则是趋势门槛仅作用新开仓或反手；K0.00025/0.0005/0.00075 × D1/3/5与旧全持仓门槛逐格匹配，S24/L5/H0.02/E0.005/V10/cap0.045固定。raw[1,1]是两个完整银行的倍数：BTC3750/N500 + ETH15000/N4500，本金18750、资本20/80%、初始名义占比2.6666666667/24%，不归一化、不缩放旧NAV/数量或平均指标，无父级订单/转移/调仓/交叉保证金。

M(i,24)只使用i−24..i−1完整日收盘，beta23/25；s=M(i,24)/M(i−D,24)−1。仅s>K为+1、s<−K为−1，其余及等号0；仅base非零且不同于actual时检查base==gate。base等于已有actual时依原快ROC退出规则保留；base0退出；反手门槛失败只平旧仓且不开相反仓。最多29日过去上下文，源有33日。engine的精确Fraction幂和与audit独立Horner双窗口交叉核验，含严格等号/微扰、未来/窗口外不可见和完整资金/时间轴守恒。

18新配置在任何行情估值前全部reserve成功（8+8+2），只执行一次evaluate。每个新配置都逐项finish；22旧实际结果/12个原生银行/36成本路径只读。相同S/K/D的全持仓门槛对照和本批/跨轮相同NAV路径另存，不把路径别名视为独立alpha。八个真实parquet、源码/spec/report/archive的版本/字节/SHA见plan、code_binding_before_evaluation及data_manifest。反复使用历史不是未触碰最终留出。

所有实际命令、cwd、UTC及退出码保存在*_commands.json、reserve_batches/、finish_batches/和all_command_receipts.json。首次计算命令为：成功运行18次registry.py reserve后，用下方research_py调用当前commands.py evaluate。已存在report时保护性拒绝重算，完成后仅复核保存的数据和账本，不重复reserve/evaluate/finish旧定义。

```bash
cd /home/desktop/Documents/Codex/EquiTide
research_py=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
research_round=research/experiments/20261104T141637Z
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
"$research_py" -B "$research_round/audit.py"
"$research_py" -B "$research_round/check_decisions.py"
"$research_py" -B "$research_round/audit_forward.py"
"$research_py" -B "$research_round/forward.py" --reproduce
"$research_py" -B "$research_round/audit_candidate.py"
"$research_py" -B "$research_round/audit_l4h02.py"
python3 checks/strategy_registry.py
python3 checks/monitor_snapshot.py
```

以上账户审计适用于本轮原始main发布状态。若后续共享指针前移，旧审计会主动拒绝不匹配；保留当前账户，不应倒改指针、重采过去截止或重新下模拟单。当前SMA与single窗口Nov4UTC10:30→12:30，L4为12:10→14:10；原现金/数量/risk/context/完整NAV前缀与冻结计划保持。本窗真实响应和审计均确认无新资金费/日决策/成交，不重复08结算。SMA65完整日线上下文仍为20261104T021133Z/forward_inputs.json.gz。partial不足180日/六折，延迟shadow与十策略真实报价观察分开。

完成全部27个真实ID的reserve/finish后，在同一排他锁内将本轮54条新增journal原字节存为本目录registry_records.jsonl，再原字节保留本轮开始的main前缀。既有registry._ledger_paths自动合并这些durable分片，归档前后完整逻辑索引逐值相同、事件内容及重复次数完全一致；文件迭代顺序会随存放位置改变，不能把列表顺序相等当作历史保持条件。首次手工校验因此退出1，根因/完整原事件多重集及索引复核退出0见read_failures.json与registry_fragment_layout.json；未重新reserve/finish、未重算金融模型/观察。registry_fragment_layout.json保留前缀/分片/拼接流/索引SHA256、事件数与ID数。当前audit_forward和check_sources已在首条reserve前明确使用完整分片视图，当前publisher.verify直接核验真实前缀与本轮分片，无需虚拟字节兼容。旧R10分片和全部历史记录不变。

在封存前完成registry、readonly snapshot和monitor检查，只读已有报告与账户，不额外估值或成交。行情大文件仍在忽略data，完整短窗响应/失败尝试及完整账本、规则、结果均保留。仅清理本轮可重建中间物。按普通非强制Git push优先，认证不可用时使用已连接GitHub应用Git Data API；force=false且只更新main。最终commit/远端完整tree/blob/真实终态与解锁回执存于.git/automation_proofs/20261104T141637Z.json，避免向封存结果追写SHA。

本轮全部54成本场景已实际完成且保存。实际9,990条新原生决策中933次已有仓绕过中性/反向趋势、285次失败反手只平旧仓；gate_scope_behavior.json保存逐场景核对，未引入额外策略配置。所有新原生和新组合最终rejected，原冻结SMA/single/L4独立延续，原始账户账本完整保留。下一L4窗口14:10→16:10可能包含16:00结算，必须按自己真实响应的时间戳、rate、mark、持仓量计算，禁止假设零资金费或复制single现金流。
