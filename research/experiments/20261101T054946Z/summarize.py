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
 C=g['BTC_capital_usdt'];alloc.append([g['fingerprint'],'readonly_matched_budget_hold',C,15000,C+15000,C/10,4500,1,1,C/(C+15000),15000/(C+15000),None,True])
for k in ['1','2','3']:
 for g in p['grid']:
  i,j=p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H']);ng=[h for h in p['grid'] if i<2 and h['BTC_capital_usdt']==p['BTC_capitals'][i+1] and h['H']==g['H'] or j<2 and h['H']==p['fast_hurdles'][j+1] and h['BTC_capital_usdt']==g['BTC_capital_usdt']]
  for h in ng:
   a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([k,g['BTC_capital_usdt'],g['H'],h['BTC_capital_usdt'],h['H'],g['fingerprint'],h['fingerprint'],abs(a['sharpe_365']-b['sharpe_365']),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
for fp,x in p['read_only_references'].items():
 if x['scope']!='native':continue
 sp=json.loads((ROOT/x['spec']).read_text());old=next(c for c in json.loads((ROOT/x['report']).read_text())['configs'].values() if c['fingerprint']==fp)
 for k,s in old['scenes'].items():sources.append([fp,x['asset'],x['capital_usdt'],sp['parameters']['fixed_entry_notional_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],x['report'],x['report_sha256']])
write('cost_scenes.csv',['configuration','fingerprint','BTC_bank','ETH_H','total_capital','BTC_capital_share','cost_multiplier','net_return_pct','whole_OOS_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','underlying_executions','underlying_closes','recent40_return_pct','positive5d_folds','status'],cost)
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
 ax=axs[j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['2%','2.5%','3%']);ax.set_yticks(range(3),['5000 / 25%','10000 / 40%','15000 / 50%']);ax.set_xlabel('ETH fast entry hurdle H');ax.set_ylabel('BTC actual bank / share of total');ax.set_title(label)
 for g in p['grid']:
  i,k=p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
 fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('Actual BTC bank5000/10000/15000 at native N500/1000/1500 | fixed ETH15000/N4500\nETH L4/S28, E0.25%, V10/cap4.5% | raw child multipliers [1,1], no NAV scaling | O=readonly, N=new | reused development history')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(x for c in rep['configs'].values() for x in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text())
lines=['# 真实银行规模与ETH入场门槛组合验证','',f"预定BTC银行5000/10000/15000 USDT×ETH入场H2/2.5/3%，固定ETH15000/N4500、L4/S28/E0.25%、V10样本log波动cap4.5%。9点网格中3旧点只读，6新组合／18成本场景全部先reserve再计算；10原生组件和3匹配银行／预算持有基准均有真实结果，只读复用，0原生策略或基准重跑。原始组件权重[1,1]表示一份完整BTC银行与一份完整ETH银行；总资金20000/25000/30000，初始BTC份额25%/40%/50%，不对小银行净值线性放大。各银行实际N500/1000/1500和ETH4500的LOT/tick/费／规模冲击／资金费已经原生核算。",'',f"完整读取{ctx['registry_events']}事件、{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论。初始16项均有真实原始证据；规范化研究定义{ctx['canonical_research_definitions_excluding_observations']}含无结果状态，不称全部回测完成。登记前family标签与已有基准计数错误均保留源和失败回执，未导致金融计算或重复登记；仅计数／格式修正，6候选规则不变。",'',
'经济假设：上轮提高ETH入场门槛虽少执行而近期稳定性下降，本轮检验更多实际BTC资金份额能否扩大近期支持。ETH严格fastROC>H空、<−H多；带内实际多仅r<E、空仅r>−E保留，等号退出。S28慢方向门控始终应用，V10/cap4.5%仅过滤新／反向入场，不拦退出或同向q。BTC原ROC31/H4/E1，全部规则／邻域在本轮见结果前固定。','',
'连续370日：2025-10-19 UTC00:01至2026-10-24 UTC00:01，12完整30日折＋10日尾折，资金/q/entry/费用/funding跨折不重置；近期40日继承day330真实状态、8×5日折。只取prior完整close，次UTC00:01原生OPEN不利tick，q=floor(N/priorclose/LOT)×LOT，终止计费平仓。新父组合没有额外调仓、转账或交叉抵押；每父仅一份BTC、一份ETH，避免同步复制同币订单低估冲击。','',
'成本：每边5bp费＋1bp半价差＋2bp滑点＋0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)，1/2/3倍压力；实际settlement纳秒/mark/rate/当时q，支出加压而正收入不放大。原生LOT/tick/minnotional、参与率<=.001、费用后1倍入场抵押、各银行独立1%闭合小时不利mark维护代理。永续不需要现货借币，不虚构借币费；缺L2/TCA、历史档位／逐tick清算／真实容量证明。基准为匹配银行和初始N的常多参考，非满仓买持或同风险比较，现金0%另列。','',
'预冻结门槛：全年每档净正、1x>=9/12正完整月折；近期每档净正且>=6/8正5日折；3x完整DD<=25%；银行规模/H索引半径1含自身的局部3x净正和严格近期比例各>=60%；至少4平仓、毛价差PnL+fund/执行成本>=2.5；零拒单／负抵押／维护代理违规、终止flat、至少180日。旧点保留原status/criteria/sensitivity，仅追加当前网格诊断，不放宽门槛。','',
'|新配置|BTC银行/总资金|H%|1x净%|2x净%|3x净%|3x完整DD%|正月/12|近期正折1/2/3x|结论|','|---|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in rep['configs'].values():lines.append('|'+c['name']+f"|{c['BTC_capital_usdt']}/{c['capital_usdt']}|{c['H']*100:g}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"实际{summary['passed']}通过／{summary['rejected']}淘汰，失败门槛分布{summary['failed_criteria']}。所有正负结果和折保留，通过仅本批历史门槛，不能称稳定实盘盈利。",'',
'10CSV完整列新18成本场景、逐月／近期／日NAV、9格点与边界／相邻边、同资金／N持有和现金对照、30原生来源场景、12份资金分配。每场景545013点NAV SHA与原账本／源SHA保留，无可重建大数组。独立核验原生q/lag、费用／冲击／资金费／cash／小时风险，重算父全NAV与折指标，不调用策略simulate/target/trade。','',
'三份冻结账户保持原规则／资金／仓位／费用和全NAV前缀：原SMA65与singleS28从Nov1UTC02:30续至04:30；独立未过滤L4/H2从04:10续至06:10，仅参考分钟06:11闭合后采集。当前历史银行组合不替换已有账户、不开新未来计划、不重复旧日决策／资金费；部分rejected保留180日计划。延迟shadow不充当十策略真实公开报价执行。','',
'固定组件无拟合／标签，purge0、30日预热与3日间隔；重复历史属于开发验证，无未触碰最终留出、DSR/PBO或成熟独立未来证据。披露全格点Sharpe／Calmar／回撤、边界及描述性悬崖，不以全年净正替代近期稳健。只读监控同main排他锁生成核验；失败恢复上次有效汇总并记录，不删旧行、负收益或改账户／冻结规则。不重部署、不新增定时任务、不下真实订单。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
