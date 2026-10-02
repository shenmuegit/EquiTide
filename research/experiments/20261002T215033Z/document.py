"""Document all predeclared portfolios, gates, concentration and partial observations."""
import collections,gzip,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary'];directions=grid['directions'];prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));reasons=collections.Counter(k for c in cfg.values() for k in c['failed_criteria'])
lines=['# 本轮：收盘通道与EMA跨资产组合','',
 '触发2026-10-02 21:50:33UTC；首工具21:51:11UTC；分支codex/strategy-research，先fetch/ff同步，基点6cb3e0f3e8fe6778a45407b5f3558003f289666c。使用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs三技能；无真实订单。','',
 '## 筛选结论','',
 f"36个新组合先独立reserve，108个新成本场景完成。36/36在1/2/3倍成本均净正；{len(s['passed'])}项达到固定历史门槛、{len(s['rejected'])}项淘汰，全部淘汰原因：{dict(reasons)}。{len(s['both_periods_passed_pairs'])}/18组相同方向/参数分别在两段历史通过。包含正收益但未过资格门槛的配置、负收益的累计观察，全部保存并finish。",
 '事前中心为通道入场15日/退出30日，EMA65、对称±1.5%；两方向及完整网格在本轮组合计算前冻结。',
 '|年份|事前中心方向|1x净收益%|3x净收益%|3x整体分钟DD%|1x正折|3x前五折累计%|3x末折%|资格|',
 '|---|---|---:|---:|---:|---:|---:|---:|---|']
for c in cfg.values():
 if c['CHANNEL_entry_days']==15 and c['EMA_span_days']==65:
  z=c['scenes'];lines.append(f"|{c['year']}|{c['direction']}|{z['1']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['3']['first_five_fold_return_pct']:.5f}|{z['3']['last_fold_return_pct']:.5f}|{c['status']}|")
