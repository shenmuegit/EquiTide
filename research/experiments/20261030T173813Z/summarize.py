"""ThreecompleteN/Msurfaces,all27newresults/3oldcontrols,allcost/fold/NAVexports."""
import csv,itertools,json
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,sha,put,grid_configs,axes,positive_recent,stress_fold_ok,ENTRIES,EXITS
from controls import all_reference_configs,baselines
report=json.loads((R/'report.json').read_text());assert json.loads((R/'verification.json').read_text())['passed'];configs=report['configs'];grid=grid_configs(configs);allc={**all_reference_configs(),**configs};refs=baselines(configs);assert len(allc)==30 and len(grid)==27
cols=['net_return_pct','max_drawdown_pct','sharpe_365','calmar'];cost=[];full=[];recent=[];daily=[];edges=[];comparisons=[]
for c in allc.values():
 for k,z in c['scenes'].items():
  t=z['recent40'];cost.append({'name':c['name'],'scope':c['scope'],'asset':c['asset'],'role':c['role'],'entry_vote_threshold':c['entry_vote_threshold'],'retention_vote_threshold':c['retention_vote_threshold'],'capital_usdt':c['capital_usdt'],'old_readonly':bool(c.get('read_only_reference')),'original_or_actual_registry_status':c['status'],'cost_multiplier':int(k),**{f:z[f] for f in cols},'recent_return_pct':t['net_return_pct'],'recent_DD_pct':t['max_drawdown_pct'],'recent_positive_folds':sum(f['net_return_pct']>0 for f in t['folds']),'positive_complete30d_folds':sum(f['net_return_pct']>0 for f in z['folds'][:12]),'executions':z['executions'],'round_trips':z['round_trips'],'cost_usdt':z['cost_usdt'],'cost_pct_initial':z['cost_pct_initial'],'funding_usdt':z['funding_usdt'],'gross_plus_funding_to_cost':z['gross_reference_PnL_to_execution_cost'],'NAV_sha256_f64le':z['NAV_sha256_f64le']})
  for dest,folds in [(full,z['folds']),(recent,t['folds'])]:
   for f in folds:dest.append({'name':c['name'],'cost_multiplier':int(k),'fold':f['fold'],'duration_days':f['duration_days'],'start_utc':f['start_utc'],'end_exclusive_utc':f['end_exclusive_utc'],**{a:f[a] for a in cols}})
  if c['name'] in configs:
   for i,v in enumerate(z['daily_equity_usdt']):daily.append({'name':c['name'],'cost_multiplier':int(k),'day_boundary_index':i,'NAV_usdt':v})
for c in grid.values():
 for typ,b in refs[c['name']].items():
  for k in ['1','2','3']:
   a,z=c['scenes'][k],b['scenes'][k];ta,tb=a['recent40'],z['recent40'];comparisons.append({'name':c['name'],'reference_type':typ,'reference_name':b['name'],'cost_multiplier':int(k),'return_pct':a['net_return_pct'],'reference_return_pct':z['net_return_pct'],'delta_return_pp':a['net_return_pct']-z['net_return_pct'],'DD_pct':a['max_drawdown_pct'],'reference_DD_pct':z['max_drawdown_pct'],'recent_return_pct':ta['net_return_pct'],'reference_recent_return_pct':tb['net_return_pct'],'recent_delta_pp':ta['net_return_pct']-tb['net_return_pct'],'positive_recent_folds':sum(f['net_return_pct']>0 for f in ta['folds']),'reference_positive_recent_folds':sum(f['net_return_pct']>0 for f in tb['folds'])})
