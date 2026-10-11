"""Describe already executed frozen period/entry-band grid;read-only financial inputs."""
from pathlib import Path
from collections import Counter
from decimal import Decimal as D
import csv,gzip,hashlib,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
T=Path(__file__).resolve().parent;R=T.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text())
r=read(T/'report.json');f=read(T/'forward_report.json');h=read(T/'history_paths.json');prior=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));cs=r['configs'];summary=r['summary'];grid=r['plan']['grid'];fresh=[c for c in cs.values()if c['is_new']];parents=[c for c in cs.values()if c['role']=='combination'];external={x['name']:read(R/x['report'])['configs'][x['name']]for x in r['plan']['read_only_comparator_refs']};funds=lambda w:[int(D(2000)*D(str(x)))for x in w]
assert len(fresh)==32 and all(x['exit_code']==0 for x in read(T/'execution_steps.json')) and all(x['exit_code']==0 for x in read(T/'reproduction_execution.json'))
comparisons=[]
for c in parents:
 if not c['is_new']:continue
 oldref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='OLD_NO_BTC_EMA');old=external[oldref['name']]
 halfref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='OLD_N30_R1_HALF');half=external[halfref['name']]
 matchedref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='MATCHED_ETH_CENTER');matched=external[matchedref['name']]
 for kind,o in [('MATCHED_ETH_CENTER',matched),('OLD_NO_BTC_EMA',old),('OLD_N30_HALF',half)]:
  comparisons.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':o['name'],'comparator_is_new':False,'config_raw_weights':c['raw_weights'],'control_raw_weights':o['raw_weights'],'config_component_capitals':funds(c['raw_weights']),'control_component_capitals':funds(o['raw_weights']),'same_total_capital_usdt':2000,'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in summary['new_both_periods_passed_combination_pairs']:
 for kind in('MATCHED_ETH_CENTER','OLD_NO_BTC_EMA','OLD_N30_HALF'):
  rows=[next(x for x in comparisons if x['config']==n and x['kind']==kind)for n in pair];rv=[v for x in rows for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in rows]
  pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)),'lower_DD3_both_years':all(v<0 for v in dd),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');cells=[c for c in cs.values()if c['year']==year and c['sensitivity_member']and(c.get('asset')==role or c['role']==role)];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['ETH_EMA_span_days'],c['ETH_EMA_symmetric_band']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[name]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'positive_sharpe3_fraction':sum((c['scenes']['3']['sharpe_365']or 0)>0 for c in cells)/len(cells),'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/len(cells),'cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'edges':len(sens['adjacent_edges']),'best_return3_coordinates':coords,'best_on_boundary':None if role=='BTC'else any(span in(20,40)or band in(.01,.015)for span,band in coords),'scope':'BTC fixed read-only source'if role=='BTC'else'9cellETHperiod/symmetricbandgrid;old30/band0.0125center preserved;externalcontrols excluded'}
