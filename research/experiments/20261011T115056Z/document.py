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
assert len(fresh)==24 and all(x['exit_code']==0 for x in read(T/'execution_steps.json')) and all(x['exit_code']==0 for x in read(T/'reproduction_execution.json'))
comparisons=[]
for c in parents:
 if not c['is_new']:continue
 old=next(x for x in parents if x['year']==c['year']and not x['is_new']and x['BTC_EMA_span_days']is None)
 halfref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='OLD_N30_R1_HALF');half=external[halfref['name']]
 matchedref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='MATCHED_SPAN20_ASYMMETRIC'and x['matched_entry_band_fraction']==c['BTC_EMA_entry_band_fraction']);matched=external[matchedref['name']]
 for kind,o in [('MATCHED_SPAN20',matched),('OLD_NO_BTC_EMA',old),('OLD_N30_HALF',half)]:
  comparisons.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':o['name'],'comparator_is_new':False,'config_raw_weights':c['raw_weights'],'control_raw_weights':o['raw_weights'],'config_component_capitals':funds(c['raw_weights']),'control_component_capitals':funds(o['raw_weights']),'same_total_capital_usdt':2000,'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in summary['new_both_periods_passed_combination_pairs']:
 for kind in('MATCHED_SPAN20','OLD_NO_BTC_EMA','OLD_N30_HALF'):
  rows=[next(x for x in comparisons if x['config']==n and x['kind']==kind)for n in pair];rv=[v for x in rows for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in rows]
  pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)),'lower_DD3_both_years':all(v<0 for v in dd),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');cells=[c for c in cs.values()if c['year']==year and c['sensitivity_member']and(c.get('asset')==role or c['role']==role)];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['BTC_EMA_span_days'],c['BTC_EMA_entry_band_fraction']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[name]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'positive_sharpe3_fraction':sum((c['scenes']['3']['sharpe_365']or 0)>0 for c in cells)/len(cells),'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/len(cells),'cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'edges':len(sens['adjacent_edges']),'best_return3_coordinates':coords,'best_on_boundary':None if role=='ETH'else any(span in(10,20)or band in(.005,.015)for span,band in coords),'scope':'ETH fixed read-only source'if role=='ETH'else'9cellperiod/entrybandgrid;span20oldresults and originalcriteria preserved;noBTCEMA baseline excluded'}
