# 长周期 BTC/ETH 日线趋势策略网格（实算）

轮次：`20261012T060005Z`；冻结批次：`2026-10-12T06:00:05Z`。

## 结论

预先登记后实际评估 24 个 SMA 趋势参数配置及 2 个同期持有基准，共 78 个 1x/2x/3x 成本场景。24 个候选全部为 rejected：BTC 和 ETH 在 1x、2x、3x 下均没有净收益为正的配置。没有发现合格正收益新候选。负结果和逐场景证据全部保留。

本区间持有基准也为负。BTC 的 SMA200、±1% 带宽配置 1x/2x/3x 收益为 -4.90%/-5.39%/-5.88%，3x 分钟收盘采样回撤 17.81%；同区间 BTC 持有收益 -34.57%/-34.73%/-34.90%，3x 回撤 54.08%。这是风险/亏损控制线索，不是正收益方法，也未达到预设全成本和逐折门槛。ETH 网格表现更弱。

## 预设规则与时间切分

- 每个配置是单独的 2,000 USDT、现货、只做多账户；全额初始资本作为策略资金，不加杠杆、不转账、不再平衡。
- 在一根 UTC 日线完整收盘后计算过去 N 个已闭合日收盘价的简单均值（窗口包含被比较的最近收盘）。空仓时，收盘高于 SMA×(1+带宽) 入场；持仓时，收盘低于 SMA×(1-带宽) 退出；中间带维持原状态。均线长度 `[150, 200, 250, 300]` 日，带宽 `[0.0, 0.005, 0.01]`。
- 执行参考为下个 UTC 日 00:01 的真实历史 Binance 1 分钟开盘价；前一日线收盘可用时间、执行时间和 60 秒延迟逐笔记录。12 个连续 30 日测试折共 360 天，rolling 365 日历史窗、3 日 embargo。参数冻结，无训练标签；较早数据只用于指标暖机。
- 数据为 BTC/ETH 官方 Binance 现货历史 1 分钟 OHLCV，连续两段共 730 日。历史已经在既往研究中重复使用，属于开发/验证历史，不是独立最终留出。

## 全部候选配置

|资产|SMA日数|对称带宽|1x净收益|2x净收益|3x净收益|3x采样回撤|1x正收益折|模拟成交1x/3x|状态|未通过项|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
|BTC|200|1.00%|-4.90%|-5.39%|-5.88%|17.81%|1/12|4/4|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|200|0.00%|-5.98%|-7.21%|-8.41%|23.10%|1/12|10/10|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|200|0.50%|-11.43%|-12.58%|-13.71%|23.38%|1/12|10/10|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|150|0.00%|-13.33%|-15.13%|-16.88%|27.62%|1/12|16/16|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|150|0.50%|-14.06%|-15.61%|-17.14%|27.84%|1/12|14/14|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|250|1.00%|-15.31%|-15.74%|-16.19%|22.66%|0/12|4/4|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|150|1.00%|-16.66%|-17.95%|-19.23%|25.42%|1/12|12/12|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|300|0.50%|-16.74%|-17.38%|-18.03%|24.37%|0/12|6/6|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|250|0.00%|-17.82%|-18.46%|-19.10%|25.35%|0/12|6/6|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|250|0.50%|-17.82%|-18.46%|-19.10%|25.35%|0/12|6/6|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|300|0.00%|-19.01%|-19.85%|-20.69%|26.82%|0/12|8/8|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|BTC|300|1.00%|-19.02%|-19.64%|-20.27%|26.43%|0/12|6/6|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|150|0.00%|-14.24%|-14.70%|-15.15%|26.60%|1/12|4/4|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|150|0.50%|-14.24%|-14.70%|-15.15%|26.60%|1/12|4/4|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|150|1.00%|-14.24%|-14.70%|-15.15%|26.60%|1/12|4/4|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|200|0.50%|-25.12%|-25.91%|-26.68%|35.95%|1/12|8/8|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|200|0.00%|-28.85%|-29.79%|-30.71%|39.46%|1/12|10/10|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|200|1.00%|-29.26%|-30.01%|-30.74%|39.49%|1/12|8/8|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|250|0.00%|-29.53%|-30.27%|-31.00%|40.08%|1/12|8/8|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|250|0.50%|-31.63%|-32.18%|-32.71%|41.21%|1/12|6/6|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|250|1.00%|-31.63%|-32.18%|-32.71%|41.21%|1/12|6/6|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|300|0.00%|-48.36%|-49.31%|-50.23%|53.84%|0/12|14/14|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|300|0.50%|-51.19%|-52.08%|-52.95%|56.37%|0/12|14/14|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|
|ETH|300|1.00%|-51.53%|-52.17%|-52.79%|56.22%|0/12|10/10|rejected|positive_all_cost_scenarios, at_least_7_of_12_positive_1x_folds, minute_close_sample_DD3_lte25pct, neighbourhood_3x_positive_fraction_gte60pct, gross_reference_pnl_to_cost1_gte2_5|

