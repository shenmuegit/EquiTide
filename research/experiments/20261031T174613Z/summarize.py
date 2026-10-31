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
fig.suptitle('Entry-only volatility ceiling V10/20/30 x C2.5/3.5/4.5% | ETH actual15000cash/4500entry | S28/zeroexit fixed\nParent adds BTC actual5000cash/500entry at raw child multipliers1/1 | O=readonly unchanged status, N=new actual | reused development history');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**plan['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['rejected']),'failed_criteria_by_scope':{scope:dict(collections.Counter(x for c in cfgs.values() if c['scope']==scope for x in c['failed_criteria'])) for scope in ['native','parent']},'positive_by_scope_role_cost':rep['summary']['positive_configs_by_scope_role_cost'],'strict_recent_grid_qualified':{scope:sum(recent_ok(full[g['fingerprint']]) for g in items) for scope,items in [('native',plan['native_grid']),('parent',plan['grid'])]},'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)

ref=plan['read_only_references'][plan['baseline_parent_fingerprint']];doc=json.loads((ROOT/ref['report']).read_text());base=next(c for c in doc['configs'].values() if c['fingerprint']==plan['baseline_parent_fingerprint']);diff=[]
for c in cfgs.values():
 if c['scope']!='parent':continue
 for k,s in c['scenes'].items():
  b=base['scenes'][k];diff.append([c['name'],c['V'],c['C'],k,s['net_return_pct'],b['net_return_pct'],s['net_return_pct']-b['net_return_pct'],s['max_drawdown_pct'],b['max_drawdown_pct'],s['executions'],b['executions'],s['cost_usdt'],b['cost_usdt'],sum(z['net_return_pct']>0 for z in s['recent40']['folds']),sum(z['net_return_pct']>0 for z in b['recent40']['folds']),ref['fingerprint']])
