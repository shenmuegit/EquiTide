"""All actualscale costs/folds/NAVs and matchedindexcomparisons after independentaudit."""
import csv,itertools,json
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,sha,put,grid_configs,axes,positive_recent,stress_fold_ok,WEIGHTS,CAPS
from controls import old_ownership,matched
report=json.loads((R/'report.json').read_text());assert json.loads((R/'verification.json').read_text())['passed'];configs=report['configs'];grid=grid_configs(configs);own,ungated,holds=matched(configs);allc={**configs,**{c['name']:c for c in old_ownership().values()}};assert len(allc)==45
cols=['net_return_pct','max_drawdown_pct','sharpe_365','calmar'];cost=[];full=[];recent=[];daily=[];comparisons=[];edges=[]
for c in allc.values():
 for k,z in c['scenes'].items():
  t=z['recent40'];cost.append({'name':c['name'],'scope':c['scope'],'asset':c['asset'],'role':c['role'],'mode':c['mode'],'BTC_capital_fraction':c['BTC_capital_fraction'],'capital_usdt':c['capital_usdt'],'old_readonly':bool(c.get('read_only_anchor')),'status':c['status'],'cost_multiplier':int(k),**{f:z[f] for f in cols},'recent_return_pct':t['net_return_pct'],'recent_DD_pct':t['max_drawdown_pct'],'recent_positive_folds':sum(f['net_return_pct']>0 for f in t['folds']),'positive_complete30d_folds':sum(f['net_return_pct']>0 for f in z['folds'][:12]),'executions':z['executions'],'round_trips':z['round_trips'],'cost_usdt':z['cost_usdt'],'cost_pct_initial':z['cost_pct_initial'],'funding_usdt':z['funding_usdt'],'gross_plus_funding_to_cost':z['gross_reference_PnL_to_execution_cost'],'NAV_sha256_f64le':z['NAV_sha256_f64le']})
  for dest,folds in [(full,z['folds']),(recent,t['folds'])]:
   for f in folds:dest.append({'name':c['name'],'cost_multiplier':int(k),'fold':f['fold'],'duration_days':f['duration_days'],'start_utc':f['start_utc'],'end_exclusive_utc':f['end_exclusive_utc'],**{a:f[a] for a in cols}})
  if c['name'] in configs:
   for i,v in enumerate(z['daily_equity_usdt']):daily.append({'name':c['name'],'cost_multiplier':int(k),'day_boundary_index':i,'NAV_usdt':v})
for c in grid.values():
 w=c['BTC_capital_fraction'];refs=[('matched_actualscale_ungated',ungated[c['scope'],w]),('matched_actualscale_constantlong',holds[c['scope'],c['asset'],w])]
 if c['scope']=='parent':refs.append(('matched_original10kbank_ownership',own[w,c['entry_funding_cost_cap_per_settlement']]))
 for typ,ref in refs:
  for k in ['1','2','3']:
   a,b=c['scenes'][k],ref['scenes'][k];ta,tb=a['recent40'],b['recent40'];comparisons.append({'name':c['name'],'reference_type':typ,'reference_name':ref['name'],'cost_multiplier':int(k),'return_pct':a['net_return_pct'],'reference_return_pct':b['net_return_pct'],'delta_return_pp':a['net_return_pct']-b['net_return_pct'],'DD_pct':a['max_drawdown_pct'],'reference_DD_pct':b['max_drawdown_pct'],'recent_return_pct':ta['net_return_pct'],'reference_recent_return_pct':tb['net_return_pct'],'recent_delta_pp':ta['net_return_pct']-tb['net_return_pct'],'positive_recent_folds':sum(f['net_return_pct']>0 for f in ta['folds']),'reference_positive_recent_folds':sum(f['net_return_pct']>0 for f in tb['folds'])})
for scope in ['native','parent']:
 sub={n:c for n,c in grid.items() if c['scope']==scope};ax=axes(next(iter(sub.values())));index={tuple(c[k] for k in ax):c for c in sub.values()}
 for c in sub.values():
  pt=[c[k] for k in ax]
  for j,(key,vals) in enumerate(ax.items()):
   i=vals.index(pt[j])
   if i+1==len(vals):continue
   nxt=pt.copy();nxt[j]=vals[i+1];b=index[tuple(nxt)];a0,b0=c['scenes']['3'],b['scenes']['3'];edges.append({'scope':scope,'axis':key,'left':c['name'],'right':b['name'],'full_return_delta_pp':b0['net_return_pct']-a0['net_return_pct'],'DD_delta_pp':b0['max_drawdown_pct']-a0['max_drawdown_pct'],'Sharpe_delta':None if a0['sharpe_365'] is None or b0['sharpe_365'] is None else b0['sharpe_365']-a0['sharpe_365'],'Calmar_delta':None if a0['calmar'] is None or b0['calmar'] is None else b0['calmar']-a0['calmar'],'recent_return_delta_pp':b0['recent40']['net_return_pct']-a0['recent40']['net_return_pct'],'left_min_positive_recent_folds':min(positive_recent(c,k) for k in ['1','2','3']),'right_min_positive_recent_folds':min(positive_recent(b,k) for k in ['1','2','3'])})
