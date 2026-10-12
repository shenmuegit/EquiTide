#!/usr/bin/env python3
"""Render the frozen report into a Chinese audit summary and sensitivity surface."""
import hashlib
import json
from pathlib import Path

ROUND = Path(__file__).resolve().parent
r = json.loads((ROUND / "report.json").read_text(encoding="utf-8"))
configs = r["configs"]
candidate_rows = [x for x in configs.values() if not x["is_comparator"]]
comparators = [x for x in configs.values() if x["is_comparator"]]

lines = [
    "# 长周期 BTC/ETH 日线趋势策略网格（实算）",
    "",
    f"轮次：`{r['round']}`；冻结批次：`{r['plan']['frozen_at_utc']}`。",
    "",
    "## 结论",
    "",
    f"预先登记后实际评估 {len(candidate_rows)} 个 SMA 趋势参数配置及 2 个同期持有基准，共 78 个 1x/2x/3x 成本场景。24 个候选全部为 rejected：BTC 和 ETH 在 1x、2x、3x 下均没有净收益为正的配置。没有发现合格正收益新候选。负结果和逐场景证据全部保留。",
    "",
    "本区间持有基准也为负。BTC 的 SMA200、±1% 带宽配置 1x/2x/3x 收益为 -4.90%/-5.39%/-5.88%，3x 分钟收盘采样回撤 17.81%；同区间 BTC 持有收益 -34.57%/-34.73%/-34.90%，3x 回撤 54.08%。这是风险/亏损控制线索，不是正收益方法，也未达到预设全成本和逐折门槛。ETH 网格表现更弱。",
    "",
    "## 预设规则与时间切分",
    "",
    "- 每个配置是单独的 2,000 USDT、现货、只做多账户；全额初始资本作为策略资金，不加杠杆、不转账、不再平衡。",
    f"- 在一根 UTC 日线完整收盘后计算过去 N 个已闭合日收盘价的简单均值（窗口包含被比较的最近收盘）。空仓时，收盘高于 SMA×(1+带宽) 入场；持仓时，收盘低于 SMA×(1-带宽) 退出；中间带维持原状态。均线长度 `{r['plan']['grid']['lookback_days']}` 日，带宽 `{r['plan']['grid']['symmetric_threshold_fraction']}`。",
    "- 执行参考为下个 UTC 日 00:01 的真实历史 Binance 1 分钟开盘价；前一日线收盘可用时间、执行时间和 60 秒延迟逐笔记录。12 个连续 30 日测试折共 360 天，rolling 365 日历史窗、3 日 embargo。参数冻结，无训练标签；较早数据只用于指标暖机。",
    "- 数据为 BTC/ETH 官方 Binance 现货历史 1 分钟 OHLCV，连续两段共 730 日。历史已经在既往研究中重复使用，属于开发/验证历史，不是独立最终留出。",
    "",
    "## 全部候选配置",
    "",
    "|资产|SMA日数|对称带宽|1x净收益|2x净收益|3x净收益|3x采样回撤|1x正收益折|模拟成交1x/3x|状态|未通过项|",
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|",
]
for row in sorted(candidate_rows, key=lambda x: (x["asset"], -x["scenes"]["1"]["net_return_pct"], x["lookback_days"], x["symmetric_threshold_fraction"])):
    s = row["scenes"]
    gates = ", ".join(row["failed_criteria"])
    lines.append(f"|{row['asset']}|{row['lookback_days']}|{row['symmetric_threshold_fraction']:.2%}|{s['1']['net_return_pct']:.2f}%|{s['2']['net_return_pct']:.2f}%|{s['3']['net_return_pct']:.2f}%|{s['3']['max_drawdown_pct']:.2f}%|{row['positive_folds_1x']}/12|{s['1']['executions']}/{s['3']['executions']}|{row['status']}|{gates}|")

