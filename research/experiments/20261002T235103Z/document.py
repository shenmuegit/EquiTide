"""Retain every confirmation configuration, failures, concentration and shadow loss."""
import collections,gzip,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());cfg=r['configs'];grid=r['plan']['grid'];s=r['summary'];prior=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));reasons=collections.Counter(k for c in cfg.values() for k in c['failed_criteria'])
lines=['# 本轮：EMA确认的收盘通道突破','',
 '触发2026-10-02 23:51:03UTC；首工具23:51:39UTC；分支codex/strategy-research，先fetch/ff同步，基点dc692309d21a1844d72828111065c98cc88e57dd。使用walk-forward-validation、ml4t-sensitivity-analysis、ml4t-transaction-costs三技能。真实行情历史回测及延迟shadow模拟，无实盘订单。','',
 '## 筛选结论','',
 f"54个新具体配置先独立reserve，162成本场景完成：36组件＋18组合、42019884分钟/执行NAV点，{s['actual_component_fills']}笔新组件模拟成交。{s['positive_1x']}/54在1x、{s['positive_3x']}/54在3x净正；{len(s['passed'])}项通过固定历史门槛、{len(s['rejected'])}项淘汰，其中3个ETH2026配置完整负收益，均保留并finish。失败原因次数（同一配置可多项失败）：{dict(reasons)}。",
 f"{len(s['both_periods_passed_combination_pairs'])}/9组相同参数组合在两段历史分别通过：EMA50及通道入场10/15/20日，退出通道30日、EMA两边1.5%、初始BTC/ETH75/25。三组2026净值完全相同，不是3条独立盈利路径。该区域由本轮预登记完整网格筛得，不能把事后筛选说成事前中心或独立样本。",
 '|年份|两段均通过区域：通道入场/EMA日|3x净收益%|3x整体分钟DD%|1x正折|3x前五折%|3x末折%|',
 '|---|---|---:|---:|---:|---:|---:|']
