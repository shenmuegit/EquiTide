"""Describe completed combinations,full sensitivity and two independently matched controls."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));h=json.loads((T/'history_paths.json').read_text())
configs=r['configs'];grid=r['plan']['grid'];comparisons=[]
for n,c in configs.items():
 for kind,axis in [('MATCHED_CHANNEL_ASMA','ETH_SMA_entry_band'),('MATCHED_VOL_CHANNEL','BTC_volume_lookback_days')]:
  on,o=next((on,o)for on,o in r['read_only_comparators'].items()if o['kind']==kind and o['year']==c['year'] and o[axis]==c[axis])
  comparisons.append({'config':n,'year':c['year'],'control_kind':kind,'comparator':on,'same_initial_funding':[1500,500],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in ('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in ('1','2','3'))})
pairchecks=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 bykind={}
 for kind in ('MATCHED_CHANNEL_ASMA','MATCHED_VOL_CHANNEL'):
  rows=[next(x for x in comparisons if x['config']==n and x['control_kind']==kind)for n in pair];returns=[v for row in rows for v in row['return_differences_pp'].values()];dds=[row['minute_DD3_difference_pp']for row in rows]
  bykind[kind]={'all_returns_nonworse_both_years':all(v>=0 for v in returns),'DD3_nonworse_both_years':all(v<=0 for v in dds),'joint_improvement_both_years':all(v>=0 for v in returns)and all(v<=0 for v in dds)and(any(v>0 for v in returns)or any(v<0 for v in dds))}
 pairchecks.append({'pair':pair,'by_control_kind':bykind,'jointly_improves_both_controls_in_both_years':all(v['joint_improvement_both_years']for v in bykind.values())})
surfaces={}
for year in ('2025','2026'):
 cells=[c for c in configs.values()if c['year']==year];sens=r['sensitivity'][year+'_BTC_VOLRATIO_ETH_ASMA'];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['BTC_volume_lookback_days'],c['ETH_SMA_entry_band']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[year]={'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':coords,'best_on_boundary':any(n in (20,40)or e in (.0125,.02)for n,e in coords)}
comparison={'report_sha256':sha(T/'report.json'),'matched_comparisons':comparisons,'qualified_pairs_vs_matched_controls':pairchecks,'new_both_periods_qualified':len(pairchecks),'new_qualified_pairs_jointly_improve_both_controls':sum(x['jointly_improves_both_controls_in_both_years']for x in pairchecks),'failure_counts':dict(Counter(k for c in configs.values()for k in c['failed_criteria'])),'source_component_path_signature_counts':prior['existing_component_path_signature_counts'],'surface_diagnostics':surfaces,'scope':'Whole-cost paths,identical1500/500funding;A sameETH/unfilteredBTC,B sameBTC/ETHchannel. Descriptive reused-history evidence,not independent market samples.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with (T/'folds.csv').open('w',newline='')as out:
 w=csv.writer(out,lineterminator='\n');w.writerow(['config','year','BTC_volume_days','ETH_entry','cost','fold','net_return_pct','minute_DD_pct','daily_DD_pct','Sharpe365','Calmar'])
 for n,c in configs.items():
  for k,s in c['scenes'].items():
   for j,z in enumerate(s['folds'],1):w.writerow([n,c['year'],c['BTC_volume_lookback_days'],c['ETH_SMA_entry_band'],k,j,*[z[x]for x in ('net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar')]])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['BTC_volume_lookback_days'],c['ETH_SMA_entry_band']):c for c in configs.values()if c['year']==year}
 for i,(key,title)in enumerate([('net_return_pct','3x net return %'),('max_drawdown_pct','3x whole minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[n,e]['scenes']['3'][key]for e in grid['ETH_SMA_entry_band']]for n in grid['BTC_volume_lookback_days']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a,n in enumerate(grid['BTC_volume_lookback_days']):
   for b,e in enumerate(grid['ETH_SMA_entry_band']):ax.text(b,a,f'{matrix[a,b]:.3f} '+('P'if cells[n,e]['status']=='passed'else'R'),ha='center',va='center',fontsize=10,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=[f'{100*x:g}'for x in grid['ETH_SMA_entry_band']],yticks=range(3),yticklabels=grid['BTC_volume_lookback_days'],xlabel='ETH SMA65 entry band % (exit 0.5%)',ylabel='BTC preceding turnover mean days',title=year+' | '+title);fig.colorbar(im,ax=ax,fraction=.035)
fig.suptitle('BTC close-channel15/30 + turnover ratio1 / ETH asymmetric SMA65\nFrozen75/25:1500/500USDT | P/R=annual gates | reused180-day histories',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
summary=r['summary'];focus=[c for c in configs.values()if c['BTC_volume_lookback_days']==30 and c['ETH_SMA_entry_band']==.015]
lines=['# BTC成交额确认通道＋ETH非对称SMA65','',f"18个新年度组合/54成本场景实际完成，1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(pairchecks)}组新跨期参数通过。12个同资金源组件只读复用，没有重跑旧信号或成交。相对两类匹配对照，同时改善两期全成本收益与三倍整体回撤的新组合{comparison['new_qualified_pairs_jointly_improve_both_controls']}组。",'',
 '## 事前规则、资金与查重','',
 '本轮只探索一个新组合方向：BTC15/30收盘通道＋相对USDT成交额确认，交叉ETH SMA65非对称阈值。看新收益前冻结BTC成交额均值N20/30/40日、阈值固定1，以及ETH入场1.25/1.5/2%、退出固定0.5%；焦点N30/ETH1.5%。希望BTC活动确认与ETH迟滞形成互补，也可能错失趋势或增大成本。两类对照预定为相同ETH的未过滤BTC通道，以及相同BTC的ETH15/30通道。','',
 'BTC决策i仅用完整前一UTC日C[i−1]、USDT成交额Q[i−1]：C[i−1]>max(C[i−16:i−1])且Q[i−1]≥mean(Q[i−N−1:i−1])、均额>0设desired-long；C[i−1]<min(C[i−31:i−1])无成交额条件退出。通道与成交额参考范围都排除被测试的i−1日，成交额相等合格，价格相等/死区延续状态，低成交额单独不强制卖出。Q是1440条真实分钟quote_volume精确Decimal和，非币数量；N日均额用Decimal28。无EMA、波动止损、arming、做空或新规则。','',
 'ETH为Decimal28最近65个已闭合收盘均值mean(C[i−65:i])，包含被比较C[i−1]。严格上破SMA×(1+entry)入场，严格下破SMA×0.995退出，等号/死区保留desired。两币OOS183起点均为现金/desired-cash，历史只暖机，六折间持仓和状态连续，不每折重置。','',
 '每组2000USDT，原始75/25是BTC1500/ETH500独立初始资金。复用完全同预算、同时间轴、已扣成本的绝对NAV，相加一次；无缩放、二次乘权重、归一化、转账、维持比例或再平衡；不平均收益率或Sharpe。','',
 f"已读取完整{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}轮全文结论、7个Freqtrade文件和4个OOS源码，源报告/归档/行情及技能SHA留档。初始16按最初16行和别名核验，缺实际结果0；已有淘汰结果不删除。18组合与3个原shadow截止全部先reserve再计算并finish，未以重命名、组件顺序或等价数值伪造新配置。",'',
 '## 三项验证','',
 'Walk-forward实际执行：2025与2026各03-18UTC00:01至09-14UTC00:01，各180天/6个连续30天折；原180日滚动历史、3日gap、purge0，无模型、标签、逐折或OOS拟合。交易在信号可得后的历史00:01真实分钟开盘估计虚拟成交，终止平仓含费用，完整连续259382点NAV计算整体回撤，不平均折回撤。两年资金独立；反复使用的历史不是未触碰最终留出。','',
 'Sensitivity实际执行：完整3×3×两年、1/2/3成本、全变体收益/整体与日采样回撤/Sharpe365/Calmar在sensitivity.csv和report.json；全部324折含负收益与零收益在folds.csv。热图保留平台、边界平局与12条邻接边；2sd差异标记只作描述，不是显著性、DSR/PBO。','',
 'Costs实际执行：手续费每侧10bp、估计半点差1bp、滑点2bp，加0.5×滞后20个完整UTC日未年化样本log波动率×sqrt(订单预算/滞后20日quote ADV)冲击，四项同时放大1/2/3倍，参与率≤0.001。Decimal28余额、PRICE不利取整、LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理沿用源核算。Oct1静态规则应用旧历史为明确估计；缺历史L2、队列、部分成交、TCA和真实接单/容量证明。现货只做多，无资金费或借币。','',
 '八项门槛保持：全成本净正、1x≥4/6严格正折、3x整体分钟及执行节点DD≤25%、3x邻域净正≥60%、1x≥2组件往返、1x毛参考PnL/成本≥2.5、无负余额/数量、终止空仓。源组件即使旧状态rejected仍按原记录只读，组合独立按自身路径判断。','',
 f"独立审计36个源场景、54新场景及{summary['new_minute_NAV_points']:,}个组合NAV点，逐段从真实分钟价格与归档现金/币数量重建，核对费用、终止现金、全折复利一致及八门槛。负折、失败和所有结果保留；无新真实订单。失败条件计数{comparison['failure_counts']}。",'',
 '## 所有组合按各年1x净收益倒序','',
 '|年份|BTC成交额N/ETH入场%|原权重|1x%|2x%|3x%|3x整体分钟DD%|1x正折|1x成交/往返|1x成本USDT（手续费/冲击）|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(configs.values(),key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 s=c['scenes']['1'];p=s['cost_parts_usdt'];lines.append(f"|{c['year']}|{c['BTC_volume_lookback_days']}/{100*c['ETH_SMA_entry_band']:g}|75/25|{s['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{s['executions']}/{s['round_trips']}|{s['cost_usdt']:.6f}（{p['fee']:.6f}/{p['impact']:.6f}）|{c['status']}|")
lines+=['','## 匹配对照、敏感性和路径身份','']
for c in focus:
 lines.append(f"事前焦点{c['year']} N30/ETH1.5%：1/2/3x收益"+'/'.join(f"{c['scenes'][k]['net_return_pct']:.6f}%"for k in ('1','2','3'))+f"，3x整体分钟DD{c['scenes']['3']['max_drawdown_pct']:.6f}%。")
 for row in [x for x in comparisons if x['config']==c['name']]:lines.append(f"- 对照{row['control_kind']}：3x收益差{row['return_differences_pp']['3']:.6f}个百分点，DD差{row['minute_DD3_difference_pp']:.6f}个百分点，全成本NAV相同={row['all_cost_NAV_identical']}。")
for year,d in surfaces.items():lines.append(f"{year}：3x净正{100*d['positive3_fraction']:.3f}%，通过{100*d['full_gate_pass_fraction']:.3f}%；描述性陡峭边{d['descriptive_cliff_flags']}/12，最高收益N/entry坐标{d['best_return3_coordinates']}，边界平局={d['best_on_boundary']}。")
lines += ['', '2025 BTC成交额均值轴的N30为局部高点，N20/N40三倍收益均低9.831921个百分点；ETH三阈值完整路径平坦。2026 BTC三长度全成本路径相同，ETH1.5/2%也同路径。绝对净正邻域与双期门槛通过不等于N30收益峰值已获独立稳定性验证。']
lines += ['',f"源组件全成本路径种数{prior['existing_component_path_signature_counts']}。54新场景中{h['new_scenes_already_in_any_prior_report']}曾见、{h['new_scenes_not_in_any_prior_report']}未见，去重后{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径；2026新组合3x未见路径{h['new_2026_combo_3x_paths_not_in_any_prior_report']}种。9组跨期合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种此前未见的跨期配对；参数不同或配对新颖不构成新的市场样本。",'',
 f"相对A未过滤BTC/同ETH，两年同时不更差并有改进的合格参数{sum(x['by_control_kind']['MATCHED_CHANNEL_ASMA']['joint_improvement_both_years']for x in pairchecks)}组；相对B同BTC/ETH通道为{sum(x['by_control_kind']['MATCHED_VOL_CHANNEL']['joint_improvement_both_years']for x in pairchecks)}组。两类对照都同步改善者{comparison['new_qualified_pairs_jointly_improve_both_controls']}组。全部36条匹配比较保存在comparison.json；现金0与原持有/SMA对照来自原报告，不重新回测或重写旧状态。",'',
 '## 原SMA延迟shadow、固定模拟盘和复现','',
 f"原SMA65/1%延迟shadow只11:00→13:00追加120个闭合分钟mark，完整保留旧{r['plan']['forward_resume']['prior_NAV_points']}点前缀，新{r['plan']['forward_resume']['total_NAV_points']}点/{r['plan']['forward_resume']['cumulative_minutes']}分钟、完整7天，0新日线决策/参考/成交/费用，下次2026-10-10UTC00:01。3x累计{f['configs']['forward_snapshot_combo']['scenes']['3']['net_return_pct']:.6f}%；原2027-03-31结束计划及SHA不改。明确为延迟真实分钟重建，不计作当时真实报价成交。",'',
 'P01–P10保持第22次真实行情观察（2026-10-09T12:59:33.875577Z），约42.454508小时，主账户合计19956.6471319277USDT。没有运行paper执行器、修改冻结参数/本金/现金/币数量/desired/日线处理/成交；180天及6窗尚未成熟，回撤仅按已保存报价快照。网页只读汇总已有账本和研究，不重新部署。','',
 f"复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`。6阶段精确重放全部新组合/源归档、原shadow、独立审计与登记检查，不HTTP或写登记/paper账户；源缓存缺失仅从同SHA真实数据重建旧NAV，不重跑信号与订单。",'',
 '正收益只表示复用历史上的结果；保留全部新配置和负折，不把网格平局、旧路径或短期虚拟业绩称稳定实盘盈利。下一轮如探索新规则或参数需另行事前冻结，本轮不因看到结果追加配置，固定模拟盘持续原计划。']
(T/'result.md').write_text('\n'.join(lines)+'\n')
(T/'forward_result.md').write_text('# 原SMA冻结账户延迟分钟mark续接\n\n'+lines[-7]+'\n\n非P01–P10真实报价前向业绩；账户不重启、无新成交。\n')
print(json.dumps({'annual_passed':len(summary['passed']),'annual_rejected':len(summary['rejected']),'new_cross_period_parameters':len(pairchecks),'new_cross_period_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'joint_both_control_improvements':comparison['new_qualified_pairs_jointly_improve_both_controls'],'surface_diagnostics':surfaces},ensure_ascii=False))
