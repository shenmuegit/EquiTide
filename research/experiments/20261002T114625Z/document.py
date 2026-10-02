"""Publish complete frozen asymmetric-SMA/EMA grid and cumulative shadow observation."""
import collections,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary']
reasons=collections.Counter(k for c in cfg.values() for k in c['failed_criteria'])
lines=['# 本轮：非对称SMA65/EMA跨资产组合与冻结持仓延续','',
 '触发2026-10-02 11:46:25UTC，首工具11:47:04UTC；分支codex/strategy-research。只研究和模拟，无真实订单。','',
 '## 结论','',
 f"36个新组合分别先reserve，108个实际成本场景完成；36/36在1/2/3倍成本净正。{len(s['passed'])}项达到固定历史门槛，{len(s['rejected'])}项因正收益折不足淘汰；{len(s['both_periods_passed_pairs'])}组相同规则在2025/2026分别通过。全部结果包括淘汰记录保留。",
 '2025两方向各9/9通过；2026 BTC_ASMA/ETH_EMA方向6/9通过（EMA80三格淘汰），BTC_EMA/ETH_ASMA方向8/9通过（ASMA入场1.25%/EMA65淘汰）。通过仅表示复用开发历史门槛，不是稳定实盘盈利；部分参数实际净值相同，不能作为独立成功样本。',
 '另3项新截止的累计观测先reserve、9场景实际完成，699分钟、0完整日，partial记为rejected表示尚无180日/六折资格，不取消原冻结收集计划。累计净值前缀、仓位、首笔模拟成交和费用完整保留。',
 '本轮共39项finish、117场景；累计530规范定义、532历史ID、1084登记行，无reserved或缺结果。初始16项已有实际回测/案例关联证据，不代表全部达到长期稳健门槛。此前1006行/491规范定义的登记、结论全文、原Freqtrade逐折结果及checks/*oos.py全文以prior_summary.json.gz保留。','',
 '## 假设、完整规则与原值权重','',
 '假设：非对称SMA与EMA响应和持仓路径不同，分别分配给BTC/ETH或可改善逐折混合，也可能强化相关风险或延误上涨。事前固定两方向BTC_ASMA_ETH_EMA、BTC_EMA_ETH_ASMA；ASMA入场1.25/1.5/2%×EMA跨度50/65/80完整3×3面。ASMA固定65日、退出0.5%；EMA固定对称±1.5%，递推alpha=2/(span+1)。每方向每段9个新组合，共36，实际结果取得前预登记全部配置。',
 'ASMA每日i用前一完整close和此前65个完整close的Decimal均值：strict C>SMA×(1+entry)设置long，strict C<SMA×0.995设置cash，deadband/equality保持desired，不做连续多日确认。EMA数据首close为seed，每个完成日递推，决策i用前一已完成close对应EMA；seed记忆可早于滚动训练段，不作每折拟合/重置。指标、desired、现金/持币在六折连续，OOS从现金起始，决策后UTC00:01实际分钟open作执行参考，终止计退出成本。',
 '原值BTC75%/ETH25%是初始2000USDT的1500/500独立分仓，与策略方向无关；无归一化、转账、维持敞口或再平衡。复用24个已实际运行、同资金规模和同历史边界的成本化组件（每个三场景）；组合只将绝对分钟NAV相加，不二次乘权重，不平均收益/Sharpe，不增加新组件回测。源spec/report/archive与NAV SHA绑定，精确旧配置只读。源组件单独未过某资格，不自动禁止组合，但不消除组合自身的风险和门槛。','',
 '## 三项验证及局限','',
 'Walk-forward：180日滚动训练历史、3日gap、purge0（固定指标无拟合或监督标签），连续六个30日诊断折。2025与2026分别03-18 UTC00:01至09-14 UTC00:01；每成本场景259382点分钟/订单NAV计算整体DD，逐折净值乘积核对总收益，现金不按折重置。没有另做未登记跨年拼接。两段历史反复研究，规则/网格受到过去结果启发，因果日信号不消除选择偏差；不能称2025当时事前选出、独立最终留出、统计显著或稳定实盘正收益。',
 'Sensitivity：每年/每方向完整ASMA entry×EMA span面，共4面36格。所有成本/逐折收益、整体DD、Sharpe365、Calmar、交易数、成本比例、资格见report.json/sensitivity.csv，四面三倍正收益和正Sharpe比例均100%，但2026资格比例6/9和8/9。全部相邻12条边的2sd Sharpe差异标记保留，只描述变化而非统计显著；不能把收益全正解释为全指标平坦或完整资格平台。',
 'Costs：复用实际1500/500账本，每边fee10bp、halfspread1bp、slip2bp、冲击0.5×严格滞后20完整日sample log sigma×sqrt(订单预算/20日quoteADV)，参与率≤0.1%。四项同时1/2/3倍，额外Decimal tick取整成本单列，LOT_SIZE/min/max/notional/前5闭合分钟VWAP代理检查。spot仅无杠杆多头，无资金费或借币；余款、拒单、终止费用保留。Oct1静态元数据套历史为明确模型假设，没有历史动态reference/真实L2、IOC实成交、队列、延迟、部分成交和容量校准证据。',
 '固定资格：各成本净正，1x≥4/6正折，3x完整分钟DD≤25%，面内3x净正比例≥60%，1x≥2组件往返，参考价毛损益/执行成本≥2.5，无负余额，终止flat。正折门槛按既定1x，不代表每个成本每个折均盈利；往返是组件加总。现金无利息0为静态参考。',
 '淘汰判据次数：'+', '.join(f'{k}={v}' for k,v in reasons.items())+'。','',
 '## 全部新组合','',
 '|年份|方向|ASMA入场%|EMA跨度|1x收益%|2x%|3x%|3x分钟DD%|1x正折|1x往返|结论|',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for c in cfg.values():
 ss=c['scenes'];lines.append(f"|{c['year']}|{c['direction']}|{100*c['ASMA_entry_band']:g}|{c['EMA_span_days']}|{ss['1']['net_return_pct']:.5f}|{ss['2']['net_return_pct']:.5f}|{ss['3']['net_return_pct']:.5f}|{ss['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{ss['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 完整敏感性面及重复净值','', '|年份|方向|通过/9|不同3x NAV/9|3x收益范围%|3x DD范围%|描述cliff边/12|','|---|---|---:|---:|---|---|---:|']
for y in ('2025','2026'):
 for direction in grid['directions']:
  rows=[c for c in cfg.values() if c['year']==y and c['direction']==direction];sens=r['sensitivity'][f'{y}_{direction}'];unique=len({c['scenes']['3']['NAV_sha256_f64le'] for c in rows});returns=sens['metrics']['3']['return_range_pct'];dds=[c['scenes']['3']['max_drawdown_pct'] for c in rows]
  lines.append(f"|{y}|{direction}|{sum(c['status']=='passed' for c in rows)}|{unique}|{returns[0]:.5f}至{returns[1]:.5f}|{min(dds):.5f}至{max(dds):.5f}|{sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges'])}|")
lines+=['','## 预定中心ASMA entry1.5% / EMA span65','', '|年份|方向|3x收益%|3x分钟DD%|三倍六折收益%|前五折累计%|末折%|','|---|---|---:|---:|---|---:|---:|']
for y in ('2025','2026'):
 for direction in grid['directions']:
  c=cfg[f'asymhybrid_{y}_{direction}_e0.015_s65']['scenes']['3'];fold_text=', '.join(format(z['net_return_pct'],'.4f') for z in c['folds'])
  lines.append(f"|{y}|{direction}|{c['net_return_pct']:.5f}|{c['max_drawdown_pct']:.5f}|{fold_text}|{c['first_five_fold_return_pct']:.5f}|{c['last_fold_return_pct']:.5f}|")
lines+=['',
 '中心BTC_ASMA/ETH_EMA的2026三倍+19.96735%、DD13.09194%，前五折-0.80481%、末折+20.94070%；反方向+11.78289%、DD11.52624%，前五折-3.15156%、末折+15.42043%。仍靠末折扭转此前亏损，没有解决收益集中；不替换原冻结方案，也不以本轮OOS挑新参数。','',
 '## 旧结果只读比较','', '|年份|旧比较|3x收益%|3x分钟DD%|','|---|---|---:|---:|']
for name,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{name}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|")
lines+=['', 'SMA65对称±1%/75:25、同参数ASMA中心、EMA50±1.5%/75:25和50/50持有均读取既往实际结果，不重跑或reserve。持有资产权重/现金/风险敞口不匹配，不能声称等风险alpha。','',
 '## 原冻结方案累计699分钟观察','',
 '原SMA65/±1%/75:25及113625/forward_plan.json哈希保持2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81。沿用原浮点数量成本模型，不静默替换为历史Decimal LOT模型。从094655/forward_state.json的09:40延续到11:40UTC，新增120闭合分钟mark、0新成交；原现金/数量/desired状态/00:01首笔模拟买入/累计费用不变，无重复买入、重置或强制平仓。旧581 NAV点逐点保留为前缀，现701点（初始+执行参考+699闭合分钟）。',
 '依据[Binance官方市场数据接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)，每币取121条1m klines（09:39重叠bar全字段与旧最后bar一致），新增120条严格连续、closeTime+1≤11:40截止。源响应原字节gzip/SHA、URL、ms时间单位、status及实际取得时间保留。取数晚于截止，属延迟shadow重建，无真实订单或实时成交证据。','',
 '|累计观测|成本|净收益%|完整mark DD%|已有模拟买入|本段新成交|','|---|---|---:|---:|---:|---:|']
for name,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{name}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['executions']}|{z['new_executions']}|")
lines+=['',
 '组合累计1/2/3倍+1.77968/+1.64647/+1.51356%，三倍DD1.06769%；先前负收益快照继续保留。当前变化来自新闭合价mark，不是新盈利交易。699分钟、0完整日，不足180日/六折WF，前向敏感性未跑，不报短样本年化Sharpe/CAGR/Calmar；无新成交不增加真实成本/容量证据。',
 '下一轮读取本轮forward_state.json，从11:40原持仓延续；Oct3UTC00:01才下一日决策，原2027-03-31终止计划保持。新累计截止须先reserve，已有截止只读，不重开。forward_inputs兼容每资产直接minute数组及首段1d/1m字典。','',
 '## 审计、复现与下一轮','',
 '独立审计从四份真实分钟parquet和源Decimal现金/数量段重建72个已完成源组件场景，核对源NAV SHA后再独立构造108个组合，共28013256新组合NAV点，检查整体/六折指标、逐笔成本求和、毛损益减成本、固定资格和预登记顺序。前向另核对120新闭合mark、原响应SHA、旧净值前缀、原仓位/费用及9场景。所有108历史+9观测场景精确重放，39独立finish绑定最终报告SHA，registry检查通过，日志及verification.json保存。',
 '本轮运行无计算失败，无数据/权限障碍。复用014132组合评估/审计框架及094655持仓延续代码；源组件已经实际验证，不把重建NAV审计重复登记为新策略。大行情与全部分钟vector留在忽略data/，Git只保留spec、报告、全部压缩结果、必要代码、哈希和少量新原响应。',
 '复现：`bash research/experiments/20261002T114625Z/reproduce.sh`，仅读取缓存/归档，不重复HTTP或写登记。prepare.py仅首次预登记使用，已finish配置禁止再作为新实验计算。提交/push状态按实际远端在运行简报核对。',
 '下一轮继续原冻结观察；这批精确混合组合有实际结果应只读复用，可研究不同完整规则/参数/原值权重，但不能把相关历史网格当作独立实盘盈利证据。','']
(ROUND/'result.md').write_text('\n'.join(lines))
fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained');values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=plt.Normalize(min(values),max(values));cmap=plt.get_cmap('YlGn')
for iy,y in enumerate(('2025','2026')):
 for ix,direction in enumerate(grid['directions']):
  rows={(c['ASMA_entry_band'],c['EMA_span_days']):c for c in cfg.values() if c['year']==y and c['direction']==direction};assert len(rows)==9
  v=np.array([[rows[(e,span)]['scenes']['3']['net_return_pct'] for span in grid['EMA_span_days']] for e in grid['ASMA_entry_band']]);ax=axes[iy,ix];im=ax.imshow(v,cmap=cmap,norm=norm)
  for i,e in enumerate(grid['ASMA_entry_band']):
   for j,span in enumerate(grid['EMA_span_days']):
    rgb=cmap(norm(v[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];label='P' if rows[(e,span)]['status']=='passed' else 'R';ax.text(j,i,f'{v[i,j]:.2f}%\n{label}',ha='center',va='center',color='white' if lum<.48 else 'black')
  ax.set(xticks=range(3),xticklabels=grid['EMA_span_days'],yticks=range(3),yticklabels=[100*e for e in grid['ASMA_entry_band']],xlabel='EMA span days (band1.5%)',ylabel='ASMA65 entry band % (exit0.5%)',title=y+' | '+direction.replace('_',' '))
fig.colorbar(im,ax=axes.ravel().tolist(),label='3x cost net return (%)');fig.suptitle('ASMA65/EMA initial75/25 | P: historical gates pass, R: reject');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved all36 hybrid rows, four sensitivity panels and all9 cumulative observations')
