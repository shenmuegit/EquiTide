"""Save all positive, rejected and partial outcomes without selecting new parameters."""
import json,gzip,collections
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());s=r['summary'];cfg=r['configs'];grid=r['plan']['grid'];p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
lines=['# BTC/ETH：57.5/42.5与62.5/37.5初始分仓的边界验证','',
'触发2026-10-03 15:23:18UTC，首工具15:23:35UTC；先fetch并ff同步codex/strategy-research，基点ce13986f2b29fe4f6e12d0e91ce54327f7deffa8。使用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs。真实行情回测和原冻结规则延迟模拟；无真实订单。','',
'## 本轮结论','',
f"36新配置（24按实际本金重算的组件＋12组合）先reserve，108成本场景完成。{s['positive_1x']}/36在1x成本净正，{s['positive_3x']}/36在3x成本净正；{len(s['passed'])}通过、{len(s['rejected'])}淘汰。18既有60/40配置/54场景只读复用，完整54配置/162成本场景永久留档。",
'新增6组相同完整规则/权重组合在2025与2026分别通过：entry10/15/20×BTC57.5或62.5%、ETH42.5或37.5%。2025全部18新配置通过；2026的6新组合达到4/6正折并通过，12新单币组件只有3/6正折而淘汰，组合资格独立核算。旧60/40的3个组合仍两段合格，完整9/9参数对通过；这是离散网格描述，不证明整个连续区间，也不是新未触碰历史证据。',
'预定中心entry15、BTC60/ETH40（旧锚点）；未因结果更换参数或模拟方案。2026同权重的三个入场窗口产生相同NAV，本轮六个新组合设置只有两条不同实现路径，不是六份独立证据。','',
'|年份|entry|BTC/ETH原权重|新/复用|3x净收益%|整体分钟DD%|1x正折|前五折3x%|末折3x%|资格|','|---|---:|---|---|---:|---:|---:|---:|---:|---|']
for c in cfg.values():
 if c['role']=='combination' and c['entry_days']==15:
  z=c['scenes']['3'];lines.append(f"|{c['year']}|15|{c['raw_weights']}|{'新' if c['is_new'] else '旧'}|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|{c['status']}|")
