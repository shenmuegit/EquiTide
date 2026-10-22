# 原冻结SMA65±1%连续账户：14→16UTC分钟估值

读取research/experiments/20261022T143252Z/forward_state.json与research/experiments/20261022T143252Z/forward_report.json并核对SHA。原计划SHA `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`；BTC/ETH本金1500/500 USDT及75/25初始分仓含义不变，不归一化、不再平衡、不转账。

真实公开Binance闭合1分钟线，从2026-10-22T14:00:00Z续至2026-10-22T16:00:00Z；每资产1根重叠校验加120根新分钟。9个成本场景29661点完整旧NAV前缀逐值保持并追加至29781点；累计29759分钟、20完整日。0新日线决策、0参考成交点、0成交，现金/数量/desired/账本/历史成本完全不变。下一日线事件 `2026-10-23T00:01:00Z`，原终点2027-03-31不变。

|观察|成本倍数|累计净收益|完整分钟采样回撤|末值USDT|
|---|---:|---:|---:|---:|
|forward_snapshot_BTC|1|-3.821701%|8.267585%|1442.6744908541|
|forward_snapshot_BTC|2|-3.947628%|8.267585%|1440.7855779029|
|forward_snapshot_BTC|3|-4.073286%|8.267585%|1438.9007110204|
|forward_snapshot_ETH|1|-10.705487%|12.990002%|446.4725653815|
|forward_snapshot_ETH|2|-10.938896%|12.990002%|445.3055199740|
|forward_snapshot_ETH|3|-11.171695%|12.990002%|444.1415264848|
|forward_snapshot_combo|1|-5.542647%|9.338833%|1889.1470562355|
|forward_snapshot_combo|2|-5.695445%|9.367352%|1886.0910978769|
|forward_snapshot_combo|3|-5.847888%|9.395856%|1883.0422375052|

三项验证：walk-forward仍不足180日/六折；未改变冻结SMA参数或增设前向变体；原1/2/3倍交易/成本持续保留，新增成交0不构成TCA或实时执行证明。3个真实部分观察以rejected finish，表示资格未成熟，长期计划继续，不重置账户或删除负结果。

完整forward_report原字节SHA `8064fcd8f69a6abb7830a7235910d676540e0392e661529ccdf600f4e9247f4d`，forward_state、输入及两份原始HTTP响应gzip均保留。抓取中curl出现一次TLS EOF/connect-error35报错，既有自动重试后整个forward命令实际exit0；原报错在forward.log、forward_commands.json及network_events.json保留，不推断失败资产。原始/压缩SHA、时刻、URL及HTTP200证据保留。9场景、完整旧前缀和同步时间轴独立核验实际exit0，见forward_verification.json。

只读复现：`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T163422Z/forward.py --reproduce`，不联网或写登记。

这是延迟真实K线shadow估值，不是paper10十策略实时报价观察或稳定实盘盈利证据。
