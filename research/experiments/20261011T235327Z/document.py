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
assert len(fresh)==36 and all(x['exit_code']==0 for x in read(T/'execution_steps.json')) and all(x['exit_code']==0 for x in read(T/'reproduction_execution.json'))
comparisons=[]
for c in parents:
 if not c['is_new']:continue
 oldref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='OLD_NO_BTC_EMA');old=external[oldref['name']]
 halfref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='OLD_N30_R1_HALF');half=external[halfref['name']]
 matchedref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='MATCHED_ETH_CENTER_TIGHT'and x['matched_entry_band_fraction']==c['ETH_EMA_entry_band_fraction']);matched=external[matchedref['name']]
 wideref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='MATCHED_ETH_SLOW_PERIOD'and x['matched_entry_band_fraction']==c['ETH_EMA_entry_band_fraction']);wide=external[wideref['name']]
 for kind,o in [('MATCHED_ETH_CENTER_TIGHT',matched),('MATCHED_ETH_SLOW_PERIOD',wide),('OLD_NO_BTC_EMA',old),('OLD_N30_HALF',half)]:
  comparisons.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':o['name'],'comparator_is_new':False,'config_raw_weights':c['raw_weights'],'control_raw_weights':o['raw_weights'],'config_component_capitals':funds(c['raw_weights']),'control_component_capitals':funds(o['raw_weights']),'same_total_capital_usdt':2000,'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in summary['new_both_periods_passed_combination_pairs']:
 for kind in('MATCHED_ETH_CENTER_TIGHT','MATCHED_ETH_SLOW_PERIOD','OLD_NO_BTC_EMA','OLD_N30_HALF'):
  rows=[next(x for x in comparisons if x['config']==n and x['kind']==kind)for n in pair];rv=[v for x in rows for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in rows]
  pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)),'lower_DD3_both_years':all(v<0 for v in dd),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');cells=[c for c in cs.values()if c['year']==year and c['sensitivity_member']and(c.get('asset')==role or c['role']==role)];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['ETH_EMA_span_days'],c['ETH_EMA_entry_band_fraction']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[name]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'positive_sharpe3_fraction':sum((c['scenes']['3']['sharpe_365']or 0)>0 for c in cells)/len(cells),'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/len(cells),'cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'edges':len(sens['adjacent_edges']),'best_return3_coordinates':coords,'best_on_boundary':None if role=='BTC'else any(span in(32,36)or band in(.01,.015)for span,band in coords),'scope':'BTC fixed read-only source'if role=='BTC'else'9cellETHEMAspan32/34/36xentrybandgrid,exit0.005fixed;matchedETH35controls excluded'}
