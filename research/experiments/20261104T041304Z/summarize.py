"""Saved native/parent S/E surfaces, all folds, controls and provenance; no simulation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());rows={}
def write(name,cols,items):
 with (R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];recent=[];daily=[];edges=[];sources=[];alloc=[]
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['H'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_reversal_L','symmetric_entry_fraction_H','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_reversal_L','symmetric_entry_fraction_H','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_reversal_L','symmetric_entry_fraction_H','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_reversal_L','symmetric_entry_fraction_H','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['hurdles'].index(g['H']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['H']==g['H'] or j<2 and h['H']==p['hurdles'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['H'],h['L'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];threshold=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(v)>threshold,'scope':'Dependentedge descriptive heuristic only,not significance/DSR/PBO or a posthoc gate.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
external=[]
for fp in p['external_control_fingerprints']:
 ref=p['read_only_references'][fp];c=next(x for x in json.loads((ROOT/ref['report']).read_text())['configs'].values() if x['fingerprint']==fp)
 for k,s in c['scenes'].items():external.append([c['name'],fp,ref['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status'],ref['report'],ref['report_sha256']])
write('readonly_reused_scenes.csv',['configuration','fingerprint','capital','cost_multiplier','return_pct','whole_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','unchanged_canonical_status','original_report','report_sha256'],external);write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_H','to_L','to_H','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());c=next(z for z in json.loads((ROOT/x['report']).read_text())['configs'].values() if z['fingerprint']==fp)
 for k,s in c['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256'],True])
for c in r['configs'].values():
 if c['scope']!='native':continue
 for k,s in c['scenes'].items():sources.append([c['fingerprint'],c['asset'],c['capital_usdt'],4500,k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],rel(R/'report.json'),sha(R/'report.json'),False])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','provenance_report','report_sha256','readonly_old'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['H'],3750,15000,18750,500,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,500,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','symmetric_entry_fraction_H','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc);put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750/N500+ETH15000/N4500 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['hurdles'].index(c['H'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['H1.5%','H2%','H2.5%']);ax.set_yticks(range(3),['L3','L5','L7']);ax.set_xlabel('ETH symmetric reversal entry H (%)');ax.set_ylabel('ETH reversal lookback L (days)');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['hurdles'].index(c['H']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH finite EWM32-gated reversal L3/5/7 x H1.5/2/2.5% | fixed E0.5%,V10/cap4.5%\nBTC3750/N500 + ETH15000/N4500 | raw[1,1],capitalshares20/80%,noNAVscaling | All grids N=newnative/parent; matchedSMA32 controls readonly outsidegrid | reused history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');eq=[]
def compare(c,base):
 return {k:{'return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'control_return_pct':base['scenes'][k]['net_return_pct'],'control_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_control_pp':z['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_control_pp':z['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct'],'new_recent_positive5d':sum(f['net_return_pct']>0 for f in z['recent40']['folds']),'control_recent_positive5d':sum(f['net_return_pct']>0 for f in base['scenes'][k]['recent40']['folds'])} for k,z in c['scenes'].items()}
for c in r['configs'].values():
 if c['scope']!='parent':continue
 control_fp=p['matched_old_estimator'][c['fingerprint']];ref=p['read_only_references'][control_fp];base=next(z for z in json.loads((ROOT/ref['report']).read_text())['configs'].values() if z['fingerprint']==control_fp)
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'L':c['L'],'H':c['H'],'S':32,'E':.005,'N':500,'control_fingerprint':control_fp,'control_report':ref['report'],'control_report_sha256':ref['report_sha256'],'same_capital_and_budgets':True,'same_LH_and_costs':True,'new_estimator':'finiteEWM32_beta31/33','control_estimator':'SMA32','all_cost_NAV_identical':all(z['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k,z in c['scenes'].items()),'cost_comparisons':compare(c,base)})
assert len(eq)==9;put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'scope':'MatchedsameL/H S32/E.005oldSMA32control foreachnewfiniteEWM32parent;sameactualcapital/N/costs/calendar. Alloldcontrolsreadonly,noextrafinancialvaluation.'})
groups={}
for c in r['configs'].values():
 if c['scope']=='parent':groups.setdefault('|'.join(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),[]).append(c['fingerprint'])
put(R/'prior_grid_NAV_aliases.json',{'new_definitions_matching_a_prior_path':sum(x['all_cost_NAV_identical'] for x in eq),'within_new_parent_grid_alias_groups':[v for v in groups.values() if len(v)>1],'scope':'Fullbank parent hashes only;native and parent capitals not compared as equal.'})
newfps={c['fingerprint'] for c in r['configs'].values()};hist={}
for fp,z in records.items():
 sp=z.get('spec',{});obs=sp.get('family')=='paper-live-portfolio-observation' or sp.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in sp.get('parameters',{})
 if fp in newfps or not sp or obs:continue
 hist.setdefault(reg.fingerprint(sp),[]).append(z)
trials={'canonical_prior_research_definitions':len(hist),'registry_marked_actual':sum(any(z.get('result_available') is True for z in zs) for zs in hist.values()),'not_marked_actual':sum(not any(z.get('result_available') is True for z in zs) for zs in hist.values()),'initial16_actual_evidence':16,'new_financial_definitions':18,'new_native_models':9,'new_cost_scenes':54,'observations_excluded':True};put(R/'prior_actual_research_counts.json',trials)
native_comparisons=[]
for c in r['configs'].values():
 if c['scope']!='native':continue
 fp=p['matched_old_estimator'][c['fingerprint']];ref=p['read_only_references'][fp];old=next(z for z in json.loads((ROOT/ref['report']).read_text())['configs'].values() if z['fingerprint']==fp);native_comparisons.append({'fingerprint':c['fingerprint'],'name':c['name'],'L':c['L'],'H':c['H'],'old_SMA32_fingerprint':fp,'old_report':ref['report'],'old_report_sha256':ref['report_sha256'],'same_capital':15000,'same_entry_N':4500,'cost_comparisons':compare(c,old)})
put(R/'matched_SMA_native_comparisons.json',{'report_sha256':sha(R/'report.json'),'comparisons':native_comparisons,'scope':'Savedmetricscomparisononly;no newSMAvaluation,allmatchedL/H,N,capital,costs.'})
lines=['有限窗口 EWM32 趋势门槛与快反转 L/H 联合验证','',p['hypothesis'],'',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论；初始16项实际证据完整，缺结果0。此前研究定义{trials['canonical_prior_research_definitions']}，标实际{trials['registry_marked_actual']}、未标{trials['not_marked_actual']}。不将全部登记当全部实际回测；反复使用历史的多重选择偏差保留。",'', '事前固定 ETH 快反转 L3/5/7×对称入场 H1.5/2/2.5%，E0.5%、entry-only V10/cap4.5%。r=C[i−1]/C[i−1−L]−1；严格r>H做空、r<−H做多，入场等号不触发。否则实际多仓仅在r<E保留、实际空仓仅在r>−E保留，退出等号flat。EWM32=sum((31/33)^j×C[i−1−j],j=0..31)/sum((31/33)^j,j=0..31)，只取此前32个完整收盘，最新完整收盘权重最大；gate=sign(C[i−1]/EWM32−1)，零或相反方向强制flat。它是每天重新限定32日窗口的归一化指数加权均值，不是无限历史递推EMA。仅新增/反向仓位应用过去10日样本logvol门槛，原方向仓位不因单独高波动退出。', '', '九个新ETH原生各本金15000/N4500，真实数量/费用/资金费/风险从冻结日历执行；九个新组合拥有完整BTC3750/N500旧银行+对应ETH15000/N4500新银行。raw[1,1]、总本金18750、资本份额20/80%、初始名义敞口份额2.6666666667/24%。没有组合权重归一化、旧NAV/数量缩放、平均指标、父订单、调仓/转移或交叉保证金。信号内的时间权重归一化属于预先规定的均值公式。22个旧实际结果中12个原生账本/36成本路径只读复用，包含同格L/H、同资本与预算的SMA32原生和组合，以及同资本/预算的常多持有基准，所有旧资格保持。', '', 'Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日，12×30日完整折+10日尾折，逐折不重置现金和持仓，整体DD使用完整分钟/事件净值。近期40日继承day330状态、8×5日。固定规则无拟合/标签、purge0，33日线上下文足够；信号来自完整过去收盘，下一UTC00:01原生OPEN执行，数量按过去收盘/LOT取整，反手先平后开，终点计成本平仓。已反复使用的开发历史不能称未触碰最终测试或独立未来。', '', '成本：5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)。1/2/3倍放大执行支出与资金费支出，资金费收入不放大。使用真实settlement ns/rate/mark和结算时自身持仓；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押与独立1%闭合小时不利mark风险代理均核验。永续空头无现货借币，不虚构借币费用。基准为同资本/预算常多持有及现金0%。缺盘口/TCA、完整历史最大量/保证金层级、逐tick强平及容量证明，正回测不代表稳定实盘盈利。', '', '固定失败门槛：所有成本全期净正；1倍>=9/12盈利完整月；各成本近期净正且>=6/8盈利五日折；3倍整体DD<=25%；L/H索引半径1含中心，邻域3倍净正与严格近期合格比例均>=60%；>=4底层平仓；毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat、>=180日。native和parent分别用预定九格邻域；看到结果后不改门槛或扩本批网格。', '', '|新配置|scope|L日数|H比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+ '|'.join([c['name'],c['scope'],str(c['L']),str(c['H']),*[f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3']],f"{c['scenes']['3']['max_drawdown_pct']:.6f}",str(c['positive_complete_30d_folds_1x']),'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3']),c['status']])+'|')
lines.extend(['',f"九个新组合通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}；九个新原生的独立资格见上表。逐项失败：{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。匹配SMA32对照与同格新旧原生比较另存；同格全成本NAV相同{sum(x['all_cost_NAV_identical'] for x in eq)}/9，网格内别名另存，不把相同净值当独立收益路径。",'', '11CSV完整保留54成本场景、702月/尾折、432近期折、20034日NAV、原生和组合两个九格L/H面、27旧SMA组合场景、72相邻边、27匹配持有/现金比较、63新旧原生成本路径和10组资金配置。正负收益折、完整DD/Sharpe/Calmar、费用与实际成交数均保留。边界最高Sharpe与相邻cliff均如实记录，只是依赖样本的描述性诊断，不是DSR/PBO显著性或新增裁定条件。', '', '来源：2026-11-04UTC阅读 [Pandas官方EWM公式](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html) 和 [Binance USD-M官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。有限32日窗口是本项目预定研究变体；不移植文档之外的收益或成交能力。8个行情/mark/资金费/约束文件、spec/report/archive/实现和数据SHA见plan/data_manifest。', '', '首个实际金融reserve之前绑定33份研究源码，旧simulate函数AST保持，仅改ETH门槛；合成检查以独立整数权重核对有限EWM、时序、等号和波动过滤。所有18配置分三批reserve成功后，实际计算27原生+27父成本路径；独立信号审计用相反遍历方向的Fraction Horner公式，独立复核Decimal现金/LOT/tick/冲击/资金费、小时风险和完整NAV，再逐配置finish。', '', '原SMA65与single续Nov4UTC00:30→02:30，原L4续02:10→04:10，均在所需参考闭合后采集；延续原本金、冻结规则、逐成本状态和完整NAV前缀，不重复已处理的Nov4午夜决策/资金费。原SMA65保留最新65日上下文源20261104T021133Z/forward_inputs.json.gz。真实事件以各自响应为准，不预设资金费/成交结果；本批EWM研究不写入冻结账户。partial不冒充180日/六折，旧延迟shadow与十策略真实报价模拟分开。', '', '只清理本轮可重建中间物；完整账户账本、冻结规则、登记、正负结果、必要代码和原始短窗/失败证据均保留。同main排他锁内更新只读监控、普通非强制push；实际发布终态/完整远端tree与blob哈希/解锁凭据见.git/automation_proofs/'+R.name+'.json。'])
(R/'result.md').write_text('\n'.join(lines).rstrip()+'\n');print(json.dumps(summary),flush=True)
