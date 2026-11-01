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
fig.suptitle('Exit hysteresis E0/0.25/0.5% x entryH2/2.5% | fastL4 | fixed entry V10/cap4.5% | ETH actual15000cash/4500entry | S28 slowgate fixed; exit E varies\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
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
ctx=json.loads((R/'context.json').read_text())
lines=['# 退出缓冲与入场门槛联合检验及跨日账户续接','',f"本轮固定L4/S28、V10日log收益样本SD入场上限4.5%，预设退出缓冲E=[0,0.0025,0.005]×入场门槛H=[0.02,0.025]，即3×2网格。零缓冲两原生／两父配置的12成本场景只读复用；4新ETH＋4新父共{len(cfgs)}配置／{len(cost)}成本场景逐项reserve后实际执行，{summary['passed']}passed、{summary['rejected']}rejected。完整读取{ctx['registry_events']}登记事件、{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份完整结论，规范化研究定义{ctx['canonical_research_definitions_excluding_observations']}包含不同状态，不代表全部有金融结果。初始16项实际证据齐全；ETH15000/N4500的56个既有完整定义已语义查重。",'',
'经济假设：快反转策略在零附近反复退出／重入可能消耗成本。E是ROC绝对收益缓冲，不是H的比例。严格fast>H做空、fast<−H做多优先；带内实际多仓仅当fast<E保留，实际空仓仅当fast>−E保留；fast等于对应退出界限即退出。E=0严格还原原零退出。缓冲不会为平仓状态创造新仓；S28慢趋势门控始终应用；只有新入场或翻向时需满足固定V10/cap4.5%，同向实际q保留，退出从不被波动过滤拦截，无隐藏方向。更长持仓可能增加资金费或亏损，全部计入实算。','',
'真实资金／权重：BTC5000/N500原L31/H4%/退出1%；ETH15000/N4500。父原始子乘数[1,1]表示两个完整银行，总20000、初始本金占比25%/75%，无归一化、权益缩放、转账、免费再平衡、借款或跨行抵押抵消。q=floor(N/priorclosedclose/LOT)×LOT，下一UTC00:01原生OPEN计不利tick；同向q保留、反向先平后开，370日终止付费平仓。','',
'Walk-forward：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折＋10日尾折；现金/q/entry/成本/资金费跨折不重置。近期40日继承day330真实状态、8×5日折各档单列。确定性规则无拟合／标签，purge0、30日预热与3日间隔；信号仅完整prior close，执行成本仅过去20完整日波动／quoteADV。重复使用的历史仅开发验证，不称未触碰最终测试集，无独立最终留出或DSR/PBO修正证明。','',
'1/2/3倍成本：每边5bp手续费＋1bp半价差＋2bp滑点＋0.5×过去20日log波动×sqrt(实际q×OPEN/过去20日quoteADV)冲击，原生LOT/tick/minnotional、参与率<=.001、费用后1倍入场抵押限制。实际永续settlement纳秒／rate／mark／当时q，支出加压、正资金费收入不放大。无虚构现货借币；独立银行1%闭合小时不利mark维护代理，缺L2/TCA、完整历史档位与逐tick清算，不称真实成交或容量已验证。','',
'预冻结失败门槛：全年所有成本净正、1x>=9/12正月折，近期各档净正且>=6/8正5日折，3x完整DD<=25%，索引半径1含自身的局部三倍净正及严格近期比例各>=60%，至少4平仓，1x毛价差PnL+资金费/执行成本>=2.5，零拒单／负抵押／维护代理违规，终止平仓、至少180日。原生／父分开，旧格点只增本轮诊断，不重写原criteria/sensitivity/status。两列H只能说明有限局部支持，边界／描述性悬崖和正Sharpe比例另存，不声称全域最优。','',
'|新配置|范围|E退出%|H入场%|1x净%|2x净%|3x净%|3x完整DD%|正月折/12|正5日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['E']*100:g}|{c['H']*100:g}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"失败判据分布{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}；当前完整网格严格近期合格数{summary['strict_recent_grid_qualified']}。全部成功／负收益／淘汰／失败保存，passed仅本批历史门槛，不称稳定实盘盈利。",'',
'exit_buffer_vs_zero.csv逐H、同本金／预算／入场过滤比较新E与只读E0的净收益、DD、交易数、执行成本及资金费；成本减少不自动等于净收益或近期稳健改善。与旧未过滤L4/H2基线、持有及现金0%比较另存；同本金不表示同风险。所有整体／逐折／近期Sharpe、Calmar、DD从完整NAV重算，不平均单币指标。10CSV含全部dailyNAV、每档545013点NAV SHA、完整状态段／交易／资金费保存，不提交可重建大数组。','',
'独立研究审计以Fraction重算4440新日决策，Decimal独立核对原生LOT/现金/规模冲击/费用/funding/小时风险；12新原生＋12新父、18只读原生／12只读父完整NAV和各折／近期指标核对，8新资格及旧格点原资格独立检查。','',
'原SMA65实际Floating现金/q/desired/累计成本不改，使用原65日/1%/75:25规则处理Nov1UTC00:01日决策；原singleS28继续10000/10000、N1000/3000、ETHL3，处理真实00资金费和00:01日转移；独立未过滤L4/H2继续原5000/15000、N500/4500、ETHL4，专属pointer从00:10续至02:10，不重新开现金，不替换成本轮缓冲策略。三份完整账本／指针／原计划和终止时刻分别保存；部分观察rejected不取消长期计划。','',
'账户核验仅复用冻结normalize进行闭合数据/事件组装，独立复核实际新完成日、Fraction目标、Decimal费用／数量／资金费／现金、正持续时间小时风险、完整原NAV前缀和当前全NAV／日边界／部分资格；不调用原target/trade/transition/advance来重做观察。旧SMA另有独立SMA/成本/Float现金和全部原NAV审计。观察都是延迟闭合数据重建，不是十策略真实报价模拟或实盘订单，不用数小时表现解释180日／六折能力。','',
'沿用已读[AQR Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)为传统股票成本背景，非加密校准或策略收益背书。真实Binance输入SHA、stdout/退出码、全部真实失败、只读snapshot和main非强制发布证明留档，无重部署／新定时任务／真实订单。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
