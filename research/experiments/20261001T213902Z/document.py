"""Publish all predeclared cells; summarize existing registered metrics only."""
import json
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROUND=Path(__file__).resolve().parent;ROOT=ROUND.parents[2]
r=json.loads((ROUND/'report.json').read_text());rows={**r['configs'],**r['read_only_diagonals']}
fig,axes=plt.subplots(2,3,figsize=(12,7),layout='constrained')
allvals=[x['scenes']['3']['net_return_pct'] for x in rows.values()]
for iy,y in enumerate(('2025','2026')):
 for iw,w in enumerate((.65,.75,.85)):
  cells={(x['BTC_lookback_days'],x['ETH_lookback_days']):x for x in rows.values() if x['year']==y and x['raw_weights'][0]==w}
  values=np.array([[cells[(a,b)]['scenes']['3']['net_return_pct'] for b in (60,65,70)] for a in (60,65,70)])
  ax=axes[iy,iw];im=ax.imshow(values,vmin=min(allvals),vmax=max(allvals),cmap='YlGn')
  for a in range(3):
   for b in range(3):
    cell=cells[((60,65,70)[a],(60,65,70)[b])]
    ax.text(b,a,f'{values[a,b]:.2f}%\n'+('PASS' if cell['status']=='passed' else 'REJECT')+('\nold' if a==b else ''),ha='center',va='center',fontsize=9)
  ax.set(xticks=range(3),xticklabels=[60,65,70],yticks=range(3),yticklabels=[60,65,70],xlabel='ETH SMA days',ylabel='BTC SMA days',title=f'{y} | initial BTC/ETH {w:.0%}/{1-w:.0%}')
fig.colorbar(im,ax=axes.ravel().tolist(),label='3x cost net return (%)')
fig.suptitle('Fixed mixed-lookback grid: reused historical diagnostics; diagonal read only')
fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
lines=['# 本轮：BTC/ETH 不同均线窗口组合','',
 '触发：2026-10-01 21:39:02 UTC；首工具：21:40:14 UTC。来源分支 `codex/strategy-research`；只做研究，未下真实订单。','',
 '## 结论','',
 '36 个新具体配置全部先reserve，共108个实际组合成本场景；30项passed、6项rejected，所有结果永久保存。12组相同数学规则在2025和2026各自的六折均满足固定数值门槛；passed仅指回溯开发门槛，尚不能证明稳定实盘正收益。',
 '36/36配置在1、2、3倍成本均为正。2025的18项全部达到门槛；2026有12项达到、6项因只有3/6正折而淘汰，这6项均使用ETH70日窗口。收益平台不等于逐折稳定。','',
 '## 假设、范围与查重','',
 'BTC与ETH的响应窗口不必相同。事前冻结BTC N∈{60,65,70} × ETH N∈{60,65,70}、±1%缓冲带、初始BTC/ETH原值资金分仓65/35、75/25、85/15。总资金2000USDT，对应BTC1300/1500/1700与ETH700/500/300。权重只用于初始资金，后续不维持比例、不调仓或转账；实际持仓取整和残余现金继承已完成的同规模组件。直接相加绝对分钟净值，禁止再次乘权重。',
 '每段六个不同窗口对×三个权重，共18新配置；两段共36。既往18个同窗口组合只读取旧结果填入敏感性对角线，不重复计算/登记。零新增组件回测，不将改名或重排组件算创新。部分不同窗口在某段行情产生完全相同持仓/收益，其规则仍不同，但这些相同实现路径不增加独立证据。',
 '登记起点520行、250保留ID、248规范去重定义，初始16条均有实际结果，无待补测。历史结论全文/原登记快照在prior_summary.json.gz；本轮完成后累计284规范定义、592行、无pending。','',
 '## 三项验证','',
 '1. Walk-forward：每段使用365日真实分钟数据，180日滚动训练历史、3日embargo、6×30日连续测试；固定规则无拟合/监督标签，purge0。2025测试2025-03-18 00:01至09-14 00:01UTC；2026测试2026-03-18 00:01至09-14 00:01UTC。上一日收盘指标在交易前可得，下一UTC00:01真实分钟open作执行参考；持仓与现金跨折延续，终止平仓扣成本。每场259382个完整分钟/订单点计算整体DD，不平均组件Sharpe或DD。两段分别报告，无跨年拼接/复利新策略。',
 '2. Sensitivity：每个年份/权重显示BTC N×ETH N完整3×3网格，6新+3旧；共54格、162成本场景，其中108新、54旧只读。所有格净收益与Sharpe在三倍成本均正；邻域正收益比例100%。CSV包含每格所有成本下净收益、分钟/日标回撤、Sharpe、Calmar、交易/成本及资格；PNG显示全网格。仍有相邻Sharpe差异被2sd描述阈值标记，见下表。阈值不是显著性检验，窗口/权重边界不能被解释为已证明最优，所有格高度相关。',
 '3. Costs：复用各实际资金规模的1/2/3倍完整账本：每边手续费10bp、half-spread1bp、滑点2bp，冲击0.5×滞后20日sigma×sqrt(交易预算/滞后20日quoteADV)，参与率上限0.1%；同时放大四项估计成本，tick额外成本单列。LOT_SIZE/PRICE_FILTER/NOTIONAL及5闭合分钟VWAP价格限制代理已入账，无再平衡额外交易；终止清仓计成本。spot仅做多，不需资金费/借币。冻结Oct1元数据对历史的应用是压力假设，不是历史交易所规则；无L2、队列、真实IOC成交、部分成交或延迟验证。完整成本拆分、拒单与资金违规计数见报告。','',
 '固定资格门槛：所有成本净正、≥4/6个一倍正折、三倍完整分钟DD≤25%、相同年份/权重九格三倍正收益占比≥60%、至少2组件往返、一倍gross reference PnL/执行成本≥2.5、无负现金/数量、两组件终止平仓。组合往返次数为组件往返之和，不是同步组合交易episode。','',
 '## 全部新配置','',
 '|年份|BTC N|ETH N|原值BTC/ETH|1x收益%|2x收益%|3x收益%|3x分钟DD%|1x正折|往返|结论|',
 '|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|']
