# 本轮实际检查与留档

轮次20261022T203553Z，固定工作目录/home/desktop/Documents/Codex/EquiTide，研究分支codex/strategy-research。基点342a58272bc41a3b6575e2cb708502b07865c7bf；SSH fetch真实exit0，启动时本地/远端0 ahead/0 behind。排他锁broker PID1353452保留到提交、普通SSH push和远端完整tree核验之后。

预登记18个单日IBS低入高出配置及3个原SMA部分观察，全部reserve成功后才计算并finish；主登记只追加42行。初始16项实际结果完整；读取完整主簿/片段11110事件、5451ID、4116规范研究定义、148份既往结论及旧freqtrade/checks证据。全登记未见IBS定义；本轮单日位置反转与多日RSI回撤或CMF强势入场不同。

真实计算18×3=54成本场景、648逐折、19494日NAV点、19440因果决策、3540成交。生产Fraction(C−L)/(H−L)与独立整数有符号位置变换(1+(2C−H−L)/(H−L))/2的规范比率SHA、阈值/实际仓位和时刻匹配；零振幅0.5约定一致。2920日高低和1460日基币量独立聚合通过，后者rtol1e−12/atol1e−8、最大差4.656612873077393e−10。54条初始本金锚定完整OOS分钟收盘/成交后参考标记整体回撤匹配，不以逐折最大值替代。

三项验证均执行：12连续30日walk-forward；退出IBS0.6/0.7/0.8×入场0.1/0.2/0.3双轴完整网格；手续费/价差/滑点/成交量冲击1/2/3倍压力。净正配置1/0/0，18全部rejected；1倍最高BTC X0.7/E0.1为+3.222187/−1.282616/−5.587440%，3倍整体回撤14.569028%、17往返，但仅5/12正折、3倍邻域0%、毛参考收益/成本比不足2.5。无配置在2/3倍成本下盈利，未放松条件或按OOS加格。18条不同三成本NAV路径和全部负收益保留，不作为独立市场证据。

原SMA65±1%、原1500/500USDT及75/25分仓保持，18→20UTC仅追加120闭合分钟估值；9场景29901点完整旧前缀续至30021点、29999累计分钟、20完整日。0新日决策/0成交；下一事件2026-10-23T00:01:00Z。3个真实partial rejected只表示180日/六折资格未成熟，长期计划继续，不重置账户或强制平仓。完整forward报告、状态、输入与两份原始响应保留。

|实际命令|退出码|日志|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T203553Z/forward.py --reproduce|0|forward_replay.log|
|python3 checks/strategy_registry.py|0|registry_gate.log|
|python3 research/monitor/snapshot.py|0|snapshot.log|
|python3 checks/monitor_snapshot.py|0|monitor_check_final.log|
|git diff --check|0|diff_check.log|

监控3883配置、96观察、10账户；54新场景收益、连续分钟回撤、完整NAV哈希、往返和12折收益与原报告六位显示口径一致。专属结束回归指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍可见；4受保护输入SHA未变。无新paper10观察、账户重置或网页重部署。

失败事实：本轮信号自检、预登记、54场景计算及独立核验、shadow获取/审计/重放及两项门禁均真实exit0。获取stderr为空，network_events.json未虚构失败；旧失败事实及历史收益/登记未改。策略淘汰属于真实负收益和不满足稳健性门槛，不能改成无结果重试。

核验后仅清理54个checkpoint，共3555877字节；本轮未生成bytecode。已finish报告SHA `ffcab8d34fbb50293152de15e64607f1edc11abc01a76a5ac7925bd2b02fac3d`，forward报告SHA `024542979f2486794312deccfbd1d02de5c3c00c5bd82ab7886aac6dec1b735b`均与登记匹配，原字节保留。必要大JSON不迁移/重编码；4原始Parquet留data/normalized既有路径，Git只保留数据SHA/大小/复现路径，不提交大行情。

命令真实stdout/stderr/退出码见initial_commands.json、research_commands.json、forward_commands.json及final_gates.json。data_manifest.json最后生成，覆盖所有本轮产物、源码、源数据、原始响应、冻结状态和监控SHA。仅本轮目录、主登记、两份汇总进入提交，既有data/normalized未跟踪项保留；push及完整tree状态以实际终验输出为准。

限制：2025–2026历史重复开发，不是未触碰最终留出，未计算DSR/PBO；历史L2/历史过滤器及实盘执行未验证。单日IBS忽略前收盘缺口且依赖UTC日边界，不代表真实主动资金流。20日延迟shadow不足以证明稳定实盘盈利。