write('baseline_comparison.csv',['new_parent','volwindow','volcap','cost_multiplier','filtered_return_pct','unfiltered_return_pct','difference_pp','filtered_DD_pct','unfiltered_DD_pct','filtered_executions','unfiltered_executions','filtered_cost_usdt','unfiltered_cost_usdt','filtered_positive5d','unfiltered_positive5d','readonly_base_fingerprint'],diff);summary['CSV_rows']=rows;put(R/'sensitivity_summary.json',summary)
lines=['# 新入场波动率上限与独立未来计划','',f"实际18个新配置／54成本场景：9个ETH原生＋9个固定BTC/ETH组合，{summary['passed']}项passed、{summary['rejected']}项rejected；所有正负收益、逐折及失败留档。完整29个ETH15000/N4500既有定义已查重，无相同入场波动率上限规则。另冻结旧L4/H2的独立未来计划，工程验证不能当金融回测结果，未创建未来账户／观察。",'',
'新经济假设：反转信号的高波动入场可能带来噪声换手，入场前的已完成日收益波动率上限或能改善一致性，也可能错过有价值趋势。预先固定过去日志收益窗口V=[10,20,30]日×样本波动率上限C=[2.5%,3.5%,4.5%]，非按OOS分布拟合。ETH基础L4/H2%/S28/零退出不变，每日先按实际q和慢趋势门控求raw目标；只有raw非零且不同于实际方向的全新或反向入场受sigma<=C约束，sigma>C则目标现金。同向真实q保留，即使sigma超限也不额外平仓；原退出／不兼容慢趋势关闭仍执行，无隐藏方向。', '',
'固定金额：BTC原L31/H4%/退出缓冲1%，本金5000USDT／N500；ETH本金15000／N4500。原始子乘数[1,1]表示两完整实际银行，总20000，初始本金25%／75%；不归一化、调NAV、转账、再平衡、借款或跨行抵押净额。q=floor(固定N/前一完整日close/LOT)×LOT，下一UTC00:01原生OPEN不利tick执行，同向q不重算，翻向先平再开，最终付费平仓。18具体spec全部逐项reserve成功后才计算。','',
'Walk-forward：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日，12完整30日折＋10日尾折；现金/q/entry/费用/资金费跨折继承，近期40日从day330真实状态继续，8个5日折。入场波动率用j=i−V至i−1的log(C[j]/C[j−1])样本标准差，最大V30和S28均只用已闭合历史；成本波动仍独立按过去20日固定，不随V改估。确定性规则无拟合／标签，purge0，30日预热＋3日间隔。反复开发历史不是未触碰最终留出，无独立未来／DSR/PBO或多重选择校正声明。','',
'成本：每边5bp手续费＋1bp半价差＋2bp滑点＋0.5×过去20完整日样本log波动×sqrt(实际下单q×OPEN/过去20完整日quoteADV)冲击；1/2/3倍压力，原生LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押上限。真实funding settlement纳秒/mark/当时q，负支出加压、正收入不放大，不将available_ts未来资金费用于信号，不虚构现货借币。1%闭合小时不利mark维护代理每银行独立。缺L2/TCA、完整历史档位和逐tick清算，不是实盘容量／成交保证。','',
'失败判据沿用全年各成本净正、1x至少9/12正完整月折、近期各档净正且至少6/8正五日折、3x完整DD<=25%、局部正3倍及局部严格近期比例各>=60%、至少4平仓、1x毛价差PnL＋资金费/执行成本>=2.5、零拒单/负抵押/维护代理违规及终止平仓。两轴3x3完整邻域、全部Sharpe/Calmar/DD和描述性邻接/边界诊断保留，未看结果后降门槛。','',
'|新配置|范围|V日|上限|1x净%|2x净%|3x净%|3x整体DD%|正月折/12|近期正5日折1/2/3x|状态|','|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|']
for c in cfgs.values():lines.append('|'+c['name']+'|'+c['scope']+f"|{c['V']}|{c['C']*100:g}%|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"失败判据分布：{json.dumps(summary['failed_criteria_by_scope'],ensure_ascii=False)}；严格近期合格格点数：{summary['strict_recent_grid_qualified']}。通过仅为冻结开发历史门槛的候选，不称稳定实盘盈利。新V30/C3.5在3倍下原生与父全年净负，均保留。",'',
'新父组合与未过滤原L4/H2父组合的27逐成本差异另存baseline_comparison.csv，同本金/预算持有和解析现金0%比较见matched_hold_comparisons。改信号会改实际风险与敞口，不把差异全归成本。完整净值按共同整数ns/事件优先级对齐，整体/逐折/近期指标重算，不平均单币指标。必要交易/资金费/费用/状态段和545013点NAV SHA、逐日NAV及9CSV保留；未提交可重建大数组。','',
'独立未来计划prospective_l4/plan.json在本轮新过滤结果计算前冻结，固定旧父L4/H2：BTC5000/N500、ETH15000/N4500、无入场波动率过滤，原始1/1。计划2026-11-01 UTC00:01至2027-04-30 UTC00:01，共180日6折，终止前不强平；新指针l4h02_forward_latest.json/窗口l4h02_observation独立于原SMA/singleS28/十策略。core/observer/计划及来源SHA冻结，带原生数量、真实资金费、正持续小时风险、严格分钟/小时/重叠/元数据检查。未开始前run强制拒绝，status无HTTP/文件/registry写入，尚未创建账户或预留未来窗口。未来每真实截止仍须先reserve再advance，失败保留原状态并按协议恢复。','',
'未来工程验证仅用合成状态转移、AST比较成本/资金费与原生引擎一致，以及2220条既有基线日决策只读身份核对；包含实际5000/15000初始金额、500/4500预算LOT、强制开始前拒绝、未闭合bar拒绝、资金收入不加压及同ns零持续风险状态检查。未来业绩result_available=false，不将工程检查充当新实际金融结果。原SMA65/singleS28账户本轮独立续接，不改其本金/规则/持仓；十策略只读。','',
'一手背景：[AQR Trading Costs of Asset Pricing Anomalies](https://www.aqr.com/Insights/Research/Working-Paper/Trading-Costs-of-Asset-Pricing-Anomalies)，作者2012-12-05网页，访问2026-10-31，仅作传统股票成本背景，不用于加密成本数值或收益背书。独立审计及复现／失败／main发布证明见本轮检查回执、manifest和REPRODUCE。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