assert [len(x) for x in [cost,full,recent,daily,edges,comparisons]]==[135,1755,1080,46746,24,135];exports={}
for name,rows in [('cost_results',cost),('walk_forward_folds',full),('recent40_folds',recent),('daily_NAV',daily),('sensitivity_edges',edges),('reference_comparisons',comparisons)]:
 path=R/(name+'.csv')
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 exports[name]={'path':str(path.relative_to(ROOT)),'rows':len(rows),'sha256':sha(path)}
frag={'report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'rows':[]}
for c in grid.values():frag['rows'].append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'status':c['status'],'BTC_capital_fraction':c['BTC_capital_fraction'],'cap':c['entry_funding_cost_cap_per_settlement'],'positive_recent_folds_by_cost':{k:positive_recent(c,k) for k in ['1','2','3']},'minimum_positive_recent_fold_pct_by_cost':{k:min((f['net_return_pct'] for f in c['scenes'][k]['recent40']['folds'] if f['net_return_pct']>0),default=None) for k in ['1','2','3']},'local_recent6of8_allcost_fraction':c['sensitivity']['local_recent6of8_allcost_fraction'],'independent_future_qualified':False})
put(R/'qualification_fragility.json',frag);figures=[];items=[('3x full net %',lambda c:c['scenes']['3']['net_return_pct']),('3x continuous max DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe',lambda c:c['scenes']['3']['sharpe_365']),('3x Calmar',lambda c:c['scenes']['3']['calmar']),('3x recent40 net %',lambda c:c['scenes']['3']['recent40']['net_return_pct']),('Minimum positive5d folds 1/2/3x',lambda c:min(positive_recent(c,k) for k in ['1','2','3']))]
for scope in ['native','parent']:
 sub={(c['BTC_capital_fraction'],c['entry_funding_cost_cap_per_settlement']):c for c in grid.values() if c['scope']==scope};fig,axs=plt.subplots(2,3,figsize=(17,9))
 for ax,(title,fn) in zip(axs.flat,items):
  a=np.array([[fn(sub[w,c]) for c in CAPS] for w in WEIGHTS],dtype=float);im=ax.imshow(a,aspect='auto',cmap='viridis');ax.set_xticks(range(3),[str(c*10000) for c in CAPS]);ax.set_yticks(range(3),[str(w*100) for w in WEIGHTS]);ax.set_xlabel('ETH directional funding cost cap (bp/settlement)');ax.set_ylabel('Actual initial BTC capital % of20000');ax.set_title(title);fig.colorbar(im,ax=ax)
  for j,i in itertools.product(range(3),range(3)):ax.text(i,j,f'{a[j,i]:.2f}',ha='center',va='center',color='white',fontsize=11)
 fig.suptitle(f'{scope}: actualcapital/nativeorders; N6fundhistory; repeated development history');fig.tight_layout();path=R/f'sensitivity_{scope}.png';fig.savefig(path,dpi=125);plt.close(fig);figures.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),'panels':6})
cliffs=[]
for scope,key in itertools.product(['native','parent'],list(axes(next(iter(grid.values()))))):
 es=[x for x in edges if x['scope']==scope and x['axis']==key];ds=[float(x['Sharpe_delta']) for x in es if x['Sharpe_delta'] is not None];sd=float(np.std(ds)) if ds else 0.;cliffs.extend({**x,'difference_std':sd,'flag_abs_delta_gt2std':abs(x['Sharpe_delta'])>2*sd} for x in es if x['Sharpe_delta'] is not None)
