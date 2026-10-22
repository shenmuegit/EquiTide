# 本轮真实检查与留档

轮次20261022T223523Z，固定目录/home/desktop/Documents/Codex/EquiTide，研究分支codex/strategy-research，基点4ab682607405dd5e6ce758423b55d62c519e7cc8；本轮初始SSH fetch真实exit0，ahead/behind0/0。排他锁broker PID1375154持续保持到普通SSH push、fresh fetch/ls-remote及远端完整tree核验后释放。

完整读取登记及片段11172事件、5482ID、4134规范研究定义及149份既往结论，初始16项无缺真实结果。按现存目录识别carry.py原隔离账本，较长672/1008/1344h与0.15/0.25/0.35单腿原始敞口为真实新参数，未重算旧8/24/48h或M1配置。

18低频B0候选＋2同窗spot持有基准均独立reserve后实际运行，60成本场景；3个原SMApartial另独立reserve，23定义全部finish。20完整结果gzip原字节含全部小时曲线、成交、资金费和决策；各SHA写在已finish报告。主登记只追加46行，不改历史或伪造无结果重试。

回测真实输入2025-09-16至2026-09-16，现货/永续/小时mark/实际资金费/合约元数据共10Parquet，4个大价格文件仍留既有data路径。成本上下文21日＋3日间隔，无模型拟合/标签或OOS选参；OOS2025-10-10 00:01至2026-09-11 00:01UTC，336日、12连续28日折。

三项验证完成：H×原值单腿f完整3×3网格；全1/2/3倍费用、价差、滑点、两腿独立ADV/波动冲击及实际负资金费支出压力，正资金费收入不放大。单腿f是入场名义额/当时NAV，毛约2f，不归一化；初始5000spot/5000perp隔离，账本不转账、现货无空头或借币，保留现金拒单和1%保证金代理检查。

18候选通过0、淘汰18，净正数2/0/0。1倍最高BTC H1008/F0.35三成本+0.041240/−0.430325/−0.894833%，仅1/12正折、3往返且各成本4030现金拒单，邻域3倍正比0；2/3倍全候选亏损。6候选现金拒单，4候选不足4往返；全部成本/折广度/邻域/安全余量失败事实保留，不能将闲置或拒单造成的较小损失称费用提升改善策略。

60场景全量确定性重放逐项相同，独立核对483900小时NAV点、29030400闭合分钟成交价标记与原子成交后参考；实际资金费符号、毫秒偏移、原数量、隔离现金/保证金、终点空仓匹配。新合成检查验证分钟内资金费归属、初始本金回撤、边界顺序以及终点不读OOS以后mark高点。原小时hh:01开盘参考与新分钟收盘/成交后参考不是严格采样超集，两套回撤分别保留；分钟代理不是一分钟mark或分钟内极值。候选最大分钟DD3.937948%、最大小时DD3.502873%，均低于25%，不改变本轮淘汰。

|实际命令|退出码|日志|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T223523Z/forward.py --reproduce|0|forward_replay.log|
|python3 checks/strategy_registry.py|0|registry_gate.log|
|python3 research/monitor/snapshot.py|0|snapshot.log|
|python3 checks/monitor_snapshot.py|0|monitor_check_final.log|
|git diff --check|0|diff_check.log|

监控3903配置、97观察、10账户；60新场景收益、完整分钟代理回撤、NAV SHA、执行/往返、720逐折收益与小时折回撤均与报告六位口径一致。历史专属结束指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍可见，4受保护输入SHA未变。无paper10新观察、账户重置或网页重部署。

原冻结SMA65±1%、1500/500USDT及75/25不改，20→22UTC只追加120闭合分钟；9场景30021旧点续至30141点、30119累计分钟、20完整日，0新决策/成交。三倍累计−6.021150%；下一原决策2026-10-23T00:01:00Z。3个partial rejected仅资格未成熟，长期计划继续，不是十策略实时报价模拟收益。

失败事实：早期误猜run.py和extension.py路径的sed读取失败，随后按目录列表找到carry.py；外层batch最终exit0来自后续成功命令，成员exit未单独捕获，不能说这两次读成功，见initial_read_failure.json。实际金融计算/合成检查/独立验证均真实exit0。SMA获取内部curl一次TLS EOF/error35报错，经既有重试整个过程exit0，stderr未标资产，不推断失败资产；原报错与时刻/命令见forward.log、forward_commands.json、network_events.json。

必要结果原字节优先：report SHA `47ef2f9f0d06063b7f7d88a6000079cf641b4c90b57fccce43c9a17996ea2b1a`，forward SHA `c2b48c85d133fd545d476714f5807e97de0ef67ea7a574d468a82949a2c2b2aa`，与finish一致；不压缩迁移已finish内容。仅删除60重复checkpoint，共6777815字节；保留20完整gzip结果、23spec、完整SMA账本/状态/两原响应及数据哈希/复现代码。分钟大曲线可由已留存原输入与完整事件精确重建且SHA一致，不提交大行情或重复可建文件。

实际进程命令/退出码/原stdout/stderr在initial_commands.json、research_commands.json、finish_command.json、forward_commands.json及final_gates.json；末尾data_manifest.json核对全部原始输入、程序、产物、旧冻结状态和新汇总哈希。仅本轮目录、主登记和两份汇总提交，保留data/normalized未跟踪项；推送与远端完整tree状态以终验实际输出为准。

限制：反复研究2025–2026开发历史，不是未触碰最终留出，无DSR/PBO结论。历史L2/清算阶梯/真实初始保证金等级及USDT锚风险未校准；冻结元数据和1%维护额为代理、终端缺小时mark用分钟成交高点代理，不证明实际可清算或实盘盈利。
