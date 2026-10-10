"""Describe completed BTCvolume x ETHEMA test;sourcecontrols and oldrejects stay read-only."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));cs=r['configs'];grid=r['plan']['grid'];fresh=[c for c in cs.values()if c['is_new']];parents=[c for c in cs.values()if c['role']=='combination'];comparisons=[]
for c in parents:
 old=next(x for x in parents if x['year']==c['year']and x['BTC_volume_lookback_days']==30 and x['EMA_span_days']==c['EMA_span_days']);center=next(x for x in parents if x['year']==c['year']and x['BTC_volume_lookback_days']==30 and x['EMA_span_days']==30)
 for kind,o in [('SAME_ETH_BTC30',old),('BTC30_ETH30_CENTER',center)]:comparisons.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':o['name'],'same_raw_weights':[.5,.5],'same_funded_capitals':[1000,1000],'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 for kind in('SAME_ETH_BTC30','BTC30_ETH30_CENTER'):
  xs=[next(x for x in comparisons if x['config']==n and x['kind']==kind)for n in pair];rv=[v for x in xs for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in xs];pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');cells=[c for c in cs.values()if c['year']==year and(c.get('asset')==role or c['role']==role)];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['BTC_volume_lookback_days'],c['EMA_span_days']]for c in cells if c['scenes']['3']['net_return_pct']==best];surfaces[name]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/len(cells),'cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'edges':len(sens['adjacent_edges']),'best_return3_coordinates':coords,'best_on_boundary':any(n in(20,40)or s in(30,35)for n,s in coords)}
comparison={'report_sha256':sha(T/'report.json'),'comparisons':comparisons,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_same_ETH_BTC30':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='SAME_ETH_BTC30'),'jointly_improved_pairs_vs_center':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='BTC30_ETH30_CENTER'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'scope':'Equal initial1000/1000USDT,raw50/50,no rebalance. New BTCN20/40 uses actualnew simulations;allETH andBTC30 archivedpaths read-only. Repeated histories/duplicatepaths do not add independent evidence.'};(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_volume_lookback_days','EMA_span_days','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_volume_lookback_days'],c['EMA_span_days'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for row,year in enumerate(('2025','2026')):
 cells={(c['EMA_span_days'],c['BTC_volume_lookback_days']):c for c in parents if c['year']==year}
 for col,(metric,label)in enumerate([('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[row,col];matrix=np.array([[cells[s,n]['scenes']['3'][metric]for n in grid['BTC_volume_lookback_days']]for s in grid['EMA_span_days']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
  for i,s in enumerate(grid['EMA_span_days']):
   for j,n in enumerate(grid['BTC_volume_lookback_days']):ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if cells[s,n]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
  ax.set(xticks=range(3),xticklabels=grid['BTC_volume_lookback_days'],yticks=range(3),yticklabels=grid['EMA_span_days'],xlabel='BTC disjoint quote-volume reference days',ylabel='ETH recursive EMA span (days)',title=year+' | '+label);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
fig.suptitle('BTCchannel15/30 + quote-volume ratio1 / ETHchannel15/30 EMA +/-1.25%\nRaw50/50 original1000/1000USDT | P/R=annualgates | bothhistories reused',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
fig,axes=plt.subplots(2,3,figsize=(15,8),layout='constrained')
for row,year in enumerate(('2025','2026')):
 cells={c['BTC_volume_lookback_days']:c for c in cs.values()if c['year']==year and c.get('asset')=='BTC'}
 for col,(metric,label)in enumerate([('net_return_pct','3x net return %'),('max_drawdown_pct','3x whole-minute NAV DD %'),('sharpe_365','3x daily Sharpe (365)')]):
  ax=axes[row,col];xx=grid['BTC_volume_lookback_days'];yy=[cells[n]['scenes']['3'][metric]for n in xx];ax.plot(xx,yy,'o-',color='#174f78')
  for n,y in zip(xx,yy):ax.annotate(f'{y:.4f}'+(' P'if cells[n]['status']=='passed'else' R'),(n,y),textcoords='offset points',xytext=(0,10),ha='center',fontsize=10)
  ax.set(xticks=xx,xlabel='BTC disjoint quote-volume reference days',ylabel=label,title=year+' | '+label);ax.margins(x=.18,y=.3);ax.grid(axis='y',alpha=.2)
fig.suptitle('BTCchannel15/30 + disjoint quote-turnover confirmation | fixed1000USDT\nN30read-only,N20/40new | componentoneaxis insidejointportfolio test',fontsize=14);fig.savefig(T/'sensitivity_BTC.png',dpi=130);plt.close(fig)
summary=r['summary'];focus=sorted([c for c in parents if c['BTC_volume_lookback_days']==20 and c['EMA_span_days']==30],key=lambda c:c['year']);fr=r['plan']['forward_resume'];ps=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/ps['last_observation_id']/'summary.json').read_text())
lines=['# 固定50/50：BTC成交额参考窗口 × ETH EMA跨度','',f"16个新历史定义：4个BTC N20/40组件＋12个年度组合，共48成本场景真实执行；1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(summary['new_both_periods_passed_combination_pairs'])}组新参数组合两期通过。旧2BTC N30、6ETH、6个N30父组合共14定义/42场景只读；旧ETH淘汰仍保留。共19新定义含原shadow截止全部先reserve后计算、独立审计并finish。",'',
'## 事前假设、规则与资金','',
'前轮47.5/52.5因2026正折不足失败，50/50合格。本轮在新结果前固定原50/50，即每个2000USDT组合初始BTC1000、ETH1000，事前声明BTC成交额参考20/30/40日与ETH EMA30/33/35日联合9格，对称带宽固定1.25%，关注BTC20/ETH30。检验同资金下入场流动性确认速度与ETH趋势速度的作用；没有本轮OOS择优、优化器、额外止损/arming或更换固定模拟组。','',
'BTC决策i仅用已闭合C[i−1]，严格高于max(C[i−16:i−1])且Q[i−1]≥mean(Q[i−N−1:i−1])、均值>0才入场，N按预设20/30/40；价格和成交额参考都排除被比较日、止于i−2。严格C[i−1]<min(C[i−31:i−1])退出，低成交额本身不退出，阈值相等可入、价格相等保持、退出优先。Q为1440个真实UTC分钟quote_volume的Decimal和，不是base币成交量。','',
'ETH：C[i−1]>max(C[i−16:i−1])且float(C[i−1])>EMA[i−1]×1.0125入场；C[i−1]<min(C[i−31:i−1])或float(C[i−1])<EMA[i−1]×0.9875退出，退出优先，其他及相等保持desired。EMA alpha=2/(span+1)、E[0]=float首数据日收盘、逐日递推、adjust=False、跨折不重置。该六份1000USDT源组件只读，不生成新的ETH信号或成交。','',
'新BTC组件从OOS183现金/desired-cash开始、暖机不生成持仓或交易，六折连续。组合在共同分钟/执行轴上将已扣成本1000/1000绝对净值相加一次，保留原50/50，不缩放或二次乘权重、不归一化、转账、维持比例或再平衡。新BTC N20/40重新模拟；BTC N30与ETH及旧父组合从同SHA归档/行情复核，不重跑旧信号或旧成交。','',
f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}轮全文结论、7份Freqtrade结果、4个OOS源码、3技能与任务/监控说明。初始16按原始首16行及别名检查均有真实证据，无缺结果配置。历史挖掘从{prior['monitor_counts_before']['registered']}新增16；观察截止不计入策略挖掘。",'',
'## 三项验证与固定八门槛','',
'Walk-forward实际执行：2025、2026各03-18UTC00:01至09-14UTC00:01，180日、6个连续30日折，180日滚动历史、3日gap、purge0；固定指标无标签、模型或逐折/OOS拟合。前日数据可得后用次UTC00:01真实历史分钟开盘参考，终止平仓扣成本。每场景259382个连续分钟收盘/执行节点计算整体回撤，不平均折回撤。两段既有历史反复使用，不能叫未触碰最终测试。','',
'Sensitivity实际执行：BTC N20/30/40 × ETH EMA30/33/35完整9格，每年原资金和成本口径相同。组件各自单轴，组合联合两轴；ETH仅只读原结果。90成本场景/540折全部保存，其中48新场景/288新折、42旧场景/252旧折；含负折、零折和所有旧淘汰。热图及BTC组件图列收益、完整DD、Sharpe365，Calmar与成本见CSV。相邻Sharpe差超过差异样本标准差2倍仅是描述性cliff，不是显著性、PBO/DSR或独立最终证据。','',
'Costs实际执行：每侧10bp手续费、1bp估计半点差、2bp滑点，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(预算/滞后20日quote ADV)冲击，全部成本同时×1/2/3；成本ADV固定20日，不随信号N改变。参与率≤0.001，Decimal28余额、PRICE不利tick、LOT下取整、NOTIONAL、前5完整分钟VWAP百分价格代理独立审计，取整成本另记。Oct1过滤快照用于旧历史是假设，缺历史L2、TCA、队列、延迟、部分成交或真实IOC接单保证。现货仅做多，资金费/借币不适用。','',
'固定八门槛：各成本净正、1x≥4/6严格正折、3x完整DD≤25%、3x邻域净正≥60%、1x≥2往返、1x毛参考盈亏/执行成本≥2.5、无负现金/币、终止空仓。新BTC/组合独立判断；旧格点的源criteria/status不改，旧ETH2026正折不足仍是淘汰。','',
f"独立审计48新场景/12,450,336NAV点、2160个排除被比较日成交额的BTC因果决策与{summary['new_component_fills']}笔新BTC历史成交；新ETH信号/成交0。42旧场景依据原现金/数量与同SHA真实分钟数据复核。新配置失败条件计数{comparison['failure_counts']}。6阶段实际执行、7阶段只读精确重放均保留退出码和日志；合成夹具不充当收益。",'',
'## 预定BTC20/ETH30与同资金旧对照','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']and x['kind']=='SAME_ETH_BTC30');lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x完整分钟DD{z['3']['max_drawdown_pct']:.6f}%。相对同ETH30、BTC N30：3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp；完整全成本路径相同={a['all_cost_NAV_identical']}。")
lines+=['',f"新跨期合格参数中，对相同ETH、旧BTC N30两期全成本收益及3x回撤均不差且至少一处改善者{comparison['jointly_improved_pairs_vs_same_ETH_BTC30']}组；相对旧BTC30/ETH30中心同标准改善{comparison['jointly_improved_pairs_vs_center']}组。36条年度比较与{len(pairs)}条配对判定见comparison.json；初始资金、原权重、执行轴和成本完全匹配。",'',
'## 全部年度组合，按1x收益倒序','','|年份|新/旧|BTC成交额N日|ETH EMA日|原BTC/ETH比例|1x%|2x%|3x%|3x完整DD%|正折1|成交/往返1|成本1USDT（手续费/冲击）|状态|','|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(parents,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];a=z['1'];p=a['cost_parts_usdt'];lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['BTC_volume_lookback_days']}|{c['EMA_span_days']}|50/50|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{a['cost_usdt']:.6f}（{p['fee']:.6f}/{p['impact']:.6f}）|{c['status']}|")
lines+=['','## 所有1000USDT组件，旧状态保留','','|年份|币种|新/旧|BTC N / ETH EMA日|1x%|2x%|3x%|3x完整DD%|正折1|成交/往返1|状态|','|---|---|---|---|---:|---:|---:|---:|---:|---|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda c:(c['year'],c['asset'],c['BTC_volume_lookback_days']or c['EMA_span_days'])):
 z=c['scenes'];a=z['1'];p=c['BTC_volume_lookback_days']if c['asset']=='BTC'else c['EMA_span_days'];lines.append(f"|{c['year']}|{c['asset']}|{'新'if c['is_new']else'旧只读'}|{p}|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{c['status']}|")
lines+=['','## 敏感性与路径新颖性','','|年份/对象|3x净正率|完整门槛通过率|cliff/邻边|最高3x收益坐标 BTC N/ETH EMA|在边界|','|---|---:|---:|---|---|---|']
for name,s in surfaces.items():lines.append(f"|{name}|{100*s['positive3_fraction']:.3f}%|{100*s['full_gate_pass_fraction']:.3f}%|{s['cliff_flags']}/{s['edges']}|{s['best_return3_coordinates']}|{s['best_on_boundary']}|")
lines+=['',f"48新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见；去重{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径。{len(summary['new_both_periods_passed_combination_pairs'])}合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见完整配对。参数新颖不等于市场样本独立；已做大量历史选择，重复路径/选择偏差和边界限制保留，不声称独立最终验证或稳定实盘盈利。",'',
'## 同期既有基准与现金','','只读既有真实SMA65±1%（原75/25）和持有（原50/50），总本金均2000USDT。SMA敞口不同，只作背景；不运行新基准或登记。现金为无收益USDT理论零线。','','|年份|旧基准/原权重|1x净收益%|2x%|3x%|3x完整分钟DD%|','|---|---|---:|---:|---:|---:|']
for b in r['read_only_background'].values():
 z=b['scenes'];lines.append(f"|{b['year']}|{b['kind']} / {b['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 两类观察与复现','']
legacy=f['configs']['forward_snapshot_combo']['scenes']['3'];shadow=f"原SMA65/1%75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}只追加120闭合分钟mark，旧{fr['prior_NAV_points']}点精确前缀，新{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟、8完整日。无新日决策、参考节点、成交或成本；次决策Oct11UTC00:01。3x累计{legacy['net_return_pct']:.6f}%，原冻结计划与2027-03-31终止安排不变。后来获取真实bar的延迟重建不是十策略当时实时报价业绩。"
lines+=[shadow,'',f"P01–P10保持第{paper['actual_quote_observations']}次真实报价观察，UTC {paper['observed_at_utc']}，实际{paper['elapsed_seconds']/3600:.6f}小时、主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。两段旧缺口与{100*paper['coverage_fraction']:.6f}%计数/时长缺口覆盖代理保留；满足95%覆盖单项不表示连续分钟覆盖或180天/六窗资格。未运行paper执行器，不改冻结规则/本金/现金/数量/desired/成本/已处理日线/交易ID，不补单。其回撤仅按保存的真实报价采样。网页只读汇总，无重新部署或新定时任务。",'',f"离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`，7阶段只读精确核对，不HTTP、不写登记或paper账户。四份真实525600行分钟parquet、完整日聚合、交易归档、过滤快照、源规则及代码SHA见data_manifest.json/report.json。大行情/NPY留忽略data，全部正负折/旧淘汰/新结果保留入Git。",'',
'本轮固定批次不继续按OOS扩参或修改门槛。未来探索必须另轮事前登记，并保留历史反复使用与选择偏差的限制。','',
'## 一手资料及访问恢复','','[Binance公开历史数据](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[官方现货REST源码文档](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md)、[官方过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)本轮读取。开发者站市场文档首次访问超时，改读官方同源REST文档成功；失败与恢复见source_access.json。资料只支持字段/时间/过滤语义，成本估计与盈利结论来自本地真实执行研究。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA延迟分钟估值\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：原50/50（1000/1000USDT），BTC通道15/30＋成交额N20/30/40倍率1 × ETH通道15/30＋EMA30/33/35±1.25%联合双轴。4新BTC＋12新组合/48场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(summary['new_both_periods_passed_combination_pairs'])}新跨期参数合格。旧2BTC N30＋6ETH＋6父组合/42场景只读，无新ETH信号/成交。对同资金同ETH旧BTC30两期联合改善{comparison['jointly_improved_pairs_vs_same_ETH_BTC30']}组，旧BTC30/ETH30中心{comparison['jointly_improved_pairs_vs_center']}组；48场景{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，未见合格配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}种。48新场景/12,450,336NAV点、2160因果决策、{summary['new_component_fills']}新BTC成交独立审计；19定义reserve/finish、6实际阶段及7只读重放完成。原shadow续120mark至21:00、12779分钟/12789点，无新决策/成交；paper37及两段缺口/95.202975%覆盖代理保持，180天未成熟。初始16实际证据完整；旧淘汰、重复历史、边界与选择偏差保留。\n"
(T/'README_entry.md').write_text(entry);p=R/'research/automation/README.md';marker='## 最近完成的轮次\n\n';assert p.read_text()==prior['read_automation_README']['text'];p.write_text(p.read_text().replace(marker,marker+entry+'\n',1))
print(json.dumps({'new_configs':16,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'joint_improvements_matched':comparison['jointly_improved_pairs_vs_same_ETH_BTC30'],'joint_improvements_center':comparison['jointly_improved_pairs_vs_center'],'focus':[{'year':c['year'],'return3':c['scenes']['3']['net_return_pct'],'DD3':c['scenes']['3']['max_drawdown_pct']}for c in focus]}))
