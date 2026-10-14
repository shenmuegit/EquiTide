#!/usr/bin/env python3
"""Render a frozen results table and sensitivity surface from report.json only."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
ASSETS=('BTC','ETH');LOOKS=(7,14,28);HURDLES=(0,2.5,5.0)
def surface(r):
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="390" viewBox="0 0 1080 390"><style>text{font-family:Arial,sans-serif;fill:#f6f7f8}.title{font-size:20px;font-weight:bold}.small{font-size:12px;fill:#c6ccd2}.v{font-size:13px;font-weight:bold}</style><rect width="100%" height="100%" fill="#171b20"/>']
 for ai,a in enumerate(ASSETS):
  x0=130+ai*500;y0=80;cw=115;ch=62
  out.append(f'<text class="title" x="{x0+1.5*cw}" y="32" text-anchor="middle">{a} — 3× cost net return</text>')
  out.append(f'<text class="small" x="{x0+1.5*cw}" y="55" text-anchor="middle">columns: entry hurdle 0%, 2.5%, 5%; rows: 7d, 14d, 28d lookback</text>')
  for li,L in enumerate(LOOKS):
   yy=y0+li*ch;out.append(f'<text class="small" x="{x0-8}" y="{yy+35}" text-anchor="end">L={L}</text>')
   for hi,H in enumerate(HURDLES):
    c=r['configs'][f'daily_roc_momentum_{a}_L{L}_H{str(H).replace(".","p")}'];v=c['scenarios']['3']['net_return_pct'];xx=x0+hi*cw
    color='#208052' if v>=10 else '#42a875' if v>=0 else '#b94c44' if v>-30 else '#812f35'
    out.append(f'<rect x="{xx}" y="{yy}" width="{cw-5}" height="{ch-5}" rx="4" fill="{color}"/><text class="v" x="{xx+(cw-5)/2}" y="{yy+31}" text-anchor="middle">{v:+.2f}%</text>')
 out.append('<text class="small" x="25" y="365">OOS variants; full predeclared grid shown. No parameters selected from this surface.</text></svg>')
 (R/'sensitivity_surface.svg').write_text(''.join(out))
def main():
 p=R/'report.json';r=json.loads(p.read_text());r['registry_fragment']='research/experiments/'+R.name+'/registry_records.jsonl';r['implementation_attempts']='research/experiments/'+R.name+'/implementation_attempts.jsonl';p.write_text(json.dumps(r,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 s=r['summary'];names=s['ranked_by_1x_net_return'];best=r['configs'][names[0]];b=[best['scenarios'][str(k)] for k in (1,2,3)];lines=[
 '# BTC/ETH 日线时间序列动量回测结果','',
 f"- 轮次 `{R.name}`；完整参数、OOS边界、失败标准在计算前冻结于 `plan.json`，SHA256 `{r['frozen_plan_sha256']}`。",
 '- 数据是 Binance 归档现货1分钟K线聚合出的历史日线，执行参考是下一日00:01的一分钟开盘。本轮不是实时行情模拟或真实订单。已重复研究的2025–2026历史不是未触碰的最终留出集。',
 '- 初始16项已由此前实际证据审计，缺实际回测结果配置为0；本轮没有重跑旧配置。',
 '','## 假设与规则','',
 '相关研究在更广的币种与区间报告过加密资产时间序列动量，本次只将其作为检验动机：[Risks and Returns of Cryptocurrency (NBER WP 24877)](https://www.nber.org/papers/w24877)。本轮BTC/ETH单币长仓规则不是该研究的复制，也不继承其历史结论。',
 '',
 '每个币种分别使用2,000 USDT独立现金账户。每根已闭合UTC日线 j 计算 ROC_L=close[j]/close[j−L]−1。空仓时 ROC_L 严格高于冻结门槛0%/2.5%/5%才入场；持仓时 ROC_L≤0退出，其余情况保留上一目标状态。Lookback为7/14/28日。信号仅在日线可用后产生，下一UTC日00:01分钟开盘成交，记录60秒延迟；OOS之前无成交。全额多头、无杠杆、无加仓或跨资产资金转移；终点统一计成本清仓。',
 '',
 '## 数据与时序','',
 f"- Binance BTCUSDT、ETHUSDT现货1分钟OHLCV；聚合UTC日收盘和quote ADV。连续性、闭合状态、每天1,440分钟、OHLC范围与成交量经检查。数据哈希见 `data_manifest.json`。",
 '- 输入期2024-09-16至2026-09-16；OOS期2025-09-19 00:01至2026-09-14 00:01 UTC，共360天。前365天用于历史暖机，首折前留3天embargo。',
 '- Walk-forward按12个连续30天窗口报告；固定日线规则不在任何折上训练或择优，账户状态跨折延续。逐折净值/收益和连续OOS净值整体采样回撤均留档。',
 '- 回撤由OOS 1分钟收盘净值及成交后参考标记采样，不含分钟内价格极值；回测成交参考价不能证明交易所会接单。',
 '',
 '## 成本与敏感性','',
 '- 每侧手续费10bp、估计半价差1bp、滑点2bp，加前20个完整UTC日日波动率与quote ADV相关的平方根冲击；参与率不超过0.1%。按当前公开Binance PRICE_FILTER/LOT_SIZE/NOTIONAL/PERCENT_PRICE规则检查并不利tick取整。历史L2盘口、历史费率层级和历史过滤器不可得，点差/滑点/即时IOC成交为模型假设。',
 '- 18个候选为资产×Lookback{7,14,28}×入场门槛{0%,2.5%,5%}。分别计算1×/2×/3×成本。局部敏感性为同币种相邻两轴的3×3网格，包含中心格。',
 '',
 '## 判定','',
 f"- 18个配置全部 `rejected`，通过0。1×/2×/3×净收益为正的配置分别 `{s['positive_configs_by_cost']['1']}` / `{s['positive_configs_by_cost']['2']}` / `{s['positive_configs_by_cost']['3']}`；18个配置的3×邻域正收益比例合计 `{s['global_3x_positive_neighbor_fraction']:.1%}`。",
 f"- 1×最佳为 `{best['name']}`：1×/2×/3×净收益 `{b[0]['net_return_pct']:.3f}% / {b[1]['net_return_pct']:.3f}% / {b[2]['net_return_pct']:.3f}%`，1×正折 `{b[0]['positive_folds']}/12`，3×采样回撤 `{b[2]['max_drawdown_1m_sampled_pct']:.2f}%`，3×局部邻域正收益占比 `{best['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}`。它未满足全成本正收益、折一致性和邻域稳健性门槛，因此淘汰。",
 '- 同期BTC/ETH持有基准只读复用 `research/experiments/20261014T084051Z/report.json`，未重算。相对基准更好不替代预先设定的资格门槛。',
 '- 没有用本窗口报告DSR/PBO，也没有把复用历史称为独立检验；仓库的多轮参数探索带来额外多重比较偏差。',
 '',
 '## 参数网格','',
 '|配置|资产|Lookback|入场门槛|1×|2×|3×|1×正折/12|1×/3×采样回撤|1×往返|3×邻域正收益|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
 for name in names:
  c=r['configs'][name];x=[c['scenarios'][str(k)] for k in (1,2,3)];lines.append(f"|{name}|{c['asset']}|{c['lookback_days']}日|{c['entry_hurdle_pct']}%|{x[0]['net_return_pct']:+.2f}%|{x[1]['net_return_pct']:+.2f}%|{x[2]['net_return_pct']:+.2f}%|{x[0]['positive_folds']}/12|{x[0]['max_drawdown_1m_sampled_pct']:.1f}% / {x[2]['max_drawdown_1m_sampled_pct']:.1f}%|{x[0]['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{c['status']}|")
 lines+=['','','## 复现与留档','','- 运行 `.venv/bin/python research/experiments/'+R.name+'/reproduce.py` 可不联网重放54个策略/成本场景和逐折/交易账本。','- 每个参数配置在计算前单独reserve，结果完成后单独finish。审计会比对原始输入SHA、信号执行时序、分钟净值采样、成本、数量精度与账户余额。','- 首次独立审计仅因审计脚本用二进制浮点做步长整除而失败；改为Decimal精确校验后，54个场景完整重放通过。该修正未改变策略规则或回测结果，尝试记录在 `implementation_attempts.jsonl`。','- 完整结果见 `report.json`；敏感性和交易明细见 `trades.csv.gz`、`decisions.csv.gz`、`daily_equity.csv.gz`、`fold_results.csv` 与 `cost_scenarios.csv`。','']
 (R/'result.md').write_text('\n'.join(lines));surface(r);print('report rendered for',len(r['configs']),'variants; best',names[0])
if __name__=='__main__':main()
