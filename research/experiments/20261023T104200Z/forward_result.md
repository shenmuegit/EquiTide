# 原冻结SMA：08:30→10:30闭合分钟续接

3个新截止先reserve后实际执行、独立审核再finish。完整报告SHA256`0cae98c1cbdef05bb1118551218dd3f219c7a766446c055a2ba32af29c3cd2f5`，原冻结计划SHA256`2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

保持原SMA65±1%、BTC1500/ETH500原75/25及Float现金/数量核算。旧30772个NAV点为完整原样前缀，各成本场景仅追加120闭合分钟到30892点，累计30869分钟（21日＋629分钟）。BTC维持多头、ETH现金，旧现金/数量/desired/历史成交/成本完全延续；无新日决策、参考点、成交或费用，不重开账户、转账、调仓或强平。

|成本|累计净收益|连续整体DD|累计成本USDT|新增成交|
|---|---:|---:|---:|---:|
|1x|-5.499914%|9.338833%|3.204208|0|
|2x|-5.652767%|9.367352%|6.400993|0|
|3x|-5.805266%|9.395856%|9.590378|0|

Walk-forward仅21完整日的实际部分观察，未成熟180日/六折，三个截止有真实结果而登记rejected，不取消原长期冻结计划。敏感性为不调参；原1/2/3倍执行路径和成本保持。

两币各121根真实分钟bar（含1重叠），两份原始HTTP响应gzip及输入gzip、URL/取得时间和原始/压缩SHA保留。核对闭合时间、重叠、连续轴、旧全部字段和完整NAV前缀；audit_forward.py和forward.py --reproduce实际exit0。离线重放无新HTTP、无账户或登记写入。原paper10计划/状态不变，旧延迟shadow不是十策略真实报价模拟。

下一轮从2026-10-23 10:30UTC继续，下个日决策2026-10-24 00:01UTC，长期终点2027-03-31不变；每个新截止先reserve，保持此完整报告/状态为下轮必需输入。已finish报告不为压缩重写。

复核：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T104200Z/forward.py --reproduce`。
