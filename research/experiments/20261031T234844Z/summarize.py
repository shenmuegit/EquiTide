"""Exports from actual saved reports only; no strategy/order calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
from run import recent_ok
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());cfgs=rep['configs'];full=rep['all_current_grid'];Ls=plan['fast_lookbacks'];Hs=plan['fast_hurdles'];rows={}
def write(name,cols,items):
 with (R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];tail=[];daily=[];grid=[];edges=[];readonly=[]
for c in cfgs.values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['L'],c['H'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(x['net_return_pct']>0 for x in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  tail.extend([c['name'],c['scope'],c['L'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]:
 for g in items:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   grid.append([scope,g['L'],g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),recent_ok(c),c['current_grid_diagnostic_sensitivity']['local_positive3_fraction'],c['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction']])
   if g['readonly']:readonly.append(grid[-1])
 for k in ['1','2','3']:
  for g in items:
   i,j=Ls.index(g['L']),Hs.index(g['H']);neighbors=[h for h in items if i<2 and h['L']==Ls[i+1] and h['H']==g['H'] or j<2 and h['H']==Hs[j+1] and h['L']==g['L']]
   for h in neighbors:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['L'],g['H'],h['L'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
write('cost_scenes.csv',['configuration','fingerprint','scope','L','H','initial_capital_usdt','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','underlying_executions','underlying_closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','L','H','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','L','H','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],tail)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['scope','L','H','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','strict_recent_gate_diagnostic','local_positive3_fraction','local_recent_fraction']
write('sensitivity_grid.csv',cols,grid);write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['scope','cost_multiplier','from_L','from_H','to_L','to_H','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
comparisons=rep['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(comparisons[0]),[list(x.values()) for x in comparisons])
flags={}
for scope in ['native','parent']:
 for k in ['1','2','3']:
  vals=[x[8] for x in edges if x[:2]==[scope,k]];threshold=2*statistics.stdev(vals);flags[scope+'_'+k]={'edge_count':len(vals),'max_Sharpe_change':max(vals),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(vals)>threshold,'scope':'Descriptive dependent-edge heuristic only, not statistical significance/PBO/DSR.'}
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(17,8),layout='constrained')
for i,(scope,items) in enumerate([('native',plan['native_grid']),('parent',plan['grid'])]):
 for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(z['net_return_pct']>0 for z in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for g in items:arr[Ls.index(g['L']),Hs.index(g['H'])]=fn(full[g['fingerprint']])
  ax=axs[i,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),[f'{x*100:g}%' for x in Hs]);ax.set_yticks(range(3),Ls);ax.set_xlabel('Fast reversal hurdle H');ax.set_ylabel('Fast ROC lookback L days');ax.set_title(scope+'\n'+label)
  for g in items:
   a,b=Ls.index(g['L']),Hs.index(g['H']);ax.text(b,a,f'{arr[a,b]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.75)
fig.suptitle('Fast reversal outward L3/4/5 x H2/2.5/3% | fixed entry V10/cap4.5% | ETH actual15000cash/4500entry | S28/zeroexit fixed\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**plan['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['rejected']),'failed_criteria_by_scope':{scope:dict(collections.Counter(x for c in cfgs.values() if c['scope']==scope for x in c['failed_criteria'])) for scope in ['native','parent']},'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_grid_qualified':{scope:sum(recent_ok(full[g['fingerprint']]) for g in items) for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]},'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)

ref=plan['read_only_references'][plan['baseline_parent_fingerprint']];doc=json.loads((ROOT/ref['report']).read_text());base=next(c for c in doc['configs'].values() if c['fingerprint']==plan['baseline_parent_fingerprint']);diff=[]
for c in cfgs.values():
 if c['scope']!='parent':continue
 for k,s in c['scenes'].items():
  b=base['scenes'][k];diff.append([c['name'],c['L'],c['H'],k,s['net_return_pct'],b['net_return_pct'],s['net_return_pct']-b['net_return_pct'],s['max_drawdown_pct'],b['max_drawdown_pct'],s['executions'],b['executions'],s['cost_usdt'],b['cost_usdt'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),sum(z['net_return_pct']>0 for z in b['recent40']['folds']),ref['fingerprint']])
write('baseline_comparison.csv',['new_parent','fast_L','fast_H','cost_multiplier','filtered_return_pct','unfiltered_return_pct','difference_pp','filtered_DD_pct','unfiltered_DD_pct','filtered_executions','unfiltered_executions','filtered_cost_usdt','unfiltered_cost_usdt','filtered_positive5d','unfiltered_positive5d','readonly_base_fingerprint'],diff);summary['CSV_rows']=rows;put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text())
lines=['# 快信号门槛向3%外扩与独立冻结计划首次观察','',f"研究预设L3/4/5×H2/2.5/3%，固定入场V10日log收益样本标准差上限4.5%、S28／零退出。仅H3%的3原生ETH＋3父组合是新金融配置，共{len(cfgs)}定义／{len(cost)}成本场景；各范围6个旧格点、共36旧成本场景只读复用，旧资格和报告不变。本轮{summary['passed']}passed、{summary['rejected']}rejected。完整读取{ctx['registry_events']}登记事件、{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份完整结论，既往规范化策略定义{ctx['canonical_research_definitions_excluding_observations']}含不同状态，不表示全部有金融结果；ETH15000/N4500的53个既有完整经济定义已查重。初始16项实际证据齐全，无缺失金融结果可补测。",'',
'假设：上一快L/H网格的最高Sharpe落在H2.5边界，预定向H3%外扩而不事后追选收益。快ROC=C[i−1]/C[i−1−L]−1，严格>H做空、<−H做多；带内实际多仓仅fast<0保留、实际空仓仅fast>0保留，精确0退出。S28慢趋势方向门控始终应用。只有raw目标非零且不同于真实方向时，要求过去10个完整日log收益样本SD<=4.5%；超限只阻止新入场/翻向，不强平同向实际仓、不拦退出，无隐藏方向。','',
'真实资金：BTC5000／N500，L31/H4%/退出1%；ETH15000／N4500。父原始子乘数[1,1]是两个完整原生银行，合计20000，初始资本占比25%/75%；无归一化、权益缩放、转账、免费再平衡、借款或跨行抵押抵消。q=floor(N/priorclosedclose/LOT)×LOT，信号后下一UTC00:01原生OPEN不利tick成交，同向q保留，反向先平再开，370日终止付费平仓。','',
'Walk-forward：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折＋10日尾折，状态和成本跨折不重置；近期40日继承day330状态，8×5日折逐成本。确定性规则无拟合/标签，purge0、30日预热/3日间隔，所有信号用完整prior close，成本特征用过去20完整日波动/quoteADV。反复开发历史不称未触碰最终测试集，未声称DSR/PBO多重选择修正或独立未来资格。','',
'1/2/3倍成本：每边5bp费＋1bp半价差＋2bp滑点＋0.5×过去20日log波动×sqrt(实际q×OPEN/过去20日quoteADV)冲击，原生LOT/tick/minnotional、参与率<=.001、费用后1倍入场抵押上限。实际永续settlement纳秒/rate/mark/当时q，资金费支出加压、正收入不放大；无虚构现货借币。独立银行1%闭合小时不利mark维护代理，缺盘口/TCA、完整历史档位和逐tick清算，不能称真实容量/成交已验证。','',
'预冻结失败门槛：所有成本全年净正，1x>=9/12正月折，近期各档净正且>=6/8正5日折，3x整体DD<=25%，索引半径1含自身的局部三倍净正与严格近期比例均>=60%，至少4平仓，1x毛价差PnL+资金费/执行成本>=2.5，零拒单/负抵押/维护代理违规，终止平仓和至少180日。原生/父分别验证，旧格点本轮邻域仅诊断，不改原criteria/sensitivity/status。','',
'|新配置|范围|L|H|1x净%|2x净%|3x净%|3x整体DD%|正月折/12|正五日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['H']*100:g}%|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"失败判据分布：{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}；当前完整网格严格近期格点数{summary['strict_recent_grid_qualified']}。全部净收益/负收益/淘汰与失败保留，passed仅历史门槛，不称稳定实盘盈利。",'',
'所有变体的全年/逐折/近期净收益、整体DD、Sharpe、Calmar、成本占比与交易数、全dailyNAV、相邻Sharpe差/边界峰保存于9CSV和图；持有/现金0%比较为同本金非同风险。旧未过滤L4/H2基线逐成本比较不独立归因于过滤器；新规则同时改变快门槛。每档完整545013点NAV SHA与原生状态段/逐笔费用和资金费保存，大数组不提交。独立Fraction核查3330新日决策、Decimal会计/规模相关冲击/资金费/小时风险、9新原生＋9新父和30只读原生／24只读父完整NAV与各折/近期指标，不调用旧策略模拟。','',
'独立未来计划保持20261031T174613Z/prospective_l4原冻结SHA，未过滤ETH L4/H2/S28/零退出，BTC5000/N500、ETH15000/N4500、raw1/1、总20000；2026-11-01 UTC00:01至2027-04-30 UTC00:01。首次截止预先固定00:10，等执行参考分钟真实闭合后才调用原执行器，独立指针l4h02_forward_latest、独立账本和3观察ID；不以本轮H3过滤研究替换它。计划开始前status为只读waiting/0HTTP/0新账户；实际首次结果、真实raw/packet SHA及独立审计见本轮l4h02_observation、l4h02_verification。9分钟部分观察不是180日/六折通过，partial rejected不取消冻结计划。','',
'首次独立观察需要真实33完整日1m预热，原始分页和packet完整保存在忽略的data/raw/binance/l4h02_forward并记录精确SHA；Git仅保留必要小响应、规范化daily上下文/实际首日决策、逐笔账本/完整短窗口NAV、全输入哈希和复现代码，不把大预热行情提交或清理。此前原SMA65/singleS28按原本金与状态续接至22:30，十策略只读，互不替代。','',
'沿用已读[AQR Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)作为传统股票成本背景，非加密成本校准或收益背书。真实Binance输入、命令、退出码、失败与完整main远端发布证明全部留档。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
