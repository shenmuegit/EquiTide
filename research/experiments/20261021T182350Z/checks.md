# 本轮实际核验与留档

18个Wilder RSI配置分别先reserve后实际运行54成本场景；均finish rejected且result_available=true。11配置全区间未触发交易，完整实际结果为现金/零收益；零收益不计正收益。其余7配置的所有正负收益均保留。

自检覆盖初始均值与递推、平坦/单向走势、缩放、未来前缀、非法价格、严格入场以及RSI/SMA等号退出边界。独立闭式指数加权公式、SMA与真实持仓状态转移、UTC可用时序共19,440条；138笔成交的Decimal余额/成本/数量/价格约束；54条初始本金锚定连续分钟回撤；648个逐折结果与19,494点日净值及全成本NAV哈希精确重放，全部通过。

原冻结SMA另3个新截止先reserve，追加120闭合分钟、0新日决策/成交；9场景保持原28,340点完整NAV前缀与现金/数量/desired/交易/成本。累计28,439分钟、19完整天，后续28,460点NAV和nextstate核对与离线重放通过后finish rejected，仅因不足180天/六折资格，长期计划继续collecting。paper10 plan/state与旧源状态/报告SHA不变。

final_gates.json保存实际命令returncode/stdout/stderr：原SMA重放、checks/strategy_registry.py、snapshot.py、checks/monitor_snapshot.py、git diff --check均真实exit0；不是用cat日志的退出码替代。监控3,649配置/83观察，新18配置54成本场景的收益、回撤、逐折和往返数逐值核对，旧exclusive-end别名仍在，未改历史收益。

可选DOI论文访问返回HTTP429，未取得或使用其内容；一手TA-Lib v0.6.4定义可用。真实访问失败保留在plan.json与report.json的source_access_failures，并在中文结果披露。回测、分钟数据请求和门禁无失败输出。initial_commands.json、research_commands.json、forward_commands.json记录各实际进程退出码。

核验后清理54个可重建checkpoint及本轮字节码缓存。保留已finish报告原字节、完整账户续接、冻结spec、两份原始分钟响应、必要复现输入与代码。原始大Parquet继续留忽略data，路径/SHA见data_manifest.json；不做结果格式迁移、收益改写或账户重置。

仅提交本轮证据、登记追加与两份只读监控汇总；不改网页或重部署、不创建定时任务、不下真实订单。提交后普通SSH非强推，fetch/ls-remote与远端完整tree核验，再释放现有分支broker。