lines+=['',
 'BTC通道/ETH EMA中心在两段历史通过；2026三倍前五折仅+0.91004%、末折+23.75126%，收益仍集中。反方向中心2026虽三倍+12.89101%、DD10.60846%，但只有3/6正折，保留并淘汰。相比旧同通道15/30的2026三倍+27.28308%/DD12.63003%，本轮通过中心+24.87745%/DD12.00428%收益较低、回撤稍小；2025也未统一超过旧同通道/同EMA。数据来自相同开发历史，不能据此声称独立显著改进。',
 f"本轮39新定义finish：36历史组合、3新截止观测。累计773规范定义、775保留ID、1570登记行；无reserved/缺结果。此前{prior['lines']}行/{prior['canonical']}规范定义、{len(prior['records'])}保留记录、{len(prior['prior_conclusions'])}轮全文结论、{len(prior['legacy_results'])}份Freqtrade结果JSON及{len(prior['checks_read'])}份checks/*oos.py全文已读取并保存在prior_summary.json.gz。初始16条都有实际关联结果，不表示全部符合长期盈利门槛。",'',
 '## 经济假设、来源与预登记','',
 '通道按过去收盘极值切换，EMA按指数衰减平均切换，异步现金/持币可能改变折间收益和回撤；共同趋势暴露、假突破及收益集中仍可能抵消分散效果。每方向测试通道入场10/15/20日×EMA50/65/80完整3×3，通道退出固定30日、EMA两边阈值固定1.5%。没有根据本轮结果改变阈值、中心、权重或原观察策略。',
 '参考[pandas.DataFrame.ewm官方说明](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)，2026-10-02访问文档版本3.0.6，支持alpha=2/(span+1)及adjust=False递推定义。现有生产信号是Python浮点手工递推，未升级本地pandas，文档不提供加密货币盈利证据。',
 '36项具体spec使用BTC/ETH已有组件指纹及原值75/25，先成功预约才计算组合净值。24个有实际结果的组件/72成本场景按原归档、spec、报告及完整NAV哈希复用；组件未重新策略回测、预约或finish。通道引用174933报告，但20/30组件原归档/NAV在154903；EMA归档/NAV在234032。实际源路径写入batch/report/data_manifest。','',
 '## 完整规则与资金','',
 '通道decision i：C[i-1]严格高于max(C[i-entry-1:i-1])设desired-long；严格低于min(C[i-31:i-1])设cash。参照区间止于i-2，排除被测试收盘，恰好entry/30个完整日CLOSE，相等或无事件保持desired；信号Decimal精度28，不用日内high/low。',
 'EMA：E[0]为数据集首个完成日收盘；alpha=2/(span+1)，E[j]=(1-alpha)E[j-1]+alpha C[j]，Python float。决策i只比较已完成C[i-1]与E[i-1]：严格高于1.015E设long、严格低于0.985E设cash，死区/相等保持desired。从数据日0递推且跨折不重置，seed记忆早于滚动train起点；无标签/拟合。两规则OOS183从desired-cash及现金开始，跨折保留现金/数量/desired。',
 '前日收盘UTC00:00可用，参考成交价取随后00:01真实分钟open。模拟marketable LIMIT IOC立即按估计不利价成交，现金/数量/手续费/LOT/tick为Decimal28：buy价向上/sell价向下取tick、数量向下取LOT，残余现金保留，拒单不改仓位，后续日决策可重试；终止平仓收费。',
 '原值BTC75%/ETH25%表示2000USDT初始独立1500/500分仓，未自动归一化、维持权重、转账或再平衡。组合为相同资金规模/时间轴/成本版本的BTC绝对NAV+ETH绝对NAV，初值2000；没有再乘75/25，未平均收益/Sharpe/DD或缩放其他本金下的冲击。完整参数在被引用组件spec及本轮39具体spec。','',
 '## 三项验证状态','',
 'Walk-forward完成：2025/2026分别03-18UTC00:01至09-14UTC00:01，各连续180日、6个30日诊断折，已有180日滚动历史及3日gap/purge0。无模型/标签拟合、测试集选参或每折仓位重置；这是固定规则的时间推进验证。每场259382分钟/执行NAV点计算连续整体DD，保存逐折收益/DD/日Sharpe365/Calmar，并核对折收益乘积等于连续净值收益。这两段历史反复用于研究，当前组合假设受既有结果启发，不能称未触碰最终测试集、真正前向验证或新跨年复利结果。',
 'Sensitivity完成：四个年份/方向3×3面全部保留，保存三档成本正收益/正Sharpe比例、收益范围、相邻12边及2sd差异描述。36格各有不同三倍NAV路径，但共享组件/历史，不能当36独立样本；2sd描述不是显著性或最优参数证明。2025两面均9/9通过；2026仅BTC通道/ETH EMA3/9、反方向4/9通过，完整资格区域比正收益区域小。',
 f"Costs完成：每边手续费10bp、halfspread1bp、滑点2bp；冲击0.5×滞后20完整日sample log sigma×sqrt(交易预算/quoteADV)，参与率≤0.1%。四项同时1/2/3倍，tick取整损失单列；终止平仓含成本。现货无杠杆多头，资金费/借币不适用，现金/USDT收益为0。已有PRICE/LOT/NOTIONAL及前5闭合分钟VWAP代理约束。本轮只读旧{s['source_component_fills_read_only']}笔组件模拟成交，0新增组件成交、0实盘订单。Oct1静态元数据用于历史为假设；无历史L2、队列、延迟、部分成交、IOC可成交或TCA/容量校准证据。",
 '固定门槛：各成本净正，1x≥4/6正折，3x整体分钟DD≤25%，本面3x正比例≥60%，1x≥2组件往返，参考价毛PnL/成本≥2.5，无负余额，终止flat。11项因正折数不足而rejected，净正结果完整保存。组合往返为组件之和，不表示每币/每折盈利。','',
 '## 全部36个新组合','',
 '|年份|方向|通道入场日|EMA日|1x收益%|2x%|3x%|3x分钟DD%|1x正折|1x往返|资格/失败原因|',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for n,c in cfg.items():
 z=c['scenes'];lines.append(f"|{c['year']}|{c['direction']}|{c['CHANNEL_entry_days']}|{c['EMA_span_days']}|{z['1']['net_return_pct']:.5f}|{z['2']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 敏感性区域与路径数','', '|年份|方向|通过/9|不同3x NAV/9|3x收益范围%|描述cliff/12|','|---|---|---:|---:|---|---:|']
for y in ('2025','2026'):
 for d in directions:
  cells=[c for c in cfg.values() if c['year']==y and c['direction']==d];sens=r['sensitivity'][y+'_'+d];a,b=sens['metrics']['3']['return_range_pct'];lines.append(f"|{y}|{d}|{sum(c['status']=='passed' for c in cells)}|{len({c['scenes']['3']['NAV_sha256_f64le'] for c in cells})}|{a:.5f}至{b:.5f}|{sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges'])}|")
lines+=['','## 全部逐折三倍收益与集中度','', '|年份|方向|通道入场/EMA日|六折收益%|前五折累计%|末折%|','|---|---|---|---|---:|---:|']
for c in cfg.values():
 z=c['scenes']['3'];foldtext=', '.join(format(x['net_return_pct'],'.4f') for x in z['folds']);lines.append(f"|{c['year']}|{c['direction']}|{c['CHANNEL_entry_days']}/{c['EMA_span_days']}|{foldtext}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['','## 原样读取旧比较','', '|年份|旧比较|三倍净收益%|整体分钟DD%|原资格|','|---|---|---:|---:|---|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['status']}|")
lines+=['','旧持有组合初始50/50而研究为75/25，两者持币/现金敞口不同，不称同风险alpha。','',
 '## 原冻结方案累计1299分钟','',
 '原113625/forward_plan.json哈希2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81保持；原SMA65±1%、浮点数量与原成本模型保持，未用本轮通道/EMA替换。读取195003源report/state，从19:40原现金/持币延续至21:40UTC；1181旧NAV点逐点保留，追加120闭合分钟后1301点（初始+参考执行+1299闭合mark）。没有重置现金、重复首买或强制平仓。',
 '使用[Binance官方行情接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)，每币121条真实1m，19:39重叠bar全字段匹配旧末bar，新120条连续且closeTime+1≤21:40截止。原HTTP响应字节gzip/SHA、URL、毫秒单位、status200及取得UTC保存；取得晚于截止，为延迟shadow重建，非实时执行。','',
 '|观测|成本|累计净收益%|累计mark DD%|本段收益%|本段新成交|','|---|---|---:|---:|---:|---:|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['new_executions']}|")
z=f['configs']['forward_snapshot_combo']['scenes']['3']
lines+=['',
 f"累计21小时39分、0完整日，BTC/ETH各成本和组合均负。组合三倍{z['net_return_pct']:.5f}%、整体DD{z['max_drawdown_pct']:.5f}%，新120分钟{z['since_previous_mark_return_pct']:.5f}%。0新成交，原费用不变，全部旧观察保留。3观测/9场景实际完成并以partial资格rejected留档，仅因缺180日/六折，原长期计划collecting。未跑前向参数敏感性，不报短样本年化Sharpe/CAGR/Calmar，不把首笔模拟买入当真实执行或容量稳健证据。",
 '下一轮读取本轮forward_state.json，从21:40现金/持币/desired/旧费用继续；Oct3UTC00:01下次日决策及2027-03-31终止日期不变。新截止须先reserve，旧截止只读。输入每资产为minute数组，解析兼容旧1d/1m字典。','',
 '## 独立审计、复现与留档','',
 '从4份真实525600分钟parquet核对哈希、closed标记、可用时间/资产轴连续性；用24旧组件/72成本场景现金/持币片段重建18675504分钟/执行NAV点并核对源SHA。108新组合另核对28013256分钟NAV、逐折/整体Sharpe/Calmar/DD、分项成本/毛PnL、终止仓位/余额/资金原值与门槛。9累计观察独立核对旧前缀、仓位/费用和真实HTTP字节/closed marks，未出现重复买入。108+9场景精确重放通过，不发新HTTP、不改登记。',
 '39项finish绑定最终report/forward_report SHA；此前736保留记录/1492行与24组件旧结果完全保持，registry检查通过。保留verification.json、日志、39具体spec、36压缩完整成本/交易档案、中文报告、图表/108行CSV、data_manifest与必要代码；大行情/全NAV为忽略data/，不提交凭据。本轮无计算失败或环境阻碍。',
 '复现：`bash research/experiments/20261002T215033Z/reproduce.sh`。prepare.py仅首次预约，精确已完成配置不再执行。实际push状态由运行简报核对远程ref、提交父/tree及本地stage/文件SHA后披露。',
 '两段历史共用、规则启发于旧结果，7/18跨期对不等于7独立实验，正收益与较低回撤不保证稳定盈利。继续寻找新参数/原值资金配置，同时按冻结规则延续真实行情模拟；本轮精确配置以后只读复用。','']
(ROUND/'result.md').write_text('\n'.join(lines))
values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=plt.Normalize(min(values),max(values));cmap=plt.get_cmap('YlGn');fig,axes=plt.subplots(2,2,figsize=(11,9),layout='constrained')
for iy,y in enumerate(('2025','2026')):
 for ix,d in enumerate(directions):
  cells={(c['EMA_span_days'],c['CHANNEL_entry_days']):c for c in cfg.values() if c['year']==y and c['direction']==d};a=np.array([[cells[(e,k)]['scenes']['3']['net_return_pct'] for k in grid['CHANNEL_entry_days']] for e in grid['EMA_span_days']]);ax=axes[iy,ix];im=ax.imshow(a,norm=norm,cmap=cmap)
  for i,e in enumerate(grid['EMA_span_days']):
   for j,k in enumerate(grid['CHANNEL_entry_days']):
    c=cells[(e,k)];rgb=cmap(norm(a[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];label='P' if c['status']=='passed' else 'R';ax.text(j,i,f'{a[i,j]:.2f}%\n{label}',ha='center',va='center',color='white' if lum<.48 else 'black')
  ax.set(xticks=range(3),xticklabels=grid['CHANNEL_entry_days'],yticks=range(3),yticklabels=grid['EMA_span_days'],xlabel='Channel entry lookback (days); exit30',ylabel='EMA span (days); +/-1.5%',title=f'{y} {d}')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day return,3x costs (%)',shrink=.75);fig.suptitle('Channel/EMA BTC75/ETH25 initial funding | P: historical pass; R: reject');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved all36 combination/cost/fold tables,four sensitivity surfaces and9 negative original-plan observations')
