"""Export saved real native/parent L/D results; no strategy calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());rows={}
def write(name,cols,items):
 with(R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];recent=[];daily=[];edges=[];alloc=[];sources=[]
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['E'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['E'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['E'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','exit_buffer_fraction_E','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','exit_buffer_fraction_E','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','exit_buffer_fraction_E','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','exit_buffer_fraction_E','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['E'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['exit_buffers'].index(g['E']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['E']==g['E'] or j<2 and h['E']==p['exit_buffers'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['E'],h['L'],h['E'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_E','to_L','to_E','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['E'],3750,15000,18750,750,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,750,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','exit_buffer_fraction_E','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['exit_buffers'].index(c['E'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['E0.375%','E0.5% old','E0.625%']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('ETH exit buffer E (%)');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['exit_buffers'].index(c['E']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fast L3/4/5 x exit E0.375/0.5/0.625% | fixed slowS28, V10/cap4.5%, HL1.5%/HS2.5%\nActual BTC3750/N750 + ETH15000/N4500 | raw[1,1], capitalshares20/80%, noNAVscaling | O=readonly,N=new | reused development history')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');eq=[]
for c in r['configs'].values():
 g=next(g for g in p['grid'] if g['L']==c['L'] and g['E']==.005);base=r['all_current_grid'][g['fingerprint']];ar=p['supplemental_N375_parent_controls'][f"{c['L']}/{c['E']}"];assert sha(ROOT/ar['report'])==ar['report_sha256'];ancestor=next(z for z in json.loads((ROOT/ar['report']).read_text())['configs'].values() if z['fingerprint']==ar['fingerprint'])
 co={k:{'return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'control_return_pct':base['scenes'][k]['net_return_pct'],'control_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_control_pp':z['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_control_pp':z['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct']} for k,z in c['scenes'].items()}
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':'parent','role':'candidate','L':c['L'],'E':c['E'],'N':750,'matched_E500_control_fingerprint':g['fingerprint'],'control_fingerprint':g['fingerprint'],'control_report':p['read_only_references'][g['fingerprint']]['report'],'control_report_sha256':p['read_only_references'][g['fingerprint']]['report_sha256'],'all_cost_NAV_identical':all(z['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k,z in c['scenes'].items()),'cost_comparisons':co,'same_E_original_N375_control':{**ar,'cost_comparisons':{k:{'new_return_pct':z['net_return_pct'],'old_N375_return_pct':ancestor['scenes'][k]['net_return_pct'],'delta_return_pp':z['net_return_pct']-ancestor['scenes'][k]['net_return_pct'],'new_DD_pct':z['max_drawdown_pct'],'old_N375_DD_pct':ancestor['scenes'][k]['max_drawdown_pct'],'delta_DD_pp':z['max_drawdown_pct']-ancestor['scenes'][k]['max_drawdown_pct'],'old_recent_counts':sum(f['net_return_pct']>0 for f in ancestor['scenes'][k]['recent40']['folds']),'new_recent_counts':sum(f['net_return_pct']>0 for f in z['recent40']['folds'])} for k,z in c['scenes'].items()}}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'scope':'Matched same-L E0.5% N750 source and same-L/E older N375 actual reports; hashes/metrics only,no new source policy or source NAV calculation.'});put(R/'prior_grid_NAV_aliases.json',{'new_definitions_matching_a_prior_path':sum(x['all_cost_NAV_identical'] for x in eq),'scope':'Exact allcost fullNAV comparison to originalE0.5% N750 parent,not independent alpha.'})
newfps={c['fingerprint'] for c in r['configs'].values()};hist={}
for fp,z in records.items():
 sp=z.get('spec',{});obs=sp.get('family')=='paper-live-portfolio-observation' or sp.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in sp.get('parameters',{})
 if fp in newfps or not sp or obs:continue
 hist.setdefault(reg.fingerprint(sp),[]).append(z)
trials={'canonical_prior_research_definitions':len(hist),'registry_marked_actual':sum(any(z.get('result_available') is True for z in zs) for zs in hist.values()),'not_marked_actual':sum(not any(z.get('result_available') is True for z in zs) for zs in hist.values()),'initial16_actual_evidence':16,'new_financial_definitions':6,'new_native_models':0,'new_cost_scenes':18,'observations_excluded':True};put(R/'prior_actual_research_counts.json',trials)
lines=['固定BTC N750后的退出缓冲组合研究','',p['hypothesis'],'',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论；初始16均有原档实际证据。此前完整研究定义{trials['canonical_prior_research_definitions']}，登记有结果{trials['registry_marked_actual']}、未标结果{trials['not_marked_actual']}，全部登记不能算全部完成回测。大量重复历史搜索有多重选择偏差。",'', '预设ETH快L3/4/5 × 退出缓冲E0.375/0.5/0.625%，慢S28固定，固定BTC真实银行3750/N750，ETH真实15000/N4500、HL1.5%/HS2.5%、V10/cap4.5%。raw[1,1]代表完整银行所有权，初始本金18750、资金份额20/80%；不归一化、不再乘资金份额、不线性缩放数量或净值，不平均Sharpe/收益/DD。E0.5%三个父、BTC、九个ETH源与匹配持有父及其源共16旧实际结果只读。六个E0.375/0.625%父逐项reserve后才对齐完整分钟/事件净值计算；0新原生策略、0新源成交、0新持有基准、0父订单。', '', 'Walk-forward：实际2025-10-19UTC00:01至2026-10-24UTC00:01，连续370日，12×30日完整折+10日尾折。现金/数量/费用不按折重开，完整OOS曲线算整体DD。近期40日继承day330状态、8×5日折。固定规则无拟合/标签，purge0、30日预热+3日间隔，过去完整收盘生成信号、下一00:01原生OPEN执行、终点平仓成本已在原生源内。历史反复开发，不能叫未触碰最终测试、独立未来或实盘稳定盈利。', '', '成本全部来自真实已执行原生源：5bp费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)，LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark维持保证金代理；真实settlement ns/rate/mark/heldq资金费，1/2/3倍放大支出、收入不放大。永续空头不借现货，不虚构借币费。父没有调仓或额外成本；匹配持有为相同银行与初始入场N750/4500，现金0%另列。缺盘口/TCA/历史全层级/逐tick强平和真实容量验证，估计及代理局限保留。', '', '原资格门槛保持：各成本全年正；1倍至少9/12正完整月；各成本近期40日正且>=6/8正5日折；3倍整体DD<=25%；含中心索引半径1的L/E邻域3倍正比例与严格近期合格比例均>=60%；至少4底层平仓、毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规，终点flat。旧原生/父的canonical status/criteria/sensitivity及报告字节不改，新L/E诊断另列。', '', '|新组合|L|E(比例)|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|','|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+ '|'.join([c['name'],str(c['L']),str(c['E']),*[f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3']],f"{c['scenes']['3']['max_drawdown_pct']:.6f}",str(c['positive_complete_30d_folds_1x']),'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3']),c['status']])+'|')
lines.extend(['',f"六个新组合历史通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}，逐项失败{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。相对E0.5%同L/N750原中心，三成本完整NAV同路径{sum(x['all_cost_NAV_identical'] for x in eq)}/6；与同L/E原N375逐成本差异及近期折数保留。本批L/E门槛通过也不能解决先前S27/29敏感性证据，不能称全参数稳健或独立未来盈利。",'', '11CSV包含18新场景、234逐月/尾折、144近期折、6678日NAV、原生只读九格与新父九格敏感性、72相邻边及来源/分配/匹配持有现金。图中ETH原生全部O=只读，父E0.375/0.625% N=新、E0.5% O=旧。全部Sharpe/Calmar/完整DD及负收益期间保留，描述性悬崖不是统计显著性，也不是事后加门槛。', '', '原SMA65与single仅续Nov3_08:30→10:30；L4/H2续10:10→12:10，仅12:11参考闭合后采集，逐条核对实际新增资金费，不预填固定时间/费率/mark，不重复既有08/00。所有cash/q/desired/已付成本/risk/context/完整NAV前缀保留，不采纳本批E、不改本金或冻结终止计划。部分延迟shadow与十策略真实报价模拟分开，不作180日/六折资格。SMA真实65日源仍为20261103T020232Z/forward_inputs.json.gz。', '', '一手资料2026-11-03实际访问：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。官方字段不证明盈利或实时执行；8源行情/mark/资金费/约束文件边界/单位/字节/SHA见plan和data_manifest。', '', '金融计算前合成检查覆盖原始完整银行资本恒等式、收益/DD不能平均、不同事件轴必须拒绝与18个L/E索引邻域。当前L/E双轴网格与账户运输适配在reserve前固定，一次绑定32个来源文件；没有结果后改规则或门槛。', '', '所有实际定义先reserve后计算并finish；正负结果和失败均保留，检查后只清理可重建中间件，完整账本不删。同main锁内生成只读监控、提交非强制push；真实发布/终态/解锁凭据见.git/automation_proofs/'+R.name+'.json。'])
(R/'result.md').write_text('\n'.join(lines).rstrip()+'\n');print(json.dumps(s),flush=True)
