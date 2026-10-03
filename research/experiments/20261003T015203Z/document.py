"""Save all faster-exit results, raw-weight surfaces and original-plan daily continuation."""
import collections,gzip,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary'];prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));fresh={n:c for n,c in cfg.items() if c['is_new']};reasons=collections.Counter(k for c in fresh.values() for k in c['failed_criteria'])
lines=['# 本轮：EMA50确认通道的更快退出参数','',
 '触发2026-10-03 01:52:03UTC；首工具01:52:46UTC。codex/strategy-research先fetch/ff同步，基点016e09c113920aa40b7a73e4d9c7510fff6c20cb。使用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs。真实行情历史回测及冻结规则延迟模拟，无真实订单。','',
 '## 筛选结论','',
 f"36新配置独立reserve后完成108成本场景：24组件＋12组合、28013256分钟/执行NAV点、{s['actual_component_fills']}笔新组件模拟成交。{s['positive_1x']}/36在1x净正，{s['positive_3x']}/36在3x净正；{len(s['passed'])}项通过固定历史门槛、{len(s['rejected'])}项淘汰。18个原exit30具体配置/54场景仅读取旧结果，组成54配置/162场景完整网格，不重复登记或策略计算。",
 f"新增跨两段历史均通过的组合参数对为{len(s['new_both_periods_passed_combination_pairs'])}。6项新通过均为2026的组合，exit10/20×entry10/15/20；其对应2025配置均仅3/6正折而淘汰。新增没有拓宽两段历史共同合格区域：仍是旧exit30、entry10/15/20、EMA50±1.5%的3参数对；2026三对原净值相同，不是3条独立盈利路径。",
 f"失败原因次数（同配置可多项失败）：{dict(reasons)}。1个新配置2026 ETH entry20/exit10，1x+1.41764%、2x+0.35852%、3x-0.69166%，压力成本使盈利消失，完整负收益结果保存并finish。其余新配置虽三倍净正，也不等于达到折数/回撤等门槛。",'',
 '### 事前中心与旧基线','',
 '|年份|entry/exit日|新/复用|3x净收益%|整体分钟DD%|1x正折|前五折3x%|末折3x%|本轮全网格资格|','|---|---|---|---:|---:|---:|---:|---:|---|']
for c in cfg.values():
 if c['role']=='combination' and c['entry_days']==15:
  z=c['scenes']['3'];lines.append(f"|{c['year']}|15/{c['exit_days']}|{'新' if c['is_new'] else '旧结果'}|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|{c['status']}|")