lines += ["", "## 同期持有基准", "", "|资产|1x|2x|3x|3x采样回撤|1x成交数|", "|---|---:|---:|---:|---:|---:|"]
for row in comparators:
    s = row["scenes"]
    lines.append(f"|{row['asset']}|{s['1']['net_return_pct']:.2f}%|{s['2']['net_return_pct']:.2f}%|{s['3']['net_return_pct']:.2f}%|{s['3']['max_drawdown_pct']:.2f}%|{s['1']['executions']}|")

lines += ["", "## 最佳 1x 参数的逐折净收益", "", "|资产|配置|" + "|".join(f"折{i}" for i in range(1, 13)) + "|累计 1x|累计 3x|", "|---|---|" + "---:|" * 12 + "---:|---:|"]
for asset in ("BTC", "ETH"):
    row = max((x for x in candidate_rows if x["asset"] == asset), key=lambda x: x["scenes"]["1"]["net_return_pct"])
    folds = row["scenes"]["1"]["folds"]
    lines.append("|" + "|".join([asset, f"SMA{row['lookback_days']} / {row['symmetric_threshold_fraction']:.2%}", *[f"{f['net_return_pct']:.2f}%" for f in folds], f"{row['scenes']['1']['net_return_pct']:.2f}%", f"{row['scenes']['3']['net_return_pct']:.2f}%"]) + "|")

lines += ["", "## 敏感性面与成本", ""]
for asset in ("BTC", "ETH"):
    sens = r["sensitivity"][asset]
    lines.append(f"**{asset}：** 3x 正收益邻域比例 {sens['positive_return_fraction_by_cost']['3']:.0%}；相邻边 {len(sens['adjacent_edges'])}，Sharpe 2σ cliff {sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges'])} 条。3x 敏感性图见 `sensitivity_surface.svg`。")
    lines.append("")

lines += [
    "- 每侧手续费 10bp、半价差估计 1bp、滑点估计 2bp，并加 0.5×前 20 个完整 UTC 日样本波动率×sqrt(订单预算/前 20 日 quote ADV) 冲击；参与率上限 0.1%。1x/2x/3x 同倍数放大全部成本。价格/数量步长、最低名义额和交易过滤器使用已留档 Binance exchangeInfo 快照；历史数据没有 L2 报价，价差与滑点属于估计，不能称历史实测盘口成本。",
    "- 现货只做多，资金费与借币不适用。持有基准同样收取入场和终止退出成本。",
    "- 报告的最大回撤使用真实 1 分钟 bar close 路径加交易参考价采样，不含 bar 内极值；折回撤、成本分解、NAV SHA256、每次交易和完整决策均保存在 `report.json`、`results/*.json.gz` 与忽略的大 NAV 文件中。",
    "",
    "## 三项验证与淘汰原因",
    "",
    "1. **Walk-forward：完成。** 12 个按时间连续的 30 日 OOS 折，365 日 rolling history、3 日 embargo；持仓与现金连续通过各折，折收益连乘精确回到 OOS 总净值。整段历史已重复使用，故不是独立最终验证。",
    "2. **Sensitivity：完成。** 两轴完整网格：SMA lookback 150/200/250/300 日 × 对称阈值 0/0.5/1.0%，BTC 与 ETH 各 12 格。全部变体逐折、逐成本报告；3x 邻域净正比例均为 0%，孤立的正收益峰值不存在。",
    "3. **Costs：完成。** 所有 26 配置（24 候选+2 基准）均实际核算 1x/2x/3x；每个候选 3 档成本后都为负收益。24 个候选因此淘汰；每个具体门槛见 report.json。",
    "",
    "## 执行及审计异常记录",
    "",
    "实际评估前的首次启动遇到模块搜索路径缺失；第二次输入预检在数据第一天对五分钟 VWAP 做负索引切片，误取了数据尾部。两处均在正式回测计算前修正：复用引擎目录加入模块路径；数据起点不足五根分钟线时不给 warm-up VWAP（交易窗 368 天后，且该项只用于校验，成本仍要求完整 20 日 ADV）。结果汇总首次生成因少导入 `hashlib` 失败；账务独审最初使用严格 Decimal 相等，发现约 1.29e-25 的舍入差，改用 `1e-20` 容差，与成交核算内核一致。每项故障、原因和修正见 `execution_attempts.json` 与日志。它们没有覆盖行情、改策略结果，也没有下真实订单。",
    "",
    "## 初始 16 项查重、复现和审计",
    "",
    "先读取 `prior_evidence_audit.json`：初始 16 个配置均已找到实际回测证据，本轮没有精确重跑。也读取了 `freqtrade_trial/results/` 的 15 分钟原始回测归档与 BTC/ETH walk-forward 报告；其时间段/周期不替代本轮日线测试。",
    "",
    f"数据摘要 SHA256 清单见 `data_manifest.json`；本轮 report SHA256：`{hashlib.sha256((ROUND / 'report.json').read_bytes()).hexdigest()}`。预登记日志 `reserve.log` 保存 26 次 reserve 成功结果。审计 `audit.json` 独立重算日线信号和现金/币量/费用恒等式，并校验所有分钟净值路径哈希。",
    "",
    "复现：",
    "```bash",
    f"./.venv/bin/python research/experiments/{ROUND.name}/evaluate.py --reproduce",
    f"./.venv/bin/python research/experiments/{ROUND.name}/audit.py",
    "python3 checks/strategy_registry.py",
    "```",
    "",
    "没有稳定实盘盈利结论。该批次停止在研究筛选层；若继续验证其他规则，必须作为新配置事前登记。",
]
(ROUND / "result.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

width, height = 1220, 430
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         '<rect width="100%" height="100%" fill="#111827"/>',
         '<style>text{font-family:Arial,sans-serif;fill:#f3f4f6}.title{font-size:22px;font-weight:bold}.label{font-size:14px}.cell{font-size:15px;font-weight:bold}</style>',
         '<text class="title" x="30" y="35">3x net return sensitivity (reused historical window)</text>']
