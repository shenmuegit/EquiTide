#!/usr/bin/env python3
"""Render the frozen short-entry ATR sensitivity report and grid chart."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
ASSETS=('BTC','ETH');ENTRY=(5,10,15);PERIODS=(7,14,28);MULTS=(2,3,4)
def plot(r):
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1250" height="690" viewBox="0 0 1250 690"><style>text{font-family:Arial,sans-serif;fill:#f5f7f8}.t{font-size:20px;font-weight:bold}.s{font-size:11px;fill:#c8cdd3}.v{font-size:11px;font-weight:bold}</style><rect width="100%" height="100%" fill="#171b20"/>']
 x0=150;y0=78;cw=108;ch=42
 for ai,a in enumerate(ASSETS):
  ax=x0+ai*565
  out.append(f'<text class="t" x="{ax+1.5*cw}" y="27" text-anchor="middle">{a} 3× net return</text>')
  out.append(f'<text class="s" x="{ax+1.5*cw}" y="49" text-anchor="middle">entry E rows; columns ATR n; panels by stop multiplier M</text>')
  for mi,M in enumerate(MULTS):
   panel_y=y0+mi*195
   out.append(f'<text class="s" x="{ax+1.5*cw}" y="{panel_y-6}" text-anchor="middle">stop M={M}</text>')
   for ei,E in enumerate(ENTRY):
    yy=panel_y+ei*ch
    out.append(f'<text class="s" x="{ax-9}" y="{yy+25}" text-anchor="end">E={E}</text>')
    for ni,N in enumerate(PERIODS):
     c=r['configs'][f'atr_short_entry_{a}_E{E}_N{N}_M{M}'];v=c['scenarios']['3']['net_return_pct'];color='#208052' if v>=10 else '#42a875' if v>=0 else '#b94c44' if v>-30 else '#812f35';xx=ax+ni*cw
     out.append(f'<rect x="{xx}" y="{yy}" width="{cw-4}" height="{ch-3}" rx="3" fill="{color}"/><text class="v" x="{xx+(cw-4)/2}" y="{yy+24}" text-anchor="middle">{v:+.1f}% n{N}</text>')
 out.append('<text class="s" x="20" y="677">Complete predeclared grid; E=5/10/15 days; local surfaces shown. Reused OOS is not an untouched holdout.</text></svg>')
 (R/'sensitivity_surface.svg').write_text(''.join(out))
def main():
 p=R/'report.json';r=json.loads(p.read_text());r['registry_fragment']='research/experiments/'+R.name+'/registry_records.jsonl';r['implementation_attempts']='research/experiments/'+R.name+'/implementation_attempts.jsonl';p.write_text(json.dumps(r,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 s=r['summary'];order=s['ranked_by_1x_net_return'];best=r['configs'][order[0]];b=[best['scenarios'][str(k)] for k in (1,2,3)]
 lines=['# BTC/ETH 短周期日线通道 + Wilder ATR 跟踪退出：历史敏感性回测','','- 轮次：`'+R.name+'`；完整规则、参数、成本、OOS边界和失败门槛在计算前冻结。计划SHA256：`'+r['frozen_plan_sha256']+'`。','- 本轮是固定规则的历史回测，不是实时行情模拟或真实成交证明。2025–2026 OOS已被仓库反复用于研究，不是未触碰最终留出。','- 初始16条旧配置均有实际回测证据，缺失数0；本轮不重算旧条目。',
 '','## 研究动机与本轮变化','','上轮E=20/40通道入场的ATR尾随止损网格中，较好参数往返交易数很少。本轮预注册了更短E=5/10/15入场邻域，同时调整ATR周期与止损倍数，目的是检验信号次数增加后是否还保有跨期、全成本稳健性；这是同一反复研究历史上的第二阶段探索，不是新留出验证。',
 '', 'ATR计算依照[TA-Lib公开实现](https://github.com/TA-Lib/ta-lib/blob/main/src/ta_func/ta_ATR.c)中的Wilder true range及递推定义。引用只固定指标算法，不为交易规则的盈利性背书。',
 '',
 '每种币、每组参数使用独立2,000 USDT现货长仓现金账户。空仓时，已闭合日线收盘严格高于前E个完整日最高价（不含当前日）则入场。信号日按ATR_n与信号收盘初始化峰值和止损：`stop=close−M×ATR_entry`。后续已闭合日线更新峰值收盘，止损按`max(旧stop, peak−M×ATR_entry)`只会上移；收盘≤stop时于次日UTC 00:01分钟开盘参考退出。ATR在入场时冻结；止损收盘确认，不是日内触发。终点持仓计成本平仓。不加杠杆、不做空、不借币、不跨资产转账。',
 '', '## 数据与验证','',
 '- Binance现货1分钟OHLCV聚合为UTC日线OHLC及quote ADV；核对四个Parquet SHA、连续性、闭合分钟状态、日内分钟数、OHLC范围和正价格。输入范围2024-09-16至2026-09-16；OOS为2025-09-19 00:01至2026-09-14 00:01 UTC，共360天。细节见`data_manifest.json`。',
 '- Walk-forward：12个连续、不重叠30日窗口，账户、ATR和峰值/止损状态跨窗连续；无需拟合、无折间重置。365日预热加3日embargo。逐折结果及连续OOS逐分钟收盘净值采样回撤已保存；不含分钟内极值。',
 '- 信号只用收盘已闭合日线；历史成交参考是信号后60秒的次日00:01一分钟开盘。参考价不代表交易所实际IOC接受或真实成交。',
 '', '## 成本与敏感性','',
 '- 每侧手续费10bp、估算半价差1bp、滑点2bp，加前20个完整UTC日收益样本波动率与quote ADV相关平方根冲击；参与率上限0.1%。按本轮公开`exchangeInfo`快照的PRICE_FILTER/LOT_SIZE/NOTIONAL/PERCENT_PRICE规则做不利tick、数量步长及5分钟前置VWAP代理校验。历史L2、历史交易所过滤器不可用；各成本假设统一按1×/2×/3×压力测试。',
 '- 预设网格为资产×E{5,10,15}×ATR n{7,14,28}×M{2,3,4}，共54组、162个场景。敏感性邻域按同资产及三参数各自相邻索引组成；完整邻域正收益比率见CSV与图。',
 '', '## 结果与判定','',
 f"- 54个配置全部 `rejected`，通过0。1×/2×/3×成本下正收益配置数为 `{s['positive_configs_by_cost']['1']}` / `{s['positive_configs_by_cost']['2']}` / `{s['positive_configs_by_cost']['3']}`。没有配置达到至少8/12个正收益折，三倍局部邻域正收益全局比例为`{s['global_3x_positive_neighbor_fraction']:.1%}`。",
 f"- 1×最佳 `{best['name']}`：1×/2×/3×净收益 `{b[0]['net_return_pct']:.3f}% / {b[1]['net_return_pct']:.3f}% / {b[2]['net_return_pct']:.3f}%`，仅`{b[0]['positive_folds']}/12`折为正、`{b[0]['round_trips']}`次往返，3×采样回撤`{b[2]['max_drawdown_1m_sampled_pct']:.2f}%`，局部三倍邻域正收益比例`{best['sensitivity']['local_3x_neighbor_positive_fraction']:.1%}`。三倍成本仍正，但利润来自少量交易及少数时间折，敏感性未形成稳健平台，故拒绝。",
 '- OOS买入持有对照只读复用`research/experiments/20261014T084051Z/report.json`，未在本轮重算。对照相对收益不改变预注册通过门槛。没有DSR/PBO结论，也不把复用区间称作独立最终样本。','',
 '## 全配置表','',
 '|配置|币种|E|ATR n|M|1×|2×|3×|1×正折/12|DD 1×/3×|往返|3×邻域正比|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
 for name in order:
  c=r['configs'][name];x=[c['scenarios'][str(k)] for k in (1,2,3)];lines.append(f"|{name}|{c['asset']}|{c['entry_lookback_days']}|{c['atr_period']}|{c['stop_multiple']}|{x[0]['net_return_pct']:+.2f}%|{x[1]['net_return_pct']:+.2f}%|{x[2]['net_return_pct']:+.2f}%|{x[0]['positive_folds']}/12|{x[0]['max_drawdown_1m_sampled_pct']:.1f}% / {x[2]['max_drawdown_1m_sampled_pct']:.1f}%|{x[0]['round_trips']}|{c['sensitivity']['local_3x_neighbor_positive_fraction']:.0%}|{c['status']}|")
 lines+=['','','## 复现与审计','','- 完整回放：`.venv/bin/python research/experiments/'+R.name+'/reproduce.py`，不联网。54参数×3成本的成交、12折、连续分钟收盘采样净值、ATR recursion、Decimal余额、交易数量步长和价格tick均独立核验。','- 所有54项配置均先reserve后完成实际历史回测并finish。两次评估接口错误分别发生在候选结果产生前、报告文件落盘前；修正后整个预注册网格重新计算并通过精确审计，详见`implementation_attempts.jsonl`。','- 原始输入、代码、报告及记录sidecar哈希见`data_manifest.json`；逐折、成本、交易与日净值见配套CSV。','']
 (R/'result.md').write_text('\n'.join(lines));plot(r);print('rendered',len(r['configs']),'config table')
if __name__=='__main__':main()
