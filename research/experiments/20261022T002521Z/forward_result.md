# 原冻结SMA：跨日决策与连续账户续接

原SMA65±1%、初始BTC1500/ETH500 USDT原始75/25分仓及2027-03-31终止计划保持。3个新截止配置均先reserve，真实续接及两项核验后finish rejected，仅因20完整天不足180天/六折资格；原长期状态继续collecting。

UTC 2026-10-21T22:00:00Z → 2026-10-22T00:20:00Z；每币追加140闭合分钟及1个日决策参考点。9场景均保留旧28700点完整净值前缀，新增141点后共28841点。累计28819分钟、20完整天。

|资产|信号日收盘|SMA65|原目标→新目标|动作|
|---|---:|---:|---|---|
|BTC|84093.42000000|80522.28400000|True→True|hold_long|
|ETH|2473.76000000|2517.720769230769230769230769|False→False|hold_cash|

信号只使用截至UTC2026-10-22 00:00已闭合的65日收盘，执行参考为00:01分钟开盘，保留60秒延迟。BTC继续持仓，ETH继续现金；所有成本副本均0新增模拟成交，原现金、数量、交易和累计成本保持。只是增加独立决策记录与时点，不重复首笔买入、不从现金重启、不归一化或再平衡，不在本轮截止强制平仓。

|成本|组合累计净收益|完整采样整体回撤|末值USDT|
|---:|---:|---:|---:|
|1|-3.252051%|9.338833%|1934.9589715820|
|2|-3.407848%|9.367352%|1931.8430310715|
|3|-3.563284%|9.395856%|1928.7343170305|

源报告 `research/experiments/20261021T222421Z/forward_report.json` SHA256 `95fadeb4b9bfe9cd8a4f98f694df8b69bd628b29539a25cbb72e76f9d3990972`；源状态 `research/experiments/20261021T222421Z/forward_state.json` SHA256 `c8cda1abfd1edfd35b3bebd2aff8b730c55c3a242f57f64f63b50640ee3c0ced`。原冻结计划SHA256 `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

原始公开响应共4页：每币141个分钟bar（含一个重叠bar）、65个已闭合日bar；与10UTC留档日线逐字段核对64个重叠日，并核对新日线收盘与分钟收盘。原始gz响应、真实HTTP状态、URL、获取时间与原始/压缩SHA留于provenance。输入当前格式为每资产含1d和1m字典；旧格式可能是直接分钟数组，均已按类型核验。

复用10UTC既有完整日决策续接：validate/simulate/evaluate/verify四个函数源码逐字一致，见continuation_reuse.json。只调整源账户、日线重叠来源、截止时间及公开读取传输；冻结信号、浮点数量核算、1/2/3倍费用/价差/滑点/前20日波动和quote ADV冲击均未改。独立audit_forward.py另核验日决策、原状态、滞后成本输入、完整净值和下一状态。今日没有新成交，不新增交易成本校准结论。

这是取得时间晚于执行参考时间的延迟shadow重建，无真实订单，也不充当paper10十策略实时公开报价模拟盘。paper10计划/状态只读未改。原模型没有历史L2、真实IOC、tick/lot和容量实证，不加装新规则改变冻结账户；整体回撤限于保存分钟/参考采样，不含分钟内极值。

下一轮必需：最新状态见forward_state.json，下一原日决策为`2026-10-23T00:01:00Z`。在此之前的新截止只追加00:20之后的闭合分钟，按实际间隔计算新增分钟，不假定总是120；不得重复执行Oct22日决策。本轮forward.py为跨日实现；无新日事件时应复用既有只追加mark的实现，审计日期读最新state，并兼容本轮1d/1m字典输入。账户全部历史、冻结规则和原2027-03-31计划保持。

forward capture/evaluate/verify及独立audit均真实exit0，见forward_commands.json、forward_independent_command.json；无HTTP错误输出。
离线重放：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T002521Z/forward.py verify`；独立审计同目录audit_forward.py，均不联网、不写登记或账户。
