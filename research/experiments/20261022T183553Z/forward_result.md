# 原冻结SMA65±1%连续账户：16→18UTC分钟估值

读取research/experiments/20261022T163422Z/forward_state.json和research/experiments/20261022T163422Z/forward_report.json，逐项SHA一致。原计划SHA `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`；BTC/ETH本金1500/500 USDT及75/25初始资金分仓含义不变，不归一化、不再平衡、不转账。

真实公开Binance闭合1分钟线，从2026-10-22T16:00:00Z续至2026-10-22T18:00:00Z；每资产1根重叠校验加120根新分钟。9个成本场景29781点完整旧NAV前缀逐值保持并追加至29901点；累计29879分钟、20完整日。0新日线决策、0参考成交点、0成交，现金/数量/desired/账本/历史成本不变。下一事件 `2026-10-23T00:01:00Z`，原终点2027-03-31不变。

|观察|成本倍数|累计净收益|完整分钟采样回撤|末值USDT|
|---|---:|---:|---:|---:|
|forward_snapshot_BTC|1|-4.374832%|8.267585%|1434.3775179483|
|forward_snapshot_BTC|2|-4.500035%|8.267585%|1432.4994683344|
|forward_snapshot_BTC|3|-4.624971%|8.267585%|1430.6254415199|
|forward_snapshot_ETH|1|-10.705487%|12.990002%|446.4725653815|
|forward_snapshot_ETH|2|-10.938896%|12.990002%|445.3055199740|
|forward_snapshot_ETH|3|-11.171695%|12.990002%|444.1415264848|
|forward_snapshot_combo|1|-5.957496%|9.338833%|1880.8500833298|
|forward_snapshot_combo|2|-6.109751%|9.367352%|1877.8049883084|
|forward_snapshot_combo|3|-6.261652%|9.395856%|1874.7669680047|

三项验证：walk-forward不足180日/六折；没有新增前向SMA变体或改变冻结参数；原1/2/3倍交易/成本保留，新增成交0不能证明TCA或实时执行。3个真实部分观察rejected表示资格未成熟，长期计划继续，账户不重置、负结果不删除。

完整forward_report原字节SHA `1bae7aaf8bc5e6428250e579464bea0fd7444021ed94bee8f94780773dd1aabe`、forward_state、输入、两份原始HTTP响应gzip、原始/压缩SHA、URL及抓取时刻保留。本轮forward获取及独立审核实际exit0、stderr为空，network_events.json如实记录；此前轮次网络失败事实不改。9场景完整旧前缀、同步时间轴、成本/持仓连续性均匹配。

只读复现：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T183553Z/forward.py --reproduce`；不联网或写登记。

本结果是延迟真实K线shadow估值，不是paper10十策略实时报价观察或稳定实盘盈利证据。
