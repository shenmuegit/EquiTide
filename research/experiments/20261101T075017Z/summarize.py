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
 ax=axs[j];im=ax.imshow(arr,cmap='RdYlGn_r' if j==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if j==3 else {}));ax.set_xticks(range(3),['2%','2.5%','3%']);ax.set_yticks(range(3),[f'{C} / {100*C/(C+15000):.2f}%' for C in p['BTC_capitals']]);ax.set_xlabel('ETH fast entry hurdle H');ax.set_ylabel('BTC actual bank / share of total');ax.set_title(label)
 for g in p['grid']:
  i,k=p['BTC_capitals'].index(g['BTC_capital_usdt']),p['fast_hurdles'].index(g['H']);ax.text(k,i,f'{arr[i,k]:.3f}'+(' O' if g['readonly'] else ' N'),ha='center',va='center',fontsize=9)
 fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('Actual BTC bank3750/5000/6250 at native N375/500/625 | fixed ETH15000/N4500\nETH L4/S28, E0.25%, V10/cap4.5% | raw child multipliers [1,1], no NAV scaling | O=readonly, N=new | reused development history')
fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(rep['summary']['passed']),'rejected':len(rep['summary']['candidate_rejected']),'failed_criteria':dict(collections.Counter(x for c in rep['configs'].values() for x in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
ctx=json.loads((R/'context.json').read_text())
lines=['# BTC原生银行边界邻域与ETH门槛联合检验','',f"预先固定BTC实际银行3750/5000/6250×ETH H2/2.5/3%，固定ETH15000/N4500、L4/S28/E0.25%、V10样本logvol cap4.5%。6新候选组合＋2新匹配持有父，共8定义／24成本场景，逐项reserve后计算；3中心旧候选与1旧匹配持有父只读，10原生资金／数量路径完整复用，不做新组件策略回测。完整读取{ctx['registry_events']}登记事件／{ctx['registry_ids']}ID、{len(ctx['prior_conclusions_read'])}份既往结论，初始16项均有真实原始证据；规范化研究定义{ctx['canonical_research_definitions_excluding_observations']}不等于全部有金融结果。",'',
'假设：上轮BTC5000银行位于资金轴最佳Sharpe边界，更大BTC资金未通过近期成本门槛。本轮将原银行从3750/5000/6250两侧夹住，检验附近支持，而非以当前结果择优。旧中心保留原canonical资格；每个新候选和基准具体配置独立登记，基准已实际计算但不是可选策略候选。','',
'原始子权重[1,1]保留，表示一份完整BTC银行和一份ETH15000银行，不对净值重复乘资本份额。总C0=18750/20000/21250，BTC初始资金份额20%/25%/29.4118%，BTC真实N375/500/625、ETHN4500；实际总初始N/C0约26%/25%/24.1176%。复用各自真正LOT/tick／规模冲击／现金／资金费路径，不线性放大或同步复制同币订单。每组合各一份BTC、ETH账户，无转账、免费调仓、NAVresize、交叉抵押或现金收益，资本不同不代表同风险。','',
'BTC原ROC31/H4/E1；ETH严格priorfastROC>H空、<−H多，带内实际多仅r<E／空仅r>−E保留、等号退出；S28方向始终门控，V10/cap4.5%仅过滤新入场／翻向，不拦退出或同向q。原生q=floor(N/prior完整close/LOT)×LOT，下一UTC00:01OPEN不利tick，反向先平后开，370日终止计费平仓。','',
'时序验证：真实2025-10-19 UTC00:01至2026-10-24 UTC00:01连续370日、12完整30日折＋10日尾折，状态／成本／funding跨折不重置；近期40日继承day330、8×5日折。固定规则无拟合／标签，purge0、预热30日／间隔3日；所有信号只用prior完整close，成本仅past20完整日quoteADV／logvol。此历史被反复研究，仅开发验证，不称未触碰最终留出、DSR/PBO或成熟独立未来证据。','',
'成本1/2/3倍：每边5bp费用＋1bp半价差＋2bp滑点＋0.5×past20logvol×sqrt(actualq×OPEN/past20quoteADV)，真实settlement纳秒/rate/mark/当时q，支出加压而正资金费不放大。原生LOT/tick/minnotional、参与率<=.001、费用后1倍入场抵押、各银行独立1%闭合小时不利mark维护代理。线性永续无需现货借币，不虚构借币费；无L2/TCA、完整历史档位／逐tick清算或真实容量证明。匹配持有为同银行和初始N的常多参考，非满仓买持或同风险基准，现金0%另列。','',
'候选门槛在见结果前固定：全年每档净正，1x>=9/12正完整月折；近期每档净正且>=6/8正5日折；3x完整DD<=25%；银行/H索引半径1含自身的局部3x净正和严格近期比例各>=60%；至少4平仓，毛价差PnL+fund/执行成本>=2.5；零拒单／负抵押／维护代理违规、终止flat、至少180日。基准role明确不作为策略候选，其实际正负结果／所有fold仍保存。','',
'|新配置|角色|BTC银行/总C0|H%|1x净%|2x净%|3x净%|3x完整DD%|正月/12|近期正折1/2/3x|结论|','|---|---|---|---:|---:|---:|---:|---:|---:|---|---|']
for c in rep['configs'].values():
 h='—' if c['H'] is None else f"{c['H']*100:g}"
 lines.append('|'+c['name']+'|'+c['role']+f"|{c['BTC_capital_usdt']}/{c['capital_usdt']}|{h}|"+'|'.join(f"{c['scenes'][k]['net_return_pct']:.6f}" for k in ['1','2','3'])+f"|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['positive_complete_30d_folds_1x']}|"+'/'.join(str(c['recent40_positive_5d_folds_by_cost'][k]) for k in ['1','2','3'])+'|'+c['status']+'|')
lines+=['',f"6新候选实际{summary['passed']}通过／{summary['rejected']}淘汰；2匹配基准单独按benchmark结果finish留档，不计候选通过数。失败判据{summary['failed_criteria']}。全部正／负收益、逐fold和场景保留；历史通过不代表稳定实盘盈利。",'',
'完整净值按两实际银行美元相加，不平均Sharpe/收益率。10CSV保存全部24新成本场景、完整月折／近期折／日NAV、9格点／边界／相邻边、同资金hold/cash比较、30原生来源场景和12资金分配说明。每场景545013完整NAV点SHA及原生逐笔／状态段归档保留，独立核验原始q/LOT/lag/费/冲击/fund/cash/小时风险和新父完整指标，不调用策略simulate/target/trade重跑组件。','',
'三份冻结账户原规则／资金／持仓／费用／全NAV前缀保持：原SMA65和singleS28从Nov1UTC04:30续至06:30；独立未过滤L4/H2从06:10续至08:10，该窗跨08资金费，必须在08:11参考分钟闭合后采集，并以真实精确纳秒/rate/mark/当时q入账一次。历史银行邻域不替换冻结账户，不重开现金／未来计划，不强制本轮平仓；部分rejected保留各自180日计划。延迟shadow不充当十策略真实公开报价执行。','',
'按冻结门槛同时披露全格点正Sharpe比例、边界及描述性悬崖／回撤，不以全年净正替代近期一致性；旧点仅增加本轮诊断，不重写原status/criteria/sensitivity。数据／代码SHA、真实命令退出码、原始响应和所有失败完整留档。只读监控同main排他锁生成核验；生成失败恢复旧有效汇总，不删历史或负收益，不改账户／规则，不重部署或新建定时器，不下真实订单。']
(R/'result.md').write_text('\n'.join(lines)+'\n');print(json.dumps(summary),flush=True)
