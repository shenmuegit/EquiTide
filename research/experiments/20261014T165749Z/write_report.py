#!/usr/bin/env python3
"""Render complete configuration table and 3x sensitivity grid from finalized report."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
ASSETS=('BTC','ETH');ENTRY=(20,40);PERIODS=(14,28,56);MULTS=(2,3,4)
def surface(r):
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1140" height="540" viewBox="0 0 1140 540"><style>text{font-family:Arial,sans-serif;fill:#f7f7f7}.t{font-size:19px;font-weight:bold}.s{font-size:11px;fill:#cbd1d6}.v{font-size:12px;font-weight:bold}</style><rect width="100%" height="100%" fill="#171b20"/>']
 x0=142;y0=95;cw=140;ch=52
 for ai,a in enumerate(ASSETS):
  xx0=x0+ai*555;out.append(f'<text class="t" x="{xx0+2.1*cw}" y="28" text-anchor="middle">{a} — 3× cost return</text>')
  out.append(f'<text class="s" x="{xx0+2.1*cw}" y="53" text-anchor="middle">rows: E=20/40; columns: ATR n=14/28/56; panels split by stop multiple 2/3/4</text>')
  for eidx,e in enumerate(ENTRY):
   for midx,m in enumerate(MULTS):
    yy=y0+(eidx*3+midx)*ch
    out.append(f'<text class="s" x="{xx0-8}" y="{yy+31}" text-anchor="end">E{e}, M{m}</text>')
    for nidx,n in enumerate(PERIODS):
     c=r['configs'][f'atr_trailing_{a}_E{e}_N{n}_M{m}'];v=c['scenarios']['3']['net_return_pct'];color='#208052' if v>=10 else '#42a875' if v>=0 else '#b94c44' if v>-30 else '#812f35';x=xx0+nidx*cw
     out.append(f'<rect x="{x}" y="{yy}" width="{cw-5}" height="{ch-4}" rx="4" fill="{color}"/><text class="v" x="{x+(cw-5)/2}" y="{yy+28}" text-anchor="middle">{v:+.2f}%</text>')
 out.append('<text class="s" x="25" y="525">Complete parameter grid shown; no OOS winner selected. All windows are previously reused development data.</text></svg>')
 (R/'sensitivity_surface.svg').write_text(''.join(out))
def main():
 p=R/'report.json';r=json.loads(p.read_text());r['registry_fragment']='research/experiments/'+R.name+'/registry_records.jsonl';r['implementation_attempts']='research/experiments/'+R.name+'/implementation_attempts.jsonl';p.write_text(json.dumps(r,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 s=r['summary'];names=s['ranked_by_1x_net_return'];best=r['configs'][names[0]];b=[best['scenarios'][str(k)] for k in (1,2,3)]
 lines=['# BTC/ETH 日线突破 + Wilder ATR 跟踪退出：历史回测', '',
 f"- 轮次 `{R.name}`；规则、参数网格、边界、成本与淘汰标准在首次计算前冻结于 `plan.json`，SHA256 `{r['frozen_plan_sha256']}`。",
 '- 使用 Binance 归档现货历史行情回测，不是本轮实时行情模拟或实盘成交。2025–2026 OOS区间已被反复用于仓库策略研究，不是未触碰的最终留出集。',
 '- 初始16个策略条目先前已有实际回测证据，缺失数为0；本轮未重测旧配置。',
 '','## 规则与动机','',
 '将Wilder ATR作为固定入场波动尺度，测试波动率归一化的趋势退出。ATR定义遵循TA-Lib公开实现：[ATR source](https://github.com/TA-Lib/ta-lib/blob/main/src/ta_func/ta_ATR.c)。该指标定义用于精确复现，不代表ATR策略有收益。',
 '',
 '每个BTC或ETH配置都是独立2,000 USDT长仓现金账户。空仓时，仅当已闭合日线收盘严格高于不含信号日的前E日最高价时入场；E∈{20,40}。入场信号日计算true range与Wilder ATR：TR=max(H−L,|H−前收盘|,|L−前收盘|)，前n个完整TR简单均值作种子，之后ATR=((n−1)×前ATR+TR)/n。入场时冻结ATR_entry和信号收盘峰值。此后每个已闭合日更新峰值=max(前峰值,当日收盘)，止损位=max(前止损位,峰值−M×ATR_entry)，M∈{2,3,4}；当收盘≤止损位时，于下个UTC日00:01分钟开盘退出。止损在日线收盘确认，不是日内触发保证。未在同日重入；OOS末端未平仓仓位按预定终点参考价计成本平仓。无杠杆、空头、借币、现金利息或跨账户转移。',
 '',
 '## 数据与验证','',
 '- 数据：BTCUSDT/ETHUSDT Binance现货1分钟OHLCV聚合为UTC日线OHLC与quote ADV；检查输入SHA、UTC连续性、已闭合分钟、每日1,440条、OHLC逻辑及正价格。输入期2024-09-16至2026-09-16，OOS期2025-09-19 00:01至2026-09-14 00:01 UTC，共360天。详情见 `data_manifest.json`。',
 '- Walk-forward：12个连续、不重叠30天窗口，账户和ATR状态跨窗口连续，不按折重置，也不拟合或选择参数；首折前365天暖机及3天embargo。逐折结果和全OOS连续分钟收盘净值采样最大回撤留档。回撤不包含分钟内极值。',
 '- 信号只用闭合日线；成交引用为信号可用60秒后的下一UTC日00:01历史分钟开盘，不等于真实交易所接单。历史L2盘口/历史过滤器不可用，按本轮公开GET `exchangeInfo` 快照、5分钟前置VWAP过滤器代理估算。',
 '',
 '## 成本与敏感性','',
 '- 每侧手续费10bp、估算半价差1bp、滑点2bp，另加前20个完整UTC日样本波动率/quote ADV平方根冲击。参与率≤0.1%，按当前PRICE_FILTER不利tick取整、LOT_SIZE向下取量、NOTIONAL及PERCENT_PRICE_BY_SIDE代理检验；成本假设统一按1×/2×/3×放大。',
 '- 36个参数配置来自BTC/ETH × 入场20/40日 × Wilder ATR 14/28/56日 × 止损倍数2/3/4。敏感性邻域逐轴取相邻参数（含中心）；所有变体均先reserve后计算。',
 '',
 '## 结果与淘汰','',
 f"- 36个配置全部 `rejected`，通过0。1×/2×/3×成本净收益为正的配置数分别 `{s['positive_configs_by_cost']['1']}` / `{s['positive_configs_by_cost']['2']}` / `{s['positive_configs_by_cost']['3']}`。没有任何配置达到8/12个正收益折，整体3×局部邻域正收益配置比例为 `{s['global_3x_positive_neighbor_fraction']:.1%}`。",
 f"- 最佳1×净收益配置 `{best['name']}`：1×/2×/3× `{b[0]['net_return_pct']:.3f}% / {b[1]['net_return_pct']:.3f}% / {b[2]['net_return_pct']:.3f}%`，1×正折`{b[0]['positive_folds']}/12`，3×采样回撤`{b[2]['max_drawdown_1m_sampled_pct']:.2f}%`，仅`{b[0]['round_trips']}`个往返，邻域3×正收益比例`{best['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}`。它虽跨成本保持正净收益，但样本交易少、正收益集中于少数窗口、局部参数面不稳，因此拒绝。",
 '- 同区间BTC/ETH持有净值仅复用 `research/experiments/20261014T084051Z/report.json`；用作描述性基准，不改变上述门槛。',
 '- 该OOS和参数搜索历史已反复研究，不报告独立最终留出、DSR/PBO或实盘稳定收益。',
 '',
 '## 完整网格结果','',
 '|配置|资产|E日|ATR n|M|1×|2×|3×|1×正折/12|1×/3×采样回撤|1×往返|邻域3×正比例|结论|','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
 for n in names:
  c=r['configs'][n];x=[c['scenarios'][str(k)] for k in (1,2,3)];lines.append(f"|{n}|{c['asset']}|{c['entry_lookback_days']}|{c['atr_period']}|{c['stop_multiple']}|{x[0]['net_return_pct']:+.2f}%|{x[1]['net_return_pct']:+.2f}%|{x[2]['net_return_pct']:+.2f}%|{x[0]['positive_folds']}/12|{x[0]['max_drawdown_1m_sampled_pct']:.1f}% / {x[2]['max_drawdown_1m_sampled_pct']:.1f}%|{x[0]['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{c['status']}|")
 lines+=['','','## 复现与审计','','- `.venv/bin/python research/experiments/'+R.name+'/reproduce.py`可本地、不联网重放全部108个策略/成本场景。审计核对36组fingerprint、108成本结果、逐折净值、minute-close NAV hashes、成交时间、费用守恒、数量/价格步长与余额。','- 每个参数组合均在计算前单独reserve，实际结果产生后独立finish。一次探索性数据schema检查误用了缺少Polars的系统Python，随后改用仓库虚拟环境复核；没有策略结果因该命令而产生或改变。','- 明细见 `report.json`、`trades.csv.gz`、`decisions.csv.gz`、`daily_equity.csv.gz`、`fold_results.csv`、`cost_scenarios.csv`及敏感性热图；尝试留痕见 `implementation_attempts.jsonl`。','']
 (R/'result.md').write_text('\n'.join(lines));surface(r);print('rendered',len(r['configs']),'configurations; best',names[0])
if __name__=='__main__':main()
