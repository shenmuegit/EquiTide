# 本轮实际检查与留档

轮次20261022T163422Z，固定工作目录/home/desktop/Documents/Codex/EquiTide，分支codex/strategy-research。基点ace615027ebba293ecfd644e0b8c33a522cf6e2a，本轮SSH fetch实际exit0，起始本地/远端0 ahead/0 behind。分支排他锁broker PID1311434持续持有，直到提交、普通SSH push与远端完整tree核验后释放。

预登记18个Ultimate Oscillator水平择时配置及3个原SMA部分观察，全部reserve成功才计算并按真实结果finish；主登记追加42行。旧配置/既有18项CMF未重算，已finish金融报告原字节不修改。初始16项均有实际结果；完整主簿和片段10986事件、5389ID、4080规范研究定义及146份既往结论已读取。

实际回测：18配置×3成本=54场景、648逐折、19494日NAV点、19440因果决策、624成交。生产精确Fraction前缀BP/TR和，独立检查用统一十进制尺度整数逐窗口求和与分母乘积；规范比率SHA、阈值和时间全匹配。2920日高低与1460日基币量独立聚合，容差rtol1e−12/atol1e−8、最大差4.656612873077393e−10。54条初始本金锚定的完整OOS分钟收盘/成交后标记整体回撤独立匹配，不用逐折最大值替代。

三项验证均执行：12连续30日walk-forward；预定基础N7/14/28（周期N/2N/4N）×入场50/55/60双轴敏感性、退出45；手续费/价差/滑点/量相关冲击1/2/3倍。1/2/3倍各3个净正，18全部rejected。最高ETH N28/E55为+26.467011/+26.134670/+25.800065%，3倍整体分钟回撤7.766444%；但仅1/12盈利折、1往返、邻域33.3%，不通过且不降低门槛。保留18种三成本NAV路径与所有负收益，不能作为独立市场样本。4/2/1及除7为指标定义，账户资金权重仍原值1，不归一化。

原SMA65±1%、初始1500/500USDT和75/25分仓未改，14→16UTC仅120闭合分钟估值；9场景29661点完整前缀续至29781点/29759累计分钟/20完整日。0新日线决策/0成交，下一事件2026-10-23T00:01:00Z。3个partial rejected仅表示180日/六折未成熟，长期收集继续；完整forward报告原字节/状态/输入/两份原始响应保留。

|实际命令|退出码|日志|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T163422Z/forward.py --reproduce|0|forward_replay.log|
|python3 checks/strategy_registry.py|0|registry_gate.log|
|python3 research/monitor/snapshot.py|0|snapshot.log|
|python3 checks/monitor_snapshot.py|0|monitor_check_final.log|
|git diff --check|0|diff_check.log|

监控3847配置、94观察、10账户；54新成本场景收益、完整分钟回撤、NAV哈希、往返、12折收益均与原报告六位显示口径一致。专属结束时间回归指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍可见；4受保护输入SHA保持。无新paper10观察或账户重置，无网页重部署。

失败事实：金融计算与全部门禁真实exit0；forward抓取内部一次curl TLS EOF/connect-error35，既有自动重试恢复，整个forward命令真实exit0。未从报错推断失败资产；原始stderr与起止时间在forward_commands.json、forward.log、network_events.json保留。历史失败事实、收益原字节及登记历史未重写。

核验后只清理54个checkpoint，共2651826字节；本轮未生成bytecode。金融report SHA `bc8a344cd41d10fd9f0e70abee84d7c6b6d56de0695b88bfa41498898163aa24`；完整forward报告SHA `8064fcd8f69a6abb7830a7235910d676540e0392e661529ccdf600f4e9247f4d`与finish一致。必要大JSON原字节优先，不做压缩格式迁移；4个原始Parquet留data/normalized原路径，Git只留数据哈希/大小/复现路径，不提交行情。

所有实际命令、stdout/stderr、真实退出码见initial_commands.json、research_commands.json、forward_commands.json及final_gates.json。data_manifest.json最后生成，覆盖本轮产物、源码、源数据、原始响应、原冻结状态及当前监控哈希。仅本轮证据、主登记与两份汇总进入提交；保留既有data/normalized未跟踪项。推送与完整tree核验以真实终验输出为准，不预先声称已推送。

限制：2025–2026历史反复研发，不是未触碰最终测试集，未计算DSR/PBO；历史L2/历史过滤器与实盘执行未验证。UO水平规则不是作者背离策略或真实主动买压观测；20日延迟shadow不足以证明稳定盈利。
