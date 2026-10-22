# 原冻结SMA65±1%连续账户：12→14UTC分钟估值

读取research/experiments/20261022T123252Z/forward_state.json与research/experiments/20261022T123252Z/forward_report.json，逐项SHA匹配。原计划SHA `2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81`；原始BTC/ETH本金1500/500 USDT及75/25初始分仓含义不变，不归一化、不再平衡、不转账。

真实公开Binance闭合1分钟线，从2026-10-22T12:00:00Z续接至2026-10-22T14:00:00Z；每资产含1根重叠校验加120根新分钟。9个成本场景完整29541点NAV前缀逐值保持并追加至29661点；累计29639分钟、20完整日。0新增日线决策、0参考成交点、0成交，现金/数量/desired/账本/历史成本完全不变。下次日线事件 `2026-10-23T00:01:00Z`，原终点2027-03-31不变。

|观察|成本倍数|累计净收益|全路径分钟采样回撤|末值USDT|
|---|---:|---:|---:|---:|
|forward_snapshot_BTC|1|-3.800129%|8.267585%|1442.9980614936|
|forward_snapshot_BTC|2|-3.926085%|8.267585%|1441.1087248871|
|forward_snapshot_BTC|3|-4.051771%|8.267585%|1439.2234352567|
|forward_snapshot_ETH|1|-10.705487%|12.990002%|446.4725653815|
|forward_snapshot_ETH|2|-10.938896%|12.990002%|445.3055199740|
|forward_snapshot_ETH|3|-11.171695%|12.990002%|444.1415264848|
|forward_snapshot_combo|1|-5.526469%|9.338833%|1889.4706268751|
|forward_snapshot_combo|2|-5.679288%|9.367352%|1886.4142448610|
|forward_snapshot_combo|3|-5.831752%|9.395856%|1883.3649617415|

三项验证：walk-forward仍不足180天/六折；没有新增SMA参数敏感性或修改冻结规则；1/2/3倍原交易及成本持续保留，新增成交为0，无法据此宣称新TCA或实时成交能力。3个真实部分观察均以rejected finish，表示资格未成熟，原长期计划继续，不删除负结果或重置账户。

保留必要的完整forward_report.json原字节SHA `d4bac590c18872fa28e9d4c8d5a6c12c8647abd9f6228633277ca48d5ccc4ce3`，以及forward_state、输入、两份原始HTTP响应gzip和原始/压缩哈希、抓取时刻与URL。全量9场景、旧NAV前缀、时间轴和账户连续性审核实际exit0，见forward_verification.json；冻结后只读重放命令为`PYTHONDONTWRITEBYTECODE=1 /home/desktop/.local/share/equitide-research/worktree/.venv/bin/python research/experiments/20261022T143252Z/forward.py --reproduce`。

本结果为延迟真实K线shadow估值，不是paper10十策略实时报价观察，也不是实时成交或稳定实盘盈利证据。
