"""Exports from actual saved reports only; no strategy/order calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
from run import recent_ok
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());cfgs=rep['configs'];full=rep['all_current_grid'];Ls=plan['exit_buffers'];Hs=plan['fast_hurdles'];rows={}
def write(name,cols,items):
 with (R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];tail=[];daily=[];grid=[];edges=[];readonly=[]
for c in cfgs.values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['E'],c['H'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(x['net_return_pct']>0 for x in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['E'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  tail.extend([c['name'],c['scope'],c['E'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]:
 for g in items:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   grid.append([scope,g['E'],g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),recent_ok(c),c['current_grid_diagnostic_sensitivity']['local_positive3_fraction'],c['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction']])
   if g['readonly']:readonly.append(grid[-1])
 for k in ['1','2','3']:
  for g in items:
   i,j=Ls.index(g['E']),Hs.index(g['H']);neighbors=[h for h in items if i<len(Ls)-1 and h['E']==Ls[i+1] and h['H']==g['H'] or j<len(Hs)-1 and h['H']==Hs[j+1] and h['E']==g['E']]
   for h in neighbors:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['E'],g['H'],h['E'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
write('cost_scenes.csv',['configuration','fingerprint','scope','E','H','initial_capital_usdt','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','underlying_executions','underlying_closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','E','H','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','E','H','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],tail)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['scope','E','H','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','strict_recent_gate_diagnostic','local_positive3_fraction','local_recent_fraction']
write('sensitivity_grid.csv',cols,grid);write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_E','from_H','to_E','to_H','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
comparisons=rep['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(comparisons[0]),[list(x.values()) for x in comparisons])
flags={}
for scope in ['native','parent']:
 for k in ['1','2','3']:
  vals=[x[8] for x in edges if x[:2]==[scope,k]];threshold=2*statistics.stdev(vals);flags[scope+'_'+k]={'edge_count':len(vals),'max_Sharpe_change':max(vals),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(vals)>threshold,'scope':'Descriptive dependent-edge heuristic only, not statistical significance/PBO/DSR.'}
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(17,8),layout='constrained')
for i,(scope,items) in enumerate([('native',plan['native_grid']),('parent',plan['grid'])]):
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(z['net_return_pct']>0 for z in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((len(Ls),len(Hs)))
  for g in items:arr[Ls.index(g['E']),Hs.index(g['H'])]=fn(full[g['fingerprint']])
  ax=axs[i,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(len(Hs)),[f'{x*100:g}%' for x in Hs]);ax.set_yticks(range(len(Ls)),[f'{x*100:g}%' for x in Ls]);ax.set_xlabel('Fast reversal hurdle H');ax.set_ylabel('Exit hysteresis E (absolute ROC)');ax.set_title(scope+'\n'+label)
  for g in items:
   a,b=Ls.index(g['E']),Hs.index(g['H']);ax.text(b,a,f'{arr[a,b]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.75)
fig.suptitle('Exit hysteresis E0/0.25/0.5% x entryH2/2.5/3% | fastL4 | fixed entry V10/cap4.5% | ETH actual15000cash/4500entry | S28 slowgate fixed; exit E varies\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**plan['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['rejected']),'failed_criteria_by_scope':{scope:dict(collections.Counter(x for c in cfgs.values() if c['scope']==scope for x in c['failed_criteria'])) for scope in ['native','parent']},'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_grid_qualified':{scope:sum(recent_ok(full[g['fingerprint']]) for g in items) for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]},'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)

ref=plan['read_only_references'][plan['baseline_parent_fingerprint']];doc=json.loads((ROOT/ref['report']).read_text());base=next(c for c in doc['configs'].values() if c['fingerprint']==plan['baseline_parent_fingerprint']);diff=[]
for c in cfgs.values():
 if c['scope']!='parent':continue
 for k,s in c['scenes'].items():
  b=base['scenes'][k];diff.append([c['name'],c['E'],c['H'],k,s['net_return_pct'],b['net_return_pct'],s['net_return_pct']-b['net_return_pct'],s['max_drawdown_pct'],b['max_drawdown_pct'],s['executions'],b['executions'],s['cost_usdt'],b['cost_usdt'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),sum(z['net_return_pct']>0 for z in b['recent40']['folds']),ref['fingerprint']])
write('baseline_comparison.csv',['new_parent','exit_E','fast_H','cost_multiplier','filtered_return_pct','unfiltered_return_pct','difference_pp','filtered_DD_pct','unfiltered_DD_pct','filtered_executions','unfiltered_executions','filtered_cost_usdt','unfiltered_cost_usdt','filtered_positive5d','unfiltered_positive5d','readonly_base_fingerprint'],diff);summary['CSV_rows']=rows;put(R/'sensitivity_summary.json',summary)

# Same H, same entry filter, actual capital and budget: isolate the exit-rule change in saved trajectories.
abl=[]
for c in cfgs.values():
 items=plan['native_grid'] if c['scope']=='native' else plan['grid'];z=next(full[g['fingerprint']] for g in items if g['E']==0 and g['H']==c['H'])
 for k,a in c['scenes'].items():
  b=z['scenes'][k];abl.append([c['name'],c['scope'],c['E'],c['H'],k,z['fingerprint'],a['net_return_pct'],b['net_return_pct'],a['net_return_pct']-b['net_return_pct'],a['max_drawdown_pct'],b['max_drawdown_pct'],a['executions'],b['executions'],a['cost_usdt'],b['cost_usdt'],a['funding_usdt'],b['funding_usdt'],sum(x['net_return_pct']>0 for x in a['recent40']['folds']),sum(x['net_return_pct']>0 for x in b['recent40']['folds'])])
write('exit_buffer_vs_zero.csv',['configuration','scope','E','H','cost_multiplier','readonly_zero_buffer_fingerprint','net_pct','zero_buffer_net_pct','difference_pp','wholeDD_pct','zero_buffer_wholeDD_pct','executions','zero_buffer_executions','cost_usdt','zero_buffer_cost_usdt','funding_usdt','zero_buffer_funding_usdt','positive5d','zero_buffer_positive5d'],abl);summary['CSV_rows']=rows;put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text());a=json.loads((R/'verification.json').read_text())
lines=['# 扩展入场门槛边界：退出缓冲与H联合验证','',f"上轮较优Sharpe处于H2.5%边界，本轮在见新结果前扩展到H3%。预设E=[0,0.0025,0.005]×H=[0.02,0.025,0.03]，每范围3×3网格。仅E0.25/0.5%、H3%的2新ETH＋2新父共{len(cfgs)}配置／{len(cost)}成本场景实算；7旧原生＋7旧父、42旧格点成本场景只读复用，不重写资格。20份唯一实际来源含BTC、未过滤L4/H2基线与匹配持有组件。完整读{ctx['registry_events']}登记事件／{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论；规范化研究定义{ctx['canonical_research_definitions_excluding_observations']}不等于全部有金融结果，初始16项均有原始实际证据。",'',
'假设与完整规则：上轮E0.25%未减少执行数、E0.5%虽少执行但净收益较差；本轮验证更高入场门槛是否提供额外局部支持，不预设缓冲必然省钱。ETH固定L4/S28，prior completed fastROC>H做空、<−H做多优先；带内实际多仓仅fast<E保留，实际空仓仅fast>−E保留，等于退出边界即平仓。E为ROC绝对收益，不是H倍数。S28慢方向门控始终作用；V10样本log收益SD<=4.5%仅用于新入场／翻向，退出不被拦截，同向实际q保持，flat不因缓冲创造仓位。','',
'真实银行与权重：BTC5000、N500、原L31/H4%/E1%；ETH15000、N4500。父原始权重[1,1]为两完整银行敞口，总20000、初始资金25%/75%，无归一化、NAV缩放、转账、免费再平衡或跨行抵押。q=floor(N/priorclose/LOT)×LOT，下一UTC00:01原生OPEN不利tick成交，反向先平后开，终止计费平仓。','',
'按时间验证：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折＋10日尾折；现金／q／entry／费用／资金费跨折不重置。近期40日继承day330真实状态并列8×5日折。确定性固定规则无拟合／标签，purge0，30日预热与3日间隔；所有信号只取prior完整close，成本输入仅past20完整日quoteADV／logvol。此历史反复用于研究，属于开发验证，非未触碰最终留出；保留多重选择、无DSR/PBO证明的局限。','',
'成本及约束：每边5bp费＋1bp半价差＋2bp滑点＋0.5×past20logvol×sqrt(实际q×OPEN/past20quoteADV)冲击，费用／价差／滑点／冲击1/2/3倍压力，资金费支出加压而正收入不放大。真实settlement纳秒／rate／mark／当时q；永续无虚构现货借币。原生LOT/tick/minnotional、参与率<=.001、费用后1倍入场抵押，独立银行1%闭合小时不利mark维护代理。无L2/TCA、完整历史档位／逐tick清算／真实容量证明。','',
'预冻结门槛不变：全年所有成本净正，1x>=9/12正完整月折；近期每档净正且>=6/8正5日折；3x完整DD<=25%；索引半径1含自身的局部三倍净正和严格近期比例各>=60%；至少4平仓，1x毛价差PnL+资金费/执行成本>=2.5；零拒单／负抵押／维护代理违规，终止flat、至少180日。旧点仅追加本轮扩大网格诊断，原status／criteria／sensitivity不变；报告边界、全格点正Sharpe比例和描述性相邻悬崖，不依据已见结果调整失败门槛。','',
'|新配置|范围|E%|H%|1x净%|2x净%|3x净%|3x完整DD%|正月/12|近期正5日1/2/3x|结论|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['E']*100:g}|{c['H']*100:g}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"实际{summary['passed']}passed／{summary['rejected']}rejected，失败判据分布{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}；当前完整网格严格近期合格数{summary['strict_recent_grid_qualified']}。正收益、负收益、所有折／变体均保留，passed仅本批历史门槛，非稳定实盘盈利。",'',
'10CSV逐档保留完整月折／近期折、连续日NAV、Sharpe／Calmar／完整DD、只读旧格点、相邻边、同资金持有／现金和旧未过滤基线；exit_buffer_vs_zero.csv同H隔离退出缓冲变化，列执行数／成本／资金费／回撤／净收益，防止将成本减少自动解释为收益改善。完整原生状态段、交易／资金费、每档545013点NAV SHA与复现代码保留，无可重建大数组。','',
f"独立研究审计actualexit0：{a['independent_new_policy_decisions']}新日决策，{a['new_native_curves']}新原生＋{a['new_parent_curves']}新父／{a['new_NAV_points']}完整NAV点，{a['read_only_native_curves']}只读原生／{a['read_only_parent_hashes']}只读父NAV；Fraction重算政策、Decimal独立核查原生数量／费用／规模冲击／资金费／现金、完整状态段和正持续时间小时风险。所有门槛另有独立check_decisions与旧资格对照。",'',
'原SMA65继续旧1500/500 Float现金／q／desired／已计成本与完整NAV前缀，从Nov1UTC00:30到02:30只加闭合分钟mark，下次Nov2UTC00:01决策不提前执行。原singleS28继续10000/10000、N1000/3000、ETHL3，独立未过滤L4/H2继续5000/15000、N500/4500、ETHL4原零退出；各自pointer续接，不把本轮过滤／缓冲装入冻结账户，0现金重启、无强制本轮平仓。新L4预定02:10到04:10仅在参考分钟闭合后采集。','',
'账户审计只复用冻结normalize做闭合数据／事件组装，独立核验Fraction目标、Decimal原生账务／资金费、正持续时间小时风险和完整NAV链；不调用原target/trade/transition/advance重跑观察。部分观察rejected保留180日计划；延迟shadow不是十策略实时公开报价执行或实盘成交。','',
'数据／代码精确SHA、reserve/finish实际命令／退出码、所有真实失败和必要恢复状态留档。只读网页同锁snapshot并检查，保留全部旧显示行／账户／报告；生成失败恢复上次有效汇总并记录，不能删负收益或改历史换取通过。不重部署网页、不增定时器、不下真实订单，直接main非强制发布。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
