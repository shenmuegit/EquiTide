"""Summarize actual fixed-batch results, funded controls and legacy daily continuity."""
from pathlib import Path
from collections import Counter
from decimal import Decimal as D
import csv,gzip,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());h=json.loads((T/'history_paths.json').read_text());prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()))
cs=r['configs'];grid=r['plan']['grid'];summary=r['summary'];fresh=[c for c in cs.values()if c['is_new']];parents=[c for c in cs.values()if c['role']=='combination']
external={ref['name']:json.loads((R/ref['report']).read_text())['configs'][ref['name']]for ref in r['plan']['read_only_comparator_refs']}
lookup={**cs,**external};comparisons=[]
funds=lambda weights:[int(D(2000)*D(str(w)))for w in weights]
for c in parents:
 same=next(x for x in parents if x['year']==c['year']and x['raw_weights']==c['raw_weights']and x['BTC_minimum_volume_ratio']==1)
 old=next(x for x in external.values()if x['year']==c['year'])
 for kind,o in [('SAME_WEIGHT_RATIO1',same),('OLD_N30_HALF',old)]:
  comparisons.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':o['name'],'comparator_is_new':bool(o.get('is_new',False))if o['name']in cs else False,'config_raw_weights':c['raw_weights'],'control_raw_weights':o['raw_weights'],'config_component_capitals':funds(c['raw_weights']),'control_component_capitals':funds(o['raw_weights']),'same_total_capital_usdt':2000,'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in summary['new_both_periods_passed_combination_pairs']:
 for kind in('SAME_WEIGHT_RATIO1','OLD_N30_HALF'):
  rows=[next(x for x in comparisons if x['config']==n and x['kind']==kind)for n in pair];returns=[v for x in rows for v in x['return_differences_pp'].values()];dds=[x['minute_DD3_difference_pp']for x in rows]
  pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in returns)and all(v<=0 for v in dds)and(any(v>0 for v in returns)or any(v<0 for v in dds)),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');cells=[c for c in cs.values()if c['year']==year and(c.get('asset')==role or c['role']==role)];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['BTC_minimum_volume_ratio'],c['BTC_initial_weight']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[name]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/len(cells),'cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'edges':len(sens['adjacent_edges']),'best_return3_coordinates':coords,'best_on_boundary':any(w in(.45,.55)or ratio in(1,1.2)for ratio,w in coords)}
