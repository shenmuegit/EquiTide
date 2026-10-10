"""Describe already-finished EMA-confirmation results,including every rejected/zero/negative fold."""
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
 name,o=next((n,z)for n,z in r['read_only_comparators'].items()if z['kind']=='MATCHED_BTC_VOLUME_PURE_ETH_CHANNEL'and z['year']==c['year'])
 comparisons.append({'config':c['name'],'year':c['year'],'comparator':name,'same_initial_funding':[1500,500],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in ('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in ('1','2','3'))})
pairs=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 rows=[next(x for x in comparisons if x['config']==n)for n in pair];ret=[v for row in rows for v in row['return_differences_pp'].values()];dd=[row['minute_DD3_difference_pp']for row in rows];seen=next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)
 pairs.append({'pair':pair,'all_returns_nonworse_both_years':all(v>=0 for v in ret),'DD3_nonworse_both_years':all(v<=0 for v in dd),'joint_improvement_both_years':all(v>=0 for v in ret)and all(v<=0 for v in dd)and(any(v>0 for v in ret)or any(v<0 for v in dd)),'strict_return_gain_in_both_years':all(any(v>0 for v in row['return_differences_pp'].values())for row in rows),'whole_pair_path_seen_before':seen})
exposure={};signatures={}
for c in cs.values():
 arc=json.loads(gzip.decompress((R/c['archive']).read_bytes()));sig=tuple(c['scenes'][k]['NAV_sha256_f64le']for k in ('1','2','3'));group=c['asset']if c['role']=='component'else'combination';signatures.setdefault(c['year']+'_'+group,set()).add(sig)
 if c['role']=='component'and c.get('asset')=='ETH':
  z=arc['scenes']['1'];d=z['decisions'];exposure[c['name']]={'year':c['year'],'EMA_span_days':c['EMA_span_days'],'EMA_symmetric_band':c['EMA_symmetric_band'],'archive_sha256':sha(R/c['archive']),'EMA_eligible_days':sum(v['EMA_entry']for v in d),'price_breakout_days':sum(v['channel_entry']for v in d),'blocked_breakout_days':sum(v['channel_entry']and not v['EMA_entry']for v in d),'desired_long_days':sum(v['long']for v in d),'invested_days':sum(st['end_day_exclusive']-st['day_offset']for st in z['position_segments']if float(st['units'])>0),'entry_events':sum(v['action']=='entry'for v in d),'executions1':z['summary']['executions'],'round_trips1':z['summary']['round_trips']}
surfaces={}
for year in ('2025','2026'):
 for group in ('ETH','combination'):
  cells=[c for c in cs.values()if c['year']==year and(c.get('asset')==group or c['role']==group)];sens=r['sensitivity'][year+'_'+group];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['EMA_span_days'],c['EMA_symmetric_band']]for c in cells if c['scenes']['3']['net_return_pct']==best]
  surfaces[year+'_'+group]={'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/9,'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/9,'descriptive_cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'adjacent_edges':12,'best_return3_coordinates':coords,'best_on_boundary':any(n in (35,65)or ratio in (.0125,.0175)for n,ratio in coords),'scope':'Descriptive reused-history sensitivity;not significance,DSR/PBO or untouched final test.'}
comparison={'report_sha256':sha(T/'report.json'),'matched_comparisons':comparisons,'qualified_pairs_vs_matched_controls':pairs,'new_both_periods_qualified':len(pairs),'new_qualified_pairs_jointly_nonworse_with_improvement':sum(x['joint_improvement_both_years']for x in pairs),'new_qualified_pairs_strict_return_gain_in_both_years':sum(x['strict_return_gain_in_both_years']for x in pairs),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'path_signature_counts':{k:len(v)for k,v in signatures.items()},'ETH_signal_exposure':exposure,'surface_diagnostics':surfaces,'interpretation':'Compare new ETH closechannel/EMA confirmation against identicalBTCvolume30/r1 and same raw75/25 funding. Reused histories and duplicate paths are not independent final evidence;no new comparator backtest.'}
anchor_comparisons=[]
focus_configs={c['year']:c for c in portfolios if(c['EMA_span_days'],c['EMA_symmetric_band'])==(35,.015)}
for year,c in focus_configs.items():
 old=next(v for v in portfolios if v['year']==year and(v['EMA_span_days'],v['EMA_symmetric_band'])==(50,.015))
 anchor_comparisons.append({'year':year,'focus':c['name'],'old_anchor':old['name'],'old_anchor_source_report':old['source_ref']['report'],'old_anchor_source_report_sha256':old['source_ref']['report_sha256'],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-old['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==old['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
focus_signature=tuple(focus_configs[year]['scenes'][k]['NAV_sha256_f64le']for year in('2025','2026')for k in('1','2','3'))
equivalent_new_parameters=sorted({(c['EMA_span_days'],c['EMA_symmetric_band'])for c in portfolios if c['year']=='2025'and c['is_new'] and tuple(cs[n]['scenes'][k]['NAV_sha256_f64le']for n in(c['name'],c['other_period_config'])for k in('1','2','3'))==focus_signature})
comparison['predeclared_focus_vs_old50_band15']=anchor_comparisons
comparison['new_parameters_sharing_predeclared_focus_paired_path']=[list(x)for x in equivalent_new_parameters]
comparison['anchor_repair_scope']='Predeclared35/1.5percent focus compared with read-only50/1.5percent center;differences computed from actual all-cost whole paths. Reused histories and any duplicate paths are not independent evidence.'
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with (T/'folds.csv').open('w',newline='')as fh:
 w=csv.writer(fh,lineterminator='\n');w.writerow(['config','year','role','is_new','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['EMA_span_days'],c['EMA_symmetric_band']):c for c in portfolios if c['year']==year}
 for i,(metric,title)in enumerate([('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute sampled NAV DD %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[n,ratio]['scenes']['3'][metric]for ratio in grid['EMA_symmetric_band']]for n in grid['EMA_span_days']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a,n in enumerate(grid['EMA_span_days']):
   for b,ratio in enumerate(grid['EMA_symmetric_band']):ax.text(b,a,f'{matrix[a,b]:.3f}'+(' P'if cells[n,ratio]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=[f'{100*x:g}%'for x in grid['EMA_symmetric_band']],yticks=range(3),yticklabels=grid['EMA_span_days'],xlabel='Symmetric EMA confirmation band',ylabel='Recursive EMA span (days)',title=year+' | '+title);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
fig.suptitle('ETH close-channel15/30 + recursive EMA confirmation / fixed BTC volume30-ratio1\nRaw75/25:1500/500USDT | P/R=annual gates | both180-day histories reused',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for j,year in enumerate(('2025','2026')):
 cells={(c['EMA_span_days'],c['EMA_symmetric_band']):c for c in leaves if c['year']==year}
 for i,(metric,title)in enumerate([('net_return_pct','3x net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[j,i];matrix=np.array([[cells[n,q]['scenes']['3'][metric]for q in grid['EMA_symmetric_band']]for n in grid['EMA_span_days']]);im=ax.imshow(matrix,cmap='YlGnBu'if i!=1 else'YlOrRd',aspect='auto')
  for a,n in enumerate(grid['EMA_span_days']):
   for b,q in enumerate(grid['EMA_symmetric_band']):ax.text(b,a,f'{matrix[a,b]:.3f}'+(' P'if cells[n,q]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[a,b]>(matrix.min()+matrix.max())/2 else'#111111')
  ax.set(xticks=range(3),xticklabels=[f'{100*q:g}%'for q in grid['EMA_symmetric_band']],yticks=range(3),yticklabels=grid['EMA_span_days'],xlabel='Symmetric EMA confirmation band',ylabel='ETH recursive EMA span (days)',title=year+' | '+title);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
fig.suptitle('ETH close-channel15/30 + recursive EMA confirmation | initial500USDT\nP/R=annual gates | completed prior bars only | both histories reused',fontsize=14);fig.savefig(T/'sensitivity_ETH.png',dpi=130);plt.close(fig)

# Apply the same predeclared comparison to every new grid coordinate, not only its focus.
center_rows=[]
for c in portfolios:
 a=next(v for v in portfolios if v['year']==c['year']and(v['EMA_span_days'],v['EMA_symmetric_band'])==(50,.015))
 center_rows.append({'config':c['name'],'year':c['year'],'comparator':a['name'],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-a['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-a['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==a['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
center_pairs=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 xs=[next(x for x in center_rows if x['config']==n)for n in pair];rv=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
 center_pairs.append({'pair':pair,'joint_improvement_both_years':all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd))})
comparison.update(all_grid_vs_old_center=center_rows,qualified_pairs_vs_old_center=center_pairs,qualified_pairs_improving_old_center=sum(x['joint_improvement_both_years']for x in center_pairs))
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
summary=r['summary'];focus=sorted(focus_configs.values(),key=lambda c:c['year']);ps=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/ps['last_observation_id']/'summary.json').read_text());fr=r['plan']['forward_resume'];legacy=f['configs']['forward_snapshot_combo']['scenes']['3']
lines=['# ETH通道EMA确认：35/50/65日 × 对称1.25/1.5/1.75%','',f"14个新ETH组件＋14个新年度组合，共28个新历史配置/84成本场景实际执行；{summary['positive_1x']}个1x净正、{summary['positive_3x']}个3x净正，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(pairs)}组新组合参数跨2025/2026绝对门槛合格；4旧ETH、4旧组合、2固定BTC配置及30场景只读，旧淘汰状态与门槛不改。31新定义含3原shadow截止均先reserve后计算并finish。",'',
 '## 事前规则、资金与假设','',
 '上一轮2026最高收益在ETH EMA50跨度下边界；本轮在新结果前固定更短35/50/65日和对称1.25/1.5/1.75%双轴邻域。旧中心50/1.5%只读，预定新关注点35/1.5%。检验更快趋势确认及带宽能否减少入场延误并保留风险控制。BTC固定15/30收盘通道＋前30日USDT成交额均值确认、倍率1。两币原始75/25，即2000USDT初始1500/500独立分仓；不重配资金或维持比例。','',
 'ETH决策i只用已闭合前日C[i−1]。严格C[i−1]>max(C[i−16:i−1])且float(C[i−1])>EMA[i−1]×(1+b)才进入；C[i−1]<min(C[i−31:i−1])或float(C[i−1])<EMA[i−1]×(1−b)即退出，退出优先；其他及相等延续desired。通道排除被比较收盘、参考止于i−2。EMA alpha=2/(span+1)，E[0]=float首个数据日收盘，逐日(1−alpha)E+alpha×float收盘、adjust=False、跨折不重置。没有延迟arming、止损、空头或新优化器。','',
 'BTC严格前日收盘突破排除该日前15收盘最高值，并且前日成交额≥前30个更早完整日成交额均值才入场；严格跌破前30收盘最低值退出，无低成交额自动退出。成交额均值正数、阈值相等可入，价格相等保持；Q由真实1440分钟quote_volume的Decimal和构成。其旧1500USDT实际结果只读，完整规则/spec/指纹及哈希随来源保存。','',
 '新ETH500USDT组件从OOS183现金和desired-cash开始，历史只暖机；六折持仓、现金、费用连续。组合直接将同预算、同UTC分钟/执行轴的已扣成本绝对NAV相加一次，不缩放、二次乘权重、归一化、转账或再平衡，也不平均单币收益率/Sharpe。两段历史独立本金。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}轮全文结论、7份Freqtrade文件、4个OOS源码及3技能；规范定义包含观察截止，历史挖掘配置原{prior['monitor_counts_before']['registered']}个、本轮新增28个。初始16按原始前16行及别名核对均有真实证据，无缺结果条目。",'',
 '## 三项验证与失败判据','',
 'Walk-forward已实际完成：2025和2026各03-18UTC00:01至09-14UTC00:01，180日、6个连续30日折；180日滚动历史、3日gap、purge0，无标签、模型或逐折/OOS拟合。前日收盘信号后按下一UTC00:01真实历史分钟开盘估计执行，终止含成本平仓。每场景259382个连续分钟收盘/执行节点计算整体回撤，不平均折回撤。已有历史反复复用，未称未触碰最终测试集。','',
 'Sensitivity已实际完成：EMA跨度和带宽同时变化，ETH与组合各年完整9格、1/2/3倍成本。sensitivity.csv含114场景，folds.csv含684折，其中84新场景/504新折及30只读旧场景/180旧折。全部负折、零折和淘汰保留；两份热图列收益、整体DD、Sharpe365，完整Calmar和成本在CSV/报告。相邻Sharpe差超过差异样本标准差2倍是描述性cliff，不是显著性、DSR/PBO或独立证据。','',
 'Costs已实际完成：每侧10bp手续费、1bp估计半点差、2bp滑点，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(订单预算/滞后20日quote ADV)冲击，四项同时×1/2/3，参与率≤0.001。Decimal28余额、PRICE不利tick、LOT下取整、NOTIONAL、前5完整分钟VWAP百分价格代理独立核对；取整额外记录。Oct1规则快照用于旧历史是假设，缺历史L2/TCA、排队/部分成交/延迟及真实IOC接单/容量保证。仅不加杠杆现货做多，资金费/借币不适用。','',
 '固定八门槛：各成本净正、1x≥4/6严格正折、3x整体DD≤25%、3x邻域净正≥60%、1x≥2往返、1x毛参考盈亏/执行成本≥2.5、无负现金/币数量、终止空仓。新组件和组合独立判断；旧格点的原criteria/status保持，不用本轮邻域把旧淘汰改为通过。','',
 f"失败条件计数{comparison['failure_counts']}。独立审计84新场景/21,788,088NAV点、7560个pandasEMA/排除当前收盘的因果决策和{summary['new_component_fills']}笔新ETH历史虚拟成交；30只读旧场景从同SHA真实价格与归档现金/数量复核，无重跑旧信号/订单。合成夹具仅为工程检查；6阶段实际执行、7阶段只读精确重放另存退出记录。",'',
 '## 预定35/1.5%与相同资金对照','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']);b=next(x for x in anchor_comparisons if x['focus']==c['name'])
 lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x整体分钟DD{z['3']['max_drawdown_pct']:.6f}%。相对同BTC＋纯ETH15/30通道：3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp；相对旧50/1.5%中心：收益差{b['return_differences_pp']['3']:.6f}pp、DD差{b['minute_DD3_difference_pp']:.6f}pp、全成本完整路径相同={b['all_cost_NAV_identical']}。")
lines+=['',f"新跨期合格参数中，相对匹配纯ETH通道的两期全成本收益和3x回撤均不差且至少一处改善者{comparison['new_qualified_pairs_jointly_nonworse_with_improvement']}组；相对旧50/1.5%中心同标准改善者{comparison['qualified_pairs_improving_old_center']}组。18条匹配比较、18条中心比较、各合格跨期判定及原中心来源见comparison.json。预定关注点共享的参数路径{comparison['new_parameters_sharing_predeclared_focus_paired_path']}，不算独立多次成功。",'',
 '## 全部组合：各年按1x净收益倒序','',
 '每行为BTC固定通道15/30＋均额30/倍率1，ETH通道15/30＋表中EMA跨度/对称带宽；原始75/25、独立初始1500/500USDT。','',
 '|年份|新/旧|ETH EMA日 / 带宽%|1x%|2x%|3x%|3x整体分钟DD%|正折1|成交/往返1|成本1USDT（手续费/冲击）|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(portfolios,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes']['1'];p=z['cost_parts_usdt'];lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['EMA_span_days']} / {100*c['EMA_symmetric_band']:g}|{z['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{z['executions']}/{z['round_trips']}|{z['cost_usdt']:.6f}（{p['fee']:.6f}/{p['impact']:.6f}）|{c['status']}|")
lines+=['','## 全部ETH独立500USDT组件','','|年份|新/旧|EMA日 / 带宽%|1x%|2x%|3x%|3x整体分钟DD%|正折1|成交/往返1|EMA入场合格日/180|EMA阻挡突破日|持仓日|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---|']
for c in sorted(leaves,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes']['1'];e=exposure[c['name']];lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['EMA_span_days']} / {100*c['EMA_symmetric_band']:g}|{z['net_return_pct']:.6f}|{c['scenes']['2']['net_return_pct']:.6f}|{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{z['executions']}/{z['round_trips']}|{e['EMA_eligible_days']}|{e['blocked_breakout_days']}|{e['invested_days']}|{c['status']}|")
lines+=['','## 敏感性与路径新颖性','','|年份/对象|3x净正率|完整门槛通过率|描述性cliff/12|最高收益3x的跨度/带宽|在网格边界|','|---|---:|---:|---:|---|---|']
for name,v in surfaces.items():lines.append(f"|{name}|{100*v['positive3_fraction']:.3f}%|{100*v['full_gate_pass_fraction']:.3f}%|{v['descriptive_cliff_flags']}|{v['best_return3_coordinates']}|{v['best_on_boundary']}|")
lines+=['',f"84新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见；去重{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径、{h['new_2026_combo_3x_paths_not_in_any_prior_report']}条未见2026三倍组合路径。{len(pairs)}组新跨期合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见合格完整跨期配对。路径签名数{comparison['path_signature_counts']}。参数不同仍是新配置，重复/新路径均不能当独立市场样本或稳定盈利证明。",'',
 '## 两类观察与复现','']
shadow=f"原SMA65/1%延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}只追加120个闭合分钟mark；旧{fr['prior_NAV_points']}点完整前缀保留，新{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟、{fr['cumulative_minutes']//1440}完整日。无新日决策/参考/成交/费用，下次2026-10-11UTC00:01；3x累计{legacy['net_return_pct']:.6f}%。原2027-03-31计划及SHA不变。这是后来取得真实bar的延迟重建，与十策略当时实际买卖报价的模拟资金前向业绩分开。"
lines+=[shadow,'',f"P01–P10保持第{paper['actual_quote_observations']}次实际报价观察（{paper['observed_at_utc']}），实际{paper['elapsed_seconds']/3600:.6f}小时、主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。未运行paper执行器或改变冻结资金/规则/现金/数量/desired/费用/已处理日线/账本。180天/六窗未成熟，DD限于真实报价快照采样。网页只读汇总既有证据，无重新部署或新定时任务。",'',f"离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`，7阶段精确复核夹具、旧缓存、原shadow、新历史、独立审计和登记；不HTTP、不写登记或paper账户。4份真实525600行分钟parquet、完整UTC日聚合、过滤规则快照、源spec/报告/订单及代码SHA见data_manifest.json和report.json。大行情/NPY留忽略data，轻量充分证据入Git。",'',
 '本轮按冻结9格全部保存正收益、负折、零折和淘汰；结果不用于当前样本继续扩参或更换P01–P10。未来若再研究边界需另轮事前固定与登记。现有两段历史反复使用，正收益和绝对门槛合格不代表独立最终验证或稳定实盘盈利。','',
 '## 一手资料','',
 '[Binance公开历史数据](https://github.com/binance/binance-public-data)、[现货市场数据REST](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)、[官方过滤规则源文档](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)于本轮读取。两个过滤规则网页路由返回工具Internal Error，已从官方源仓库读取，访问记录见source_access.json/sources.json；没有行情执行故障。数据单位/过滤语义由官方资料支持，成本估计及盈利结论来自本地真实执行研究。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原SMA冻结账户延迟分钟mark\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：ETH通道15/30＋EMA35/50/65日×对称1.25/1.5/1.75%，BTC固定通道15/30＋均额30/倍率1，原75/25（1500/500USDT）。14新ETH＋14新组合/84场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰；{len(pairs)}新跨期组合参数合格。旧4ETH＋4父组合及2BTC/30场景只读。预定35/1.5%三倍2025/2026为"+'/'.join(f"{c['scenes']['3']['net_return_pct']:.6f}%/DD{c['scenes']['3']['max_drawdown_pct']:.6f}%"for c in focus)+f"；对匹配纯ETH通道两期联合改善{comparison['new_qualified_pairs_jointly_nonworse_with_improvement']}组，对旧50/1.5%中心联合改善{comparison['qualified_pairs_improving_old_center']}组。84场景{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见、未见跨期配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}；两期历史复用和边界/cliff限制保留。84新/30旧场景、21,788,088新NAV点、7560因果决策及168新ETH历史成交独立审计；31定义reserve/finish和7阶段重放完成。原shadow续120mark至03:00、累计11699分钟/11709点、8完整日，无新决策/成交，下次Oct11UTC00:01；固定paper29不变。初始16实际证据完整，全部负折和旧淘汰保留。\n"
(T/'README_entry.md').write_text(entry);readme=R/'research/automation/README.md';marker='## 最近完成的轮次\n\n';assert readme.read_text()==prior['read_automation_README']['text'];assert marker in readme.read_text();readme.write_text(readme.read_text().replace(marker,marker+entry+'\n',1))
print(json.dumps({'historical_configs':28,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'new_qualified_pairs':len(pairs),'joint_nonworse_vs_pure_ETH':comparison['new_qualified_pairs_jointly_nonworse_with_improvement'],'joint_nonworse_vs_old_center':comparison['qualified_pairs_improving_old_center'],'path_signatures':comparison['path_signature_counts'],'surfaces':surfaces},ensure_ascii=False))
