"""Render every channel grid cell, historical diagnostic and continued shadow scene."""
import collections,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary']
reasons=collections.Counter(k for c in cfg.values() for k in c['failed_criteria']);negative=[(n,c) for n,c in cfg.items() if c['scenes']['3']['net_return_pct']<=0]
lines=['# 本轮：收盘价通道突破与原冻结持仓延续','',
 '触发2026-10-02 15:49:03UTC，首工具15:49:45UTC；分支codex/strategy-research。仅研究和模拟，无真实订单。','',
 '## 结论','',
 f"54个新配置在计算前分别reserve，162个实际成本场景完成；一倍{s['positive_1x']}/54、三倍{s['positive_3x']}/54净正。{len(s['passed'])}项达到固定历史门槛，{len(s['rejected'])}项淘汰；{len(s['both_periods_passed_combination_pairs'])}组同规则组合在2025/2026分别通过。三倍亏损的5项完整保留，不把rejected等同亏损。",
 '2025 BTC2/9、ETH3/9、组合2/9通过；2026 BTC/ETH各0/9、组合3/9通过。唯一两段均通过组合为20日入场/30日退出、初始BTC75/ETH25：三倍2025+45.65645%/DD13.45690%，2026+25.11036%/DD11.95188%。它在网格最短入场/最长退出边缘，且两段共同资格仅1/9，不能当广泛稳健平台或事前选出的前向新候选。',
 '事前预定中心40/20组合两段均未通过：三倍2025+18.99501%、2026+15.69166%，各仅3/6个一倍正折。20/10组合的2026前五折+4.94615%、末折+3.36360%，收益较分散但2025未过折数门槛；20/30的2026前五折仅+1.00016%、末折+23.87145%，利润仍集中。不得只挑改善的单段覆盖另一段失败，不替换原冻结方案。',
 '另3个新截止累计观测先reserve，9场景完成；939分钟、0完整日，partial记rejected仅表示没有180日/六折资格，原长期计划继续收集。原持仓/费用连续，新120分钟0新成交。三倍组合累计从旧+2.17390%回落至+0.05924%，最新ETH各成本已负，变化来自价格mark，无新增已平仓盈利交易。',
 '本轮共57项finish、171场景；累计644规范定义、646保留ID、1312登记行，无reserved或缺结果。初始16条已有真实案例/回测关联证据，不表示全部长期合格。此前1198行/587规范定义的登记、全部中文结论、原Freqtrade逐折结果与checks/*oos.py全文保存为prior_summary.json.gz。','',
 '## 知识来源和经济假设','',
 '参考[Brock/Lakonishok/LeBaron：Simple Technical Trading Rules and the Stochastic Properties of Stock Returns](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1992.tb04681.x)，Journal of Finance47(5)，1992年12月，1731–1764，2026-10-02访问出版者摘要。摘要研究DJIA1897–1986的均线和区间突破，提供研究方向；本轮收盘价、多头/现金、双窗口规则是自定假设，不是论文原规则、bootstrap方法或加密货币盈利结论复现。',
 '假设：区间上破识别延续趋势、下破转现金，可能改变均线族的进出时点；也可能因假突破、退出反弹或入场滞后亏损。事前固定完整入场20/40/60日×退出10/20/30日，中心40/20，两币种、两段历史；每年18组件+9组合。没有看到本轮结果后换窗口/阈值或降低固定门槛。','',
 '## 完整规则、权重与时序','',
 '每日决策i的测试收盘为C[i-1]。入场上界=max(C[i-entry-1:i-1])，恰好entry个完整日收盘，最晚i-2；退出下界=min(C[i-exit-1:i-1])，恰好exit个、也最晚i-2。两个比较区间都排除被测试的C[i-1]，不能包含它导致无法strict突破。只用CLOSE，不是日内high/low通道；Decimal精度28。',
 'strict C[i-1]>上界设置desired-long；strict C[i-1]<下界设置desired-cash；相等或无事件保持desired。无均线、波动过滤、缓冲、多日确认、金字塔加仓、盘中止损或空头。网格允许退出窗口长于入场窗口（如20/30），明确作为原始新规则，不称经典海龟规则。',
 'OOS183从desired-cash及真实模拟现金开始，先前max窗口+1个close暖机，不预填持仓；跨六折保持desired与模拟现金/持币。指标仅用完成行情，前日收盘UTC00:00可得，随后UTC00:01真实分钟open作为执行参考；终止退出扣成本。实际拒单不改持仓，后续决策可重试。',
 '原值BTC75%/ETH25%指定2000USDT的1500/500初始独立分仓，无自动归一化、跨仓转账、每日维持权重或再平衡。新规则组件按实际资金独立算成交、取整和成本。组合直接复用本轮同资金规模的成本化绝对分钟NAV相加，不再乘权重、不平均Sharpe/回撤。','',
 '## 三项验证、固定门槛与限制','',
 'Walk-forward完成：180日滚动训练历史、3日gap、purge0，无拟合/监督标签；连续六个30日诊断折，不在每折重新开仓。2025/2026分别03-18UTC00:01至09-14UTC00:01。每场259382个连续分钟/订单点算整体DD，终止点计费用；逐折净值乘积与整体收益核对。旧历史反复研究，选择方向/网格受旧结果启发；因果信号不能消除回溯选择、多重试验或市场样本相关性。这是开发历史诊断，不是未触碰最终测试集或稳定实盘盈利证据。',
 'Sensitivity完成：六个3×3面（每年BTC/ETH/组合），全部54格/162成本、逐折收益、整体DD、日Sharpe365、Calmar、交易/费用、前五/末折和资格保存。相邻12边均列示，Sharpe差异超过其2sd的标记只是描述，差值分布接近恒定时可大量标记，不代表显著性。正收益比例与完整资格比例分别报告；边缘结果不宣称全局最优，相同NAV不能增加独立证据。',
 'Costs完成：每边fee10bp、halfspread1bp、slip2bp，冲击0.5×滞后20完整日样本log收益sigma×sqrt(预算/20日quoteADV)，参与率≤0.1%；四项同时1/2/3倍，额外Decimal tick成本单列。LOT/min/max/notional、前5闭合分钟VWAP代理和现金/持币约束检查。现货无杠杆多头，资金费/借币不适用；无USDT利息。Oct1静态元数据应用历史为模型假设，不是当时交易所校验；无历史L2、真实IOC、队列、延迟、部分成交或成交量冲击校准证据。',
 '固定门槛保持：每成本净正；1x≥4/6正折；3x完整分钟DD≤25%；同面3x净正比例≥60%；1x≥2组件往返；参考价毛损益/执行成本≥2.5；无负余额；终止flat。组合往返是组件之和。passed仅表示历史门槛，不表示所有折/所有成本均盈利。同期50/50持有权重和现金敞口不同，只读比较，不声称等风险alpha。',
 '淘汰判据次数可重叠：'+', '.join(f'{k}={v}' for k,v in reasons.items())+'。不是互斥淘汰人数，全部逐项原因留在report.json。','',
 '## 全部54项历史结果','',
 '|年份|范围|入场日|退出日|1x收益%|2x%|3x%|3x分钟DD%|1x正折|1x往返|结论/失败判据|',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for name,c in cfg.items():
 ss=c['scenes'];lines.append(f"|{c['year']}|{c.get('asset','BTC75/ETH25组合')}|{c['entry_days']}|{c['exit_days']}|{ss['1']['net_return_pct']:.5f}|{ss['2']['net_return_pct']:.5f}|{ss['3']['net_return_pct']:.5f}|{ss['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{ss['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 完整敏感性面','', '|年份|范围|通过/9|三倍正收益/9|不同3x NAV/9|3x收益范围%|描述cliff边/12|','|---|---|---:|---:|---:|---|---:|']
for y in ('2025','2026'):
 for group in ('BTC','ETH','combination'):
  rows=[c for c in cfg.values() if c['year']==y and c.get('asset','combination')==group];sens=r['sensitivity'][f'{y}_{group}'];a,b=sens['metrics']['3']['return_range_pct'];unique=len({c['scenes']['3']['NAV_sha256_f64le'] for c in rows})
  lines.append(f"|{y}|{group}|{sum(c['status']=='passed' for c in rows)}|{sum(c['scenes']['3']['net_return_pct']>0 for c in rows)}|{unique}|{a:.5f}至{b:.5f}|{sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges'])}|")
lines+=['','## 全部组合的连续前五折/末折与逐折收益','', '|年份|入场/退出日|三倍六折收益%|前五折累计%|末折%|资格|','|---|---|---|---:|---:|---|']
for c in cfg.values():
 if c['role']=='combination':
  z=c['scenes']['3'];fold_text=', '.join(format(a['net_return_pct'],'.4f') for a in z['folds']);lines.append(f"|{c['year']}|{c['entry_days']}/{c['exit_days']}|{fold_text}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|{c['status']}|")
lines+=['','## 三倍成本负收益配置完整保留','', '|配置|1x收益%|2x%|3x%|3x DD%|','|---|---:|---:|---:|---:|']
for name,c in negative:lines.append(f"|{name}|{c['scenes']['1']['net_return_pct']:.5f}|{c['scenes']['2']['net_return_pct']:.5f}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|")
lines+=['','## 只读旧结果比较','', '|年份|旧比较|3x收益%|3x分钟DD%|','|---|---|---:|---:|']
for name,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{name}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|")
lines+=['', '旧SMA65±1%/75:25、无过滤ASMA中心与50/50持有仅读取真实旧结果，无重算/重新登记。20/30组合的两段收益/分钟DD数值优于旧SMA中心，但属于本轮结果后识别的边缘格点，不增加未见样本验证或自动更换冻结规则。','',
 '## 原冻结方案累计939分钟观察','',
 '继续原SMA65±1%/75:25，113625/forward_plan.json哈希保持2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81。保留原浮点数量/成本模型，不替换成历史Decimal LOT。读取134733/forward_state.json和report，从13:40原现金/数量/desired/历史费用延续至15:40UTC，新增120闭合分钟mark、0新成交；不重复初始模拟买入、不重置、不每轮强制平仓。旧821 NAV点逐点保留，现941点（初始+执行参考+939闭合分钟）。',
 '依照[Binance官方行情接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)，每币取得121条真实1m klines，13:39重叠bar全字段匹配旧末bar；新增120条连续且closeTime+1≤15:40截止。保存原HTTP响应字节gzip及SHA、URL、毫秒单位、status和取得时间。数据在截止后取得，明确是延迟shadow重建，不是实时执行或真实下单证据。','',
 '|累计观测|成本|净收益%|完整mark DD%|本段收益%|已有模拟买入|本段新成交|','|---|---|---:|---:|---:|---:|---:|']
for name,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{name}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['executions']}|{z['new_executions']}|")
lines+=['',
 '组合累计1/2/3倍+0.32155/+0.19026/+0.05924%，三倍DD2.08737%；前轮三倍+2.17390%和本轮ETH负收益全部保留，最新120分钟组合约-2.06966%。939分钟仅15小时39分、0完整日，180日/六折WF未完成，未跑前向参数敏感性，不报短样本年化Sharpe/CAGR/Calmar，也不把已有费用三倍情景当实际新成交容量验证。',
 '下一轮读取本轮forward_state.json，从15:40原持仓继续，Oct3UTC00:01下一日决策和2027-03-31计划终止日保持。新截止先reserve，旧截止只读，输入兼容每资产直接minute数组及首段1d/1m字典。','',
 '## 审计、复现与下一轮','',
 f"独立审计从四份真实分钟parquet/Decimal日收盘，以排序区间边界和历史前缀末次强制事件独立核对19440个通道决定，不调用生产signal；核对{s['actual_component_fills']}个Decimal成交、滞后ADV/波动/参与率/成本/取整/现金，核对42019884历史NAV及完整/逐折指标和门槛。原观察另审原响应SHA、120新closed mark、旧前缀、仓位/费用和9场景。全部162历史+9观测场景精确重放，57独立finish绑定最终报告SHA，registry检查通过；日志和verification.json保存。",
 '本轮无回测计算失败或数据/权限障碍。复用133655的成交/分钟NAV框架和213902的指标/门槛，134733框架仅替换明确通道signal及独立审计；保留全部spec/压缩逐配置结果/报告/数据哈希/必要代码/少量新原响应。大行情及全分钟vector在忽略data/。',
 '复现：`bash research/experiments/20261002T154903Z/reproduce.sh`；仅缓存重放，无新HTTP/登记。prepare.py仅首次预登记，已finish完整配置不得作为新实验重复运行。实际push在运行简报用远程ref与staged tree核对。',
 '下一轮继续原冻结模拟并探索新规则或新原值组合。此通道精确配置只读复用。20/10的一段集中收益改善不覆盖2025失败；20/30的双段边缘结果需新的未使用时间证据，不能现在换规则再把原前向称其验证。','']
(ROUND/'result.md').write_text('\n'.join(lines))
fig,axes=plt.subplots(2,3,figsize=(13,8),layout='constrained');values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=TwoSlopeNorm(vmin=min(values),vcenter=0,vmax=max(values));cmap=plt.get_cmap('RdYlGn')
for iy,y in enumerate(('2025','2026')):
 for ix,group in enumerate(('BTC','ETH','combination')):
  cells={(c['entry_days'],c['exit_days']):c for c in cfg.values() if c['year']==y and c.get('asset','combination')==group};assert len(cells)==9
  z=np.array([[cells[(e,x)]['scenes']['3']['net_return_pct'] for x in grid['exit_lookback_days']] for e in grid['entry_lookback_days']]);ax=axes[iy,ix];im=ax.imshow(z,norm=norm,cmap=cmap)
  for i,e in enumerate(grid['entry_lookback_days']):
   for j,x in enumerate(grid['exit_lookback_days']):
    rgb=cmap(norm(z[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];label='P' if cells[(e,x)]['status']=='passed' else 'R';ax.text(j,i,f'{z[i,j]:.2f}%\n{label}',ha='center',va='center',color='white' if lum<.48 else 'black')
  ax.set(xticks=range(3),xticklabels=[10,20,30],yticks=range(3),yticklabels=[20,40,60],xlabel='Exit close-range lookback (days)',ylabel='Entry close-range lookback (days)',title=f'{y} {group} | 3x costs')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day net return (%)',shrink=.75);fig.suptitle('Fixed close-only channel grid | P: historical gates pass, R: reject');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved all54 channel cells,6 sensitivity panels,all negative results and9 cumulative original-plan observations')
