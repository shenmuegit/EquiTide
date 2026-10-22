# 本轮实际核验与必要留档

18个Wilder RSI动量配置分别先reserve后实际计算54成本场景，全部finish rejected，result_available=true。三倍成本3项净正，但盈利折数、往返数或邻域不足；ETH28入场60/65的完整三成本分钟NAV相同，仅为两项不同参数配置，不作独立市场证据，分组见path_equivalence.json。全部正负结果保留。

公式自检覆盖Wilder初值/递推、平坦/单向价格、缩放、未来前缀、非法值、动量严格入场和退出等号/缓冲状态。独立闭式指数权重公式、真实持仓状态和UTC时序共19,440条，738笔Decimal余额/成本/步长/tick，54条初始本金锚定连续分钟回撤，648逐折及19,494日净值和全成本NAV哈希精确重放均通过。

原冻结SMA另3个新截止先reserve后捕获实际公开数据。UTC22:00→00:20追加140闭合分钟，并每币执行一次Oct22UTC00:01原规则决策；BTC继续持仓、ETH继续现金，所有成本副本0新模拟成交。每场景原28,700点NAV完整前缀不变，加140分钟与1个日参考点后共28,841点，累计28,819分钟/20完整天；下一原日决策UTC2026-10-23 00:01。账户未重启、未改冻结规则/本金/持仓，原180天/六折未成熟，partial观察finish rejected不取消长期计划。

公开输入4页：每币141分钟bar含重叠、65已闭合日bar；64个日线重叠逐字段相同，日/分钟收盘一致。公开HTTP状态与原始字节哈希保留。完整日续接复用10UTC旧实现，validate/simulate/evaluate/verify函数源码逐字一致，只有源状态、日线重叠来源、截止和读取传输变化。独立audit_forward.py另外核对冻结信号、日线成本输入、余额、完整NAV与nextstate；今天没有新增成交成本校准证据。

下一轮在Oct23UTC00:01前仅续00:20之后真实闭合mark，按实际间隔计算，不假设120分钟；不能重做Oct22决策。本轮forward.py适用于跨日，纯mark用既有追加实现并读当前nextstate，兼容当前资产内含1d/1m字典的输入结构。完整说明见forward_result.md。

initial_commands.json、research_commands.json、forward_commands.json和final_gates.json保留实际returncode/stdout/stderr。候选核验、日续接重放及独立检查、checks/strategy_registry.py、snapshot.py、checks/monitor_snapshot.py、git diff --check均实际exit0，不以cat日志退出码替代。本轮无错误输出，历史失败事实及已finish报告原字节保留。

监控3,703配置/86观察，新18配置54成本场景收益、回撤、逐折及往返数逐值核对；旧exclusive-end别名仍在，paper10及旧源输入SHA不变。核验后只清理54个可重建checkpoint及本轮字节码，完整报告、源状态、冻结spec、4页原始响应、必要输入与复现代码保留。大行情留忽略data并保存路径/SHA；不做格式迁移、真实下单、账户重置、网页重部署或重复定时任务。

提交后普通SSH非强推，fetch/ls-remote及完整tree核验后释放分支broker。
