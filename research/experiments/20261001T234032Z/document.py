"""Publish every registered result and the full frozen sensitivity surface."""
import collections,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
ROUND=Path(__file__).resolve().parent;r=json.loads((ROUND/'report.json').read_text());rows=r['configs'];plan=r['plan']
fig,axes=plt.subplots(2,3,figsize=(12,7),layout='constrained');vals=[x['scenes']['3']['net_return_pct'] for x in rows.values()]
for iy,y in enumerate(('2025','2026')):
 for ig,g in enumerate(('BTC','ETH','combination')):
  cells={(x['span_days'],x['band']):x for x in rows.values() if x['year']==y and x.get('asset','combination')==g}
  data=np.array([[cells[(n,b)]['scenes']['3']['net_return_pct'] for b in plan['grid']['symmetric_band_fraction']] for n in plan['grid']['span_days']]);ax=axes[iy,ig];im=ax.imshow(data,cmap='RdYlGn',norm=TwoSlopeNorm(vmin=min(vals),vcenter=0,vmax=max(vals)))
  for i in range(3):
   for j in range(3):
    cell=cells[(plan['grid']['span_days'][i],plan['grid']['symmetric_band_fraction'][j])];ax.text(j,i,f'{data[i,j]:.2f}%\n'+('PASS' if cell['status']=='passed' else 'REJECT'),ha='center',va='center',fontsize=9)
  ax.set(xticks=range(3),xticklabels=['0.5%','1.0%','1.5%'],yticks=range(3),yticklabels=[50,65,80],xlabel='Symmetric band',ylabel='EMA span days',title=f'{y} | '+('BTC/ETH 75/25' if g=='combination' else g))
