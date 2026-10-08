"""Chinese complete results and parameter surfaces from immutable actual reports."""
import hashlib,json,math
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
T=Path(__file__).resolve().parent;R=T.parents[2]
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());s=r['summary'];grid=r['plan']['grid'];recovery=json.loads((T/'cache_recovery.json').read_text())
label=lambda c:('BTC收盘通道20/'+str(c['CHANNEL_exit_days'])+'；ETH EMA'+str(c['EMA_span_days'])+'±1.5%' if c['direction']=='BTC_CHANNEL_ETH_EMA' else 'BTC EMA'+str(c['EMA_span_days'])+'±1.5%；ETH收盘通道20/'+str(c['CHANNEL_exit_days']))
lookup={(c['year'],c['direction'],c['EMA_span_days'],c['CHANNEL_exit_days']):c for c in r['configs'].values()}
comparison=[]
for n,c in r['configs'].items():
 if not c['is_new']:continue
 anchor=lookup[c['year'],c['direction'],c['EMA_span_days'],30];a,b=c['scenes']['3'],anchor['scenes']['3']
 comparison.append({'name':n,'year':c['year'],'anchor_name':anchor['name'],'exit_days':c['CHANNEL_exit_days'],'return_difference_3x_pct_points':a['net_return_pct']-b['net_return_pct'],'DD_difference_3x_pct_points':a['max_drawdown_pct']-b['max_drawdown_pct'],'lower_return_and_higher_DD3':a['net_return_pct']<b['net_return_pct'] and a['max_drawdown_pct']>b['max_drawdown_pct']})
