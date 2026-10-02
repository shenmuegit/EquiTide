"""Render full frozen-grid results and Chinese research conclusion."""
import json,collections
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());fr=json.loads((ROUND/'forward_report.json').read_text());s=r['summary'];cfg=r['configs'];reasons=collections.Counter(k for c in cfg.values() for k in c['failed_criteria'])
lines=['# 本轮：SMA连续多日确认与冻结模拟持仓延续','',
 '触发2026-10-02 05:44:34UTC，首工具05:45:13UTC；分支codex/strategy-research。仅研究/模拟，无真实订单。','',
 '## 结论','',
 f"54个新具体配置先reserve，162个真实成本场景完成；54/54在1/2/3倍成本均净正。{len(s['passed'])}项passed、{len(s['rejected'])}项rejected，全部保留。通过的仅是2025九个组合，2026组合0/9通过：全部只有3/6正收益折。相同规则在两段分别都通过的组合0组，连续确认未解决收益集中，不能替换原冻结计划。",
 '另3个新截止时间的累计观测配置分别reserve/finish，9成本场景有实际结果，含ETH三倍亏损。累计339分钟、0完整日，不能满足180日/六折资格，partial记录为rejected不取消长期计划。',
 '本轮合计57项finish、171场景；登记簿从377规范定义/778行变为434规范定义/892行，保留436历史ID，无reserved/缺结果。初始16项已有真实案例/回测证据，不代表全部通过完整长期资格。','',
 '## 假设、规则与预登记','',
 '假设：连续多日越过SMA缓冲带才改变desired持仓，或可过滤短暂穿越；也可能延迟入场/退出而错过上涨或放大回撤。事前固定SMA60/65/70日×连续确认2/3/4日，±1%对称带；两币种、两段历史，每段18组件+9组合，共54项。每项保存独立spec、reserve返回0后才计算。完整旧登记/结论/原Freqtrade逐折结果快照见prior_summary.json.gz。',
 '每日决策i只用已完整闭合的C[i-1]和prior N收盘Decimal均值SMA。strict C>SMA×1.01时above计数+1，否则above归零；strict C<SMA×0.99时below+1，否则below归零。above≥Q设置long，below≥Q设置cash，deadband/equality只保留desired但重置两个计数。最初OOS183从cash及两个0计数开始，暖机不预填确认计数；跨折保持计数、desired、真实模拟现金及数量。订单拒绝仅保持实际持仓，后续每日按desired重试。',
 'BTC/ETH原值75%/25%是初始2000USDT的1500/500，非维持敞口、无自动归一化、转账或再平衡。新参数组件各自实际计算完整成交与成本，组合复用本轮已算的同规模绝对分钟NAV相加，不再乘权重。终止平仓计费用。','',
 '## 三项验证与限制','',
 'Walk-forward：180日训练历史、3日gap、purge0（无拟合/标签），连续六个30日测试。2025与2026各自03-18 UTC00:01至09-14 UTC00:01，两段都已反复用于开发，不能称未触碰最终留出。完整259382点分钟/订单NAV计算每场整体DD，逐折净值乘积与连续总收益核对。无每折现金重置，也没有新登记的跨年收益拼接。',
 'Sensitivity：每年BTC、ETH、组合各有完整N×Q3×3面，共6面54格；全部1/2/3收益、DD、Sharpe365、Calmar、交易、成本、逐折、前五折和末折在report.json/CSV。六面三倍净正比例均100%，但2026组合资格0%，不能把盈利平台说成完整稳健平台。相邻2sd Sharpe差异只是描述标记，不作统计显著或最优声明。CSV的span列表示SMA lookback N，confirm_days列表示Q。',
 'Costs：每边fee10bp、halfspread1bp、slip2bp；冲击0.5×strictly previous20完整日sample log sigma×sqrt(订单预算/20日quote ADV)，参与率≤0.1%。四项同时1/2/3倍；Decimal tick/lot取整费用另记，min/max/notional、前5已闭合分钟VWAP参考代理按继承模型检查。仅无杠杆现货多头，无资金费或借币；成本/余款/拒单/终止退出完整保留。Oct1静态元数据套历史是明确压力假设，缺历史动态reference、真实L2/IOC实成交/队列/延迟/部分成交和容量校准，不能声称这些得到验证。',
 '固定门槛：各成本净正、1x≥4/6正折、3x完整分钟DD≤25%、邻域3x正比例≥60%、1x≥2组件往返、gross reference PnL/成本≥2.5、余额无负、终止flat。往返为组件加总。单项passed仅表示历史数值门槛。所有反复试验存在相关性和多重选择偏差，没有独立前向盈利结论。',
 '失败判据出现次数（可重叠）：'+', '.join(f'{k}={v}' for k,v in reasons.items())+'。','',
 '## 全部历史配置','',
 '|年份|范围|SMA N|确认Q|1x收益%|2x%|3x%|3x分钟DD%|1x正折|1x往返|结论|',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for c in cfg.values():
 ss=c['scenes'];lines.append(f"|{c['year']}|{c.get('asset','BTC75/ETH25组合')}|{c['lookback_days']}|{c['confirm_days']}|{ss['1']['net_return_pct']:.5f}|{ss['2']['net_return_pct']:.5f}|{ss['3']['net_return_pct']:.5f}|{ss['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{ss['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 预定中心N65/Q3：分折与比较','', '|年份|三倍六折收益%|前五折累计%|末折%|','|---|---|---:|---:|']
for y in ('2025','2026'):
 c=cfg[f'confirm_{y}_combo_n65_q3_btc0.75']['scenes']['3'];fold_text=', '.join(format(f['net_return_pct'],'.4f') for f in c['folds']);lines.append(f"|{y}|{fold_text}|{c['first_five_fold_return_pct']:.5f}|{c['last_fold_return_pct']:.5f}|")
lines+=['', '中心2026三倍总收益+21.00043%、分钟DD14.19589%，前五折-2.22772%、末折+23.75740%；原无连续确认SMA65同规模比较三倍+21.57073%、DD13.91280%。单个回溯参数点不能证明改进。','', '|年份|旧比较（只读）|3x收益%|3x分钟DD%|1x往返|','|---|---|---:|---:|---:|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['scenes']['1']['round_trips']}|")
lines+=['', '旧SMA65/75:25及50/50持有只读取旧实际结果，不重复计算或重新reserve。持有权重/现金风险不匹配，不声称等风险alpha；现金无利息0为静态参考，未另跑新现金策略。','',
 '## 原冻结方案延续：339分钟实际累计观测','',
 '原SMA65/±1%/75:25规则和113625/forward_plan.json哈希不变，原浮点数量核算继续。由014132的forward_state.json按币种/成本保留真实模拟现金、数量、desired状态、00:01买入成交及已计费用；01:40至05:40UTC只增加240个已闭合分钟mark，无新成交、无重复买入、无现金重置、无强制平仓。旧101个NAV点完全保留为前缀，现341点（初始+执行参考+339闭合分钟）。',
 '依据[Binance官方市场数据接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)取得1m klines，每币种241条含01:39重叠检查，raw响应原字节gzip/SHA、ms时间、URL/status/真实取得时间已保存。重叠bar全部字段与旧输入精确相同；新增240条连续且closeTime+1≤05:40截止。延迟取得的数据用于shadow重建，没有实时成交或真实交易。','',
 '|累计观测|成本|净收益%|完整mark DD%|既有模拟买入|本段新成交|',
 '|---|---|---:|---:|---:|---:|']
for name,c in fr['configs'].items():
 for k,v in c['scenes'].items():lines.append(f"|{name}|{k}x|{v['net_return_pct']:.5f}|{v['max_drawdown_pct']:.5f}|{v['executions']}|{v['new_executions']}|")
lines+=['',
 '组合1/2/3倍累计+0.92407/+0.79199/+0.66019%，三倍DD1.04923%；ETH三倍仍-0.07307%，全部正/负结果保留。组合从初始成本后的短期亏损转正只是当前价格mark变化。只有339分钟、0完整日，walk-forward180日/六折未完成、前向敏感性未运行，不报短样本年化Sharpe/CAGR/Calmar。无新成交只能验证持仓/成本连续性，不能新增真实成交成本或容量证据。',
 '最新forward_state.json来源/报告SHA与旧状态链均保留。下一轮必须从05:40UTC继续原仓位，Oct3UTC00:01才下一日决策；同日只加入随后闭合分钟。新累计截止先reserve，保持历史净值前缀/累计费用，已有截止只读。新forward_inputs.json.gz按资产直接存minute数组（旧首段按资产含1d/1m字典），续接时须兼容两种格式。原2027-03-31终止计划保持，不因为partial rejected而取消。','',
 '## 审计、复现与下一轮','',
 '独立审计从四份真实分钟parquet、Decimal SMA及独立倒序确认窗口重建19440个因果决策，逐笔核对330个Decimal成交的数量/参考/预算/滞后ADV/波动/fee/spread/slip/impact/tick/现金，核对42019884分钟NAV、逐折与资格。前向另审原始响应SHA、240新闭合marks、旧前缀、原仓位/累计成本以及9场景。全162历史+9累计观测场景精确重放；57个独立finish绑定相应最终报告，registry检查通过。',
 '模型/核算复用133655 Decimal kernel及234032的评估/审计框架，仅信号改为声明的连续确认；原代码/旧报告不修改。运行无策略计算失败、无数据/权限阻碍。行情/全分钟vector留忽略data/，Git只存轻量报告、spec、压缩逐笔状态、源哈希/原响应及代码。',
 '复现（使用已缓存行情，不重新HTTP/写登记）：`bash research/experiments/20261002T054434Z/reproduce.sh`。prepare.py仅首次预登记审计，已经finish的配置禁止再次计算为新实验。',
 '下一轮继续冻结计划并探索其他事前定义的低换手规则。连续确认的本轮精确配置不重跑；不要因总收益正就降低正折门槛或从这批OOS重新挑选后称独立验证。commit/push状态由运行简报另核对。','']
(ROUND/'result.md').write_text('\n'.join(lines))
fig,axes=plt.subplots(2,3,figsize=(13,8),layout='constrained');vals=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];vmin=min(vals);vmax=max(vals)
for row,y in enumerate(('2025','2026')):
 for col,group in enumerate(('BTC','ETH','combination')):
  ax=axes[row,col];cells=[c for c in cfg.values() if c['year']==y and c.get('asset','combination')==group];z=np.empty((3,3));labels={}
  for c in cells:
   i=[60,65,70].index(c['lookback_days']);j=[2,3,4].index(c['confirm_days']);z[i,j]=c['scenes']['3']['net_return_pct'];labels[(i,j)]='P' if c['status']=='passed' else 'R'
  im=ax.imshow(z,origin='upper',cmap='YlGn',vmin=vmin,vmax=vmax)
  for i in range(3):
   for j in range(3):ax.text(j,i,f'{z[i,j]:.2f}%\n{labels[(i,j)]}',ha='center',va='center',color='black',fontsize=10)
  ax.set_xticks(range(3),[2,3,4]);ax.set_yticks(range(3),[60,65,70]);ax.set_xlabel('Consecutive confirmations Q');ax.set_ylabel('SMA lookback N');ax.set_title(f'{y} {group} / 3x costs')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day net return (%)',shrink=.75);fig.suptitle('Fixed full SMA confirmation grid | P: historical gates pass, R: reject',fontsize=13)
fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved full Chinese result and six complete3x3 sensitivity panels')
