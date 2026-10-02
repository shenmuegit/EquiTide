"""Render extension grids with explicit new/reused scopes and original-plan losses."""
import collections,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary'];fresh={n:c for n,c in cfg.items() if c['is_new']}
reasons=collections.Counter(k for c in fresh.values() for k in c['failed_criteria'])
lines=['# 本轮：收盘通道参数边界扩展与原冻结持仓延续','',
 '触发2026-10-02 17:49:33UTC，首工具17:49:48UTC；分支codex/strategy-research。仅研究与模拟，无真实订单。','',
 '## 结论','',
 f"48个新定义全部先reserve，144个新实际成本场景完成；48/48在1/2/3倍成本均净正。{len(s['passed'])}项达到固定历史门槛，{len(s['rejected'])}项淘汰，全部保留。另6个20/30已有配置及18成本场景仅读取旧报告/归档/完整NAV，未重复reserve/finish或跑生产回测。完整54格/162成本场景保留。",
 f"完整组合邻域{len(s['both_periods_passed_combination_pairs'])}/9组在2025/2026分别通过，其中{len(s['new_both_periods_passed_combination_pairs'])}组为本轮新配置、1组20/30旧配置。事前中心15/40也在两段通过：三倍2025+34.48492%/DD14.03555%，2026+23.57471%/DD15.12711%。这是重复开发历史中的局部资格区域，不是独立前向、统计显著或稳定实盘盈利。",
 '中心2026三倍前五折-0.21733%、末折+23.84386%，收益集中仍未解决；15/30的2026前五折+2.74556%、末折+23.88183%，较宽窗口退出常伴随更大回撤或较低收益。2025组合只6条不同三倍NAV，部分不同退出窗口实现相同路径，不能当6/9个独立验证样本。',
 '另3个新截止累计观测先reserve，9场景实际完成；原冻结SMA65持仓累计1059分钟、0完整日，三倍从旧+0.05924%转为-0.84762%、DD2.95723%，BTC/ETH全部成本都负。新120分钟0新成交，亏损来自原持仓mark，不是新增交易。partial记rejected只表示未取得180日/六折资格，原冻结计划继续收集。',
 '本轮共51新配置finish、153新成本场景；加18只读旧场景，全171场景留证/审计。累计695规范定义、697保留ID、1414登记行，无reserved或缺结果。初始16条已有真实案例/回测关联证据，不表示全部长期合格。此前1312行/644规范定义的完整登记、全部结论、原Freqtrade逐折结果与checks/*oos.py全文保存为prior_summary.json.gz。','',
 '## 假设、知识来源与预登记','',
 '上一轮20/30通道组合处于最短入场/最长退出边缘，本轮预设入场10/15/20日×退出30/40/50日、中心15/40，检验邻域完整资格是否扩大。更快入场可能增加假突破；延长退出可能减少反复交易，也可能扩大下跌损失和回吐。没有在本轮结果后换网格、阈值或门槛。',
 '参考[Brock/Lakonishok/LeBaron：Simple Technical Trading Rules and the Stochastic Properties of Stock Returns](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1992.tb04681.x)，Journal of Finance47(5)，1992年12月，1731–1764，2026-10-02重新访问出版者摘要。摘要研究DJIA1897–1986的均线和区间突破，提供方向；收盘通道/多头现金/本轮窗口是自定扩展，不是论文原规则或bootstrap复现，不能从论文推断加密货币盈利。',
 '精确复用20/30的完整spec，指纹、原规则文字、参数外的资金/执行/数据边界一致；新具体spec仅调整入场/退出长度，不通过改名/描述制造新配置。48新格先reserve，6旧格记录源report/spec/archive和NAV SHA供比较，登记原状态/原criteria/报告哈希保持。完整面包含旧格的扩展邻域判据仅是结果比较，不追加旧条目finish。','',
 '## 完整规则与资金含义','',
 '每日决策i测试C[i-1]；入场上界max(C[i-entry-1:i-1])恰好entry个完整日CLOSE、最晚i-2；退出下界min(C[i-exit-1:i-1])恰好exit个、同样最晚i-2。区间排除被测试收盘，Decimal精度28，不用日内high/low。strict收盘>上界设置desired-long，strict收盘<下界设置desired-cash，相等或无事件保持desired。',
 '允许exit>entry，明确作为本轮规则，不称经典海龟原规则。无均线、波动过滤、缓冲、多日确认、盘中止损、金字塔或空头。原参数描述的61日暖机上限保留以保持规则身份，所用窗口最长50日；实际可用历史充足，OOS183从desired-cash及现金开始，无预填持仓。',
 '前日收盘UTC00:00可得，随后UTC00:01真实分钟open作执行参考；终止退出计费用。跨六折持续desired及模拟现金/持币，拒单不改持仓、后续每日可重试。原值BTC75/ETH25为2000USDT的1500/500初始独立分仓；无自动归一化、跨仓转账、维持权重或再平衡。组合复用本轮同资金规模成本化绝对分钟NAV相加，无二次乘权重或平均Sharpe/回撤。','',
 '## 三项验证及限制','',
 'Walk-forward完成：每段180日滚动训练历史、3日gap、purge0，无拟合/监督标签；连续六个30日诊断折、持仓/现金跨折延续。2025/2026分别03-18UTC00:01至09-14UTC00:01；每场259382个完整分钟/订单NAV点计算整体回撤，核对逐折乘积与连续收益。两段反复研究，本轮网格由已见旧结果启发；信号因果不消除回溯选择和多重试验偏差。不是未触碰最终测试集，不新造跨年拼接收益。',
 'Sensitivity完成：每年BTC/ETH/组合各完整3×3面、共54格，其中48新+6只读旧；全部成本/逐折收益、完整DD、日Sharpe365、Calmar、交易/费用、前五/末折和资格保存。三倍收益/Sharpe正比例全部100%，完整资格另列。相邻12边Sharpe差异的2sd标记只作描述，不是显著性或最优点证明；相同NAV和相同历史不能增加独立证据。',
 'Costs完成：每边fee10bp、halfspread1bp、slip2bp，冲击0.5×滞后20完整日sample log sigma×sqrt(预算/20日quoteADV)，参与率≤0.1%；四项同时1/2/3倍，Decimal tick成本单列。LOT/min/max/notional、前5闭合分钟VWAP代理、现金/持币约束实际检查。现货无杠杆多头，无资金费/借币、USDT利息。Oct1静态元数据用于历史是假设，不是历史交易所校验；无真实历史L2、IOC、队列、延迟、部分成交或冲击容量校准证据。',
 '门槛保持：各成本净正；1x≥4/6正折；3x分钟DD≤25%；同面三倍正收益比例≥60%；1x≥2组件往返；参考价毛损益/执行成本≥2.5；无负余额；终止flat。组合往返为组件之和，不保证每折/每成本盈利。旧50/50持有权重/现金敞口不同，只读比较，不声称等风险alpha。',
 '新配置淘汰判据次数可重叠：'+', '.join(f'{k}={v}' for k,v in reasons.items())+'。全部19项与逐项原因保存，不把资格失败等同亏损。','',
 '## 完整54格历史结果','',
 '|年份|范围|新/复用|入场日|退出日|1x收益%|2x%|3x%|3x分钟DD%|1x正折|1x往返|本面资格/失败判据|',
 '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for name,c in cfg.items():
 ss=c['scenes'];mode='新' if c['is_new'] else '复用';lines.append(f"|{c['year']}|{c.get('asset','BTC75/ETH25组合')}|{mode}|{c['entry_days']}|{c['exit_days']}|{ss['1']['net_return_pct']:.5f}|{ss['2']['net_return_pct']:.5f}|{ss['3']['net_return_pct']:.5f}|{ss['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{ss['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 六个完整敏感性面','', '|年份|范围|本面通过/9|新增通过/8|不同3x NAV/9|3x收益范围%|描述cliff边/12|','|---|---|---:|---:|---:|---|---:|']
for y in ('2025','2026'):
 for group in ('BTC','ETH','combination'):
  rows=[c for c in cfg.values() if c['year']==y and c.get('asset','combination')==group];sens=r['sensitivity'][f'{y}_{group}'];a,b=sens['metrics']['3']['return_range_pct'];unique=len({c['scenes']['3']['NAV_sha256_f64le'] for c in rows})
  lines.append(f"|{y}|{group}|{sum(c['status']=='passed' for c in rows)}|{sum(c['status']=='passed' and c['is_new'] for c in rows)}|{unique}|{a:.5f}至{b:.5f}|{sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges'])}|")
lines+=['','## 全部组合的前五折/末折与逐折收益','', '|年份|入场/退出日|新/复用|三倍六折收益%|前五折累计%|末折%|资格|','|---|---|---|---|---:|---:|---|']
for c in cfg.values():
 if c['role']=='combination':
  z=c['scenes']['3'];fold_text=', '.join(format(a['net_return_pct'],'.4f') for a in z['folds']);mode='新' if c['is_new'] else '复用';lines.append(f"|{c['year']}|{c['entry_days']}/{c['exit_days']}|{mode}|{fold_text}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|{c['status']}|")
lines+=['','## 六个旧格原始状态保持','', '|旧配置|原登记状态|本扩展面状态|原报告|','|---|---|---|---|']
for name,c in cfg.items():
 if not c['is_new']:lines.append(f"|{name}|{c['source_record_status']}|{c['status']}|{c['source_ref']['report']}|")
lines+=['','## 只读旧比较','', '|年份|旧比较|3x收益%|3x分钟DD%|','|---|---|---:|---:|']
for name,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{name}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|")
lines+=['','## 原冻结方案累计1059分钟：转负结果保留','',
 '原SMA65±1%/75:25、113625/forward_plan.json哈希仍为2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81。保留原浮点数量/成本模型，读取154903/forward_state.json/report，从15:40原现金/数量/desired/历史费用延续到17:40UTC；新增120closed mark、0新成交，不重置、不重复初始模拟买入、不在本轮强制平仓。旧941 NAV点逐点保持，现1061点（初始+执行参考+1059闭合分钟）。',
 '依据[Binance官方行情接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)，每币取得121条真实1m klines，15:39重叠bar全字段匹配旧末bar；新120条连续且closeTime+1≤17:40截止。保存原HTTP响应字节gzip/SHA、URL、毫秒单位、status和取得时间，晚于截止的取得明确是延迟shadow重建，无实时执行或真实订单证据。','',
 '|累计观测|成本|净收益%|完整mark DD%|本段收益%|已有模拟买入|本段新成交|','|---|---|---:|---:|---:|---:|---:|']
for name,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{name}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['executions']}|{z['new_executions']}|")
lines+=['',
 '组合累计1/2/3倍-0.58769/-0.71780/-0.84762%，三倍DD2.95723%，BTC/ETH各成本全负；最新120分钟组合约-0.90633%。旧正/负收益记录均保留，不能以反复正收益历史代替这段新亏损。1059分钟仅17小时39分、0完整日，180日/六折WF未完成，前向参数敏感性未跑，不报短样本年化Sharpe/CAGR/Calmar；无新成交不增加费用/容量实证。',
 '下一轮读取本轮forward_state.json，从17:40原持仓延续；Oct3UTC00:01下一日决策与2027-03-31计划终止保持，新截止先reserve，旧截止只读。输入兼容每资产直接minute数组及首段1d/1m字典。','',
 '## 审计、复现与下一轮','',
 f"独立审计对完整54格162场景（144新、18只读旧）从四份真实分钟parquet/Decimal收盘，用排序区间和逐前缀末次强制事件核对19440因果决定；核对{s['audited_component_fills']}个已有/新增Decimal回测模拟成交，其中{s['actual_component_fills']}个为本轮回测模拟成交，核对42019884个完整分钟NAV和逐折/整体指标、门槛。前向另审源响应SHA、120新closed mark、旧前缀、仓位/费用和9场景。全部144新历史+9新观测精确重放，18旧场景读取核验，51独立finish绑定最终报告SHA；旧6记录不变、registry检查通过，日志和verification.json保留。",
 '本轮无回测计算失败或数据/权限障碍。复用154903信号及成交/分钟NAV框架，仅扩展已冻结窗口并增加精确旧格读取；原信号文件字节相同。所有新spec、压缩逐配置结果、报告、数据哈希、必要代码和少量新原响应保存；大行情及全分钟vector在忽略data/。新报告指向完整旧归档，不复制或覆盖旧结果。',
 '复现：`bash research/experiments/20261002T174933Z/reproduce.sh`；只缓存重放，无新HTTP/登记。prepare.py仅首次预登记，已finish精确配置不得作为新实验重复。实际push由运行简报核对远程ref/提交tree和本地文件。',
 '下一轮继续原冻结模拟并探索新规则/新原值权重组合。此扩展精确配置只读复用。6/9只是重复历史局部数值资格区域；中心仍集中末折，较长退出扩大某些回撤，原真实行情模拟已转负，不能声称找到稳定实盘正收益。','']
(ROUND/'result.md').write_text('\n'.join(lines))
fig,axes=plt.subplots(2,3,figsize=(13,8),layout='constrained');values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=plt.Normalize(min(values),max(values));cmap=plt.get_cmap('YlGn')
for iy,y in enumerate(('2025','2026')):
 for ix,group in enumerate(('BTC','ETH','combination')):
  cells={(c['entry_days'],c['exit_days']):c for c in cfg.values() if c['year']==y and c.get('asset','combination')==group};assert len(cells)==9
  z=np.array([[cells[(e,x)]['scenes']['3']['net_return_pct'] for x in grid['exit_lookback_days']] for e in grid['entry_lookback_days']]);ax=axes[iy,ix];im=ax.imshow(z,norm=norm,cmap=cmap)
  for i,e in enumerate(grid['entry_lookback_days']):
   for j,x in enumerate(grid['exit_lookback_days']):
    c=cells[(e,x)];rgb=cmap(norm(z[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];label='P' if c['status']=='passed' else 'R';suffix=' *' if not c['is_new'] else '';ax.text(j,i,f'{z[i,j]:.2f}%\n{label}{suffix}',ha='center',va='center',color='white' if lum<.48 else 'black')
  ax.set(xticks=range(3),xticklabels=[30,40,50],yticks=range(3),yticklabels=[10,15,20],xlabel='Exit close-range lookback (days)',ylabel='Entry close-range lookback (days)',title=f'{y} {group} | 3x costs')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day net return (%)',shrink=.75);fig.suptitle('Channel boundary extension | P: historical pass, R: reject | *: exact reused cell');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved all54 cells with explicit48 NEW/6 REUSED labels,6 sensitivity panels and all9 negative cumulative observations')
