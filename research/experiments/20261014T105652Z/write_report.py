#!/usr/bin/env python3
"""Build concise tables/summary from the saved full result; never evaluates strategy outcomes."""
import csv,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
DAYS=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
def write_surface(report):
 colors=lambda x:'#20805a' if x>=10 else '#42a875' if x>=0 else '#bb473e' if x>-30 else '#842f33'
 cell=[];x0=145;y0=75;cw=84;ch=45
 for ai,asset in enumerate(('BTC','ETH')):
  ax=x0+ai*690
  cell.append(f'<text x="{ax+cw*3.5}" y="30" text-anchor="middle" class="asset">{asset}</text>')
  for j,d in enumerate(DAYS):cell.append(f'<text x="{ax+cw*j+cw/2}" y="58" text-anchor="middle" class="label">{d[:3]}</text>')
  for hrow,h in enumerate((1,3)):
   yy=y0+hrow*(ch+12)
   cell.append(f'<text x="{ax-18}" y="{yy+ch/2+5}" text-anchor="end" class="label">{h}d</text>')
   for dow in range(7):
    c=report['configs'][f'weekday_window_{asset}_dow{dow}_hold{h}d'];v=c['scenarios']['3']['net_return_pct'];xx=ax+cw*dow
    cell.append(f'<rect x="{xx}" y="{yy}" width="{cw-4}" height="{ch}" rx="4" fill="{colors(v)}"/><text x="{xx+(cw-4)/2}" y="{yy+27}" text-anchor="middle" class="value">{v:+.1f}%</text>')
 svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1530" height="240" viewBox="0 0 1530 240"><style>text{font-family:Arial,sans-serif;fill:#f5f5f5}.asset{font-size:20px;font-weight:bold}.label{font-size:12px;fill:#c8cdd2}.value{font-size:13px;font-weight:bold}</style><rect width="100%" height="100%" fill="#171b20"/>'''+''.join(cell)+'''<text x="35" y="225" class="label">3× net returns; all 28 candidates are negative at 3×; weekday columns are categorical, no OOS selection.</text></svg>'''
 (R/'sensitivity_surface.svg').write_text(svg)
