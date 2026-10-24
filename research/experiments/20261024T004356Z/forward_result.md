# 原冻结SMA延迟shadow跨日续接

2026-10-23T22:30:00Z→2026-10-24T00:30:00Z，新增120闭合分钟与1个日决策参考。
组合1/2/3倍累计收益-6.323499795%/-6.475275332%/-6.626698160%。
每日决策：{"BTC": [{"executed_at_utc": "2026-10-24T00:01:00Z", "prior_close": "81189.43000000", "SMA65": "80961.44261538461538461538462", "before_desired_long": true, "desired_long": true, "action": "hold_long", "last_daily_close_available_utc": "2026-10-24T00:00:00Z", "daily_bars": 65, "lagged_daily_quote_ADV": 1170796699.0391934, "lagged_daily_volatility": 0.015192796995793553, "reference_minute_open": 81168.13}], "ETH": [{"executed_at_utc": "2026-10-24T00:01:00Z", "prior_close": "2387.60000000", "SMA65": "2527.045230769230769230769231", "before_desired_long": false, "desired_long": false, "action": "hold_cash", "last_daily_close_available_utc": "2026-10-24T00:00:00Z", "daily_bars": 65, "lagged_daily_quote_ADV": 640532879.734572, "lagged_daily_volatility": 0.020572605436311564, "reference_minute_open": 2386.41}]}
全成本新增虚拟成交数：0
旧完整NAV前缀、cash/units/desired、原交易与成本逐一核对；原2027-03-31终止不变，下一UTC日决策2026-10-25T00:01:00Z。仅未成熟180天/六折的partial观察，不是十策略实时盘。
