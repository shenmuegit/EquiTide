# 原冻结SMA账户：连续分钟续接

原SMA65±1%规则、BTC1500/ETH500 USDT原始75/25资金分仓及2027-03-31长期计划保持。3个新截止配置分别先reserve，真实续接后finish rejected，仅因19完整天不足180天/六折资格；长期状态仍为collecting。

UTC 2026-10-21T16:00:00Z → 2026-10-21T18:00:00Z；每币追加120个闭合分钟。累计28439分钟、19完整天。9场景均保留原28340点NAV完整前缀，追加后每场景28460点。

|成本倍数|组合累计净收益|连续采样整体回撤|末值USDT|
|---:|---:|---:|---:|
|1|-2.894313%|9.338833%|1942.1137330652|
|2|-3.050579%|9.367352%|1938.9884247302|
|3|-3.206482%|9.395856%|1935.8703629305|

无新增日决策、参考点或成交；各币各成本现金、数量、desired、交易和累计成本保持。下一决策UTC2026-10-22 00:01。截止仅估值，不强平、不重新从现金开仓、不归一化或再平衡。

源报告 `research/experiments/20261021T162250Z/forward_report.json` SHA256 `d3f6ab2097550e6379b95b319e776b6cb3a70015dc3d0011173c5bfb96c7f2e8`；源状态 `research/experiments/20261021T162250Z/forward_state.json` SHA256 `1f77450b0547ba5612ea65d93d8ac5652125593f63eea71fd18e7aaec3cf8f2e`。原冻结计划SHA256 `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

本轮两个公开分钟请求各121条，包含重叠bar。原始gz响应、URL、获取时间、状态200、原始与gzip字节SHA保存在provenance；重叠、闭合性、毫秒单位、分钟连续性及完整状态/NAV前缀已实际检查。原始大行情留忽略data，路径和SHA见data_manifest.json。

取得时间晚于执行参考时刻，属于延迟shadow重建，无真实订单，不充当paper10十策略真实报价模拟盘。本轮只读paper10冻结计划与状态。保持原浮点数量模型，不声称历史L2、真实IOC、过滤器或容量实证；回撤不含分钟内极值。

forward.py与audit_forward.py命令均实际exit0，stdout/stderr见forward_commands.json；本轮分钟请求没有失败或重试错误输出。
离线精确重放：`/home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261021T182350Z/forward.py --reproduce`；独立检查同目录audit_forward.py。重放不联网、不写登记或账户。