def main():
 p=R/'report.json';r=json.loads(p.read_text());r['registry_fragment']='research/experiments/'+R.name+'/registry_records.jsonl';cs=r['configs'];s=r['summary'];rank=s['ranked_by_1x_net_return'];best=cs[rank[0]];b1,b2,b3=(best['scenarios'][str(k)] for k in (1,2,3))
 lines=[]
 lines += ['# BTC/ETH 固定星期 UTC 交易窗口研究结果','',f"- 轮次：`{R.name}`。星期、持有期、时间范围、成本和淘汰标准在计算前冻结于 `plan.json`；SHA256 `{r['frozen_plan_sha256']}`。",'- 本轮为 Binance 归档现货历史回测，不是本轮实时报价模拟、真实订单或实盘收益。已反复使用的 2025–2026 历史不是未触碰的最终留出集。','- 初始16项历史证据此前已逐项审计，缺少实际回测结果的配置为0；本轮未重算这些旧策略。',
 '','## 候选规则与动机','',
 '部分既有研究报告过 BTC/加密货币星期效应，本轮据此做独立的可交易性反证测试，不复现论文结论：[The day of the week effect in the cryptocurrency market](https://www.sciencedirect.com/science/article/pii/S1544612318304240)；[Bitcoin time-of-day, day-of-week and month-of-year effects](https://www.sciencedirect.com/science/article/pii/S1544612319301710)。这些旧样本只作动机，不能证明本策略有效。','',
 'BTC 与 ETH 分别建立独立 2,000 USDT 现货账户。每个配置每个 UTC 周在预先指定的星期一至星期日之一，于 00:00 确定性时间信号可得后，按 00:01 的下一分钟开盘买入；持有24或72小时，于对应日 00:01 的一分钟开盘卖出。每周最多一笔、窗口互不重叠；卖单被交易所过滤器代理拒绝时，下分钟重试至 OOS 终点；买单若被拒则跳过当周。只做多、不加杠杆、不借币、不跨币转账、不计现金利息。所有周几和持有期都预注册，未用 OOS 选定“最佳星期”。','',
 '','## 数据与时序','',
 '- 数据：Binance BTCUSDT、ETHUSDT 现货连续一分钟 OHLCV，聚合检查 UTC 时间戳、已闭合状态、连续性、正价格、成交量非负及每日 1,440 根分钟K线。输入范围 `2024-09-16` 至 `2026-09-16`；OOS `2025-09-19 00:01` 至 `2026-09-14 00:01 UTC`。输入文件 SHA256 见 `data_manifest.json`。',
 '- Walk-forward：360日分成12个连续、不重叠的30日评估窗，账户跨窗连续持仓和结算；没有模型训练、信号拟合或折间重置。首折前包含365日暖机和3日隔离。每配置仅约51–52笔往返交易，统计把握有限。',
 '- 成交价是回测历史下一分钟开盘引用，不是当前市场报价，也不代表 Binance 实际接单或成交保证。百分比价格限制以成交前5分钟VWAP作代理；没有历史盘口、历史费率层级或历史交易所过滤器，按本轮公开 `exchangeInfo` 当前过滤器快照近似。',
 '','## 成本与敏感性','',
 '- 每侧手续费10bp、估算半价差1bp、滑点2bp，加 `0.5 × 前20个完整UTC日日收益样本标准差 × sqrt(订单金额 / 前20日quote ADV)` 冲击；最大参与率0.1%。按 Binance PRICE_FILTER 向不利方向tick取整、LOT_SIZE向下取量，并检查NOTIONAL与PERCENT_PRICE_BY_SIDE。所有成本假设同倍数生成1×/2×/3×场景；审计中容量/余额拒绝数均为0。',
 '- 二维敏感性网格为资产 × 星期7类 × 持有期{1,3}，共28组、84个成本场景。局部邻域固定为同币种、循环星期距离≤1、两个持有期共6格；报告全量局部邻域3×正收益比例及热图。没用最优网格角点代替稳健性。',
 '','## 结论','',
 f"- 28组全部 `rejected`，通过0。1×、2×、3×净收益为正的配置数分别 `{s['positive_configurations_by_cost']['1']}`、`{s['positive_configurations_by_cost']['2']}`、`{s['positive_configurations_by_cost']['3']}`。3×局部邻域为正的全局比例为 `{s['global_3x_neighbor_robustness_fraction']:.1%}`；均未通过所有成本场景为正及≥60%局部邻域门槛。",
 f"- 1×最高配置 `{best['name']}`：1×/2×/3×收益 `{b1['net_return_pct']:.3f}% / {b2['net_return_pct']:.3f}% / {b3['net_return_pct']:.3f}%`，1×正收益折 `{b1['positive_folds']}/12`，3×分钟收盘与成交后采样回撤 `{b3['max_drawdown_1m_sampled_pct']:.2f}%`，3×局部邻域正收益比例 `{best['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}`。它在更高成本下转负，且回撤/邻域门槛失败，故不保留。",
 f"- 同期买入持有基准只读复用 `20261014T084051Z/report.json`，BTC 1×/3×为 `{r['benchmark_read_only']['same_OOS_period_cost_adjusted_buy_hold']['BTC']['1']['net_return_pct']:.2f}% / {r['benchmark_read_only']['same_OOS_period_cost_adjusted_buy_hold']['BTC']['3']['net_return_pct']:.2f}%`，ETH为 `{r['benchmark_read_only']['same_OOS_period_cost_adjusted_buy_hold']['ETH']['1']['net_return_pct']:.2f}% / {r['benchmark_read_only']['same_OOS_period_cost_adjusted_buy_hold']['ETH']['3']['net_return_pct']:.2f}%`。基准只作市场参照，不改变候选失败判定。",'- 本轮没有保留盈利候选。没有计算 DSR/PBO，也没有把重复使用的 OOS 称为最终测试集；仓库已有大量策略试验，星期选择存在多重比较风险。','',
 '','## 全部预注册配置','',
 '|配置|币种|UTC星期|持有天数|1×净收益|2×|3×|1×正折/12|1×/3×采样回撤|1×往返|3×邻域正比例|判定|','|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
 for name in rank:
  c=cs[name];a,b,d=(c['scenarios'][str(k)] for k in (1,2,3));lines.append(f"|{name}|{c['asset']}|{c['weekday_name']}|{c['holding_days']}|{a['net_return_pct']:+.2f}%|{b['net_return_pct']:+.2f}%|{d['net_return_pct']:+.2f}%|{a['positive_folds']}/12|{a['max_drawdown_1m_sampled_pct']:.1f}% / {d['max_drawdown_1m_sampled_pct']:.1f}%|{a['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{c['status']}|")
 lines += ['', '','## 复现与审计','',f"- 环境复现命令：`.venv/bin/python research/experiments/{R.name}/reproduce.py`。",'- 28个fingerprint均先成功 reserve，完整计算后逐项 finish。审计独立重放28×3成本结果、逐折收益、成交账本与连续净值哈希；详情见 `audit.log`。','- `report.json` 保存逐格净收益、逐折收益/回撤/Sharpe/Calmar、交易成本分项和净值哈希；`fold_results.csv`、`cost_scenarios.csv`、`daily_equity.csv.gz`、`trades.csv.gz` 及 `weekday_daily_returns.csv` 提供明细。','- 回撤是分钟收盘净值与成交后参考价采样，不含分钟内高低点或逐笔路径。','']
 (R/'result.md').write_text('\n'.join(lines))
 p.write_text(json.dumps(r,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 write_surface(r)
 print(f'rendered {len(cs)} rows; best={rank[0]} 1x={b1["net_return_pct"]:.5f}%')
if __name__=='__main__':main()