for x in r['configs'].values():
 s=x['scenes'];lines.append(f'|{x["year"]}|{x["BTC_lookback_days"]}|{x["ETH_lookback_days"]}|{x["raw_weights"][0]:.0%}/{x["raw_weights"][1]:.0%}|{s["1"]["net_return_pct"]:.5f}|{s["2"]["net_return_pct"]:.5f}|{s["3"]["net_return_pct"]:.5f}|{s["3"]["max_drawdown_pct"]:.5f}|{x["positive_folds_1x"]}/6|{s["1"]["round_trips"]}|{x["status"]}|')
lines+=['','## 分折与参数落差','', '|年份/初始BTC权重|三倍正收益格|相邻差异标记/12|','|---|---:|---:|']
for g,v in r['sensitivity'].items():lines.append(f'|{g}|9/9|{sum(e["cliff_flag_2sd"] for e in v["adjacent_edges"])}/12|')
lines+=['','以75/25权重展示所有不同窗口对的三倍逐折收益，完整各权重/各成本分折见report.json：','', '|年份|BTC/ETH N|六个三倍折收益%|前五折合计%|','|---|---|---|---:|']
for x in r['configs'].values():
 if x['raw_weights'][0]!=.75:continue
 folds=x['scenes']['3']['folds'];five=100*(math.prod(1+f['net_return_pct']/100 for f in folds[:5])-1)
 lines.append(f'|{x["year"]}|{x["BTC_lookback_days"]}/{x["ETH_lookback_days"]}|'+', '.join(f'{f["net_return_pct"]:.4f}' for f in folds)+f'|{five:.5f}|')
lines+=['',
 '2026仍显著依赖末折上涨：75/25各混合配置最后一折约+23.7–23.8%，前五折合计为负。不得把“4/6正折”解释为每段稳定赚钱。固定同窗口N65/75:25旧策略在2026三倍+21.57073%、分钟DD13.91280%；本轮同权重混合窗口三倍收益均更低，未证明改进该冻结候选。2025存在相同实现路径，表中相等收益与邻域正数不可当独立胜利。','',
 '## 比较与局限','',
 '同期已登记50/50现货持有仅只读：2025三倍+88.58976%、分钟DD24.91393%；2026三倍+4.55488%、分钟DD33.38795%。现金无利息收益0。研究组合持仓/现金比例变化，与50/50持有权重和风险不同，不声称等风险超额收益。',
 '两段历史均已使用且本轮受旧结果启发，属于回溯开发诊断；不称最终未触碰留出、统计显著发现或前向实盘证据。分钟收盘/订单点DD仍不能捕获完整分钟内低价或可执行清算风险。USDT、交易所和容量假设未作实盘验证。',
 '原113625/forward_plan.json的N65、±1%、BTC75/ETH25前向计划保持原哈希，Oct2UTC00:01才开始，本轮冻结时未开始，无前向收益。下一轮优先取得开始后的已闭合行情并建立匹配成本的前向模拟证据，不根据本轮结果改原计划；未触碰的新参数需要另行完整预登记。','',
 '## 数据、核验与复现','',
 '来源为已保存Binance官方月度kline ZIP及官方CHECKSUM；2025原26 ZIP清单见173606/download_manifest.json，2026原54 ZIP见013355/data_manifest.json。四份parquet SHA256、边界与108组件成本净值SHA在data_manifest.json，归档source refs含原报告/具体spec/持仓成交archive哈希。数据留在忽略目录data/。',
 'audit.py独立核对4个分钟数据哈希/连续性/时间对齐、19440因果决策；从真实分钟价格与冻结现金/数量重建108个组件场景，再验证108个新组合完整28013256个NAV点、六折/Sharpe/DD/成本/终止余额、全网格资格、预登记先后与旧对角线只读。首次检查器日收盘索引错误已修正并保留audit_failure.md；未改策略/参数。',
 '全108场景及report.json精确重放，36条独立finish绑定同一最终report SHA。轻量JSON.gz保留完整成本化成交、dailyNAV、指标、分钟向量SHA与可无损重建组件引用；实际分钟向量不提交Git。',
 '复现：从仓库根执行 `bash research/experiments/20261001T213902Z/reproduce.sh`。prepare.py仅供首次预登记审计，不在已完成配置重跑。终结记录见finish.log；最终验证见verification.json。push采用已连接GitHub Git Data API、force=false，真实commit与推送核对由运行简报给出。','']
(ROUND/'result.md').write_text('\n'.join(lines))
print('PASS:36 new configuration rows, full fold examples and six complete sensitivity panels documented.')
