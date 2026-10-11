"""Actual BTCvolume+EMA neighbourhood,matching controls and separate legacy shadow."""
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
comparisons=[]
for c in parents:
 if not c['is_new']:continue
 old=next(x for x in parents if x['year']==c['year']and not x['is_new'])
 halfref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='OLD_N30_R1_HALF');half=external[halfref['name']]
 symref=next(x for x in r['plan']['read_only_comparator_refs']if x['year']==c['year']and x['kind']=='MATCHED_SYMMETRIC_BTC_EMA'and x['matched_entry_band_fraction']==c['BTC_EMA_entry_band_fraction']);sym=external[symref['name']]
 for kind,o in [('MATCHED_SYMMETRIC',sym),('OLD_NO_BTC_EMA',old),('OLD_N30_HALF',half)]:
  comparisons.append({'config':c['name'],'year':c['year'],'kind':kind,'comparator':o['name'],'comparator_is_new':False,'config_raw_weights':c['raw_weights'],'control_raw_weights':o['raw_weights'],'config_component_capitals':funds(c['raw_weights']),'control_component_capitals':funds(o['raw_weights']),'same_total_capital_usdt':2000,'return_differences_pp':{k:c['scenes'][k]['net_return_pct']-o['scenes'][k]['net_return_pct']for k in('1','2','3')},'minute_DD3_difference_pp':c['scenes']['3']['max_drawdown_pct']-o['scenes']['3']['max_drawdown_pct'],'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==o['scenes'][k]['NAV_sha256_f64le']for k in('1','2','3'))})
pairs=[]
for pair in summary['new_both_periods_passed_combination_pairs']:
 for kind in('MATCHED_SYMMETRIC','OLD_NO_BTC_EMA','OLD_N30_HALF'):
  rows=[next(x for x in comparisons if x['config']==n and x['kind']==kind)for n in pair];rv=[v for x in rows for v in x['return_differences_pp'].values()];dd=[x['minute_DD3_difference_pp']for x in rows]
  pairs.append({'pair':pair,'kind':kind,'joint_improvement_both_years':all(v>=0 for v in rv)and all(v<=0 for v in dd)and(any(v>0 for v in rv)or any(v<0 for v in dd)),'lower_DD3_both_years':all(v<0 for v in dd),'whole_path_seen_before':next(x['whole_path_seen_before']for x in h['qualified_pair_histories']if x['pair']==pair)})
surfaces={}
for name,sens in r['sensitivity'].items():
 year,role=name.split('_');cells=[c for c in cs.values()if c['year']==year and c['sensitivity_member']and(c.get('asset')==role or c['role']==role)];best=max(c['scenes']['3']['net_return_pct']for c in cells);coords=[[c['BTC_EMA_entry_band_fraction'],c['BTC_EMA_exit_band_fraction']]for c in cells if c['scenes']['3']['net_return_pct']==best]
 surfaces[name]={'cells':len(cells),'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cells)/len(cells),'full_gate_pass_fraction':sum(c['status']=='passed'for c in cells)/len(cells),'cliff_flags':sum(e['cliff_flag_2sd']for e in sens['adjacent_edges']),'edges':len(sens['adjacent_edges']),'best_return3_coordinates':coords,'best_on_boundary':None if role=='ETH'else any(span in(.005,.015)or band in(.02,.04)for span,band in coords),'scope':'ETH is one fixed read-only source,not a new sweep'if role=='ETH'else'NewBTC/parent9cell entry/exitbandgrid;oldcontrols excluded'}
comparison={'report_sha256':sha(T/'report.json'),'comparisons':comparisons,'qualified_pair_comparisons':pairs,'jointly_improved_pairs_vs_matched_symmetric':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='MATCHED_SYMMETRIC'),'jointly_improved_pairs_vs_old_no_BTC_EMA':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_NO_BTC_EMA'),'jointly_improved_pairs_vs_old_N30_half':sum(x['joint_improvement_both_years']for x in pairs if x['kind']=='OLD_N30_HALF'),'lower_DD3_pairs_vs_old_no_BTC_EMA':sum(x['lower_DD3_both_years']for x in pairs if x['kind']=='OLD_NO_BTC_EMA'),'failure_counts':dict(Counter(k for c in fresh for k in c['failed_criteria'])),'surfaces':surfaces,'scope':'Primary matchedsame-entry-band R38EMA20 symmetriccontrols atsame1100/900/raw55/45;secondarysamefundsnoBTCEMA baseline. Channel15/30,N40/r1.1 andETHfixed. SecondaryoldN30/r1raw50/50 total2000 hasdifferentassetexposure/volumeparameters. Oldcriteria/status preserved;histories repeatedlyused.'}
(T/'comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
with(T/'folds.csv').open('w',newline='')as file:
 w=csv.writer(file,lineterminator='\n');w.writerow(['config','year','role','is_new','BTC_initial_weight','BTC_EMA_entry_band_fraction','BTC_EMA_exit_band_fraction','cost','fold','net_return_pct','minute_DD_pct','Sharpe365','Calmar'])
 for c in cs.values():
  for k,z in c['scenes'].items():
   for ff in z['folds']:w.writerow([c['name'],c['year'],c['role'],c['is_new'],c['BTC_initial_weight'],c['BTC_EMA_entry_band_fraction'],c['BTC_EMA_exit_band_fraction'],k,ff['fold'],ff['net_return_pct'],ff['max_drawdown_pct'],ff['sharpe_365'],ff['calmar']])
metrics=[('net_return_pct','3x cumulative net return %'),('max_drawdown_pct','3x whole-minute NAV drawdown %'),('sharpe_365','3x daily Sharpe (365)')]
for role,filename in [('combination','sensitivity.png'),('BTC','sensitivity_BTC.png')]:
 fig,axes=plt.subplots(2,3,figsize=(15,9),layout='constrained')
 for row,year in enumerate(('2025','2026')):
  cells={(c['BTC_EMA_entry_band_fraction'],c['BTC_EMA_exit_band_fraction']):c for c in cs.values()if c['year']==year and c['is_new']and(c['role']==role or c.get('asset')==role)}
  for col,(metric,label)in enumerate(metrics):
   ax=axes[row,col];matrix=np.array([[cells[span,band]['scenes']['3'][metric]for span in grid['BTC_EMA_entry_band_fraction']]for band in grid['BTC_EMA_exit_band_fraction']]);im=ax.imshow(matrix,cmap='YlOrRd'if col==1 else'YlGnBu',aspect='auto')
   for i,band in enumerate(grid['BTC_EMA_exit_band_fraction']):
    for j,span in enumerate(grid['BTC_EMA_entry_band_fraction']):ax.text(j,i,f'{matrix[i,j]:.3f}'+(' P'if cells[span,band]['status']=='passed'else' R'),ha='center',va='center',fontsize=10,color='white'if matrix[i,j]>(matrix.min()+matrix.max())/2 else'#111')
   ax.set(xticks=range(3),xticklabels=['0.5%','1%','1.5%'],yticks=range(3),yticklabels=['2%','3%','4%'],xlabel='BTC EMA20 entry band',ylabel='BTC EMA20 exit band',title=year+' | '+label);ax.title.set_fontsize(10);fig.colorbar(im,ax=ax,fraction=.035)
 title='BTC own1100USDT volume/channel+asymmetric EMA20'if role=='BTC'else'BTCvolume/channel+asymmetric EMA20 x fixed ETHchannel/EMA30 | raw55/45,own1100/900'
 fig.suptitle(title+'\nEntry15/exit30,N40/min1.1 fixed | P/R=annual gates | repeated histories',fontsize=14);fig.savefig(T/filename,dpi=130);plt.close(fig)
fr=r['plan']['forward_resume'];paperstate=read(R/'research/paper10/state.json');paper=read(R/'research/paper10/observations'/paperstate['last_observation_id']/'summary.json');focus=sorted([c for c in parents if c['is_new']and c['BTC_EMA_entry_band_fraction']==.005 and c['BTC_EMA_exit_band_fraction']==.03],key=lambda c:c['year'])
lines=['# BTC EMA20非对称入场/退出过滤：ETH与原55/45固定','',f"36个新历史配置：18个BTC组件＋18个年度组合，108个成本场景实际执行；1x净正{summary['positive_1x']}、3x净正{summary['positive_3x']}，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰。{len(summary['new_both_periods_passed_combination_pairs'])}组新参数跨期合格。4旧组件＋2旧父组合/18场景及6匹配对称EMA、2旧N30中心只读。另3个原SMA shadow截止；共39项先reserve、实际执行与独立审计后finish。",'',
 '## 事前假设与完整规则','',
 '上轮BTC EMA过滤降低部分回撤但牺牲2026收益。本轮事前固定EMA20，联合测试入场0.5%/1%/1.5% × 退出2%/3%/4%，关注+0.5%/−3%，检验宽退出能否减少过早离场。选择EMA20及邻域依据已反复使用的上轮开发历史，包括边界结果，不冒充未触碰验证。通道15/30、成交额N40≥1.1、ETH EMA30±1.25%、原55/45与成本/门槛固定，不按本轮OOS扩参。六个同入场带宽、EMA20对称父组合作只读匹配对照。','',
 'BTC决策i只看已闭合C[i−1]/Q[i−1]：C[i−1]>max(C[i−16:i−1])、Q[i−1]≥1.1×mean(Q[i−41:i−1])且参考均值>0、float(C[i−1])>EMA20[i−1]×(1+e)必须同一决策均成立才long。两参考区间均止于i−2，排除被比较收盘/成交额。C[i−1]<min(C[i−31:i−1])或float(C[i−1])<EMA20[i−1]×(1−d)任一成立退出优先。e=0.5/1/1.5%，d=2/3/4%，二者独立；其他/价格或EMA相等保持，低成交额自身不退出，成交额阈值相等可入，无延迟入场记忆。Q为1440个真实UTC分钟quote_volume的Decimal和。','',
 'BTC EMA alpha=2/21，E0=float(数据首日闭合收盘)，Ej=(1−alpha)E[j−1]+alpha×float(Cj)，adjust=False、跨折不重置。ETH同一定义固定s30/b1.25%，入场通道突破AND EMA上破，退出通道下破OR EMA下破。逐spec完整逻辑、组件指纹、源码哈希保留。','',
 '每个组合2000USDT、原BTC55%/ETH45%对应独立1100/900USDT；新BTC组件各自以1100预算运行Decimal28、数量舍入、手续费与预算相关冲击，ETH900只读复用完整已扣成本NAV。父组合只加一次绝对NAV，不缩放旧1000曲线、不归一化、转账、维持比例或再平衡。OOS183初始现金/desired-cash，暖机不生成交易或历史持仓，跨六折连续。','',
 f"完整读取{prior['lines']}行登记、{prior['preserved_ids']}保留ID/{prior['canonical']}规范配置、{len(prior['conclusions'])}份全文结论、7份Freqtrade结果、4个OOS源码、任务/监控说明及3技能。初始16条均有实际证据，缺结果0。历史试验从{prior['monitor_counts_before']['registered']}新增36，观察截止另计。",'',
 '## 三项验证、门槛与实际检查','',
 'Walk-forward：2025和2026分别03-18UTC00:01至09-14UTC00:01，各180日/6个连续30日折；180日滚动历史、3日gap、purge0，无模型/标签/逐折拟合/优化。前日闭合后在次日真实历史00:01分钟开盘参考执行，终止平仓计成本。每场景259382个分钟收盘/执行点计算连续OOS整体回撤，不平均折回撤。两段历史已反复研究，不是未触碰最终测试集。','',
 'Sensitivity：BTC EMA20入场带宽×退出带宽联合9格/年，组件和父组合分别评估。旧无BTC EMA基准、6个匹配对称父组合均不混入邻域；ETH每年1个固定旧来源无新扫描。126场景/756折保存，其中108新场景/648折、18旧场景/108折。相邻Sharpe差超过差异样本标准差2倍仅描述cliff，非统计显著性/PBO/DSR；边界峰值不用于同轮扩参。','',
 'Costs：每侧手续费10bp、估计半点差1bp、估计滑点2bp，加0.5×滞后20完整UTC日未年化样本log波动率×sqrt(订单预算/20日quote ADV)冲击，全部同倍率×1/2/3。ADV固定20，与信号成交额N40分开，最大参与率0.001。Decimal28、不利PRICE tick、LOT下取整、NOTIONAL及前5完整分钟VWAP百分价格代理逐单复核。Oct1过滤快照在历史是估计，缺历史L2/TCA、队列、部分成交或真实IOC接单证明；现货仅多，资金费/借币不适用。','',
 '冻结八门槛：全成本净正、1x≥4/6严格正折、3x整体分钟DD≤25%、3x邻域净正≥60%、1x≥2往返、毛参考盈亏/成本≥2.5、无负余额、终止空仓。新组件和父组合独立判断，旧criteria/status不回改，所有负折/零折及淘汰保留。','',
 f"独立审计108新场景/28,013,256 NAV点、9720次BTC因果决策（Pandas独立EMA＋排除自身的成交额参考）和{summary['new_component_fills']}笔新BTC历史虚拟成交，18旧场景完整分钟NAV只读复核。6个实际阶段首次退出0，7个只读精确重放阶段退出0；金融源码冻结后未改。手工期望夹具核对EMA过滤、仅EMA退出、低成交额不强制退出、无延迟入场与未来尾部隔离，夹具不作收益证据。失败计数{comparison['failure_counts']}。",'',
 '## 预定关注BTC EMA20 +0.5%/−3%与对照','']
for c in focus:
 z=c['scenes'];a=next(x for x in comparisons if x['config']==c['name']and x['kind']=='MATCHED_SYMMETRIC')
 lines.append(f"{c['year']}：1/2/3x净收益{z['1']['net_return_pct']:.6f}%/{z['2']['net_return_pct']:.6f}%/{z['3']['net_return_pct']:.6f}%，3x完整DD{z['3']['max_drawdown_pct']:.6f}%，状态{c['status']}；相对同入场带宽的EMA20对称对照，3x收益差{a['return_differences_pp']['3']:.6f}pp、DD差{a['minute_DD3_difference_pp']:.6f}pp。")
lines+=['',f"跨期合格参数中，两期所有成本收益及3x回撤均不差且至少一处改善：相对匹配对称EMA为{comparison['jointly_improved_pairs_vs_matched_symmetric']}组、同资金旧无BTC EMA为{comparison['jointly_improved_pairs_vs_old_no_BTC_EMA']}组，相对旧N30/r1原50/50为{comparison['jointly_improved_pairs_vs_old_N30_half']}组；仅3x回撤两期都下降为{comparison['lower_DD3_pairs_vs_old_no_BTC_EMA']}组，不能忽略收益代价。54条年度比较及{len(pairs)}条配对判断见comparison.json。主对照匹配EMA20入场带宽、资金、通道/成交额及ETH规则，仅改变退出带宽；次对照总资金2000相同但资产敞口和成交额参数不同。",'',
 '## 全部年度组合（各年按1x净收益倒序）','','|年份|新/旧|BTC EMA20入场/退出|原BTC/ETH|初始BTC/ETH USDT|1x%|2x%|3x%|3x完整DD%|正折1|成交/往返1|成本1（手续费/冲击）|状态/失败|','|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|']
for c in sorted(parents,key=lambda c:(c['year'],-c['scenes']['1']['net_return_pct'],c['name'])):
 z=c['scenes'];a=z['1'];cp=a['cost_parts_usdt'];axis=f"+{100*c['BTC_EMA_entry_band_fraction']:g}%/−{100*c['BTC_EMA_exit_band_fraction']:g}%"if c['is_new']else'无BTC EMA';failed=[k for k,v in c['criteria'].items()if not v]
 lines.append(f"|{c['year']}|{'新'if c['is_new']else'旧只读'}|{axis}|55/45|1100/900|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['executions']}/{a['round_trips']}|{a['cost_usdt']:.6f}（{cp['fee']:.6f}/{cp['impact']:.6f}）|{c['status']}/{failed}|")
lines+=['','## 全部组件与资金/失败条件','','|年份|币种|新/旧|资金USDT|BTC EMA20入场/退出|1x%|2x%|3x%|3x完整DD%|正折1|往返1|状态/失败|','|---|---|---|---:|---|---:|---:|---:|---:|---|---:|---|']
for c in sorted([c for c in cs.values()if c['role']=='component'],key=lambda c:(c['year'],c['asset'],c['BTC_EMA_entry_band_fraction']or 0,c['BTC_EMA_exit_band_fraction']or 0)):
 z=c['scenes'];a=z['1'];axis=f"+{100*c['BTC_EMA_entry_band_fraction']:g}%/−{100*c['BTC_EMA_exit_band_fraction']:g}%"if c['is_new']else'ETH EMA30±1.25%固定'if c['asset']=='ETH'else'旧BTC无EMA';failed=[k for k,v in c['criteria'].items()if not v]
 lines.append(f"|{c['year']}|{c['asset']}|{'新'if c['is_new']else'旧只读'}|{c['capital_usdt']}|{axis}|{a['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|{c['positive_folds_1x']}/6|{a['round_trips']}|{c['status']}/{failed}|")
lines+=['','## 平台、边界及重复路径','','|年份/对象|3x净正率|完整门槛通过率|cliff/邻边|最高3x收益入场/退出|边界|','|---|---:|---:|---|---|---|']
for name,z in surfaces.items():lines.append(f"|{name}|{100*z['positive3_fraction']:.3f}%|{100*z['full_gate_pass_fraction']:.3f}%|{z['cliff_flags']}/{z['edges']}|{z['best_return3_coordinates']}|{z['best_on_boundary']}|")
lines+=['',f"108新场景中{h['new_scenes_already_in_any_prior_report']}曾见、{h['new_scenes_not_in_any_prior_report']}未见，去重{h['distinct_new_scene_paths_not_in_prior']}种未见单场景。{len(summary['new_both_periods_passed_combination_pairs'])}合格参数只有{h['qualified_cross_period_pairs_not_in_any_prior_report']}种未见完整跨期路径。参数/路径新颖不等于独立市场样本；旧淘汰、边界峰值与大量历史选择偏差全部披露，不称稳定实盘盈利。",'',
 '## 既有同期基准与现金','','旧SMA65±1%原75/25及持有原50/50均为已有2000USDT历史，只读背景；敞口与本轮不同。现金是无收益USDT理论零线，不是新回测。','','|年份|旧基准/原权重|1x%|2x%|3x%|3x完整分钟DD%|','|---|---|---:|---:|---:|---:|']
for bg in r['read_only_background'].values():
 z=bg['scenes'];lines.append(f"|{bg['year']}|{bg['kind']}/{bg['raw_weights']}|{z['1']['net_return_pct']:.6f}|{z['2']['net_return_pct']:.6f}|{z['3']['net_return_pct']:.6f}|{z['3']['max_drawdown_pct']:.6f}|")
lines+=['|各期|USDT理论现金|0|0|0|0|','','## 原冻结SMA延迟shadow与十策略隔离',''];legacy=f['configs']['forward_snapshot_combo']['scenes'];shadow=f"原SMA65/1%原75/25延迟shadow {fr['resume_utc']}→{fr['cutoff_utc']}，原{fr['prior_NAV_points']}点前缀精确保留，增加120闭合分钟mark，现{fr['total_NAV_points']}点/{fr['cumulative_minutes']}分钟、9完整日。新增日线决策/参考点/成交均0，原float现金/数量/desired/trades/费用不变，无强制平仓/数量舍入回改；下一决策2026-10-12T00:01:00Z，原2027-03-31结束安排保持。1/2/3x累计{legacy['1']['net_return_pct']:.6f}%/{legacy['2']['net_return_pct']:.6f}%/{legacy['3']['net_return_pct']:.6f}%。真实公开GET取得时间晚于被标记分钟，属于延迟shadow重建，不能当十策略当时实时报价前向业绩。不足180天/六窗，partial rejected不取消持续计划。"
lines+=[shadow,'',f"P01–P10保持第{paper['actual_quote_observations']}次真实报价观察，UTC {paper['observed_at_utc']}、实际{paper['elapsed_seconds']/3600:.6f}小时、主账户合计{paper['totals_by_cost']['1']['NAV_usdt']}USDT。两段旧缺口与{100*paper['coverage_fraction']:.6f}%计数/时长覆盖代理保留，非连续分钟覆盖。监控只增加非对称EMA参数标签，3579个旧ID标签逐字保持；旧汇总源码保存在monitor_snapshot_before.py，before/after哈希见monitor_label_checks.json。该只读源码哈希更新已显式留档，后续账户预检应按记录接受此标签迁移，不能回改旧预检记录。本轮未运行paper执行器，不改规则/本金/数量/现金/desired/已处理日线/费用/交易ID，不补单；其回撤仅真实报价采样，180天/六窗未成熟。网页只读汇总，不重部署或创建重复定时任务。",'',
 f"精确离线复现：`.venv/bin/python research/experiments/{T.name}/replay_verify.py`，7阶段只读，不HTTP、不写登记/账户。4份真实525600行分钟parquet、日聚合、全部交易、过滤快照及源码SHA见data_manifest.json/report.json；shadow公开GET原始响应和延迟见forward_report.json。大行情/NPY留忽略data，全部正负/零折和淘汰保存；未来另轮预登记，不回改本轮OOS/门槛，不替换固定P01–P10。",'',
 '## 一手资料','',
 '[Binance公开历史数据](https://raw.githubusercontent.com/binance/binance-public-data/master/README.md)、[官方现货REST](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/rest-api.md)、[官方过滤规则](https://raw.githubusercontent.com/binance/binance-spot-api-docs/master/filters.md)本轮读取成功，时间见sources.json/source_access.json；支持字段、UTC和过滤语义，成本估计及收益来自本地实际执行研究。']
(T/'result.md').write_text('\n'.join(lines)+'\n');(T/'forward_result.md').write_text('# 原冻结SMA延迟shadow续接\n\n'+shadow+'\n')
entry=f"- [{T.name}](../experiments/{T.name}/result.md)：BTC EMA20入场0.5/1/1.5% × 退出2/3/4%联合，通道15/30＋成交额N40≥1.1、ETH EMA30±1.25%、原55/45独立1100/900固定。18新BTC＋18父组合/108场景实算，{len(summary['passed'])}通过、{len(summary['rejected'])}淘汰，失败{comparison['failure_counts']}；{len(summary['new_both_periods_passed_combination_pairs'])}跨期合格、{h['qualified_cross_period_pairs_not_in_any_prior_report']}新完整跨期路径。相对同入场的6个EMA20对称父组合联合改善{comparison['jointly_improved_pairs_vs_matched_symmetric']}组，无BTC EMA对照{comparison['jointly_improved_pairs_vs_old_no_BTC_EMA']}组；旧4组件＋2父组合/18场景及2旧N30只读。标签仅支持非对称阈值，3579旧ID标签不变，before/after哈希及旧源码留档，后续预检显式接受此只读标签迁移。原SMA07→09UTC仅120mark/0新交易，paper43保持；复用历史不称实盘盈利。\n"
(T/'README_entry.md').write_text(entry);marker='## 最近完成的轮次\n\n';base=prior['read_automation_README']['text'];out=base.replace(marker,marker+entry+'\n',1);assert(R/'research/automation/README.md').read_text()in(base,out);(R/'research/automation/README.md').write_text(out)
print(json.dumps({'passed':True,'new_qualified_pairs':len(summary['new_both_periods_passed_combination_pairs']),'joint_improvements_matched':comparison['jointly_improved_pairs_vs_matched_symmetric'],'joint_improvements_no_BTC_EMA':comparison['jointly_improved_pairs_vs_old_no_BTC_EMA'],'both_years_DD3_lower_pairs':comparison['lower_DD3_pairs_vs_old_no_BTC_EMA'],'new_cross_period_paths':h['qualified_cross_period_pairs_not_in_any_prior_report'],'failure_counts':comparison['failure_counts']}))
