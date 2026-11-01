"""Export every saved scene and fixed bank/H grid; no strategy calculation."""
import collections,csv,json,statistics
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
rep=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());full=rep['all_current_grid'];rows={}
def write(n,cols,items):
 with (R/n).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[n]=len(items)
cost=[];wf=[];recent=[];daily=[];grid=[];readonly=[];edges=[];alloc=[];sources=[]
for c in rep['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['BTC_capital_usdt'],c['H'],c['capital_usdt'],c['BTC_capital_usdt']/c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']])
  wf.extend([c['name'],c['BTC_capital_usdt'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['duration_days'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['folds'])
  recent.extend([c['name'],c['BTC_capital_usdt'],c['H'],k,z['fold'],z['start_utc'],z['end_exclusive_utc'],z['net_return_pct'],z['max_drawdown_pct'],z['sharpe_365'],z['calmar']] for z in s['recent40']['folds'])
  daily.extend([c['name'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
for g in p['grid']:
 c=full[g['fingerprint']];C=g['BTC_capital_usdt'];alloc.append([g['fingerprint'],'candidate',C,15000,C+15000,C/10,4500,1,1,C/(C+15000),15000/(C+15000),g['H'],g['readonly']])
 for k,s in c['scenes'].items():
  d=c['current_grid_diagnostic_sensitivity'];z=[C,g['H'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']];grid.append(z)
  if g['readonly']:readonly.append(z)
for g in p['benchmarks']:
 C=g['BTC_capital_usdt'];alloc.append([g['fingerprint'],'matched_budget_hold',C,15000,C+15000,C/10,4500,1,1,C/(C+15000),15000/(C+15000),None,g['readonly']])
for k in ['1','2','3']:
 for g in p['grid']:
  i,j=p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H']);ng=[h for h in p['grid'] if i<2 and h['BTC_capital_usdt']==p['BTC_capitals'][i+1] and h['H']==g['H'] or j<2 and h['H']==p['fast_hurdles'][j+1] and h['BTC_capital_usdt']==g['BTC_capital_usdt']]
  for h in ng:
   a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([k,g['BTC_capital_usdt'],g['H'],h['BTC_capital_usdt'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('cost_scenes.csv',['configuration','fingerprint','BTC_bank','signal_H','total_capital','BTC_capital_share','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','underlying_executions','underlying_closes','recent40_return_pct','positive5d_folds','status'],cost)
write('walk_forward_folds.csv',['configuration','BTC_bank','ETH_H','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf)
write('recent40_folds.csv',['configuration','BTC_bank','ETH_H','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent)
write('daily_NAV.csv',['configuration','cost_multiplier','boundary','NAV_usdt'],daily)
cols=['BTC_bank','ETH_H','fingerprint','readonly_old','unchanged_canonical_status','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_recent_fraction']
write('sensitivity_grid.csv',cols,grid);write('readonly_reused_scenes.csv',cols,readonly)
write('adjacent_edges.csv',['cost_multiplier','from_BTC_bank','from_H','to_BTC_bank','to_H','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges)
cs=rep['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_initial_entry_N','cost_multiplier','return_pct','wholeDD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','readonly_report','readonly_report_sha256'],sources)
write('bank_allocations.csv',['fingerprint','role','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_component_weight','raw_ETH_component_weight','explicit_BTC_capital_share','explicit_ETH_capital_share','ETH_H','readonly'],alloc)
flags={}
for k in ['1','2','3']:
 vals=[x[7] for x in edges if x[0]==k];threshold=2*statistics.stdev(vals);flags[k]={'edge_count':len(vals),'max_Sharpe_change':max(vals),'two_std_change_threshold':threshold,'descriptive_cliff_flag':max(vals)>threshold,'scope':'Descriptive dependent-edge heuristic, not DSR/PBO or statistical significance.'}
put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(1,4,figsize=(16,5.2),layout='constrained')
for j,(label,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(z['net_return_pct']>0 for z in c['scenes']['3']['recent40']['folds']))]):
 arr=np.empty((3,3))
 for g in p['grid']:arr[p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H'])]=fn(full[g['fingerprint']])
 ax=axs[j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['2%','2.5%','3%']);ax.set_yticks(range(3),[f'{C} / {100*C/(C+15000):.2f}%' for C in p['BTC_capitals']]);ax.set_xlabel('ETH fast entry hurdle H');ax.set_ylabel('BTC actual bank / share of total');ax.set_title(label)
 for g in p['grid']:
  i,k=p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
 fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('Actual BTC bank3125/3750/4375 at native N312.5/375/437.5 | fixed ETH15000/N4500\nETH L4/S28, E0.25%, V10/cap4.5% | raw child multipliers [1,1], no NAV scaling | O=readonly, N=new | reused development history')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(x for c in rep['configs'].values() for x in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text());cand=[c for c in rep['configs'].values() if c['role']=='candidate'];comp=[c for c in rep['configs'].values() if c['role']=='component'];controls=[c for c in rep['configs'].values() if c['role'].startswith('benchmark')]
lines=['# BTC原生资金临界区间与ETH入场门槛验证','',f"本轮12个新金融定义：BTC3125/N312.5和4375/N437.5各自的动量组件及常多参考共4个原生路径，交叉ETH H2%/2.5%/3%共6个新父候选，两个同资金/同初始入场预算常多父参考；36个1/2/3倍成本场景全部先独立reserve再计算。旧BTC3750的3个组合候选、1个持有父及6个原生来源只读复用，共10个唯一旧定义。完整读取{ctx['registry_events']}事件、{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份结论；初始16项均有真实原始证据，不精确重复。",'',
'假设见结果前固定：上轮BTC2500近期失败，旧3750/H2.5成为宽网格内部Sharpe峰值，但宽网格严格近期仅4/9。预先选3750两侧等距625的3125/4375实际银行，保留H2/2.5/3%邻域，检验更近的真实数量取整/成本临界区域。BTC N固定为自身初始资金10%，资金与入场预算绑定，不能声称两个独立参数。新的4原生路径从真实行情计算q/LOT、tick、规模冲击、现金和资金费，不线性缩放旧NAV。此选择已使用过往结果，只是开发研究，不是独立未触碰最终测试。','',
'组合原权重[1,1]为一份完整BTC原生银行和一份ETH15000银行。总初始资金18125/18750/19375，BTC资金占比17.241379%/20%/22.580645%；BTC初始N312.5/375/437.5，ETH N4500。美元净值直接相加，不重复乘资金份额、不平均Sharpe/收益率；无父再平衡订单、资金转账、NAVresize或跨账户抵押净额。实际N/C0各不相同，不称同风险比较。常多基准匹配银行及初始N，非满仓买持或同风险基准；另与现金0%比较。','',
'BTC原ROC31/H4%/E1%；ETH固定L4/S28、退出缓冲绝对ROC0.0025、V10样本logvol cap0.045，仅新入场/翻向过滤。ETH priorfastROC>H空、<−H多；带内实际多仅r<E、空仅r>−E保留，等号退出，slow方向始终门控。q=floor(N/prior完整日close/LOT)×LOT，下一UTC00:01原生OPEN不利tick，翻向先平后开，同向保留实际q，370日终止计费平仓。','',
'历史边界2025-10-19 UTC00:01至2026-10-24 UTC00:01，连续370天、12个完整30天折和10天尾折；跨折不重置现金/q/成本/funding。近期40天继承day330，8个5天折。固定规则无拟合或标签，purge0、预热30天/间隔3天，决策仅用prior完整日close；成本仅past20完整日quoteADV和样本logvol。历史多次使用与多重选择偏差明示，不把本轮正收益或局部邻域当独立未来/DSR/PBO证明。','',
'1/2/3倍成本：每边5bp费用、1bp半价差、2bp滑点、0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)。真实资金费结算纳秒/rate/mark/当时q，支出倍增、正收入不放大。实际LOT/tick/minnotional、参与率<=0.001、费用后1倍入场抵押和每银行1%闭合小时不利mark维护代理；线性永续无需现货借币，不虚构借币费。没有L2/TCA、完整历史抵押阶梯/逐tick清算或真实容量证明。','',
'原门槛不放宽：每档全年净正，1倍>=9/12正完整30天折；每档近期40天净正且>=6/8正5天折；3倍完整DD<=25%；资金/H索引半径1含中心的局部3倍净正比例与严格近期达标比例各>=60%；至少4次平仓，毛价差PnL+fund/执行成本>=2.5，零拒单/负抵押/维护代理违规、终止flat、至少180天。原生动量component按资金轴一维邻域执行同样财务门槛，单列资格，不计父候选。4个持有控制（2原生、2父）按冻结非候选criterion=false保留真实结果，控制角色失败不等于未计算。','',
'|新配置|角色|BTC银行/总C0|H%|1倍净%|2倍净%|3倍净%|3倍整体DD%|正月/12|近期正折1/2/3倍|状态|','|---|---|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in rep['configs'].values():
 h='—' if c['H'] is None else f"{c['H']*100:g}"
 lines.append('|'+c['name']+'|'+c['role']+f"|{c['BTC_capital_usdt']}/{c['capital_usdt']}|{h}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"6个新父候选{len(rep['summary']['passed'])}通过、{len(rep['summary']['candidate_rejected'])}淘汰；两个原生动量组件状态{[(c['name'],c['status'],c['failed_criteria']) for c in comp]}；4个持有控制单列。全部配置失败判据{ {c['name']:c['failed_criteria'] for c in rep['configs'].values()} }。所有正/负收益、逐折/逐变体及控制结果保存并finish，不择优隐藏失败。",'',
'10份CSV保留36新成本场景、逐月/近期折/每日NAV、9格点、9旧父场景、36相邻边、27同资金hold/cash比较、18旧原生成本来源与12资金分配说明。每场景545013完整NAV点SHA、原生逐笔/资金费/状态段及新父源哈希保留。独立审计用Fraction信号和Decimal账务核对实际q/LOT、成本、fund、抵押、闭合小时风险、完整净值和整体/逐折DD，不调用策略simulate/decide/trade重跑。','',
'全网格正Sharpe比例、最高点/边界、多个指标和描述性相邻悬崖均披露；旧点仅增加当前邻域诊断，原canonical status/criteria/sensitivity不重写。描述性相邻2std启发式不是统计显著性，正收益回测不能称稳定实盘盈利。','',
'冻结延迟观察分别续接：原SMA65、原singleS28从Nov1 UTC08:30至10:30；独立未过滤L4/H2从10:10至12:10，仅在12:11参考分钟闭合后采集。08资金费已记账，不重复；真实cash/q/risk和全NAV前缀不重置。三账户原规则/本金/持仓/成本/终止计划保持，历史资金邻域不替换冻结账户；部分资格rejected保留各自180天计划。延迟shadow不充当十策略实时公开报价成交。','',
'只读网页快照同main排他锁生成，执行登记/监控门禁；生成失败恢复上次有效快照并留档。只汇总已有报告/账户，不新建回测或模拟成交，不改规则/本金/持仓/预算、不部署网页或新增定时器、不下真实订单。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