comparison={'report_sha256':sha(T/'report.json'),'comparisons':comparisons,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_matched_span20':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='MATCHED_SPAN20'),'jointly_improved_pairs_vs_old_no_BTC_EMA':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_NO_BTC_EMA'),'jointly_improved_pairs_vs_old_N30_half':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_N30_HALF'),'lower_DD3_pairs_vs_old_no_BTC_EMA':sum(x['lower_DD3_both_years']for x in pairs if x['kind']=='OLD_NO_BTC_EMA'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'scope':'Primarysame-entryband/exits3percent R39EMA20 controls;only EMAperiod changes atown1100/900/raw55/45,channel15/30,N40/r1.1 andETHfixed. SecondarysamefundsnoBTCEMA andoldN30/r1raw50/50(differentexposure). Allcontrolsread-only;repeatedhistories.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_initial_weight','BTC_EMA_span_days','BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_initial_weight'],c['BTC_EMA_span_days'],c['BTC_EMA_entry_band_fraction'],c['BTC_EMA_exit_band_fraction'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
metrics=[('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]
for role,filename in [('combination','sensitivity.png'),('BTC','sensitivity_BTC.png')]:
 fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
 for row,year in enumerate(('2025','2026')):
  cells={(c['BTC_EMA_span_days'],c['BTC_EMA_entry_band_fraction']):c for c in cs.values()if c['year']==year and c['sensitivity_member']and(c['role']==role or c.get('asset')==role)}
  for col,(metric,label)in enumerate(metrics):
   ax=axes[row,col];matrix=np.array([[cells[span,band]['scenes']['3'][metric]for band in grid['BTC_EMA_entry_band_fraction']]for span in grid['BTC_EMA_span_days']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
   for i,span in enumerate(grid['BTC_EMA_span_days']):
    for j,band in enumerate(grid['BTC_EMA_entry_band_fraction']):
     c=cells[span,band];ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if c['status']=='passed'else' R')+(' O'if not c['is_new']else''),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
   ax.set(xticks=range(3),xticklabels=['0.5%','1%','1.5%'],yticks=range(3),yticklabels=['10','15','20 (old)'],xlabel='BTC EMA entry band;exit3% fixed',ylabel='BTC EMA span days',title=year+' | '+label);ax.title.set_fontsize(10);fig.colorbar(im,ax=ax,fraction=.035)
 fig.suptitle(('BTC own1100USDT'if role=='BTC'else'BTC x fixed ETHchannel/EMA30 | raw55/45,own1100/900')+'\nChannel15/30,N40/min1.1 fixed | P/R=annual gates,O=old | repeated histories',fontsize=14);fig.savefig(T/filename,dpi=130);plt.close(fig)
fr=r['plan']['forward_resume'];paperstate=read(R/'research/paper10/state.json');paper=read(R/'research/paper10/observations'/paperstate['last_observation_id']/'summary.json');focus=sorted([c for c in parents if c['is_new']and c['BTC_EMA_span_days']==15 and c['BTC_EMA_entry_band_fraction']==.01],key=lambda c:c['year'])
lines=['# BTC非对称EMA周期与入场带宽：ETH及原55/45固定','',f"24个新历史配置：12个BTC组件＋12个年度组合、72个成本场景实际执行；1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(summary['new_both_periods_passed_combination_pairs'])}组新参数跨期合格。10旧组件＋8旧父组合/54场景只读；其中EMA20每年3格继续进入邻域，但保留其原criteria/status。6个匹配EMA20父组合作对照指针，2个旧N30父组合只读。另3个原SMA shadow截止，共27项先reserve、实际运行与独立审计后finish。",'',
 '## 事前假设与完整规则','',r['plan']['hypothesis'],'',
 'BTC联合EMA周期10/15/20日 × 入场0.5%/1%/1.5%，退出带宽3%固定；事前关注15日/+1%/−3%。20日三格均有实际结果，不重跑。该方向依据上轮复用历史，检验更短EMA改变突破确认和退出时点的影响；不能将同一开发历史当独立最终测试，也不按本轮OOS扩参或改门槛。','',
 '决策i只看闭合C[i−1]/Q[i−1]：C[i−1]>max(C[i−16:i−1])、Q[i−1]≥1.1×mean(Q[i−41:i−1])且参考均值>0、float(C[i−1])>EMAs[i−1]×(1+e)同一决策全部成立才long。两参考区间止于i−2，排除被比较收盘/成交额。C[i−1]<min(C[i−31:i−1])或float(C[i−1])<EMAs[i−1]×0.97任一成立退出优先；价格/EMA相等及其余情况保持，低成交额本身不退出，成交额阈值相等可入，无延迟入场记忆。Q为1440个真实UTC分钟quote_volume的Decimal和。','',
 'BTC EMA alpha=2/(s+1)，E0=float(真实数据首日闭合收盘)，Ej=(1−alpha)E[j−1]+alpha×float(Cj)，Python float、adjust=False、跨折不重置；s=10/15/20。ETH固定通道15/30、EMA30±1.25%，同一递推，入场通道突破AND EMA上破，退出通道下破OR EMA下破。每份spec保存完整确切逻辑和组件指纹。','',
 '组合2000USDT的原BTC55%/ETH45%为独立1100/900USDT初始预算。12个新BTC组件各以1100预算执行Decimal28、数量舍入、手续费和预算相关冲击；ETH900只读复用已扣成本完整NAV。父组合只相加绝对NAV一次，不缩放旧1000曲线、不归一化、不转账或维持比例/再平衡。OOS183从现金/desired-cash开始，暖机不产生交易；六折连续，不折间重置。','',
 f"读取完整{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范配置、{len(prior['conclusions'])}份全文结论、7份Freqtrade结果含zip成员、4个OOS源码与3技能。初始16条实际证据均完整、缺0。历史研究配置从{prior['monitor_counts_before']['registered']}新增24，3个持续观察截止另计。",'',
 '## 三项验证与冻结门槛','',
 'Walk-forward：2025、2026分别03-18UTC00:01至09-14UTC00:01，180日/六个连续30日折；180日滚动历史、3日gap、purge0，固定规则无监督标签/模型训练/逐折拟合/优化。前日已闭合后用次日真实历史00:01分钟开盘参考执行，终止平仓计成本。每场景259382个分钟收盘/执行点计算完整连续OOS整体回撤，不平均折回撤。两期历史已反复研究，不能称未触碰测试集。','',
 'Sensitivity：周期×入场带宽9格/年，BTC组件与父组合分别评估；EMA20三格为旧结果，只读保留原门槛结论。旧无BTC EMA基线不进邻域；ETH每年1个固定旧来源，没有新调参。逐变体1/2/3倍成本的收益、整体回撤、Sharpe、Calmar见sensitivity.csv/report.json；126场景/756折含72新场景/432新折与54旧场景/324旧折。相邻Sharpe差超过差异样本标准差2倍仅描述cliff，不是显著性/PBO/DSR证据；边界结果不用于同轮扩大扫描。','',
 'Costs：每侧手续费10bp＋估计半点差1bp＋估计滑点2bp＋0.5×前20完整UTC日未年化样本log波动率×sqrt(订单预算/20日quote ADV)，全部按1/2/3倍率放大。ADV20与信号成交额N40分开，最大参与率0.001。Decimal28、不利PRICE tick、LOT下取整、NOTIONAL和前5完整分钟VWAP百分价格代理独立逐单复核。Oct1交易规则快照为历史假设，缺历史L2/TCA/队列/部分成交/真实IOC接单证明；现货只多，无资金费/借币。','',
 '八个门槛保持：全成本净正、1x≥4/6严格正折、3x整体分钟DD≤25%、3x邻域净正≥60%、1x≥2往返、毛参考盈亏/成本≥2.5、无负余额、终止空仓。新BTC组件和父组合独立判定，不回改旧criteria/status。','',
 f"6个实际阶段和7个只读精确重放阶段退出均0；独立审计72新场景/18,675,504 NAV点、6480次因果决策与{summary['new_component_fills']}笔新组件历史虚拟成交，Pandas独立EMA、排除自身成交额窗口、账务与整体/逐折指标均核对；54旧成本场景只读复核。冻结后金融源码哈希保持。手工期望夹具检验周期差、带宽差、EMA单独退出、低量不强平、无延迟入场及未来尾部隔离，夹具不作收益。失败计数：{comparison['failure_counts']}。",'',
 '## 预定关注EMA15/+1%/−3%与匹配EMA20','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']and x['kind']=='MATCHED_SPAN20');lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x完整DD{z['3']['max_drawdown_pct']:.6f}%，1x正折{c['positive_folds_1x']}/6、{c['status']}；相对同入场/退出带宽EMA20，3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp。3x前五折累计{z['3']['first_five_fold_return_pct']:.6f}%、末折{z['3']['last_fold_return_pct']:.6f}%。")
lines+=['',f"新跨期合格组合中，两期全成本收益及3x回撤均不差且至少一处改善：匹配EMA20为{comparison['jointly_improved_pairs_vs_matched_span20']}组、同资金无BTC EMA为{comparison['jointly_improved_pairs_vs_old_no_BTC_EMA']}组、旧N30/r1原50/50为{comparison['jointly_improved_pairs_vs_old_N30_half']}组；相对无BTC EMA仅两期DD3都下降为{comparison['lower_DD3_pairs_vs_old_no_BTC_EMA']}组。36条年度对照及{len(pairs)}条配对判断见comparison.json。旧N30对照资产分配和成交额参数不同，仅作背景。",'',
 '## 年度组合（各年按1x成本后收益倒序）','','|年|新/旧|BTC EMA周期/入场/退出|原BTC/ETH|初始BTC/ETH USDT|1x%|2x%|3x%|3x分钟DD%|Sharpe3|Calmar3|正折1|成交/往返1|成本1（手续费/冲击）|结论|','|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|']
for c in sorted(parents,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];p=z['1'];rule='无BTC EMA'if c['BTC_EMA_span_days']is None else f"{c['BTC_EMA_span_days']}日/+{100*c['BTC_EMA_entry_band_fraction']:g}%/−3%";lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{rule}|55/45|1100/900|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{z['3']['sharpe_365']}|{z['3']['calmar']}|{c['positive_folds_1x']}/6|{p['executions']}/{p['round_trips']}|{p['cost_usdt']:.6f}（{p['cost_parts_usdt']['fee']:.6f}/{p['cost_parts_usdt']['impact']:.6f}）|{c['status']} {'/'.join(c.get('failed_criteria',[]))}|")
lines+=['','## 单币组件（同一年度按1x净收益倒序）','','|年/币|新/旧|BTC EMA周期/入场/退出；ETH固定|本金USDT|1x%|2x%|3x%|3x整体分钟DD%|1x正折|状态|','|---|---|---|---:|---:|---:|---:|---:|---|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];rule='ETH EMA30±1.25%'if c['asset']=='ETH'else'BTC 无EMA'if c['BTC_EMA_span_days']is None else f"BTC EMA{c['BTC_EMA_span_days']} +{100*c['BTC_EMA_entry_band_fraction']:g}%/−3%";lines.append(f"|{c['year']}/{c['asset']}|{'新'if c['is_new']else'旧只读'}|{rule}|{c['capital_usdt']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{c['status']}|")
lines+=['','## 预定组合逐折（全部756折另存folds.csv）','','|年|成本倍率|折|净收益%|完整分钟DD%|Sharpe365|Calmar|','|---|---|---|---:|---:|---:|---:|']
for c in focus:
 for k,z in c['scenes'].items():
  for ff in z['folds']:lines.append(f"|{c['year']}|{k}x|{ff['fold']}|{ff['net_return_pct']:.6f}|{ff['max_drawdown_pct']:.6f}|{ff['sharpe_365']}|{ff['calmar']}|")
lines+=['','## 参数平台与路径重复','','|年/对象|3x净正率|3x正Sharpe率|完整门槛通过率|cliff/邻边|最高3x收益周期/入场|边界|','|---|---:|---:|---:|---|---|---|']
for name,z in surfaces.items():lines.append(f"|{name}|{100*z['positive3_fraction']:.3f}%|{100*z['positive_sharpe3_fraction']:.3f}%|{100*z['full_gate_pass_fraction']:.3f}%|{z['cliff_flags']}/{z['edges']}|{z['best_return3_coordinates']}|{z['best_on_boundary']}|")
lines+=['',f"72新场景中{h['new_scenes_already_in_any_prior_report']}曾见、{h['new_scenes_not_in_any_prior_report']}未见，去重{h['distinct_new_scene_paths_not_in_prior']}种未见单场景。{len(summary['new_both_periods_passed_combination_pairs'])}合格参数有{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见完整跨期路径。参数/路径新颖不等于独立市场样本，所有负/零折和淘汰保留；重复开发、多重选择、边界峰值不能冒充稳健实盘盈利。",'',
 '## 同期旧基准与理论现金','','SMA65±1%原75/25、持有原50/50均为已有2000USDT历史，只读背景，敞口与本轮不同。USDT现金0为分析零线，不是新回测。','','|年|基准/原权重|1x%|2x%|3x%|3x分钟DD%|','|---|---|---:|---:|---:|---:|']
for bg in r['read_only_background'].values():
 z=bg['scenes'];lines.append(f"|{bg['year']}|{bg['kind']}/{bg['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 原SMA延迟shadow与十策略隔离',''];legacy=f['configs']['forward_snapshot_combo']['scenes'];shadow=f"原SMA65/1%原75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}，原{fr['prior_NAV_points']}点前缀精确保留，增加120闭合分钟mark，现{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟、{fr['cumulative_minutes']//1440}完整日。新增日决策/参考点/成交均0，原float现金/数量/desired/trades/费用不变，不强平或回改舍入。下一决策2026-10-12T00:01:00Z，原2027-03-31结束安排保持。1/2/3x累计{legacy['1']['net_return_pct']:.6f}%/{legacy['2']['net_return_pct']:.6f}%/{legacy['3']['net_return_pct']:.6f}%。真实公开GET晚于被标记分钟，属于延迟shadow重建，不能当十策略当时实时报价前向业绩。未满180天/六窗，partial rejected不取消计划。"
lines+=[shadow,'',f"P01–P10保持第{paper['actual_quote_observations']}次真实报价观察，UTC {paper['observed_at_utc']}、实际{paper['elapsed_seconds']/3600:.6f}小时、主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。两段缺口与{100*paper['coverage_fraction']:.6f}%计数/时长覆盖代理保留，非分钟连续覆盖。本轮未运行paper执行器，冻结plan/state/规则/本金/数量/现金/desired/已处理日线/成本/交易ID及旧观察完整保持，不补单。监控源码保持原哈希，只读生成汇总，不新建成交，不改网页源码、不重部署或重复创建任务。",'',
 f"精确离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`；7阶段只读，无HTTP/ledger或账户写入。4份真实525600行分钟parquet及日聚合/完整交易/过滤快照/源码哈希见data_manifest.json/report.json；shadow原始响应、时间及哈希留档。大行情/NPY留忽略data，所有结果包括负折、零折、淘汰永久保留。",'',
 '## 一手资料','',
 '[Binance公开历史](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[现货REST](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md)、[过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)与[pandas EMA递推](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)本轮读取成功；来源支持字段/时序/递推定义，收益与成本来自本地实际计算。访问时间见sources.json；文档当前3.0.6，运行版本2.2.3单独记录，不混同版本。']
lines+=['','## 留档的工程准备修正','','生成只读最终核验源码时，旧的宽泛字面量防残留检查将合法15日通道/关注周期与36条对照计数误判，builder退出1；实际回测、两项独立审计及finish均已退出0。保留verify_builder_before.py与verification_preparation_failure.json，改为核对具体旧批次数及标签残留后生成verify.py，修复后builder见verify_builder_repaired.py。未改金融规则、参数、结果/门槛或重新获取报价/运行收益计算。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA延迟shadow续接\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：BTC EMA10/15/20日 × 入场0.5/1/1.5%、退出3%固定，通道15/30＋成交额N40≥1.1、ETH EMA30±1.25%、原55/45独立1100/900固定。12新BTC＋12组合/72场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，失败{comparison['failure_counts']}；{len(summary['new_both_periods_passed_combination_pairs'])}跨期合格、{h['qualified_cross_period_pairs_not_in_any_prior_report']}新完整跨期路径。匹配EMA20对照联合改善{comparison['jointly_improved_pairs_vs_matched_span20']}组，无BTC EMA对照{comparison['jointly_improved_pairs_vs_old_no_BTC_EMA']}组；10旧组件＋8旧组合/54场景只读。原SMA09→11UTC仅120mark/0新交易，paper44保持；复用历史不称稳定实盘盈利。\n"
(T/'README_entry.md').write_text(entry);marker='## 最近完成的轮次\n\n';base=prior['read_automation_README']['text'];out=base.replace(marker,marker+entry+'\n',1);assert(R/'research/automation/README.md').read_text()in(base,out);(R/'research/automation/README.md').write_text(out)
print(json.dumps({'passed':True,'new_qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'joint_improvements_matched':comparison['jointly_improved_pairs_vs_matched_span20'],'joint_improvements_no_BTC_EMA':comparison['jointly_improved_pairs_vs_old_no_BTC_EMA'],'both_years_DD3_lower_pairs':comparison['lower_DD3_pairs_vs_old_no_BTC_EMA'],'new_cross_period_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'failure_counts':comparison['failure_counts']}))
