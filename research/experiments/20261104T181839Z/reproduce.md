本轮实际结果及复核

固定cwd=/home/desktop/Documents/Codex/EquiTide，仅main，共用research/automation/branch.lock。当前37源码中33个在首条reserve前绑定；engine.py与20261104T161708Z整个文件字节相同。预设BTC入场N750/1000/1250 × ETH最小斜率K0.00025/0.0005/0.00075，ETH D1固定。其余ETH S24/L5/H.02/E.005/仅开仓反手趋势门槛/V10/cap.045、BTC ROC31/H.04/E.01不变。

原始权重[1,1]是两个完整银行倍数，BTC3750+ETH15000、总18750，资本20/80%；不归一化、不把资本比例再乘NAV。BTC名义预算占组合4/5.333333/6.666667%、占自身银行20/26.666667/33.333333%；ETH4500占组合24%。没有父订单、资金转移、克隆、调仓、交叉保证金或旧NAV/数量/冲击线性缩放。

完整父九格含8新+1旧中心，BTC源三格含1新+2旧，匹配持有父三档含1新+2旧。只新计算BTC1250动量和BTC1250持有两个原生银行，复用所有其他真实组件。实际新增11金融配置：2原生+8候选组合+1持有组合，全部reserve成功（8+3）后唯一执行commands.py evaluate，保存33成本场景。已有report时计算入口拒绝重跑。每个新定义逐个finish；旧中心、旧组件、旧持有不重新reserve/evaluate/finish，原criteria/status/sensitivity与旧报告字节保留。当前邻域诊断另命名，old_center_qualification_preservation.json核对了这一点。

所有正收益、负收益、失败折、成本明细与交易账本保留，15旧实际结果/9原生/27成本路径只读。新原生6成本路径共2220决策、6660资金费记录、108成交；原生独立审计不调用simulate/decide/trade，重建LOT数量、费用、冲击、资金费、现金、风险和完整NAV，父组合逐折/近期/连续DD分别核验。native_sizing_behavior.json只比较保存账本：96笔数量和108笔冲击不能由旧N1000按1.25倍缩放；不是额外策略试验。TDD_red_receipt.json是合成重复资金加权的预期退出1，实际市场回测0。真实命令、cwd、UTC和退出码保存在*_commands.json、reserve_batches/、finish_batches/、all_command_receipts.json及failure_receipts.json。

```bash
cd /home/desktop/Documents/Codex/EquiTide
research_py=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
research_round=research/experiments/20261104T181839Z
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

账户审计对应本轮原始main发布状态。后续共享指针前移时旧审计会拒绝，不应倒改指针、重采已完成截止或重复成交。原SMA65与single本窗Nov4UTC14:30→16:30，独立L4为16:10→18:10。single此次实际16:00.001资金费按自己BTCq=-0.012、真实mark80274.30000000、rate0.00010000逐场景收入0.09632916USDT，收入不乘成本倍数；ETH零持仓保留零现金流。L4的16:00上轮已按自己的BTCq=-0.006处理，此窗不重复，没有复制现金流。三账户无新日决策或成交，完整NAV前缀、原规则/本金/数量/risk/context保持。SMA65完整日线上下文仍是20261104T021133Z/forward_inputs.json.gz。partial不冒充180日/六折，延迟shadow与十策略真实报价观察分开。

5个新组合通过预设历史门槛、3个BTC1250组合未过；旧中心虽在新邻域出现不同诊断，仍保留旧rejected，绝不算新通过。该批由上一轮单点观察启发，已经使用同段历史多次，selection_bias_notes.json明确记录；历史通过不是未触碰最终、独立前向或稳定实盘盈利。三个原冻结账户未采用当前新规则，任何独立前向计划必须另行冻结，不能拿当前旧规则账户观察作这些新组合的前向证据。

所有20个新ID完成后、同一排他锁内，将40条新增journal原字节保存registry_records.jsonl，再保留本轮main开始时原字节前缀。registry._ledger_paths自动读取全部durable分片。归档前后完整timestamp合并索引逐值相同、事件内容和重复次数完全相同；物理文件迭代顺序可以变化。registry_fragment_layout.json保存原前缀、分片、拼接流、完整索引/事件多重集SHA及before/after计数。没有删除任何旧记录、新结果或恢复机会。

全部真实结果与核验后再运行只读snapshot/monitor检查，不额外估值/产生模拟成交/改原账户/部署/建定时任务。完整短窗API响应、完整packet、任何失败尝试、账本和冻结规则保留，大行情仍在忽略data。本轮仅清理可重建中间物。普通非强制Git push优先，凭据不可用才用已连接GitHub Git Data API、force=false且仅main。最终SHA、完整远端tree/blob、实际publisher退出码和解锁后状态保存在.git/automation_proofs/20261104T181839Z.json，不向封存报告追写SHA。
