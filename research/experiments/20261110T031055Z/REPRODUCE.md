固定工作目录 /home/desktop/Documents/Codex/EquiTide，main；解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python，环境 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。

真实命令、UTC时间、原生退出码见各 *_commands.json、reserve_batches/、finish_batches/ 和 reproduction_history.json。plan.json/specs/ 固定完整规则、数值参数、原始权重、时间与失败判据，36根源及immutable依赖在首次reserve前绑定，之后未改。

本轮M=[2,3,4]×F=[0.00005,0.000075,0.0001]两9格。旧F50ppm三M实际银行和父组合只读；新75/100ppm各6组件+6父组合独立reserve后计算36场景。H0.02/E0.0075/L5/K0.0075/S16/D3/V10/VC0.05固定，代表M3/F75ppm事前确定。整个金融引擎全部函数AST和原字节与上轮一致，仅spec cap数值改变。最新M个实际结算年龄1–36h且available<=signal，中位数按SIGNED率排序，偶数为中间二率均值，缺数阻止新入场。available=settlement+1h是保守假设，非历史网络到达证明。

实际顺序：freeze、真实资金费暖启动/可用源检查、合成正确检查和三个预期退出1的故障注入（重复资金权重、均值替代median、未来费率）、绑定；reserve8+4项；evaluate一次；独立audit现金/LOT/成交/费用/量冲击/资金费/小时风险/完整NAV/逐折/近期，counts/summary/exports/decisions/grid后逐项finish。固定连续370日12×30+10尾和近期40日8×5，不fit/labels/purge/embargo。1/2/3倍执行成本和资金费支出、收入不放大。真实行情路径/字节/哈希见plan、funding_signal_preflight和源manifest。

6组合historical passed保留，但其中5项与旧未过滤H2原有三成本完整NAV相同；唯一不同M3/F75的收益低、整体DD相同，受旧未过滤对照支配。另6ETH组件因近期门槛等rejected。unfiltered_control_comparison.json 与同M旧F50对比保存全部实际标量/路径哈希，不计算新控制策略、不改原资格。参数确实不同和实际等路径并存，不将别名/重复开发历史当独立最终、前向或实盘盈利证明。

SMA/single本窗Nov9 22:30–Nov10 00:30：各自新日决策；single自己的实际00资金费先于原日规则。SMA用原R030420日适配器，首次reserve前仅把PREV切为CURRENT P011054源report/state、DAILY切为上一完整65日R030420以及预期日期Nov10；validate/capture/simulate/evaluate/verify/finish六函数AST和原资金成本/数量逻辑完全一致，证明见original_SMA_rule_source_identity.json。每币新取65个完整SPOT日及121分钟，64日逐字段重叠和末分钟close核验。旧输入asset->minute-array、新输入asset->1d/1m，两结构明确处理，原Floatcash/q/desired/成本/成交和56109点NAV前缀不重置，续至56230。新R/forward_inputs.json.gz为最新完整65SPOT上下文，必须留给下轮。

L4/FEWM本窗00:10–02:10仅mark/risk，原00/daily已各完成一次，不重复。FEWM仅复用同窗真实L4公共市场响应，自己的账本独立。Nov10实际资金费字段来自原R011054真实API响应，本轮原字节只读复用和native0证明，未复制任何账户现金流。所有新观察先reserve、实际capture/advance、独立audit和finish。

下一SMA/single00:30–02:30和L4/FEWM02:10–04:10均仅闭合mark/risk，等参考分钟闭合后才推进；四账户下一日决策Nov11。SMA下轮应在新轮复制并适配P011054的mark-only模板，PREV/源状态指向THIS当前report/state，并从THIS字典输入选1m做重叠。日决策模板本轮R/forward.py留作Nov11跨日参考，未来跨日需新完整65SPOT日，禁止旧context/perpclose/cashrestart/研究参数采用。冻结原计划终止日期均不变，所有观察仍partial、非180日前向资格或十策略实时报价表现。

核验命令（不重新评估策略配置，读取已保存真实证据）：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261110T031055Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261110T031055Z/check_decisions.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261110T031055Z/check_grid_diagnostics.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261110T031055Z/check_exports.py
```

这些审计器生成派生核验JSON。封存后不要覆盖原产物，复核时将派生输出定向至临时存储。registry.reserve对已完成配置返回3，读取旧结果，不以名称/数字格式/组件顺序/metadata规避。完整登记用registry.read_events/read_records读主日志+全部片段。

24ID/48事件保留本轮片段，旧主日志/片段字节、全事件多重集和逻辑索引不改。原生registry门禁与同锁只读monitor生成/检查后封存、commit/push main，独立HTTPS ref、完整远端tree/必要blob和账户链核验后解锁。实际SHA/原生终态见.git/automation_proofs/20261110T031055Z.json。完整原始大行情留忽略data/，Git仅核验必需轻量证据；无真实订单、重部署或新定时任务。