for c in cfg.values():
 if c['role']=='combination' and c['span_days']==50:
  z=c['scenes']['3'];lines.append(f"|{c['year']}|{c['entry_days']}/{c['span_days']}|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['',
 '事前中心通道15/30日＋EMA65±1.5%：2025组合三倍+30.91536%/DD13.06905%、4/6正折而通过；2026三倍+11.52889%/DD10.17854%、仅3/6正折而淘汰。2026中心前五折-3.19144%、末折+15.20561%；通过EMA50区域前五折-1.38211%、末折+15.10789%，收益集中问题没有消失。',
 '通过区域2026三倍+13.51698%/DD13.32351%，低于旧同通道15/30的+27.28308%/DD12.63003%，也低于上一轮BTC通道＋ETH EMA中心+24.87745%/DD12.00428%。加入确认/提前退出在本段历史未得到统一改善。组件2026全部未达到折数门槛，但EMA50的组合有4/6正折，资格按真实组合连续净值评估，不要求每组件单独通过。','',
 f"本轮57新定义finish，含3个新截止观察；累计830规范定义、832保留ID、1684登记行，无reserved或缺结果。此前{prior['lines']}行/{prior['canonical']}规范定义、{len(prior['records'])}保留记录、{len(prior['prior_conclusions'])}轮全文结论、{len(prior['legacy_results'])}份Freqtrade结果JSON和{len(prior['checks_read'])}份checks/*oos.py全文已读并保存在prior_summary.json.gz。初始16条已有实际关联结果，不代表均符合长期盈利门槛。",'',
 '## 假设、来源与预登记','',
 '新规则将通道突破与EMA趋势确认结合到同一持仓状态：入场需两条件同时成立，退出由任一反向条件触发。假设过滤弱突破可能减少错误持仓；同时承认会错过回升、加大反复出入及仍集中在趋势末段。完整网格及中心在本轮结果前固定，未根据收益改变门槛、参数或原观察方案。它是新信号规则，不能复用原通道或EMA单组件的交易净值；36新组件按真实1500/500本金重算，18新组合复用这些刚完成的成本化绝对净值。',
 '参考[pandas.DataFrame.ewm官方说明](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)，2026-10-02访问文档3.0.6，支持alpha=2/(span+1)及adjust=False递推。生产信号Python浮点手工递推，独立审计用本地pandas2.2.3另算；未升级运行时。联合确认/OR退出是本轮自定经济假设，文档没有提供加密货币盈利证据。','',
 '## 完整规则、资金与边界','',
 '决策i的已完成C[i-1]严格高于max(C[i-entry-1:i-1])且float(C[i-1])>E[i-1]×1.015，才设desired-long；C[i-1]严格低于min(C[i-31:i-1])或float(C[i-1])<E[i-1]×0.985时设cash，退出优先；其余/相等保持desired。通道参照止于i-2，排除被测试收盘，使用CLOSE而非日内high/low。没有突破后等待EMA的arming记忆。',
 '通道比较Decimal28；EMA为float：E[0]=数据集首个完成日收盘，alpha=2/(span+1)，E[j]=(1-alpha)E[j-1]+alpha C[j]，从日0递推且跨折不重置，seed记忆早于滚动train起点。各配置OOS183从现金和desired-cash开始。无标签/模型拟合、测试集选参、盘中止损、空头、杠杆、加仓或每折重开。',
 '网格通道entry10/15/20×EMAspan50/65/80；exit30与EMA±1.5%固定。前日收盘UTC00:00可得，参考执行取随后UTC00:01真实分钟open，假设marketable LIMIT IOC立即按估计不利价成交。Decimal28现金/数量/成本核算，buy价向上/sell向下取tick、数量向下取LOT、残余现金留存；拒单不改现金/数量、下次日决策可重试。终止平仓含成本。',
 'BTC/ETH原值75%/25%表示2000USDT初始独立1500/500分仓，现金/持币跨折连续，无自动归一化、维持权重、转账或再平衡。组合=sum真实本金下BTC和ETH绝对NAV，初始2000；没有二次乘75/25，未平均组件收益/Sharpe/DD或缩放其他资金规模下的冲击。全部参数、资金与组件指纹在具体spec。','',
 '## 三项验证','',
 'Walk-forward完成：2025/2026分别03-18UTC00:01至09-14UTC00:01，连续180日/6×30日诊断折，180日滚动train、3日gap、purge0（无未来标签）。固定规则仅用当时已完成数据，无拟合或OOS调参；跨折不重置现金/单位/desired。每场259382个分钟/执行NAV点核算整体DD、逐折净收益/风险、日Sharpe365、Calmar、前五/末折，折收益乘积核对连续净值。两段历史反复开发，已有结果启发规则，不是未触碰最终测试集、独立前向验证或新的跨年复利结果。',
 'Sensitivity完成：BTC、ETH、组合×两个年份的6个3×3面全保留；162行CSV与报告列出三档成本收益/DD/Sharpe/Calmar、正收益/正Sharpe比例、相邻12边的2sd差异描述。2026 ETH正收益及正Sharpe6/9，其余5面9/9；资格区域另报。2026组合仅4条不同NAV、3个通过配置共1条路径，重复实现不算独立证据。2sd旗标为描述，不是显著性或最优参数证明。',
 'Costs完成：每边手续费10bp、halfspread1bp、滑点2bp；冲击0.5×滞后20完整日sample log sigma×sqrt(交易预算/quoteADV)，参与率≤0.1%。四项同时1/2/3倍，tick损失单列，终止平仓收费。全36组件重算实际资金规模下成本；570笔模拟成交独立核对，非实盘。现货无杠杆多头，资金费/借币不适用，USDT/现金收益假设0。PRICE/LOT/NOTIONAL及前5闭合分钟VWAP代理约束保留。Oct1静态交易所元数据应用于历史为假设，无历史L2、队列、IOC可成交、部分成交、延迟及TCA/容量校准。',
 '固定门槛：各成本净正，1x≥4/6正折，3x整体分钟DD≤25%，本面3x正比例≥60%，1x≥2往返，参考价毛PnL/成本≥2.5，无负余额，终止flat。24项均缺正折资格，其中3项还同时负收益和毛PnL/成本不足，全部保留。组合往返为两组件之和，不表示每币/每折盈利。','',
 '## 全部54个新配置','',
 '|年份|配置|通道入场日|EMA日|1x收益%|2x%|3x%|3x分钟DD%|1x正折|1x往返|资格/原因|',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
for c in cfg.values():
 z=c['scenes'];lines.append(f"|{c['year']}|{c.get('asset','组合75/25')}|{c['entry_days']}|{c['span_days']}|{z['1']['net_return_pct']:.5f}|{z['2']['net_return_pct']:.5f}|{z['3']['net_return_pct']:.5f}|{z['3']['max_drawdown_pct']:.5f}|{c['positive_folds_1x']}/6|{z['1']['round_trips']}|{c['status']}: {', '.join(c['failed_criteria'])}|")
lines+=['','## 敏感性区域与路径数','', '|年份/资产|通过/9|不同3x NAV/9|3x收益范围%|描述cliff/12|','|---|---:|---:|---|---:|']
for group,v in r['sensitivity'].items():
 cells=[c for c in cfg.values() if c['year']+'_'+c.get('asset','combination')==group];a,b=v['metrics']['3']['return_range_pct'];lines.append(f"|{group}|{sum(c['status']=='passed' for c in cells)}|{len({c['scenes']['3']['NAV_sha256_f64le'] for c in cells})}|{a:.5f}至{b:.5f}|{sum(e['cliff_flag_2sd'] for e in v['adjacent_edges'])}|")
lines+=['','## 全部54配置逐折三倍收益与集中度','', '|年份|资产|通道入场/EMA日|六折收益%|前五折累计%|末折%|','|---|---|---|---|---:|---:|']
for c in cfg.values():
 z=c['scenes']['3'];foldtext=', '.join(format(x['net_return_pct'],'.4f') for x in z['folds']);lines.append(f"|{c['year']}|{c.get('asset','组合75/25')}|{c['entry_days']}/{c['span_days']}|{foldtext}|{z['first_five_fold_return_pct']:.5f}|{z['last_fold_return_pct']:.5f}|")
lines+=['','## 原样读取旧比较','', '|年份|旧比较|三倍净收益%|整体分钟DD%|原资格|','|---|---|---:|---:|---|']
for n,c in r['read_only_comparators'].items():lines.append(f"|{c['year']}|{n}|{c['scenes']['3']['net_return_pct']:.5f}|{c['scenes']['3']['max_drawdown_pct']:.5f}|{c['status']}|")
lines+=['','旧持有组合为50/50，研究为75/25，持币/现金敞口不同，不称同风险alpha。','',
 '## 原冻结方案累计1419分钟','',
 '原113625/forward_plan.json哈希2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81保持；原SMA65±1%、浮点数量和原成本模型保持，未被本轮新规则替换。读取215033源report/state，21:40原现金/持币延续至23:40UTC，旧1301个NAV点精确保留；追加120闭合分钟后1421点（初始+参考执行+1419闭合mark）。0新成交，原费用/交易记录保持，无重复首买或本轮强制平仓。',
 '按[Binance官方行情接口](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)取得每币121条1m；21:39重叠bar全字段匹配旧末bar，新120条连续且closeTime+1≤23:40。保存原HTTP字节gzip/SHA、URL、毫秒单位、status200、取得UTC及延迟标记；取得晚于截止，为延迟shadow重建，无实时执行证明。','',
 '|观测|成本|累计净收益%|累计mark DD%|本段收益%|本段新成交|','|---|---|---:|---:|---:|---:|']
for n,c in f['configs'].items():
 for k,z in c['scenes'].items():lines.append(f"|{n}|{k}x|{z['net_return_pct']:.5f}|{z['max_drawdown_pct']:.5f}|{z['since_previous_mark_return_pct']:.5f}|{z['new_executions']}|")
z=f['configs']['forward_snapshot_combo']['scenes']['3']
lines+=['',
 f"累计23小时39分、0完整日，BTC/ETH及组合各成本仍负。组合三倍{z['net_return_pct']:.5f}%/整体DD{z['max_drawdown_pct']:.5f}%，新120分钟{z['since_previous_mark_return_pct']:.5f}%。3观测/9场景实际完成，partial以rejected留档仅因缺180日/六折；原长期计划collecting。未新增前向敏感性，不报短样本年化Sharpe/CAGR/Calmar，不以首笔模拟买入当实盘执行/容量稳健证据。",
 '下一轮读取本轮forward_state.json，从23:40现金/持币/desired/累计费用继续。跨Oct3UTC00:01必须执行原冻结日决策、读取当时可用完整前日及滞后20日成本数据，并检查新的执行参考和真实闭合分钟；当前仅追加mark脚本不能直接越过该决策。2027-03-31终止保持，新的截止先reserve，旧截止只读。','',
 '## 首次工程失败与修复留档','',
 '首次把1299+120误记为1429（应1419），使forward.py在NAV长度断言中止，尚未写报告；随后历史入口因缺forward_report在首配置之前中止，0历史场景计算。已保存failed_attempts/的原脚本/spec/错误日志、原回复与输入及SHA manifest，修正为1301+120=1421点、1419分钟。count_correction写明修复时间。策略规则/参数/门槛/截止和57个登记指纹保持，同一仍reserved配置恢复成功；没有伪造首次完成或另建重复配置。','',
 '## 独立审计、复现与提交','',
 '4份真实525600分钟parquet核对SHA、closed/可用时间/资产轴连续性；每日收盘、UTC00:01参考与OOS边界逐点核对。独立用pandas EWM与排序收盘区间重建19440条联合信号/持仓状态，另在36组件的3个时点进行108次当前/未来收盘扰动，过去及当时决策完全不变。这些是相同已登记策略的工程因果检查，不是新参数变体或额外收益回测。',
 '570笔Decimal模拟成交核对滞后ADV/sigma、预算/参与率、tick/LOT、现金/持币、五成本项；重建162场42019884个完整分钟/执行NAV，核对逐折/整体DD/Sharpe/Calmar、折收益乘积、费用、仓位/余额和门槛。9累计观察独立核对原前缀/仓位/费用、原HTTP字节及closed marks；162+9场景精确重放通过，无新HTTP/登记改动。',
 '57项finish绑定最终report/forward_report SHA，此前775记录/1570行完全保持。registry检查通过；保留verification.json、首次失败证据、全部具体spec、54压缩完整场景/信号/成交/持仓档案、中文报告/图表/162行CSV/data_manifest与必要代码。大行情/全NAV为忽略data/，不提交凭据。',
 '复现：`bash research/experiments/20261002T235103Z/reproduce.sh`。prepare.py为首次预约入口，已完成精确配置不再重复运行。实际push在运行简报核对远端ref、提交父/tree及本地stage/文件SHA后披露。',
 '本轮找到3组历史跨期资格通过的参数，但2026共用同一净值，收益仍集中且原模拟亏损，不得称稳定正收益。下一批可改变未测退出条件/参数或真实初始资金，继续冻结方案模拟；本轮精确配置以后只读复用。','']
(ROUND/'result.md').write_text('\n'.join(lines))
values=[c['scenes']['3']['net_return_pct'] for c in cfg.values()];norm=TwoSlopeNorm(vmin=min(values),vcenter=0,vmax=max(values));cmap=plt.get_cmap('RdYlGn');fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for iy,y in enumerate(('2025','2026')):
 for ix,asset in enumerate(('BTC','ETH','combination')):
  cells={(c['span_days'],c['entry_days']):c for c in cfg.values() if c['year']==y and c.get('asset','combination')==asset};a=np.array([[cells[(e,k)]['scenes']['3']['net_return_pct'] for k in grid['entry_lookback_days']] for e in grid['EMA_span_days']]);ax=axes[iy,ix];im=ax.imshow(a,norm=norm,cmap=cmap)
  for i,e in enumerate(grid['EMA_span_days']):
   for j,k in enumerate(grid['entry_lookback_days']):
    c=cells[(e,k)];rgb=cmap(norm(a[i,j]))[:3];lum=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2];label='P' if c['status']=='passed' else 'R';ax.text(j,i,f'{a[i,j]:.2f}%\n{label}',ha='center',va='center',color='white' if lum<.48 else 'black')
  ax.set(xticks=range(3),xticklabels=grid['entry_lookback_days'],yticks=range(3),yticklabels=grid['EMA_span_days'],xlabel='Channel entry (days); exit30',ylabel='EMA span (days); +/-1.5%',title=f'{y} {asset}')
fig.colorbar(im,ax=axes.ravel().tolist(),label='180-day return,3x costs (%)',shrink=.75);fig.suptitle('Joint channel AND EMA entry / either exit | P: historical pass; R: reject');fig.savefig(ROUND/'sensitivity.png',dpi=140);plt.close(fig)
print('Saved54 configuration/cost/fold tables,six surfaces,three losses and9 negative shadow scenes with first failure evidence')
