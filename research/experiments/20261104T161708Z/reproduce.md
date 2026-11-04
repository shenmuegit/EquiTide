本轮实际回测及已保存证据复核

固定工作目录/home/desktop/Documents/Codex/EquiTide，根目录已核验，只使用main及research/automation/branch.lock。当前37源码中33个在首条reserve前绑定；engine.py与20261104T141637Z整个文件字节一致。新配置是实际BTC入场预算N1000/2000/3000 × 只读ETH间隔D1/3/5；ETH K0.0005/S24/L5/H0.02/E0.005/仅开仓反手趋势门槛/V10/cap0.045固定，BTC原ROC31/H0.04/E0.01不变。

银行BTC3750+ETH15000，总本金18750，原始权重[1,1]相加两条完整银行NAV，不归一化或再乘20/80%资本份额。BTC名义预算占自身银行26.666667/53.333333/80%，占组合5.333333/10.666667/16%；ETH4500占组合24%。不缩放旧数量/NAV/冲击，不克隆银行、转移现金、设置父订单或交叉保证金。三个BTC动量金额组件与三个同N恒定持有组件分别原生计算；三个旧ETH组件只读复用。九个候选组合与三个同本金同预算持有组合对齐分钟/事件共同轴，完整净值计算DD与逐折指标。

实际18个金融定义全部reserve成功（8+8+2）后，唯一一次金融计算命令为research_py -B research/experiments/20261104T161708Z/commands.py evaluate。report存在时run.py拒绝重算。完成后逐项finish，所有正负收益、6个负收益持有对照及负收益折都保留，不重新reserve/evaluate/finish旧定义。10旧实际结果/6原生银行/18成本路径只读。

预登记准备的第一次freeze因family含大写BTC/ETH被fingerprint格式检查拒绝，退出1，无reserve/行情估值。failures/保留失败源码及无效spec，原freeze_commands.json不改退出码；freeze_retry1修正小写后退出0并生成正式定义。TDD_red_receipt.json是合成资金重复加权的预期退出1，不是行情回测。实际命令、UTC、cwd、退出码见*_commands.json、reserve_batches/、finish_batches/、read_failures.json、failure_receipts.json及all_command_receipts.json。原生独立审计不调用simulate/decide/trade，重建数量、费用、冲击、资金费、风险与完整NAV。

当前18原生成本路径包含6660次实际新决策、19980条资金费记录、324笔成交。native_sizing_behavior.json对照旧N500账本，246笔LOT数量与324笔冲击成本不能由旧值线性缩放得到；这是保存结果的描述性核对，不是额外策略试验。原生BTC仅N一维敏感性，父组合联合N/D二维，持有对照不属于策略候选；所有门槛固定，已复用历史不能当未触碰最终/独立未来验证。

```bash
cd /home/desktop/Documents/Codex/EquiTide
research_py=/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python
research_round=research/experiments/20261104T161708Z
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

以上账户复核适用于当前原始main发布状态。若后续共享指针已经前移，旧审计会主动拒绝；不得倒改指针、重采已完成截止或重复模拟下单。原SMA65和single窗口Nov4UTC12:30→14:30；独立L4窗口14:10→16:10，均无新日决策或成交。L4此次实际包含16:00.001结算，按自己原BTC q=-0.006与真实mark/rate逐场景核算，资金费收入不乘成本倍数，ETH零持仓同样记录零现金流；没有复制尚未到16:00的single账户账本。完整原NAV前缀、原规则/本金/数量/risk/context保留。SMA完整日线来源仍为20261104T021133Z/forward_inputs.json.gz；partial不冒充180日/六折，延迟shadow不充当十策略实时报价模拟。

下一single窗口14:30→16:30可能跨16:00，必须先reserve，用其自己的真实响应、原BTC q=-0.012及实际结算ns/rate/mark核算，禁止复制L4现金流。下一L4窗口16:10→18:10须保留已入账16:00结算，不能重计。所有账户不采纳当前研究、不重开现金、不在每轮mark截止强平。

在全部27个ID完成后，同一排他锁内将54条新增journal原字节保存registry_records.jsonl，保留本轮开始main原字节前缀。既有registry._ledger_paths自动读取全部durable分片；归档前后完整timestamp合并索引逐值相同、事件内容与重复次数完全相同，仅物理文件迭代顺序可以变化。registry_fragment_layout.json保存原前缀、分片、拼接流、完整索引和事件多重集SHA256，及before/after计数。旧记录、旧分片与所有新结果均未删除；新配置下一轮仍会被查重拦住。

所有金融/账户检查与真实结果登记完成后，再运行只读snapshot和monitor检查，不额外估值/下单/重部署/新增定时任务。全部短窗API响应、失败TLS尝试、完整packet、账本、冻结规则和核验哈希保留；大行情留在忽略data。本轮仅清理可重建中间物。普通非强制Git push优先，凭据不可用才使用已连接GitHub应用Git Data API、force=false且仅main。最终SHA、完整远端tree/blob核验、实际publisher退出码和解锁后终态保存在.git/automation_proofs/20261104T161708Z.json，不向封存报告追写SHA。
