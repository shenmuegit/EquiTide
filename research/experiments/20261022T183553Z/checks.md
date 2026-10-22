# 本轮实际检查与留档

轮次20261022T183553Z，固定工作目录/home/desktop/Documents/Codex/EquiTide，分支codex/strategy-research。基点b30bf09ecfc5089400634df33d042f95689bd879；本轮SSH fetch真实exit0，起始本地/远端0 ahead/0 behind。排他锁broker PID1332602持续持有到提交、普通SSH push与远端完整tree核验之后。

预登记18个Wilder RSI2趋势内回撤/SMA5反弹退出配置和3个原SMA部分观察，全部先reserve成功后计算并finish；主簿只追加42行。初始16项真实结果均齐备，读完整主簿/片段11048事件、5420ID、4098规范研究定义及147份既往结论。旧Wilder7/14/28和Cutler RSI2与本轮的周期、递推/退出规则不同；不同真实参数合法独立登记。

真实计算18×3=54成本场景，648逐折、19494日NAV点、19440因果决策、714成交。生产Fraction Wilder2递推及快慢SMA前缀和，独立核验用统一十进制尺度整数、2次幂闭式加权及逐窗SMA和；规范RSI比率SHA、SMA和、阈值/实际仓位和时刻匹配。2920日高低、1460日基币量独立聚合通过，基币量rtol1e−12/atol1e−8，最大差4.656612873077393e−10；54条初始本金锚定完整OOS分钟收盘/成交后标记整体回撤匹配。

三项验证均实算：12个连续30日walk-forward；慢趋势SMA100/150/200×RSI2入场10/20/30双轴敏感性，RSI周期2/快退出均线5固定；手续费、价差、滑点和量相关冲击1/2/3倍。净正配置5/4/2，18全部rejected。最佳ETH T150/E20三成本+14.482043/+12.084928/+9.739802%，3倍整体分钟回撤15.100265%、8往返，但仅2/12盈利折、邻域22.2%，不达原门槛。18种三成本NAV路径均保留，不作为独立市场证据；未按最高点调参或放宽门槛。

原SMA65±1%、初始1500/500USDT和75/25资金分仓不变，16→18UTC仅120闭合分钟估值；9场景29781点完整前缀续至29901点/29879累计分钟/20完整日。0新日决策/0成交；下一事件2026-10-23T00:01:00Z。3个真实partial rejected仅表示180日/六折未成熟，长期计划继续；完整forward报告/状态/输入/两份原始响应保持。

|实际命令|退出码|日志|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T183553Z/forward.py --reproduce|0|forward_replay.log|
|python3 checks/strategy_registry.py|0|registry_gate.log|
|python3 research/monitor/snapshot.py|0|snapshot.log|
|python3 checks/monitor_snapshot.py|0|monitor_check_final.log|
|git diff --check|0|diff_check.log|

监控3865配置、95观察、10账户；54新场景收益、连续分钟回撤、NAV哈希、往返、12折收益与原报告六位显示口径一致。专属结束回归指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍在；4受保护输入SHA未变。没有新增paper10观察、重置账户或重部署网页。

失败事实：本轮信号自检、预登记、54场景计算/独立审计、shadow获取/审计/只读重放及两项门禁均真实exit0；forward获取stderr为空，network_events.json的episodes为空，不虚构网络失败，也不覆盖上轮已保存的TLS重试记录。所有淘汰与负收益均保留。

核验后仅清理54个checkpoint，共2935036字节；本轮未生成bytecode。已finish报告原字节SHA `aa277cd8181636e9269f393bb207a616c91053791d955e45354761953da84628`，forward原字节SHA `1bae7aaf8bc5e6428250e579464bea0fd7444021ed94bee8f94780773dd1aabe`与登记一致。必要大JSON不迁移/重编码；4原始Parquet留data/normalized既有路径并保留SHA/大小/复现路径，不提交大行情。

命令真实stdout/stderr/退出码见initial_commands.json、research_commands.json、forward_commands.json及final_gates.json。data_manifest.json最后生成并核对全部产物/源代码/源数据/原始响应/受保护输入/监控SHA。仅本轮目录、主登记及两份监控汇总提交；既有data/normalized未跟踪项保留。推送后的SHA与完整tree以实际终验输出为准，不预先声称已推送。

限制：反复使用2025–2026开发历史，不是未触碰最终留出，未计算DSR/PBO；历史L2/历史过滤器及实盘执行未验证。Wilder2回撤/SMA退出是独立加密资产适配，不复刻来源股票结果；20日延迟shadow不足以证明稳定实盘盈利。
