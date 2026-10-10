"""Document completed funding/span grid,all rejected folds and predeclared controls."""
from pathlib import Path
from collections import Counter
import csv,gzip,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));cs=r['configs'];plan=r['plan'];grid=plan['grid'];fresh=[c for c in cs.values()if c['is_new']];parents=[c for c in cs.values()if c['role']=='combination'];comparison=[]
for c in parents:
 old=next(x for x in parents if x['year']==c['year']and x['EMA_span_days']==c['EMA_span_days']and x['BTC_initial_weight']==.525)
 center=next(x for x in parents if x['year']==c['year']and x['EMA_span_days']==30 and x['BTC_initial_weight']==.525)
 for kind,control in [('SAME_RULES_OLD52_5_47_5',old),('OLD30DAY_52_5_47_5_CENTER',center)]:
  comparison.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':control['name'],'new_raw_weights':c['raw_weights'],'control_raw_weights':control['raw_weights'],'same_total_capital_usdt':2000,'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-control['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-control['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==control['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in r['summary']['new_both_periods_passed_combination_pairs']:
 for kind in ('SAME_RULES_OLD52_5_47_5','OLD30DAY_52_5_47_5_CENTER'):
  rows=[next(x for x in comparison if x['config']==name and x['kind']==kind)for name in pair];returns=[v for x in rows for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in rows]
  pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in returns)and all(v<=0 for v in dd)and(any(v>0 for v in returns)or any(v<0 for v in dd)),'strict_return_gain_both_years':all(all(v>0 for v in x['return_differences_pp'].values())for x in rows),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for group,sens in r['sensitivity'].items():
 year,role=group.split('_');cells=[c for c in cs.values()if c['year']==year and(c.get('asset')==role or c['role']==role)];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['EMA_span_days'],c['BTC_initial_weight']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[group]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/len(cells),'descriptive_cliff_flags':sum(x['cliff_flag_2sd']for x in sens['adjacent_edges']),'adjacent_edges':len(sens['adjacent_edges']),'best_return3_coordinates':coords,'best_on_boundary':any(w in(.475,.525)or n in(30,35)for n,w in coords)}
