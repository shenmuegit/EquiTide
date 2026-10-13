#!/usr/bin/env python3
"""Render the frozen 4h reversal experiment summary in Chinese."""
import json
from pathlib import Path

R = Path(__file__).resolve().parent
report = json.loads((R / "report.json").read_text())
audit = json.loads((R / "audit.json").read_text())
configs = report["configs"]
lines = [
    "# BTC/ETH 四小时下跌反转：逐折与交易成本结果",
    "",
    f"- 轮次：`{R.name}`；全部18个策略定义与2个对照均在计算前成功登记。",
    "- 假设来源：De Nicola (2021) 报告 BTC 在1/2/4小时级别存在负的一阶收益自相关，较大价格变动的百分比反转更强；本研究把它作为动机，在 Binance BTC/ETH 现货上作独立规则筛选，不声称复现原论文。",
    "- 结论：18个候选全部 rejected；两个同期买入持有基准用于参照。所有候选的1×/2×/3×成本累计收益都为负，没有达到预设逐折、回撤和邻域门槛的配置。",
    "",
    "## 预设规则与数据",
    "",
    "对每根已闭合 UTC 4小时K线，计算 `close[j]/close[j-1]-1`。空仓时若收益小于等于预设负阈值则买入；成交引用为信号完成后下一根4小时块开始1分钟的 Binance 1分钟开盘。持仓后，当后续4小时收盘回到入场信号收盘价，或达到最长持有根数时卖出；卖出优先，同一决策根不重新买入。所有账户每个资产独立起始2000 USDT、只做多、不加仓/不跨币转账，并在共同终点尝试计成本清仓。",
    "",
    "阈值预设为0.5%、1%、1.5%，最长持有1、2、4根4小时K线；BTC和ETH分别核算。OOS为2025-09-19至2026-09-14 UTC，12个连续30天折，前365天用于暖机/滞后成本输入，边界前留3天embargo。该历史在仓库被反复用于研究，不能称作未触碰最终留出集。输入来自闭合 Binance 1分钟 OHLCV；文件 SHA256 与4小时/日线收盘序列SHA位于 `data_manifest.json`。",
    "",
    "## 策略结果",
    "",
    "回撤采用 OOS 1分钟收盘净值点加每笔成交后的即时参考净值采样，不包含分钟内或逐笔路径。收益含终点持仓估值及所有已计成本。",
    "",
    "|候选|币种|下跌门槛|最长持有|1×净收益|2×|3×|1×采样回撤|3×采样回撤|1×正折/12|1×往返|1×成本USDT|3×正邻域比例|",
    "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
]
for name in report["summary"]["ranking_1x"]:
    c = configs[name]
    s1, s2, s3 = (c["scenarios"][str(m)] for m in (1, 2, 3))
    lines.append(f"|{name}|{c['asset']}|{100*c['entry_drop_fraction']:.2f}%|{c['max_holding_4h_bars']}根|"
                 f"{s1['net_return_pct']:.3f}%|{s2['net_return_pct']:.3f}%|{s3['net_return_pct']:.3f}%|"
                 f"{s1['max_drawdown_pct']:.3f}%|{s3['max_drawdown_pct']:.3f}%|{s1['positive_1x_folds']}/12|"
                 f"{s1['round_trips']}|{float(s1['cost_usdt']):.2f}|{c['neighbor_3x_positive_fraction']:.0%}|")

lines += ["", "### 同期买入持有基准", "",
          "|基准|1×|2×|3×|", "|---|---:|---:|---:|"]
for name, cfg in report["benchmarks"].items():
    lines.append(f"|{name}|{cfg['scenarios']['1']['net_return_pct']:.3f}%|"
                 f"{cfg['scenarios']['2']['net_return_pct']:.3f}%|{cfg['scenarios']['3']['net_return_pct']:.3f}%|")

lines += [
    "",
    "## Walk-forward、敏感性与成本",
    "",
    "- **Walk-forward：**12个连续30天OOS折，账户持仓跨折延续；每折收益与累计净值摘要保存在 `report.json`。候选1×正收益折数为0至6/12；没有候选通过预设的至少6折、最大3×采样回撤25%及成本后正收益门槛。",
    "- **Sensitivity：**同时扫描下跌门槛和持有期（3×3×2个币种，18配置），相邻门槛/持有期构成预定义邻域；所有候选的3×邻域正收益比例为0%，没有成本后正收益平台。未在OOS上择优后再称为独立验证。",
    "- **Costs：**每侧10bp手续费、每侧1bp估算半价差、每侧2bp滑点、基于此前20个完整UTC日波动率及quote ADV的平方根冲击；最大参与率0.1%，冻结 Binance PRICE/LOT/NOTIONAL/PERCENT_PRICE 过滤器及不利tick/数量向下取整。1×/2×/3×分别放大成本项，报告列出各币种/变体成本、费用组成与成交拒绝数。缺少历史L2盘口，价差和冲击是估算；现货只做多，不适用资金费/借币。",
    "",
    "## 核对与复现",
    "",
    f"独立账务/时序/登记审核：`audit.json`，结果 **{'通过' if audit['passed'] else '失败'}**；60个成本场景、每场景361个日净值点、518400个1分钟收盘采样点、12折及源行情SHA已核对。",
    "",
    "复现命令：",
    "",
    "```sh",
    f"./.venv/bin/python research/experiments/{R.name}/evaluate.py",
    f"./.venv/bin/python research/experiments/{R.name}/audit.py",
    "```",
    "",
    "全体18个策略配置均为完整实际回测结果后登记 `rejected`；两个基准也以真实计算结果登记为 `rejected`，均非运行失败。负收益、逐折值、交易账本和成本场景保留在报告及忽略的大型复现目录 `data/runs/`；Git仅提交轻量代码与结果证据。",
    "",
    "## 判定与限制",
    "",
    "更宽的1.5%门槛相对0.5%门槛减少了一些往返，但最好的配置仍为负收益（BTC、1.5%下跌、持有2根4小时K线：1× −21.318%，3× −52.409%，1×仅4/12正收益折）。其回撤与同期持有基准相比没有改善到预设要求。其余配置亏损更大，3×敏感性邻域没有正格。该简单长仓反转不适合在本成本模型下继续保留为候选；重复历史结果不是未来收益保证。",
]
(R / "result.md").write_text("\n".join(lines) + "\n")
print(json.dumps({"result": str(R / "result.md"), "rows": len(configs), "candidate_passed": report["summary"]["candidate_passed"],
                  "candidate_rejected": report["summary"]["candidate_rejected"], "scenes": report["summary"]["cost_scenes"]}, ensure_ascii=False))
