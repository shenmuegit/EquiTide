"""Describe every frozen paired-exit result and matching read-only controls."""
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
external={ref['name']:json.loads((R/ref['report']).read_text())['configs'][ref['name']]for ref in r['plan']['read_only_comparator_refs']};comparisons=[]
funds=lambda weights:[int(D(2000)*D(str(w)))for w in weights]
for c in parents:
 same=next(x for x in parents if x['year']==c['year']and x['BTC_exit_lookback_days']==x['ETH_exit_lookback_days']==30)
 old=next(x for x in external.values()if x['year']==c['year'])
 for kind,o in [('OLD_EXIT30_30',same),('OLD_N30_HALF',old)]:
  comparisons.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':o['name'],'comparator_is_new':False,'config_raw_weights':c['raw_weights'],'control_raw_weights':o['raw_weights'],'config_component_capitals':funds(c['raw_weights']),'control_component_capitals':funds(o['raw_weights']),'same_total_capital_usdt':2000,'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in summary['new_both_periods_passed_combination_pairs']:
 for kind in('OLD_EXIT30_30','OLD_N30_HALF'):
  rows=[next(x for x in comparisons if x['config']==n and x['kind']==kind)for n in pair];returns=[v for x in rows for v in x['return_differences_pp'].values()];dds=[x['minute_DD3_difference_pp']for x in rows]
  pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in returns)and all(v<=0 for v in dds)and(any(v>0 for v in returns)or any(v<0 for v in dds)),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');cells=[c for c in cs.values()if c['year']==year and(c.get('asset')==role or c['role']==role)];best=max(c['scenes']['3']['net_return_pct']for c in cells)
 coords=[[c['BTC_exit_lookback_days'],c['ETH_exit_lookback_days']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[name]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'full_gate_pass_fraction_preserving_old_status':sum(c['status']=='passed'for c in cells)/len(cells),'cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'edges':len(sens['adjacent_edges']),'best_return3_exit_coordinates':coords,'best_on_boundary':any(any(v in(20,40)for v in xy if v is not None)for xy in coords)}
comparison={'report_sha256':sha(T/'report.json'),'comparisons':comparisons,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_old_exit30_30':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_EXIT30_30'),'jointly_improved_pairs_vs_old_N30_half':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_N30_HALF'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'scope':'Primary oldexit30/30 controls match raw55/45,own1100/900USDT,N40/r1.1,ETHEMA30+/-1.25%. SecondaryoldN30/r1raw50/50 has same total2000 butdifferentassetexposure/volumeparameters. Alloldcriteria/status preserved;no untouchedholdout claim.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_initial_weight','BTC_exit_lookback_days','ETH_exit_lookback_days','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_initial_weight'],c['BTC_exit_lookback_days'],c['ETH_exit_lookback_days'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
metrics=[('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]
fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
for row,year in enumerate(('2025','2026')):
 cells={(c['BTC_exit_lookback_days'],c['ETH_exit_lookback_days']):c for c in parents if c['year']==year}
 for col,(metric,label)in enumerate(metrics):
  ax=axes[row,col];matrix=np.array([[cells[bx,ex]['scenes']['3'][metric]for bx in grid['BTC_exit_lookback_days']]for ex in grid['ETH_exit_lookback_days']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
  for i,ex in enumerate(grid['ETH_exit_lookback_days']):
   for j,bx in enumerate(grid['BTC_exit_lookback_days']):ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if cells[bx,ex]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
  ax.set(xticks=range(3),xticklabels=grid['BTC_exit_lookback_days'],yticks=range(3),yticklabels=grid['ETH_exit_lookback_days'],xlabel='BTC prior-close channel exit days (N40/r1.1)',ylabel='ETH prior-close channel exit days (EMA30 +/-1.25%)',title=year+' | '+label);fig.colorbar(im,ax=ax,fraction=.035)
fig.suptitle('Paired channel exits | original BTC55%/ETH45% of2000USDT,own1100/900\nEntry15 unchanged | P/R=annual gates;old30/30 statuses retained | repeated histories',fontsize=14);fig.savefig(T/'sensitivity.png',dpi=130);plt.close(fig)
fig,axes=plt.subplots(2,3,figsize=(15,8),layout='constrained')
for row,year in enumerate(('2025','2026')):
 cells=sorted([c for c in cs.values()if c['year']==year and c.get('asset')=='BTC'],key=lambda c:c['BTC_exit_lookback_days'])
 for col,(metric,label)in enumerate(metrics):
  ax=axes[row,col];xs=[c['BTC_exit_lookback_days']for c in cells];ys=[c['scenes']['3'][metric]for c in cells];ax.plot(xs,ys,'o-',color='#176159');ax.grid(alpha=.2)
  for x,y,c in zip(xs,ys,cells):ax.annotate(f'{y:.3f} '+('P'if c['status']=='passed'else'R'),(x,y),xytext=(0,8),textcoords='offset points',ha='center',fontsize=10)
  ax.margins(x=.16,y=.3);ax.set(xticks=xs,xlabel='BTC channel exit days',ylabel=label,title=year+' | '+label)
fig.suptitle('BTC own1100USDT | entry15,disjoint quote-turnover N40/min1.1 fixed\nP/R=annual gates;oldexit30 read-only | ETH own900 exit sensitivity in CSV/joint heatmap',fontsize=14);fig.savefig(T/'sensitivity_BTC.png',dpi=130);plt.close(fig)
focus=sorted([c for c in parents if c['BTC_exit_lookback_days']==c['ETH_exit_lookback_days']==20],key=lambda c:c['year']);fr=r['plan']['forward_resume'];state=json.loads((R/'research/paper10/state.json').read_text());paper=json.loads((R/'research/paper10/observations'/state['last_observation_id']/'summary.json').read_text())
lines=['# BTC/ETH收盘通道退出窗口联合验证：原55/45与过滤规则固定','',f"24个新历史定义：8个组件（4BTC、4ETH）＋16个年度组合，72成本场景真实执行；1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(summary['new_both_periods_passed_combination_pairs'])}组新退出参数跨期合格。旧4组件＋2父组合/18场景、2个额外旧N30中心只读。另3个原shadow截止定义；共27项先reserve，真实执行及独立审计后finish。",'',
 '## 事前假设、资金与精确规则','',
 '前轮N40/r1.1、ETH EMA30±1.25%、原55/45满足历史门槛；本轮冻结BTC退出20/30/40日 × ETH通道退出20/30/40日联合9格，每年各自验证。预定关注20/20，检验较早退出的资本保护与换手/错失上涨代价。BTC成交额40日、最低倍率1.1、两币入场15日、ETH EMA30与1.25%带、全部成本与失败门槛保持冻结，不按本轮OOS继续扩参。','',
 'BTC在决策i仅看已闭合C[i−1]：严格高于max(C[i−16:i−1])且Q[i−1]≥1.1×mean(Q[i−41:i−1])、参考均值>0才入场。两参考均止于i−2，排除被比较收盘/成交额。C[i−1]<min(C[i−X−1:i−1])退出优先，X=20/30/40；成交额不足本身不退出，价格相等保持，成交额阈值相等可入。Q为1440个真实UTC分钟quote_volume的Decimal和。','',
 'ETH：EMA alpha=2/31，首数据日float收盘为种子，逐日adjust=False递推、跨折不重置。C[i−1]严格上破排除自身的15日收盘通道且float(C[i−1])>EMA[i−1]×1.0125入场；下破排除自身的X日通道或float(C[i−1])<EMA[i−1]×0.9875退出优先，X=20/30/40，其他/相等保持。plan.complete_rules是30日源模板，逐个spec完整保存对应X日确切逻辑及参数。','',
 '所有组合2000USDT，原BTC55%/ETH45%对应独立1100/900USDT；新20/40组件各自以真实预算运行Decimal28数量、手续费和预算相关冲击，旧30组件净值只读。父组合将已扣成本的绝对NAV相加一次，不缩放、归一化、跨币转账、自动维持比例或再平衡。OOS183从现金/desired-cash开始，暖机不生成交易，六折连续。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范定义、{len(prior['conclusions'])}份全文结论、7份Freqtrade结果、4个OOS源码、任务/监控说明及3技能。初始16条实际证据均完整，缺结果0。历史试验从{prior['monitor_counts_before']['registered']}新增24，观察截止不计入策略挖掘。",'',
 '## 三项验证与失败条件','',
 'Walk-forward：2025和2026各03-18UTC00:01至09-14UTC00:01，180日/六个连续30日窗口；180日滚动历史、3日gap、purge0，无模型/标签/逐折拟合/优化。前日收盘后在次日UTC00:01真实历史分钟开盘参考执行，终止平仓计成本。每场景259382分钟收盘/执行点计算连续OOS整体回撤，不平均折回撤。两段历史已经反复研究，不是未触碰最终测试集。','',
 'Sensitivity：两币退出窗口联合9格/年，BTC、ETH组件各3点；90成本场景/540折全部保存，其中72新场景/432折、18旧场景/108折。逐变体净收益、完整DD、Sharpe365、Calmar、成本及正负/零折见sensitivity.csv、folds.csv与两图。相邻Sharpe差超过差异样本标准差2倍仅描述cliff，非统计显著性或PBO/DSR；旧criteria/status原样保留。','',
 'Costs：每侧10bp手续费、1bp估计半点差、2bp估计滑点，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(订单预算/滞后20日quote ADV)冲击，全部同倍率×1/2/3；ADV固定20日，与信号成交额N40分开。最大参与率0.001、Decimal28、不利PRICE tick、LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理独立核对。Oct1过滤快照用于历史是估计，缺历史L2/TCA、队列、部分成交或真实IOC接单证明。现货仅多，资金费/借币不适用。','',
 '固定八门槛：所有成本净正、1x≥4/6严格正折、3x整体分钟DD≤25%、3x邻域净正≥60%、1x≥2往返、毛参考盈亏/成本≥2.5、无负余额、终止空仓。组件和父组合独立判断；旧门槛状态不追溯修改，完整负折和零折保留。','',
 f"独立审计72新场景/18,675,504 NAV点、4320次因果决策（BTC/ETH各2160）与{summary['new_component_fills']}笔新组件历史成交；18旧场景全分钟NAV只读复核。失败计数{comparison['failure_counts']}。6个最终实际阶段和7个只读重放阶段退出码均为0；合成夹具不充当收益。",'',
 '## 工程失败与审计修复留档','',
 '冻结前生成器预检沿用错误前轮路径，首次生成退出1、随后缺preflight.py调用退出2；bootstrap_repair.json保存修复说明，当时未登记或计算。计算后原audit.py误把旧55/45对照断言为50/50而退出1；原冻结audit.py、audit.log及initial_failure_execution_steps.json保持原样，audit_repaired.py仅改该权重检查为55/45。修复元数据、原/新源码哈希、原金融report/spec/所有源码哈希留档，已算结果、源数据、账户及冻结参数未改；finish_verified.py核对修正版历史审计与原forward审计绑定后finish，replay_verified.py使用修正版审计。原失败不能写成原检查器通过。','',
 '## 预定关注20/20与对照','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']and x['kind']=='OLD_EXIT30_30');b=next(x for x in comparisons if x['config']==c['name']and x['kind']=='OLD_N30_HALF')
 lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x完整DD{z['3']['max_drawdown_pct']:.6f}%，状态{c['status']}。相对同资金同过滤旧30/30，3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp；相对旧N30/r1原50/50，3x收益差{b['return_differences_pp']['3']:.6f}pp、DD差{b['minute_DD3_difference_pp']:.6f}pp。")
lines+=['',f"新跨期合格参数中，两期所有成本收益和3x回撤均不差且至少一处改善：相对同55/45旧30/30为{comparison['jointly_improved_pairs_vs_old_exit30_30']}组，相对旧N30/r1原50/50为{comparison['jointly_improved_pairs_vs_old_N30_half']}组。36条年度比较与{len(pairs)}条配对判断见comparison.json。主对照固定相同1100/900预算、N40/r1.1与ETH EMA；次对照只匹配2000总资金，资产敞口/成交额参数不同。",'',
 '## 全部年度组合（各年按1x收益倒序）','','|年份|新/旧|BTC/ETH退出日|原BTC/ETH|初始BTC/ETH USDT|1x%|2x%|3x%|3x完整DD%|正折1|成交/往返1|成本1（手续费/冲击）|状态/失败|','|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|']
for c in sorted(parents,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];a=z['1'];cp=a['cost_parts_usdt'];failed=[k for k,v in c['criteria'].items()if not v]
 lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['BTC_exit_lookback_days']}/{c['ETH_exit_lookback_days']}|55/45|1100/900|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{a['cost_usdt']:.6f}（{cp['fee']:.6f}/{cp['impact']:.6f}）|{c['status']}/{failed}|")
lines+=['','## 全部组件与资金/失败条件','','|年份|币种|新/旧|资金USDT|退出日|1x%|2x%|3x%|3x完整DD%|正折1|往返1|状态/失败|','|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda c:(c['year'],c['asset'],c[c['asset']+'_exit_lookback_days'])):
 z=c['scenes'];a=z['1'];failed=[k for k,v in c['criteria'].items()if not v]
 lines.append(f"|{c['year']}|{c['asset']}|{'新'if c['is_new']else'旧只读'}|{c['capital_usdt']}|{c[c['asset']+'_exit_lookback_days']}|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['round_trips']}|{c['status']}/{failed}|")
lines+=['','## 平台、边界与重复路径','','|年份/对象|3x净正率|门槛通过率（旧状态保留）|cliff/邻边|最高3x收益BTC/ETH退出坐标|在边界|','|---|---:|---:|---|---|---|']
for name,z in surfaces.items():lines.append(f"|{name}|{100*z['positive3_fraction']:.3f}%|{100*z['full_gate_pass_fraction_preserving_old_status']:.3f}%|{z['cliff_flags']}/{z['edges']}|{z['best_return3_exit_coordinates']}|{z['best_on_boundary']}|")
lines+=['',f"72新场景中{h['new_scenes_already_in_any_prior_report']}曾见、{h['new_scenes_not_in_any_prior_report']}未见，去重{h['distinct_new_scene_paths_not_in_prior']}种未见单场景。6组合格参数仅{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见完整跨期路径。不同退出规则在某段市场可能产生相同交易/NAV，参数新颖不等于独立样本；完整路径重复、边界峰值与大量历史选择偏差均披露，不能称稳定实盘盈利。",'',
 '## 已有同期基准与现金','','原SMA65±1%原75/25、持有原50/50均为已有2000USDT历史，仅只读背景；敞口不同。现金是无收益USDT理论零线，不算新回测。','','|年份|旧基准/原权重|1x%|2x%|3x%|3x完整分钟DD%|','|---|---|---:|---:|---:|---:|']
for bg in r['read_only_background'].values():
 z=bg['scenes'];lines.append(f"|{bg['year']}|{bg['kind']} / {bg['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 原冻结SMA延迟shadow与十策略分别维护','']
legacy=f['configs']['forward_snapshot_combo']['scenes']
shadow=f"原SMA65/1%原75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}保留{fr['prior_NAV_points']}点精确前缀，增加120闭合分钟mark，现{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟、9完整日。新增日线决策0、执行0、参考点0；原cash/units/desired/trades/costs不变，无强制平仓或数量舍入回改，下一日线决策2026-10-12T00:01:00Z、原2027-03-31结束计划保持。1/2/3x累计收益{legacy['1']['net_return_pct']:.6f}%/{legacy['2']['net_return_pct']:.6f}%/{legacy['3']['net_return_pct']:.6f}%；不足180天/六窗，partial rejected不取消长期计划。两次真实公开GET取得时间晚于被标记分钟，仅作延迟shadow净值重建，不是十策略当时实时报价前向业绩。"
lines+=[shadow,'',f"P01–P10保持第{paper['actual_quote_observations']}次实际报价观察，UTC {paper['observed_at_utc']}、实际{paper['elapsed_seconds']/3600:.6f}小时，主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。两段旧缺口与{100*paper['coverage_fraction']:.6f}%计数/时长覆盖代理保持，非连续分钟覆盖。本轮未运行paper执行器，不改冻结规则、本金、数量、现金、desired、已处理日线、费用或交易ID，不补单；其回撤仅实际报价采样。180天/六窗尚未成熟，网页只读汇总，无重部署/重复定时任务。",'',
 f"离线精确复现：`.venv/bin/python research/experiments/{T.name}/replay_verified.py`。7阶段只读、不HTTP、不写登记/账户；使用已说明的audit_repaired.py，原失败留档。四份真实525600行分钟parquet、完整日聚合、全部交易、过滤快照/代码SHA见data_manifest.json/report.json；shadow原始公开GET及延迟见forward_report.json。大行情/NPY留忽略data；全部正负/零折、淘汰及工程失败证据保留。",'',
 '本轮固定批次已结束；未来另轮预登记，不回改本轮参数/失败门槛。历史验证合格只允许作为后续研究证据，不能替换固定P01–P10。','',
 '## 一手资料','',
 '[Binance公开历史数据](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[官方现货REST文档](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md)、[官方过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)本轮读取成功，时间见sources.json/source_access.json。引用支持字段/UTC/过滤语义；费用估计和收益来自本地实际运行研究。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA续接（延迟shadow）\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：BTC/ETH退出20/30/40日联合9格，入场15、BTC N40/r1.1、ETH EMA30±1.25%、原55/45与独立1100/900USDT固定。8新组件＋16父组合/72场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰（7项正折不足、1项3x回撤超限），6新跨期参数合格；4旧组件＋2父组合/18场景及2旧N30中心只读。对同55/45旧30/30联合改善{comparison['jointly_improved_pairs_vs_old_exit30_30']}组，旧N30/r1原50/50为{comparison['jointly_improved_pairs_vs_old_N30_half']}组；未见完整跨期路径{h['qualified_cross_period_pairs_not_in_any_prior_report']}种。原50/50审计窄断言失败保留，另存55/45修正版通过，冻结金融哈希不变。原SMA续接01→03UTC仅120marks/0决策/0成交；paper40/79.790小时状态保留。历史重复使用，不称实盘盈利。\n"
(T/'README_entry.md').write_text(entry)
marker='## 最近完成的轮次\n\n';base=prior['read_automation_README']['text'];assert marker in base
out=base.replace(marker,marker+entry+'\n',1);current=(R/'research/automation/README.md').read_text();assert current in(base,out);(R/'research/automation/README.md').write_text(out)
print(json.dumps({'passed':True,'new_qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'joint_improvement_vs_old_exit30_30':comparison['jointly_improved_pairs_vs_old_exit30_30'],'joint_improvement_vs_old_N30_half':comparison['jointly_improved_pairs_vs_old_N30_half'],'new_cross_period_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'focus':[{k:c[k]for k in('year','status','positive_folds_1x')}for c in focus],'failure_counts':comparison['failure_counts']}))
