"""Export actual new parent results and old-source D/K sensitivity; no simulation."""
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
cost=[];wf=[];rec=[];daily=[]
for c in r['configs'].values():
 for k,z in c['scenes'].items():
  prefix=[c['name'],c['fingerprint'],c['scope'],c['role'],c['N'],c['D'],c['K'],c['capital_usdt'],k];cost.append(prefix+[z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar'],z['cost_usdt'],z['cost_pct_initial'],z['funding_usdt'],z['gross_reference_PnL_to_execution_cost'],z['executions'],z['round_trips'],z['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in z['recent40']['folds']),c['status']]);wf.extend([c['name'],c['D'],c['K'],k,f['fold'],f['start_utc'],f['end_exclusive_utc'],f['duration_days'],f['net_return_pct'],f['max_drawdown_pct'],f['sharpe_365'],f['calmar']] for f in z['folds']);rec.extend([c['name'],c['D'],c['K'],k,f['fold'],f['start_utc'],f['end_exclusive_utc'],f['net_return_pct'],f['max_drawdown_pct'],f['sharpe_365'],f['calmar']] for f in z['recent40']['folds']);daily.extend([c['name'],c['D'],c['K'],k,i,v] for i,v in enumerate(z['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','entry_N','ETH_D','ETH_K','capital','cost_multiplier','return_pct','whole_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','D','K','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf);write('recent40_folds.csv',['configuration','D','K','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],rec);write('daily_NAV.csv',['configuration','D','K','cost_multiplier','boundary','NAV_usdt'],daily)
edges=[];flags={};cols=['ETH_D','ETH_K','fixed_native_or_BTC_N','fingerprint','readonly_old','canonical_status','cost_multiplier','return_pct','whole_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_strict_recent_fraction']
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']];diag=c['current_grid_diagnostic_sensitivity']
  for k,z in c['scenes'].items():items.append([g['D'],g['K'],g['N'],g['fingerprint'],g['readonly'],c['status'],k,z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar'],z['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in z['recent40']['folds']),diag['local_positive3_fraction'],diag['local_strict_recent_fraction']])
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['slope_lags'].index(g['D']),p['slope_strengths'].index(g['K']);adj=[h for h in grid if i<2 and h['D']==p['slope_lags'][i+1] and h['K']==g['K'] or j<2 and h['K']==p['slope_strengths'][j+1] and h['D']==g['D']]
   for h in adj:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['D'],g['K'],h['D'],h['K'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  x=[z[8] for z in edges if z[0]==scope and z[1]==k];threshold=2*statistics.stdev(x);flags[scope][k]={'edge_count':len(x),'max_Sharpe_change':max(x),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(x)>threshold,'scope':'Dependentadjacencydiagnostic,notmultiplicity-adjusted significance or postresultgate.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
external=[]
for fp in p['external_control_fingerprints']:
 ref=p['read_only_references'][fp];c=next(c for c in json.loads((ROOT/ref['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,z in c['scenes'].items():external.append([c['name'],fp,750,c['D'],c['K'],ref['capital_usdt'],k,z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar'],z['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in z['recent40']['folds']),c['status'],ref['report'],ref['report_sha256']])
write('readonly_reused_scenes.csv',['configuration','fingerprint','reference_BTC_N','ETH_D','ETH_K','capital','cost_multiplier','return_pct','whole_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','unchanged_canonical_status','report','report_sha256'],external);write('adjacent_edges.csv',['scope','cost_multiplier','from_D','from_K','to_D','to_K','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges);cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
sources=[]
for fp,ref in p['read_only_references'].items():
 if ref['scope']!='native':continue
 sp=json.loads((ROOT/ref['spec']).read_text());c=next(c for c in json.loads((ROOT/ref['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,z in c['scenes'].items():sources.append([fp,ref['asset'],ref['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],sp['parameters'].get('trend_slope_lag_days'),sp['parameters'].get('trend_slope_hurdle_fraction'),k,z['net_return_pct'],z['max_drawdown_pct'],z['cost_usdt'],z['funding_usdt'],z['executions'],z['NAV_sha256_f64le'],ref['report'],ref['report_sha256'],True])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','ETH_D','ETH_K','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','report','report_sha256','readonly_old'],sources)
alloc=[[g['fingerprint'],g['role'],g['N'],g['D'],g['K'],3750,15000,18750,750,4500,1,1,.2,.8,750/18750,.24,g['readonly']] for g in p['grid']+p['benchmarks']];write('fixed_allocations.csv',['fingerprint','role','BTC_entry_N','ETH_D','ETH_K','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','BTC_initial_nominal_share','ETH_initial_nominal_share','readonly'],alloc);put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(label,key) in enumerate([('ETH bank15000/N4500;6old+3new','all_current_native_grid'),('BTC3750/N750 + ETH15000/N4500 parent','all_current_grid')]):
 full=r[key]
 for j,(metric,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['slope_lags'].index(c['D']),p['slope_strengths'].index(c['K'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,aspect='auto',cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['K1%','K2%','K3%']);ax.set_yticks(range(3),['D6','D7','D8']);ax.set_xlabel('ETH minimum finiteEWM slope K');ax.set_ylabel('ETH slope lag days D');ax.set_title(label+'\n'+metric,fontsize=10)
  for c in full.values():i,k=p['slope_lags'].index(c['D']),p['slope_strengths'].index(c['K']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH D6/7/8 x K1/2/3% | S24,L5,H2%,E0.5%,entry-only trend gate,V10/cap4.5%\nBTC3750/N750 + ETH15000/N4500 | raw[1,1],capital20/80% | O=old readonly,N=new | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(x for c in r['configs'].values() for x in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
comparisons=[];native_comparisons=[]
for c in r['configs'].values():
 fp=p['predeclared_reference_by_fingerprint'][c['fingerprint']];ref=p['read_only_references'][fp];old=next(c for c in json.loads((ROOT/ref['report']).read_text())['configs'].values() if c['fingerprint']==fp);assert c['D']==old['D'] and old['K']==.02 and c['K']==.03 and c['scope']==old['scope']
 row={'fingerprint':c['fingerprint'],'name':c['name'],'scope':c['scope'],'role':c['role'],'N':c['N'],'D':c['D'],'K':c['K'],'reference_D':old['D'],'reference_K':old['K'],'reference_fingerprint':fp,'reference_BTC_N':750,'reference_report':ref['report'],'reference_report_sha256':ref['report_sha256'],'same_initial_bank_capitals':True,'same_entry_notionals':True,'same_D_and_other_signal_rules':True,'ETH_hurdle_intentionally_differs':True,'all_cost_NAV_identical':all(z['NAV_sha256_f64le']==old['scenes'][k]['NAV_sha256_f64le'] for k,z in c['scenes'].items()),'cost_comparisons':{k:{'return_pct':z['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'control_return_pct':old['scenes'][k]['net_return_pct'],'control_DD_pct':old['scenes'][k]['max_drawdown_pct'],'delta_return_to_control_pp':z['net_return_pct']-old['scenes'][k]['net_return_pct'],'delta_DD_to_control_pp':z['max_drawdown_pct']-old['scenes'][k]['max_drawdown_pct'],'new_recent_positive5d':sum(f['net_return_pct']>0 for f in z['recent40']['folds']),'control_recent_positive5d':sum(f['net_return_pct']>0 for f in old['scenes'][k]['recent40']['folds'])} for k,z in c['scenes'].items()}}
 (comparisons if c['scope']=='parent' else native_comparisons).append(row)
for n,x in [('equivalent_realized_NAV_paths.json',comparisons),('predeclared_native_reference_comparisons.json',native_comparisons),('benchmark_reference_comparisons.json',[])]:put(R/n,{'report_sha256':sha(R/'report.json'),'comparisons':x,'scope':'PresetK3new->oldK2eachD;capital/BTC750/allotherpolicyparametersmatched,ETHhurdleintentionallydiffers. Descriptive reusedhistory comparisons,oldcanonicalstatusunchanged.'})
groups={}
for c in r['configs'].values():groups.setdefault(c['scope']+'|'+'|'.join(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),[]).append(c['fingerprint'])
put(R/'prior_grid_NAV_aliases.json',{'new_definitions_matching_reference_NAV':sum(x['all_cost_NAV_identical'] for x in comparisons+native_comparisons),'within_new_grid_alias_groups':[v for v in groups.values() if len(v)>1],'scope':'Nativeandparentaliasesnotindependentalpha;declaredparametersremainseparated.'})
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');newfps={c['fingerprint'] for c in r['configs'].values()};hist={}
for fp,z in rs.items():
 sp=z.get('spec',{});obs=sp.get('family')=='paper-live-portfolio-observation' or sp.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in sp.get('parameters',{})
 if fp not in newfps and sp and not obs:hist.setdefault(reg.fingerprint(sp),[]).append(z)
trials={'canonical_prior_research_definitions':len(hist),'registry_marked_actual':sum(any(z.get('result_available') is True for z in zs) for zs in hist.values()),'not_marked_actual':sum(not any(z.get('result_available') is True for z in zs) for zs in hist.values()),'initial16_actual_evidence':16,'new_financial_definitions':6,'new_native_models':3,'new_cost_scenes':18,'observations_excluded':True};put(R/'prior_actual_research_counts.json',trials)
ctx=json.loads((R/'context.json').read_text());allnew=list(r['configs'].values());cs=[c for c in allnew if c['scope']=='parent'];ns=[c for c in allnew if c['scope']=='native'];net=[c['scenes']['3']['net_return_pct'] for c in cs];dd=[c['scenes']['3']['max_drawdown_pct'] for c in cs];native_passed=sum(c['status']=='passed' for c in ns)
lines=[f"本轮3个新K3%组件、3个新BTC750组合，共6配置/18成本场景实际完成；新组合通过{len(r['summary']['passed'])}/3、淘汰{len(r['summary']['candidate_rejected'])}/3，组件通过{native_passed}/3。连续370日walk-forward、D/K两轴敏感性与1/2/3倍成本压力测试完成。新组合3倍净收益{min(net):.6f}%～{max(net):.6f}%，整体回撤{min(dd):.6f}%～{max(dd):.6f}%。历史收益不等于独立前向或稳定实盘盈利。",'',p['hypothesis'],'',f"完整读取{ctx['registry_events']}登记事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}既往结论、三技能/README/OOS/freqtradeZIP。初始16项缺实际结果0；此前独立研究定义{trials['canonical_prior_research_definitions']}、标实际{trials['registry_marked_actual']}、未标{trials['not_marked_actual']}。重复开发历史与多重选择偏差明确保留。",'',
'规则：BTC ROC31/H4%/E1%，N750/本金3750。ETH反转ROC5/H2%/E0.5%，有限归一化EWM24 beta23/25，斜率M(i,24)/M(i-D,24)-1，D6/7/8×K1/2/3%。仅新开/反手检查趋势和V10样本logvol<=4.5%，同向实际数量保留；失败反转先平旧仓、不新开。全部过去完整收盘，下一UTC00:01 OPEN执行；N/priorclose按LOT下取整，终点计成本平仓。', '',
'raw[1,1]相加BTC3750/ETH15000完整银行，总本金18750。权重原值不归一化、不再乘20/80%资金份额；BTC名义占自身20%/总4%，ETH4500占自身30%/总24%。3新ETH组件真实计算数量、LOT、冲击、资金费与风险；BTC及6旧ETH当前格子和持有控制的9旧原生银行/27旧成本路径只读，16旧结果不改状态/criteria/sensitivity。父组合不缩放旧NAV/数量/成本、不产新订单、转移或交叉保证金。', '',
'6个新配置全部在首次估值前成功reserve，3新K3组件与3新组合逐D匹配旧K2%；其余规则、本金和BTC750均相同。12个K1/K2当前网格格子只读；原canonical资格保留，新网格诊断另列，不把旧配置重新计算或重判。同期同本金/N750+N4500持有和现金0%只读对照。', '',
'2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12×30日完整折+10日尾折；最近40日继承day330实际状态，8×5日、不重开。共同事件轴545013点，整体回撤基于全连续分钟/事件NAV。无训练拟合或标签，purge0；33日过去上下文含3日embargo，最大S+D32/BTC32过去收盘。反复使用历史不能称未触碰最终测试集。', '',
'事前D/K索引半径1含中心：父组合和ETH组件分别完整9格，报告所有成本下收益、整体DD、Sharpe、Calmar、72条相邻边、描述性cliff与边界最优；不据结果追加或改变门槛、不把相依邻域当DSR/PBO显著性。', '',
'手续费每边5bp、半价差1bp、滑点2bp；冲击0.5×过去20完整日样本logvol×sqrt(实际q×OPEN/过去20日quoteADV)。执行成本和资金费支出压力1/2/3倍，资金费收入不放大；真实结算ns/rate/mark/持仓，费率不作信号。LOT/tick/minnotional、参与率<=0.1%、费后1倍入场抵押与1%闭合小时不利mark风险代理核验。线性永续无现货借币；缺L2/TCA、全层级/最大量/逐tick强平证据，未证明真实容量。', '',
'固定失败判据：全期各成本净正；1倍>=9/12正月；每成本近期净正且>=6/8正五日折；3倍整体DD<=25%；邻域3倍正收益与严格近期合格率均>=60%；>=4原生平仓；毛参考PnL+资金费/执行成本>=2.5；0现金/订单/保证金代理违规，终点flat、>=180日。', '',
'|新配置|类型|D|K|1x净%|2x净%|3x净%|3x整体DD%|1x正月|近期正折1/2/3|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in allnew:lines.append('|'+ '|'.join([c['name'],c['scope'],str(c['D']),str(c['K']),*[f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3']],f"{c['scenes']['3']['max_drawdown_pct']:.6f}",str(c['positive_complete_30d_folds_1x']),'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3']),c['status']])+'|')
lines.extend(['',f"全部失败项：{ {c['name']:c['failed_criteria'] for c in allnew} }。",'',
'11CSV保存18新成本场景、234月/尾折、144近期折、6678日NAV、27父/27原生网格、18旧对照场景、72邻接边、27同本金持有/现金比较、27旧原生成本路径及10资金配置；全部正负结果留档。原生逐决策/交易/资金费、完整NAV SHA与独立Fraction信号、Decimal账本审计保留。', '',
'四账户独立续接：SMA65/single Nov5_18:30→20:30，L4/FEWM20:10→22:10，均从各自post16账本延续真实闭合mark/小时风险核验，无日目标/新成交/新结算，不重复16或08。保留cash/units/desired/cost/risk/完整NAV前缀，SMA65日spot源20261105T022141Z。FEWM固定N750/4500、D1/K.0005，与本轮K3研究独立。只复用公开市场响应；single只复用L4元数据/时间、自取分钟/hour/funding；FEWM同窗公共数组及provenance相同，自己的账本/现金流/NAV独立计算。均为未成熟延迟shadow，非180日/六折资格、非十策略真实报价模拟业绩。', '',
'2026-11-05UTC实际读取[Binance官方市场数据文档](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)，核对真实资金费字段与单位。实际行情来自既有parquet/公共API，成本无真实TCA时为明确模型。', '',
'同main排他锁内完成登记、只读snapshot与monitor检查，不改冻结规则/本金/持仓、不重部署或新增定时任务。完整账户账本、冻结计划、登记、行情和核验证据保留，清理仅可重建中间物。实际push/远端完整tree/blob/解锁终态见.git/automation_proofs/'+R.name+'.json。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