proof={'report_sha256':sha(T/'report.json'),'comparisons':comparison,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_same_rules':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='SAME_RULES_OLD52_5_47_5'),'jointly_improved_pairs_vs_old_center':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD30DAY_52_5_47_5_CENTER'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'interpretation':'Same total2000USDT,deliberately different asset initial funding. Changed capital receives new cost/LOT/impact simulation,not oldNAV rescaling. Reused histories/paths are not independent market evidence.'};(T/'comparison.json').write_text(json.dumps(proof,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_initial_weight','EMA_span_days','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_initial_weight'],c['EMA_span_days'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
for role,output in [('combination','sensitivity.png'),('ETH','sensitivity_ETH.png')]:
 fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
 for row,year in enumerate(('2025','2026')):
  cells={(c['EMA_span_days'],c['BTC_initial_weight']):c for c in cs.values()if c['year']==year and(c.get('asset')==role or c['role']==role)}
  for col,(metric,label)in enumerate([('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
   ax=axes[row,col];matrix=np.array([[cells[n,w]['scenes']['3'][metric]for w in grid['BTC_initial_weight']]for n in grid['EMA_span_days']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
   for i,n in enumerate(grid['EMA_span_days']):
    for j,w in enumerate(grid['BTC_initial_weight']):ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if cells[n,w]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
   ax.set(xticks=range(3),xticklabels=['47.5/52.5','50/50','52.5/47.5'],yticks=range(3),yticklabels=grid['EMA_span_days'],xlabel='Declared BTC/ETH original weights (%)',ylabel='ETH recursive EMA span (days)',title=year+' | '+label);bar=fig.colorbar(im,ax=ax,fraction=.035);bar.ax.ticklabel_format(style='plain',useOffset=False,axis='y')
 fig.suptitle(('BTCvolume30-ratio1 + ETHchannel15/30 EMA +/-1.25%'if role=='combination'else'ETHchannel15/30 EMA +/-1.25% funded at1050 / 1000 / 950USDT')+'\nP/R=annual gates | fixed raw initial allocation,no rebalance | both histories reused',fontsize=14);fig.savefig(T/output,dpi=130);plt.close(fig)
summary=r['summary'];focus=sorted([c for c in parents if c['BTC_initial_weight']==.5 and c['EMA_span_days']==30],key=lambda c:c['year']);fr=plan['forward_resume'];legacy=f['configs']['forward_snapshot_combo']['scenes']['3'];ps=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/ps['last_observation_id']/'summary.json').read_text())
lines=['# 初始分仓比例 × ETH EMA确认跨度','',f"28个新历史定义：4个BTC资金规模组件＋12个ETH组件＋12个年度组合，共84成本场景实际执行。1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}；{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(summary['new_both_periods_passed_combination_pairs'])}个新参数组合分别通过2025/2026历史门槛。8个原1050/950USDT组件＋6个旧52.5/47.5组合/42成本场景只读；原状态与门槛保留。共31新定义含3原shadow截止均先reserve后实算并finish。",'',
'## 预先固定的研究与资金','',
'上一轮45/55组合未过2026正折门槛，52.5/47.5仍合格。本轮事前固定中间比例47.5/52.5、50/50及旧52.5/47.5，联合EMA跨度检验折数边界及风险代价：BTC固定15/30收盘通道＋前30个更早完整UTC日USDT成交额均值、倍率1；ETH固定15/30通道＋EMA30/33/35日，对称1.25%。原BTC/ETH比例明确给定47.5/52.5、50/50、52.5/47.5；总本金2000USDT，分别初始950/1050、1000/1000、1050/950。预定关注EMA30、50/50，全部9格在看新结果前冻结。','',
'改变资金规模的BTC与ETH组件分别重新执行Decimal成本、tick、LOT和冲击核算，不缩放旧1050/950净值，不把已扣成本路径二次乘权重。旧52.5/47.5每格只读。各组件在共同分钟/执行时间轴上按已扣成本绝对NAV相加一次，无归一化、资金转移、自动维持比例或再平衡。两年各自独立本金，不连接当作360天未见样本。','',
'BTC：决策i只用前日C[i−1]，严格超过max(C[i−16:i−1])且Q[i−1]≥mean(Q[i−31:i−1])、参考均值>0才入场；严格跌破min(C[i−31:i−1])即退出。通道及Q参考都排除被比较日、止于i−2。成交额为1440个真实UTC分钟quote_volume的Decimal和；阈值相等可进入，低成交额本身不退出，价格相等保持desired，退出优先。','',
'ETH：C[i−1]>max(C[i−16:i−1])且float(C[i−1])>EMA[i−1]×1.0125才入场；C[i−1]<min(C[i−31:i−1])或float(C[i−1])<EMA[i−1]×0.9875退出，退出优先；其他与相等保持。EMA alpha=2/(span+1)、E[0]=float首数据日收盘，逐日递推、adjust=False、跨折不重置。前日收盘只暖指标，OOS183初始现金/desired-cash，不生成暖机交易。','',
f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}轮完整中文结论、7份Freqtrade结果、4个OOS源码、3指定技能与任务/监控说明。初始16按原始首16行及别名核验全部有真实证据，无缺结果配置。历史挖掘试验由{prior['monitor_counts_before']['registered']}增加28；持续观察截止不计入策略挖掘。",'',
'## 三项验证与固定门槛','',
'Walk-forward实算：2025、2026各03-18UTC00:01至09-14UTC00:01，180日、6个连续30日折；180日滚动历史、3日gap、purge0，无标签、模型或逐折/OOS拟合。信号仅用可得闭合前日数据，成交参考下一UTC00:01真实历史分钟开盘；期末平仓扣成本。每场景259382个连续分钟收盘/执行节点计算整体回撤，不平均逐折回撤。已反复使用的两段历史仍是开发/验证历史，未称独立最终测试。','',
'Sensitivity实算：EMA30/33/35 × 原47.5/52.5、50/50、52.5/47.5同时变动，ETH和组合各年9格；BTC指标不变，3个资金规模仅做成本/参与率检验，不伪称新的双参数指标探索。126成本场景、756折全部保存，其中84新场景/504新折、42旧场景/252旧折；含全部负折、零折和淘汰。两张热图列收益、完整分钟DD、Sharpe365，Calmar/成本/成交见CSV与报告。相邻Sharpe差超过其差异样本标准差2倍仅作描述性cliff，不是显著性、DSR/PBO或独立证据。','',
'Costs实算：每侧10bp手续费、1bp估计半点差、2bp滑点，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(预算/滞后20日quote ADV)冲击，成本项同时×1/2/3，参与率≤0.001。Decimal28余额、PRICE不利tick、LOT下取整、NOTIONAL、前5完整分钟VWAP百分价格代理独立审计，取整成本另记。Oct1规则快照用于旧历史是假设，缺历史L2、TCA、队列、延迟及部分成交/IOC接单保证；仅现货做多，资金费和借币不适用。','',
'八门槛保持：各成本净正、1x≥4/6严格正折、3x完整DD≤25%、3x邻域净正≥60%、1x≥2往返、1x毛参考盈亏/执行成本≥2.5、无负现金/币、终止空仓。新组件与组合分别判断，旧criteria/status不改。','',
f"失败条件计数{proof['failure_counts']}。独立复核84新场景/21,788,088NAV点、6480个ETH pandasEMA因果决策、2160个BTC排除当日成交额因果决策和{summary['new_component_fills']}笔新组件历史成交；42只读旧场景从同SHA行情/归档现金数量复核，无旧信号/交易重跑。6阶段实际执行与7阶段只读重放保存退出码。",'',
'## 预定关注点及既有对照','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparison if x['config']==c['name']and x['kind']=='SAME_RULES_OLD52_5_47_5');lines.append(f"{c['year']} EMA30、原50/50：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x完整分钟DD{z['3']['max_drawdown_pct']:.6f}%，1x正折{c['positive_folds_1x']}/6。相对同指标旧52.5/47.5：3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp。")
lines+=['',f"{len(summary['new_both_periods_passed_combination_pairs'])}组新跨期合格参数中，相对同指标52.5/47.5两期各成本收益与3x回撤均不差且至少一处改善者{proof['jointly_improved_pairs_vs_same_rules']}组；相对旧EMA30/52.5/47.5中心同标准改善者{proof['jointly_improved_pairs_vs_old_center']}组。全36条年度对照与{len(pairs)}条跨期判定见comparison.json。各对照总本金相同但初始资产资金有意不同，不能声称相同资产敞口。",'',
'## 所有年度组合，按1x收益倒序','','BTC均为通道15/30＋30日成交额确认倍率1，ETH通道15/30＋表中EMA、对称1.25%。','','|年份|新/旧|EMA日|原BTC/ETH比例|1x%|2x%|3x%|3x完整分钟DD%|正折1|成交/往返1|成本1USDT（手续费/冲击）|状态|','|---|---|---:|---|---:|---:|---:|---:|---:|---|---|---|']
for c in sorted(parents,key=lambda x:(x['year'],-x['scenes']['1']['net_return_pct'],x['name'])):
 z=c['scenes'];a=z['1'];p=a['cost_parts_usdt'];weights='/'.join(f'{100*w:g}'for w in c['raw_weights']);lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['EMA_span_days']}|{weights}|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{a['cost_usdt']:.6f}（{p['fee']:.6f}/{p['impact']:.6f}）|{c['status']}|")
lines+=['','## 所有独立资金组件','','|年份|币种|新/旧|本金USDT|ETH EMA日|1x%|2x%|3x%|3x完整DD%|正折1|成交/往返1|状态|','|---|---|---|---:|---|---:|---:|---:|---:|---:|---|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda x:(x['year'],x['asset'],x['capital_usdt'],x['EMA_span_days']or 0)):
 z=c['scenes'];a=z['1'];lines.append(f"|{c['year']}|{c['asset']}|{'新'if c['is_new']else'旧只读'}|{c['capital_usdt']}|{c['EMA_span_days']}|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{c['status']}|")
lines+=['','## 敏感性、路径与选择偏差','','|年份/对象|3x净正率|完整门槛通过率|cliff/邻边|最高3x收益坐标 EMA日/BTC初始比|在边界|','|---|---:|---:|---|---|---|']
for name,s in surfaces.items():lines.append(f"|{name}|{100*s['positive3_fraction']:.3f}%|{100*s['full_gate_pass_fraction']:.3f}%|{s['descriptive_cliff_flags']}/{s['adjacent_edges']}|{s['best_return3_coordinates']}|{s['best_on_boundary']}|")
lines+=['',f"84新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见；去重{h['distinct_new_scene_paths_not_in_prior']}种未见单场景路径，{len(summary['new_both_periods_passed_combination_pairs'])}合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见完整配对。完整SHA查重保留。资金或参数变化属于新具体配置，路径变化仍不增加独立市场样本；历史上多次探索导致选择偏差，不报告未计算的显著性或稳定实盘收益。",'',
'## 同期已存基准与现金','','原SMA65±1%使用75/25；原持有使用50/50且敞口不同，仅作背景。都只读取已执行证据，不新增回测或登记。现金为无收益USDT理论零线。','','|年份|旧基准/原权重|1x净收益%|2x%|3x%|3x完整分钟DD%|','|---|---|---:|---:|---:|---:|']
for b in r['read_only_background'].values():
 z=b['scenes'];lines.append(f"|{b['year']}|{b['kind']} / {b['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 观察隔离与复现','']
shadow=f"原SMA65/1%75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}只追加120闭合分钟mark；旧{fr['prior_NAV_points']}点精确前缀，新{fr['total_NAV_points']}点、{fr['cumulative_minutes']}分钟/{fr['cumulative_minutes']//1440}完整日。无新日线决策、参考节点、成交或费用，下次Oct11UTC00:01。3x累计{legacy['net_return_pct']:.6f}%；原冻结计划及2027-03-31终止安排不变。该延迟真实bar重建不是十策略当时实时报价的业绩。"
lines+=[shadow,'',f"P01–P10仍为第{paper['actual_quote_observations']}次真实报价观察，UTC {paper['observed_at_utc']}、实际{paper['elapsed_seconds']/3600:.6f}小时；主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT，覆盖代理估计{100*paper['coverage_fraction']:.6f}%、两段原缺口保留，达到冻结95%覆盖单项门槛，原缺口未补齐，其他180天/六窗条件未成熟。未运行paper执行器、不改其冻结计划/现金/数量/desired/费用/已处理日线/交易ID，不补单。180天/6窗未成熟，回撤仅限已存实际报价采样。网页只读汇总，无重新部署/新定时任务。",'',f"离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`。7阶段核对合成夹具、旧现金数量缓存、原shadow、新资金回测、独立因果/账务审计及登记；不HTTP、不写登记或paper账户。四份真实525600行分钟parquet及完整日聚合、规则快照、源spec、归档订单和代码哈希见data_manifest.json/report.json；大行情/NPY留忽略data，所有新定义/正负折/淘汰保留入Git。",'',
'预登记查重与合成夹具仅属工程检查；新的历史成交、资金核算及收益均在reserve成功后实际执行，并在独立审计后finish。','',
'研究参数保持本批次冻结；不依据本轮OOS继续扩参或替换固定模拟组。后续若研究边界必须另轮事前登记，并承认历史重复使用。','',
'## 一手资料','','[Binance公开历史数据](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[现货市场公开REST](https://developers.binance.com/en/docs/catalog/core-trading-spot-trading/api/rest-api/market)、[官方过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)于本轮读取；访问记录在sources.json。资料仅支持数据/接口/规则语义；成本估计、资金规模效应及收益结论来自本地实际回测证据。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA延迟分钟估值\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：BTC通道15/30＋成交额N30/r1，ETH通道15/30＋EMA30/33/35±1.25%；原47.5/52.5、50/50、52.5/47.5（总2000USDT）联合双轴。新资金规模重新核算，不缩放旧NAV。16新组件＋12新组合/84场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(summary['new_both_periods_passed_combination_pairs'])}新跨期参数合格；8旧组件＋6旧组合/42场景只读。相对同指标旧52.5/47.5两期联合改善{proof['jointly_improved_pairs_vs_same_rules']}组、旧30日52.5/47.5中心{proof['jointly_improved_pairs_vs_old_center']}组；84场景{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，未见合格配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}种。84新场景/21,788,088NAV点、8640因果决策、{summary['new_component_fills']}组件成交独立审计；31定义reserve/finish、6实际阶段和7只读重放完成。原shadow续120mark至19:00、12659分钟/12669点，无新决策/成交；paper36及其两段缺口/95.068315%覆盖代理分类保持，单项跨95%不代表180天资格。初始16实际证据完整，重复历史、边界及选择偏差限制保留。\n"
(T/'README_entry.md').write_text(entry);p=R/'research/automation/README.md';marker='## 最近完成的轮次\n\n';assert p.read_text()==prior['read_automation_README']['text'];p.write_text(p.read_text().replace(marker,marker+entry+'\n',1))
print(json.dumps({'new_configs':28,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'jointly_improved_vs_same_rules':proof['jointly_improved_pairs_vs_same_rules'],'jointly_improved_vs_center':proof['jointly_improved_pairs_vs_old_center'],'focus':[{k:c[k]for k in('name','year','raw_weights','EMA_span_days')}|{'return3':c['scenes']['3']['net_return_pct'],'DD3':c['scenes']['3']['max_drawdown_pct']}for c in focus]}))
