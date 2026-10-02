"""Render every mixed-rule configuration and loss-making cumulative observation."""
import collections,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary'];directions=grid['directions'];reasons=collections.Counter(k for c in cfg.values() for k in c['failed_criteria'])
lines=['# 本轮：收盘通道与非对称均线跨资产组合','',
 '触发2026-10-02 19:50:03UTC；首工具19:50:39UTC；分支codex/strategy-research。仅回测及影子模拟，无真实订单。','',
 '## 结论','',
 f"36个新组合先reserve，108个新成本场景实际完成。36/36在1/2/3倍成本均净正；{len(s['passed'])}项达到固定历史门槛、{len(s['rejected'])}项淘汰。{len(s['both_periods_passed_pairs'])}/18组相同方向/参数组合在两段历史分别通过。所有通过、失败资格和负收益观测均保留；未重跑已验证组件策略。",
 '事前中心通道入场15日/退出30日，非对称SMA65入场1.5%/退出0.5%。BTC通道/ETH均线方向三倍2025+29.41739%、DD15.13932%；2026+26.17496%、DD12.41450%，前五折+1.90063%、末折+23.82157%。反方向三倍2025+40.97674%、DD12.29891%；2026+22.37298%、DD11.46506%，前五折+1.03071%、末折+21.12454%。两个中心均达到历史门槛，但收益集中仍在。',
 'BTC均线/ETH通道的2026中心比旧同均线中心三倍+21.26486%/DD13.45730%有更高收益和较小回撤；BTC通道/ETH均线中心比旧同通道15/30组合+27.28308%/DD12.63003%收益稍低、DD稍小。仅是同一开发历史上的数值比较，不证明统一改进、独立显著或稳定盈利。',
 '原冻结SMA65±1%/75:25保持，累计1179分钟（19小时39分、0完整日）。组合一/二/三倍净收益-1.01037/-1.13992/-1.26920%，三倍整体DD3.76620%；新120分钟0新成交，仓位/费用未重置。3个新截止观测的9场景真实行情模拟完成，partial记rejected仅表示缺180日/六折资格，原长期收集计划继续。',
 '本轮39新定义finish；累计734规范定义、736保留ID、1492登记行，无reserved或缺结果。此前1414行/695规范定义、697保留记录、17轮全文结论、5份Freqtrade结果JSON和4份checks/*oos.py全文已读并保存prior_summary.json.gz。初始16条均有实际关联证据，不等同长期全部合格。','',
 '## 经济假设、知识来源与预登记','',
 '上一轮同通道15/30组合在2026较快响应，已有非对称均线使用不同参考区间和退出阈值。本轮冻结两种资产方向，检验异步持币/现金能否减少回撤或分散逐折收益，也允许共同趋势暴露、假突破和收益集中使组合无改进。两种方向各通道入场10/15/20日×均线入场1.25/1.5/2%完整3×3面；固定通道退出30日、SMA65退出0.5%，没有看本轮结果后改规则/门槛。',
 '参考[Harry Markowitz：Portfolio Selection](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1952.tb01525.x)，Journal of Finance7(1)，1952年3月，77–91，2026-10-02访问出版者书目信息，该页未提供全文。不同规则组合的分散假设为本轮自定；未复现论文、未做均值方差优化、未从论文推断加密货币正收益。',
 '完整具体spec以既有BTC/ETH组件指纹和原值75/25形成新组合，36项各自预约成功后才相加净值。24个已完成组件按原报告/归档/spec/NAV哈希只读复用，未改名制造新规则，未重新reserve/finish或重新策略生产计算。通道20/30组件源报告为174933，实际旧归档/NAV仍位于154903，明确追踪原来源。','',
 '## 完整规则、时间与资金','',
 '通道：daily decision i的C[i-1]严格高于max(C[i-entry-1:i-1])设置desired-long，严格低于min(C[i-31:i-1])设置desired-cash；参照区间止于i-2，排除被测试收盘，恰好entry/30个完整日CLOSE。相等/无事件保持desired；Decimal精度28，不用日内high/low。',
 '非对称SMA：mean(C[i-65:i])包含65个已完成收盘且止于i-1；C[i-1]严格高于mean×(1+entry-band)设置long，严格低于mean×0.995设置cash；相等/死区保持desired。没有确认计数、EMA、波动过滤、盘中止损、金字塔或空头。两规则OOS183从现金及desired-cash开始，已有历史暖机，跨折连续保留现金/数量/desired。',
 '信号前日收盘在UTC00:00可得，实际执行参考随后UTC00:01真实分钟open；假设LIMIT IOC立刻按估计不利价成交，Decimal tick及LOT向下取量、残余现金保留。拒单不改变持仓，后续每日决策可重试；终止平仓收费。原值BTC75%/ETH25%为2000USDT初始1500/500独立分仓，未自动归一化、维持权重、转账或再平衡。',
 '组合使用完全相同资金规模/时间轴/成本版本的BTC绝对NAV+ETH绝对NAV，初值2000；没有再乘75/25、平均收益/Sharpe/回撤或复用按不同本金产生的冲击。所有参数均写入组件spec和本轮具体组合引用。','',
 '## 三项验证','',
 'Walk-forward完成：2025/2026分别03-18UTC00:01至09-14UTC00:01，两段各连续180日/六个30日诊断折。已有180日滚动历史、3日gap、purge0；无模型/标签/权重拟合，无每折重置或OOS选参。每场259382个完整分钟与执行点NAV计算整体回撤，报告逐折净收益/风险、日Sharpe365、Calmar和前五/末折，逐折乘积核对整体。两段反复用于研究，本轮组合由既有结果启发，不是未触碰最终测试集、前向验证或新的跨年复利结果。',
 'Sensitivity完成：四个方向/年份3×3面全保留，两参数同时变动，每档成本的正收益/正Sharpe比例及相邻12边的2sd差异描述保存。全部格三档成本净正，但完整资格区域另列；净值相同参数不能算独立证据，相邻描述旗标不是显著性或最优点证明。',
 'Costs完成：每边手续费10bp、halfspread1bp、滑点2bp，冲击0.5×滞后20完整日sample log sigma×sqrt(交易预算/quoteADV)，参与率≤0.1%，四项同时1/2/3倍，tick成本单列。复用1500/500本金下实际成本化现金/持币与成交；现货无杠杆多头，不含资金费/借币/USDT收益。LOT/price/NOTIONAL和前5闭合分钟VWAP代理已检查。Oct1静态交易所元数据用于历史是假设，无历史L2、队列、IOC可成交性、延迟、部分成交或TCA/容量校准证据。本轮没有新增组件模拟成交，不能把旧384笔模拟成交当新成交证据。',
 '固定门槛：各成本净正，1x≥4/6正折，3x分钟DD≤25%，本面三倍正比例≥60%，1x≥2组件往返，参考价毛PnL/成本≥2.5，无负余额，终止flat。所有9项淘汰仅four_positive_1x_folds失败；正收益仍完整保留。组合往返为两组件之和，不意味着每折/每币盈利。','',
 '## 全部36个新组合','',
 '|年份|方向|通道入场日|SMA入场%|1x收益%|2x%|3x%|3x分钟DD%|1x正折|1x往返|资格/失败原因|',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for n,c in cfg.items():
 z=c['scenes'];lines.append(f"|{c['year']}|{c['direction']}|{c['CHANNEL_entry_days']}|{100*c['ASMA_entry_band']:g}|{z['1']['net_return_pct']:.5f}|{z['2']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 敏感性区域与有效路径数','', '|年份|方向|通过/9|不同3x NAV/9|3x收益范围%|描述cliff/12|','|---|---|---:|---:|---|---:|']
for y in ('2025','2026'):
 for d in directions:
  cells=[c for c in cfg.values() if c['year']==y and c['direction']==d];sens=r['sensitivity'][y+'_'+d];a,b=sens['metrics']['3']['return_range_pct'];lines.append(f"|{y}|{d}|{sum(c['status']=='passed' for c in cells)}|{len({c['scenes']['3']['NAV_sha256_f64le'] for c in cells})}|{a:.5f}至{b:.5f}|{sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges'])}|")
lines+=['','## 全部逐折三倍收益与集中度','', '|年份|方向|通道入场/SMA入场%|六折收益%|前五折累计%|末折%|','|---|---|---|---|---:|---:|']
for c in cfg.values():
 z=c['scenes']['3'];foldtext=', '.join(format(x['net_return_pct'],'.4f') for x in z['folds']);lines.append(f"|{c['year']}|{c['direction']}|{c['CHANNEL_entry_days']}/{100*c['ASMA_entry_band']:g}|{foldtext}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['','## 原样读取旧比较','', '|年份|旧比较|三倍净收益%|整体分钟DD%|原资格|','|---|---|---:|---:|---|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['status']}|")
lines+=['','旧持有组合是50/50而研究是75/25初始分仓，持币/现金敞口不同，不能称同风险alpha；现金收益0假设不变。','',
 '## 原冻结方案累计1179分钟','',
 '原113625/forward_plan.json哈希2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81不变，原SMA65±1%及浮点数量/成本模型保持。读取174933源report/state，从17:40原持仓延续至19:40UTC，旧1061个NAV点逐点保留，追加120闭合分钟后1181点（初始+参考执行+1179闭合mark）；没有重置现金、重复首买或本轮强制平仓。',
 '依据[Binance官方行情接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)，每币121条真实1m，17:39重叠bar全字段匹配旧末bar；新120条连续且closeTime+1≤19:40截止。原HTTP响应字节gzip/SHA、URL、毫秒单位、status200和取得UTC保留；取得晚于截止明确为延迟shadow重建，不是实时执行或真实订单。','',
 '|观测|成本|累计净收益%|累计mark DD%|本段收益%|本段新成交|','|---|---|---:|---:|---:|---:|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['new_executions']}|")
lines+=['',
 '累计19小时39分、0完整日，BTC/ETH各成本全负；组合三倍-1.26920%、DD3.76620%，新120分钟约-0.42518%，费用未因新交易增加，全部旧正/负观察保留。180日/六折验证尚未完成，前向参数敏感性不跑，不报短样本年化Sharpe/CAGR/Calmar，也不把只有首笔买入的成本压力当真实执行/容量稳健证明。partial记rejected不取消长期收集。',
 '下一轮读取本轮forward_state.json，从19:40现金/持币/desired/旧费用继续；Oct3UTC00:01下一日决策和2027-03-31终止保持，新截止须先reserve，旧截止只读。输入按资产为minute数组，同时兼容旧1d/1m字典。','',
 '## 独立审计、复现与留档','',
 '24个既有组件/72成本场景，从4份真实parquet和旧现金/持币片段重建全部18675504分钟/执行NAV点并核对源SHA。108个新组合另核对28013256分钟NAV、逐折/整体Sharpe/Calmar/DD、成本各项/参考价毛PnL、终止仓位/余额以及本面门槛，发现二次乘权重或日线DD替代分钟DD的错误。全部9新累计观测的原前缀/仓位/费用、HTTP原响应和closed mark独立核对。新108+9成本场景精确重放通过，无新HTTP或登记改动。',
 '本轮39独立finish绑定最终report/forward_report SHA。原697记录/1414行及24组件旧结果保持，registry.py检查通过，verification.json、日志、39具体spec、36组合压缩逐场景结果、报告/图表/CSV/源数据哈希和必要代码保留；大行情/全NAV位于忽略data/。本轮无计算失败或数据/权限障碍。',
 '复现：`bash research/experiments/20261002T195003Z/reproduce.sh`，只用缓存；prepare.py为首次预约，不重复执行已完成精确配置。实际push状态在运行简报核对远程ref、提交父/tree、本地stage及文件SHA后披露。',
 '下一批可探索新资金配置或另类规则，继续原冻结方案真实行情模拟；本轮36组合精确设置只读复用。9/18参数对不是9个独立时期：组件/历史共用且部分参数实现同NAV。即使本轮均历史净正且有回撤改善，集中末折、回溯选择与原模拟亏损仍限制稳定正收益结论。','']
(ROUND/'result.md').write_text('\n'.join(lines))
values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=plt.Normalize(min(values),max(values));cmap=plt.get_cmap('YlGn');fig,axes=plt.subplots(2,2,figsize=(11,9),layout='constrained')
for iy,y in enumerate(('2025','2026')):
 for ix,d in enumerate(directions):
  cells={(c['ASMA_entry_band'],c['CHANNEL_entry_days']):c for c in cfg.values() if c['year']==y and c['direction']==d};a=np.array([[cells[(e,k)]['scenes']['3']['net_return_pct'] for k in grid['CHANNEL_entry_days']] for e in grid['ASMA_entry_band']]);ax=axes[iy,ix];im=ax.imshow(a,norm=norm,cmap=cmap)
  for i,e in enumerate(grid['ASMA_entry_band']):
   for j,k in enumerate(grid['CHANNEL_entry_days']):
    c=cells[(e,k)];rgb=cmap(norm(a[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];label='P' if c['status']=='passed' else 'R';ax.text(j,i,f'{a[i,j]:.2f}%\n{label}',ha='center',va='center',color='white' if lum<.48 else 'black')
  ax.set(xticks=range(3),xticklabels=grid['CHANNEL_entry_days'],yticks=range(3),yticklabels=[100*x for x in grid['ASMA_entry_band']],xlabel='Channel entry lookback (days); exit30',ylabel='ASMA65 entry (%); exit0.5%',title=f'{y} {d}')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day return,3x costs (%)',shrink=.75);fig.suptitle('Mixed-rule BTC75/ETH25 initial funding | P: historical pass; R: reject');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved all36 combination/cost/fold tables,four sensitivity surfaces and9 negative original-plan observations')
