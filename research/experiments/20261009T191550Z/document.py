"""Describe already-finished volume-confirmation results,including every rejected/zero/negative fold."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));cs=r['configs'];grid=r['plan']['grid'];fresh=[c for c in cs.values()if c['is_new']];portfolios=[c for c in cs.values()if c['role']=='combination'];leaves=[c for c in cs.values()if c['role']=='component'and c.get('asset')=='ETH'];comparisons=[]
for c in portfolios:
 name,o=next((n,z)for n,z in r['read_only_comparators'].items()if z['kind']=='MATCHED_UNFILTERED_ETH'and z['year']==c['year'])
 comparisons.append({'config':c['name'],'year':c['year'],'comparator':name,'same_initial_funding':[1500,500],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in ('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in ('1','2','3'))})
pairs=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 rows=[next(x for x in comparisons if x['config']==n)for n in pair];ret=[v for row in rows for v in row['return_differences_pp'].values()];dd=[row['minute_DD3_difference_pp']for row in rows];seen=next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)
 pairs.append({'pair':pair,'all_returns_nonworse_both_years':all(v>=0 for v in ret),'DD3_nonworse_both_years':all(v<=0 for v in dd),'joint_improvement_both_years':all(v>=0 for v in ret)and all(v<=0 for v in dd)and(any(v>0 for v in ret)or any(v<0 for v in dd)),'strict_return_gain_in_both_years':all(any(v>0 for v in row['return_differences_pp'].values())for row in rows),'whole_pair_path_seen_before':seen})
exposure={};signatures={}
for c in cs.values():
 arc=json.loads(gzip.decompress((R/c['archive']).read_bytes()));sig=tuple(c['scenes'][k]['NAV_sha256_f64le']for k in ('1','2','3'));group=c['asset']if c['role']=='component'else'combination';signatures.setdefault(c['year']+'_'+group,set()).add(sig)
 if c['role']=='component'and c.get('asset')=='ETH':
  z=arc['scenes']['1'];d=z['decisions'];exposure[c['name']]={'year':c['year'],'volume_lookback_days':c['volume_lookback_days'],'minimum_volume_ratio':c['minimum_volume_ratio'],'archive_sha256':sha(R/c['archive']),'volume_eligible_days':sum(v['volume_eligible']for v in d),'price_breakout_days':sum(v['price_breakout']for v in d),'blocked_breakout_days':sum(v['price_breakout']and not v['volume_eligible']for v in d),'desired_long_days':sum(v['long']for v in d),'invested_days':sum(st['end_day_exclusive']-st['day_offset']for st in z['position_segments']if float(st['units'])>0),'entry_events':sum(v['action']=='entry'for v in d),'executions1':z['summary']['executions'],'round_trips1':z['summary']['round_trips']}
surfaces={}
for year in ('2025','2026'):
 for group in ('ETH','combination'):
  cells=[c for c in cs.values()if c['year']==year and(c.get('asset')==group or c['role']==group)];sens=r['sensitivity'][year+'_'+group];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['volume_lookback_days'],c['minimum_volume_ratio']]for c in cells if c['scenes']['3']['net_return_pct']==best]
  surfaces[year+'_'+group]={'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':coords,'best_on_boundary':any(n in (15,25)or ratio in (.75,1)for n,ratio in coords),'scope':'Descriptive reused-history sensitivity;not significance,DSR/PBO or untouched final test.'}
comparison={'report_sha256':sha(T/'report.json'),'matched_comparisons':comparisons,'qualified_pairs_vs_matched_controls':pairs,'new_both_periods_qualified':len(pairs),'new_qualified_pairs_jointly_nonworse_with_improvement':sum(x['joint_improvement_both_years']for x in pairs),'new_qualified_pairs_strict_return_gain_in_both_years':sum(x['strict_return_gain_in_both_years']for x in pairs),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'path_signature_counts':{k:len(v)for k,v in signatures.items()},'ETH_signal_exposure':exposure,'surface_diagnostics':surfaces,'interpretation':'Compare new ETHactivity confirmation against identicalBTCvolume30/r1 and same raw75/25 funding. Reused histories and duplicate paths are not independent final evidence;no new comparator backtest.'}
anchor_comparisons=[]
focus_configs={c['year']:c for c in portfolios if(c['volume_lookback_days'],c['minimum_volume_ratio'])==(20,.875)}
for year,c in focus_configs.items():
 old=next(v for v in portfolios if v['year']==year and(v['volume_lookback_days'],v['minimum_volume_ratio'])==(20,1))
 anchor_comparisons.append({'year':year,'focus':c['name'],'old_anchor':old['name'],'old_anchor_source_report':old['source_ref']['report'],'old_anchor_source_report_sha256':old['source_ref']['report_sha256'],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-old['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==old['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
focus_signature=tuple(focus_configs[year]['scenes'][k]['NAV_sha256_f64le']for year in('2025','2026')for k in('1','2','3'))
equivalent_new_parameters=sorted({(c['volume_lookback_days'],c['minimum_volume_ratio'])for c in portfolios if c['year']=='2025'and c['is_new'] and tuple(cs[n]['scenes'][k]['NAV_sha256_f64le']for n in(c['name'],c['other_period_config'])for k in('1','2','3'))==focus_signature})
comparison['predeclared_focus_vs_old20_r1']=anchor_comparisons
comparison['new_parameters_sharing_predeclared_focus_paired_path']=[list(x)for x in equivalent_new_parameters]
comparison['anchor_repair_scope']='2025wholecost paths unchanged from oldETH20/r1;2026 restores existing unfilteredETH baseline. All individual scene paths were already seen;new paired path is development evidence,not independent market data or minute-risk/live-profit proof.'
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with (T/'folds.csv').open('w',newline='')as fh:
 w=csv.writer(fh,lineterminator='\n');w.writerow(['config','year','role','is_new','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['volume_lookback_days'],c['minimum_volume_ratio']):c for c in portfolios if c['year']==year}
 for i,(metric,title)in enumerate([('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute sampled NAV DD %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[n,ratio]['scenes']['3'][metric]for ratio in grid['minimum_volume_ratio']]for n in grid['volume_lookback_days']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a,n in enumerate(grid['volume_lookback_days']):
   for b,ratio in enumerate(grid['minimum_volume_ratio']):ax.text(b,a,f'{matrix[a,b]:.3f}'+(' P'if cells[n,ratio]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=[f'{x:g}'for x in grid['minimum_volume_ratio']],yticks=range(3),yticklabels=grid['volume_lookback_days'],xlabel='Minimum prior-day quote-volume / prior-N-day mean',ylabel='Preceding quote-volume mean days (tested day excluded)',title=year+' | '+title);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
fig.suptitle('ETH close-channel15/30 + quote-turnover entry confirmation / fixed BTC volume30-ratio1\nRaw75/25:1500/500USDT | P/R=annual gates | both180-day histories reused',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['volume_lookback_days'],c['minimum_volume_ratio']):c for c in leaves if c['year']==year}
 for i,(metric,title)in enumerate([('net_return_pct','3x net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[n,q]['scenes']['3'][metric]for q in grid['minimum_volume_ratio']]for n in grid['volume_lookback_days']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a,n in enumerate(grid['volume_lookback_days']):
   for b,q in enumerate(grid['minimum_volume_ratio']):ax.text(b,a,f'{matrix[a,b]:.3f}'+(' P'if cells[n,q]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=[f'{q:g}'for q in grid['minimum_volume_ratio']],yticks=range(3),yticklabels=grid['volume_lookback_days'],xlabel='Prior-day USDT turnover / preceding N-day mean',ylabel='ETH quote-volume mean days',title=year+' | '+title);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
fig.suptitle('ETH close-channel15/30 + quote-turnover confirmation | initial500USDT\nP/R=annual gates | completed prior bars only | both histories reused',fontsize=14);fig.savefig(T/'sensitivity_ETH.png',dpi=130);plt.close(fig)
focus=[c for c in portfolios if(c['volume_lookback_days'],c['minimum_volume_ratio'])==(20,.875)]
ps=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/ps['last_observation_id']/'summary.json').read_text());summary=r['summary']
lines=['# ETH成交额确认中间阈值：15/20/25日 × 0.75/0.875/1','',f"14个新ETH组件＋14个新年度组合，28个历史配置/84成本场景实际执行，1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}；{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(pairs)}组新组合参数跨两期合格。旧ETH20/r0.75、20/r1及对应组合共8个年度配置，另2BTC固定组件均只读；30旧成本场景核对而不重跑旧信号或成交。31新定义含3原shadow截止全部reserve/finish。",'',
 '## 事前假设和精确规则','',
 '上一轮ETH20/r1提高2025收益，却使2026收益/回撤变差；ETH20/r0.75与原对照同曲线。本轮在新结果之前冻结ETH均额N15/20/25与阈值0.75/0.875/1，关注和中心都是20/r0.875。希望中间阈值保留2025过滤作用并减少2026入场延误，也可能完全重复旧路径或仍有取舍。BTC固定既有15/30通道＋成交额N30/r1；原75/25、1500/500USDT保持。选择邻域依据已研究历史提出，当前仍是复用历史，不是新的独立留出。','',
 '决策i只用已闭合UTC前日C[i−1]与USDT成交额Q[i−1]。C[i−1]严格大于max(C[i−16:i−1])且Q[i−1]≥r×mean(Q[i−N−1:i−1])、均额>0才置desired-long；C[i−1]严格小于min(C[i−31:i−1])无成交额条件置现金。参考范围止于i−2并排除被比较日；成交额阈值相等合格，价格相等/死区延续状态，低成交额本身不退出，均额零禁入。BTC N/r固定30/1，ETH按3×3网格。无EMA/SMA/ATR、arming、止损或空头。','',
 'Q为1440条真实UTC分钟quote_volume精确Decimal和，不是币数量；均额/比率Decimal28，1460个双币/双年日聚合独立核对。ETH新组件500USDT，旧BTC1500USDT；组合2000USDT原75/25为独立初始分仓，同时间轴已扣成本绝对NAV只相加一次，不缩放、二次加权、归一化、跨币转账、维持比例或再平衡。OOS183起始现金/desired-cash，历史只暖机，六折状态连续。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范配置、{len(prior['conclusions'])}轮全文结论、7个Freqtrade文件、4个OOS源码和3技能。初始16按原始前16行与别名核对均有实际证据。此前2470历史配置，本轮28新增后2498；观察截止不计挖掘策略。精确旧8格点直接读取原spec/报告/归档，未重新reserve或改写原criteria/status；新邻域统计用于新配置，旧通过/淘汰仅沿用原批次结论。",'',
 '## 三项验证与失败判据','',
 'Walk-forward实际完成：2025及2026各03-18UTC00:01→09-14UTC00:01，每段180天、6个连续30天折；180日滚动历史/3日gap/purge0，无模型、标签、逐折/OOS拟合。前日闭合信号之后用下一00:01真实历史分钟开盘估计虚拟成交，终止含成本平仓；完整连续259382点分钟收盘/执行节点NAV算整体回撤，不平均折回撤。两年本金独立；已有反复研究历史不是未触碰最终留出。','',
 'Sensitivity实际完成：两参数联合变化，ETH和组合每年完整9格。114行sensitivity.csv涵盖84新及30只读旧成本场景，保留净收益、整体/日回撤、Sharpe365、Calmar、成本和往返；684折（504新、180旧）含负收益/零收益。两份热图及12条相邻边保留；旧状态原样展示，描述性2sd差异不是显著性、PBO/DSR或独立优化证据。','',
 'Costs实际完成：每侧10bp手续费、1bp估计半点差、2bp滑点，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(订单预算/滞后20日quote ADV)冲击，四项同时×1/2/3，参与率≤0.001。Decimal28现金/数量、PRICE不利tick、LOT下取整、NOTIONAL和前5完整分钟VWAP百分价格代理独立核对。Oct1静态规则用于旧历史为假设；无历史L2/TCA、队列/部分成交、延迟或真实IOC接单/容量保证。只做多现货，资金费/借币不适用。','',
 '八门槛不变：全成本净正、1x≥4/6严格正折、3x整体分钟/执行节点DD≤25%、3x邻域净正≥60%、1x≥2往返、1x毛参考盈亏/成本≥2.5、无负现金/币数量、终止空仓。组件和组合独立判断，旧格点criteria保留原值，不能用新网格统计重写旧淘汰为通过。','',
 f"新配置失败条件计数{comparison['failure_counts']}。独立审计84新场景/21,788,088NAV点/7560因果日决策及{summary['new_component_fills']}新ETH历史虚拟成交；18旧组件场景从归档现金/数量重建、12旧组合场景按1500/500源NAV相加核对。7阶段完整离线重放逐进程退出留档；合成时序夹具不是业绩。",'',
 '## 预定ETH20/r0.875与匹配旧对照','']
for c in focus:
 d=next(x for x in comparisons if x['config']==c['name']);z=c['scenes']['3'];lines.append(f"{c['year']}：1/2/3x收益{c['scenes']['1']['net_return_pct']:.6f}%/{c['scenes']['2']['net_return_pct']:.6f}%/{z['net_return_pct']:.6f}%，3x整体分钟DD{z['max_drawdown_pct']:.6f}%；对照3x收益差{d['return_differences_pp']['3']:.6f}个百分点、DD差{d['minute_DD3_difference_pp']:.6f}个百分点，完整全成本NAV相同={d['all_cost_NAV_identical']}。")
lines+=['','与旧ETH20/r1相比，预定20/r0.875在2025全部成本的完整NAV相同；2026三倍收益恢复0.476864个百分点、整体分钟回撤降低0.292439个百分点，回到原ETH纯通道对照曲线。当前新参数'+str(comparison['new_parameters_sharing_predeclared_focus_paired_path'])+'共享这个跨期全成本路径，不能计为多个独立成功。','相对更早的ETH纯通道对照，2025三倍收益增加7.813528个百分点，同时整体分钟回撤增加0.249851个百分点；2026完全同路径。因此是提高2025回报、保留2026表现的历史候选，仍有首期风险取舍，并非在两年所有指标都更强。84个新场景的单期完整路径均此前已见，只形成1种未见跨期配对；复用历史、多重选择及未独立前向的限制保持。']
lines+=['',f"合格参数中，两期全成本收益和3x回撤均不更差且有改善者{comparison['new_qualified_pairs_jointly_nonworse_with_improvement']}组；严格两年收益都提高者{comparison['new_qualified_pairs_strict_return_gain_in_both_years']}组。逐项18条匹配比较保存在comparison.json。现金0与旧持有/SMA仅作历史背景，不把其他分配当严格匹配控制，不在当前样本选优后称独立验证。",'',
 '## 完整9格组合按各年1x收益倒序','',
 '各组合技术指标均为BTC固定15/30通道＋N30/r1成交额，ETH15/30通道＋表中N/r，原始75/25、2000USDT。','',
 '|年份|新/旧|ETH N/r|1x%|2x%|3x%|3x整体分钟DD%|正折1|成交/往返1|成本1USDT（手续费/冲击）|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(portfolios,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes']['1'];p=z['cost_parts_usdt'];lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['volume_lookback_days']}/{c['minimum_volume_ratio']:g}|{z['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{z['executions']}/{z['round_trips']}|{z['cost_usdt']:.6f}（{p['fee']:.6f}/{p['impact']:.6f}）|{c['status']}|")
lines+=['','## 完整9格ETH组件按各年1x收益倒序','','每行真实执行的独立500USDT组件；不把组合门槛通过改写为组件通过。','', '|年份|新/旧|ETH N/r|1x%|2x%|3x%|3x整体分钟DD%|正折1|成交/往返1|活动合格日/180|被挡突破日|持仓日|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---|']
for c in sorted(leaves,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes']['1'];e=exposure[c['name']];lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['volume_lookback_days']}/{c['minimum_volume_ratio']:g}|{z['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{z['executions']}/{z['round_trips']}|{e['volume_eligible_days']}|{e['blocked_breakout_days']}|{e['invested_days']}|{c['status']}|")
lines+=['','## 敏感性、重复路径与证据范围','', '|年份/对象|3x净正比例|门槛通过率|描述性陡峭边/12|3x最高收益N/r|边界点|','|---|---:|---:|---:|---|---|']
for name,v in surfaces.items():lines.append(f"|{name}|{100*v['positive3_fraction']:.3f}%|{100*v['full_gate_pass_fraction']:.3f}%|{v['descriptive_cliff_flags']}|{v['best_return3_coordinates']}|{v['best_on_boundary']}|")
lines+=['',f"84新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，去重后{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径。新2026组合3x未见路径{h['new_2026_combo_3x_paths_not_in_any_prior_report']}种；{len(pairs)}组双期合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种此前未见的跨期配对。路径签名数{comparison['path_signature_counts']}；参数新颖、路径新颖均不是新的独立市场样本。全部来源JSON包括旧补充组件报告按登记实际结果指针查找，旧结果、失败/负折永久保留。",'',
 '4份525600行真实分钟parquet、两份双币日聚合、规则快照、源报告/归档/代码/规范参数与SHA见spec.json、report.json、data_manifest.json。大行情和完整NPY留忽略data目录；轻量订单/分段持仓、逐折、统计与哈希入Git，完整分钟回撤可从相同输入重建。采样风险不是tick内最大风险。','',
 '## 两类模拟保持连续','']
shadow=f"原SMA65/1%延迟shadow仅17:00→19:00追加120个已闭合分钟mark，旧{r['plan']['forward_resume']['prior_NAV_points']}点完整前缀不变，新{r['plan']['forward_resume']['total_NAV_points']}点/{r['plan']['forward_resume']['cumulative_minutes']}分钟、完整7天，0新日决策/参考/成交/费用，下次Oct10UTC00:01，3x累计{f['configs']['forward_snapshot_combo']['scenes']['3']['net_return_pct']:.6f}%。原计划SHA及2027-03-31结束保持；这是延迟历史分钟重建，不是十策略当时公开报价前向成交。"
lines+=[shadow,'',f"固定P01–P10保持第{paper['actual_quote_observations']}次真实报价观察（{paper['observed_at_utc']}），跨度{paper['elapsed_seconds']/3600:.6f}小时，主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。未运行paper执行器或修改冻结规则/本金/现金/币数量/desired/已处理日线/费用及交易；180天/6窗未成熟，回撤限于实际保存报价快照。网页只读汇总已有账本和报告，不重新部署或建重复任务。",'', '## 复现与后续','',f"`.venv/bin/python research/experiments/{T.name}/replay_verify.py`；7阶段信号夹具、旧缓存、新历史、原shadow、独立审计和登记检查，不HTTP、不写登记或paper账户。新配置31条全部先reserve后执行/抓取并finish；旧BTC只读从归档/同SHA数据恢复NAV，未重跑旧信号/订单。",'', '绝对历史门槛通过不等于稳定实盘盈利或独立最终验证。全部新参数、真实负折、失败和成本证据保留，当前不追加未预定网格、不替换固定模拟盘；后续新规则/时间区间须另行冻结登记。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原SMA冻结账户延迟分钟mark\n\n'+shadow+'\n')
print(json.dumps({'historical_configs':28,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'portfolio_pairs':len(pairs),'joint_nonworse_pairs':comparison['new_qualified_pairs_jointly_nonworse_with_improvement'],'strict_both_year_return_gain_pairs':comparison['new_qualified_pairs_strict_return_gain_in_both_years'],'path_signatures':comparison['path_signature_counts'],'surfaces':surfaces},ensure_ascii=False))
