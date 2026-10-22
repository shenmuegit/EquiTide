# 原冻结SMA：UTC02→04纯分钟续接

原SMA65±1%、初始BTC1500/ETH500 USDT的75/25原值分仓及2027-03-31终止计划保持。3个新截止配置在取价和计算前分别reserve；部分观察不足180天/六折，因此按真实结果rejected留档，原长期状态仍为collecting。

UTC 2026-10-22T02:00:00Z → 2026-10-22T04:00:00Z，新增120闭合分钟；九场景各保留完整28941点旧前缀并追加至29061点，累计29039分钟/20完整天。

|成本|组合累计净收益|完整采样整体回撤|末值USDT|
|---:|---:|---:|---:|
|1|-4.444547%|9.338833%|1911.1090601516|
|2|-4.598783%|9.367352%|1908.0243466483|
|3|-4.752660%|9.395856%|1904.9467927259|

0新增日决策、参考点或模拟成交；Oct22当日00UTC轮次已完成原规则唯一日决策，不重复。现金、数量、desired、历史交易、费用和最新日决策记录保持，BTC继续持仓、ETH继续现金，不重开、不归一化、不跨币转账、不再平衡、不在本轮截止强平。

源报告 `research/experiments/20261022T022521Z/forward_report.json` SHA256 `6b4af44c42b8dc21698109369e2605d1723898b575a279ee28c3057836fb1a75`；源状态 `research/experiments/20261022T022521Z/forward_state.json` SHA256 `cc6f5468c8357fe4742ba37db7b6dbec91f53ef0bf0d2c8277a33295d8243e46`。原冻结计划 `research/experiments/20261001T113625Z/forward_plan.json` SHA256 `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

两份公开分钟响应各121条，含一个重叠bar。原始gzip字节、URL、实际获取时间、原始/压缩SHA与HTTP成功状态留在provenance；输入毫秒UTC、闭合、连续性、两币时间轴及重叠bar均通过核验。源资产输入本次是直接minute数组，代码也兼容旧1d/1m字典。完全复用上轮mark实现及审计，源码字节未改；实际续接和独立审计均exit0，没有HTTP错误。

下一原日决策 `2026-10-23T00:01:00Z`；此前只从本轮04:00截止追加新闭合分钟。跨该时刻需使用冻结的日决策处理及其滞后20日成本，不可越界只mark；原00UTC轮次完整处理已留档可复用。必须保留本轮source state、费用和完整净值前缀，不重复Oct22决策。

这是延迟取得真实bar的shadow重建，不证明当时参考价可成交，不充当paper10十策略真实公开报价观察，未下真实订单。paper10冻结计划及当前状态只读未改，原浮点会计与历史L2/tick/lot/IOC/容量局限保持。大行情留忽略data，输入与结果SHA及复现路径见data_manifest.json。
离线重放：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T042721Z/forward.py --reproduce`；独立审计同目录audit_forward.py，不联网、不写登记或账户。