comparison={'report_sha256':sha(T/'report.json'),'comparisons':comparisons,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_matched_eth_center':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='MATCHED_ETH_CENTER'),'jointly_improved_pairs_vs_old_no_BTC_EMA':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_NO_BTC_EMA'),'jointly_improved_pairs_vs_old_N30_half':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_N30_HALF'),'lower_DD3_pairs_vs_old_no_BTC_EMA':sum(x['lower_DD3_both_years']for x in pairs if x['kind']=='OLD_NO_BTC_EMA'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'scope':'PrimaryR40ETH30/band0.0125center withidenticalBTCandfunds;onlyETHperiod/band changes. SecondarynoBTCEMA/ETH30center andN30/r1raw50/50 havedifferent rules/exposure. Repeatedhistories,allcontrolsread-only.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_initial_weight','BTC_EMA_span_days','BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction','ETH_EMA_span_days','ETH_EMA_symmetric_band','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_initial_weight'],c['BTC_EMA_span_days'],c['BTC_EMA_entry_band_fraction'],c['BTC_EMA_exit_band_fraction'],c['ETH_EMA_span_days'],c['ETH_EMA_symmetric_band'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
metrics=[('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]
for role,filename in [('combination','sensitivity.png'),('ETH','sensitivity_ETH.png')]:
 fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
 for row,year in enumerate(('2025','2026')):
  cells={(c['ETH_EMA_span_days'],c['ETH_EMA_symmetric_band']):c for c in cs.values()if c['year']==year and c['sensitivity_member']and(c['role']==role or c.get('asset')==role)}
  for col,(metric,label)in enumerate(metrics):
   ax=axes[row,col];matrix=np.array([[cells[span,band]['scenes']['3'][metric]for band in grid['ETH_EMA_symmetric_band']]for span in grid['ETH_EMA_span_days']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
   for i,span in enumerate(grid['ETH_EMA_span_days']):
    for j,band in enumerate(grid['ETH_EMA_symmetric_band']):
     c=cells[span,band];ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if c['status']=='passed'else' R')+(' O'if not c['is_new']else''),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
   ax.set(xticks=range(3),xticklabels=['1%','1.25%','1.5%'],yticks=range(3),yticklabels=['20','30','40'],xlabel='ETH EMA symmetric band',ylabel='ETH EMA span days',title=year+' | '+label);ax.title.set_fontsize(10);fig.colorbar(im,ax=ax,fraction=.035)
 fig.suptitle(('ETH own900USDT'if role=='ETH'else'Fixed BTC EMA15 x ETH channel/EMA grid | raw55/45,own1100/900')+'\nChannel15/30;BTCN40/r1.1 fixed | P/R=annual gates,O=oldcenter | repeated histories',fontsize=14);fig.savefig(T/filename,dpi=130);plt.close(fig)
fr=r['plan']['forward_resume'];paperstate=read(R/'research/paper10/state.json');paper=read(R/'research/paper10/observations'/paperstate['last_observation_id']/'summary.json');focus=sorted([c for c in parents if c['is_new']and c['ETH_EMA_span_days']==30 and c['ETH_EMA_symmetric_band']==.01],key=lambda c:c['year'])
lines=['# ETH EMA周期与对称带宽：BTC固定EMA15、原55/45','',f"本轮32个新历史配置：16个ETH组件＋16个年度组合、96个成本场景。1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰；{len(summary['new_both_periods_passed_combination_pairs'])}组新参数跨两段历史合格。4旧组件＋2旧组合/18场景只读，另3个旧SMA延迟shadow截止。共35项先reserve，实际执行与审计后finish。",'',
 '## 预先冻结的假设、规则与资金','',r['plan']['hypothesis'],'',
 'ETH联合EMA20/30/40日 × 对称带宽1%/1.25%/1.5%，通道15入30出；事前关注EMA30±1%，旧EMA30±1.25%为只读中心。BTC沿用已有EMA15上破1%/下破3%、通道15/30及成交额N40≥1.1规则，复用原1100USDT组件完整净值。既有排名不替换P01–P10。','',
 'ETH决策i只用闭合C[i−1]：C[i−1]>max(C[i−16:i−1]) AND float(C[i−1])>EMA[i−1]×(1+b)同一决策均成立才long；C[i−1]<min(C[i−31:i−1]) OR float(C[i−1])<EMA[i−1]×(1−b)任一成立退出优先。通道参考止于i−2，排除被比较收盘；其余及阈值相等保持，没有延迟入场记忆。EMA alpha=2/(s+1)，E0=float(数据首日闭合收盘)，Ej=(1−alpha)E[j−1]+alpha×float(Cj)，Python float、adjust=False、跨折不重置。','',
 'BTC闭合C[i−1]突破排除自身的15日收盘通道、Q[i−1]≥1.1×mean(Q[i−41:i−1])且均值>0、C[i−1]严格上破EMA15×1.01同时成立才long；下破30日收盘通道或EMA15×0.97退出优先。成交额Q为真实1440分钟quote_volume的Decimal和，参考止于i−2；低量本身不退出，成交额阈值相等可入。完整确切源码/每份spec/组件指纹保留。','',
 '每个组合2000USDT原始BTC55%/ETH45%对应独立1100/900初始预算，不归一化、不转账、不维持比例或再平衡。新ETH以900资金执行Decimal28及预算相关冲击；BTC使用同1100资金已扣成本NAV，只相加绝对NAV一次，不缩放旧曲线。OOS183初始cash/desired-cash，暖机不产生收益或持仓，六折账户连续。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范配置、{len(prior['conclusions'])}份全文结论、7份Freqtrade结果含zip成员、4个OOS源码、任务/监控说明及3技能。初始16条实际结果齐全、缺0。历史试验从{prior['monitor_counts_before']['registered']}新增32，持续观察截止另计。",'',
 '## 三项验证、失败门槛与实际执行','',
 'Walk-forward：2025、2026分别03-18UTC00:01至09-14UTC00:01，各180日/六个连续30日折；180日滚动历史、3日gap、purge0。固定规则，无模型标签/拟合/逐折优化；前日闭合后用次日真实历史00:01分钟开盘参考执行，终止平仓计成本。每场景259382个分钟收盘/执行点计算连续OOS整体回撤，不平均折回撤。两段历史已反复研究，不是未触碰最终测试集。','',
 'Sensitivity：ETH周期×带宽9格/年，组件与组合分别评估；旧中心保留原criteria/status并纳入邻域，BTC每年1个固定旧来源无新调参。114场景/684折含96新场景/576折和18旧场景/108折，逐变体1/2/3倍成本收益、整体回撤、Sharpe、Calmar见sensitivity.csv/report.json。相邻Sharpe差超过差异样本标准差2倍只描述cliff，不是PBO/DSR或显著性证据；边界结果不在同轮扩参。','',
 'Costs：每侧10bp手续费＋估计1bp半点差＋估计2bp滑点＋0.5×前20完整UTC日未年化样本log波动率×sqrt(订单预算/20日quote ADV)，全部按1/2/3倍放大，参与率≤0.001。成本ADV20与BTC信号成交额N40分开。Decimal28、不利PRICE tick、LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理逐单复核。Oct1过滤快照为历史假设；缺历史L2/TCA/排队/部分成交/真实IOC接单证明，现货仅多，无资金费/借币。','',
 '冻结八门槛：全成本净正、1x≥4/6严格正折、3x完整分钟DD≤25%、3x邻域净正≥60%、1x≥2往返、毛参考盈亏/成本≥2.5、无负余额、终止空仓。新ETH组件和组合独立判断，不回改旧状态；负/零折及淘汰全部保留。','',
 f"6个实际阶段在恢复后成功完成，7个只读精确重放阶段退出均0；独立审计96新场景/24,900,672 NAV点、8640次ETH因果决策、{summary['new_component_fills']}笔新ETH历史虚拟成交，并只读复核18旧场景。Pandas独立EMA、Decimal费用/舍入/余额及整体/逐折指标核对，冻结后金融源码哈希不变。夹具检验周期与带宽差异、EMA单独退出、同一决策联合入场、等值边界与未来尾部隔离，不作收益证据。失败计数{comparison['failure_counts']}。",'',
 '## 预定关注ETH EMA30±1%','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']and x['kind']=='MATCHED_ETH_CENTER');lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x整体分钟DD{z['3']['max_drawdown_pct']:.6f}%，1x正折{c['positive_folds_1x']}/6、{c['status']}；相对ETH30±1.25%旧中心，3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp。前五折3x累计{z['3']['first_five_fold_return_pct']:.6f}%、末折{z['3']['last_fold_return_pct']:.6f}%。")
lines+=['',f"新跨期合格组合中，两期全成本收益和3x回撤均不差、至少一处改善：匹配ETH中心{comparison['jointly_improved_pairs_vs_matched_eth_center']}组、无BTC EMA背景{comparison['jointly_improved_pairs_vs_old_no_BTC_EMA']}组、旧N30/r1原50/50背景{comparison['jointly_improved_pairs_vs_old_N30_half']}组。主对照BTC组件完全相同，只变ETH两参数；次对照规则/敞口不同，不作单一因素归因。48条年度比较及配对判断见comparison.json。",'',
 '## 年度组合（各年按1x成本后净收益倒序）','','|年|新/旧|ETH EMA周期/对称带宽|原BTC/ETH；初始USDT|1x%|2x%|3x%|3x分钟DD%|Sharpe3|Calmar3|正折1|成交/往返1|成本1（手续费/冲击）|状态/失败|','|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|']
for c in sorted(parents,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];a=z['1'];lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{c['ETH_EMA_span_days']}日/±{100*c['ETH_EMA_symmetric_band']:g}%|55/45；1100/900|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{z['3']['sharpe_365']}|{z['3']['calmar']}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{a['cost_usdt']:.6f}（{a['cost_parts_usdt']['fee']:.6f}/{a['cost_parts_usdt']['impact']:.6f}）|{c['status']} {'/'.join(c.get('failed_criteria',[]))}|")
lines+=['','## 单币组件','','|年/币|新/旧|指标|本金USDT|1x%|2x%|3x%|3x分钟DD%|正折1|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];label='BTC固定EMA15 +1%/−3%＋通道/成交额'if c['asset']=='BTC'else f"ETH通道15/30＋EMA{c['ETH_EMA_span_days']}±{100*c['ETH_EMA_symmetric_band']:g}%";lines.append(f"|{c['year']}/{c['asset']}|{'新'if c['is_new']else'旧只读'}|{label}|{c['capital_usdt']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{c['status']}|")
lines+=['','## 预定关注组合逐折（全部684折见folds.csv）','','|年|成本|折|净收益%|分钟DD%|Sharpe365|Calmar|','|---|---|---|---:|---:|---:|---:|']
for c in focus:
 for k,z in c['scenes'].items():
  for ff in z['folds']:lines.append(f"|{c['year']}|{k}x|{ff['fold']}|{ff['net_return_pct']:.6f}|{ff['max_drawdown_pct']:.6f}|{ff['sharpe_365']}|{ff['calmar']}|")
lines+=['','## 参数平台、边界与重复路径','','|对象|3x净正率|3x正Sharpe率|门槛通过率|cliff/邻边|最高3x收益周期/带宽|边界|','|---|---:|---:|---:|---|---|---|']
for name,z in surfaces.items():lines.append(f"|{name}|{100*z['positive3_fraction']:.3f}%|{100*z['positive_sharpe3_fraction']:.3f}%|{100*z['full_gate_pass_fraction']:.3f}%|{z['cliff_flags']}/{z['edges']}|{z['best_return3_coordinates']}|{z['best_on_boundary']}|")
lines+=['',f"96新场景中{h['new_scenes_already_in_any_prior_report']}条曾见、{h['new_scenes_not_in_any_prior_report']}条未见，去重{h['distinct_new_scene_paths_not_in_prior']}种新单段路径。{len(summary['new_both_periods_passed_combination_pairs'])}合格参数只有{h['qualified_cross_period_pairs_not_in_any_prior_report']}种全成本跨期路径配对未见。参数/路径新颖不是独立市场样本；重复历史、多重选择、边界与负折风险均披露，不称稳定实盘盈利。",'',
 '## 同期旧基准与理论现金','','已有2000USDT的SMA65±1%原75/25和持有原50/50只读作背景，敞口不同；现金零收益为分析基线，不新回测。','','|年|旧基准/原权重|1x%|2x%|3x%|3x分钟DD%|','|---|---|---:|---:|---:|---:|']
for bg in r['read_only_background'].values():
 z=bg['scenes'];lines.append(f"|{bg['year']}|{bg['kind']}/{bg['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 原SMA延迟shadow及固定十策略',''];legacy=f['configs']['forward_snapshot_combo']['scenes'];shadow=f"原SMA65/1%原75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}；原{fr['prior_NAV_points']}点前缀精确保留，增加120闭合分钟mark到{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟/{fr['cumulative_minutes']//1440}完整日。0新日决策/参考点/成交，原float现金/数量/desired/trades/费用不变，不强平或回改舍入。下一决策2026-10-12T00:01:00Z，原2027-03-31结束安排保持。1/2/3x累计{legacy['1']['net_return_pct']:.6f}%/{legacy['2']['net_return_pct']:.6f}%/{legacy['3']['net_return_pct']:.6f}%。公开GET晚于被标记分钟，属于延迟shadow重建，不能冒充十策略当时实时报价前向业绩。未满180天/六窗，partial rejected不取消长期计划。"
lines+=[shadow,'',f"P01–P10仍第{paper['actual_quote_observations']}次真实报价观察、UTC {paper['observed_at_utc']}，累计{paper['elapsed_seconds']/3600:.6f}小时；主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。两段缺口及{100*paper['coverage_fraction']:.6f}%计数/时长覆盖代理保留，非连续分钟覆盖。冻结plan/state、本金、持仓、desired/已处理日线、成本/交易ID及旧观察完整保持，本轮未运行paper执行器、不补单。监控源码哈希保持，只读生成汇总，不新增成交、不改网页/重部署或重复建任务。",'',
 f"离线精确复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`，7阶段无HTTP/登记或账户写入。4份真实525600行分钟parquet、日聚合、完整交易与过滤快照/源码SHA见data_manifest.json/report.json；shadow真实原始GET/时间/哈希留档。大行情/NPY留忽略data，全部成功/负折/零折/淘汰保存。",'',
 '## 一手资料','',
 '[Binance公开历史](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[现货REST](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md)、[过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)、[pandas EMA](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)本轮读取成功；访问时间见sources.json/source_access.json。文档当前3.0.6与实际运行2.2.3分开记录；来源支持字段/时序/递推，收益来自真实本地计算，成本为上述估计。']
lines+=['','## 真实执行故障与恢复','','首次旧SMA shadow公开GET在TLS握手阶段超时、退出1，发生于本轮历史回测之前，未生成完整forward_report。保留forward_attempt1.log、execution_steps_initial.json、execution_attempts.json及execution_recovery.json；同一已预约截止13:00UTC的第二次请求成功。金融源码/参数/旧账户哈希未改，历史收益评估仅执行一次；没有为十策略补做旧订单，重放仍只读已有真实输入。']
lines+=['', '## 旧报告元数据兼容核验修正', '', '最终只读核验首次因旧R35组合报告未包含后来新增的BTC_EMA_span_days元数据字段而KeyError退出1。保留verify_before.py、verify_attempt1.log和verification_recovery.json；修正为读取可选元数据，同时直接核对原BTC完整spec确实无EMA参数且成交额N40/r1.1。不修改旧报告、金融源码、收益/费用/门槛或登记，不复算收益。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA延迟shadow续接\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：ETH EMA20/30/40日×对称1/1.25/1.5%，BTC固定EMA15 +1%/−3%及通道/成交额；原55/45独立1100/900。16新ETH＋16组合/96场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，失败{comparison['failure_counts']}；{len(summary['new_both_periods_passed_combination_pairs'])}跨期合格、{h['qualified_cross_period_pairs_not_in_any_prior_report']}新跨期路径。匹配ETH30±1.25%中心联合改善{comparison['jointly_improved_pairs_vs_matched_eth_center']}组；4旧组件＋2旧组合/18场景只读。原SMA11→13UTC只追加120mark/0交易；paper45及旧缺口保持。重复历史不称实盘稳定盈利。\n"
(T/'README_entry.md').write_text(entry);marker='## 最近完成的轮次\n\n';base=prior['read_automation_README']['text'];out=base.replace(marker,marker+entry+'\n',1);assert(R/'research/automation/README.md').read_text()in(base,out);(R/'research/automation/README.md').write_text(out)
print(json.dumps({'passed':True,'new_qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'joint_improvements_matched':comparison['jointly_improved_pairs_vs_matched_eth_center'],'joint_improvements_no_BTC_EMA':comparison['jointly_improved_pairs_vs_old_no_BTC_EMA'],'new_cross_period_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'failure_counts':comparison['failure_counts']}))
