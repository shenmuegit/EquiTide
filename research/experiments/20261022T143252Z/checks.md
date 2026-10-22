# 本轮实际检查与留档

轮次20261022T143252Z，工作目录固定/home/desktop/Documents/Codex/EquiTide，分支codex/strategy-research。基点f2909d56708f51a0265a997a93e3249d3ad4f009，fetch实际exit0，启动时本地/远端0 ahead/0 behind。分支锁broker PID1287722持续持有到推送/远端完整树核验之后。

预登记18个基币成交量CMF择时配置及3个原SMA部分观察，全部先reserve成功再计算，均按真实结果finish；主登记追加42行，不重算既有结果或修改已finish报告字节。初始16项均有实际结果；读完整主簿与片段10924事件、5358ID、4062既往规范研究定义及145份既往结论。

实际回测：18配置×3成本=54场景、648逐折、19494日NAV点、19440因果决策、1182成交。精确Fraction生产信号与独立整数/LCM窗口算法的规范比率SHA、阈值和时间全部一致。2920日高低与1460日基币量独立聚合，容差和最大差保留。54条完整OOS分钟收盘及成交后标记整体回撤由初始本金锚定复核；不是逐折最大回撤替代。

三项验证均执行：12连续30日walk-forward、预定10/20/40日与0/.05/.10双轴敏感性、手续费/价差/滑点/量相关冲击1/2/3倍。1/2/3倍4/4/3个净正，18全部rejected。最高1倍ETH40/.10为+21.226711/+20.589162/+19.952521%，3倍回撤17.278909%；1/12正折、2往返、邻域50%失败。保留全部负收益、格边界与18种三成本NAV路径，不能作为独立市场样本。

原SMA65±1%、初始1500/500USDT和75/25冻结分仓不变，12→14UTC120闭合分钟只追加估值；9场景29541点完整旧前缀保持，续至29661点/29639累计分钟/20完整日。0新日线决策/0新成交，下一事件2026-10-23T00:01:00Z。3个部分观察rejected表示180日/六折未成熟，长期收集继续；完整forward_report原字节、forward_state、输入及两份必要原始响应gzip留存。

|实际命令|退出码|日志|
|---|---:|---|
|/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T143252Z/forward.py --reproduce|0|forward_replay.log|
|python3 checks/strategy_registry.py|0|registry_gate.log|
|python3 research/monitor/snapshot.py|0|snapshot.log|
|python3 checks/monitor_snapshot.py|0|monitor_check_final.log|
|git diff --check|0|diff_check.log|

监控3829配置、93观察、10账户；54新成本场景的收益/连续分钟回撤/完整分钟NAV SHA/往返/12折收益与原报告六位显示口径一致，专属结束回归指纹537f5a8fc4b6e58511fabbde15096659e072be117d9a365d3827ac178134c70e仍显示。4个受保护输入SHA未变；无新paper10观察、无重置、无网页重部署。

失败事实：门禁全部真实exit0；额外只读feed结构探查因误用id字段报KeyError/exit1，已原样注明于validation_probe_failure.json，读取真实fingerprint键后完整核验通过；未为此改monitor代码或历史收益。既往轮次失败日志和登记历史保持。

核验后清理54个可重建checkpoint，共2855594字节；本轮未生成bytecode。金融report SHA `bc7f67749e9ea7e78c55be5e81c3a8f84bf8708744efe7e7af94533cd75d117b`；完整forward_report SHA `d4bac590c18872fa28e9d4c8d5a6c12c8647abd9f6228633277ca48d5ccc4ce3`，均与finish一致。必要大JSON原字节优先，不做压缩迁移；原始Parquet留data/normalized既有路径，保留SHA及复现代码，不提交大行情。

完整命令和真实stdout/stderr/退出码见initial_commands.json、research_commands.json、forward_commands.json和final_gates.json。data_manifest.json核对所有本轮证据、源码、源数据、旧账户、原始响应和当前监控哈希。仅本轮目录、主登记与两份监控汇总进入提交；保留既有未跟踪data/normalized。推送后的SHA和完整树以实际终验输出为准，提交前不声称已推送。

限制：重复2025–2026研发历史不是未触碰最终测试集，未计算DSR/PBO；真实历史L2/历史过滤器及实盘成交未验证。CMF是日内收盘区间压力代理，会忽略日间价格缺口；20日延迟shadow不足以证明稳定实盘盈利。

推送过程真实情况：首个研究提交24d633f3e4b5467f32bd08df545d8c318cb72318普通SSH push exit0，SSH ls-remote匹配；随后HTTPS fetch因GnuTLS握手失败exit128，已记录。改用同仓库SSH fetch exit0，HEAD/origin/FETCH_HEAD与完整tree逐字节一致，远端金融报告/forward报告/主登记原字节SHA核验通过。详见push_verification.json。本轻量网络失败/恢复证据另作追加提交，分支锁仍持有至该最终提交的推送/完整树核验后。
