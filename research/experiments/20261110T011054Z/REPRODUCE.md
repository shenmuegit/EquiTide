本轮工作目录固定 /home/desktop/Documents/Codex/EquiTide，main。解释器 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python；环境 PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1。

完整实际命令、开始/结束时间、原生退出码见各 *_commands.json、reserve_batches/、finish_batches/ 与 reproduction_history.json。code_binding_before_evaluation.json 的36个根源及immutable依赖在首次reserve前冻结，之后未改。plan.json/specs/ 固定全部参数/规则、失败门槛、370日和近期40日边界。funding_signal_preflight.json 保存每个真实决策最新4笔可得历史结算来源，不计算收益。

M=[1,2,3,4]×F=[0,0.00005]两8格：M1是上轮原1–12小时规则的真实最近单笔费率结果，只读2格，不加median元数据；新M2/3/4使用年龄1–36小时且available<=signal的最新M笔SIGNED实际率，中位数奇数取中间、偶数取中间二率均值。缺M笔阻止新开/反手，同向q保留。H0.02/E0.0075/L5/K0.0075/S16/D3/V10/VC0.05固定，代表M3/F0.00005事前确定。数据available=settlement+1h为保守假设，非历史网络到达证据。1/2/3倍实际执行成本与资金费支出，收入不放大。所有真实输入及哈希见计划、源manifest与封存data_manifest.json。

实际顺序：freeze；公开Nov10_00实际结算字段及真实历史暖启动检查；合成正例与三个预期退出1的故障注入（重复资本权重、均值替代中位数、未来费率）；绑定。reserve_batch_0（8项）和_1（4项）成功后evaluate一次，独立audit现金/数量/成交/费用/资金费/小时风险/fullNAV/逐折/近期指标，counts/summary/exports/decisions/grid后逐项finish。所有参数变体、负收益/失败与别名均保留。

原SMA/single本窗20:30–22:30仅闭合mark/risk；L4/FEWM22:10–Nov10 00:10先各自新真实00资金费，再各自00:01日决策；原账户规则/本金/实际q/cash/desired/风险和完整NAV前缀不重置、不采用研究median。每个新观察先reserve再advance/独立audit/finish。FEWM只复用同窗真实L4公共市场响应，自己的账本独立计算。Nov10零点实际fundingTime=1794268800000ms，BTC rate0.00010000/mark75331.44223188，ETH rate0.00006634/mark2134.20490698，原始HTTP响应及时间精度保存。不得把Nov9午夜或Nov9_16.001当本次新00。

下一SMA/single22:30–Nov10 00:30跨自己的新00和00:01；SMA须新实际65个完整SPOT日、原日决策适配器并使用本轮CURRENT source_report/state，不能沿用Nov9旧上下文或永续close。L4/FEWM00:10–02:10只有mark/risk，必须等参考闭合后推进，下一日决策Nov11。原完整SMA65上下文R030420永久留存作核验，不冒充新Nov10上下文。

可核验命令（不重新评估策略，读取真实已存证据）：

```sh
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261110T011054Z/audit.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261110T011054Z/check_decisions.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261110T011054Z/check_grid_diagnostics.py
/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python -B research/experiments/20261110T011054Z/check_exports.py
```

这些旧式审计器会生成自己的派生核验JSON。封存后不得直接覆盖原产物，复核时将派生输出定向到临时存储。registry reserve 对已完成配置返回3，必须读旧结果，不以改名/数字格式/组件顺序或新metadata规避查重。完整登记必须通过 registry.read_events/read_records 读取主日志和全部片段。

24ID/48事件本轮片段保留，旧主日志/片段原字节及事件多重集/逻辑索引不改。原生registry门禁、同锁只读monitor生成与检查后封存、提交main、普通非forcepush、独立HTTPS ref与完整远端tree/必要blob/账户链核验后释放锁。实际推送SHA和原生终态见.git/automation_proofs/20261110T011054Z.json。全部原始大行情保留忽略data/，Git仅必要轻量证据。重复开发历史、多重选择、partial延迟shadow均非独立最终、180日前向资格或稳定实盘盈利；无真实订单、重部署或新定时任务。