figures=[];cliffs=[];groups={}
for asset in ['BTC','ETH','COMBO']:
 sub={(c['entry_vote_threshold'],c['retention_vote_threshold']):c for c in grid.values() if c['asset']==asset};assert len(sub)==9;ax=axes(next(iter(sub.values())))
 for c in sub.values():
  pt=[c[k] for k in ax]
  for j,(key,vals) in enumerate(ax.items()):
   i=vals.index(pt[j])
   if i+1==len(vals):continue
   nxt=pt.copy();nxt[j]=vals[i+1];b=sub[tuple(nxt)];a0,b0=c['scenes']['3'],b['scenes']['3'];edges.append({'scope':c['scope'],'asset':asset,'axis':key,'left':c['name'],'right':b['name'],'full_return_delta_pp':b0['net_return_pct']-a0['net_return_pct'],'DD_delta_pp':b0['max_drawdown_pct']-a0['max_drawdown_pct'],'Sharpe_delta':None if a0['sharpe_365'] is None or b0['sharpe_365'] is None else b0['sharpe_365']-a0['sharpe_365'],'Calmar_delta':None if a0['calmar'] is None or b0['calmar'] is None else b0['calmar']-a0['calmar'],'recent_return_delta_pp':b0['recent40']['net_return_pct']-a0['recent40']['net_return_pct'],'left_min_positive_recent_folds':min(positive_recent(c,k) for k in ['1','2','3']),'right_min_positive_recent_folds':min(positive_recent(b,k) for k in ['1','2','3'])})
 fig,axs=plt.subplots(2,3,figsize=(17,9));items=[('3x full net %',lambda c:c['scenes']['3']['net_return_pct']),('3x continuous max DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe',lambda c:c['scenes']['3']['sharpe_365']),('3x Calmar',lambda c:c['scenes']['3']['calmar']),('3x recent40 net %',lambda c:c['scenes']['3']['recent40']['net_return_pct']),('Minimum positive5d folds 1/2/3x',lambda c:min(positive_recent(c,k) for k in ['1','2','3']))]
 for plot,(title,fn) in zip(axs.flat,items):
  v=np.array([[fn(sub[N,M]) for M in EXITS] for N in ENTRIES],dtype=float);im=plot.imshow(v,aspect='auto',cmap='viridis');plot.set_xticks(range(3),EXITS);plot.set_yticks(range(3),ENTRIES);plot.set_xlabel('Retention votes H of nine');plot.set_ylabel('Entry votes E of nine');plot.set_title(title);fig.colorbar(im,ax=plot)
  for j,i in itertools.product(range(3),range(3)):plot.text(i,j,f'{v[j,i]:.2f}',ha='center',va='center',color='white',fontsize=11)
 fig.suptitle(asset+': nine prior-close channels; entry/retention vote hysteresis; repeated development history');fig.tight_layout();p=R/f'sensitivity_{asset}.png';fig.savefig(p,dpi=125);plt.close(fig);figures.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'panels':6})
 for key in ax:
  es=[x for x in edges if x['asset']==asset and x['axis']==key];ds=[x['Sharpe_delta'] for x in es if x['Sharpe_delta'] is not None];sd=float(np.std(ds)) if ds else 0;cliffs.extend({**x,'difference_std':sd,'flag_abs_delta_gt2std':abs(x['Sharpe_delta'])>2*sd} for x in es if x['Sharpe_delta'] is not None)
 best=max(sub.values(),key=lambda c:c['scenes']['3']['net_return_pct']);groups[asset]={'candidate_cells':9,'passed':sum(c['status']=='passed' for c in sub.values()),'rejected':sum(c['status']=='rejected' for c in sub.values()),'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in sub.values()) for k in ['1','2','3']},'strict_individual_costfold_passes':sum(stress_fold_ok(c) for c in sub.values()),'failed_criterion_counts':dict(Counter(k for c in sub.values() for k in c['failed_criteria'])),'observed_max_return_cell':best['name'],'max_return_at_grid_edge':best['entry_vote_threshold'] in [5,7] or best['retention_vote_threshold'] in [2,4]}
assert [len(x) for x in [cost,full,recent,daily,edges,comparisons]]==[90,1170,720,30051,36,81];exports={}
for name,rows in [('cost_results',cost),('walk_forward_folds',full),('recent40_folds',recent),('daily_NAV',daily),('sensitivity_edges',edges),('reference_comparisons',comparisons)]:
 p=R/(name+'.csv')
 with p.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 exports[name]={'path':str(p.relative_to(ROOT)),'rows':len(rows),'sha256':sha(p)}
summary={'report_sha256':sha(R/'report.json'),'exports':exports,'figures':figures,'candidate_grid_cells':27,'cells_per_scope':9,'new_candidates':27,'reference_configs':0,'read_only_controls':3,'old_unique_references':21,'edges':36,'candidate_status_counts':dict(Counter(c['status'] for c in grid.values())),'groups':groups,'failed_criterion_counts':dict(Counter(k for c in grid.values() for k in c['failed_criteria'])),'cliff_diagnostics':cliffs,'global_optimum_not_claimed':True};put(R/'sensitivity_summary.json',summary)
centers={}
for a in ['BTC','ETH','COMBO']:
 c=next(c for c in grid.values() if c['asset']==a and c['entry_vote_threshold']==6 and c['retention_vote_threshold']==3);centers[a]={'name':c['name'],'fingerprint':c['fingerprint'],'status':c['status'],'return3_pct':c['scenes']['3']['net_return_pct'],'whole_DD3_pct':c['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':c['scenes']['3']['recent40']['net_return_pct'],'positive_recent_folds_by_cost':{k:positive_recent(c,k) for k in ['1','2','3']},'sensitivity':c['sensitivity'],'failed_criteria':c['failed_criteria'],'independent_future_qualified':False,'selection':'PrespecifiedE6/H3,notbestPnL.'}
put(R/'representative.json',{'centers':centers,'raw_parent_weights':[1,1],'bank_capitals_usdt':[10000,10000],'fixed_entry_notionals_usdt':[1000,2000]});put(R/'qualification_fragility.json',{'report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'rows':[{'name':c['name'],'asset':c['asset'],'fingerprint':c['fingerprint'],'status':c['status'],'entry_vote_threshold':c['entry_vote_threshold'],'retention_vote_threshold':c['retention_vote_threshold'],'positive_recent_folds_by_cost':{k:positive_recent(c,k) for k in ['1','2','3']},'minimum_positive_recent_fold_pct_by_cost':{k:min((f['net_return_pct'] for f in c['scenes'][k]['recent40']['folds'] if f['net_return_pct']>0),default=None) for k in ['1','2','3']},'local_strict_fraction':c['sensitivity']['local_recent6of8_allcost_fraction']} for c in grid.values()]})
from write_result import main as write_result
write_result()
