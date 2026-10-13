#!/usr/bin/env python3
"""Render the frozen parameter/cost results as a concise Chinese report."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
r=json.loads((R/'report.json').read_text());names=r['summary']['candidates_ranked_by_1x_return']
def pct(x):return f"{x:.2f}%"
def money(x):return f"{float(x):,.2f}"
lines=[f"# 半小时动量延续研究 — {R.name}","","## 结论","",
"按预登记配置对 BTC/ETH 现货 UTC 小时首半小时动量与同槽成交额过滤做了 360 天历史验证。18 个候选全部 rejected；1×/2×/3×成本下均未有正收益的配置。最好的 1×结果仍分别亏损约 90.8%（BTC）和 91.5%（ETH），所有候选的 1× 12 折里正收益折数均为 0。该方向按冻结失败门槛淘汰，不进入 paper10，也不构成任何实盘盈利结论。","",
"研究动机来自 Shen、Urquhart 与 Wang 对比特币日内时间序列动量的研究：论文报告首半小时对末半小时有预测关系，并提到高成交量/高波动时段更强。本次 UTC 小时首半小时、BTC/ETH、现货成本设置是事先定义的独立适配测试，不是论文复现或论文结论的再验证。[论文 DOI](https://doi.org/10.1111/fire.12290)","",
"## 预登记规则与验证范围","",
"- 每个独立 2,000 USDT 现货账户只做多，不加仓、不借贷、不跨币转账。18 个候选由两币 × 首半小时收益阈值 `{0, 0.05%, 0.10%}` × 同 UTC 小时前 20 个完整日首半小时成交额比率 `{0.75, 1.00, 1.25}` 组成；另有 BTC/ETH 两个买入持有对照。所有 20 个 fingerprint 均在计算前独立 reserve。",
"- 信号在 UTC 小时 H 的 00–29 分钟闭合后可得：`close(H+29)/open(H)-1`。过滤比率只用当前时段之前 20 个完整 UTC 日的同一小时首半小时 quote volume，不含当前日。信号出现后 60 秒，在 H+31 的一分钟开盘虚拟成交；全平仓定于 H+61 开盘，约 30 分钟持有。拒绝的退出每分钟开盘重试，持仓时跳过新信号。没有使用成交持有区间的数据生成入场条件。",
"- 数据为仓库 Binance 现货一分钟历史，UTC 边界 2024-09-16 至 2026-09-16；warm-up 365 天，OOS 2025-09-19 至 2026-09-14（终端执行 00:01），12 个连续、不重叠的 30 天测试折。没有参数拟合。该仓库历史已反复用于研究，因此不是未触碰的最终留出集；存在多重尝试与样本选择偏差。",
"- 成本按每侧手续费 10bp、估计半价差 1bp、滑点 2bp，以及 `0.5 × 前 20 个完整 UTC 日收益标准差 × sqrt(订单 quote 金额 / 前 20 日 quote ADV)` 冲击计算；每项分别按 1×/2×/3× 放大。使用冻结 Binance 价格、数量、名义额与 percent-price filters，步长向下取整，且订单参与率不超过 lagged ADV 的 0.1%。没有历史 L2，因此价差、执行价格与冲击均为估计，不是实际成交。只做现货多头，funding/borrow 不适用。",
"- Walk-forward 用途是报告 12 个连续固定参数 OOS 时间块；敏感性使用预登记的 3×3 两参数网格及相邻网格 3×正收益比例；成本压力使用 1×/2×/3×。这些历史结果只是筛选，不代表可持续前向或实盘表现。","",
"## 候选总表","","按 1× 净收益降序。回撤是 OOS 一分钟收盘及成交后参考价采样回撤，不含分钟内极值。成本列为三档总成本；`拒单` 为 1×/2×/3×分别计数。","",
"| 配置 | 资产 | 1×净收益 | 2×净收益 | 3×净收益 | 1×/3×回撤 | 1×往返 | 1×正折 | 邻居3×正比 | 1×/2×/3×成本 USDT | 拒单 1×/2×/3× | 状态 |",
"|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
for name in names:
 c=r['configs'][name];s=c['scenarios'];one,two,three=(s[x] for x in '123');g=s['gates'];pos=sum(f['net_return_pct']>0 for f in one['folds']);rej='/'.join(str(s[x]['rejected_orders']) for x in '123');costs='/'.join(money(s[x]['cost_usdt']) for x in '123')
 lines.append(f"| `{name}` | {c['asset']} | {pct(one['net_return_pct'])} | {pct(two['net_return_pct'])} | {pct(three['net_return_pct'])} | {pct(one['max_drawdown_pct'])}/{pct(three['max_drawdown_pct'])} | {one['round_trips']} | {pos}/12 | {pct(s['adjacent_3x_positive_fraction']*100)} | {costs} | {rej} | **rejected** |")
lines += ["","## 对照与敏感性","","| 对照配置 | 资产 | 1× / 2× / 3×净收益 | 最大采样回撤（1×） |","|---|---|---:|---:|"]
for n,c in r['configs'].items():
 if c['is_comparator']:
  s=c['scenarios'];lines.append(f"| `{n}` | {c['asset']} | {pct(s['1']['net_return_pct'])} / {pct(s['2']['net_return_pct'])} / {pct(s['3']['net_return_pct'])} | {pct(s['1']['max_drawdown_pct'])} |")
lines += ["","![两参数敏感性图](sensitivity.svg)","","每个候选的全部 12 折、三档成本净收益、采样回撤、Sharpe 与 Calmar 保存于 [fold_results.csv](fold_results.csv)；54 行参数与成本敏感性数据在 [sensitivity.csv](sensitivity.csv)，60 个场景汇总在 [cost_scenarios.csv](cost_scenarios.csv)。完整逐笔交易账本、每日净值和逐分钟净值数组保存在本机忽略目录 `data/runs/20261013T052946Z/`，报告列出可复核的 SHA-256 与路径。","",
"## 失败判据与审计","","要求：三档成本净收益都为正；1×至少 8/12 折为正；3×采样回撤不超过 25%；相邻 3×网格正收益比例至少 60%；1×至少 250 次往返；毛参考 PnL/模型成本至少 2.5；无过滤器/容量/余额拒绝且终端空仓。18 个候选均未通过。虽然最好的若干配置有超过 250 次往返，但毛参考收益本身为负，无法覆盖成本；全候选 1× 正折为 0/12，相邻 3×正收益率为 0%，深度回撤远超 25%，3×还出现由最小名义额导致的拒单。负收益与拒单按完整实测结果保留，没有删除。","",
"审计通过：60 个场景净值数组的 SHA 与长度、有限正值、现金/持仓非负、信号可得后执行、没有早于计划时点的卖出、拒单计数与逐笔账本对账、毛参考盈亏与成本恒等关系。逐分钟回撤只代表存档的分钟收盘/成交后采样，并非分钟内整体最大回撤。","",
"## 复现和来源","","运行顺序：","","```bash\npython3 research/experiments/20261013T052946Z/prepare.py\npython3 research/experiments/20261013T052946Z/evaluate.py\npython3 research/experiments/20261013T052946Z/audit.py\npython3 research/experiments/20261013T052946Z/result.py\npython3 research/experiments/20261013T052946Z/finish.py\n```","","主要输入 SHA-256："]
for a,info in r['data_manifest']['assets'].items():
 for x in info['source_files']:lines.append(f"- `{x['path']}` — `{x['sha256']}` ({x['bytes']} bytes, {x['bars']} bars)")
lines.append(f"- 执行 filters 源 `research/experiments/20261012T035429Z/report.json` — `{r['data_manifest']['filter_source_sha256']}`")
lines += [f"- 预登记执行器 `prepare.py` — `{__import__('hashlib').sha256((R/'prepare.py').read_bytes()).hexdigest()}`",f"- 回测执行器 `evaluate.py` — `{__import__('hashlib').sha256((R/'evaluate.py').read_bytes()).hexdigest()}`","","虚拟历史撮合不是交易所真实订单或实盘成交保证。本轮没有生成实盘成交，也没有修改十策略 paper10 账户。"]
(R/'result.md').write_text('\n'.join(lines)+'\n')
print(f"wrote {R/'result.md'}; best={names[0]} {r['configs'][names[0]]['scenarios']['1']['net_return_pct']:.3f}%")