comparison={'report_sha256':sha(T/'report.json'),'comparisons':comparisons,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_matched_eth_period':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='MATCHED_ETH_CENTER_TIGHT'),'jointly_improved_pairs_vs_slow_period':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='MATCHED_ETH_SLOW_PERIOD'),'jointly_improved_pairs_vs_old_no_BTC_EMA':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_NO_BTC_EMA'),'jointly_improved_pairs_vs_old_N30_half':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_N30_HALF'),'lower_DD3_pairs_vs_old_no_BTC_EMA':sum(x['lower_DD3_both_years']for x in pairs if x['kind']=='OLD_NO_BTC_EMA'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'scope':'Primarysameentry/exit ETH35R44parentswithidenticalBTCandfundsisolateperiod.Matchedsameentry/exitETH40R45parentsalsoisolateperiod. SecondarynoBTCEMA/ETH30center andN30/r1raw50/50 havedifferentrules/exposure.Allread-only;repeatedhistories.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_initial_weight','BTC_EMA_span_days','BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction','ETH_EMA_span_days','ETH_EMA_symmetric_band','ETH_EMA_entry_band_fraction','ETH_EMA_exit_band_fraction','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_initial_weight'],c['BTC_EMA_span_days'],c['BTC_EMA_entry_band_fraction'],c['BTC_EMA_exit_band_fraction'],c['ETH_EMA_span_days'],c['ETH_EMA_symmetric_band'],c['ETH_EMA_entry_band_fraction'],c['ETH_EMA_exit_band_fraction'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
metrics=[('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]
for role,filename in [('combination','sensitivity.png'),('ETH','sensitivity_ETH.png')]:
 fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
 for row,year in enumerate(('2025','2026')):
  cells={(c['ETH_EMA_span_days'],c['ETH_EMA_entry_band_fraction']):c for c in cs.values()if c['year']==year and c['sensitivity_member']and(c['role']==role or c.get('asset')==role)}
  for col,(metric,label)in enumerate(metrics):
   ax=axes[row,col];matrix=np.array([[cells[span,band]['scenes']['3'][metric]for band in grid['ETH_EMA_entry_band_fraction']]for span in grid['ETH_EMA_span_days']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
   for i,span in enumerate(grid['ETH_EMA_span_days']):
    for j,band in enumerate(grid['ETH_EMA_entry_band_fraction']):
     c=cells[span,band];ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if c['status']=='passed'else' R')+(' O'if not c['is_new']else''),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
   ax.set(xticks=range(3),xticklabels=['1%','1.25%','1.5%'],yticks=range(3),yticklabels=['32','34','36'],xlabel='ETH EMA entry band',ylabel='ETH EMA span (days)',title=year+' | '+label);ax.title.set_fontsize(10);fig.colorbar(im,ax=ax,fraction=.035)
 fig.suptitle(('ETH own900USDT'if role=='ETH'else'Fixed BTC EMA15 x ETH EMA span/entry | exit0.5%,raw55/45,own1100/900')+'\nChannel15/30;BTCN40/r1.1 fixed | P/R=annual gates,O=old | repeated histories',fontsize=14);fig.savefig(T/filename,dpi=130);plt.close(fig)
fr=r['plan']['forward_resume'];paperstate=read(R/'research/paper10/state.json');paper=read(R/'research/paper10/observations'/paperstate['last_observation_id']/'summary.json');focus=sorted([c for c in parents if c['is_new']and c['ETH_EMA_span_days']==34 and c['ETH_EMA_entry_band_fraction']==.0125 and c['ETH_EMA_exit_band_fraction']==.005],key=lambda c:c['year'])
recovery=read(T/'execution_recovery.json');network_failures=len(recovery['network_failures'])
lines=['# ETH EMA周期与入场带宽：退出0.5%、BTC与原55/45固定','',f"36个新历史配置：18个ETH组件＋18个年度组合、108个成本场景实际执行。1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，{len(summary['new_both_periods_passed_combination_pairs'])}组参数跨两段历史合格。2个固定BTC组件/6成本场景只读，16个旧父组合对照指针只读，另3个原SMA shadow截止；共39项先reserve再实际计算、审计和finish。",'',
 '## 事前假设、完整规则与资金','',r['plan']['hypothesis'],'',
 '固定ETH退出0.5%，联合EMA周期32/34/36日 × 入场1%/1.25%/1.5%，通道15入30出；事前关注34日、+1.25%/−0.5%。旧R44同入场及退出阈值的EMA35父组合逐一作主对照，仅改变周期；R45同入场及退出阈值的EMA40父组合另作对照，也仅改变周期。检验周期扰动的正折一致性、回撤与成本权衡。BTC沿用已有EMA15 +1%/−3%、通道15/30及成交额N40≥1.1，原始55/45和成本/八门槛固定；方向来自重复开发历史，不在本轮OOS扩参或择优后重称独立验证。','',
 'ETH决策i只用闭合C[i−1]：C[i−1]>max(C[i−16:i−1]) AND float(C[i−1])>EMA[n][i−1]×(1+e)同一决策均成立才long；C[i−1]<min(C[i−31:i−1]) OR float(C[i−1])<EMA[n][i−1]×(1−d)任一成立退出优先。e与d独立，通道参考止于i−2，排除被比较收盘；其余及阈值相等保持，无延迟入场记忆。EMA周期n取32/34/36，alpha=2/(n+1)，E0=float(首个数据日闭合收盘)，Ej=(1−alpha)E[j−1]+alpha×float(Cj)，Python float、adjust=False、跨折不重置。','',
 'BTC参考同样排除自身：15日收盘突破AND Q[i−1]≥1.1×mean(Q[i−41:i−1])且均值>0 AND float(C[i−1])>EMA15[i−1]×1.01才long；下破30日收盘通道或EMA15×0.97退出优先。Q为真实1440分钟quote_volume的Decimal和，参考止于i−2；低量本身不退出，成交额阈值相等可入。规则/参数/代码哈希逐spec留存。','',
 '每个组合2000USDT原BTC55%/ETH45%对应独立1100/900预算，不归一化、不转账、不维持比例或再平衡。新ETH以900资金执行Decimal28与预算相关冲击；BTC复用同1100资金已扣成本完整NAV，组合只相加绝对NAV一次，不缩放旧1000曲线。OOS183从cash/desired-cash开始，暖机不产生收益或持仓，六折连续。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范配置、{len(prior['conclusions'])}份全文结论、7份Freqtrade结果含zip成员、4个OOS源码、任务/监控说明与3技能。初始16条均有实际结果、缺0。历史研究从{prior['monitor_counts_before']['registered']}新增36，持续观察截止另计。",'',
 '## 三项验证与冻结门槛','',
 'Walk-forward：2025、2026分别03-18UTC00:01至09-14UTC00:01，各180日/六个连续30日折，180日滚动历史、3日gap、purge0。固定规则，无模型标签/拟合/逐折调参；前日闭合后用次日真实历史00:01分钟开盘参考执行，终止平仓计成本。每场景259382个分钟收盘/执行点计算完整连续OOS整体回撤，不平均折回撤。两段历史已反复使用，不能称未触碰最终测试集。','',
 'Sensitivity：ETH周期×入场带宽9格/年，退出0.5%固定，组件及组合分别评估；BTC每年1个固定旧来源无新调参，旧EMA35父组合不混入新邻域。114场景/684折含108新场景/648折与6旧场景/36折，逐变体1/2/3成本净收益、整体回撤、Sharpe、Calmar见sensitivity.csv/report.json。相邻Sharpe差超过差异样本标准差2倍只描述cliff，不是显著性/PBO/DSR证据；边界结果不在同轮扩参。','',
 'Costs：每侧10bp手续费＋估计1bp半点差＋估计2bp滑点＋0.5×前20完整UTC日未年化样本log波动率×sqrt(订单预算/20日quote ADV)，全项按1/2/3倍放大，最大参与率0.001。成本ADV20与BTC信号N40分开。Decimal28、不利PRICE tick、LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理独立逐单复核。Oct1规则快照为历史假设，缺历史L2/TCA/队列/部分成交/真实IOC保证；现货只多，资金费/借币不适用。','',
 '八门槛不变：全成本净正、1x≥4/6严格正折、3x整体分钟DD≤25%、3x邻域净正≥60%、1x≥2往返、毛参考盈亏/成本≥2.5、无负余额、终止空仓。新ETH组件与父组合独立判断，旧状态不回改；所有负/零折与淘汰保留。','',
 f"6个实际阶段完成、7阶段精确只读重放退出均0；独立审计108新场景/28,013,256 NAV点、9720次ETH因果决策、{summary['new_component_fills']}笔新组件历史虚拟成交和6旧成本场景。Pandas独立EMA与Decimal费用/舍入/余额、整体/逐折指标核对，冻结后金融源码哈希保持。手工夹具覆盖独立入场/退出带宽、EMA单独退出、通道联合门槛、未来尾部隔离及仅合成数据的对称规则等价，不作收益证据。失败计数{comparison['failure_counts']}。",'',
 '## 预定关注ETH EMA34 +1.25%/−0.5%','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']and x['kind']=='MATCHED_ETH_CENTER_TIGHT');lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x完整分钟DD{z['3']['max_drawdown_pct']:.6f}%，1x正折{c['positive_folds_1x']}/6、{c['status']}；相对同入场/退出带宽的EMA35对照，3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp。前五折3x累计{z['3']['first_five_fold_return_pct']:.6f}%、末折{z['3']['last_fold_return_pct']:.6f}%。")
lines+=['',f"跨期合格组合中，两期全成本收益与3x回撤均不差、至少一处改善：匹配EMA35紧退出ETH为{comparison['jointly_improved_pairs_vs_matched_eth_period']}组、匹配EMA40为{comparison['jointly_improved_pairs_vs_slow_period']}组、无BTC EMA背景{comparison['jointly_improved_pairs_vs_old_no_BTC_EMA']}组、旧N30/r1原50/50背景{comparison['jointly_improved_pairs_vs_old_N30_half']}组。主对照同ETH入场/退出、BTC组件和资金，只变ETH周期；EMA40对照也只变周期，其余背景规则/敞口不同，不作单因素归因。72条年度比较及配对判断见comparison.json。",'',
 '## 年度组合（各年按1x成本后净收益倒序）','','|年|ETH EMA周期；入场/退出|原BTC/ETH；初始USDT|1x%|2x%|3x%|3x分钟DD%|Sharpe3|Calmar3|正折1|成交/往返1|成本1（手续费/冲击）|结论|','|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|']
for c in sorted(parents,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];a=z['1'];lines.append(f"|{c['year']}|EMA{c['ETH_EMA_span_days']}；+{100*c['ETH_EMA_entry_band_fraction']:g}%/−{100*c['ETH_EMA_exit_band_fraction']:g}%|55/45；1100/900|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{z['3']['sharpe_365']}|{z['3']['calmar']}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{a['cost_usdt']:.6f}（{a['cost_parts_usdt']['fee']:.6f}/{a['cost_parts_usdt']['impact']:.6f}）|{c['status']} {'/'.join(c.get('failed_criteria',[]))}|")
lines+=['','## 单币组件','','|年/币|新/旧|指标|本金USDT|1x%|2x%|3x%|3x分钟DD%|正折1|结论|','|---|---|---|---:|---:|---:|---:|---:|---|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];label='BTC固定EMA15 +1%/−3%＋通道/成交额'if c['asset']=='BTC'else f"ETH通道15/30＋EMA{c['ETH_EMA_span_days']} +{100*c['ETH_EMA_entry_band_fraction']:g}%/−{100*c['ETH_EMA_exit_band_fraction']:g}%";lines.append(f"|{c['year']}/{c['asset']}|{'新'if c['is_new']else'旧只读'}|{label}|{c['capital_usdt']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{c['status']}|")
lines+=['','## 预定组合逐折（全部684折见folds.csv）','','|年|成本|折|净收益%|分钟DD%|Sharpe365|Calmar|','|---|---|---|---:|---:|---:|---:|']
for c in focus:
 for k,z in c['scenes'].items():
  for ff in z['folds']:lines.append(f"|{c['year']}|{k}x|{ff['fold']}|{ff['net_return_pct']:.6f}|{ff['max_drawdown_pct']:.6f}|{ff['sharpe_365']}|{ff['calmar']}|")
lines+=['','## 参数平台、边界及路径重复','','|对象|3x净正率|3x正Sharpe率|门槛通过率|cliff/邻边|最高3x收益周期/入场|边界|','|---|---:|---:|---:|---|---|---|']
for name,z in surfaces.items():lines.append(f"|{name}|{100*z['positive3_fraction']:.3f}%|{100*z['positive_sharpe3_fraction']:.3f}%|{100*z['full_gate_pass_fraction']:.3f}%|{z['cliff_flags']}/{z['edges']}|{z['best_return3_coordinates']}|{z['best_on_boundary']}|")
lines+=['',f"108新场景中{h['new_scenes_already_in_any_prior_report']}条曾见、{h['new_scenes_not_in_any_prior_report']}条未见，去重{h['distinct_new_scene_paths_not_in_prior']}种新单段路径；{len(summary['new_both_periods_passed_combination_pairs'])}合格参数只有{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见全成本跨期配对。参数/路径新颖不等于独立市场样本，重复历史、多重选择与边界/负折风险均披露，不称稳定实盘盈利。",'',
 '## 同期旧基准与理论现金','','已有2000USDT的SMA65±1%原75/25及持有原50/50只读作背景，敞口不同；USDT零收益为理论基线，不新回测。','','|年|基准/原权重|1x%|2x%|3x%|3x分钟DD%|','|---|---|---:|---:|---:|---:|']
for bg in r['read_only_background'].values():
 z=bg['scenes'];lines.append(f"|{bg['year']}|{bg['kind']}/{bg['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 原SMA延迟shadow与固定十策略',''];legacy=f['configs']['forward_snapshot_combo']['scenes'];shadow=f"原SMA65/1%原75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}；原{fr['prior_NAV_points']}点前缀精确保留，增加120闭合分钟mark到{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟/{fr['cumulative_minutes']//1440}完整日。0新日决策/参考点/成交，原float现金/数量/desired/trades/费用不变，不强平或回改舍入。下一决策2026-10-12T00:01:00Z，原2027-03-31结束安排保持。1/2/3x累计{legacy['1']['net_return_pct']:.6f}%/{legacy['2']['net_return_pct']:.6f}%/{legacy['3']['net_return_pct']:.6f}%。公开GET晚于被标记分钟，属于延迟shadow重建，不能冒充十策略当时实时报价前向业绩。未满180天/六窗，partial rejected不取消持续计划。"
lines+=[shadow,'',f"P01–P10仍第{paper['actual_quote_observations']}次真实报价观察，UTC {paper['observed_at_utc']}、累计{paper['elapsed_seconds']/3600:.6f}小时，主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。两段旧缺口与{100*paper['coverage_fraction']:.6f}%计数/时长覆盖代理保留，非连续分钟覆盖。冻结plan/state、本金/持仓/desired/已处理日线/成本/交易ID与旧观察保持，本轮未运行paper执行器、不补单。监控源码哈希保持，只读汇总，不新增成交或改网页/重部署/重复建任务。",'',
 f"精确离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`，7阶段无HTTP/登记/账户写入。4份真实525600行分钟parquet、日聚合、交易/过滤快照与源码SHA见data_manifest.json/report.json；shadow原始GET/时间/哈希留档。大行情/NPY留忽略data，全部成功/负折/零折/淘汰永久保留。",'',
 '## 执行与故障记录','',f"公开行情失败请求{network_failures}次；每次失败日志、部分输入及同一冻结截止的恢复记录见execution_attempts.json/execution_recovery.json。6阶段最终成功，历史收益计算仅1次，金融源码/参数/旧账户哈希未改；不存在为十策略倒填旧订单。",'',
 '## 一手资料','',
 '[Binance公开历史](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[现货REST](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md)、[过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)、[pandas EMA](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)本轮读取成功，访问时间见sources.json/source_access.json。文档当前3.0.6与运行2.2.3分开记录；来源支持字段/时序/递推，收益来自实际本地计算，成本为上述估计。']
lines+=['','## 既往索引说明','','R43 README索引的退出2/3/4%为旧文案残留；其不可变spec、实际report和result.md为0.25/0.5/0.75%。本轮只读源spec及真实报告，未重写旧证据。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA延迟shadow续接\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：ETH EMA32/34/36日×入场1/1.25/1.5%，退出0.5%固定，BTC固定EMA15 +1%/−3%及通道/成交额，原55/45独立1100/900。18新ETH＋18组合/108场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，失败{comparison['failure_counts']}；{len(summary['new_both_periods_passed_combination_pairs'])}跨期合格、{h['qualified_cross_period_pairs_not_in_any_prior_report']}新跨期路径。匹配同入场/退出EMA35联合改善{comparison['jointly_improved_pairs_vs_matched_eth_period']}组；2旧BTC/6场景只读。原SMA21→23UTC只追加120mark/0交易；paper50及旧缺口保持，网络失败{network_failures}次留档；重复历史不称实盘稳定盈利。\n"
(T/'README_entry.md').write_text(entry);marker='## 最近完成的轮次\n\n';base=prior['read_automation_README']['text'];out=base.replace(marker,marker+entry+'\n',1);assert(R/'research/automation/README.md').read_text()in(base,out);(R/'research/automation/README.md').write_text(out)
print(json.dumps({'passed':True,'new_qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'joint_improvements_matched':comparison['jointly_improved_pairs_vs_matched_eth_period'],'joint_improvements_slow':comparison['jointly_improved_pairs_vs_slow_period'],'joint_improvements_no_BTC_EMA':comparison['jointly_improved_pairs_vs_old_no_BTC_EMA'],'new_cross_period_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'failure_counts':comparison['failure_counts'],'network_failures':network_failures}))
