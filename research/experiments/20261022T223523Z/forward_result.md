# 原冻结SMA65±1%：20→22UTC延续

原计划SHA `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`，BTC/ETH原1500/500USDT、75/25初始分仓、每成本现金/数量/desired/旧交易成本保持，不转账、不再平衡、不重开。

从2026-10-22T20:00:00Z续至2026-10-22T22:00:00Z，每币1根真实重叠校验＋120新闭合分钟。9场景30021点完整旧前缀逐值保持，续至30141点、30119累计分钟、20完整日。0新日线决策/参考点/成交。下次原决策2026-10-23T00:01:00Z，终点2027-03-31不变。

|观察|成本倍数|累计收益|连续分钟采样DD|末值USDT|
|---|---:|---:|---:|---:|
|forward_snapshot_BTC|1|-4.053322%|8.267585%|1439.2001687741|
|forward_snapshot_BTC|2|-4.178946%|8.267585%|1437.3158047991|
|forward_snapshot_BTC|3|-4.304302%|8.267585%|1435.4354771490|
|forward_snapshot_ETH|1|-10.705487%|12.990002%|446.4725653815|
|forward_snapshot_ETH|2|-10.938896%|12.990002%|445.3055199740|
|forward_snapshot_ETH|3|-11.171695%|12.990002%|444.1415264848|
|forward_snapshot_combo|1|-5.716363%|9.338833%|1885.6727341556|
|forward_snapshot_combo|2|-5.868934%|9.367352%|1882.6213247731|
|forward_snapshot_combo|3|-6.021150%|9.395856%|1879.5770036338|

三项验证：不足180日/六折，不改原SMA参数、也不增设新前向变体；原1/2/3倍交易成本保留，新增成交0不证明TCA或实时执行。3个真实partial以rejected finish表示资格未成熟，长期计划继续。

forward_report原字节SHA `c2b48c85d133fd545d476714f5807e97de0ef67ea7a574d468a82949a2c2b2aa`。状态、输入、两份原始响应gzip及原始/压缩SHA、URL、抓取时刻均保留。实际获取/独立审核exit0；内部curl曾有TLS EOF/error35，已有重试恢复，stderr原文留在forward.log/forward_commands.json/network_events.json，不据最终exit0掩盖报错。

只读复现：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T223523Z/forward.py --reproduce`。不联网或写登记。

这是延迟真实K线shadow重建，不是paper10十策略实时报价观察；不下真实订单，不证明稳定盈利。
