事前拟定的下一批BTC入场阈值.0275/.03/.0325 × ETH趋势滞后2/3/4天已有9格真实结果，next_parameter_availability.json返回空候选；未重算，也不将旧结果当新结果。此补充在本轮结果完成后、任何未来reserve前，按预先写入本脚本绑定的定义优先次序查询，不使用收益排序，不修改本轮代表/参数网格、原账户或原有交接状态。

首个定义可用批次：{"BTC_axis": "lookback_days", "BTC_values": [28, 29, 30], "ETH_axis": "entry_volatility_window_days", "ETH_values": [5, 6, 7], "new_graphs": 4, "old_graphs": 5}。完整来源指纹、其他固定参数、已测/未测格见next_definition_followup.json；下一轮须重新读取完整登记，固定完整spec并reserve成功，才能计算。此处0新策略/账户/现金流评估。
