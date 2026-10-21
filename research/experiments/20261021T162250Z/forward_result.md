# 原冻结SMA账户：连续分钟续接

本轮沿用原SMA65±1%规则及初始资金BTC1500/ETH500 USDT（原始75/25），不归一化、不重开账户、不再平衡。三项新截止配置均先reserve，使用真实公开已闭合分钟数据续接后独立finish rejected，原因仅为长期观察尚未达到180天/六折资格，原长期计划继续collecting。

续接UTC 2026-10-21T14:00:00Z → 2026-10-21T16:00:00Z；每币120个新闭合分钟，累计28319分钟、19完整天。每场景原28220点完整前缀保持，追加后28340点；9个场景全部核对。

|成本倍数|组合累计净收益|连续采样整体回撤|组合末值USDT|
|---:|---:|---:|---:|
|1|-3.018443%|9.338833%|1939.6311408657|
|2|-3.174546%|9.367352%|1936.5090830218|
|3|-3.330287%|9.395856%|1933.3942647506|

0新增日决策、0新参考点、0新成交；各币各成本现金、数量、desired、历史交易和累计成本保持。下一日决策UTC2026-10-22 00:01，原终止计划2027-03-31不改。不在本轮估值截止强制平仓。

源报告 `research/experiments/20261021T142125Z/forward_report.json` SHA256 `35d7f759ed7458d6cde16ea714a37e1ecdf4113511e144b5b630873b3b1cd862`；源状态 `research/experiments/20261021T142125Z/forward_state.json` SHA256 `ee507fee1d53556627f2b88a134c8a2b6a8a8e8720aceb2fb66babf6ff1ecc13`。冻结原计划SHA256 `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

输入为两个带重叠bar的公开请求，各121行；原始响应gz、URL、真实获取时间、状态、原始和压缩字节SHA保留于provenance。核对重叠bar、UTC毫秒单位、闭合性、连续时间轴、完整NAV前缀与下轮状态。原始大历史行情在忽略的data缓存，源路径及SHA见data_manifest.json。

该账户是取得时间晚于执行参考时间的延迟shadow；不证明当时能够按参考价成交，不充当paper10十策略真实报价模拟盘。无真实订单；paper10冻结计划与账户只读。原浮点数量核算及已有成本约束保持，没有历史L2、真实IOC、过滤器或容量实证；连续采样回撤不含分钟内极值。

本轮forward.py与audit_forward.py实际exit0，详见forward_commands.json与forward_verification.json；无HTTP失败或重试错误输出。离线原字节复现：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261021T162250Z/forward.py --reproduce`；核验同目录audit_forward.py，不联网、不写登记或账户。
