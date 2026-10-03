"""Retain complete entry/allocation surfaces, actual funded costs and original simulated losses."""
import collections,gzip,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary'];prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));fresh={n:c for n,c in cfg.items() if c['is_new']};reasons=collections.Counter(k for c in fresh.values() for k in c['failed_criteria'])
lines=['# 本轮：EMA50确认通道的初始BTC/ETH分仓权重','',
 '触发2026-10-03 05:20:49UTC；首工具05:21:27UTC。codex/strategy-research先fetch/ff同步，基点4573a312faae840a37278e9fc162e3d1d23f6ce1。使用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs。真实行情历史回测及冻结规则延迟模拟，无真实订单。','',
 '## 筛选结论','',
 f"36新配置先独立reserve，108成本场景完成：24个实际资金规模组件＋12组合、28013256分钟/执行NAV点、{s['actual_component_fills']}笔新组件模拟成交。{s['positive_1x']}/36一倍、{s['positive_3x']}/36三倍成本净正；{len(s['passed'])}历史门槛通过、{len(s['rejected'])}淘汰。18个既有75/25配置/54场景只读复用，完整54配置/162场景网格保留。没有按线性比例缩放旧净值或重复生产回测旧配置。",
 f"新增{len(s['new_both_periods_passed_combination_pairs'])}组相同完整规则/权重组合在2025和2026均通过：entry10/15/20×原始BTC60/90%、ETH40/10%；退出30日、EMA50±1.5%。加上3个旧75/25组合，完整9/9组合参数对在两段分别通过。2026每个权重的3个入场窗口实现相同净值，整个9格只有3条不同NAV；6个新参数对只有2条2026路径，不能算6份独立盈利证据。",
 f"12个淘汰全部是2026单币组件（BTC1200/1800与ETH800/200），原因均{dict(reasons)}。这些组件也全部实际净正，但仅3/6正折；组合有4/6正折且按真实连续组合净值独立过门槛，不要求每组件单独合格。没有负收益新历史配置，淘汰完整结果仍永久保存。原冻结模拟仍负，所有既往负收益记录保持。",'',
 '### 预定中心与新权重比较','',
 '事前中心entry15、75/25为旧结果锚点；本轮固定60/40和90/10两侧，不因结果改变参数或原模拟计划。','',
 '|年份|entry日|原BTC/ETH权重|新/复用|3x净收益%|整体分钟DD%|1x正折|前五折3x%|末折3x%|历史资格|','|---|---:|---|---|---:|---:|---:|---:|---:|---|']
for c in cfg.values():
 if c['role']=='combination' and c['entry_days']==15:
  z=c['scenes']['3'];lines.append(f"|{c['year']}|15|{c['raw_weights']}|{'新' if c['is_new'] else '旧'}|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|{c['status']}|")