lines+=['',
 '事前中心entry15/exit20：2025三倍+18.63402%/DD21.61074%，3/6正折，淘汰；2026三倍+13.31698%/DD13.32351%，4/6正折，通过。相比exit30，2025收益明显下降、DD上升；2026 DD相同、收益略降，前五折仍-1.38211%、末折+14.90509%。更快退出没有一致改善。',
 'exit10的2026组合entry10/15三倍+8.31725%/DD10.63163%，前五折+0.74312%、末折+7.51826%；entry20三倍+5.34732%/DD10.51085%，前五折+1.91605%、末折+3.36676%。回撤/末折集中有所下降但收益也下降，且对应2025全部淘汰。entry10和15在2026 exit10实现同一净值；exit20的3个入场参数亦实现同一净值。不会以重复实现数量增强独立证据。','',
 f"本轮39个新定义finish（36历史＋3新截止观察）。累计869规范定义、871保留ID、1762登记行，无reserved/缺结果。此前{prior['lines']}行/{prior['canonical']}规范定义/{len(prior['records'])}记录、{len(prior['prior_conclusions'])}轮完整结论、{len(prior['legacy_results'])}份Freqtrade JSON及{len(prior['checks_read'])}份checks代码全文已读并保存prior_summary.json.gz。初始16条均有实际关联结果；不代表全通过。",'',
 '## 假设、来源与预登记','',
 '在不改变联合确认数学规则的前提下，预定entry10/15/20×exit10/20/30、EMA50和±1.5%固定，中心15/20。假设更短退出通道能减少趋势回吐及末折集中，同时可能增加反复成交并错过反弹。所有时间、资金、完整规则和失败门槛在结果前冻结；实际新参数24组件重算资金相关成本，12新组合复用对应1500/500真实本金净值。exit30的18个完全相同配置保存源spec/report/archive/NAV哈希，读取既有结果；旧登记状态和原门槛保持，报告另列本轮完整邻域的描述资格。',
 '2026-10-03查阅[pandas EWM官方文档](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)，其adjust=False递推支持alpha=2/(span+1)。生产信号沿用上一轮Python float递推，独立审计本地pandas2.2.3 EWM；没有升级运行时。退出参数假设由研究提出，文档没有提供正收益证据。真实续接接口依据[Binance官方行情文档](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)。','',
 '## 完整规则、资金与数据边界','',
 '决策i只看完成C[i-1]；若C[i-1]<min(C[i-exit-1:i-1])或float(C[i-1])<E[i-1]×0.985，desired=cash；否则若C[i-1]>max(C[i-entry-1:i-1])且float(C[i-1])>E[i-1]×1.015，desired=long；其余/相等保留状态。退出优先，通道参照结束i-2，排除测试收盘，采用日close而非high/low，没有arming记忆。',
 'EMA50：E[0]=数据集首个完成日float close，alpha=2/51，从日0递推，跨折不重置；seed记忆早于180日train边界。通道比较与成交现金单位用Decimal28，EMA用float。OOS183以现金/desired-cash起步；没有模型拟合、未来标签、测试集调参、盘中止损、杠杆、空头、加仓或每折重开。',
 '前日close UTC00:00可得，次日UTC00:01真实分钟open参考成交；假设marketable LIMIT IOC立即按估计不利价格完整成交。买价向上/卖价向下tick，数量向下LOT，余现金留存，PRICE/LOT/NOTIONAL/VWAP代理及参与率约束拒单不改余额，下次日决策可重试；历史边界终止平仓收费。',
 '原始BTC75%/ETH25%为2000USDT初始独立分仓1500/500，不归一化、不再平衡、不转账，现金/持币跨折连续。组合为这两笔实际资金下成本化绝对NAV之和，初始2000，不二次加权、平均收益/风险或缩放其他本金下冲击。spec包含每组件实际本金和原权重。','',
 '## 三项历史验证','',
 'Walk-forward完成：2025及2026各03-18UTC00:01至09-14UTC00:01，连续180日/6×30日折，180日滚动train、3日gap、purge0（无未来标签）。固定因果规则不拟合/OOS选参，不跨折重置。每场259382分钟/执行NAV点核算连续整体回撤，逐折收益/DD/Sharpe365/Calmar及前五/末折；折收益乘积与完整净值一致。两段历史多轮开发，不能称未触碰最终测试集、独立前向或新的跨年复利。',
 'Sensitivity完成：BTC/ETH/组合×2025/2026六个3×3完整面；entry与exit双轴，EMA50固定。162行CSV包含三档成本收益/分钟和日DD/Sharpe365/Calmar、正折/往返/费用/集中度。18复用配置不再跑生产回测，旧完整档案只读核对。相邻12边与2sd cliff为描述，非统计显著性或最优参数证明。实际不同NAV路径数另报，同路径参数不得作为独立样本。',
 'Costs完成：每边fee10bp、halfspread1bp、slippage2bp；impact=0.5×滞后20完整日sample log sigma×sqrt(交易预算/quoteADV)，参与率≤0.1%。四项同时1/2/3倍、tick损失单列，终止平仓成本计入。570笔新组件成交以及180笔只读旧成交独立核对；现货多头无资金费/借币，USDT/现金收益0。Oct1静态交易所过滤元数据用于历史为假设；没有历史L2、队列、IOC可成交/部分成交/延迟、TCA或实际容量校准。',
 '固定门槛：全部成本净正；1x≥4/6正折；3x整体分钟DD≤25%；同面3x正比例≥60%；1x≥2往返；参考价毛PnL/1x成本≥2.5；无负余额；终止flat。组合往返为两组件之和，不表示每币/每折皆正。表内旧结果列“原资格”以保持历史，完整邻域资格不改旧ledger。','',
 '## 全部54配置及三档成本结果','',
 '|年份|资产|entry/exit日|新/复用|1x%|2x%|3x%|3x整体DD%|1x正折|往返1x|本轮资格/失败原因|旧原资格|','|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfg.values():
 z=c['scenes'];lines.append(f"|{c['year']}|{c.get('asset','组合75/25')}|{c['entry_days']}/{c['exit_days']}|{'新' if c['is_new'] else '复用'}|{z['1']['net_return_pct']:.5f}|{z['2']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|{c.get('source_record_status','—')}|")
lines+=['','## 全部54配置三倍成本逐折结果','', '|年份|资产|entry/exit日|六折净收益%|前五折累计%|末折%|','|---|---|---|---|---:|---:|']
for c in cfg.values():
 z=c['scenes']['3'];folds=', '.join(format(x['net_return_pct'],'.4f') for x in z['folds']);lines.append(f"|{c['year']}|{c.get('asset','组合75/25')}|{c['entry_days']}/{c['exit_days']}|{folds}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['','## 六个敏感性面','', '|年份/资产|本轮通过/9|3x正比例|不同3x NAV/9|3x收益范围%|描述cliff/12|','|---|---:|---:|---:|---|---:|']
for group,v in r['sensitivity'].items():
 cells=[c for c in cfg.values() if c['year']+'_'+c.get('asset','combination')==group];a,b=v['metrics']['3']['return_range_pct'];lines.append(f"|{group}|{sum(c['status']=='passed' for c in cells)}|{v['metrics']['3']['positive_return_fraction']:.3f}|{len({c['scenes']['3']['NAV_sha256_f64le'] for c in cells})}|{a:.5f}至{b:.5f}|{sum(e['cliff_flag_2sd'] for e in v['adjacent_edges'])}|")
lines+=['','## 原样读取旧比较','', '|年份|配置|3x净收益%|分钟DD%|原资格|','|---|---|---:|---:|---|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['status']}|")
lines+=['','旧持有组合50/50，研究75/25，敞口和风险不同，不能直接称同风险alpha。','',
 '## 原冻结模拟跨UTC日决策：累计1539分钟','',
 '原20261001T113625Z/forward_plan.json SHA2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81保持；原SMA65±1%、浮点数量及原成本模型保持。读取235103源report/state，从Oct2 23:40继续至Oct3 01:40UTC，保留1421个原NAV点；本段120闭合分钟＋Oct3 00:01参考净值1点，累计1542点（初始＋2个日执行参考＋1539闭合分钟）。参考index1442，即使HOLD也纳入整体回撤。没有账户重置、重复首买、自动再平衡或本段强制平仓。',
 '从Binance public kline接口实际取每币121条1m（含23:39旧重叠）及65条完整1d，原HTTP字节gzip/SHA、URL、status200、毫秒单位、取得UTC及固定endTime全部保留。分钟连续，closeTime+1≤01:40；日线通过Oct2收盘，00:00可得且早于00:01决策。64个日bar与首轮原65日窗口重叠完整字段相等；Oct2 daily close与真实23:59 minute close一致。取得晚于截止，属于延迟shadow重建，不是真实成交/实时执行证明。','',
 '|资产|前日close|SMA65|决策|参考minute open|滞后20日quote ADV|sigma|','|---|---:|---:|---|---:|---:|---:|']
for a,d in f['daily_decisions_by_asset'].items():lines.append(f"|{a}|{float(d['prior_close']):.5f}|{float(d['SMA65']):.5f}|{d['action']}|{d['reference_minute_open']:.5f}|{d['lagged_daily_quote_ADV']:.5f}|{d['lagged_daily_volatility']:.8f}|")
lines+=['','原BTC/ETH desired均继续持有，原6套成本仓位、费用、交易记录保持，新增成交0。每日决策独立重算SMA、上下1%阈值、ADV/sample log sigma；未来或当前分钟close未参与日线决策。原日决策若触发成交将用当日00:01open及滞后成本，保留原浮点fill，不改为历史新Decimal/tick模型。','',
 '|观察|成本|累计净收益%|累计分钟/参考DD%|本段收益%|新增成交|','|---|---|---:|---:|---:|---:|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['new_executions']}|")
z=f['configs']['forward_snapshot_combo']['scenes']['3'];lines+=['',
 f"累计25小时39分，只有1完整日。组合三倍{z['net_return_pct']:.5f}%/DD{z['max_drawdown_pct']:.5f}%，仍亏损，本段{z['since_previous_mark_return_pct']:.5f}%。三观察/9场景已计算，partial以rejected留档仅因180日/六折资格不完整；原长期计划collecting至2027-03-31UTC00:01。没有新增前向敏感性或短样本年化指标。",
 '下一轮读取本轮forward_state.json，从Oct3 01:40原现金/单位/desired/累计成本继续；下次Oct4UTC00:01日决策之前仅追加闭合分钟；跨决策读取当时可用65日/SMA、滞后20日成本及实际执行参考。新截止先reserve，旧截止只读。','',
 '## 独立审计、复现与提交','',
 '4份真实525600分钟parquet、daily_inputs、交易所元数据SHA、closed/可用时间、UTC00:01参考和资产轴独立核对。pandasEMA＋排序区间重建19440个全网格成本场景的因果持仓决定；24新组件各3个当前/未来close扰动共72次，过去/当时输出不变。这是同一已登记策略的工程因果检查，不是新增参数变体/收益实验。',
 '570新＋180旧模拟fill核对Decimal费用/预算/参与率/ADV/sigma/tick/LOT/余额，独立重建162场42019884分钟/执行NAV点，核对逐折/整体回撤、Sharpe/Calmar、折复利、成本和门槛。54旧成本场景为只读证据核对，108新场景为生产回测。9原模拟场景独立核对raw日/分钟回复、64日重叠、日决策、NAV时间轴、1421旧前缀、最终现金/units/desired及nextstate。',
 '108新历史成本场景精确重放，54旧场景只读验证，9累计模拟场景含跨日决策/状态精确重放，无新HTTP/ledger写。39定义finish绑定最终报告SHA，旧832记录/1684行逐项及字节保持。registry检查通过；保留36新历史完整压缩信号/交易/持仓档案、39spec、54全网格spec引用、中文报告、162行CSV/六面图、数据哈希、原HTTP、脚本/日志及verification.json。忽略data/中大行情/全NAV，不提交凭据。',
 '复现：`bash research/experiments/20261003T015203Z/reproduce.sh`。prepare.py是首次reserve入口，完成后不重复运行。提交推送通过已连接GitHub的GitData API，ref更新force=false；运行简报披露经ref/父/tree/本地文件核对的真实SHA和push状态。',
 '结论：6个新2026组合历史合格，但2025均淘汰；没有新增共同通过方法。更快退出有收益/回撤/集中度取舍，未满足稳定正收益目标。保留原方案模拟并继续探索预登记的新配置。','']
(ROUND/'result.md').write_text('\n'.join(lines))
values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=TwoSlopeNorm(vmin=min(values),vcenter=0,vmax=max(values));cmap=plt.get_cmap('RdYlGn');fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for iy,y in enumerate(('2025','2026')):
 for ix,asset in enumerate(('BTC','ETH','combination')):
  cells={(c['exit_days'],c['entry_days']):c for c in cfg.values() if c['year']==y and c.get('asset','combination')==asset};a=np.array([[cells[(e,k)]['scenes']['3']['net_return_pct'] for k in grid['entry_lookback_days']] for e in grid['exit_lookback_days']]);ax=axes[iy,ix];im=ax.imshow(a,norm=norm,cmap=cmap)
  for i,e in enumerate(grid['exit_lookback_days']):
   for j,k in enumerate(grid['entry_lookback_days']):
    c=cells[(e,k)];rgb=cmap(norm(a[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];label=('P' if c['status']=='passed' else 'R')+(' / old' if not c['is_new'] else ' / new');ax.text(j,i,f'{a[i,j]:.2f}%\n{label}',ha='center',va='center',color='white' if lum<.48 else 'black')
  ax.set(xticks=range(3),xticklabels=grid['entry_lookback_days'],yticks=range(3),yticklabels=grid['exit_lookback_days'],xlabel='Channel entry (days)',ylabel='Channel exit (days); EMA50 +/-1.5%',title=f'{y} {asset}')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day return,3x costs (%)',shrink=.75);fig.suptitle('Faster channel exits | P: historical pass; R: reject | exit30 reused read-only');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved all54grid/162cost rows,folds,750fill audit,stress loss and9partial simulated scenes.')
