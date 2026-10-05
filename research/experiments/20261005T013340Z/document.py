"""Publish all registered entry/exit outcomes and fixed original observer evidence."""
import json,gzip
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent;ROOT=T.parents[2]
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());d=json.loads((T/'diagnostic.json').read_text());s=r['summary'];p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
lines=['# BTC/ETH：固定67.5/32.5的入场×退出窗口验证','',
'触发2026-10-05T01:33:40.359Z；先fetch/ff同步研究分支，基点ee38a411cdbeb9f10f0bbdd77be1f392e3624547。使用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs。首工具时间未精确记录，登记和计算UTC为准。未下真实订单。','',
'## 结论','',
f"36个新历史定义（24组件、12组合）事前reserve，完成108成本场景；{len(s['passed'])}通过、{len(s['rejected'])}淘汰。全部36定义1/2/3x总收益为正，正收益与通过全部资格门槛不同。18个entry10/15/20、exit30旧定义54场景只读；全网格54定义162场景。",
'新增3组跨两段历史合格参数对：entry10/15/20、exit40、EMA50±1.5%、原初始67.5/32.5。它们在两个年份及所有成本下的完整分钟NAV都与同entry的旧exit30相同，所以新增不同参数配置，但新增不同的合格历史收益路径为0，不能称3份独立改进。',
f"21个淘汰中18个失败于four_positive_1x_folds（2025的exit20 BTC及组合6个，2026所有新单币12个）；另外3个2025 exit20 ETH失败于3x分钟回撤超过25%。所有正收益淘汰均保留。",
'退出20日使2025更差；在2026只影响BTC末折、略减组合总收益，未减少前五折合计损失。2026全部九格组合3x前五折合计-1.49708%，利润仍依赖末折；不能把前五折合计为负说成五折各自为负。2026九格仅两条实现NAV（exit20一条、exit30/40同一条），不是九份独立证据。',
f"108个新成本场景中{d['identical_new_scenes_to_matching_old_exit30']}个完整NAV与匹配旧exit30相同：exit40全54场景及2026 ETH exit20的9场景。其余新轨迹也已实际计算、审计、保存。新方案没有改善目标稳健性；保留合格参数和淘汰证据，继续原冻结模拟。",'',
'## 冻结完整规则、参数、资金和成本','',
'事前固定entry10/15/20 × exit20/30/40双轴；EMA跨度50、±1.5%和BTC/ETH原值.675/.325不变；预定中心entry15、exit30为旧只读配置，不根据结果改中心。未更改初始OOS、费用、门槛或终止边界。',
'决策i只看完成日C[i-1]。若C[i-1]<min(C[i-exit-1:i-1])或float(C[i-1])<EMA50[i-1]×0.985，则desired=cash；否则若C[i-1]>max(C[i-entry-1:i-1])且float(C[i-1])>EMA50[i-1]×1.015，则desired=long；其余/相等保持。退出优先，通道参考区间止于i-2。EMA首seed为数据第0日float close，alpha=2/51、adjust=False逐日递推，跨折不重置。',
'2000USDT以原值.675/.325明确初始分仓1350/650独立账户，不自动归一化、维持敞口、再平衡或转账。组件按实际本金和自己的交易计算；组合直接相加已成本化绝对NAV一次，不再乘权重或缩放旧净值。现货多头/现金，无杠杆、空头、拟合、未来标签、延迟arming、日内stop或加仓。',
'日收盘UTC00:00可得，下一UTC00:01真实minute open为参考。历史账户使用Decimal28，IOC立即完整成交是假设，买价上取PRICE tick、卖价下取tick、qty下取LOT，残余现金保留。静态PRICE/LOT/NOTIONAL/PERCENT_PRICE_BY_SIDE与前5闭合分钟VWAP代理核查；拒单不改现金、可后续重试，终点平仓收费。',
'单边fee10bp、half-spread1bp、slippage2bp；impact=0.5×滞后20完整日sample log-return sigma×sqrt(实际预算/quoteADV)，ADV参与率≤0.1%。四项同时1/2/3倍，tick损失单列；现货多头无需资金费/借币。过滤器为Oct1快照，价差/滑点/冲击为估计，缺L2、TCA、历史动态过滤器/盘口、队列、部分成交和延迟，未证明实盘容量。现金收益为0。','',
'## 三项验证与固定失败判据','',
'Walk-forward：2025和2026各03-18UTC00:01至09-14UTC00:01，180日连续OOS、六个30日折；180日滚动train、3日gap、purge0（无未来标签/拟合）。首OOS183从cash启动，跨折现金/units/desired连续。每场259382分钟及交易参考NAV点计算整体DD；所有逐折净收益/DD/Sharpe365/Calmar和连续OOS保存，不平均组件风险。两段均已反复研究，只是开发验证历史，不能称未触碰最终测试集。',
'Sensitivity：entry与exit同时变化，两个年份×BTC/ETH/组合共六面3×3；全部1/2/3x收益、分钟DD、Sharpe365、Calmar、正收益/正Sharpe比例、12条相邻边和2sd描述性cliff保存。正收益平台不等于资格平台；相同NAV不能算独立样本。没有OOS择优后独立验证，也没有声称通过多重选择偏差校正。',
'Costs：完整费用/价差/滑点/成交量相关冲击压力完成，报告各场景cost、成本占初始本金比、reference毛PnL/成本、往返数、参与率、拒单和终点平仓。沿用只读同期持有与现金比较，持有不是等风险超额收益基准。',
'八个固定门槛：三档成本净正、1x至少4/6正折、3x分钟DD≤25%、同面3x正收益比例≥60%、1x至少2往返、参考毛PnL/1x成本≥2.5、无负余额、终点flat。passed只表示本轮历史数值门槛通过，尚待独立长时观察。',
'参考[pandas EWM官方文档](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)和[Binance行情文档](https://developers.binance.com/en/docs/binance-spot-api-docs/rest-api/market-data-endpoints)，2026-10-05访问；本地pandas2.2.3未升级，文档不是收益证据。','',
'## 全部配置和三档成本','',
'|年份|资产|entry|exit|原权重|本金|新/旧|1x收益%|2x收益%|3x收益%|3x分钟DD%|1x正折|1x往返|资格/失败|','|---|---|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|']
for c in r['configs'].values():
 z=c['scenes'];lines.append(f"|{c['year']}|{c.get('asset','组合')}|{c['entry_days']}|{c['exit_days']}|{c['raw_weights']}|{c['capital_usdt']}|{'新' if c['is_new'] else '旧只读'}|{z['1']['net_return_pct']:.5f}|{z['2']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 全部3x逐折','', '|年份|资产|entry|exit|六折收益%|前五折合计%|末折%|','|---|---|---:|---:|---|---:|---:|']
for c in r['configs'].values():
 z=c['scenes']['3'];a=', '.join(f"{q['net_return_pct']:.4f}" for q in z['folds']);lines.append(f"|{c['year']}|{c.get('asset','组合')}|{c['entry_days']}|{c['exit_days']}|{a}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['','## 只读旧基准','', '|年份|配置|3x收益%|分钟DD%|原资格|','|---|---|---:|---:|---|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['status']}|")
lines+=['','## 原冻结SMA65前向模拟跨日续接','',
'原SMA65±1%、BTC75/ETH25、1500/500和原浮点交易核算不变，未应用本轮exit20/40或67.5历史资金分配。冻结计划SHA2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81不变，仍collecting至2027-03-31UTC00:01。',
'来源233340 state/report，从Oct4 23:10续接至Oct5 01:10UTC；保留4273旧NAV前缀，追加120闭合minute及1个00:01参考点，共4394点，累计4389分钟（73小时9分，3完整日）。每天使用65个此前已完成日收盘，在Oct5UTC00:01按原SMA65/±1%与前20日quoteADV/sigma判断；本次两币均hold_long，三成本场景6个账户均无新成交，数量/现金/成本/trades保持。nextstate的desired和下一日决策时间保存；没有重买、重置、缩放或强平。',
'每币1m API121条包含23:09重叠bar，与上一轮末bar全部字段相同；新增120条连续、闭合且两币对齐。每币65条完成1d，与Oct4决策的65日窗口核对64日重叠；最新日close和23:59分钟close一致，日close可得时间早于00:01真实minute open。4份原HTTP响应gzip、URL、status200、ms单位、取得UTC与原/压缩SHA保存；取得晚于执行参考，是延迟shadow重建，不是实时成交证明。',
'|观察|成本|累计收益%|累计DD%|本段收益%|新增成交|','|---|---|---:|---:|---:|---:|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['new_executions']}|")
lines+=['','3个观察定义9场景finish rejected仅说明不足180天/六折，不终止原冻结长期计划。下一日决策Oct6UTC00:01，之前续接闭合mark。短期不年化、不称稳定实盘盈利或前向敏感性通过。','',
'## 留档、审计、复现和多重尝试','',
f"完整读取2773行登记簿、1339保留ID/1337规范定义、{len(p['prior_conclusions'])}轮全部结论、7份Freqtrade文件/zip成员、lookahead.csv和4份OOS检查；原快照只有2凭据式字段脱敏，非凭据性能完整且源SHA核对。初始16均已有实际证据，无未完成/缺结果补测条目。新36历史+3观察各自先reserve成功才计算。",
'历史独立审计162场景、42019884NAV点、19440因果决定、72当前/未来close扰动、588个成本化fill（408新）；独立pandas EMA/通道、Decimal成交、余额/成本、全部折指标与合并NAV/资格核对通过。前向独立审计9场景、4394点/4273旧前缀、6个日决定、每币65日/64日重叠、00:01参考轴和nextstate通过。原报告哈希和旧ledger记录不改。',
'全部39配置在两项审计通过后finish，15新历史passed、21新历史rejected、3partial rejected；原2773行和1339记录保留，新增78事件至2851行，1376规范定义/1378保留ID，无pending。所有负收益折、资格淘汰和不足观测均永久保存。',
'复现：`bash research/experiments/20261005T013340Z/reproduce.sh`；108新成本场景精确重放，54旧只读核验，9前向场景及nextstate重放，不HTTP、不写登记。diagnose.py/diagnostic.json保存全部108场景对旧exit30的NAV/收益/DD/前五折比较；行情parquet和大NAV留忽略data目录，Git保存轻量充分证据、源/数据SHA、代码、日志、全结果和图。',
'下一步：20日退出未减少2026前五折损失，40日实现路径等于30日，退出窗口本身未解决集中收益。后续可事前固定更短退出/EMA退出条件变体，用完整两轴邻域诊断；已测试精确配置只读，不在同一OOS挑最佳后称独立确认。','']
(T/'result.md').write_text('\n'.join(lines))
fig,axs=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for i,y in enumerate(('2025','2026')):
 for j,a in enumerate(('BTC','ETH','combination')):
  cells={(c['exit_days'],c['entry_days']):c for c in r['configs'].values() if c['year']==y and c.get('asset','combination')==a};v=np.array([[cells[x,e]['scenes']['3']['net_return_pct'] for e in (10,15,20)] for x in (20,30,40)]);ax=axs[i,j];im=ax.imshow(v,cmap='YlGn',vmin=0,vmax=100)
  for ii,x in enumerate((20,30,40)):
   for jj,e in enumerate((10,15,20)):
    c=cells[x,e];ax.text(jj,ii,f"{v[ii,jj]:.2f}%\n{c['status']} / {'new' if c['is_new'] else 'old'}",ha='center',va='center',fontsize=9,color='white' if v[ii,jj]>65 else 'black')
  ax.set(xticks=range(3),xticklabels=[10,15,20],yticks=range(3),yticklabels=['20 (new)','30 (old)','40 (new)'],title=y+' '+a,xlabel='Entry lookback days',ylabel='Exit lookback days; EMA50 +/-1.5%')
fig.colorbar(im,ax=axs.ravel().tolist(),label='180-day return,3x costs (%)',shrink=.75);fig.suptitle('Entry x exit windows | fixed BTC/ETH67.5/32.5 initial capital | exit30 read-only');fig.savefig(T/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved54configs162scenes and9partial outcomes with all folds/unchanged daily observer/limitations')
