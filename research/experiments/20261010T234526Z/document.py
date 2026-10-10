"""Describe completed volume-window/ratio results and read-only evidence."""
from pathlib import Path
from collections import Counter
import csv, gzip, hashlib, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text())
h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
cs=r['configs'];grid=r['plan']['grid'];summary=r['summary']
fresh=[c for c in cs.values()if c['is_new']];parents=[c for c in cs.values()if c['role']=='combination']
comparisons=[]
for c in parents:
 old=next(x for x in parents if x['year']==c['year']and x['BTC_volume_lookback_days']==c['BTC_volume_lookback_days']and x['BTC_minimum_volume_ratio']==1)
 center=next(x for x in parents if x['year']==c['year']and x['BTC_volume_lookback_days']==30 and x['BTC_minimum_volume_ratio']==1)
 for kind,o in [('SAME_N_RATIO1',old),('N30_RATIO1_CENTER',center)]:
  comparisons.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':o['name'],'same_raw_weights':[.5,.5],'same_funded_capitals':[1000,1000],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in summary['new_both_periods_passed_combination_pairs']:
 for kind in('SAME_N_RATIO1','N30_RATIO1_CENTER'):
  xs=[next(x for x in comparisons if x['config']==n and x['kind']==kind)for n in pair]
  rv=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs]
  pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');cells=[c for c in cs.values()if c['year']==year and(c.get('asset')==role or c['role']==role)]
 best=max(c['scenes']['3']['net_return_pct']for c in cells)
 coords=[[c['BTC_volume_lookback_days'],c['BTC_minimum_volume_ratio']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[name]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/len(cells),'cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'edges':len(sens['adjacent_edges']),'best_return3_coordinates':coords,'best_on_boundary':None if role=='ETH'else any(n in(20,40)or ratio in(.9,1.1)for n,ratio in coords)}
comparison={'report_sha256':sha(T/'report.json'),'comparisons':comparisons,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_same_N_ratio1':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='SAME_N_RATIO1'),'jointly_improved_pairs_vs_center':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='N30_RATIO1_CENTER'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'scope':'Matched1000/1000USDT,raw50/50,ETHEMA30/1.25percent fixed. PrimarysameNratio1,secondaryN30ratio1. Repeated histories/duplicate paths do not add independent evidence.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_volume_lookback_days','BTC_minimum_volume_ratio','EMA_span_days','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_volume_lookback_days'],c['BTC_minimum_volume_ratio'],c['EMA_span_days'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
for group,filename in [('combination','sensitivity.png'),('BTC','sensitivity_BTC.png')]:
 fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
 for row,year in enumerate(('2025','2026')):
  cells={(c['BTC_minimum_volume_ratio'],c['BTC_volume_lookback_days']):c for c in cs.values()if c['year']==year and(c['role']==group or c.get('asset')==group)}
  for col,(metric,label)in enumerate([('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
   ax=axes[row,col];matrix=np.array([[cells[ratio,n]['scenes']['3'][metric]for n in grid['BTC_volume_lookback_days']]for ratio in grid['BTC_minimum_volume_ratio']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
   for i,ratio in enumerate(grid['BTC_minimum_volume_ratio']):
    for j,n in enumerate(grid['BTC_volume_lookback_days']):ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if cells[ratio,n]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
   ax.set(xticks=range(3),xticklabels=grid['BTC_volume_lookback_days'],yticks=range(3),yticklabels=grid['BTC_minimum_volume_ratio'],xlabel='BTC disjoint quote-volume reference days',ylabel='Minimum quote-turnover ratio',title=year+' | '+label);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
 title='BTC channel15/30 volume N x ratio | component1000USDT'if group=='BTC'else'BTC channel15/30 volume N x ratio / fixed ETH channel15/30 EMA30 +/-1.25%'
 fig.suptitle(title+'\nRaw50/50 original1000/1000USDT | ratio1 archived | P/R=annual gates | histories reused',fontsize=14);fig.savefig(T/filename,dpi=130);plt.close(fig)
focus=sorted([c for c in parents if c['BTC_volume_lookback_days']==30 and c['BTC_minimum_volume_ratio']==1.1],key=lambda c:c['year'])
fr=r['plan']['forward_resume'];ps=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/ps['last_observation_id']/'summary.json').read_text())
lines=['# BTC成交额参考窗口 × 入场倍率：固定ETH与原50/50资金','',
 f"24个新历史配置：12个BTC组件＋12个年度组合，72成本场景真实执行；1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(summary['new_both_periods_passed_combination_pairs'])}组新参数组合跨2025/2026通过。旧6个BTC倍率1组件、2个ETH与6个父组合共14定义/42场景只读，旧状态/criteria保持。27个新定义含3个原shadow截止均先reserve、实际执行、独立审计再finish。",'',
 '## 事前假设、完整规则与资金','',
 '前轮只改变成交额窗口时2026路径不变、2025的30日表现为局部峰。本轮事前声明BTC成交额参考N20/30/40 × 最低倍率r0.9/1/1.1完整9格，价格通道15/30；固定ETH通道15/30＋EMA30对称1.25%，每组2000USDT原50/50，即BTC1000/ETH1000。预定关注N30/r1.1：更强流动性确认可能减少假突破，也可能错过收益或减少往返。没有在本轮OOS上择优追加参数、止损、优化器或改门槛。','',
 'BTC决策i只用已闭合C[i−1]：C[i−1]>max(C[i−16:i−1])且Q[i−1]≥r×mean(Q[i−N−1:i−1])、均值>0入场；C[i−1]<min(C[i−31:i−1])退出优先。价格与成交额参考均排除被比较日、止于i−2。成交额不足本身不平仓，价格相等保持、成交额阈值相等可入；desired从OOS183空仓开始连续保留。Q为完整1440个真实UTC分钟quote_volume的Decimal和，不是base币量。','',
 'ETH固定EMA30：alpha=2/31、E[0]=float数据首日收盘、逐日递推、adjust=False、跨折不重置。C[i−1]上破前15日收盘通道且float(C[i−1])>EMA[i−1]×1.0125入场；下破前30日收盘通道或float(C[i−1])<EMA[i−1]×0.9875退出优先，其他保持。两份1000USDT源组件只读，无新的ETH信号或成交。','',
 '新BTC倍率0.9/1.1各在1000USDT重新模拟。倍率1的六份BTC、固定ETH及六份旧父组合使用同SHA归档与完整分钟价格复核；不重跑旧信号/成交或覆盖旧criteria/status。父组合将已经扣成本的1000/1000绝对NAV在共同时间轴相加一次，不缩放、二次乘权重、归一化、转账、维持比例或再平衡。暖机不产生OOS前持仓/收益。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}轮全文结论、7份Freqtrade结果与4个OOS源码、3技能及任务/监控说明。初始16按原始首16行逐项核对实际证据，全部有结果。历史试验从{prior['monitor_counts_before']['registered']}新增24；观察截止单列，不混入策略挖掘。",'',
 '## 三项验证、失败判据与限制','',
 'Walk-forward实际执行：2025、2026各03-18UTC00:01至09-14UTC00:01，180日/6个连续30日折，180日滚动历史、3日gap、purge0；固定指标无标签、逐折拟合或优化。只用前日已闭合信息，于次UTC00:01真实历史分钟开盘参考执行、终止平仓扣成本。每场景259382个分钟收盘与执行节点计算连续OOS整体回撤，不平均折回撤。两段历史已反复研究，不能称未触碰最终留出。','',
 'Sensitivity实际执行：BTC N20/30/40 × r0.9/1/1.1联合双轴，BTC组件和父组合各9格/年；ETH只是固定只读点，不声称新ETH敏感性。114场景/684折全部保存：72新场景/432折、42旧场景/252折。所有变体净收益、完整DD、Sharpe365、Calmar和成本见CSV及两张热图；相邻Sharpe差超过差异样本标准差2倍为描述性cliff，不是统计显著性、PBO/DSR或独立证据。','',
 'Costs实际执行：每侧10bp手续费、1bp估计半点差、2bp滑点，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(预算/滞后20日quote ADV)冲击，各项同倍率×1/2/3。成本ADV固定20日，不随信号N/r改变。最大参与率0.001、Decimal28、PRICE不利tick、LOT下取整、NOTIONAL与前5个完整分钟VWAP百分价格代理独立审计。Oct1过滤快照对历史是估计假设，缺历史L2、TCA、队列、延迟、部分成交或IOC接单保证；现货只做多，资金费/借币不适用。','',
 '固定八门槛：所有成本净正、1x至少4/6严格正折、3x整体分钟DD≤25%、3x邻域净正≥60%、1x至少2往返、毛参考盈亏/执行成本≥2.5、无负余额、终止空仓。未通过任何一项即淘汰并完整保留；旧ETH2026的淘汰状态保持，父组合独立按组合门槛判断。','',
 f"独立审计72新场景/18,675,504NAV点、6480个BTC因果决策及{summary['new_component_fills']}笔新BTC历史成交；新ETH信号/成交0，真实订单0。42旧场景同源哈希复核。失败条件计数{comparison['failure_counts']}；6阶段实际执行与7阶段离线精确重放均保留日志/退出码。合成夹具不是收益证据。",'',
 '## 预定关注N30/r1.1与同资金旧对照','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']and x['kind']=='SAME_N_RATIO1')
 lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x完整DD{z['3']['max_drawdown_pct']:.6f}%。相对同N旧倍率1：3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp，完整全成本NAV相同={a['all_cost_NAV_identical']}。")
lines+=['',f"新跨期合格参数中，相对同N旧倍率1，两年所有成本收益不差、3x回撤不差且至少一处改善者{comparison['jointly_improved_pairs_vs_same_N_ratio1']}组；相对旧N30/r1中心同标准改善{comparison['jointly_improved_pairs_vs_center']}组。36条年度比较与{len(pairs)}条跨期判定见comparison.json。原资金、ETH规则、执行轴和成本一致。",'',
 '## 全部年度组合（每年按主成本后收益倒序）','','|年份|新/旧|BTC N/r|固定ETH EMA|原BTC/ETH|1x%|2x%|3x%|3x完整DD%|正折1|成交/往返1|成本1USDT（手续费/冲击）|状态|','|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|']
for c in sorted(parents,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];a=z['1'];cp=a['cost_parts_usdt'];lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['BTC_volume_lookback_days']}/{c['BTC_minimum_volume_ratio']}|30±1.25%|50/50|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{a['cost_usdt']:.6f}（{cp['fee']:.6f}/{cp['impact']:.6f}）|{c['status']}|")
lines+=['','## 全部1000USDT组件与淘汰理由','','|年份|币种|新/旧|BTC N/r或ETH EMA|1x%|2x%|3x%|3x完整DD%|正折1|往返1|状态/失败条件|','|---|---|---|---|---:|---:|---:|---:|---|---:|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda c:(c['year'],c['asset'],c['name'])):
 z=c['scenes'];a=z['1'];p=f"{c['BTC_volume_lookback_days']}/{c['BTC_minimum_volume_ratio']}"if c['asset']=='BTC'else'30±1.25%';failed=[key for key,value in c['criteria'].items()if not value]
 lines.append(f"|{c['year']}|{c['asset']}|{'新'if c['is_new']else'旧只读'}|{p}|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['round_trips']}|{c['status']}/{failed}|")
lines+=['','## 敏感性平台、边界与重复路径','','|年份/对象|3x净正率|完整门槛通过率|cliff/邻边|最高3x收益坐标N/r|在边界|','|---|---:|---:|---|---|---|']
for name,s in surfaces.items():lines.append(f"|{name}|{100*s['positive3_fraction']:.3f}%|{100*s['full_gate_pass_fraction']:.3f}%|{s['cliff_flags']}/{s['edges']}|{s['best_return3_coordinates']}|{s['best_on_boundary']}|")
lines+=['',f"72新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，去重{h['distinct_new_scene_paths_not_in_prior']}种未见单场景；{len(summary['new_both_periods_passed_combination_pairs'])}合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见完整跨期路径。参数新颖不等于独立市场样本。全部历史选择、重复路径、局部峰/边界和选择偏差披露，不宣称独立最终验证或稳定实盘盈利。",'',
 '## 同期已存基准与现金','','原SMA65±1%75/25和持有50/50均为既有真实2000USDT结果，只读参考；SMA敞口不同。现金为无收益USDT理论零线，不是新回测或合格候选。','','|年份|旧基准/原权重|1x%|2x%|3x%|3x完整分钟DD%|','|---|---|---:|---:|---:|---:|']
for bg in r['read_only_background'].values():
 z=bg['scenes'];lines.append(f"|{bg['year']}|{bg['kind']} / {bg['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 两类持续账户与复现','']
legacy=f['configs']['forward_snapshot_combo']['scenes']['3']
shadow=f"原SMA65/1%75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}仅追加120个闭合分钟mark，旧{fr['prior_NAV_points']}点精确前缀，新{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟、8完整日。无新日决策、参考节点、成交或成本；下一原冻结日决策Oct11UTC00:01，原2027-03-31终止安排保持。3x累计{legacy['net_return_pct']:.6f}%。后取真实分钟的延迟重建不能当十策略当时实时报价前向业绩。"
lines+=[shadow,'',f"P01–P10保持第{paper['actual_quote_observations']}次真实报价观察，UTC {paper['observed_at_utc']}，实际{paper['elapsed_seconds']/3600:.6f}小时，主账户总净值{paper['totals_by_cost']['1']['NAV_usdt']}USDT。两段旧缺口与{100*paper['coverage_fraction']:.6f}%计数/时长覆盖代理完整保留；95%单项满足不等于连续分钟覆盖或180天/六窗成熟。未运行paper执行器、不改冻结规则/本金/现金/数量/desired/费用/交易ID、不补单。paper回撤只按已存真实报价采样；监控只读，无重新部署或新建定时任务。",'',
 f"离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`；7阶段只读精确重放，不HTTP、不写登记或paper账户。真实四份525600行分钟parquet、完整UTC日聚合、成交归档、过滤快照与源代码SHA见data_manifest.json/report.json。大行情/NPY在忽略data中；所有正负折、零折及淘汰完整保存。",'',
 '本轮不按结果继续扩参或改变失败条件。后续探索另轮事前声明，保留两段历史反复使用与选择偏差。','',
 '## 一手资料','',
 '[Binance公开历史数据](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[官方现货REST源码文档](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md)、[官方过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)本轮成功读取，访问时间见sources.json/source_access.json。资料支持字段、时间与过滤语义；成本估计和收益来自本地真实执行研究。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA延迟分钟估值\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：原50/50（1000/1000USDT），BTC通道15/30成交额N20/30/40 × 倍率0.9/1/1.1双轴；ETH通道15/30＋EMA30±1.25%固定只读。12新BTC＋12年度组合/72场景真实执行，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(summary['new_both_periods_passed_combination_pairs'])}新跨期参数合格；8组件＋6父组合/42场景只读。相对同N旧倍率1联合改善{comparison['jointly_improved_pairs_vs_same_N_ratio1']}组，相对N30/r1中心{comparison['jointly_improved_pairs_vs_center']}组；72场景{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，合格配对未见{h['qualified_cross_period_pairs_not_in_any_prior_report']}种。72场景/18,675,504NAV点、6480因果决策、{summary['new_component_fills']}新BTC成交独立审计；27定义reserve/finish、6实际阶段及7只读重放完成。原shadow续120mark至23:00、12899分钟/12909点，无新决策/成交；paper38及两段旧缺口/95.331147%覆盖代理保持，180天未成熟。初始16实际证据完整，旧淘汰/重复历史/边界/选择偏差保留。\n"
(T/'README_entry.md').write_text(entry);p=R/'research/automation/README.md';marker='## 最近完成的轮次\n\n'
assert p.read_text()==prior['read_automation_README']['text'];p.write_text(p.read_text().replace(marker,marker+entry+'\n',1))
print(json.dumps({'new_configs':24,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'joint_improvements_matched':comparison['jointly_improved_pairs_vs_same_N_ratio1'],'joint_improvements_center':comparison['jointly_improved_pairs_vs_center'],'focus':[{'year':c['year'],'return3':c['scenes']['3']['net_return_pct'],'DD3':c['scenes']['3']['max_drawdown_pct']}for c in focus]}))
