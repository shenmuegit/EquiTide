"""Describe already-finished volume-confirmation results,including every rejected/zero/negative fold."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));cs=r['configs'];grid=r['plan']['grid'];fresh=[c for c in cs.values()if c['is_new']];portfolios=[c for c in fresh if c['role']=='combination'];leaves=[c for c in fresh if c['role']=='component'];comparisons=[]
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
 if c['is_new']and c['role']=='component':
  z=arc['scenes']['1'];d=z['decisions'];exposure[c['name']]={'year':c['year'],'volume_lookback_days':c['volume_lookback_days'],'minimum_volume_ratio':c['minimum_volume_ratio'],'archive_sha256':sha(R/c['archive']),'volume_eligible_days':sum(v['volume_eligible']for v in d),'price_breakout_days':sum(v['price_breakout']for v in d),'blocked_breakout_days':sum(v['price_breakout']and not v['volume_eligible']for v in d),'desired_long_days':sum(v['long']for v in d),'invested_days':sum(st['end_day_exclusive']-st['day_offset']for st in z['position_segments']if float(st['units'])>0),'entry_events':sum(v['action']=='entry'for v in d),'executions1':z['summary']['executions'],'round_trips1':z['summary']['round_trips']}
surfaces={}
for year in ('2025','2026'):
 for group in ('ETH','combination'):
  cells=[c for c in fresh if c['year']==year and(c.get('asset')==group or c['role']==group)];sens=r['sensitivity'][year+'_'+group];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['volume_lookback_days'],c['minimum_volume_ratio']]for c in cells if c['scenes']['3']['net_return_pct']==best]
  surfaces[year+'_'+group]={'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':coords,'best_on_boundary':any(n in (10,30)or ratio in (.75,1.25)for n,ratio in coords),'scope':'Descriptive reused-history sensitivity;not significance,DSR/PBO or untouched final test.'}
comparison={'report_sha256':sha(T/'report.json'),'matched_comparisons':comparisons,'qualified_pairs_vs_matched_controls':pairs,'new_both_periods_qualified':len(pairs),'new_qualified_pairs_jointly_nonworse_with_improvement':sum(x['joint_improvement_both_years']for x in pairs),'new_qualified_pairs_strict_return_gain_in_both_years':sum(x['strict_return_gain_in_both_years']for x in pairs),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'path_signature_counts':{k:len(v)for k,v in signatures.items()},'ETH_signal_exposure':exposure,'surface_diagnostics':surfaces,'interpretation':'Compare new ETHactivity confirmation against identicalBTCvolume30/r1 and same raw75/25 funding. Reused histories and duplicate paths are not independent final evidence;no new comparator backtest.'}
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
  ax.set(xticks=range(3),xticklabels=[f'{x:g}'for x in grid['minimum_volume_ratio']],yticks=range(3),yticklabels=grid['volume_lookback_days'],xlabel='Minimum prior-day quote-volume / prior-N-day mean',ylabel='Preceding quote-volume mean days (tested day excluded)',title=year+' | '+title);fig.colorbar(im,ax=ax,fraction=.035)
fig.suptitle('ETH close-channel15/30 + quote-turnover entry confirmation / fixed BTC volume30-ratio1\nRaw75/25:1500/500USDT | P/R=annual gates | both180-day histories reused',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['volume_lookback_days'],c['minimum_volume_ratio']):c for c in leaves if c['year']==year}
 for i,(metric,title)in enumerate([('net_return_pct','3x net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[n,q]['scenes']['3'][metric]for q in grid['minimum_volume_ratio']]for n in grid['volume_lookback_days']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a,n in enumerate(grid['volume_lookback_days']):
   for b,q in enumerate(grid['minimum_volume_ratio']):ax.text(b,a,f'{matrix[a,b]:.3f}'+(' P'if cells[n,q]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=[f'{q:g}'for q in grid['minimum_volume_ratio']],yticks=range(3),yticklabels=grid['volume_lookback_days'],xlabel='Prior-day USDT turnover / preceding N-day mean',ylabel='ETH quote-volume mean days',title=year+' | '+title);fig.colorbar(im,ax=ax,fraction=.035)
fig.suptitle('ETH close-channel15/30 + quote-turnover confirmation | initial500USDT\nP/R=annual gates | completed prior bars only | both histories reused',fontsize=14);fig.savefig(T/'sensitivity_ETH.png',dpi=130);plt.close(fig)
focus=[c for c in portfolios if(c['volume_lookback_days'],c['minimum_volume_ratio'])==(20,1)]
ps=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/ps['last_observation_id']/'summary.json').read_text());summary=r['summary']
lines=['# ETH成交额确认通道＋固定BTC既有成交额通道','',f"18个新ETH组件＋18个新年度组合，共36个历史配置/108成本场景真实执行；1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。新组合18个全部通过绝对门槛，{len(pairs)}组跨期参数合格。旧BTC N30/r1两份1500USDT组件/6场景只读，不重跑旧信号和成交。39个新定义含原shadow截止均reserve/finish，全部负折/零折与淘汰保留。",'',
 '## 事前假设、规则和资金','',
 'BTC成交额确认曾改善2025，但2026与旧BTC通道同路径；ETH的SMA/EMA混合降低了相对ETH通道的收益。本轮预定只研究ETH入场活动确认，完整N10/20/30日均额×最小倍率0.75/1/1.25，关注N20/r1。BTC固定既有15/30收盘通道＋N30/r1成交额确认。过滤ETH低活动突破可能减少错误入场，也可能错失大行情；同BTC、同ETH15/30通道及同1500/500资金的旧组合是预定匹配对照，不按当前结果追加参数。','',
 '两个资产决策i均仅用完整UTC前日收盘C[i−1]及USDT成交额Q[i−1]。严格C[i−1]>max(C[i−16:i−1])且Q[i−1]≥r×mean(Q[i−N−1:i−1])、均额>0才设desired-long；严格C[i−1]<min(C[i−31:i−1])则设现金，退出不受成交额限制。价格/成交额参考都止于i−2，排除被比较日；成交额阈值相等合格，价格等号/死区保持状态，低成交额本身不退出，均额零禁入。BTC N/r固定30/1；ETH按完整网格变化，无EMA/SMA/ATR、延迟挂起、止损或空头。','',
 'Q为真实1440个UTC分钟quote_volume精确Decimal和，非币数量；信号均额/比率用Decimal28，1460个双币/双年日聚合全部独立核对。定义沿用[Binance官方K线字段](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints)，当前规则为预定研究假设，不是已知alpha。成本滞后ADV与信号的N日均额分别计算。','',
 '每个ETH新组件以500USDT实际执行，BTC既有组件1500USDT；每组组合2000USDT，原始75/25只代表初始分仓。用同时间轴、同资金且已扣成本的绝对NAV相加一次，不缩放旧NAV、二次乘权重、归一化、转账、维持比例或再平衡。所有OOS183起始为现金/desired-cash，历史仅暖机，不造旧持仓，跨折状态连续。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范配置、{len(prior['conclusions'])}轮全文结论、7个Freqtrade文件、4个OOS源码及3技能。初始16按原始前16行与别名逐份核对实际证据，缺实际结果0。此前2434历史配置，本轮新增36后2470；持续观察截止不计为挖掘试验。全部新配置先成功reserve，再执行和finish；旧BTC/对照status、criteria与报告哈希保持。",'',
 '## 三项验证和失败判据','',
 'Walk-forward实际完成：2025与2026各03-18UTC00:01→09-14UTC00:01，分别180天、6个连续30天折。原180日滚动历史/3日gap/purge0；无模型、标签或逐折/OOS拟合。前日闭合信号后使用下一00:01真实历史分钟开盘估计虚拟执行，期末含成本平仓，完整259382点连续分钟收盘/执行节点NAV计算整体回撤，不平均折回撤。两年本金独立，已有反复研究历史不是未触碰最终留出。','',
 'Sensitivity实际完成：ETH N与倍率两轴同时变化，组件与组合各9格×两年。sensitivity.csv保留108新及6旧BTC场景的净收益/整体与日采样回撤/Sharpe365/Calmar/成本与往返，folds.csv保留684折（648新、36旧），负收益及零收益不删。组合与ETH组件热图分别留档；12条相邻边及描述性2sd差异不是显著性、PBO或DSR。','',
 'Costs实际完成：每侧10bp手续费、1bp估计半点差、2bp滑点，加0.5×前20个完整UTC日未年化样本log波动率×sqrt(订单预算/滞后20日quote ADV)冲击，四项同时×1/2/3；参与率≤0.001。Decimal28现金/数量、PRICE不利tick、LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理独立核对。Oct1静态规则用于旧历史为假设；无历史L2、真实TCA、队列/部分成交、延迟及真实IOC接单/容量保证；只做多现货，资金费/借币不适用。','',
 '八门槛保持：全成本净正、1x≥4/6严格正折、3x整体分钟/执行节点DD≤25%、3x邻域净正≥60%、1x≥2往返、1x毛参考盈亏/成本≥2.5、无负余额/币数量、终止空仓。ETH组件和组合按各自真实路径独立判断；组件淘汰不删除其结果，也不重启账户。','',
 f"失败条件计数{comparison['failure_counts']}。独立审计108场景、28,013,256个NAV点、9720次因果日决策及{summary['new_component_fills']}个新ETH配置内历史虚拟成交；旧BTC6场景从同SHA真实价格与归档持仓重建核验。合成时序夹具只作工程检查。7阶段完整离线重放另行保留逐进程退出码。",'',
 '## 事前N20/r1与匹配旧对照','']
for c in focus:
 d=next(x for x in comparisons if x['config']==c['name']);z=c['scenes']['3'];lines.append(f"{c['year']}：1/2/3x收益{c['scenes']['1']['net_return_pct']:.6f}%/{c['scenes']['2']['net_return_pct']:.6f}%/{z['net_return_pct']:.6f}%，3x整体分钟DD{z['max_drawdown_pct']:.6f}%；对照3x收益差{d['return_differences_pp']['3']:.6f}个百分点、DD差{d['minute_DD3_difference_pp']:.6f}个百分点，完整全成本NAV相同={d['all_cost_NAV_identical']}。")
lines+=['',f"合格参数中，两期全成本收益和3x回撤均不更差且有改善者{comparison['new_qualified_pairs_jointly_nonworse_with_improvement']}组；严格两年收益都提高者{comparison['new_qualified_pairs_strict_return_gain_in_both_years']}组。逐项18条匹配比较保存在comparison.json。现金0与旧持有/SMA仅作历史背景，不把其他分配当严格匹配控制，不在当前样本选优后称独立验证。",'',
 '## 组合按各年1x收益倒序','',
 '各组合技术指标均为BTC固定15/30通道＋N30/r1成交额，ETH15/30通道＋表中N/r，原始75/25、2000USDT。','',
 '|年份|ETH N/r|1x%|2x%|3x%|3x整体分钟DD%|正折1|成交/往返1|成本1USDT（手续费/冲击）|状态|','|---|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(portfolios,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes']['1'];p=z['cost_parts_usdt'];lines.append(f"|{c['year']}|{c['volume_lookback_days']}/{c['minimum_volume_ratio']:g}|{z['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{z['executions']}/{z['round_trips']}|{z['cost_usdt']:.6f}（{p['fee']:.6f}/{p['impact']:.6f}）|{c['status']}|")
lines+=['','## ETH组件按各年1x收益倒序','','每行真实执行的独立500USDT组件；不把组合门槛通过改写为组件通过。','', '|年份|ETH N/r|1x%|2x%|3x%|3x整体分钟DD%|正折1|成交/往返1|活动合格日/180|被挡突破日|持仓日|状态|','|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---|']
for c in sorted(leaves,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes']['1'];e=exposure[c['name']];lines.append(f"|{c['year']}|{c['volume_lookback_days']}/{c['minimum_volume_ratio']:g}|{z['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{z['executions']}/{z['round_trips']}|{e['volume_eligible_days']}|{e['blocked_breakout_days']}|{e['invested_days']}|{c['status']}|")
lines+=['','## 敏感性、重复路径与证据范围','', '|年份/对象|3x净正比例|门槛通过率|描述性陡峭边/12|3x最高收益N/r|边界点|','|---|---:|---:|---:|---|---|']
for name,v in surfaces.items():lines.append(f"|{name}|{100*v['positive3_fraction']:.3f}%|{100*v['full_gate_pass_fraction']:.3f}%|{v['descriptive_cliff_flags']}|{v['best_return3_coordinates']}|{v['best_on_boundary']}|")
lines+=['',f"108新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，去重后{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径。新2026组合3x未见路径{h['new_2026_combo_3x_paths_not_in_any_prior_report']}种；{len(pairs)}组双期合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种此前未见的跨期配对。路径签名数{comparison['path_signature_counts']}；参数新颖、路径新颖均不是新的独立市场样本。全部来源JSON包括旧补充组件报告按登记实际结果指针查找，旧结果、失败/负折永久保留。",'',
 '4份525600行真实分钟parquet、两份双币日聚合、规则快照、源报告/归档/代码/规范参数与SHA见spec.json、report.json、data_manifest.json。大行情和完整NPY留忽略data目录；轻量订单/分段持仓、逐折、统计与哈希入Git，完整分钟回撤可从相同输入重建。采样风险不是tick内最大风险。','',
 '## 两类模拟保持连续','']
shadow=f"原SMA65/1%延迟shadow仅15:00→17:00追加120个已闭合分钟mark，旧{r['plan']['forward_resume']['prior_NAV_points']}点完整前缀不变，新{r['plan']['forward_resume']['total_NAV_points']}点/{r['plan']['forward_resume']['cumulative_minutes']}分钟、完整7天，0新日决策/参考/成交/费用，下次Oct10UTC00:01，3x累计{f['configs']['forward_snapshot_combo']['scenes']['3']['net_return_pct']:.6f}%。原计划SHA及2027-03-31结束保持；这是延迟历史分钟重建，不是十策略当时公开报价前向成交。"
lines+=[shadow,'',f"固定P01–P10保持第{paper['actual_quote_observations']}次真实报价观察（{paper['observed_at_utc']}），跨度{paper['elapsed_seconds']/3600:.6f}小时，主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。未运行paper执行器或修改冻结规则/本金/现金/币数量/desired/已处理日线/费用及交易；180天/6窗未成熟，回撤限于实际保存报价快照。网页只读汇总已有账本和报告，不重新部署或建重复任务。",'', '## 复现与后续','',f"`.venv/bin/python research/experiments/{T.name}/replay_verify.py`；7阶段信号夹具、旧缓存、新历史、原shadow、独立审计和登记检查，不HTTP、不写登记或paper账户。新配置39条全部先reserve后执行/抓取并finish；旧BTC只读从归档/同SHA数据恢复NAV，未重跑旧信号/订单。",'', '绝对历史门槛通过不等于稳定实盘盈利或独立最终验证。全部新参数、真实负折、失败和成本证据保留，当前不追加未预定网格、不替换固定模拟盘；后续新规则/时间区间须另行冻结登记。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原SMA冻结账户延迟分钟mark\n\n'+shadow+'\n')
print(json.dumps({'historical_configs':36,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'portfolio_pairs':len(pairs),'joint_nonworse_pairs':comparison['new_qualified_pairs_jointly_nonworse_with_improvement'],'strict_both_year_return_gain_pairs':comparison['new_qualified_pairs_strict_return_gain_in_both_years'],'path_signatures':comparison['path_signature_counts'],'surfaces':surfaces},ensure_ascii=False))
