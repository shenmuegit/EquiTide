"""Render complete fixed volatility-ceiling results and cumulative original-plan observation."""
import collections,gzip,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary']
reasons=collections.Counter(k for c in cfg.values() for k in c['failed_criteria']);blocked={}
for name,c in cfg.items():
 if c['role']=='component':
  archive=json.loads(gzip.decompress((ROOT/c['archive']).read_bytes()));blocked[name]=sum(not d['volatility_eligible'] for d in archive['scenes']['1']['decisions'])
lines=['# 本轮：SMA65波动率上限过滤与原冻结持仓延续','',
 '触发2026-10-02 13:47:33UTC，首工具13:48:25UTC；分支codex/strategy-research。仅研究和模拟，无真实订单。','',
 '## 结论','',
 f"54个新配置全部先reserve，162个实际成本场景完成；54/54在1/2/3倍成本净正。{len(s['passed'])}项达到固定历史门槛，{len(s['rejected'])}项淘汰；{len(s['both_periods_passed_combination_pairs'])}组同规则组合在2025/2026分别通过。全部结果保留，不把rejected等同亏损。",
 '2025 BTC9/9、ETH3/9、组合9/9通过；2026 BTC/ETH各0/9，组合6/9通过，60%波动上限的三个组合因正折不足淘汰。较低波动门槛没有统一改善稳健性。',
 '事前中心入场1.5%/波动上限80%的三倍收益2025+29.85703%、2026+20.43557%，分钟DD14.03735/13.45730%。2026前五折+0.18578%、末折+20.21225%；前五折与无过滤中心相同，过滤主要减少末折收益，尚未证明改善原问题。2026上限100%两币均0个高波动日，组合净值等于无过滤旧结果，不能当新保护效果证据。',
 '另3个新截止的累计观测先reserve，9场景实际完成；819分钟、0完整日，partial记为rejected表示未取得180日/六折资格，不取消原冻结计划。仓位、净值前缀、原首笔模拟买入和累计成本连续保留。',
 '本轮共57项finish、171场景；累计587规范定义、589历史ID、1198登记行，无reserved或缺结果。初始16项已有实际案例/回测关联证据，不表示全部取得长期稳健资格；此前1084行/530定义的登记、所有结论、原Freqtrade逐折结果与checks/*oos.py全文以prior_summary.json.gz保存。','',
 '## 知识来源、假设和完整规则','',
 '研究动机参考[Moreira/Muir：Volatility Managed Portfolios](https://www.nber.org/papers/w22208)，NBER WP22208、2016年4月/6月修订，2026-10-02访问摘要。摘要提出高波动时降低风险的思路，其研究对象包括股票因子和货币套利；本轮BTC/ETH二元现金上限规则是新假设，不是论文策略复现，也不能从论文推断虚拟货币盈利。',
 '假设：滞后波动率过高时转现金，或可避开波动行情，也可能退出后错过反弹并增加换手。预先固定SMA65、入场缓冲1.25/1.5/2%×年化波动上限60/80/100%完整3×3面，退出固定0.5%，波动窗口20个日收益；两币种、两段历史各18组件+9组合，共54。未见本轮结果前登记全部spec，不在OOS调参或降低门槛。',
 '每日决策i只用截至i-1的完整close。SMA为此前65个close的Decimal均值；波动用此前21个close形成20个ln(C[t]/C[t-1])收益，ddof1样本方差，年化vol=sqrt(365×方差)，Decimal精度28。单位为年化波动fraction，与策略年化收益不同。vol≤cap允许趋势规则，vol>cap立即设置desired=cash。允许时strict priorclose>SMA×(1+entry)设置long；strict priorclose<SMA×0.995设置cash；deadband/equality保持desired。',
 '高波动将desired重置为cash，恢复后价格在deadband时仍现金；恢复且priorclose已经高于入场阈值即可入场，不要求新的一次由下到上的价格穿越事件。OOS183从cash开始，指标暖机，但不预填持仓；跨六折保持desired及实际模拟现金/数量，无多日确认或每折重置。每日决策后的UTC00:01真实分钟open作执行参考，终止退出计成本。按日过滤不保证盘中止损。',
 '原值BTC75%/ETH25%为初始2000USDT的1500/500独立分仓；无归一化、转账、每日维持敞口或再平衡。新规则组件实际计算完整成交、取整和成本；组合优先复用本轮已算的同资金规模成本化绝对分钟NAV相加，不二次乘权重，不平均Sharpe/收益。','',
 '## 三项验证及限制','',
 'Walk-forward：180日滚动训练历史、3日gap、purge0（固定规则，无拟合或标签），连续六个30日诊断折。2025/2026分别03-18 UTC00:01至09-14 UTC00:01；每场259382点订单/分钟NAV计算整体DD，核对逐折净值乘积与连续总收益，不按折重置现金，不新建未登记跨年拼接净值。两段历史反复开发，规则选择受旧结果启发，日信号因果不能消除回溯选择和多重试验偏差；不是独立最终留出或稳定实盘盈利证据。',
 'Sensitivity：每年BTC、ETH、组合各有完整entry×cap面，共6面54格。全部成本/逐折收益、整体DD、日Sharpe365、Calmar、交易数、成本、前五/末折及资格在report.json/CSV保留。六面三倍收益/Sharpe正比例均100%，完整资格并非全部通过；相邻12条边的2sd Sharpe差异仅为描述，标记和所有格点保留，不作统计显著/最优参数声明。相同净值不增加独立证据。',
 'Costs：每边fee10bp、halfspread1bp、slip2bp，冲击0.5×严格滞后20完整日sample log sigma×sqrt(预算/20日quoteADV)，参与率≤0.1%。四项同时1/2/3倍，额外Decimal tick取整成本单列，LOT_SIZE/min/max/notional和前5闭合分钟VWAP代理检查。现货无杠杆多头，无资金费/借币；余款、拒单、终止成本保留。Oct1静态元数据用于历史是模型假设；历史动态reference、真实L2/IOC实成交、队列、延迟、部分成交和容量校准未验证。',
 '固定门槛：各成本净正，1x≥4/6正折，3x完整分钟DD≤25%，同面3x净正比例≥60%，1x≥2组件往返，参考价毛损益/执行成本≥2.5，无负余额，终止flat。组合往返为组件之和；正折门槛按原1x，不代表每成本每折均盈利。现金无利息0为静态参考。',
 '失败判据次数可重叠：'+', '.join(f'{k}={v}' for k,v in reasons.items())+'。27项淘汰都出现正折不足，其中6项另有回撤超限。','',
 '## 全部历史配置','',
 '|年份|范围|入场%|年化vol上限%|1x收益%|2x%|3x%|3x分钟DD%|1x正折|1x往返|高波动日/180|结论|',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for name,c in cfg.items():
 ss=c['scenes'];guard=str(blocked[name]) if name in blocked else '组件分别见上'
 lines.append(f"|{c['year']}|{c.get('asset','BTC75/ETH25组合')}|{100*c['entry_band']:g}|{100*c['volatility_ceiling']:g}|{ss['1']['net_return_pct']:.5f}|{ss['2']['net_return_pct']:.5f}|{ss['3']['net_return_pct']:.5f}|{ss['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{ss['1']['round_trips']}|{guard}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 完整敏感性面','', '|年份|范围|通过/9|不同3x NAV/9|3x收益范围%|描述cliff边/12|','|---|---|---:|---:|---|---:|']
for y in ('2025','2026'):
 for group in ('BTC','ETH','combination'):
  rows=[c for c in cfg.values() if c['year']==y and c.get('asset','combination')==group];sens=r['sensitivity'][f'{y}_{group}'];a,b=sens['metrics']['3']['return_range_pct'];unique=len({c['scenes']['3']['NAV_sha256_f64le'] for c in rows})
  lines.append(f"|{y}|{group}|{sum(c['status']=='passed' for c in rows)}|{unique}|{a:.5f}至{b:.5f}|{sum(e['cliff_flag_2sd'] for e in sens['adjacent_edges'])}|")
lines+=['','## 预定入场中心1.5%：完整上限邻域与分折','', '|年份|vol上限%|3x收益%|3x DD%|三倍六折收益%|前五折累计%|末折%|结论|','|---|---:|---:|---:|---|---:|---:|---|']
for y in ('2025','2026'):
 for cap in grid['annual_volatility_ceiling']:
  c=cfg[f'volguard_{y}_combo_e0.015_v{cap}_btc0.75'];z=c['scenes']['3'];fold_text=', '.join(format(a['net_return_pct'],'.4f') for a in z['folds'])
  lines.append(f"|{y}|{100*cap:g}|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{fold_text}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|{c['status']}|")
lines+=['',
 '中心80%相较无过滤ASMA中心：2025三倍收益35.90921→29.85703%、DD14.55663→14.03735%；2026收益21.26486→20.43557%、DD仍13.45730%，前五折仍+0.18578%。60%门槛的2025中心DD降至10.73934%，但2026前五折-1.22987%、正折不够，不能只取某段改善。100%门槛在2026全180日两币均未触发，净值与无过滤对应参数完全一致。不能称过滤统一改进或6组独立保护证明，不更换原冻结前向规则。','',
 '## 旧结果只读比较','', '|年份|旧比较|3x收益%|3x分钟DD%|','|---|---|---:|---:|']
for name,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{name}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|")
lines+=['', '旧SMA65±1%/75:25、同entry1.5%/exit0.5%的无过滤ASMA及50/50持有均只读取实际结果，不重算/登记。持有权重/现金/敞口不匹配，不声称等风险alpha。','',
 '## 原冻结方案累计819分钟观察','',
 '原SMA65/±1%/75:25及113625/forward_plan.json哈希保持2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81，不把新波动过滤应用到原观察器。保留原浮点数量/成本模型，不静默替换为历史Decimal LOT模型。从114625/forward_state.json的11:40延续至13:40UTC，新120闭合分钟mark、0新成交。原现金/数量/desired/首笔模拟买入/累计成本不变，无重复买入、重置或强制平仓；旧701 NAV点逐点保留为前缀，现821点（初始+执行参考+819闭合分钟）。',
 '依据[Binance官方市场数据接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)，每币取得121条1m klines，11:39重叠bar全字段与旧末bar相同；新增120条连续且closeTime+1≤13:40截止。源响应原字节gzip/SHA、URL、ms单位、status和实际取得时间保留；取得时间晚于截止，属延迟shadow重建，无真实订单或实时成交证据。','',
 '|累计观测|成本|净收益%|完整mark DD%|已有模拟买入|本段新成交|','|---|---|---:|---:|---:|---:|']
for name,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{name}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['executions']}|{z['new_executions']}|")
lines+=['',
 '组合累计1/2/3倍+2.44175/+2.30768/+2.17390%，三倍DD1.06769%；旧负收益记录继续保留。当前变化来自价格mark，不是新增盈利交易。819分钟、0完整日，180日/六折WF未完成，前向敏感性未跑，不报短样本年化Sharpe/CAGR/Calmar；无新成交不增加真实费用/容量证据。',
 '下一轮读取本轮forward_state.json，从13:40原持仓延续；Oct3UTC00:01才下一日决策，原2027-03-31终止日保持。新累计截止先reserve，已有截止只读；输入兼容每资产直接minute数组及首段1d/1m字典。','',
 '## 审计、复现和下一轮','',
 f"独立审计从四份真实分钟parquet和Decimal收盘计算19440个因果波动/均值/desired决定，逐历史前缀倒查末次强制cash或趋势事件，核对{s['actual_component_fills']}个Decimal成交的预算、价格、数量、滞后ADV和成本/取整/现金，检查42019884个历史NAV点和逐折/资格。前向另审源响应SHA、120新闭合mark、旧前缀、仓位/费用和9场景。全部162历史+9观测场景精确重放；57独立finish绑定最终报告SHA，registry检查通过，日志及verification.json保留。",
 '本轮无计算失败或数据/权限障碍。复用094655评估/成交/分钟NAV框架，仅按预定规则增加波动过滤，独立审计不调用生产signal。大行情/全分钟vector留忽略data/，Git保存全部spec、报告、压缩逐配置结果、必要代码、数据哈希和少量新原响应。',
 '复现：`bash research/experiments/20261002T134733Z/reproduce.sh`，仅使用缓存/归档，不重复HTTP或写登记；prepare.py仅首次预登记使用，已finish精确配置不能再次作为新实验。提交/push状态由运行简报核对远端。',
 '下一轮继续原冻结观察，研究不同完整规则/参数或原值权重。这批过滤精确配置应读取复用；不得从同历史重选80/100%后称独立验证，也不得把未触发过滤的路径当新风险控制成功。','']
(ROUND/'result.md').write_text('\n'.join(lines))
fig,axes=plt.subplots(2,3,figsize=(13,8),layout='constrained');values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=plt.Normalize(min(values),max(values));cmap=plt.get_cmap('YlGn')
for iy,y in enumerate(('2025','2026')):
 for ix,group in enumerate(('BTC','ETH','combination')):
  cells={(c['entry_band'],c['volatility_ceiling']):c for c in cfg.values() if c['year']==y and c.get('asset','combination')==group};assert len(cells)==9
  z=np.array([[cells[(e,cap)]['scenes']['3']['net_return_pct'] for cap in grid['annual_volatility_ceiling']] for e in grid['entry_band_fraction']]);ax=axes[iy,ix];im=ax.imshow(z,norm=norm,cmap=cmap)
  for i,e in enumerate(grid['entry_band_fraction']):
   for j,cap in enumerate(grid['annual_volatility_ceiling']):
    rgb=cmap(norm(z[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];label='P' if cells[(e,cap)]['status']=='passed' else 'R';ax.text(j,i,f'{z[i,j]:.2f}%\n{label}',ha='center',va='center',color='white' if lum<.48 else 'black')
  ax.set(xticks=range(3),xticklabels=[60,80,100],yticks=range(3),yticklabels=[1.25,1.5,2],xlabel='Annualized20-day volatility ceiling (%)',ylabel='ASMA65 entry band % (exit0.5%)',title=f'{y} {group} | 3x costs')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day net return (%)',shrink=.75);fig.suptitle('Fixed volatility ceiling grid | P: historical gates pass, R: reject');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved all54 fixed configurations, six sensitivity panels, guard activity and all9 observations')
