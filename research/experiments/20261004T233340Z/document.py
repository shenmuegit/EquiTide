"""Save complete parameter/fold outcomes and describe limitations without selecting a winner."""
import json,gzip,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent;ROOT=T.parents[2]
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());s=r['summary'];p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
old=(ROOT/'research/experiments/20261003T212439Z/result.md').read_text()
# Preserve unchanged, fully specified accounting and signal descriptions as quoted methodology.
method=old.split('## 完整规则、预登记与资金含义')[1].split('## 三项验证和失败判据')[0]
method=method.split('原始权重')[0]
lines=['# BTC/ETH：61.5/38.5、73.5/26.5 的较宽分配邻域验证','',
'触发2026-10-04T23:33:40.315Z；先fetch/ff同步研究分支，基点c5dedfb4a804fd648e2051a30a8f81e4a67de3ed。使用三个指定验证技能，不下真实订单。spec不精确记录首工具时间，以登记事件及evaluation_started_utc/observation_started_utc为准。','',
'## 结论','',
f"36个新配置（24组件、12组合）先独立reserve，完成108成本场景；{len(s['passed'])}通过、{len(s['rejected'])}淘汰。{s['positive_1x']}/36在1x成本总收益为正、{s['positive_3x']}/36在3x成本为正。18个67.5/32.5旧配置54场景只读复用；全网格54配置162场景。",
'新增6组组合设置在2025、2026两个180日开发历史分别通过：BTC61.5/ETH38.5与BTC73.5/ETH26.5各配合entry10/15/20。2025的18新配置均通过；2026六新组合1x有4/6正折通过，12新单币组件只有3/6正折而淘汰。全部正收益淘汰仍永久保存。',
'预定中心entry15、BTC67.5/ETH32.5只读，没有根据本轮结果改中心。2026同权重三个entry产生相同实现NAV，因此六个新参数对只有两条新2026路径，不能当六份独立确认。前五折合计仍为负，最后一折贡献全部净利润；较宽分配邻域资格一致不修复利润集中。更多BTC降低两段总收益和2025回撤，略升2026回撤。','',
'## 固定规则与实际资金','',method,
'权重原值[.615,.385]、[.675,.325]、[.735,.265]为2000USDT初始资金份额，分别1230/770、1350/650、1470/530独立账户；不自动归一化、维持敞口、再平衡或转账。61.5/73.5的组件按自身本金重算冲击、tick和LOT，组合优先复用本轮组件绝对NAV相加一次，不再乘权重，不缩放旧净值。67.5旧spec/archive/report和登记记录不改。',
'IOC立即完整成交为假设；买price上取tick、卖下取tick、qty下取LOT，残余现金保留。PRICE/LOT/NOTIONAL/VWAP5和参与率拒单不改余额，后续决策允许重试；完整历史终点平仓收费。完整规则、过滤器、参数、时间及fingerprint见spec。','',
'## 三项验证','',
'Walk-forward完成：两段各03-18UTC00:01至09-14UTC00:01，180日、六个30日折；180日滚动train、3日gap、purge0（无未来标签或拟合）；跨折现金/持仓/desired连续，信号仅用完成日，次日00:01参考成交。每场259382分钟及执行NAV点计算整体DD，不平均单组件风险；所有逐折和连续OOS指标见report。两段历史均反复使用，是开发验证，不能称未触碰最终测试集。',
'Sensitivity完成：entry10/15/20与原BTC资金份额61.5/67.5/73.5双轴，BTC/ETH/组合×两年份六面；全部成本净收益、分钟DD、Sharpe365、Calmar、邻接边/2sd描述性cliff完整保存。组件权重轴是实际资金规模/舍入/冲击敏感性；同路径重复不当独立样本。',
'Costs完成：单边fee10bp、halfspread1bp、slippage2bp，impact=0.5×滞后20完整日sample log sigma×sqrt(实际预算/quoteADV)，参与率≤0.1%；四项同时1/2/3倍，tick损失单列，终点平仓计成本。现货多头无资金费/借币，现金收益0；Oct1静态交易过滤器、缺历史盘口和TCA、IOC部分成交和延迟均为限制，未证明实际容量。',
'八个固定门槛：所有成本净正、1x至少4/6正折、3x整体DD≤25%、同面3x正收益比例≥60%、1x至少2往返、参考毛PnL/1x成本≥2.5、无负余额、终点flat。12个2026新单币只失败four_positive_1x_folds；组合资格由真实合并NAV独立核算。','',
'参考[pandas EWM官方说明](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)的span/adjust=False递推和[Binance官方行情文档](https://developers.binance.com/en/docs/binance-spot-api-docs/rest-api/market-data-endpoints)，2026-10-04查阅；本地pandas2.2.3未升级，文档不作为盈利证据。','',
'## 全部配置三档成本','',
'|年份|资产|entry|原权重|本金|新/旧|1x收益%|2x收益%|3x收益%|3x分钟DD%|1x正折|1x往返|资格/失败|','|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|']
for c in r['configs'].values():
 z=c['scenes'];lines.append(f"|{c['year']}|{c.get('asset','组合')}|{c['entry_days']}|{c['raw_weights']}|{c['capital_usdt']}|{'新' if c['is_new'] else '旧只读'}|{z['1']['net_return_pct']:.5f}|{z['2']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 全部3x逐折','', '|年份|资产|entry|原权重|六折收益%|前五折累计%|末折%|','|---|---|---:|---|---|---:|---:|']
for c in r['configs'].values():
 z=c['scenes']['3'];a=', '.join(f"{q['net_return_pct']:.4f}" for q in z['folds']);lines.append(f"|{c['year']}|{c.get('asset','组合')}|{c['entry_days']}|{c['raw_weights']}|{a}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['','## 只读基准比较','', '|年份|旧配置|3x收益%|分钟DD%|原资格|','|---|---|---:|---:|---|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['status']}|")
lines+=['','## 原冻结模拟延续','',
'原SMA65±1%、BTC75/ETH25、1500/500、原浮点账户不变；冻结计划SHA2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81不变。读取213240源state/report，从Oct4 21:10至23:10UTC，保留4153旧NAV前缀，追加120闭合minute至4273点，累计4269分钟（71小时9分，2完整日）。Oct4日决策已处理；本段无新决策/参考点/成交，数量、现金、desired、trades和成本均保留，不重买、不缩放、不强平。',
'每币API121条含21:09重叠bar，与旧末bar全部字段相同；120条新minute连续、closedTime+1≤23:10且两币对齐。保留2份原HTTP字节gzip、原/压缩SHA、URL、status200、毫秒单位及取得UTC。取得晚于截止，是延迟shadow重建，不是实时成交证明。',
'|观察|成本|累计收益%|累计DD%|本段收益%|新增成交|','|---|---:|---:|---:|---:|---:|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['new_executions']}|")
lines+=['','3个实际观察定义9场景finish rejected仅说明不足180天/六折，不终止原计划collecting至2027-03-31UTC00:01。下一日决策Oct5UTC00:01，之前只追加闭合mark，跨日须完成日数据、原SMA65/1%、滞后成本及真实00:01open。短期不年化，不称稳定盈利或前向敏感性通过。','',
'## 留档、独立审计与复现','',
f"完整读取2695行ledger/1300保留ID/1298规范定义、{len(p['prior_conclusions'])}轮完整结论、7份既有Freqtrade文件/zip成员、lookahead.csv和4份oos检查代码。既有快照仅2凭据式字段脱敏，所有性能和非凭据key保留，源SHA重新核对；初始16均已有实际结果，无pending。",
'实际reserve36历史＋3观察定义后计算。审计162场景42019884NAV点、19440因果决策、72当前/未来close扰动、540fill（360新）；独立pandas EMA/通道/Decimal成交/成本/余额/折指标/合并NAV/门槛校验。原模拟审计9场景4273点及4153点旧前缀、下一state、持仓和成本连续性。两项审计通过后finish全部39结果。',
'复现108新场景精确重放、54旧只读核验、9观察及nextstate重放，不新HTTP、不新登记。原2695行和1300记录保留，新增78事件至2773行、1337规范定义/1339ID，pending0。所有结果包括收益为正但资格淘汰、模拟亏损完整提交。',
'复现：`bash research/experiments/20261004T233340Z/reproduce.sh`。prepare仅首次reserve使用。行情parquet和大NAV留忽略data目录；Git保存spec、report、压缩信号成交、原API响应、完整历史快照、哈希、中文报告、图和日志。普通git凭据不可用则GitData API force=false，核对远程parent/tree/ref和本地暂存字节后报告commit。','',
'结论：新增两权重×三个entry历史合格，较宽分配邻域没有孤立峰值迹象，但重复开发历史、多重尝试和末折依赖未消除，原模拟仍短，收益正负以本段结果为准。保留证据，尚无稳定实盘盈利证据。','']
lines+=['','下一步：此前多轮调整初始权重仍未改变2026末折集中，后续优先预登记退出规则/窗口变化以检查是否能降低前五折损失；勿继续仅缩窄权重，勿据同一OOS选胜者后称独立确认。']
(T/'result.md').write_text('\n'.join(lines))
fig,axs=plt.subplots(2,3,figsize=(15,9),layout='constrained');weights=r['plan']['grid']['BTC_initial_weights']
for i,y in enumerate(('2025','2026')):
 for j,a in enumerate(('BTC','ETH','combination')):
  d={(c['BTC_weight'],c['entry_days']):c for c in r['configs'].values() if c['year']==y and c.get('asset','combination')==a};v=np.array([[d[w,e]['scenes']['3']['net_return_pct'] for e in (10,15,20)] for w in weights]);ax=axs[i,j];im=ax.imshow(v,cmap='YlGn',vmin=0,vmax=100)
  for ii,w in enumerate(weights):
   for jj,e in enumerate((10,15,20)):
    c=d[w,e];ax.text(jj,ii,f"{v[ii,jj]:.2f}%\n{c['status']} / {'new' if c['is_new'] else 'old'}",ha='center',va='center',fontsize=9,color='white' if v[ii,jj]>65 else 'black')
  ax.set(xticks=range(3),xticklabels=[10,15,20],yticks=range(3),yticklabels=['61.5/38.5','67.5/32.5 (old)','73.5/26.5'],title=y+' '+a,xlabel='Entry days; exit30 EMA50',ylabel='BTC/ETH initial funded fractions')
fig.colorbar(im,ax=axs.ravel().tolist(),label='180-day return,3x costs (%)',shrink=.75);fig.suptitle('Allocation neighbourhood: 61.5/38.5 and73.5/26.5 new | 67.5/32.5 read-only');fig.savefig(T/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved all54configs/162scenes plus9partial outcomes, complete folds and limitations')
