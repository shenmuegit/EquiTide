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
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['asset'],c['L'],c['S'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['S'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['scope'],c['L'],c['S'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','asset','ETH_fast_L','slow_window_days_S','initial_capital','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','ETH_fast_L','slow_window_days_S','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','ETH_fast_L','slow_window_days_S','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['ETH_fast_L','slow_window_days_S','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction'];flags={};readonly=[]
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   d=c['current_grid_diagnostic_sensitivity'];z=[g['L'],g['S'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];items.append(z)
   if scope=='parent' and g['readonly']:readonly.append(z)
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['lookbacks'].index(g['L']),p['slow_windows'].index(g['S']);ng=[h for h in grid if i<2 and h['L']==p['lookbacks'][i+1] and h['S']==g['S'] or j<2 and h['S']==p['slow_windows'][j+1] and h['L']==g['L']]
   for h in ng:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['S'],h['L'],h['S'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  v=[x[8] for x in edges if x[0]==scope and x[1]==k];t=2*statistics.stdev(v);flags[scope][k]={'edge_count':len(v),'max_Sharpe_change':max(v),'two_std_change_threshold':t,'descriptive_cliff_flag':max(v)>t,'scope':'Dependentedgeheuristiconly,notstatisticalsignificance,DSRorPBO.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_S','to_L','to_S','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
for g in p['grid']:alloc.append([g['fingerprint'],'candidate',g['L'],g['S'],3750,15000,18750,375,4500,1,1,.2,.8,g['readonly']])
alloc.append([p['benchmark_parent_fingerprint'],'matched_initial_budget_hold',None,None,3750,15000,18750,375,4500,1,1,.2,.8,True]);write('fixed_allocations.csv',['fingerprint','role','ETH_L','slow_window_days_S','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','readonly'],alloc)
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(16,9),layout='constrained')
for row,(scope,key) in enumerate([('ETH native15000/N4500','all_current_native_grid'),('BTC3750+ETH15000 parent','all_current_grid')]):
 full=r[key]
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in full.values():arr[p['lookbacks'].index(c['L']),p['slow_windows'].index(c['S'])]=fn(c)
  ax=axs[row,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['S27','S28 old','S29']);ax.set_yticks(range(3),['L3','L4','L5']);ax.set_xlabel('ETH slow lookback S (days)');ax.set_ylabel('ETH fast lookback L');ax.set_title(scope+'\n'+label,fontsize=10)
  for c in full.values():i,k=p['lookbacks'].index(c['L']),p['slow_windows'].index(c['S']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH fast L3/4/5 x slow S27/28/29 | fixed E0.5%, V10/cap4.5%, HL1.5%/HS2.5%\nActual BTC3750/N375 + ETH15000/N4500 | raw[1,1], capitalshares20/80%, noNAVscaling | O=readonly,N=new | reused development history')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
s={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(f for c in r['configs'].values() for f in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',s)
ctx=json.loads((R/'context.json').read_text());eq=[]
for c in r['configs'].values():
 grid=p['native_grid'] if c['scope']=='native' else p['grid'];key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';g=next(g for g in grid if g['L']==c['L'] and g['S']==p['control_slow_window']);base=r[key][g['fingerprint']]
 eq.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'S':c['S'],'HL':.015,'matched_S28_control_fingerprint':g['fingerprint'],'identical_full_NAV_by_cost':{k:c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']},'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==base['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'cost_comparisons':{k:{'return_pct':c['scenes'][k]['net_return_pct'],'whole_DD_pct':c['scenes'][k]['max_drawdown_pct'],'control_return_pct':base['scenes'][k]['net_return_pct'],'control_DD_pct':base['scenes'][k]['max_drawdown_pct'],'delta_return_to_control_pp':c['scenes'][k]['net_return_pct']-base['scenes'][k]['net_return_pct'],'delta_DD_to_control_pp':c['scenes'][k]['max_drawdown_pct']-base['scenes'][k]['max_drawdown_pct']} for k in ['1','2','3']}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':eq,'policy':'Newslow-window values are preserved as new definitions; identical realized fullNAV paths, if any, are disclosed rather than called independentalpha. PriorS28 canonicalstatus/report unchanged, no completed-policy rerun.'})
prior_ref=p['prior_report'];assert sha(ROOT/prior_ref['path'])==prior_ref['sha256'];prior_report=json.loads((ROOT/prior_ref['path']).read_text());prior_aliases=[];prior_records=reg.read_records(ROOT/'research/automation/registry.jsonl')
for c in r['configs'].values():
 key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';matches=[]
 for oldc in prior_report[key].values():
  if oldc['L']==c['L'] and oldc['scenes']['1']['initial_capital_usdt']==c['scenes']['1']['initial_capital_usdt'] and all(oldc['scenes'][k]['NAV_sha256_f64le']==c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']):
   sp=prior_records[oldc['fingerprint']]['spec']['parameters'];matches.append({'old_fingerprint':oldc['fingerprint'],'old_S':sp.get('trend_lookback_days',sp.get('ETH_trend_lookback_days')),'old_E':sp.get('exit_buffer_fraction',sp.get('ETH_exit_buffer_fraction')),'old_name':oldc['name'],'canonical_old_status_unchanged':oldc['status']})
 prior_aliases.append({'fingerprint':c['fingerprint'],'name':c['name'],'scope':c['scope'],'L':c['L'],'S':c['S'],'E':.005,'prior_grid_full_NAV_matches_allcost':matches,'matches_existing_path':bool(matches)})
put(R/'prior_grid_NAV_aliases.json',{'scope':'Metadata-only comparison to previous L/E grid, beyond matched S28/E0.5 controls. Exact fullNAV SHA256 at allcosts,sameL/scope/bankcapital. No policy/NAV/orders/metrics recomputed; new actual parameters do not imply independent alpha.','prior_report':prior_ref,'new_definitions_matching_a_prior_path':sum(x['matches_existing_path'] for x in prior_aliases),'comparisons':prior_aliases})
# Historical definition counts are separate from actual-result flags and from the new batch.
records=reg.read_records(ROOT/'research/automation/registry.jsonl');newfps={x['fingerprint'] for x in r['configs'].values()};historical={}
for fp,z in records.items():
 sp=z.get('spec',{});obs=sp.get('family')=='paper-live-portfolio-observation' or sp.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in sp.get('parameters',{})
 if fp in newfps or not sp or obs:continue
 canon=reg.fingerprint(sp);historical.setdefault(canon,[]).append(z)
prior_counts={'canonical_historical_research_definitions':len(historical),'registry_marked_actual_result_available':sum(any(z.get('result_available') is True for z in zs) for zs in historical.values()),'registry_not_marked_actual_result_available':sum(not any(z.get('result_available') is True for z in zs) for zs in historical.values()),'initial_16_actual_evidence_resolution':ctx['initial_16_evidence_resolution'],'new_actual_configurations':len(r['configs']),'new_cost_scenes':36,'observations_excluded':True,'scope':'Read-only full registry metadata, excluding this new batch. Missing-result flags are not treated as completed backtests; separately archived original16 evidence remains verified. This count does not confer statistical independence or significance.'};assert len(historical)==ctx['canonical_research_definitions_excluding_observations'];put(R/'prior_actual_research_counts.json',prior_counts)
lines=['# ETH 快回望与慢方向窗口联合验证','',f"完整读取{ctx['registry_events']}事件/{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论；排除观察后的完整研究定义数{ctx['canonical_research_definitions_excluding_observations']}。初始16条均有真实证据，本轮6个ETH原生和6组合、36成本场景先reserve再实际执行，全部失败/负收益期间保留。",'',p['hypothesis'],'',f"既往完整定义{prior_counts['canonical_historical_research_definitions']}，登记明确有实际结果{prior_counts['registry_marked_actual_result_available']}，未标实际结果{prior_counts['registry_not_marked_actual_result_available']}；初始16条原档解析单列。定义数与无结果配置不能全算完成回测，重复历史存在大量选择偏差。",'',
'预设L=[3,4,5]与慢趋势S=[27,28,29]日；固定E=0.005（ROC价格收益率阈值0.5%）、HL=0.015、HS=0.025、V10/cap0.045。S28的3原生/3组合、BTC、匹配持有父与其2原生共10旧结果只读。真正改变S是新配置，名称/排序/数字格式不是。','',
'价格规则：fastROC=C[i−1]/C[i−1−L]−1；严格r>0.025空、r<−0.015多，等号不新开。否则已有多仅r<+0.005保留、已有空仅r>−0.005保留，等号退出。慢ROC=C[i−1]/C[i−1−S]−1，其绝对正/负方向门控反转方向，等于0必须flat。最后10个完成日log收益样本std>0.045只过滤新开/翻向，等号允许；实际同向持仓不因高波动单独强平。无额外慢幅度、时限、残差或资金费信号。前完整日信号后下一UTC00:01原生OPEN执行，翻向先平后开。','',
'数据与walk-forward：真实2025-10-19UTC00:01至2026-10-24UTC00:01连续370日，12个30日完整折与10日尾折；现金、数量和成本跨折连续，完整分钟/事件NAV计算整体回撤。最近40日继承day330状态，8个5日折单列。固定规则无拟合/标签，purge0；预热30日+3日间隔提供首决策i33的33个完整日收盘，最大S29使用index3，不截短或负索引，不引未来。成本只用前20完整日。历史反复开发，不称未触碰最终留出、独立未来或DSR/PBO显著结果。','',
'资金与权重：BTC真实3750USDT银行/N375复用原ROC31/H4%/E1%的已执行原生曲线；ETH15000银行/N4500实际数量/LOT/OPEN/成本/抵押重算。原[1,1]为两个完整银行美元NAV相加，总本金18750；20%/80%仅初始本金份额，不再乘一次或归一化。初始名义4875为本金26%，无父调仓/转账/跨抵押/NAV复利调N/线性放缩旧净值，翻向及历史终止平仓计成本。','',
'成本：每边手续费5bp、半价差1bp、滑点2bp，冲击0.5×past20样本logvol×sqrt(实际q×OPEN/past20完整quoteADV)，逐1/2/3倍。真实资金费按结算ns/rate/mark/heldq入账，支出倍增、正收入不放大。核验LOT/tick/minnotional、参与率<=0.001、费用后1倍抵押及独立银行1%闭合小时不利mark维护代理。线性永续无现货借币；缺实测L2/TCA、完整历史保证金档位、逐tick清算与容量证明。同期同银行/初始名义持有和现金0%对照，非等风险匹配。','',
'固定失败判据：各成本全年净正；1倍>=9/12正完整月；各成本近期净正且>=6/8正5日折；3倍整体DD<=25%；L/S索引半径1含中心邻域3倍净正和严格近期支持均>=60%；>=4底层平仓；1倍毛参考价格PnL+funding/执行成本>=2.5；零拒单/负抵押/小时代理违规、终止flat且>=180日。新原生和组合分别判断，旧S28资格/旧邻域字段保持，当前网格诊断另列。','',
'|新配置|范围|L|慢窗口S日|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in r['configs'].values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['S']}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines.extend(['',f"新组合历史通过{len(r['summary']['passed'])}、淘汰{len(r['summary']['candidate_rejected'])}；全部失败判据{ {c['name']:c['failed_criteria'] for c in r['configs'].values()} }。不以年度峰值替代近期/逐月/邻域要求。",'',f"相对同L旧S28/E0.5中心，完整NAV全同{sum(z['all_cost_NAV_identical'] for z in eq)}/{len(eq)}；相对上一轮整个L/E网格同路径{sum(x['matches_existing_path'] for x in prior_aliases)}/12。hash和每成本收益/完整DD差异逐项保存；新参数不等于独立alpha。",'',
'11CSV包含36成本场景、全部完整月/尾折/近期折、每日NAV、原生和组合九格敏感性、72相邻边以及来源/分配/匹配持有现金。图含收益/整体DD/Sharpe/近期折数，Calmar在表内。边界及2std相邻悬崖仅为描述诊断，不作显著性或结果后加门槛。','',
'合成检查先确认上一轮慢窗口接纳范围拒绝S27，再仅扩展S27/28/29接纳；Fraction价格、退出和会计公式复用。144个严格阈值/翻向/慢门控/波动/未来不变fixture，18个准确S滞后与慢ROC等号flat案例，18个旧行补S元数据/4-6-9索引邻域/原资格保持案例另存。S29最早i30有30完整close时可执行、只有29close时必须拒绝；实际首i33有33完整close可用，防负索引暖启动泄漏。独立核验不调用simulate/decide/trade重新评估。','',
'原SMA65与singleS28从Nov2UTC22:30续Nov3_00:30，处理原00:01日决策；single按真实Nov3新资金费计账。独立未过滤L4/H2从Nov3_00:10续02:10，仅02:11参考闭合后采集；它此前已记Nov3午夜资金费和日决策，本轮不重复。全部cash/q/desired/risk/context/NAV前缀连续，不采纳本批新S。SMA65新增65日真实数据并与20261102T015622Z的64个重叠日严格核对。部分延迟shadow与十策略实时报价模拟区分，长期规则/本金/终止日期保持，不重开账户/下真实单。','',
'一手资料2026-11-03实际访问：[Binance市场数据API](https://developers.binance.com/en/docs/catalog/core-trading-derivatives-trading-usd-s-m-futures/api/rest-api/market-data)。8份源年bars/mark/funding/约束文件路径、单位、边界/字节/hash见plan/data_manifest；文档不证明假设盈利、历史发布延迟或实际成本。','',
'全部实际配置逐项finish，负收益/失败结果完整保存；同main排他锁内完成登记/来源/导出/监控检查、提交非强制push。只读监控不新回测/成交，不改冻结账户，不部署网页/增任务/下真实订单。'])
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(s),flush=True)
