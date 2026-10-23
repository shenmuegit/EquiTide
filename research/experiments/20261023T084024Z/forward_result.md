# 原冻结SMA：06:30→08:30闭合分钟续接

3个新观察截止先reserve后实际执行、独立审核再finish；完整报告SHA256`47573ca940eb070d21b5ba0266ac09b37eafdea814b702f685df0879b02ee636`，原冻结计划SHA256`2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`。

原SMA65±1%、BTC1500/ETH500原75/25及Float现金/数量核算不变。旧30652点完整NAV前缀保持，各场景追加120个闭合分钟到30772点，累计30749分钟（21完整日＋509分钟）。BTC维持多头、ETH现金，原现金/数量/desired/历史成交与累计成本完全保留；无新日决策/参考点/成交或费用，无重开账户、转账、再平衡或强制卖出。

|成本|累计收益|连续整体DD|累计成本USDT|新增成交|
|---|---:|---:|---:|---:|
|1x|-5.411656%|9.338833%|3.204208|0|
|2x|-5.564625%|9.367352%|6.400993|0|
|3x|-5.717239%|9.395856%|9.590378|0|

Walk-forward仍仅21日部分观察，未成熟180日/六折；3个有真实部分结果的截止登记rejected，不取消长期冻结计划。敏感性为原规则不调参；1/2/3倍成本路径原样保留，不产生额外模拟交易。

两币各121根真实1分钟bar（含1重叠），保留两份原始HTTP响应gzip、输入gzip、URL/取得时间及原始/压缩SHA，核对闭合时间、重叠、完整分钟轴和旧全部NAV前缀。独立audit_forward.py与forward.py --reproduce实际exit0，离线重放不访问HTTP。paper10计划/状态只读；旧延迟shadow不是十策略真实报价模拟。

下一轮从2026-10-23 08:30UTC继续，下一日决策Oct24 00:01UTC，长期终点2027-03-31不变。新截止先reserve，本报告和完整账户状态为下一轮必需输入；已finish报告原字节保持。

复核：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261023T084024Z/forward.py --reproduce`。