lines+=['','## 完整规则、预登记与资金含义','',
'同上一轮EMA50确认通道：决策i只用完成日C[i-1]；若C[i-1]<min(C[i-31:i-1])或float(C[i-1])<EMA50[i-1]×0.985，desired=cash；否则若C[i-1]>max(C[i-entry-1:i-1])且float(C[i-1])>EMA50[i-1]×1.015，desired=long；其余/相等保持，退出优先。通道区间截至i-2。entry10/15/20、退出30、EMA50±1.5%全部事前固定。',
'EMA[0]为首完成日float close，alpha=2/51、adjust=False、从日0递推且跨折不重置；首seed早于180日train。通道及成交账户用Decimal28。OOS第183日cash/desired-cash启动，日close UTC00:00可用，随后00:01真实minute open参考成交。无拟合、未来标签、测试选参、arming、日内stop、杠杆、空头或加仓。',
'原始权重[.575,.425]、[.60,.40]、[.625,.375]分别为2000USDT的独立1150/850、1200/800、1250/750初始分仓。无自动归一化、维持敞口、再平衡或转账。新组件按自身实际本金重新计算冲击与tick/LOT；新组合复用刚完成组件绝对NAV逐点相加，初始2000，只加一次，不再乘权重、不平均风险指标、不线性缩放旧净值。18个60/40配置不重复生产回测，保留旧spec/report/archive/NAV/hash和原ledger资格。',
'沿用marketable LIMIT IOC立即完整成交假设，买price上取tick、卖下取tick、qty下取LOT，残余cash保留。PRICE/LOT/NOTIONAL/VWAP5及参与率拒单不改余额，后续日决策可重试。历史终点实际模拟平仓含成本。所有完整规则、参数、资金、时间和组件fingerprint见各spec。','',
'## 三项验证和失败判据','',
'Walk-forward完成：2025和2026各03-18UTC00:01至09-14UTC00:01，连续180日，6×30日折；180日滚动train、3日gap、purge0（无未来标签），固定规则不拟合。现金、数量、desired跨折连续，不逐折重开。每场259382分钟/执行NAV点，逐折收益/DD/Sharpe365/Calmar及整体分钟DD、折复利核对；两段历史已反复开发使用，不能称未触碰最终测试集或独立前向。',
'Sensitivity完成：BTC、ETH、组合×两年份六个3×3面，entry和初始资金分配双轴；全部1/2/3成本场景、邻接边和2sd cliff描述留档report.json/sensitivity.csv。组件的权重轴表示实际本金/冲击/舍入敏感性。旧源资格原样保存，本轮网格邻域资格另报；路径重复不能当独立样本。',
'Costs完成：单边fee10bp、halfspread1bp、slippage2bp；impact=0.5×滞后20完整日sample log sigma×sqrt(实际预算/quoteADV)，参与率≤0.1%。四项同时1/2/3倍，tick损失另列，终点平仓收费。360新模拟fill＋180旧只读fill独立核对；现货多头资金费/借币不适用，USDT现金收益0。Oct1静态交易所过滤器应用于历史是建模假设，未校准历史L2、真实IOC部分成交/队列/延迟、TCA和容量。',
'固定八门槛：所有成本净正；1x至少4/6正折；3x整体分钟DD≤25%；同面3x正收益比例≥60%；1x至少2往返；参考毛PnL/1x成本≥2.5；无负余额；终点flat。组合往返为两组件之和，不代表每币或每折合格。12个新2026单币组件淘汰仅four_positive_1x_folds；完整正收益淘汰记录仍是已测试结果。','',
'参考[pandas EWM官方说明](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)确认递推及[Binance官方行情接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)的minute/startTime/endTime；2026-10-03查阅，不是利润来源证据，本地pandas2.2.3未升级。','',
'## 全部54配置及三档成本','',
'|年份|资产|entry|原权重|实际本金|新/复用|1x%|2x%|3x%|3x整体DD%|1x正折|1x往返|资格/失败|旧原资格|','|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfg.values():
 z=c['scenes'];lines.append(f"|{c['year']}|{c.get('asset','组合')}|{c['entry_days']}|{c['raw_weights']}|{c['capital_usdt']}|{'新' if c['is_new'] else '复用'}|{z['1']['net_return_pct']:.5f}|{z['2']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|{c.get('source_record_status','—')}|")
lines+=['','## 全部3x逐折结果','', '|年份|资产|entry|原权重|六折收益%|前五折累计%|末折%|','|---|---|---:|---|---|---:|---:|']
for c in cfg.values():
 z=c['scenes']['3'];a=', '.join(f"{q['net_return_pct']:.4f}" for q in z['folds']);lines.append(f"|{c['year']}|{c.get('asset','组合')}|{c['entry_days']}|{c['raw_weights']}|{a}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['','## 只读比较','', '|年份|旧配置|3x收益%|整体DD%|原资格|','|---|---|---:|---:|---|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['status']}|")
lines+=['','## 原冻结模拟续接至15:10UTC','',
'原SMA65±1%、BTC75/ETH25、1500/500、原浮点fill和费用账户保持，冻结计划SHA2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81不变。读112118源state/report，从11:10续接15:10UTC；2112旧NAV前缀逐点保留，追加240闭合分钟至2352点、累计2349分钟（39小时9分，1完整日）。无新日决策、参考执行点或成交，没有重买、缩放、再平衡或强平。',
'每币API241条（含11:09 overlap，与旧末bar所有字段匹配），240新bar逐分钟连续、closedTime+1≤15:10、两币轴匹配。留原HTTP字节gzip、原/压缩SHA、URL、status200、毫秒单位和获取UTC。获取晚于截止，是延迟模拟重建，不是实时交易。','',
'|观察|成本|累计净收益%|累计DD%|本段收益%|新增成交|','|---|---:|---:|---:|---:|---:|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['new_executions']}|")
z=f['configs']['forward_snapshot_combo']['scenes']['3'];lines+=['',f"原模拟3x累计{z['net_return_pct']:.5f}%、DD{z['max_drawdown_pct']:.5f}%；3个实际观察配置/9场景finish rejected仅表示不满足180日六折资格，长期计划仍collecting至2027-03-31UTC00:01。下一轮从15:10保持原状态；Oct4UTC00:01前只追加闭合marks，跨日时须原SMA65、滞后20日成本、真实00:01open。短样本不年化，也不称前向敏感性已通过。",'',
'## 独立审计、复现和全量保留','',
'4份真实525600minute parquet、daily_inputs和元数据核对SHA/闭合/可用时间/连续轴；pandas EMA与独立区间排序重建19440因果决策，24新组件×3次当前/未来close扰动72次不影响过去/当时决定。这是同配置工程审计，不是新增收益参数变体。',
'独立重建162场景42019884分钟/执行NAV点，360新＋180旧fill核对真实预算/ADV/sigma/参与率/Decimal价格数量费用余额；核对组合逐点绝对NAV相加、逐折/整体风险、终点平仓和门槛。9原模拟场景核对原HTTP/重叠/2112旧前缀/2352完整轴及state、费用不变。',
'108新场景精确重放、54旧场景只读核验、9累计观察精确重放，包括nextstate，无新HTTP/ledger写。39新定义独立reserve/finish，绑定最终报告SHA。原2071行字节及988记录不变；累计1025规范定义/1027保留ID/2149行，全部有实际结果，无reserved。',
f"已全文读取{len(p['prior_conclusions'])}轮结论、完整ledger、{len(p['legacy_results'])}份Freqtrade JSON/zip成员、lookahead.csv及{len(p['checks_read'])}份检查代码，初始16条均已有实际结果关联。历史快照完整保留性能指标；只将2个凭据式配置字段替换[REDACTED]，源字节/成员SHA和所有非凭据key保留，未输出字段值。",
'保留39spec、36新压缩成交/信号/账户档案、54网格引用、162行敏感性数据、数据哈希、响应、报告、图和代码/日志。市场原大数据及全NAV在忽略data目录。复现：`bash research/experiments/20261003T152318Z/reproduce.sh`；prepare.py仅首次reserve使用。普通git凭据不可用时GitData API force=false推送；最终简报核对远端ref/parent/tree及本地/暂存字节后报告SHA。',
'结论：57.5/42.5、62.5/37.5达到2026折一致性门槛，本轮新增6组跨期历史合格组合，但只有2条新的2026实现路径，且前五折仍负、末折依赖明显。保留全部正收益淘汰和模拟亏损证据。重复开发历史正收益不能称稳定实盘盈利。','']
(T/'result.md').write_text('\n'.join(lines))
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for i,y in enumerate(('2025','2026')):
 for j,a in enumerate(('BTC','ETH','combination')):
  d={(c['BTC_weight'],c['entry_days']):c for c in cfg.values() if c['year']==y and c.get('asset','combination')==a};v=np.array([[d[w,e]['scenes']['3']['net_return_pct'] for e in (10,15,20)] for w in (.575,.6,.625)]);ax=axes[i,j];im=ax.imshow(v,cmap='YlGn',vmin=0,vmax=max(c['scenes']['3']['net_return_pct'] for c in cfg.values()))
  for ii,w in enumerate((.575,.6,.625)):
   for jj,e in enumerate((10,15,20)):
    c=d[w,e];ax.text(jj,ii,f"{v[ii,jj]:.2f}%\n{c['status']} / {'new' if c['is_new'] else 'old'}",ha='center',va='center',fontsize=9,color='white' if v[ii,jj]>60 else 'black')
  ax.set(xticks=range(3),xticklabels=[10,15,20],yticks=range(3),yticklabels=['57.5/42.5','60/40','62.5/37.5'],title=y+' '+a,xlabel='Entry days; exit30 EMA50',ylabel='BTC/ETH initial funded fractions')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day return,3x costs (%)',shrink=.75);fig.suptitle('57.5/42.5 and62.5/37.5 allocation neighbourhood: combinations pass | 60/40 read-only');fig.savefig(T/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved complete54cell evidence and originalpartial outcomes')

# CSV asset label describes the combined account; allocation is in BTC_initial_weight/spec.
import csv,io
p=T/"sensitivity.csv"
rows=list(csv.reader(io.StringIO(p.read_text())))
for row in rows[1:]:
 if row[3]=="combination":row[4]="combination"
with p.open("w",newline="") as out:csv.writer(out,lineterminator="\n").writerows(rows)