fig.colorbar(im,ax=axes.ravel().tolist(),label='3x cost net return (%)');fig.suptitle('Frozen EMA grid | reused histories | no prospective evidence');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
lines=['# 本轮：递推 EMA 缓冲带趋势策略','',
 '触发2026-10-01 23:40:32 UTC，首工具23:41:12UTC；网格冻结23:43:24UTC。研究分支codex/strategy-research；无真实订单。','',
 '## 结论','',
 '54项全部先reserve，162个真实成本场景已完成；28项passed、26项rejected，全部结果包括负收益永久保留。36实际资金规模组件与18个75/25组合；53项一倍净正、52项三倍净正。2025全部27项达到数值门槛；2026仅1个组合达到，其余26项淘汰。',
 '唯一跨两段都满足门槛的组合为EMA span50日、对称±1.5%带、原值BTC75%/ETH25%。它是本轮待进一步观察的回溯候选，尚非稳定实盘正收益方法。2026只有1/9组合满足完整资格，邻近配置盈利却未通过逐折门槛；不能把该单点解释为广泛稳定的合格参数平台。','',
 '## 规则、查重与事前边界','',
 '日线EMA跨度50/65/80 × 对称带0.5%/1%/1.5%，每年BTC、ETH与75/25组合各9格；两段共54新指纹。规则与参数均在本轮信号/回测前冻结，不因结果改变。旧15m双EMA交叉与本轮日线“前收盘价对单EMA缓冲带”不同；不因策略族相同排除新参数，也不将改名视作创新。',
 'EMA alpha=2/(span+1)，第一完整日收盘C0作为E0，Ej=(1-alpha)E[j-1]+alpha*Cj，adjust=False，无NaN。首OOS决定i=183从现金desired状态开始；只比较C[i-1]与E[i-1]*(1±band)，严格超过上带希望持币，严格低于下带希望现金，等号/带内保留状态。真实执行失败保留实际现金/持仓，以后日决定可重试。EMA从数据首日暖机并跨折连续，不从每个滚动训练边界重置，seed记忆可能早于训练窗口，是固定状态指标而非训练模型。',
 '公式经[官方pandas EWM文档](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)核对，访问2026-10-01；独立审计用本地pandas2.2.3 ewm(span,adjust=False)交叉验证。公式来源只定义计算，不支持经济正收益论断。',
 '初始总2000USDT，BTC1500/ETH500；原值75/25代表初始资本，不自动归一化/每天维持比例。各资产无杠杆、无转账/再平衡，不计USDT收益。买入最大可负担lot取整量，保留余额；组合复用本轮先算好的同规模成本净值直接相加，不二次加权。',
 '此前592登记行、286保留ID、284规范定义；初始16条均有实际结果，无pending，完整登记与历史中文结论快照见prior_summary.json.gz。完成后累计338规范定义、700行，无pending。','',
 '## 三项验证','',
 'Walk-forward：两段各365日真实Binance spot分钟行情，180日滚动历史/3日embargo/六个连续30日测试。固定无标签/拟合，purge0。2025 OOS2025-03-18 00:01至09-14 00:01UTC，2026 OOS2026-03-18 00:01至09-14 00:01UTC。前日完整收盘在交易前可得，下一UTC00:01真实分钟open为模拟成交参考，首折现金、跨折连续持仓，终止平仓扣成本。每场259382分钟/订单点算完整DD，逐折净值不重置。两段分别报告，没有构造未登记的跨年拼接组合。',
 'Sensitivity：每年/每角色完整3×3跨度/带宽表，共6组54格；CSV列出所有1/2/3倍净收益、分钟与日标DD、Sharpe365、Calmar、往返、成本、前五折与末折。下方PNG显示三倍收益/资格；相邻Sharpe2sd落差只作描述标记，不是显著性。2026组合三倍9/9盈利但仅1/9完整资格，通过格位于跨度/带宽边缘，应避免择优放大和“最优已确定”的说法。',
 'Costs：继承冻结Decimal IOC执行模型：每边费10bp、half-spread1bp、滑点2bp；冲击0.5×滞后20日sigma×sqrt(预算/滞后20日quoteADV)，参与率≤0.1%，四项估计成本同时乘1/2/3，tick成本独立列出。PRICE_FILTER逆向取整、LOT_SIZE下取整、NOTIONAL/5分钟已完成VWAP价格代理、买卖资金守恒及终止成本全部保留。spot做多无资金费/借币。旧Oct1元数据统一应用历史只是压力假设；没有历史动态交易所reference、盘口/排队、延迟、部分成交或真实IOC可成交证据，分钟DD亦不含完整分钟内风险。',
 '门槛完整沿用此前：所有成本收益>0；1倍至少4/6正折；3倍完整分钟DD≤25%；同年同角色9格3倍净正比例≥60%；1倍至少2往返、gross reference PnL/执行成本≥2.5；无负余额与终止平仓。组合往返为组件之和，不是同步交易episode。passed只表示历史开发门槛。','',
 '## 跨两段通过的组合','',
 '|年份|成本|净收益%|分钟DD%|Sharpe365|成本USDT|正折1x|往返|前五折累计%|','|---|---|---:|---:|---:|---:|---:|---:|---:|']
for y in ('2025','2026'):
 x=rows[f'ema_{y}_combo_s50_b0.015_btc0.75']
 for k,s in x['scenes'].items():lines.append(f'|{y}|{k}x|{s["net_return_pct"]:.5f}|{s["max_drawdown_pct"]:.5f}|{s["sharpe_365"]:.5f}|{s["cost_usdt"]:.5f}|{x["positive_folds_1x"]}/6|{s["round_trips"]}|{s["first_five_fold_return_pct"]:.5f}|')
 lines+=['',f'{y}三倍六折净收益%：'+', '.join(f'{f["net_return_pct"]:.5f}' for f in x['scenes']['3']['folds'])+'。','']
