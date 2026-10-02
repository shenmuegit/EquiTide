"""Publish complete hybrid diagnostics and honest initial shadow losses."""
import json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROUND=Path(__file__).resolve().parent;r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());rows=r['configs'];grid=r['plan']['grid']
fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained');values=[x['scenes']['3']['net_return_pct'] for x in rows.values()]
for iy,y in enumerate(('2025','2026')):
 for ix,direction in enumerate(grid['directions']):
  cells={(x['SMA_lookback_days'],x['EMA_span_days']):x for x in rows.values() if x['year']==y and x['direction']==direction};v=np.array([[cells[(n,s)]['scenes']['3']['net_return_pct'] for s in grid['EMA_span_days']] for n in grid['SMA_lookback_days']]);ax=axes[iy,ix];im=ax.imshow(v,cmap='YlGn',vmin=min(values),vmax=max(values))
  for i in range(3):
   for j in range(3):ax.text(j,i,f'{v[i,j]:.2f}%\n'+('PASS' if cells[(grid['SMA_lookback_days'][i],grid['EMA_span_days'][j])]['status']=='passed' else 'REJECT'),ha='center',va='center')
  ax.set(xticks=range(3),xticklabels=[50,65,80],yticks=range(3),yticklabels=[60,65,70],xlabel='EMA span days (band1.5%)',ylabel='SMA lookback days (band1%)',title=y+' | '+direction.replace('_',' '))
