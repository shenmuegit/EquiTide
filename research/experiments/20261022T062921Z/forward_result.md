# 原冻结SMA：UTC04→06纯分钟续接

原SMA65±1%、初始BTC1500/ETH500 USDT的75/25原值分仓及2027-03-31终止计划保持。3个新截止配置在取价和计算前分别reserve；部分观察不足180天/六折，因此按真实结果rejected留档，原长期状态仍为collecting。

UTC 2026-10-22T04:00:00Z → 2026-10-22T06:00:00Z，新增120闭合分钟；九场景各保留完整29061点旧前缀并追加至29181点，累计29159分钟/20完整天。

|成本|组合累计净收益|完整采样整体回撤|末值USDT|
|---:|---:|---:|---:|
|1|-4.540488%|9.338833%|1909.1902438700|
|2|-4.694598%|9.367352%|1906.1080426984|
|3|-4.848350%|9.395856%|1903.0329957262|

0新增日决策、参考点或模拟成交；Oct22当日00UTC轮次已完成原规则唯一日决策，不重复。现金、数量、desired、历史交易、费用和最新日决策记录保持，BTC继续持仓、ETH继续现金。不重开、不归一化、不跨币转账、不再平衡、不在本轮截止强平。

源报告 `research/experiments/20261022T042721Z/forward_report.json` SHA256 `0cb57ddc16a80be81d48839dbc4672c7910cbf7ab3941f02941b5dd13a2f6c36`；源状态 `research/experiments/20261022T042721Z/forward_state.json` SHA256 `0501e18455341259fea8ead871a1d15373653dc94ad9fd4ed1608bb5514eb631`。原冻结计划 `research/experiments/20261001T113625Z/forward_plan.json` SHA256 `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

两份公开分钟响应各121条，含一个重叠bar。原始gzip字节、URL、实际获取时间、原始/压缩SHA与HTTP成功状态留在provenance；输入毫秒UTC、闭合、连续性、两币时间轴及重叠bar均通过核验。源资产输入本次是直接minute数组，代码也兼容旧1d/1m字典。完全复用上轮mark实现及审计，源码字节未改；实际续接和独立审计均exit0，没有HTTP错误。

下一原日决策 `2026-10-23T00:01:00Z`；此前只从本轮06:00截止追加新闭合分钟。跨该时刻需使用冻结日决策处理及其滞后20日成本，不可越界只mark；原00UTC轮次完整处理已留档可复用。必须保留本轮source state、费用和完整净值前缀，不重复Oct22决策。

这是延迟取得真实bar的shadow重建，不证明当时参考价可成交，不充当paper10十策略真实公开报价观察，未下真实订单。paper10冻结计划及当前状态只读未改，原浮点会计与历史L2/tick/lot/IOC/容量局限保持。大行情留忽略data，输入与结果SHA及复现路径见data_manifest.json。
离线重放：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T062921Z/forward.py --reproduce`；独立审计同目录audit_forward.py，不联网、不写登记或账户。
