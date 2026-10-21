# 原冻结SMA：连续分钟续接

原SMA65±1%、BTC1500/ETH500 USDT初始75/25分仓、2027-03-31终止计划保持。3个新截止均先reserve后完成真实续接，再finish rejected，仅因19完整天不足180天/六折资格；原长期状态继续collecting。

UTC 2026-10-21T18:00:00Z → 2026-10-21T20:00:00Z；每币120个新闭合分钟。累计28559分钟，每场景原28460点完整NAV前缀保持，追加后28580点；9场景全部核验。

|成本|组合累计净收益|完整采样整体回撤|末值USDT|
|---:|---:|---:|---:|
|1|-3.062969%|9.338833%|1938.7406151209|
|2|-3.219014%|9.367352%|1935.6197232541|
|3|-3.374697%|9.395856%|1932.5060684626|

0新增日决策、参考点或成交。现金、数量、desired、历史交易和累计成本保持；下一日决策UTC2026-10-22 00:01。截止只估值，不强平、不从现金重开、不归一化、不再平衡。

源报告 `research/experiments/20261021T182350Z/forward_report.json` SHA256 `202e405775aabc65bf8f061ca946cb94506af2c9e5147289471afb8ea06278b2`；源状态 `research/experiments/20261021T182350Z/forward_state.json` SHA256 `a569341b1643cbd27cddcd7bf6a21aca19488e9de0132578f70ef361ada40eff`。原冻结计划SHA256 `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

两份公开分钟请求各121条，包含重叠bar；原始gz响应、URL、真实获取时间、状态200、原始/压缩SHA留于provenance。已验证毫秒UTC单位、闭合性、连续性、重叠bar、完整NAV前缀和nextstate。大行情保持在忽略data中，路径与SHA见data_manifest.json。

延迟取得真实bar的shadow重建不证明当时参考价可成交，不充当paper10十策略实时报价模拟盘。本轮只读paper10冻结计划及账户。保持原浮点数量模型；没有历史L2、真实IOC、过滤器或容量实证，回撤不含分钟内极值。

forward.py与audit_forward.py实际exit0，见forward_commands.json；本轮分钟HTTP请求无错误输出。
离线精确重放：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261021T202350Z/forward.py --reproduce`；独立检查同目录audit_forward.py，不联网、不写登记或账户。
