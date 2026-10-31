"""Exports from actual saved reports only; no strategy/order calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
from run import recent_ok
rep=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());cfgs=rep['configs'];full=rep['all_current_grid'];Ls=plan['volatility_windows'];Hs=plan['volatility_caps'];rows={}
def write(name,cols,items):
 with (R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];tail=[];daily=[];grid=[];edges=[];readonly=[]
for c in cfgs.values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['V'],c['C'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(x['net_return_pct']>0 for x in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['scope'],c['V'],c['C'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  tail.extend([c['name'],c['scope'],c['V'],c['C'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],c['scope'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]:
 for g in items:
  c=full[g['fingerprint']]
  for k,s in c['scenes'].items():
   grid.append([scope,g['V'],g['C'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),recent_ok(c),c['current_grid_diagnostic_sensitivity']['local_positive3_fraction'],c['current_grid_diagnostic_sensitivity']['local_strict_recent_fraction']])
   if g['readonly']:readonly.append(grid[-1])
 for k in ['1','2','3']:
  for g in items:
   i,j=Ls.index(g['V']),Hs.index(g['C']);neighbors=[h for h in items if i<2 and h['V']==Ls[i+1] and h['C']==g['C'] or j<2 and h['C']==Hs[j+1] and h['V']==g['V']]
   for h in neighbors:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['V'],g['C'],h['V'],h['C'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
write('cost_scenes.csv',['configuration','fingerprint','scope','V','C','initial_capital_usdt','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','underlying_executions','underlying_closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','scope','V','C','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','scope','V','C','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],tail)
write('daily_NAV.csv',['configuration','scope','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['scope','V','C','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','strict_recent_gate_diagnostic','local_positive3_fraction','local_recent_fraction']
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
  for g in items:arr[Ls.index(g['V']),Hs.index(g['C'])]=fn(full[g['fingerprint']])
  ax=axs[i,j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),[f'{x*100:g}%' for x in Hs]);ax.set_yticks(range(3),Ls);ax.set_xlabel('Entry sample-logvol ceiling C');ax.set_ylabel('Past log-vol window V days');ax.set_title(scope+'\n'+label)
  for g in items:
   a,b=Ls.index(g['V']),Hs.index(g['C']);ax.text(b,a,f'{arr[a,b]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.75)
fig.suptitle('Entry-only volatility ceiling Outward V5/10/15 x C3.5/4.5/5.5% | ETH actual15000cash/4500entry | S28/zeroexit fixed\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**plan['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['rejected']),'failed_criteria_by_scope':{scope:dict(collections.Counter(x for c in cfgs.values() if c['scope']==scope for x in c['failed_criteria'])) for scope in ['native','parent']},'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_grid_qualified':{scope:sum(recent_ok(full[g['fingerprint']]) for g in items) for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]},'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)

ref=plan['read_only_references'][plan['baseline_parent_fingerprint']];doc=json.loads((ROOT/ref['report']).read_text());base=next(c for c in doc['configs'].values() if c['fingerprint']==plan['baseline_parent_fingerprint']);diff=[]
for c in cfgs.values():
 if c['scope']!='parent':continue
 for k,s in c['scenes'].items():
  b=base['scenes'][k];diff.append([c['name'],c['V'],c['C'],k,s['net_return_pct'],b['net_return_pct'],s['net_return_pct']-b['net_return_pct'],s['max_drawdown_pct'],b['max_drawdown_pct'],s['executions'],b['executions'],s['cost_usdt'],b['cost_usdt'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),sum(z['net_return_pct']>0 for z in b['recent40']['folds']),ref['fingerprint']])
write('baseline_comparison.csv',['new_parent','volwindow','volcap','cost_multiplier','filtered_return_pct','unfiltered_return_pct','difference_pp','filtered_DD_pct','unfiltered_DD_pct','filtered_executions','unfiltered_executions','filtered_cost_usdt','unfiltered_cost_usdt','filtered_positive5d','unfiltered_positive5d','readonly_base_fingerprint'],diff);summary['CSV_rows']=rows;put(R/'sensitivity_summary.json',summary)
lines=['# 新入场波动率上限外扩验证','',f"本轮预定外扩V=[5,10,15]日×C=[3.5%,4.5%,5.5%]，补充7原生ETH＋7父组合，共{len(cfgs)}个新配置／{len(cost)}成本场景，{summary['passed']}passed、{summary['rejected']}rejected。各范围2个旧点直接只读复用，12旧成本场景资格／原报告保持。完整38个ETH15000/N4500既有经济定义查重，无精确新点重复。所有正负收益与失败保留。",'',
'假设：上轮峰位于V10/C4.5的边界，向更短窗口和更宽上限外扩检验平台，不沿OOS挑局部赢家。基础ETH L4/H2%/S28/零退出和对新旧实际仓位始终应用的慢趋势方向门控不变；只在raw目标非零且不同于真实方向时，要求截至前一完整日的V个log日收益样本标准差sigma<=C。sigma>C阻止全新或翻向新仓，不阻止原有退出、不强平同方向仓位，无隐藏方向。18个旧批次不重跑，本轮14个新spec逐项reserve成功才计算。','',
'资金／执行固定：BTC真实5000USDT本金／N500、L31/H4%/退出缓冲1%；ETH真实15000／N4500。父原始子乘数[1,1]是两个完整银行，总20000，初始本金占比25%／75%，无归一化、NAV权益份额缩放、转账、免费再平衡、借款或跨行抵押抵消。q=floor(N/前一完整日close/LOT)×LOT，下一UTC00:01原生OPEN不利tick成交，同向q保留，反向先平再开，终止付费平仓。','',
'Walk-forward：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折＋10日尾折，现金/q/entry/费用/资金费跨折不重置；近期40日继承day330真实状态并报告8个5日折。波动窗口j=i−V至i−1严格只用已闭合close；执行成本仍用过去20完整日波动及quoteADV，独立于入场V，不随新参数降低成本假设。确定性规则无拟合／标签，purge0、30日预热＋3日间隔，信号可得后60秒成交。反复开发历史不是未触碰最终测试集，无独立未来或多重选择修正证明。','',
'成本：每边5bp手续费＋1bp半价差＋2bp滑点＋0.5×过去20完整日样本log波动×sqrt(实际q×OPEN/过去20完整日quoteADV)冲击；1/2/3倍压力。原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押上限。实际funding settlement纳秒／mark／当时q记账，支出加压，正收入不增，available_ts不进入信号，无虚构现货借币。独立银行1%闭合小时不利mark维护代理；缺L2/TCA、完整历史档位和逐tick清算，不称真实容量／成交已验证。','',
'敏感性与门槛：完整两轴3x3、索引半径1含自身，原生与父分别检查，旧点本轮邻域诊断单列不重写原criteria/sensitivity/status。沿用全年所有成本净正、1x至少9/12正月折、近期各档净正且至少6/8正五日折、3x完整DD<=25%、局部3倍净正与局部严格近期比例各>=60%、至少4平仓、1x毛价差PnL＋资金费/执行成本>=2.5、零拒单／负抵押／维护代理违规及终止平仓；未看结果后改门槛。全部变体Sharpe/Calmar/DD、正Sharpe比例、边界／描述性邻接启发式保存，不作DSR/PBO或独立样本声明。','',
'|新配置|范围|V日|上限|1x净%|2x净%|3x净%|3x整体DD%|正月折/12|正五日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['V']}|{c['C']*100:g}%|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"失败判据分布：{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}；完整网格严格近期合格数：{summary['strict_recent_grid_qualified']}。所有passed仅为历史开发候选，不称稳定实盘盈利。",'',
'21个新父逐成本对未过滤旧L4/H2的净收益、完整DD、成交数和成本差异见baseline_comparison；27逐完整父格点／成本持有与解析现金0%比较见matched_hold_comparisons，相同本金不等于相同风险。真实联合时间轴按事件优先级对齐，整体／折／近期指标由完整NAV重算，不平均单币指标。每档545013点SHA、状态段、实际交易／资金费／费用、全部dailyNAV及9CSV保留，不提交可重建大数组。','',
'独立审计：Fraction重算7770条新日决策，独立样本方差重算入场波动率，Decimal逐笔复核LOT/tick/现金/冲击/费用/funding/小时维护，21新原生＋21新父以及18只读原生／12只读父的NAV与全部折／近期指标核对；新资格及旧点原资格另核验，旧信号／回测不重跑。','',
'已冻结的独立未来旧L4/H2计划仍在20261031T174613Z/prospective_l4/，原始SHA、5000/15000本金与500/4500预算、无波动过滤和180日规则保持，未复制／重绑／修改。开始2026-11-01 UTC00:01，终止2027-04-30 UTC00:01；本轮仅status只读确认尚未开始，0新账户／0未来观察／0HTTP和registry写入，不把工程检查作为新金融结果。原SMA65/singleS28本轮各自续接，十策略只读，不使用新过滤策略替换其规则、本金或持仓。','',
'一手背景：[AQR Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，作者2012-12-05网页，访问2026-10-31，仅作传统股票成本背景，不作加密成本校准或收益背书。真实数据SHA、原始响应小副本、复现命令／退出码、失败与main实际发布证明完整留档。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