lines+=['2026该组合前五折三倍累计-3.44189%，末折+14.76692%；总体盈利仍靠最后上涨，未解决收益集中。2025末折则为-7.05831%，零收益第一折与四个上涨折也不等于每期赚钱。','',
 '与已完成SMA65/±1%/75:25旧结果只读比较：2025旧三倍+32.91111%、分钟DD14.55663%，2026旧+21.57073%、DD13.91280%；新EMA50/1.5%分别+32.74362%、DD14.13490%及+10.81677%、DD13.34575%。有限DD改善伴随2026明显收益降低及更高换手，不能宣称风险收益优于原冻结候选，更不据此替换原前向计划。','',
 '## 全部54个具体配置','',
 '|年份|角色|span|带宽|1x净收益%|2x%|3x%|3x分钟DD%|1x正折|往返|结论/失败项|','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for x in rows.values():
 ss=x['scenes'];lines.append(f'|{x["year"]}|{x.get("asset","75/25组合")}|{x["span_days"]}|{x["band"]:.1%}|{ss["1"]["net_return_pct"]:.5f}|{ss["2"]["net_return_pct"]:.5f}|{ss["3"]["net_return_pct"]:.5f}|{ss["3"]["max_drawdown_pct"]:.5f}|{x["positive_folds_1x"]}/6|{ss["1"]["round_trips"]}|{x["status"]}: {", ".join(x["failed_criteria"])}|')
lines+=['','## 敏感性与负收益','', '|年份/角色|三倍净正|三倍Sharpe正|相邻差异标记/12|','|---|---:|---:|---:|']
for g,ss in r['sensitivity'].items():lines.append(f'|{g}|{ss["metrics"]["3"]["positive_return_fraction"]:.1%}|{ss["metrics"]["3"]["positive_sharpe_fraction"]:.1%}|{sum(e["cliff_flag_2sd"] for e in ss["adjacent_edges"])}/12|')
lines+=['',
 '2026 ETH span80/0.5%：一倍+4.04237%、三倍-0.22718%、DD26.14513%；span80/1.5%：一倍-8.81080%、三倍-11.16939%、DD22.54940%。亏损、成本变负及所有资格失败都保留，不能只展示唯一合格组合。资格失败项可同时出现：26项正折不足、2项所有成本正收益未满足、2项DD超限、1项gross/cost不足。',
 '全网格54格是相关参数试验；部分不同参数实现路径相同，不能当独立盈利证据。不存在未触碰最终测试集/前向利润或多重试验后统计显著的证明。','',
 '## 数据、复现与下一轮','',
 '四份完整真实分钟parquet SHA、时间边界、旧daily_inputs归档SHA见data_manifest.json。2025源26ZIP官方checksum见173606/download_manifest.json，2026源54ZIP见013355/data_manifest.json，实际行情与全分钟向量留在忽略data/；Git只保留轻量完整成交/持仓分段/逐折/每日NAV/全向量SHA及必要代码。',
 'audit.py用真实分钟价重建全部162场景42019884个净值点，pandas独立核对19440因果决定，逐笔复核702个Decimal成交的滞后ADV/sigma、VWAP、逆向tick/lot取整、费用/冲击、现金数量守恒；检查预登记时间、四个数据哈希、逐折乘积/完整分钟DD/Sharpe/敏感性/资格与旧比较只读。继承kernel的逆向边界检查见kernel_check.log。全162场景与report.json精确重放，54条finish绑定最终报告，查重检查通过。',
 '从仓库根运行 `bash research/experiments/20261001T234032Z/reproduce.sh`。prepare.py仅首次冻结/预登记，已finish不能重跑；report.json与已绑定源文件不再改。所有结果及实际push状态由最终简报给出。',
 '原113625/forward_plan.json保持哈希：N65/±1%/BTC75%ETH25%，计划Oct2UTC00:01开始；本轮冻结23:43时尚未开始，没有收集前向观测。下一轮在已开始后使用新闭合真实行情按原参数建立前向模拟，并诚实保留早期样本不足；不得从本轮更换原计划或把历史EMA称前向。','']
(ROUND/'result.md').write_text('\n'.join(lines));print('PASS:all54 configurations,negative outcomes,full six-panel surface and concentration limits published.')
