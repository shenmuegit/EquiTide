# BTC/ETH 日线波动压缩突破：历史回测结果

- 轮次：`20261013T184141Z`；计划在查看结果前冻结，运行了 27 个独立参数定义。
- 结论：**27 个配置均拒绝，0 个通过全部预注册门槛。**这是历史回测，不是实盘行情模拟或实盘盈利证明。
- 假设：波动率处于低分位时若价格收盘突破既往区间，扩张可能延续；测试规则只做多现货。压缩是 10 日收盘收益波动低于前 180 个已完结日波动样本的 10/20/30 分位之一；入场要求最近 3 个已闭合日中出现压缩，并且收盘突破不含比较收盘的 10/20/40 日上轨；退出为不含比较收盘的 10/20/30 日下轨。
- 信号只读前一根已闭合 UTC 日线，执行参考下一日 00:01 UTC 1 分钟开盘。组合是每配置 2,000 USDT，BTC 与 ETH 分别 1,000 USDT 独立资金，不跨币转账、不加杠杆。数据为 Binance 现货 1 分钟 OHLCV，原始规范 Parquet 的 SHA256 见 `data_manifest.json`。
- OOS 时间为 2025-09-19 至 2026-09-14，12 个连续 30 日窗口，窗口间账户状态连续。该日期区间已被此前研究反复使用，**不是未触碰的最终留出集**。本批次在初始 8,559 条登记事件基础上，按查重后的 4,500 个配置指纹核验，新增 27 个配置均先 reserve 后评估。

## 参数网格结果

每行代表一个新登记配置。回撤是 3×成本下 1 分钟收盘价样本及成交参考价样本的最大回撤，不包括分钟内极值。交易成本含每侧 10bp 手续费、1bp 半价差估计、2bp 滑点估计及前 20 个完整 UTC 日 quote ADV / 波动率驱动的平方根冲击；1×/2×/3×同时放大成本项。缺历史 L2，且即刻全额 IOC 只是模拟假设。

|入场天数|退出天数|压缩分位|1×净收益|2×净收益|3×净收益|3×样本回撤|1×正收益折|往返数|邻域3×为正|结论与失败门槛|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
|20|20|10|15.05%|14.00%|12.97%|15.66%|4/12|7|50.0%|拒绝：positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60|
|20|30|10|12.03%|11.01%|10.00%|17.91%|4/12|7|58.3%|拒绝：positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60|
|10|20|10|7.97%|6.85%|5.74%|17.84%|4/12|8|58.3%|拒绝：positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60|
|10|30|30|7.82%|6.57%|5.33%|30.80%|5/12|9|37.5%|拒绝：positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60|
|10|10|10|6.45%|4.79%|3.16%|14.37%|4/12|12|50.0%|拒绝：positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60|
|40|20|10|6.12%|5.44%|4.76%|16.84%|3/12|5|50.0%|拒绝：positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60|
|20|10|10|5.45%|4.20%|2.97%|14.51%|5/12|9|41.7%|拒绝：positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60|
|10|30|10|5.32%|4.22%|3.14%|22.70%|4/12|8|62.5%|拒绝：positive_1x_folds_at_least_8|
|20|30|30|5.09%|3.99%|2.90%|27.17%|5/12|8|25.0%|拒绝：positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60|
|20|30|20|4.93%|3.84%|2.75%|27.17%|5/12|8|50.0%|拒绝：positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60|
|40|30|10|3.66%|2.99%|2.32%|18.67%|3/12|5|62.5%|拒绝：positive_1x_folds_at_least_8|
|10|30|20|1.59%|0.41%|-0.75%|30.97%|5/12|9|58.3%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60|
|20|20|20|1.37%|0.20%|-0.97%|24.48%|4/12|9|40.7%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|40|30|20|0.73%|-0.06%|-0.85%|21.63%|4/12|6|50.0%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|10|10|20|-1.16%|-2.91%|-4.64%|21.88%|4/12|14|33.3%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|10|20|20|-1.56%|-2.80%|-4.03%|27.11%|5/12|10|50.0%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|40|10|10|-2.17%|-2.94%|-3.70%|14.32%|4/12|6|37.5%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|40|20|20|-2.77%|-3.53%|-4.29%|23.30%|3/12|6|38.9%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|10|20|30|-3.05%|-4.44%|-5.79%|31.04%|4/12|11|25.0%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|10|10|30|-3.87%|-5.87%|-7.82%|25.78%|5/12|16|0.0%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|20|10|20|-4.19%|-5.54%|-6.87%|19.92%|5/12|11|27.8%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|40|30|30|-5.20%|-6.06%|-6.91%|26.26%|4/12|7|25.0%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|20|20|30|-5.37%|-6.60%|-7.82%|30.09%|4/12|10|16.7%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|40|10|20|-7.85%|-8.68%|-9.50%|19.60%|4/12|7|25.0%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|40|20|30|-11.89%|-12.81%|-13.72%|29.93%|3/12|8|16.7%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, sampled_1m_drawdown_3x_at_most_25pct, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|20|10|30|-12.29%|-13.78%|-15.25%|24.34%|5/12|13|0.0%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|
|40|10|30|-17.26%|-18.34%|-19.40%|24.65%|3/12|10|0.0%|拒绝：all_cost_scenarios_positive, positive_1x_folds_at_least_8, local_3x_positive_fraction_at_least_0_60, gross_reference_pnl_to_1x_cost_at_least_2_5|

