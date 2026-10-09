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
 for kind,axis in [('MATCHED_CHANNEL_EMA','ETH_EMA_span_days'),('MATCHED_VOL_CHANNEL','BTC_volume_lookback_days')]:
  on,o=next((on,o)for on,o in r['read_only_comparators'].items()if o['kind']==kind and o['year']==c['year'] and o[axis]==c[axis])
  comparisons.append({'config':n,'year':c['year'],'control_kind':kind,'comparator':on,'same_initial_funding':[1500,500],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in ('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in ('1','2','3'))})
pairchecks=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 bykind={}
 for kind in ('MATCHED_CHANNEL_EMA','MATCHED_VOL_CHANNEL'):
  rows=[next(x for x in comparisons if x['config']==n and x['control_kind']==kind)for n in pair];returns=[v for row in rows for v in row['return_differences_pp'].values()];dds=[row['minute_DD3_difference_pp']for row in rows]
  bykind[kind]={'all_returns_nonworse_both_years':all(v>=0 for v in returns),'DD3_nonworse_both_years':all(v<=0 for v in dds),'joint_improvement_both_years':all(v>=0 for v in returns)and all(v<=0 for v in dds)and(any(v>0 for v in returns)or any(v<0 for v in dds))}
 pairchecks.append({'pair':pair,'by_control_kind':bykind,'jointly_improves_both_controls_in_both_years':all(v['joint_improvement_both_years']for v in bykind.values())})
surfaces={}
for year in ('2025','2026'):
 cells=[c for c in configs.values()if c['year']==year];sens=r['sensitivity'][year+'_BTC_VOLRATIO_ETH_EMA'];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['BTC_volume_lookback_days'],c['ETH_EMA_span_days']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[year]={'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':coords,'best_on_boundary':any(n in (20,40)or e in (50,80)for n,e in coords)}
comparison={'report_sha256':sha(T/'report.json'),'matched_comparisons':comparisons,'qualified_pairs_vs_matched_controls':pairchecks,'new_both_periods_qualified':len(pairchecks),'new_qualified_pairs_jointly_improve_both_controls':sum(x['jointly_improves_both_controls_in_both_years']for x in pairchecks),'failure_counts':dict(Counter(k for c in configs.values()for k in c['failed_criteria'])),'source_component_path_signature_counts':prior['existing_component_path_signature_counts'],'surface_diagnostics':surfaces,'scope':'Whole-cost paths,identical1500/500funding;A sameETH/unfilteredBTC,B sameBTC/ETHchannel. Descriptive reused-history evidence,not independent market samples.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with (T/'folds.csv').open('w',newline='')as out:
 w=csv.writer(out,lineterminator='\n');w.writerow(['config','year','BTC_volume_days','ETH_EMA_span_days','cost','fold','net_return_pct','minute_DD_pct','daily_DD_pct','Sharpe365','Calmar'])
 for n,c in configs.items():
  for k,s in c['scenes'].items():
   for j,z in enumerate(s['folds'],1):w.writerow([n,c['year'],c['BTC_volume_lookback_days'],c['ETH_EMA_span_days'],k,j,*[z[x]for x in ('net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar')]])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['BTC_volume_lookback_days'],c['ETH_EMA_span_days']):c for c in configs.values()if c['year']==year}
 for i,(key,title)in enumerate([('net_return_pct','3x net return %'),('max_drawdown_pct','3x whole minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[n,e]['scenes']['3'][key]for e in grid['ETH_EMA_span_days']]for n in grid['BTC_volume_lookback_days']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a,n in enumerate(grid['BTC_volume_lookback_days']):
   for b,e in enumerate(grid['ETH_EMA_span_days']):ax.text(b,a,f'{matrix[a,b]:.3f} '+('P'if cells[n,e]['status']=='passed'else'R'),ha='center',va='center',fontsize=10,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=[str(x)for x in grid['ETH_EMA_span_days']],yticks=range(3),yticklabels=grid['BTC_volume_lookback_days'],xlabel='ETH EMA span days (symmetric 1.5%)',ylabel='BTC preceding turnover mean days',title=year+' | '+title);fig.colorbar(im,ax=ax,fraction=.035)
fig.suptitle('BTC close-channel15/30 + turnover ratio1 / ETH recursive EMA1.5%\nFrozen75/25:1500/500USDT | P/R=annual gates | reused180-day histories',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
summary=r['summary'];focus=[c for c in configs.values()if c['BTC_volume_lookback_days']==30 and c['ETH_EMA_span_days']==65]
paperstate=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/paperstate['last_observation_id']/'summary.json').read_text())
lines=['# BTC成交额确认通道＋ETH递推EMA','',f"18个新年度组合/54成本场景实际完成；1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(pairchecks)}组新参数分别通过两段复用历史门槛。12个1500/500USDT源组件只读，无旧信号或成交重跑。两类匹配对照均在两年收益/风险同步改善者{comparison['new_qualified_pairs_jointly_improve_both_controls']}组。",'',
 '## 事前假设、精确规则和原始资金','',
 '上一轮BTC成交额确认＋ETH非对称SMA组合未胜过相同BTC的ETH通道对照。本轮事前固定BTC15/30收盘通道＋前日成交额不低于之前N日均额（N20/30/40，倍率1），交叉ETH EMA50/65/80日、对称1.5%迟滞；关注点N30/EMA65。较快的指数响应可能改变趋势参与和回撤，也可能增大反复交易或错失行情；比较同ETH的未过滤BTC、同BTC的ETH15/30通道两个控制轴。未见新结果前冻结完整3×3×两年，不在结果之后扩网格。','',
 'BTC决策i仅使用已闭合UTC前日C[i−1]、USDT成交额Q[i−1]。严格C[i−1]>max(C[i−16:i−1])且Q[i−1]≥mean(Q[i−N−1:i−1])、参考均额>0设多头；严格C[i−1]<min(C[i−31:i−1])无成交额条件设现金。通道和成交额参考都止于i−2，排除被比较日；成交额相等合格，价格相等/死区保留desired，低成交额本身不退出。Q为1440条真实UTC分钟quote_volume精确Decimal和，均额Decimal28；无额外波动门槛、止损、arming或做空。','',
 'ETH递推EMA与原源代码完全一致：Python float，alpha=2/(span+1)，E[0]=各年度源数据day0首个已闭合收盘；j>0时E[j]=(1−alpha)×E[j−1]+alpha×float(C[j])，adjust=False，连续递推、不逐折或每轮重置。决策i比较float(C[i−1])与E[i−1]，严格高于1.015倍设多头、严格低于0.985倍设现金，其余/等号保持desired。EMA包含被比较的前日收盘；两币均以OOS183现金/desired-cash开始，暖机不造持仓或交易，六折状态连续。','',
 '原始BTC/ETH75/25是每组2000USDT的1500/500独立初始分仓，不是维持权重或杠杆。把相同预算、相同分钟/执行节点时间轴、已扣成本的绝对NAV相加一次；无归一化、缩放其他规模净值、二次加权、转账或再平衡，不平均收益率/Sharpe。','',
 f"事前完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范配置、{len(prior['conclusions'])}轮全文结论、7个Freqtrade结果和4个OOS源码。最初16行与别名的实际证据逐份核对，缺真实结果0；工程夹具不算回测。18新组合及3个原shadow截止均先reserve再执行、按实际结果finish；旧源/对照状态和criteria保留，组件被淘汰不等于没有真实结果。",'',
 '## 三项验证和门槛','',
 '时间walk-forward实际完成：2025与2026各03-18UTC00:01→09-14UTC00:01，分别180天、6个连续30天折，原180日滚动历史/3日gap/purge0。固定因果规则无模型、标签或逐折/OOS拟合。信号可得后在历史下一00:01真实分钟开盘估计成交，期末含成本清仓；跨折延续，整体回撤使用259382个连续分钟收盘及执行节点，不平均折回撤。两年资金独立，反复研究历史不是未触碰最终测试集。','',
 '参数敏感性实际完成：BTC成交额均值N与ETH EMA长度独立交叉，完整9格×两年×1/2/3倍成本。sensitivity.csv保留54场景净收益、连续整体/日采样回撤、Sharpe365、Calmar、成本/往返；folds.csv保留全部324折，包括负收益/零收益。最高点、边界平局和12条邻接边保留，描述性2sd差异不是显著性、PBO或DSR。','',
 '成本压力实际完成：每侧10bp手续费、1bp估计半点差、2bp滑点，加0.5×前20个完整UTC日未年化样本log波动率×sqrt(订单预算/滞后20日quote ADV)冲击，四项同时×1/2/3；参与率≤0.001。沿用Decimal28现金/数量、PRICE不利tick/LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理。Oct1静态规则用于旧历史为假设；缺历史L2、TCA、队列/部分成交、延迟或真实IOC接单/容量保证。只做多现货，资金费/借币不适用。','',
 '八门槛固定：全成本净正、1x≥4/6严格正折、3x整体分钟及执行节点DD≤25%、3x邻域净正≥60%、1x≥2组件往返、1x毛参考盈亏/成本≥2.5、无负余额/币数量、终止空仓。独立从真实分钟价格＋源归档现金/数量重建36旧源及54新场景，核对14,006,628个组合NAV点、逐折复利、费用和门槛；旧对照只读。', '',f"失败条件计数{comparison['failure_counts']}。正收益仍可能因折数/风险等淘汰，所有结果和负折保留。",'',
 '## 所有组合按各年1x收益倒序','',
 '|年份|BTC均额N/ETH EMA天|原权重|1x%|2x%|3x%|3x整体分钟DD%|1x正折|1x成交/往返|成本1USDT（手续费/冲击）|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(configs.values(),key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 s=c['scenes']['1'];parts=s['cost_parts_usdt'];lines.append(f"|{c['year']}|{c['BTC_volume_lookback_days']}/{c['ETH_EMA_span_days']}|75/25|{s['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{s['executions']}/{s['round_trips']}|{s['cost_usdt']:.6f}（{parts['fee']:.6f}/{parts['impact']:.6f}）|{c['status']}|")
lines+=['','## 预定焦点和匹配对照','']
for c in focus:
 lines.append(f"{c['year']} N30/EMA65：1/2/3x收益"+'/'.join(f"{c['scenes'][k]['net_return_pct']:.6f}%"for k in ('1','2','3'))+f"，3x整体分钟DD{c['scenes']['3']['max_drawdown_pct']:.6f}%。")
 for row in [x for x in comparisons if x['config']==c['name']]:lines.append(f"对照{row['control_kind']}：3x收益差{row['return_differences_pp']['3']:.6f}个百分点，DD差{row['minute_DD3_difference_pp']:.6f}个百分点，完整全成本NAV相同={row['all_cost_NAV_identical']}。")
for year,d in surfaces.items():lines.append(f"{year}：3x净正{100*d['positive3_fraction']:.3f}%，通过{100*d['full_gate_pass_fraction']:.3f}%；描述性陡峭边{d['descriptive_cliff_flags']}/12，最高3x收益N/EMA坐标{d['best_return3_coordinates']}，边界平局={d['best_on_boundary']}。")
lines += ['',f"源全成本路径种数{prior['existing_component_path_signature_counts']}。54新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，去重后{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径，2026新组合3x未见路径{h['new_2026_combo_3x_paths_not_in_any_prior_report']}。合格跨期参数{len(pairchecks)}组，仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种此前未见的全成本跨期配对；路径身份不等于新的市场样本。",'',
 f"相对相同ETH的未过滤BTC对照，两年同步不更差且有改善者{sum(x['by_control_kind']['MATCHED_CHANNEL_EMA']['joint_improvement_both_years']for x in pairchecks)}组；相对相同BTC的ETH通道对照为{sum(x['by_control_kind']['MATCHED_VOL_CHANNEL']['joint_improvement_both_years']for x in pairchecks)}组；两控制轴均同步改善者{comparison['new_qualified_pairs_jointly_improve_both_controls']}组。36条匹配比较逐项留comparison.json；现金0和旧持有/SMA基准亦保留为历史背景，无新回测或改写旧结论。",'',
 '## 两类模拟边界与复现','']
shadow=f"原SMA65/1%延迟shadow只13:00→15:00追加120个已闭合分钟mark，保留旧{r['plan']['forward_resume']['prior_NAV_points']}点完整前缀，新{r['plan']['forward_resume']['total_NAV_points']}点/{r['plan']['forward_resume']['cumulative_minutes']}分钟、完整7天；0新日决策/参考/成交/费用，下次Oct10UTC00:01，3x累计{f['configs']['forward_snapshot_combo']['scenes']['3']['net_return_pct']:.6f}%。原计划SHA和2027-03-31终止不改；这是延迟真实分钟重建，不是十策略当时公开报价的前向成交。"
lines+=[shadow,'',f"固定P01–P10保持第{paper['actual_quote_observations']}次实际报价观察（{paper['observed_at_utc']}），真实跨度{paper['elapsed_seconds']/3600:.6f}小时，主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。本轮未运行paper执行器，冻结规则/本金/现金/数量/desired/已处理日线/费用与交易状态保持。180天/六窗未成熟，回撤仅保存报价快照口径。网页只读汇总已有结果，不重新部署。",'',f"复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`；6阶段源缓存/新组合/原shadow/独立核算与登记精确重放，不HTTP、不写登记或paper账户。源缓存缺失只从同SHA真实数据重建已有NAV，不重跑旧信号/成交。",'', '所有新配置、低收益、负折和淘汰永久保存；正收益历史不等于稳定实盘盈利。局部峰值、路径复用、多重选择和成本估计限制保持，不从本轮结果追加网格或替换固定模拟盘。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原SMA冻结账户延迟续接\n\n'+shadow+'\n')
print(json.dumps({'annual_passed':len(summary['passed']),'annual_rejected':len(summary['rejected']),'new_cross_period_parameters':len(pairchecks),'new_cross_period_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'joint_both_control_improvements':comparison['new_qualified_pairs_jointly_improve_both_controls'],'surface_diagnostics':surfaces},ensure_ascii=False))
