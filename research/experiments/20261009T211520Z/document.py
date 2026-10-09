"""Document complete old/new parent grid and matched BTC30 controls;no new financial evaluation."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));cs=r['configs'];grid=r['plan']['grid'];fresh=[c for c in cs.values()if c['is_new']]
comparisons=[]
for c in cs.values():
 name,o=next((name,o)for name,o in r['read_only_comparators'].items()if o['kind']=='MATCHED_BTC30_SAME_ETH'and o['year']==c['year']and o['ETH_volume_lookback_days']==c['ETH_volume_lookback_days'])
 comparisons.append({'config':c['name'],'year':c['year'],'is_new':c['is_new'],'comparator':name,'same_initial_funding':[1500,500],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 xs=[next(x for x in comparisons if x['config']==name)for name in pair];ret=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
 pairs.append({'pair':pair,'all_returns_nonworse_both_years':all(v>=0 for v in ret),'DD3_nonworse_both_years':all(v<=0 for v in dd),'joint_improvement_both_years':all(v>=0 for v in ret)and all(v<=0 for v in dd)and(any(v>0 for v in ret)or any(v<0 for v in dd))})
surfaces={}
for year in('2025','2026'):
 cells=[c for c in cs.values()if c['year']==year];sens=r['sensitivity'][year+'_BTC_ETH_VOLUME_WINDOW_INTERACTION'];best=max(c['scenes']['3']['net_return_pct']for c in cells)
 surfaces[year]={'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'displayed_full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':[[c['BTC_volume_lookback_days'],c['ETH_volume_lookback_days']]for c in cells if c['scenes']['3']['net_return_pct']==best],'whole_cost_path_signature_count':len({tuple(c['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))for c in cells})}
comparison={'report_sha256':sha(T/'report.json'),'matched_comparisons':comparisons,'qualified_pairs_vs_matched_controls':pairs,'new_both_periods_qualified':len(pairs),'new_pairs_jointly_improve_same_ETH_BTC30_controls':sum(p['joint_improvement_both_years']for p in pairs),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'source_component_path_signature_counts':prior['existing_component_path_signature_counts'],'surface_diagnostics':surfaces,'scope':'Raw75/25 exact1500/500USDT;change BTCwindow against sameETH control. Oldcentre30/20 and BTC30row preserve source status/criteria. Reused history and repeated NAVs are not independent market evidence.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as out:
 w=csv.writer(out,lineterminator='\n');w.writerow(['config','year','is_new','BTC_mean_days','ETH_mean_days','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['is_new'],c['BTC_volume_lookback_days'],c['ETH_volume_lookback_days'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['BTC_volume_lookback_days'],c['ETH_volume_lookback_days']):c for c in cs.values()if c['year']==year}
 for i,(key,title)in enumerate([('net_return_pct','3x net return %'),('max_drawdown_pct','3x whole minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[bn,en]['scenes']['3'][key]for en in grid['ETH_volume_lookback_days']]for bn in grid['BTC_volume_lookback_days']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a,bn in enumerate(grid['BTC_volume_lookback_days']):
   for b,en in enumerate(grid['ETH_volume_lookback_days']):
    c=cells[bn,en];ax.text(b,a,f'{matrix[a,b]:.3f} '+('N'if c['is_new']else'O'),ha='center',va='center',fontsize=10,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=grid['ETH_volume_lookback_days'],yticks=range(3),yticklabels=grid['BTC_volume_lookback_days'],xlabel='ETH preceding turnover mean days (ratio0.875)',ylabel='BTC preceding turnover mean days (ratio1)',title=year+' | '+title);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
fig.suptitle('Both close-channel15/30 + quote-turnover entry confirmation\nRaw75/25:1500/500USDT | N=new O=old read-only | old gates preserved | reused180-day histories',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
paperstate=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/paperstate['last_observation_id']/'summary.json').read_text());summary=r['summary']
lines=['# BTC/ETH成交额窗口独立交叉：20/30/40 × 15/20/25','',f"12个新年度组合/36新成本场景实际执行，1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}；{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(pairs)}组新跨期参数合格。完整18组合含6个BTC30旧行/18场景只读；12个精确1500/500USDT源组件/36场景只读，无旧信号和成交重跑。15新定义含原shadow截止均reserve/finish。",'',
 '## 事前假设、规则、原始资金','',
 '上一轮ETH20/r0.875修复了旧r1在2026的退化，但2025比不加ETH过滤的早期基线有更高回撤。本轮事前固定ETH倍率0.875、BTC倍率1，把BTC均额20/30/40日与ETH均额15/20/25日独立交叉；中心和关注点BTC30/ETH20已存在，严格只读。测试BTC活动窗口改变是否破坏这个新跨期配对，或邻居能在保持回报时降低风险。完整网格及门槛先冻结，不在结果之后追加参数。','',
 '每币决策i仅用完整UTC前日C[i−1]、USDT成交额Q[i−1]。严格C[i−1]>max(C[i−16:i−1])且Q[i−1]≥r×mean(Q[i−N−1:i−1])、均额>0才设desired-long；严格C[i−1]<min(C[i−31:i−1])无成交额条件退出。价格/成交额参考都止于i−2，排除被比较日；成交额相等合格，价格相等/死区保持状态，低活动本身不强制退出，零均额禁入。Q为真实1440分钟quote_volume精确Decimal和，均额/比率Decimal28。无EMA/SMA/ATR、arming、止损或空头。','',
 'BTC/ETH原75/25仅为2000USDT的1500/500独立初始分仓。复用相同预算、相同UTC分钟/执行节点、已扣成本的绝对NAV，相加一次；不缩放旧NAV、二次乘权重、归一化、转账、维持比例或再平衡，不平均收益率或Sharpe。源组件OOS183均为现金/desired-cash，暖机不造旧持仓，六折资金和状态连续。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}轮全文结论、7个Freqtrade结果、4个OOS源码与3技能。初始16原始行/别名实际证据核验均完整。此前2498历史配置，本轮12新增后2510；6旧年度组合未重新reserve或改criteria/status，源12组件不重跑。",'',
 '## 三项验证和门槛','',
 'Walk-forward实际完成：2025、2026各03-18UTC00:01→09-14UTC00:01，分别180天/6个连续30天折；原180日滚动历史、3日gap、purge0，无模型/标签/逐折或OOS拟合。信号可得后用下一00:01真实历史分钟开盘估计执行，末端平仓含成本；连续259382点分钟收盘和执行节点计算整体回撤，不平均折回撤。两年本金独立，已有反复使用历史不是未触碰最终留出。','',
 'Sensitivity实际完成：两个资产活动窗口同时变化，完整9格×两年×1/2/3倍成本。sensitivity.csv保留54组合场景（36新、18旧）的收益/整体与日采样回撤/Sharpe365/Calmar/成本/往返；folds.csv含324折（216新、108旧），负收益与零收益全部保留。旧BTC30行沿用原状态与criteria，描述性2sd相邻差异不是显著性、DSR/PBO或独立优化。','',
 'Costs实际完成：每侧10bp手续费、估计半点差1bp、滑点2bp，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(订单预算/滞后20日quote ADV)冲击，四项同时×1/2/3，参与率≤0.001。Decimal28现金/数量、PRICE不利tick、LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理独立核对。Oct1静态规则用于旧历史为假设，缺历史L2、TCA、队列/部分成交、延迟与真实IOC接单/容量保证。只做多现货，资金费/借币不适用。','',
 '八门槛保持：全成本净正、1x≥4/6严格正折、3x整体分钟/执行节点DD≤25%、3x邻域净正≥60%、1x≥2组件往返、1x毛参考盈亏/成本≥2.5、无负余额/数量、终止空仓。源ETH2026旧淘汰结果仍保留，组合按自身路径独立判断。','',
 f"新配置失败条件计数{comparison['failure_counts']}。独立核对36源组件场景和54完整组合场景，其中36新组合场景有9,337,752NAV点；旧18组合场景与全部源现金/数量从相同真实价格重建，费用和各折复利/风险核对。6阶段完整只读重放与登记退出码留档。",'',
 '## 全部组合按各年1x净收益倒序','',
 '|年份|新/旧|BTC/ETH均额天|原权重|1x%|2x%|3x%|3x整体分钟DD%|正折1|成交/往返1|成本1USDT（手续费/冲击）|状态|','|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(cs.values(),key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes']['1'];p=z['cost_parts_usdt'];lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['BTC_volume_lookback_days']}/{c['ETH_volume_lookback_days']}|75/25|{z['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{z['executions']}/{z['round_trips']}|{z['cost_usdt']:.6f}（{p['fee']:.6f}/{p['impact']:.6f}）|{c['status']}|")
lines+=['','## 匹配BTC30控制、旧中心与新颖性','']
for year in('2025','2026'):
 centre=next(c for c in cs.values()if c['year']==year and c['BTC_volume_lookback_days']==30 and c['ETH_volume_lookback_days']==20);assert not centre['is_new'];s=centre['scenes']['3'];lines.append(f"旧中心{year} BTC30/ETH20：3x收益{s['net_return_pct']:.6f}%，整体分钟DD{s['max_drawdown_pct']:.6f}%；来源原status/criteria及完整NAV只读，未重新测成新成功。")
for year,d in surfaces.items():lines.append(f"{year}：3x净正{100*d['positive3_fraction']:.3f}%，展示门槛通过{100*d['displayed_full_gate_pass_fraction']:.3f}%；描述性陡峭边{d['descriptive_cliff_flags']}/12，最高三倍收益BTC/ETH窗口{d['best_return3_coordinates']}，全成本路径种数{d['whole_cost_path_signature_count']}。")
lines+=['',f"{len(pairs)}组新跨期参数通过绝对门槛；相对相同ETH的旧BTC30控制，两期全成本收益/3x风险同时不更差且有改善者{comparison['new_pairs_jointly_improve_same_ETH_BTC30_controls']}组。18条匹配比较含旧行自比，全部留comparison.json；现金0及旧持有/SMA只是历史背景。",'',
 f"36新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，去重后{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径；2026新3x组合未见路径{h['new_2026_combo_3x_paths_not_in_any_prior_report']}，合格新跨期配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}种。源全成本路径种数{prior['existing_component_path_signature_counts']}。参数变化是新配置，重复NAV不算独立市场证据；新配对也不是新样本。",'',
 '4份真实525600行分钟parquet、两份日聚合、源报告/组件spec/归档、元数据/代码/输入SHA见spec.json/report.json/data_manifest.json。大行情及NPY留忽略data目录；轻量订单/分段持仓/指标与哈希入Git，完整分钟风险可重建。复用历史、多重选择、成本估计和采样风险限制保持，正收益不等于稳定实盘盈利。','',
 '## 两类模拟与复现','']
shadow=f"原SMA65/1%延迟shadow仅19:00→21:00增加120个已闭合分钟mark，保留旧{r['plan']['forward_resume']['prior_NAV_points']}点完整前缀，新{r['plan']['forward_resume']['total_NAV_points']}点/{r['plan']['forward_resume']['cumulative_minutes']}分钟、完整7天，0新日决策/参考/成交/费用，下次Oct10UTC00:01，3x累计{f['configs']['forward_snapshot_combo']['scenes']['3']['net_return_pct']:.6f}%。原2027-03-31计划和SHA不变；这是延迟历史分钟重建，不是十策略当时真实买卖报价前向成交。"
lines+=[shadow,'',f"固定P01–P10维持第{paper['actual_quote_observations']}次实际报价观察（{paper['observed_at_utc']}），真实跨度{paper['elapsed_seconds']/3600:.6f}小时，主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。本轮未运行paper执行器或修改冻结规则/本金/现金/数量/desired/已处理日线/累计成本和交易。180天/6窗未成熟，回撤限于报价快照采样；网页只读汇总既有账本与研究，无重新部署。",'', f"复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`；6阶段精确检查旧缓存、原shadow、新/旧组合、独立审计与登记，不HTTP、不写登记或paper账户。15个新定义全部先reserve后执行/抓取并finish；旧源/父组合只读，未因同族排除新组合，也未重跑旧信号/成交。",'', '全部新正收益、负折/零折及已有淘汰永久保存。当前不追加未预定参数、不替换固定模拟盘；后续规则、资金或时间区间变化须另行事前固定并登记。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原SMA冻结延迟shadow续接\n\n'+shadow+'\n');print(json.dumps({'new_configs':12,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'old_parent_configs':6,'new_cross_period_parameters':len(pairs),'joint_control_improvements':comparison['new_pairs_jointly_improve_same_ETH_BTC30_controls'],'surfaces':surfaces},ensure_ascii=False))