## 结果概要

- 1×成本下 14/27 配置净收益为正，2×为 13/27，3×为 11/27；但所有配置只有 3–5/12 个 1×正收益折，远低于预注册的 8 折门槛。
- 最佳 1× 配置为 `vbreak_e20_x20_q10`：净收益 **15.05%**，2× **14.00%**，3× **12.97%**；3×采样回撤 15.66%，仅 4/12 折为正，邻域 3×正收益比例 50.0%。其回测收益/1×成本约 17.99 倍，但收益折一致性与邻域平台均不足。
- 同期已登记 50/50 BTC/ETH 买入持有比较（复用既有报告，不重新评估）为 1×/2×/3× -40.36%/-40.53%/-40.68%。该基准不是独立最终留出。
- 失败计数（允许多项同时失败）：{"positive_1x_folds_at_least_8": 27, "local_3x_positive_fraction_at_least_0_60": 25, "all_cost_scenarios_positive": 16, "gross_reference_pnl_to_1x_cost_at_least_2_5": 15, "sampled_1m_drawdown_3x_at_most_25pct": 10}。最大 3×样本回撤门槛仍有 17 个配置满足，成本压力与某些局部网格并非主要共同失败原因；核心问题是跨折一致性。

## 三项验证

- **Walk-forward：未通过。** 360 天顺序 OOS 切成 12 个连续 30 日折，所有每日信号只使用已闭合数据，交易状态跨折延续，训练/拟合参数为零；全部 27 组只达到 3–5/12 个 1×正收益折。持续净值和逐折值见 `equity_curves_daily.csv.gz`、`fold_results.csv.gz`。1 分钟样本回撤是分钟收盘及成交参考点采样，不含分钟内极值。
- **Sensitivity：未通过。** 在结果前冻结入场 10/20/40 日 × 退出 10/20/30 日 × 压缩分位 10/20/30 的 3×3×3 网格。27 个全量变体及本地 3×邻域见 `sensitivity.csv`；图见 `sensitivity_surface.svg`。25/27 未达到邻域 3×收益正比例 ≥60%，全部因正收益折不足而拒绝。没有根据 OOS 结果重新挑选或补做参数。
- **Transaction costs：未通过总体稳健性门槛。** 81 个配置×成本场景全部完成，明细在 `cost_scenarios.csv.gz`；3×成本下 11/27 仍为正，但 27/27 都未通过折一致性。1×/2×/3×手续费、点差估计、滑点、平方根冲击同倍率计算；BTC/ETH 独立袖套，没有交叉转账、资金费或借币。

## 评估启动记录

首次启动在加载数据前因滤网快照按 BTC/ETH 而非 BTCUSDT/ETHUSDT 键索引而停止；没有信号计算、订单或局部结果。修正查找键后，使用同一批 27 个已预登记定义完整运行。修复说明保存在 `setup_recovery.json`。

## 复现与证据

- 计划与完整规则：`plan.json`、`specs/`、`batch.json`。
- 数据输入 SHA、滤网规则 SHA、内核 SHA：`data_manifest.json`。
- 注册预留：27 个逐配置 reserve 记录；评估结束后逐个 finish 为 `rejected`，每项有真实完整回测结果。
- 审计：`audit.json`、`audit.log`。核对 4 个源 Parquet 的大小/哈希、连续性、27 个 reserve 状态、81 个成本场景、972 条逐折结果、29,322 个每日权益标记、1,434 个模拟订单事件、信号至执行时序、逐笔费用/余额守恒、数量和参与率限制；结果全部通过工程审计。逐笔明细在 `trade_ledger.csv.gz`，完整 evaluator detail 在 `full_evaluation_report.json.gz`，`report.json` 保留紧凑汇总与全折指标。
- 运行：`.venv/bin/python research/experiments/research/experiments/20261013T184141Z/prepare.py`、`.venv/bin/python research/experiments/research/experiments/20261013T184141Z/evaluate.py`、`.venv/bin/python research/experiments/research/experiments/20261013T184141Z/audit.py`。
- 文献背景仅用于提出假设：[Moskowitz、Ooi 与 Pedersen (2012)](https://doi.org/10.1016/j.jfineco.2011.11.003)；[Shen、Urquhart 与 Wang (2022)](https://onlinelibrary.wiley.com/doi/10.1111/fire.12290)。它们没有验证本轮规则。

截至已有 4,500 个配置指纹与过往多轮的广泛试验，本结果存在明显多重选择偏差。没有一个预注册设置达到通过标准，**不建议将最佳单项从网格中摘出称为稳健候选**。下一轮应选择新的预设方向或更长的新前向观察，而不是继续针对本轮这段历史择优微调。