lookbacks = [150, 200, 250, 300]
bands = [0.0, 0.005, 0.01]
for panel, asset in enumerate(("BTC", "ETH")):
    x0 = 40 + panel * 590
    parts.append(f'<text class="title" x="{x0}" y="85">{asset}</text>')
    parts.append(f'<text class="label" x="{x0}" y="112">Lookback / band</text>')
    for j, band in enumerate(bands):
        parts.append(f'<text class="label" x="{x0 + 150 + j*125}" y="112">{band:.1%}</text>')
    for i, lookback in enumerate(lookbacks):
        y = 130 + i * 58
        parts.append(f'<text class="label" x="{x0}" y="{y+31}">{lookback}d</text>')
        for j, band in enumerate(bands):
            name = f"sma{lookback}_band{int(band*10000):03d}_{asset}"
            value = configs[name]["scenes"]["3"]["net_return_pct"]
            # All cells are losses in this batch; shade deeper losses darker.
            strength = min(1.0, max(0.0, abs(value) / 55.0))
            red = int(65 + 145 * strength)
            green = int(86 - 38 * strength)
            blue = int(96 - 42 * strength)
            color = f"#{red:02x}{green:02x}{blue:02x}"
            x = x0 + 130 + j * 125
            parts.append(f'<rect x="{x}" y="{y}" width="112" height="45" rx="4" fill="{color}"/>')
            parts.append(f'<text class="cell" x="{x+56}" y="{y+28}" text-anchor="middle">{value:.1f}%</text>')
parts.append('<text class="label" x="40" y="390">All 24 candidates lose at 3x estimated costs; this surface is descriptive, not a deployability claim.</text>')
parts.append('</svg>')
(ROUND / "sensitivity_surface.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")
print("wrote result.md and sensitivity_surface.svg")
