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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['S'],c['E'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['S'],c['E'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['S'],c['E'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_slow_S','exit_buffer_fraction_E','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_slow_S','exit_buffer_fraction_E','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_slow_S','exit_buffer_fraction_E','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_slow_S','exit_buffer_fraction_E','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['S'],g['E'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['slow_windows'].index(g['S']),p['exit_buffers'].index(g['E']);ng=[h for h in grid if i<2 and h['S']==p['slow_windows'][i+1] and h['E']==g['E'] or j<2 and h['E']==p['exit_buffers'][j+1] and h['S']==g['S']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['S'],g['E'],h['S'],h['E'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];threshold=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(v)>threshold,'scope':'Dependentedge descriptive heuristic only,not significance/DSR/PBO or a posthoc gate.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly);write('adjacent_edges.csv',['scope','cost_multiplier','from_S','from_E','to_S','to_E','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());c=next(z for z in json.loads((ROOT/x['report']).read_text())['configs'].values() if z['fingerprint']==fp)
 for k,s in c['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256'],True])
for c in r['configs'].values():
 if c['scope']!='native':continue
 for k,s in c['scenes'].items():sources.append([c['fingerprint'],c['asset'],c['capital_usdt'],4500,k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],rel(R/'report.json'),sha(R/'report.json'),False])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','provenance_report','report_sha256','readonly_old'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['S'],g['E'],3750,15000,18750,750,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,750,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_S','exit_buffer_fraction_E','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc);put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750/N750+ETH15000/N4500 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['slow_windows'].index(c['S']),p['exit_buffers'].index(c['E'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['E0.375%','E0.5%','E0.625%']);ax.set_yticks(range(3),['S27','S28','S29']);ax.set_xlabel('ETH exit buffer E (%)');ax.set_ylabel('ETH slow lookback S (days)');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['slow_windows'].index(c['S']),p['exit_buffers'].index(c['E']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('Fixed ETH fastL4 | slowS27/28/29 x exitE0.375/0.5/0.625% | V10/cap4.5%,HL1.5%/HS2.5%\nBTC3750/N750 + ETH15000/N4500 | raw[1,1],capitalshares20/80%,noNAVscaling | O=oldreadonly,N=newnative/parent | reused history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');eq=[]
def compare(c,base):
 return {k:{'return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'control_return_pct':base['scenes'][k]['net_return_pct'],'control_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_control_pp':z['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_control_pp':z['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct'],'new_recent_positive5d':sum(f['net_return_pct']>0 for f in z['recent40']['folds']),'control_recent_positive5d':sum(f['net_return_pct']>0 for f in base['scenes'][k]['recent40']['folds'])} for k,z in c['scenes'].items()}
for c in r['configs'].values():
 if c['scope']!='parent':continue
 g=next(g for g in p['grid'] if g['S']==28 and g['E']==c['E']);base=r['all_current_grid'][g['fingerprint']];ref=p['read_only_references'][g['fingerprint']];h=next(g for g in p['grid'] if g['S']==c['S'] and g['E']==.005);other=r['all_current_grid'][h['fingerprint']]
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'L':4,'S':c['S'],'E':c['E'],'N':750,'control_fingerprint':g['fingerprint'],'control_report':ref['report'],'control_report_sha256':ref['report_sha256'],'all_cost_NAV_identical':all(z['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k,z in c['scenes'].items()),'cost_comparisons':compare(c,base),'same_S_E500_control':{'fingerprint':h['fingerprint'],'cost_comparisons':compare(c,other)}})
assert len(eq)==4;put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'scope':'Saved sameE S28 positive controls and sameS E500 existing controls,all readonly;no extra financial valuation.'});put(R/'prior_grid_NAV_aliases.json',{'new_definitions_matching_a_prior_path':sum(x['all_cost_NAV_identical'] for x in eq),'scope':'Only fullbank parent paths;native and parent capitals are never compared as equal.'})
newfps={c['fingerprint'] for c in r['configs'].values()};hist={}
for fp,z in records.items():
 sp=z.get('spec',{});obs=sp.get('family')=='paper-live-portfolio-observation' or sp.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in sp.get('parameters',{})
 if fp in newfps or not sp or obs:continue
 hist.setdefault(reg.fingerprint(sp),[]).append(z)
trials={'canonical_prior_research_definitions':len(hist),'registry_marked_actual':sum(any(z.get('result_available') is True for z in zs) for zs in hist.values()),'not_marked_actual':sum(not any(z.get('result_available') is True for z in zs) for zs in hist.values()),'initial16_actual_evidence':16,'new_financial_definitions':8,'new_native_models':4,'new_cost_scenes':24,'observations_excluded':True};put(R/'prior_actual_research_counts.json',trials)
lines=['固定快窗L4的退出缓冲×慢窗真实交叉验证','',p['hypothesis'],'',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论。初始16有原档实际证据，缺实际结果0。此前研究定义{trials['canonical_prior_research_definitions']}，标实际结果{trials['registry_marked_actual']}，未标{trials['not_marked_actual']}；大量重复历史搜索存在多重选择偏差，不能说所有登记均有实际回测。",'', '预设快L4，慢S27/28/29×退出E0.375/0.5/0.625%，HL1.5%/HS2.5%、V10/cap4.5%。五格原生/五格组合已有实际结果只读。四角新ETH原生各15000本金/N4500，必须真实重算信号、LOT数量、成本、资金费与现金；四角新组合复用实际BTC3750/N750与对应新ETH净值。raw[1,1]为完整银行所有权，总本金18750、银行资金份额20/80%、初始入场名义占比4/24%；不归一化、不重复乘资金份额、不缩放数量/净值，不平均收益/Sharpe/DD，不跨银行转移/调仓。', '', 'Walk-forward：2025-10-19UTC00:01至2026-10-24UTC00:01，真实连续370日、12×30日完整折+10日尾折；完整OOS曲线算整体DD，不按折重开。近期40日从day330真实持仓/现金承接，8×5日。固定规则无拟合/标签，purge0，30日预热+3日间隔，过去已完成日线决定下一00:01原生OPEN，终点计成本平仓。该历史反复使用，不能称未触碰最终测试或独立未来验证。', '', '成本：每侧5bp手续费+1bp半价差+2bp滑点+0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整日quoteADV)，不使用未来量价；1/2/3倍压力放大所有支出和资金费支出，收入不放大。真实settlement ns/rate/mark/heldq资金费；LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押、独立1%闭合小时不利mark保证金代理。线性永续空头无现货借币，不虚构借币费。父无新订单/额外成本。匹配持有复用相同银行和入场N750/4500，另比现金0%。缺盘口/TCA、历史完整层级/最大量、逐tick强平与容量证明。', '', '失败门槛事先固定：全年各成本正，1倍>=9/12正完整月，近期各成本总收益正且>=6/8正5日折，3倍整体DD<=25%；含中心S/E索引半径1邻域3倍正与严格近期合格比例均>=60%；>=4底层平仓，毛参考PnL+资金费/执行成本>=2.5；0订单/现金/保证金代理违规、终点flat，至少180日。所有新原生/新组合按同一门槛分别裁定；旧canonical状态/判据/敏感性和旧报告不改，本批S/E诊断另列。', '', '|新配置|scope|S|E比例|1x收益%|2x收益%|3x收益%|3x整体DD%|1x正月|近期正折1/2/3|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+ '|'.join([c['name'],c['scope'],str(c['S']),str(c['E']),*[f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3']],f"{c['scenes']['3']['max_drawdown_pct']:.6f}",str(c['positive_complete_30d_folds_1x']),'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3']),c['status']])+'|')
lines.extend(['',f"四个新组合通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}；四个新原生独立状态亦在表内。逐项失败{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。新组合对同E/S28控制全成本NAV同路径{sum(x['all_cost_NAV_identical'] for x in eq)}/4，差异及同S/E0.5%控制逐成本对比均保存。正收益不等于稳健或稳定实盘盈利。",'', '11CSV保存24新场景、312逐月/尾折、192近期折、8904日NAV、两张九格敏感性、15旧组合场景、72相邻边、27持有/现金比较、36新旧原生成本路径与10资金分配。图中两个scope均为四角N=新、五格O=旧只读；完整DD/Sharpe/Calmar与负收益折全部保留。边界按真实S/E端点检查；相邻悬崖为描述性依赖样本统计，不是DSR/PBO或事后新增门槛。', '', '原SMA65与single续10:30→12:30；独立原L4/H2续12:10→14:10，仅14:11执行参考闭合后采集。原现金/q/desired/成本/risk/context/完整NAV前缀连续，不改冻结规则/本金/持仓/终止日，不重复08/00资金费，不采纳本批参数。SMA真实65日上下文源20261103T020232Z/forward_inputs.json.gz不变。延迟真实数据shadow与十策略实盘报价模拟分开，部分观测不冒充180日/六折资格。', '', '一手资料2026-11-03实际访问：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。官方真实资金费字段不证明策略盈利、容量或实时成交。8行情/mark/资金费/元数据文件边界/字节/SHA与不可变实现哈希见plan和data_manifest。', '', '全部八项先逐项成功reserve，才计算12原生及12组合成本路径。预登记前合成检查覆盖完整银行资本恒等式、平均DD/收益错误、事件轴错位、18个S/E邻域、未来close不可见、S27与S29索引区分及退出等号边界。独立Fraction信号与Decimal数量/成本/资金费/小时风险及全净值核验；旧实现、源和报告保留。原生/组合成功与负结果均分别finish，失败记录不删。', '', '本轮只清理可重建中间件，保留完整账本及核验必需证据；同一main排他锁内生成只读监控、提交非强制push，发布/远端完整tree/锁释放终态见.git/automation_proofs/'+R.name+'.json。'])
(R/'result.md').write_text('\n'.join(lines).rstrip()+'\n');print(json.dumps(summary),flush=True)
