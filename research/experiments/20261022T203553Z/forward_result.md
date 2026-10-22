# 原冻结SMA65±1%连续账户：18→20UTC分钟估值

读取research/experiments/20261022T183553Z/forward_state.json和research/experiments/20261022T183553Z/forward_report.json并核对SHA。原计划SHA `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`；BTC/ETH本金1500/500 USDT及75/25初始资金分仓含义不变，不归一化、不再平衡、不转账。

真实公开Binance闭合1分钟线，从2026-10-22T18:00:00Z续至2026-10-22T20:00:00Z；每资产1根重叠校验加120根新分钟。9成本场景29901点完整旧NAV前缀逐值保持并追加至30021点；累计29999分钟、20完整日。0新日线决策、0参考成交点、0成交，现金/数量/desired/账本/历史成本不变。下一事件 `2026-10-23T00:01:00Z`，原终点2027-03-31不变。

|观察|成本倍数|累计净收益|完整分钟采样回撤|末值USDT|
|---|---:|---:|---:|---:|
|forward_snapshot_BTC|1|-4.042242%|8.267585%|1439.3663696321|
|forward_snapshot_BTC|2|-4.167881%|8.267585%|1437.4817880481|
|forward_snapshot_BTC|3|-4.293250%|8.267585%|1435.6012432551|
|forward_snapshot_ETH|1|-10.705487%|12.990002%|446.4725653815|
|forward_snapshot_ETH|2|-10.938896%|12.990002%|445.3055199740|
|forward_snapshot_ETH|3|-11.171695%|12.990002%|444.1415264848|
|forward_snapshot_combo|1|-5.708053%|9.338833%|1885.8389350135|
|forward_snapshot_combo|2|-5.860635%|9.367352%|1882.7873080221|
|forward_snapshot_combo|3|-6.012862%|9.395856%|1879.7427697399|

三项验证：walk-forward不足180日/六折；不新增SMA前向变体、不改冻结参数；原1/2/3倍交易/成本保留，新增成交0不能证明TCA或实时执行。3个真实partial rejected表示资格未成熟，长期计划继续，不重置或删除负结果。

完整forward_report原字节SHA `024542979f2486794312deccfbd1d02de5c3c00c5bd82ab7886aac6dec1b735b`、forward_state、输入、两份原始HTTP响应gzip、原始/压缩SHA、URL及抓取时刻保留。本轮获取及独立审核实际exit0、stderr为空，network_events.json如实记录；历史网络失败事实不改。9场景旧前缀、同步时间轴和账户连续性匹配。

只读复现：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T203553Z/forward.py --reproduce`；不联网或写登记。

这是延迟真实K线shadow估值，不是paper10十策略实时报价观察或稳定实盘盈利证据。