selection={'report_sha256':hashlib.sha256((T/'report.json').read_bytes()).hexdigest(),'comparisons':comparison,'2026_lower_return_higher_DD3_count':sum(x['year']=='2026' and x['lower_return_and_higher_DD3'] for x in comparison),'interpretation':'Historical gates passed does not imply relative improvement or stable live profit;retain all actual results. No replacement of any frozen paper account.'}
(T/'comparison.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
lines=[f'# BTC/ETH通道退出窗口与递推EMA组合：{T.name}','',f"24个新组合/72个成本场景，1x净正{s['positive_1x']}、3x净正{s['positive_3x']}；{len(s['passed'])}历史门槛通过、{len(s['rejected'])}淘汰，新增跨两段历史分别通过的参数{len(s['new_both_periods_passed_combination_pairs'])}组。12个旧30日退出组合/36场景及24个同规模组件/72场景只读复用，没有重跑旧组件信号与交易。",'', '## 冻结假设、指标和权重','', '上一轮通道20日入场配更快退出10/20日、另一币种SMA65没有新增跨期合格配置。本轮预设通道20日入场、退出10/20/30日×EMA50/65/80日、对称带宽1.5%，测试BTC通道/ETH EMA及反方向的完整3×3邻域。中心退出20日、EMA65，30日退出为已有只读锚；检验不同均线时序能否改善早期折与跨期一致性。没有看结果后改参数或失败判据。','', '日决策i只使用完成的C[i-1]；通道最高/最低来自C[i-L-1:i-1]，止于i-2并排除被比较收盘。EMA以alpha=2/(span+1)、样本首个真实日收盘为种子、adjust=False方式逐日Python float递推；比较C[i-1]与EMA[i-1]×(1±1.5%)，等号和未越界保留desired。成交与余额为Decimal28，UTC00:01真实分钟open为回测参考；OOS起点空仓，跨折不重置，末端计成本平仓。完整源spec、组件指纹和哈希保存。','', 'BTC/ETH原权重75%/25%表示2000USDT初始1500/500独立分仓，不自动归一化、维持比例、转账或再平衡。组件使用恰好1500/500的真实预算与取整成本；组合直接相加同时间轴成本后绝对NAV一次，不再乘权重、不平均收益或Sharpe。','', '读取完整4697行登记、2299规范定义/2301保留ID、57轮全文结论，初始16项均有实际证据。27个新历史/观察定义均reserve成功后才计算；既有纸盘blocked窗口仍保持可恢复说明，不当缺历史策略补测。', '', '## 三项验证与固定失败判据','', 'Walk-forward完成：2025与2026分别UTC03-18 00:01至09-14 00:01，各连续180天、6×30日折，180日滚动历史/3日gap/purge0。固定规则无拟合或标签、无OOS选择。每场259382个分钟/执行净值点计算逐折与整体回撤；两年独立账本，不拼成跨年复利。两段均反复研究，只是复用开发验证历史，不能称未触碰最终测试集。','', 'Sensitivity完成：两年×两个方向的4个完整3×3面，同时变化通道退出周期与EMA跨度。全部格点、1/2/3成本收益、分钟/日回撤、Sharpe365、Calmar、逐折、12条邻接边及描述性2sd cliff保留。参数不同但NAV相同的情况单独披露，不视为独立证据。','', 'Costs完成：手续费10bp/侧、估计半价差1bp、滑点2bp及0.5×前20日样本sigma×sqrt(实际预算/前20日quoteADV)冲击，四项均乘1/2/3；最高参与率0.001。Decimal28、PRICE/LOT、最低名义额、Oct1静态过滤、前5个闭合分钟VWAP百分价格代理及立即全额LIMIT IOC假设保持，残余现金保留。现货多头无杠杆，资金费/借币不适用；缺历史真实盘口/TCA校准，未证明真实成交容量。','', '八项门槛保持：所有成本正收益、1x至少4/6正折、3x完整分钟回撤≤25%、邻域3x净正≥60%、至少2个组件往返、1x毛参考PnL/执行成本≥2.5、无负余额、末端空仓。旧30日组合按原criteria/status只读，扩展网格不改旧登记。','', '## 与30日退出锚比较','', f"新组合{len(s['passed'])}个单年度通过、{len(s['rejected'])}个淘汰，失败原因为正收益折不足；新增跨两段历史均通过的参数{len(s['new_both_periods_passed_combination_pairs'])}组。2026年BTC通道20/10＋ETH EMA65的三倍前五折累计改善至+3.939924%、整体回撤9.848983%，但仍只有3/6正收益折，按原门槛淘汰。反方向EMA50/80的2026新配置通过，2025对应配置未通过；20日退出在2026部分NAV与30日锚相同，不能当独立样本。本轮没有跨期合格改进，不替换10组冻结模拟盘。",'', '## 2026年组合按三倍成本收益倒序（180天累计，非年化）','', '|技术指标/参数|新配置|BTC/ETH原权重|1x收益%|2x收益%|3x收益%|3x整体回撤%|1x正折|3x前五折累计%|2025年3x收益%|跨两段门槛|','|---|---|---|---|---|---|---|---|---|---|---|']
for n,c in sorted(r['configs'].items(),key=lambda z:-z[1]['scenes']['3']['net_return_pct']):
 if c['year']!='2026':continue
 a=c['scenes'];other=r['configs'][c['other_period_config']]
 lines.append(f"|{label(c)}|{c['is_new']}|75%/25%|{a['1']['net_return_pct']:.6f}|{a['2']['net_return_pct']:.6f}|{a['3']['net_return_pct']:.6f}|{a['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['3']['first_five_fold_return_pct']:.6f}|{other['scenes']['3']['net_return_pct']:.6f}|{c['both_periods_meet_full_gates']}|")
lines+=['', '## 全部逐配置、成本与六折结果','', '|配置|新测|状态|成本倍数|净收益%|分钟整体回撤%|Sharpe365|Calmar|成本占初始%|六折净收益%|失败判据|','|---|---|---|---|---|---|---|---|---|---|---|']
for n,c in r['configs'].items():
 for k,a in c['scenes'].items():
  folds=','.join(f"{x['net_return_pct']:.5f}" for x in a['folds']);lines.append(f"|{n}|{c['is_new']}|{c['status']}|{k}|{a['net_return_pct']:.6f}|{a['max_drawdown_pct']:.6f}|{a['sharpe_365']:.6f}|{a['calmar']:.6f}|{a['cost_pct_initial']:.6f}|{folds}|{','.join(c['failed_criteria'])}|")
lines+=['', '## 全历史路径比较与选择偏差','', f"核对全部{len(h['all_prior_report_sha256'])}份旧report及SHA；72个新场景中{h['new_scenes_already_in_any_prior_report']}条完整NAV此前出现，{h['new_scenes_not_in_any_prior_report']}条未见。2026新组合3x共{h['new_2026_combo_3x_paths_not_in_any_prior_report']}条未见路径，合格跨年全成本配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见。新参数/组合及金额哈希不等于独立市场样本，多重研究选择偏差仍存在。",'', '只读现金0收益、同期持有、SMA65、原通道和EMA中心比较保存在report；不同敞口/风险，不能把持有差额直接当alpha。','', '## 原SMA账户延迟shadow连续估值','', '原账户从UTC Oct7 22:50延续至Oct8 00:50，8576旧NAV点完整保留，追加120闭合分钟及1个日决策参考点至8697点；累计8689分钟、6完整日。本轮按原SMA65±1%处理Oct8 UTC00:01：BTC/ETH均hold_long，6个资产/成本状态独立核对，零新成交、零新费用、无强平或重置；下一决策UTC Oct9 00:01，2027Mar31终点与冻结规则保持。','', '|原账户|成本倍数|累计收益%|分钟整体回撤%|','|---|---|---|---|']
for name,c in f['configs'].items():
 for k,a in c['scenes'].items():lines.append(f"|{name}|{k}|{a['net_return_pct']:.6f}|{a['max_drawdown_pct']:.6f}|")
lines+=['', '这是原SMA账户依据实际分钟行情的延迟shadow重建，不计入用户P01–P10真实观察报价模拟盘。paper10 plan/state哈希与本轮开始一致，没有重置或更换任何账户。3个partial观测rejected仅表示未成熟，原计划继续。','', '## 检查、恢复缓存和复现','', f"计算前从旧归档现金/数量与同SHA真实分钟行情重建{len(recovery['missing_cache_files_restored'])}个缺失的只读缓存，共核对108个只读成本场景，所有完整NAV哈希吻合；没有重跑旧信号或交易。独立审计重建72个来源成本场景、108个组合成本场景/28013256个分钟NAV点，检查资金恒等式、全部费用、折复利与整体回撤；9个原账户估值场景检查真实HTTP200原始数据、每币65条已闭合日线/64条重叠、6项日决策、1个日参考点、旧前缀与账户连续性。原SMA是冻结浮点数量模型，未追改交易所取整；它与P01–P10的Decimal真实报价前向账本分开。",'', '全部27个新定义实际完成、独立审计通过后finish；完整新旧结果、负收益折、原账户亏损及零交易留档。大行情和完整NAV仅留忽略data缓存，Git保留spec、report、压缩成交、输入来源/哈希、CSV、图与stdout。','', f'复现：`bash research/experiments/{T.name}/reproduce.sh`；仅同SHA缓存与实际已保存输入，不HTTP、改登记或新增历史订单。','', '继续寻找改善折间一致性的独立规则；本轮不替换10组冻结前向账户。历史门槛通过不能称稳定实盘盈利。']
(T/'result.md').write_text('\n'.join(lines)+'\n')
fig,axes=plt.subplots(2,2,figsize=(12,8),constrained_layout=True)
for ax,(y,direction) in zip(axes.flat,[(y,d) for y in ('2025','2026') for d in grid['directions']]):
 vals=np.array([[lookup[y,direction,e,x]['scenes']['3']['net_return_pct'] for x in grid['CHANNEL_exit_days']] for e in grid['EMA_span_days']]);im=ax.imshow(vals,cmap='YlGnBu',aspect='auto')
 ax.set_xticks(range(3),grid['CHANNEL_exit_days']);ax.set_yticks(range(3),[str(e) for e in grid['EMA_span_days']]);ax.set_xlabel('Channel exit lookback (days); entry20 fixed');ax.set_ylabel('EMA span (days); symmetric1.5% fixed');ax.set_title(y+' '+direction.replace('_',' ')+'\n3x cost net return,180days; P/R=passed/rejected')
 for i in range(3):
  for j in range(3):ax.text(j,i,f"{vals[i,j]:.2f}%\n{'P' if lookup[y,direction,grid['EMA_span_days'][i],grid['CHANNEL_exit_days'][j]]['status']=='passed' else 'R'}",ha='center',va='center',color='white' if vals[i,j]>np.mean(vals) else 'black')
 fig.colorbar(im,ax=ax,label='Net return (%)')
fig.savefig(T/'sensitivity.png',dpi=150);plt.close(fig)
print(json.dumps({'new_configs':24,'passed':len(s['passed']),'matched_2026_dominated':selection['2026_lower_return_higher_DD3_count'],'full_scene_rows':sum(len(c['scenes']) for c in r['configs'].values()),'new_cross_period_qualified':len(s['new_both_periods_passed_combination_pairs'])}))