summary={'report_sha256':sha(R/'report.json'),'exports':exports,'figures':figures,'candidate_grid_cells':18,'edges':24,'candidate_status_counts':dict(Counter(c['status'] for c in grid.values())),'reference_configs':24,'failed_criterion_counts':dict(Counter(k for c in grid.values() for k in c['failed_criteria'])),'strict_individual_costfold_passes':sum(stress_fold_ok(c) for c in grid.values()),'positive_3x_Sharpe_fraction_by_scope':{s:sum(c['scenes']['3']['sharpe_365'] is not None and c['scenes']['3']['sharpe_365']>0 for c in grid.values() if c['scope']==s)/9 for s in ['native','parent']},'cliff_diagnostics':cliffs};put(R/'sensitivity_summary.json',summary)
center=next(c for c in grid.values() if c['scope']=='parent' and c['BTC_capital_fraction']==.25 and c['entry_funding_cost_cap_per_settlement']==.00005);put(R/'representative.json',{'name':center['name'],'fingerprint':center['fingerprint'],'status':center['status'],'scope':'parent','actual_component_capitals_usdt':[5000,15000],'actual_component_entry_notionals_usdt':[500,4500],'raw_bank_multipliers':[1,1],'entry_funding_lookback_settlements':6,'cap':.00005,'return3_pct':center['scenes']['3']['net_return_pct'],'whole_DD3_pct':center['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':center['scenes']['3']['recent40']['net_return_pct'],'positive_recent_folds_by_cost':{k:positive_recent(center,k) for k in ['1','2','3']},'sensitivity':center['sensitivity'],'failed_criteria':center['failed_criteria'],'independent_future_qualified':False,'selection':'Preset geometric grid center,presentation only,not maximumreturn selection'})
with (R/'result.md').open('w') as f:
 f.write('# BTC/ETH 真正原生分仓本金与资金费过滤回测\n\n42新配置/126成本场景：21实际新规模原生银行、15真实分仓父组合、6复用旧10k银行的所有权对照。18候选含ETH与父组合各9格，另24固定执行组件或参考仅作对照、未作单独alpha资格。\n\n本金20000，BTC初始份额18.75/25/31.25%明确对应3750/5000/6250，ETH16250/15000/13750；BTC固定新仓N375/500/625，ETH4875/4500/4125，各自为本金10%/30%。每银行独立现金与lot/tick/冲击/资金费/抵押真实重算，父净值用原值[1,1]相加，不能再乘本金份额。旧规模对照原值[2w,2(1−w)]保留，中心[0.5,1.5]三项旧结果只读，外侧6项新组合先reserve。没有自动归一化、调仓、共享保证金或按净值复利变更数量。\n\n固定BTC动量ROC31/H4/E1与ETH反转L3/H2.5/E−1/S28多数慢门控；ETH资金费N6固定，上限0/0.5/1bp与本金份额双轴预设。特征1212条完整历史按available_ts和settlement_ts均≤信号时刻筛选，OOS1110条仅作真实入账；已有兼容仓位不因资金费门控强平。\n\n370日连续OOS、12×30日+10尾日，33上下文含3天初始embargo，近期40日继承day330状态/8×5日。开发历史已反复研究，不是未触碰留出。逐折与完整连续NAV整体回撤、Sharpe/Calmar、1/2/3倍费用/价差/滑点/成交额冲击/资金费/lot/tick/抵押与闭合小时风险已完成。\n\n')
 f.write('18候选历史通过'+str(len(report['summary']['passed']))+'，淘汰'+str(len(report['summary']['rejected']))+'。参考与固定BTC执行组件24项均真实回测并按reference-only登记rejected，不表示其收益一定为负；BTC只改变所需规模，未声称其单独具备二维参数alpha。候选失败计数：`'+json.dumps(summary['failed_criterion_counts'],ensure_ascii=False)+'`。\n\n|配置|状态|3倍净收益%|整体DD%|近期净收益%|1/2/3倍正五日折|局部严格比例|\n|---|---|---:|---:|---:|---|---:|\n')
 for c in grid.values():f.write('|'+c['name']+'|'+c['status']+'|'+f"{c['scenes']['3']['net_return_pct']:.6f}|{c['scenes']['3']['max_drawdown_pct']:.6f}|{c['scenes']['3']['recent40']['net_return_pct']:.6f}|"+'/'.join(str(positive_recent(c,k)) for k in ['1','2','3'])+'|'+f"{c['sensitivity']['local_recent6of8_allcost_fraction']:.6f}"+'|\n')
 f.write('\n预设严格门槛不变：每成本全期/近期净正、月折9/12、近期正五日折各6/8、局部达到严格正折的比例≥60%、3倍整体DD≤25%、至少4往返、成本安全边际≥2.5、无拒单/负现金/风险代理违规并终止平仓。实际scale与同scale无过滤/持有及旧所有权的逐成本比较见reference_comparisons；现金0%仅定义上比较，无新现金模拟。\n\n局限：新金额的成交模型现在被实测，但估计价差/滑点/ADV冲击与normalized历史过滤器、1%闭合小时保证金代理没有L2/TCA/全历史保证金档位/逐tick清算支持，不能称真实交易所容量或稳定实盘盈利。尚无独立未来资格，不改原冻结账户。\n\n来源：[Binance官方交易所信息API](https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information)、[资金费机制](https://www.binance.com/en/support/faq/detail/360033525031)；本轮实际打开，但API目录未完整显示历史lot/filter细节，研究使用原始已哈希metadata，不宣称官方验证了历史全过滤器或收益。本金/量化冲击试验为研究推断。\n')
print(json.dumps({k:v for k,v in summary.items() if k!='cliff_diagnostics'},ensure_ascii=False),flush=True)
