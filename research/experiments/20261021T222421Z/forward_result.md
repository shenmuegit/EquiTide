# 原冻结SMA：连续分钟续接

原SMA65±1%、BTC1500/ETH500 USDT原始75/25资金分仓及2027-03-31终止计划保持。3个新截止均先reserve后完成真实续接，finish rejected只因19完整天不足180天/六折资格；原长期状态继续collecting。

UTC 2026-10-21T20:00:00Z → 2026-10-21T22:00:00Z；每币追加120闭合分钟。累计28679分钟，原28580点完整NAV前缀保持，追加后28700点；9场景全部核对。

|成本|组合累计净收益|完整采样整体回撤|末值USDT|
|---:|---:|---:|---:|
|1|-2.750243%|9.338833%|1944.9951366752|
|2|-2.906697%|9.367352%|1941.8660556800|
|3|-3.062789%|9.395856%|1938.7442293012|

0新增日决策、参考点或成交。现金、数量、desired、历史交易和累计成本保持，截止只估值；不强平、不从现金重开、不归一化或再平衡。

源报告 `research/experiments/20261021T202350Z/forward_report.json` SHA256 `eff894c47c74d24b0ca01aeaf8ed072935c1ea5996f5d02c4c746442122fe9a4`；源状态 `research/experiments/20261021T202350Z/forward_state.json` SHA256 `4895c0fb5228bcb5e1ff23e94bbe62c0fc07af1aa3e4d537516aedfcea4dd6a9`。原冻结计划SHA256 `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

两份公开分钟请求各121条，含重叠bar。原始gz响应、URL、真实取得时间、状态200、原始/压缩SHA保存在provenance；毫秒UTC、闭合性、连续性、重叠、完整NAV前缀和nextstate已实际检查。大Parquet保留在忽略data，路径与SHA见data_manifest.json。

延迟取得真实bar的shadow重建不证明当时参考价可成交，不充当paper10十策略真实报价模拟盘。本轮只读paper10冻结计划及账户。保持原浮点数量模型；没有历史L2、真实IOC、过滤器或容量实证，回撤不含分钟内极值。

下轮必需边界：下一原冻结日决策为UTC2026-10-22 00:01。若新截止跨过该时刻，不能把本轮只追加mark的forward.py直接用于越界续接；必须沿用原SMA65±1%和每币每成本当前现金/数量/desired/成本/交易，使用当时已闭合日线与滞后20日成本输入，完成该日唯一决策及必要模拟成交后再追加mark。新截止仍须先reserve，不重置首笔买入。完整日决策续接的既有实现见20261021T102104Z对应代码；本轮不提前执行尚未来到的决策。

forward.py与audit_forward.py实际exit0，见forward_commands.json；分钟请求无错误输出。
离线精确重放：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261021T222421Z/forward.py --reproduce`；独立核验同目录audit_forward.py，均不联网、不写登记或账户。
