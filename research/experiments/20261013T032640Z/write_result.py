#!/usr/bin/env python3
"""Render the annual Cutler RSI(2) sensitivity and walk-forward report."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
r=json.load(open(R/"report.json"));prev=json.load(open("research/experiments/20261012T212608Z/report.json"))
lines=[
 f"# RSI(2) 趋势过滤回撤买入：全年12折复核 `{R.name}`",
 "",
 "## 结论",
 "",
 "将已预先测试过的日线 Cutler RSI(2) 规则扩展到完整360天OOS，以核对先前半年样本是否支持参数。18个候选均已成功登记并实际计算；18个全部按预设标准 `rejected`，两个匹配买入持有基准也已完成并登记。没有正收益且满足成本、逐折和敏感性门槛的候选。",
 "",
 "## 冻结规则和时间边界",
 "",
 "逐币种独立2000 USDT、多头现货。Cutler RSI(2) 用最近两个已闭合日收盘变化计算简单均值：RSI=100×平均正变动/(平均正变动+平均绝对负变动)，仅涨为100、仅跌为0、两者均零为50。空仓时 RSI≤5/10/15 且信号日收盘高于包含当日收盘的SMA100/150/200才入场；持仓时 RSI≥50 或收盘≤SMA 时退出，退出优先且同日不重入。每日UTC日线闭合后产生信号，下一UTC日00:01的一分钟开盘作为执行参考。独立账户无杠杆、不互转/再平衡，终点计成本清仓。",
 "",
 "OOS为2025-09-19至2026-09-14 UTC，共360日和12个连续30日折；前365日暖机，并在首折前留3天embargo。此数据区间已反复用于研究，不是未触碰最终留出集。全历史闭合一分钟数据、数据SHA、汇率过滤器快照和成本算法见 `data_manifest.json` 与 `plan.json`。此前183日RSI(2)筛选18项全部拒绝；本轮在看结果前固定同一参数网格并扩展年度边界，未对原半年样本结果择优。",
 "",
 "## 全部配置结果",
 "",
 "收益均为成本后；回撤按连续每日收盘净值加成交参考点采样，未覆盖分钟内或逐tick路径。邻域是同币种相邻RSI门槛/SMA长度的3×3网格，包含中心。",
 "",
 "|候选|币种|RSI入场|趋势SMA|1×净收益|2×|3×|1×/3×采样回撤|1×正折/12|往返数|3×正邻域比例|相对持有基准1×|",
 "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
]
for name in r["summary"]["ranking_1x"]:
 c=r["configs"][name];p=json.load(open(c["spec"]))["parameters"];a,b,d=(c["scenarios"][str(m)] for m in (1,2,3))
 lines.append(f"|{name}|{c['asset']}|{p['entry_rsi']}|{p['trend_sma_days']}|{a['net_return_pct']:+.3f}%|{b['net_return_pct']:+.3f}%|{d['net_return_pct']:+.3f}%|{a['max_drawdown_pct']:.2f}% / {d['max_drawdown_pct']:.2f}%|{a['positive_1x_folds']}/12|{a['round_trips']}|{a['neighborhood_positive_fraction_3x']:.0%}|{c['excess_vs_asset_buy_hold_1x_percentage_points']:+.2f}pp|")
lines += ["","### 同期买入持有对照","","|资产|1×|2×|3×|","|---|---:|---:|---:|"]
for a,c in r["benchmarks"].items():
 lines.append(f"|{a}|{c['scenarios']['1']['net_return_pct']:+.3f}%|{c['scenarios']['2']['net_return_pct']:+.3f}%|{c['scenarios']['3']['net_return_pct']:+.3f}%|")
lines += [
 "",
 "## 三项验证",
 "",
 "- **Walk-forward：**12个30天折，共360天；账户状态连续跨折。单个候选最多仅2/12个1×正收益折，未达预设8/12门槛。全体18个1×结果中BTC为2/9、ETH为4/9为正；2×与3×成本下均为0/18为正。",
 "- **Sensitivity：**预设RSI门槛5/10/15 × SMA100/150/200，共18个两参数配置。3×正收益邻域比例全部0%；正值只落在孤立的1×点，不能当稳健平台。与先前半年结果比较仅用于评估时间扩展影响，没有把该历史描述成独立最终测试集。",
 "- **Costs：**每侧手续费10bp、估算半价差1bp、滑点2bp，冲击为0.5×前20个完整UTC日日收益标准差×sqrt(订单quote预算/前20日quote ADV)，参与率上限0.1%；冻结Binance PRICE/LOT/NOTIONAL规则、不利tick、步长向下取整和5分钟VWAP百分比价格代理。1×/2×/3×放大成本项。没有历史L2盘口，价差与冲击为估计；现货多头无需资金费或借币。",
 "",
 "## 成本与逐折观察",
 "",
 "- BTC 1×累计收益范围−7.725%至+2.067%，所有门槛/SMA配置在2×和3×成本下亏损。最高1×净收益为RSI≤15/SMA100的+2.067%，仅2/12正收益折，3×为−4.159%，邻域正收益比例0%。",
 "- ETH 1×累计收益范围−8.135%至+0.866%，2×/3×全部配置亏损。最高1×配置仅2/12正收益折，3×为−3.311%，邻域正收益比例0%。",
 "- BTC、ETH同期匹配买入持有基准1×分别−34.571%与−46.181%；一些RSI配置在下行样本中相对少跌，但绝对成本后收益与逐折一致性不达标，不据此保留为盈利候选。",
 "",
 "## 审计与复现",
 "",
 "18个候选与2个基准均成功reserve后完成；60个1×/2×/3×场景、361点每日连续OOS净值、源文件SHA、60秒因果执行延迟、逐单Decimal余额/成本和12折连续性均由 `audit.py` 独立核对。原始逐单/逐场景文件留在忽略目录 `data/runs/`。",
 "",
 "```sh",
 f"./.venv/bin/python research/experiments/{R.name}/evaluate.py",
 f"./.venv/bin/python research/experiments/{R.name}/audit.py",
 "```",
 "",
 "最终候选数：0通过 / 18淘汰。历史复用与大量既往配置产生的多重选择偏差仍在；回测不证明前向模拟或实盘稳定盈利。",
]
(R/"result.md").write_text("\n".join(lines)+"\n")
print(json.dumps({"result":str(R/"result.md"),"configs":len(r["configs"]),"passed":r["summary"]["passed"],"rejected":r["summary"]["rejected"],"scenes":r["summary"]["cost_scenes"]},ensure_ascii=False))