## 同期持有基准

|资产|1x|2x|3x|3x采样回撤|1x成交数|
|---|---:|---:|---:|---:|---:|
|BTC|-34.57%|-34.73%|-34.90%|54.08%|2|
|ETH|-46.18%|-46.33%|-46.47%|68.19%|2|

## 最佳 1x 参数的逐折净收益

|资产|配置|折1|折2|折3|折4|折5|折6|折7|折8|折9|折10|折11|折12|累计 1x|累计 3x|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|BTC|SMA200 / 1.00%|-8.62%|-0.78%|0.00%|0.00%|0.00%|0.00%|0.00%|0.00%|0.00%|0.00%|0.00%|4.89%|-4.90%|-5.88%|
|ETH|SMA150 / 0.00%|-15.37%|-7.55%|0.00%|0.00%|0.00%|0.00%|0.00%|0.00%|0.00%|0.00%|0.00%|9.62%|-14.24%|-15.15%|

## 敏感性面与成本

**BTC：** 3x 正收益邻域比例 0%；相邻边 17，Sharpe 2σ cliff 4 条。3x 敏感性图见 `sensitivity_surface.svg`。

**ETH：** 3x 正收益邻域比例 0%；相邻边 17，Sharpe 2σ cliff 3 条。3x 敏感性图见 `sensitivity_surface.svg`。

- 每侧手续费 10bp、半价差估计 1bp、滑点估计 2bp，并加 0.5×前 20 个完整 UTC 日样本波动率×sqrt(订单预算/前 20 日 quote ADV) 冲击；参与率上限 0.1%。1x/2x/3x 同倍数放大全部成本。价格/数量步长、最低名义额和交易过滤器使用已留档 Binance exchangeInfo 快照；历史数据没有 L2 报价，价差与滑点属于估计，不能称历史实测盘口成本。
- 现货只做多，资金费与借币不适用。持有基准同样收取入场和终止退出成本。
- 报告的最大回撤使用真实 1 分钟 bar close 路径加交易参考价采样，不含 bar 内极值；折回撤、成本分解、NAV SHA256、每次交易和完整决策均保存在 `report.json`、`results/*.json.gz` 与忽略的大 NAV 文件中。

## 三项验证与淘汰原因

1. **Walk-forward：完成。** 12 个按时间连续的 30 日 OOS 折，365 日 rolling history、3 日 embargo；持仓与现金连续通过各折，折收益连乘精确回到 OOS 总净值。整段历史已重复使用，故不是独立最终验证。
2. **Sensitivity：完成。** 两轴完整网格：SMA lookback 150/200/250/300 日 × 对称阈值 0/0.5/1.0%，BTC 与 ETH 各 12 格。全部变体逐折、逐成本报告；3x 邻域净正比例均为 0%，孤立的正收益峰值不存在。
3. **Costs：完成。** 所有 26 配置（24 候选+2 基准）均实际核算 1x/2x/3x；每个候选 3 档成本后都为负收益。24 个候选因此淘汰；每个具体门槛见 report.json。

## 执行及审计异常记录

实际评估前的首次启动遇到模块搜索路径缺失；第二次输入预检在数据第一天对五分钟 VWAP 做负索引切片，误取了数据尾部。两处均在正式回测计算前修正：复用引擎目录加入模块路径；数据起点不足五根分钟线时不给 warm-up VWAP（交易窗 368 天后，且该项只用于校验，成本仍要求完整 20 日 ADV）。结果汇总首次生成因少导入 `hashlib` 失败；账务独审最初使用严格 Decimal 相等，发现约 1.29e-25 的舍入差，改用 `1e-20` 容差，与成交核算内核一致。每项故障、原因和修正见 `execution_attempts.json` 与日志。它们没有覆盖行情、改策略结果，也没有下真实订单。

## 初始 16 项查重、复现和审计

先读取 `prior_evidence_audit.json`：初始 16 个配置均已找到实际回测证据，本轮没有精确重跑。也读取了 `freqtrade_trial/results/` 的 15 分钟原始回测归档与 BTC/ETH walk-forward 报告；其时间段/周期不替代本轮日线测试。

数据摘要 SHA256 清单见 `data_manifest.json`；本轮 report SHA256：`bf4aefa4acd28729cfe8fa442f7253cffea9693abe83eaa3c2d95bffbe4aba0e`。预登记日志 `reserve.log` 保存 26 次 reserve 成功结果。审计 `audit.json` 独立重算日线信号和现金/币量/费用恒等式，并校验所有分钟净值路径哈希。

复现：
```bash
./.venv/bin/python research/experiments/20261012T060005Z/evaluate.py --reproduce
./.venv/bin/python research/experiments/20261012T060005Z/audit.py
python3 checks/strategy_registry.py
```

没有稳定实盘盈利结论。该批次停止在研究筛选层；若继续验证其他规则，必须作为新配置事前登记。