lines+=['',
 '新60/40的entry15组合三倍2025 +48.53838%/DD14.08109%、2026 +16.36465%/DD13.11195%。比旧75/25收益两段更高，2025回撤也增加、2026回撤略降，风险改善并不一致。2026前五折-1.61399%、末折+18.27358%，仍依赖最后一折；全部60/40入场参数的2026路径相同。',
 '新90/10的entry15组合三倍2025 +25.41083%/DD12.92102%、2026 +10.67449%/DD13.53229%。更低ETH初始仓位减少历史收益，2026整体回撤反而略高。2026前五折-1.14801%、末折+11.95980%，仍集中。权重变化只改变组合初始资金，后续真实持仓权重随净值漂移，不能称恒定60/40或90/10敞口。',
 '新增跨期资格区域为完整预定网格的历史描述；相同重复历史上的策略/权重探索存在多重选择偏差，不能当独立验证、确定alpha或稳定实盘利润。原冻结方案仍SMA65±1%、75/25，本轮不替换。','',
 f"39个新定义全部finish（36历史＋3截止观察）。累计908规范定义、910保留ID、1840登记行，无reserved或缺结果。此前{prior['lines']}行/{prior['canonical']}规范定义/{len(prior['records'])}记录、{len(prior['prior_conclusions'])}轮全文结论、{len(prior['legacy_results'])}份Freqtrade原JSON/zip成员及{len(prior['checks_read'])}份checks代码全文已读。初始16条均有实际关联结果，不代表全合格。",'',
 '## 假设、来源与预登记','',
 '前两轮EMA确认退出30日已有75/25跨历史合格区域，更短退出没拓宽区域。本轮假设初始分仓权重可能改变组合持续回撤及折收益一致性；更多ETH可能增收益/回撤，更多BTC可能降低收益但不保证降低组合最大回撤。entry10/15/20×初始BTC60/75/90%全网格与75%中心、exit30/EMA50/band1.5%、数据/成本/门槛在结果前冻结。24新组件按1200/800和1800/200实际规模重算，12新组合复用这些刚完成的对应成本净值；18旧1500/500及75/25配置保存spec/report/archive/NAV哈希，仅读取。',
 '2026-10-03参考[pandas EWM官方文档](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)的adjust=False、alpha=2/(span+1)递推；沿用上一轮Python float EMA、独立审计本地pandas2.2.3，无运行时升级。权重研究假设是本轮提出，文档没有正收益证据。续接真实minute接口参考[Binance官方行情文档](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)。','',
 '## 完整规则、原权重与资金含义','',
 '日决策i只用已完成C[i-1]。若C[i-1]<min(C[i-31:i-1])或float(C[i-1])<EMA50[i-1]×0.985，desired=cash；否则若C[i-1]>max(C[i-entry-1:i-1])且float(C[i-1])>EMA50[i-1]×1.015，desired=long；其余/相等保持，退出优先，通道参照止于i-2，排除测试收盘。采用日close，没有arming记忆、日内stop、杠杆、空头或加仓。',
 'EMA[0]=数据集首个完成日float close，alpha=2/51，从日0递推，跨折不重置，seed早于180日train。通道比较、成交/现金/数量用Decimal28，EMA浮点。OOS183由cash/desired-cash起步；无模型拟合、未来标签、OOS调参、每折重开。前日close UTC00:00可得，随后UTC00:01真实分钟open参考执行。',
 'raw weights完全保留[0.6,0.4]、[0.75,0.25]、[0.9,0.1]，分别代表2000USDT初始1200/800、1500/500、1800/200分仓；没有自动归一化、维持目标敞口、再平衡、转账或再投资跨账户。components用其实际金额计算冲击/tick/LOT，组合=sum两个对应绝对NAV，初始2000，没有二次乘权重、平均收益/Sharpe/DD或从其他本金线性缩放。组件敏感性图的BTC占比轴代表对应本金/冲击/舍入设置，不能解释为单币自身又乘此权重。',
 '沿用marketable LIMIT IOC立即完整成交假设；买price向上、卖向下tick，qty向下LOT，余现金留存。PRICE/LOT/NOTIONAL/VWAP5及参与率约束拒单不改余额、下次日决策可重试。历史边界终止平仓含成本。全部完整规则、资金、时间和组件fingerprint在spec。','',
 '## 三项验证','',
 'Walk-forward完成：2025及2026各03-18UTC00:01至09-14UTC00:01、连续180日/6×30折；180日滚动train、3日gap、purge0（无未来标签）。固定规则/原权重不拟合或测试集选参，cash/units/desired跨折连续。每场259382分钟/执行NAV点核算整体回撤及逐折收益/DD/Sharpe365/Calmar，折复利核对完整净值。两段反复用于开发，不是未触碰最终测试集、独立前向或跨年池化收益。',
 'Sensitivity完成：BTC、ETH、组合×两年份六个3×3面，entry与初始BTC占比双轴；全部162成本行CSV含收益/整体分钟和日DD/Sharpe/Calmar/正折/往返/费用/集中度。六面每格三倍净收益和正Sharpe比例均9/9；组合两段9/9达固定门槛，但2026单币仍0/9达门槛。相邻12边及2sd cliff只是描述，不是显著性/最优参数证据，路径重复另列。旧记录原资格/门槛完全保留，当前全邻域资格另报。',
 'Costs完成：单边fee10bp、halfspread1bp、slippage2bp；impact=0.5×滞后20完整日sample log sigma×sqrt(实际交易预算/quoteADV)，参与率≤0.1%。四项同时1/2/3倍，tick损失单列、终止平仓收费。360笔新模拟fill＋180笔旧只读fill独立核对；现货多头资金费/借币不适用，USDT/现金收益0。Oct1静态交易所过滤元数据应用于历史为假设；缺历史L2/队列、真实IOC/部分成交/延迟、TCA及容量校准。',
 '门槛固定：各成本净正；1x≥4/6正折；3x完整分钟DD≤25%；同面3x正收益比例≥60%；1x≥2往返；参考价毛PnL/1x成本≥2.5；无负余额；终止flat。组合往返为组件之和，不表示每币或每折均盈利。','',
 '## 全部54配置、实际资金及三档成本','',
 '|年份|资产|entry日|原BTC/ETH权重|实际本金USDT|新/复用|1x%|2x%|3x%|3x分钟DD%|1x正折|1x往返|本轮资格/失败|旧原资格|','|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfg.values():
 z=c['scenes'];lines.append(f"|{c['year']}|{c.get('asset','组合')}|{c['entry_days']}|{c['raw_weights']}|{c['capital_usdt']}|{'新' if c['is_new'] else '复用'}|{z['1']['net_return_pct']:.5f}|{z['2']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|{c.get('source_record_status','—')}|")
lines+=['','## 全部54配置三倍逐折结果','', '|年份|资产|entry日|原权重|六折收益%|前五折累计%|末折%|','|---|---|---:|---|---|---:|---:|']
for c in cfg.values():
 z=c['scenes']['3'];folds=', '.join(format(x['net_return_pct'],'.4f') for x in z['folds']);lines.append(f"|{c['year']}|{c.get('asset','组合')}|{c['entry_days']}|{c['raw_weights']}|{folds}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['','## 敏感性面与实现路径数','', '|年份/资产|本轮通过/9|3x正收益比例|不同3x NAV/9|3x收益范围%|cliff/12|','|---|---:|---:|---:|---|---:|']
for group,v in r['sensitivity'].items():
 cells=[c for c in cfg.values() if c['year']+'_'+c.get('asset','combination')==group];a,b=v['metrics']['3']['return_range_pct'];lines.append(f"|{group}|{sum(c['status']=='passed' for c in cells)}|{v['metrics']['3']['positive_return_fraction']:.3f}|{len({c['scenes']['3']['NAV_sha256_f64le'] for c in cells})}|{a:.5f}至{b:.5f}|{sum(e['cliff_flag_2sd'] for e in v['adjacent_edges'])}|")
lines+=['','## 原样读取旧比较','', '|年份|旧配置|3x净收益%|完整分钟DD%|原资格|','|---|---|---:|---:|---|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['status']}|")
lines+=['','旧持有比较50/50，本轮初始权重60/40、75/25、90/10且持币/现金时间不同，不能直接宣称同风险超额收益。','',
 '## 原冻结方案累计1749分钟','',
 '原113625/forward_plan.json SHA2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81保持。原SMA65±1%、75/25实际1500/500、浮点fill和原成本账本保持。本轮读取015203源report/state，Oct3 01:40继续至05:10UTC，1542旧NAV点逐点保留（含两个过去日执行参考），追加210个闭合minute marks后1752点=初始＋两个旧日参考＋1749闭合分钟。没有新日决策、参考执行点、成交、重复首买、仓位缩放、重新平衡或本段强制平仓。',
 '每币真实API取211条1m，含01:39重叠bar并与旧末bar全字段匹配，210新bar连续、closeTime+1≤05:10；两个币时间轴一致。保存原HTTP字节gzip/原及gzip SHA、URL、status200、毫秒单位、取得UTC。取得晚于截止，是延迟shadow重建，不是真实/实时执行。','',
 '|观察|成本|累计净收益%|累计分钟/参考DD%|本段收益%|新增成交|','|---|---|---:|---:|---:|---:|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['new_executions']}|")
z=f['configs']['forward_snapshot_combo']['scenes']['3'];lines+=['',
 f"累计29小时9分，1完整日，组合三倍{z['net_return_pct']:.5f}%/DD{z['max_drawdown_pct']:.5f}%，本段{z['since_previous_mark_return_pct']:.5f}%，仍亏损。3观察/9场景实际完成，以rejected留档仅表示不满足180日/六折资格，原长期方案仍collecting至2027-03-31UTC00:01。没有新增前向敏感性/短样本年化指标。",
 '下一轮从本轮forward_state.json的05:10原现金/持币/desired/交易/费用继续。下一日决策Oct4UTC00:01前只追加闭合marks；跨日决策需原SMA65、前65完整日、滞后20日成本与实际00:01open，原冻结权重保持。新截止先reserve，旧截止只读。','',
 '## 独立审计、复现和留档','',
 '4份真实525600minute parquet、daily_inputs和交易所过滤元数据核对SHA、closed、可用时间、minute连续性、UTC00:01成交参考及两币时间轴；pandas EMA与排序收盘区间独立重建19440个因果决策。24新组件各3个当前/未来close扰动共72次，既有/当时决策不变；这属于同一配置工程检查，不是新增收益变体。',
 '360新＋180旧模拟fill独立核对真实预算/参与率/ADV/sigma/Decimal tick/LOT/费用/余额；独立重建162历史场景42019884分钟/执行NAV点，逐折和整体风险/费用/折复利/gates正确。组合逐点相加正确，资金等于raw weights×2000，没有第二次权重缩放。9原模拟场景核对raw响应/重叠、1542旧前缀、1752完整时间轴和原状态/费用保持。',
 '108新成本场景精确重放，54旧场景只读核验，9累计观察精确重放，包括nextstate；无新HTTP或ledger写。39finish绑定最终报告SHA；此前871记录/1762登记行逐项及字节保持。registry检查通过。保留39spec、36新完整压缩信号/成交/持仓档案、全部54网格引用/162成本行、中文报告/六面图、数据哈希、原HTTP及代码/日志/verification.json。大行情/全NAV位于忽略data/。',
 '扩展既往结果读取包含原Freqtrade zip结果/配置成员、meta和last_result，以及lookahead.csv。初始快照安全检查发现配置中2个非空凭据式字段，留档artifact_notes.json，在新快照中用[REDACTED]替换；原来源文件保持、源文件和成员SHA保留、所有性能指标和非凭据字段保留，没有输出字段值。策略计算和回测结果不受影响。',
 '复现：`bash research/experiments/20261003T052049Z/reproduce.sh`。prepare.py为首次reserve入口，已完成具体配置不重复执行。推送采用已连接GitHub的GitData API，force=false；实际SHA/push在最终运行简报经远端ref/parent/tree/本地文件核对后披露。',
 '结论：原资金占比邻域扩大到6个新增跨期历史合格参数对，但2026只有2条新实现路径且末折依赖显著，原冻结模拟仍负。继续观察原方案，并探索事先固定的新规则/权重；不能把本轮历史正收益称稳定实盘盈利。','']
(ROUND/'result.md').write_text('\n'.join(lines))
values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=Normalize(vmin=0,vmax=max(values));cmap=plt.get_cmap('YlGn');fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for iy,y in enumerate(('2025','2026')):
 for ix,asset in enumerate(('BTC','ETH','combination')):
  cells={(c['BTC_weight'],c['entry_days']):c for c in cfg.values() if c['year']==y and c.get('asset','combination')==asset};a=np.array([[cells[(w,e)]['scenes']['3']['net_return_pct'] for e in grid['entry_lookback_days']] for w in grid['BTC_initial_weights']]);ax=axes[iy,ix];im=ax.imshow(a,norm=norm,cmap=cmap)
  for i,w in enumerate(grid['BTC_initial_weights']):
   for j,e in enumerate(grid['entry_lookback_days']):
    c=cells[(w,e)];rgb=cmap(norm(a[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];tag=('P' if c['status']=='passed' else 'R')+(' / new' if c['is_new'] else ' / old');ax.text(j,i,f'{a[i,j]:.2f}%\n{tag} | ${c["capital_usdt"]}',ha='center',va='center',color='white' if lum<.48 else 'black',fontsize=10)
  ax.set(xticks=range(3),xticklabels=grid['entry_lookback_days'],yticks=range(3),yticklabels=['60/40','75/25','90/10'],xlabel='Channel entry (days); exit30 / EMA50',ylabel='Original BTC/ETH funded fractions',title=f'{y} {asset}')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day return,3x costs (%)',shrink=.75);fig.suptitle('Actual initial allocation sensitivity | P: historical pass; R: reject | 75/25 read-only');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved54 funded configurations/162cost rows,allfolds,six surfaces,6new cross-period pairs and9partial original scenes.')
