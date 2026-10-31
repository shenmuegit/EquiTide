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
fig.suptitle('Fast reversal L3/4/5 x H1.5/2/2.5% | fixed entry V10/cap4.5% | ETH actual15000cash/4500entry | S28/zeroexit fixed\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**plan['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['rejected']),'failed_criteria_by_scope':{scope:dict(collections.Counter(x for c in cfgs.values() if c['scope']==scope for x in c['failed_criteria'])) for scope in ['native','parent']},'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_grid_qualified':{scope:sum(recent_ok(full[g['fingerprint']]) for g in items) for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]},'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)

ref=plan['read_only_references'][plan['baseline_parent_fingerprint']];doc=json.loads((ROOT/ref['report']).read_text());base=next(c for c in doc['configs'].values() if c['fingerprint']==plan['baseline_parent_fingerprint']);diff=[]
for c in cfgs.values():
 if c['scope']!='parent':continue
 for k,s in c['scenes'].items():
  b=base['scenes'][k];diff.append([c['name'],c['L'],c['H'],k,s['net_return_pct'],b['net_return_pct'],s['net_return_pct']-b['net_return_pct'],s['max_drawdown_pct'],b['max_drawdown_pct'],s['executions'],b['executions'],s['cost_usdt'],b['cost_usdt'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),sum(z['net_return_pct']>0 for z in b['recent40']['folds']),ref['fingerprint']])
write('baseline_comparison.csv',['new_parent','fast_L','fast_H','cost_multiplier','filtered_return_pct','unfiltered_return_pct','difference_pp','filtered_DD_pct','unfiltered_DD_pct','filtered_executions','unfiltered_executions','filtered_cost_usdt','unfiltered_cost_usdt','filtered_positive5d','unfiltered_positive5d','readonly_base_fingerprint'],diff);summary['CSV_rows']=rows;put(R/'sensitivity_summary.json',summary)
lines=['# 固定波动率入场过滤后的快信号邻域检验','',f"本轮预先固定V10日log收益样本波动率上限4.5%，只扰动快信号L=[3,4,5]日、H=[1.5%,2%,2.5%]。8原生ETH＋8父组合，共{len(cfgs)}新配置／{len(cost)}新成本场景，{summary['passed']}passed、{summary['rejected']}rejected；两个旧L4/H2中心配置的6成本场景只读复用，原资格／criteria／sensitivity／报告不改。本轮完整读取登记{json.loads((R/'context.json').read_text())['registry_events']}事件／{json.loads((R/'context.json').read_text())['registry_ids']}ID及256份完整中文结论；ETH真实15000/N4500的45个既有经济定义已逐项查重。初始16历史项实际证据齐全，没有以代码／工程检查冒充回测。",'',
'经济假设：既有V/cap外扩支持不等于快信号规则稳健，因此在固定旧入场过滤条件下，预设快ROC窗口和门槛的完整3×3联合邻域。rawfast=C[i−1]/C[i−1−L]−1；严格rawfast>H做空、<−H做多；带内仅当rawfast<0保留实际多仓、rawfast>0保留实际空仓，精确0退出。对新旧仓始终应用S28慢趋势方向门控，方向不合即目标平。仅当目标非零且不同于实际方向时，要求过去10个完整日log收益样本标准差<=4.5%；超限禁止全新／翻向新仓，不强平同向实际仓，不阻止退出，无隐藏方向状态。','',
'资金与权重：BTC真实5000USDT／N500，原L31/H4%/退出1%；ETH真实15000／N4500，S28/零退出。父子原始乘数[1,1]保留，是两完整银行合计20000，初始资本占比25%/75%；不是权益份额缩放，不自动归一化、不转账、无免费再平衡、借款或跨行抵押抵消。q=floor(N/前一完整日close/LOT)×LOT，下一UTC00:01原生OPEN计不利tick，同向q保留、反向先平后开、终止付费平仓。','',
'Walk-forward：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折＋10日尾折；现金/q/entry/成本/资金费跨折不重置。近期40日继承day330实际状态，8个5日折逐档报告。所有信号只用prior closed close，成本用过去20完整日波动和quoteADV，参数变化不降低成本假设。确定性规则无拟合／标签，purge0、30日预热和3日间隔，信号可得后60秒成交；反复使用的历史仅开发验证，不称未触碰最终测试集，没有独立未来或多重选择修正证明。','',
'成本压力1/2/3倍：每边5bp手续费＋1bp半价差＋2bp滑点＋0.5×过去20日log波动×sqrt(实际q×OPEN/过去20日quoteADV)冲击，原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押上限；永续使用实际settlement纳秒／rate／mark／当时q，资金费支出加压、正收入不放大，无虚构现货借币。独立银行1%闭合小时不利mark维护代理不等于真实逐tick清算；缺L2/TCA及完整历史档位，不称真实成交或容量已验证。','',
'失败门槛在结果前冻结：所有成本全年净正、1x至少9/12正月折、近期各档净正且至少6/8正五日折、3x完整DD<=25%、索引半径1含自身的局部三倍净正及严格近期比例各>=60%、至少4平仓、1x毛价差PnL＋资金费/执行成本>=2.5、零拒单／负抵押／维护代理违规、终止平仓、至少180日。原生和父分别检验。描述性相邻Sharpe变化、边界峰和正Sharpe比例另存，不在看结果后新增／放松资格门槛。','',
'|新配置|范围|L日|H|1x净%|2x净%|3x净%|3x整体DD%|正月折/12|正五日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['L']}|{c['H']*100:g}%|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"失败判据分布：{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}；完整3×3严格近期合格单元：{summary['strict_recent_grid_qualified']}。passed仅是本批历史门槛通过，不称稳定实盘盈利。",'',
'相同真实银行的持有与现金0%对照见matched_hold_comparisons；baseline_comparison以旧未过滤L4/H2原基线逐成本比较。新L/H变体同时改变快信号，因此此基线差异不能独立归因于过滤器本身。所有原生/父整体DD、Sharpe、Calmar和逐折指标由完整NAV重算，不平均单币指标。每成本545013点NAV SHA、实际状态段／交易／资金费、dailyNAV和全部逐折CSV保留，不提交可重建大数组。','',
'独立审计：Fraction逐条重算8880个新日决策，独立fsum样本方差核验V10过滤，Decimal逐笔复核LOT/现金/费用/size-ADV冲击/funding/小时风险。24新原生＋24新父，以及15只读原生和9只读父完整NAV SHA、整体／13折／近期8折指标核对；16新资格和两个旧中心原资格独立检查，旧信号／回测不重跑。','',
'原SMA65与singleS28按各自冻结规则／本金／状态续接，十策略只读。独立未来旧未过滤L4/H2计划仍引用20261031T174613Z/prospective_l4原文件，开始2026-11-01 UTC00:01、结束2027-04-30 UTC00:01，未复制／重绑／改参数，本轮仅status确认waiting，0新账户／观察／HTTP／registry写入。新过滤研究不替换该未来计划或原账户。','',
'预登记前一次family含大写的schema检查失败，随后的只读检查因未生成plan而失败；两个真实失败和修正前源／spec保留在engineering_failures。修正发生在任何金融reserve／计算前，既无未登记金融结果，也无完成回测重跑。全部成功、负收益、淘汰及失败保留。','',
'一手成本背景沿用已读[AQR Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，仅传统股票成本方法背景，不作加密成本校准或本策略收益背书。实际数据为已哈希Binance历史与本窗口公开响应；复现、账本连续性、只读快照和main远端发布证据另存。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