fig.colorbar(im,ax=axes.ravel().tolist(),label='3x cost net return (%)');fig.suptitle('Hybrid75/25 portfolios | both histories reused | no real orders');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
lines=['# 本轮：SMA/EMA跨资产组合与冻结计划首段观测','',
 '触发2026-10-02 01:41:32UTC；首工具01:41:57UTC。研究分支codex/strategy-research，无真实订单。','',
 '## 结论','',
 '36个新混合组合先reserve，108成本场景完成；三倍成本36/36净正，28项达到固定历史门槛、8项因正折不足淘汰。10组相同规则在2025/2026分别都达到门槛；所有结果完整保留。',
 '另3个固定截止时间的前向观测配置分别先reserve，9成本场景实际完成。原冻结SMA65/±1%/75:25计划在Oct2UTC00:01起点有BTC/ETH入场信号；截至01:40UTC的99分钟模拟组合一/二/三倍净收益-0.34871/-0.47913/-0.60927%，三倍分钟/订单DD0.69425%。不强制平仓，持仓状态用于后续延续。该段不足180天/六折，三条观测以实际结果的rejected留档，只表示本次短窗口不能取得长期资格，不表示取消/淘汰原冻结计划。','',
 '## 新组合：假设、查重与资金','',
 'SMA与EMA响应速度不同，检验分别放在不同资产是否改善逐折混合。事前冻结SMA窗口60/65/70（±1%）×EMA跨度50/65/80（±1.5%），两方向BTC_SMA_ETH_EMA、BTC_EMA_ETH_SMA；每方向每年9格，两段共36。EMA1.5%受上一轮结果启发，已明确是开发选择，不是未触碰验证。两段历史都已使用，不宣称事前选出2025策略、统计显著发现或稳定实盘盈利。',
 '原值BTC75%/ETH25%代表初始1500/500USDT，总2000；不同方向不改变资产权重。复用24个已有实际规模、量化取整、完整1/2/3成本的组件，绝对分钟净值相加，不再乘权重；无转账/再平衡/维持权重。仅换EMA/SMA资产和参数才构成新指纹，旧策略/比较对象只读。部分参数实现相同净值，不能增加独立证据。',
 '此前700行、340保留ID、338规范定义，初始16条均有真实结果，无待补测。全部登记和历史结论全文快照见prior_summary.json.gz。本轮36混合+3观测共39项finish后为778行、379保留ID、377规范定义，无pending。','',
 '## 三项历史验证','',
 'Walk-forward：每段180日滚动训练历史、3日gap、连续六个30日测试。固定指标无拟合/监督标签，purge0，指标/desired状态和实际现金数量跨折连续。SMA从前N完整日收盘均值；EMA递推alpha2/(span+1)、数据首日seed、前一已完成close的EMA，种子记忆可早于滚动训练窗口，不作模型训练/每折重置。决策均先于下一UTC00:01真实分钟open；终止清仓扣成本。2025 OOS03-18至09-14、2026同月日，均UTC00:01边界。组合对齐共同全分钟轴，每场259382点计算完整DD；两段分别报告，没有未登记的跨年收益拼接。',
 'Sensitivity：每年每方向完整SMA N×EMA span3×3，共四面36格；全部变体1/2/3收益/DD/Sharpe365/Calmar/往返/成本与资格见CSV及report.json，PNG显示完整三倍面。每面净收益/Sharpe三倍正比例100%，但2026完整资格为BTC_SMA方向6/9、BTC_EMA方向4/9，不能把盈利比例当全部稳健资格。相邻Sharpe差异2sd为描述标记，无显著性推断；边界/单点不能证明最优。',
 'Costs：复用实际BTC1500/ETH500账本：每边费10bp、half-spread1bp、滑点2bp；冲击0.5×滞后20日sample log sigma×sqrt(预算/滞后20日quoteADV)，参与率≤0.1%，四项估计同时1/2/3倍；tick额外成本单列。lot/tick/notional和5闭合分钟VWAP代理、终止费用、残余现金及拒单完整入账，组合无额外换仓。spot仅做多无资金费/借币。Oct1静态元数据用于历史是压力假设，未验证历史动态reference/L2/队列/延迟/部分成交/IOC实成交，分钟mark DD不包含完整分钟内可执行风险。',
 '资格门槛保持：所有成本净正、1x至少4/6正折、3x完整分钟DD≤25%、相同面3x净正比例≥60%、1x至少2组件往返、gross reference PnL/成本≥2.5、无负余额、终止平仓。组合往返为组件之和，不是同步交易episode；passed仅指历史门槛。','',
 '## 全部混合配置','',
 '|年份|方向|SMA N|EMA span|1x收益%|2x%|3x%|3x分钟DD%|1x正折|往返|结论|','|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for x in rows.values():
 s=x['scenes'];lines.append(f'|{x["year"]}|{x["direction"]}|{x["SMA_lookback_days"]}|{x["EMA_span_days"]}|{s["1"]["net_return_pct"]:.5f}|{s["2"]["net_return_pct"]:.5f}|{s["3"]["net_return_pct"]:.5f}|{s["3"]["max_drawdown_pct"]:.5f}|{x["positive_folds_1x"]}/6|{s["1"]["round_trips"]}|{x["status"]}: {", ".join(x["failed_criteria"])}|')
lines+=['','展示预定网格中心SMA65/EMA65，完整逐折/全部成本见报告：','', '|年份|方向|三倍六折收益%|前五折累计%|','|---|---|---|---:|']
for y in ('2025','2026'):
 for direction in grid['directions']:
  s=rows[f'hybrid_{y}_{direction}_n65_s65']['scenes']['3'];five=100*(math.prod(1+a['net_return_pct']/100 for a in s['folds'][:5])-1);lines.append(f'|{y}|{direction}|'+', '.join(f'{a["net_return_pct"]:.4f}' for a in s['folds'])+f'|{five:.5f}|')
lines+=['',
 '中心BTC_SMA65/ETH_EMA65在两段三倍+33.93710/+21.80378%、DD14.31049/13.51957%；其2026前五折-1.62344%、末折+23.81382%，利润仍集中末折。中心反方向2026只有3/6正折而淘汰。开发面改善不能替换原冻结前向参数。',
 '旧比较全部只读：SMA65/±1%/75:25在2025/2026三倍+32.91111/+21.57073%；EMA50/±1.5%/75:25为+32.74362/+10.81677%。50/50持有为+88.58976/+4.55488%、分钟DD24.91393/33.38795%，权重/现金/风险不匹配，不声称等风险alpha。现金无利息收益0，未新计算比较策略。','',
 '## 首段冻结前向模拟：亏损完整保留','',
 '原113625/forward_plan.json哈希保持、N65/±1%/BTC75%ETH25%未变。观测规则沿用原浮点数量、费用/价差/滑点/冲击模型，与上述lot取整历史组件实现有区别，未暗中替换原模型。65个已闭合1d暖机（Jul29至Oct1）来自Binance公共REST；49个重叠日收盘/quote_volume与旧归档精确匹配。Oct2 00:00至01:40排除边界后的100个闭合1m，以00:01open作模拟入场参考，其后99分钟闭合价mark。原信号Decimal均值与原sig.step直接单步处理，不补造当前日收盘。',
 '依据[Binance官方市场数据接口](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints)获取公共klines；源响应时间单位ms、closeTime+1为闭合可得时间，严格按固定截止边界过滤。URL、真实取得时间及原response SHA在forward_report.json；完整65日/100分钟源数组在forward_inputs.json.gz，原响应字节重建后SHA相同的gzip见forward_response_manifest.json。没有把ticker/当前价冒充历史成交。',
 '规则冻结早于开始，但行情在开始后延迟取得，所以本段是延迟shadow重建，不是00:01实时执行/真实订单或实盘盈利证据。记录时BTC priorclose84880.05/SMA74564.28215、ETH2706.42/SMA2322.892，现金初始状态均触发希望持币；每成本场景各两笔组件模拟买入。','',
 '|观测|成本|99分钟净收益%|完整mark DD%|实际模拟买入数|','|---|---|---:|---:|---:|']
for n,x in f['configs'].items():
 for k,s in x['scenes'].items():lines.append(f'|{n}|{k}x|{s["net_return_pct"]:.5f}|{s["max_drawdown_pct"]:.5f}|{s["executions"]}|')
lines+=['',
 '三项前向验证状态：1/2/3成本场景已经实际计算，但只有99分钟、0完整日，walk-forward六折/180天资格未完成；前向敏感性未计算，不把过去参数面当新前向证据；不报短样本年化Sharpe/CAGR/Calmar。全部短窗口收益负，3个partial配置以rejected/result_available=true保存实际结果，原长期计划仍collecting。',
 '不在01:40人工卖出、不重置现金。forward_state.json分别保存BTC/ETH三个成本账本的现金、实际数量与desired状态；下一日决策为Oct3UTC00:01。下一轮从此延续，同日只加已闭合分钟mark，不重复首笔买入；新截止时间先reserve，保留原trade/cost与持仓连续性。原planned终止2027-03-31计退出成本，此次只是mark快照。',
 '首次历史数组适配要求额外完整日而失败，以及单步float均值恢复原Decimal精度均留痕于forward_failure.md；第一次有效浮点适配输出/source原SHA匹配快照完整保存在forward_adapter_first_report.json和forward_adapter_first_source.py.txt，最终报告绑定正确Decimal规则。','',
 '## 数据、审计和复现','',
 '历史四份真实parquet SHA、组件spec/report/archive SHA、72个已有组件成本场景的完整NAV SHA与来源见data_manifest.json；2025的26 ZIP与2026的54 ZIP官方checksum沿用原清单。独立audit从真实分钟价及现金/数量段重建72源场景，再核对108新组合28013256个NAV、六折乘积/Sharpe/DD/成本/资格与预登记顺序；9个首段观测的真实暖机/闭合价、原Decimal signal、模拟买入成本/数量、现金与组合求和亦复核。',
 '所有108混合+9前向场景与冻结报告精确重放，39独立finish绑定各自report SHA，registry检查通过。大行情和全分钟向量留忽略data/；Git只保留轻量充分证据。',
 '复现：仓库根 `bash research/experiments/20261002T014132Z/reproduce.sh`，使用已保存源数据/向量，不再次网络获取或写登记。prepare.py与forward.py --reserve仅供首次预登记审计，已完成配置禁止重跑reserve。真push状态与commit在运行简报核对。','']
(ROUND/'result.md').write_text('\n'.join(lines));print('PASS:all36 hybrid rows and all9 forward losses documented;frozen plan/continuation clear.')