comparison={'report_sha256':sha(T/'report.json'),'comparisons':comparisons,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_same_weight_ratio1':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='SAME_WEIGHT_RATIO1'),'jointly_improved_pairs_vs_old_N30_half':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_N30_HALF'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'scope':'Primarysamefundingratio1controls may be new registered actualtrials;secondary oldN30/r1raw50/50 has same total2000 but different assetexposure. Alloldsourcecriteria/status preserved;no untouchedholdout claim.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_initial_weight','BTC_minimum_volume_ratio','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_initial_weight'],c['BTC_minimum_volume_ratio'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
for role,filename in [('combination','sensitivity.png'),('BTC','sensitivity_BTC.png')]:
 fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
 for row,year in enumerate(('2025','2026')):
  cells={(c['BTC_initial_weight'],c['BTC_minimum_volume_ratio']):c for c in cs.values()if c['year']==year and(c['role']==role or c.get('asset')==role)}
  for col,(metric,label)in enumerate([('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]):
   ax=axes[row,col];matrix=np.array([[cells[weight,ratio]['scenes']['3'][metric]for ratio in grid['BTC_minimum_volume_ratio']]for weight in grid['BTC_initial_weight']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
   for i,weight in enumerate(grid['BTC_initial_weight']):
    for j,ratio in enumerate(grid['BTC_minimum_volume_ratio']):ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if cells[weight,ratio]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
   ax.set(xticks=range(3),xticklabels=grid['BTC_minimum_volume_ratio'],yticks=range(3),yticklabels=['45%','50%','55%'],xlabel='Minimum BTC quote-turnover ratio (N40)',ylabel='Original initial BTC allocation',title=year+' | '+label);fig.colorbar(im,ax=ax,fraction=.035)
 title='BTC N40 channel15/30: volume ratio x own900/1000/1100USDT funding'if role=='BTC'else'BTC N40 channel15/30 x original allocation / fixed ETH EMA30 +/-1.25%'
 fig.suptitle(title+'\nRaw45/55,50/50,55/45 of2000USDT | P/R=annual gates | repeated histories',fontsize=14);fig.savefig(T/filename,dpi=130);plt.close(fig)
focus=sorted([c for c in parents if c['BTC_minimum_volume_ratio']==1.1 and c['BTC_initial_weight']==.45],key=lambda c:c['year']);fr=r['plan']['forward_resume'];state=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/state['last_observation_id']/'summary.json').read_text())
lines=['# BTC成交额倍率 × 初始资金分配：N40与ETH EMA30固定','',f"30个新历史定义：16个组件（14BTC、2ETH）＋14个年度组合，90成本场景真实执行；1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(summary['new_both_periods_passed_combination_pairs'])}组新参数跨期合格。旧8组件＋4父组合/36场景、2个额外旧N30中心只读。33个新定义含原shadow截止均先reserve，实际执行和独立审计后finish。",'',
 '## 事前假设、资金和完整规则','',
 '前轮N40/r1.1原50/50降低2026组合回撤，同时略降收益；本轮事前固定N40与ETH通道15/30＋EMA30对称1.25%，联合测试BTC最低成交额倍率1/1.1/1.2 × 原BTC权重45%/50%/55%。每组2000USDT，原BTC/ETH分别900/1100、1000/1000、1100/900。预定关注r1.1与45/55，检验风险、收益及正折数的权衡；不在本轮OOS追加择优参数、优化器或更改失败门槛。','',
 'BTC在决策i只看已闭合C[i−1]：严格高于max(C[i−16:i−1])且Q[i−1]≥r×mean(Q[i−41:i−1])、参考均值>0才入场。两参考范围止于i−2，均排除被比较收盘/成交额。C[i−1]<min(C[i−31:i−1])退出优先，成交额不足本身不退出；价格相等保持，成交额阈值相等可入。Q是1440个真实UTC分钟quote_volume的Decimal和。','',
 'ETH固定：EMA alpha=2/31、首数据日float收盘为种子、逐日递推adjust=False、跨折不重置。C[i−1]上破排除自身的15日收盘通道且float(C[i−1])>EMA[i−1]×1.0125入场；下破排除自身的30日通道或float(C[i−1])<EMA[i−1]×0.9875退出优先，其他保持。新900USDT ETH组件真实重新模拟；旧1000/1100USDT仅只读。','',
 '每个新资金/规则组件以自己的900/1000/1100USDT运行Decimal数量、手续费及预算相关冲击；不缩放旧1000USDT曲线。父组合将已经扣成本的对应绝对NAV相加一次，不二次加权、归一化、转账、维持比例或再平衡。所有组件从OOS183现金/desired-cash开始、暖机不生成交易，跨六折连续。原始权重和旧淘汰状态全部保留。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}份全文结论、7份Freqtrade结果、4个OOS源码、3技能及任务/监控说明。初始16实际证据均完整，缺结果0。历史试验从{prior['monitor_counts_before']['registered']}新增30，观察截止不计入策略挖掘。",'',
 '## 三项验证与失败条件','',
 'Walk-forward：2025、2026各03-18UTC00:01至09-14UTC00:01，180日/六个连续30日折；180日滚动历史、3日gap、purge0，无标签/逐折拟合/优化。前日闭合信息后在下一UTC00:01真实历史分钟开盘参考执行，终止平仓计成本。每场景259382分钟收盘/执行点计算连续OOS整体回撤，不平均折回撤。两段历史已反复研究，不是未触碰最终留出。','',
 'Sensitivity：完整倍率×初始资金分配联合9格/年；BTC和父组合均双轴，ETH只是资金规模单轴，EMA规则不调。126场景/756折全部保存，其中90新场景/540折、36旧场景/216折。全部净收益、完整DD、Sharpe365、Calmar、成本与正负/零折见CSV和热图。相邻Sharpe差超过差异样本标准差2倍仅作描述性cliff，非统计显著性、PBO/DSR或独立验证。','',
 'Costs：每侧10bp手续费、1bp估计半点差、2bp滑点，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(实际订单预算/滞后20日quote ADV)冲击，全部同倍率×1/2/3。成本ADV固定20日，最大参与率0.001；Decimal28、不利PRICE tick、LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理独立复核。Oct1过滤快照对历史是估计，缺历史L2/TCA、队列、延迟、部分成交或真实IOC接单证明。现货仅多，资金费/借币不适用。','',
 '固定八门槛：全成本净正、1x≥4/6严格正折、3x整体分钟DD≤25%、3x邻域净正≥60%、1x≥2往返、毛参考盈亏/成本≥2.5、无负余额、终止空仓。组件和父组合独立判断，旧criteria/status不追溯修改。失败或负折仍完整登记保存。','',
 f"独立审计90新场景/23,344,380NAV点、8640个因果决策（BTC7560、ETH1080）和{summary['new_component_fills']}笔新组件历史成交。36旧场景同源完整分钟NAV验证。失败条件计数{comparison['failure_counts']}。6个实际阶段、7个只读重放阶段退出码留档；工程合成夹具不充当收益。旧缓存预检沿用1000USDT/6父组合的窄断言失败，已按冻结资金与4旧父组合修正，并保留initial_failure日志及cache_recovery_repair.json；未重登记、改冻结计划或重跑旧信号/成交。",'',
 '## 预定关注r1.1、原45/55与对照','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']and x['kind']=='SAME_WEIGHT_RATIO1');b=next(x for x in comparisons if x['config']==c['name']and x['kind']=='OLD_N30_HALF')
 lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x完整DD{z['3']['max_drawdown_pct']:.6f}%。同45/55倍率1对照新评估={a['comparator_is_new']}，3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp；相对旧N30/r1原50/50，3x收益差{b['return_differences_pp']['3']:.6f}pp、DD差{b['minute_DD3_difference_pp']:.6f}pp。状态{c['status']}。")
lines+=['',f"新跨期合格参数中，所有成本收益和3x回撤两期均不差且至少一处改善：相对同原权重倍率1为{comparison['jointly_improved_pairs_vs_same_weight_ratio1']}组，相对旧N30/r1原50/50为{comparison['jointly_improved_pairs_vs_old_N30_half']}组。36条年度比较及{len(pairs)}条配对判定见comparison.json。主对照可能是本轮已reserve的新实际配置；次对照只匹配2000总资金，资产敞口不同，不冒充纯参数对照。",'',
 '## 全部年度组合（每年按1x净收益倒序）','','|年份|新/旧|BTC倍率|原BTC/ETH|初始BTC/ETH USDT|1x%|2x%|3x%|3x完整DD%|正折1|成交/往返1|成本1（手续费/冲击）|状态|','|---|---|---:|---|---|---:|---:|---:|---:|---|---|---|---|']
for c in sorted(parents,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];a=z['1'];cp=a['cost_parts_usdt'];weights='/'.join(f'{w*100:g}'for w in c['raw_weights']);ff='/'.join(map(str,funds(c['raw_weights'])))
 lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['BTC_minimum_volume_ratio']}|{weights}|{ff}|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{a['cost_usdt']:.6f}（{cp['fee']:.6f}/{cp['impact']:.6f}）|{c['status']}|")
lines+=['','## 全部组件与资金/失败条件','','|年份|币种|新/旧|资金USDT|BTC倍率或ETH EMA|1x%|2x%|3x%|3x完整DD%|正折1|往返1|状态/失败条件|','|---|---|---|---:|---|---:|---:|---:|---:|---|---:|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda c:(c['year'],c['asset'],c['capital_usdt'],c['name'])):
 z=c['scenes'];a=z['1'];parameter=c['BTC_minimum_volume_ratio']if c['asset']=='BTC'else'30±1.25%';failed=[k for k,v in c['criteria'].items()if not v]
 lines.append(f"|{c['year']}|{c['asset']}|{'新'if c['is_new']else'旧只读'}|{c['capital_usdt']}|{parameter}|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['round_trips']}|{c['status']}/{failed}|")
lines+=['','## 平台、边界与重复路径','','|年份/对象|3x净正率|完整门槛通过率|cliff/邻边|最高3x收益坐标倍率/BTC权重|在边界|','|---|---:|---:|---|---|---|']
for name,z in surfaces.items():lines.append(f"|{name}|{100*z['positive3_fraction']:.3f}%|{100*z['full_gate_pass_fraction']:.3f}%|{z['cliff_flags']}/{z['edges']}|{z['best_return3_coordinates']}|{z['best_on_boundary']}|")
lines+=['',f"90新场景中{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，去重{h['distinct_new_scene_paths_not_in_prior']}种未见单场景。{len(summary['new_both_periods_passed_combination_pairs'])}合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见完整跨期路径。参数新颖不等于独立市场样本；全部旧淘汰、重复路径、边界与大量历史选择偏差披露，不能宣称稳定实盘盈利。",'',
 '## 既有同期基准与现金','','原SMA65±1%原75/25与持有原50/50均为已有真实2000USDT历史，只读背景；SMA及部分新组合敞口不同。现金为无收益USDT理论零线，不是新回测。','','|年份|旧基准/原权重|1x%|2x%|3x%|3x完整分钟DD%|','|---|---|---:|---:|---:|---:|']
for bg in r['read_only_background'].values():
 z=bg['scenes'];lines.append(f"|{bg['year']}|{bg['kind']} / {bg['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 原冻结SMA日线续接与十策略隔离','']
fd=f['daily_decisions_by_asset'];af=json.loads((T/'audit_forward.log').read_text());legacy=f['configs']['forward_snapshot_combo']['scenes']['3']
shadow=f"原SMA65/1%75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}保留{fr['prior_NAV_points']}点精确前缀，增加120闭合分钟mark和1个原UTC00:01决策参考，现{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟、9完整日。BTC/ETH决策分别{fd['BTC']['action']}/{fd['ETH']['action']}；6份成本账户原日线决策独立核对，新增组件成交{af['new_component_executions']}笔。各65个完整UTC日/64个前轮重叠日一致，SMA/成本滞后样本、时序、资金与完整轴审计。下一决策{json.loads((T/'forward_state.json').read_text())['next_daily_decision_utc']}，原2027-03-31终止安排保持，3x累计{legacy['net_return_pct']:.6f}%。沿用原浮点数量/成本模型，不补改LOT/当前过滤保证；后来取得的00:01历史分钟参考是延迟shadow，不是实时可成交或十策略当时实时报价业绩。"
lines+=[shadow,'',f"P01–P10保持第{paper['actual_quote_observations']}次真实报价观察，UTC {paper['observed_at_utc']}，实际{paper['elapsed_seconds']/3600:.6f}小时，主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT；两段旧缺口与{100*paper['coverage_fraction']:.6f}%计数/时长覆盖代理保持，非连续分钟覆盖。未运行paper执行器，不改冻结规则、2000本金、数量、现金、desired、已处理日线、成本或交易ID，不补单；其回撤仅实际报价采样。180天/六窗未成熟，未宣称验证通过。网页只读汇总，无重部署或新建定时任务。",'',
 f"离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`，7阶段只读精确核对，不HTTP、不写登记/账户。四份真实525600行分钟parquet、完整日聚合、成交、过滤快照及代码SHA见data_manifest.json/report.json；原shadow真实公开GET输入及延迟见forward_report.json。大行情/NPY留忽略data，全部正负收益/折与失败保留。",'',
 '固定批次不按OOS继续扩参或更改门槛；未来另轮预登记，保留重复使用历史与选择偏差。','',
 '## 一手资料','',
 '[Binance公开历史数据](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[官方现货REST源码文档](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md)、[官方过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)本轮成功读取，时间见sources.json。仅支持字段/时间/过滤语义；成本估计和收益来自本地真实执行研究。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA日线续接（延迟shadow）\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：BTC N40倍率1/1.1/1.2 × 原BTC权重45/50/55%联合双轴，ETH通道15/30＋EMA30±1.25%固定；实际900/1100、1000/1000、1100/900USDT独立分仓，不缩放旧NAV。16新组件＋14组合/90场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(summary['new_both_periods_passed_combination_pairs'])}新跨期参数合格；8旧组件＋4父组合/36场景及2旧N30中心只读。对同权重倍率1联合改善{comparison['jointly_improved_pairs_vs_same_weight_ratio1']}组，旧N30/r1原50/50{comparison['jointly_improved_pairs_vs_old_N30_half']}组。90场景{h['new_scenes_already_in_any_prior_report']}曾见/{h['new_scenes_not_in_any_prior_report']}未见，合格未见配对{h['qualified_cross_period_pairs_not_in_any_prior_report']}种。90场景/23,344,380NAV点、8640因果决策、{summary['new_component_fills']}新成交独立审计；33定义reserve/finish，6实际阶段与7只读重放完成。旧缓存断言恢复保留。原SMA跨Oct11UTC00:01续120mark+1参考至01:00，13019分钟/13030点，6日线决策独立审计/新成交{af['new_component_executions']}；原浮点冻结规则不改，不是实时盘。paper39及两段旧缺口/95.452090%覆盖代理保持，180天未成熟。初始16证据完整，负折、淘汰、边界、重复历史与选择偏差保留。\n"
(T/'README_entry.md').write_text(entry);p=R/'research/automation/README.md';marker='## 最近完成的轮次\n\n';assert p.read_text()==prior['read_automation_README']['text'];p.write_text(p.read_text().replace(marker,marker+entry+'\n',1))
print(json.dumps({'new_configs':30,'passed':len(summary['passed']),'rejected':len(summary['rejected']),'qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'joint_improvement_same_weight':comparison['jointly_improved_pairs_vs_same_weight_ratio1'],'joint_improvement_old_center':comparison['jointly_improved_pairs_vs_old_N30_half'],'focus':[{'year':c['year'],'return3':c['scenes']['3']['net_return_pct'],'DD3':c['scenes']['3']['max_drawdown_pct'],'status':c['status']}for c in focus]}))
