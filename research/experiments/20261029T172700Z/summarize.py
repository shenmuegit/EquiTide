"""Read completed report;export every cost/fold/grid/comparison and Chinese results."""
import csv,hashlib,itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,sha,put,grid_configs,axes,positive_recent,stress_fold_ok,WEIGHTS,NEW_WEIGHTS,EXITS,SLOWS
report=json.loads((R/'report.json').read_text());assert json.loads((R/'verification.json').read_text())['passed'];cs=report['configs'];grid=grid_configs(cs);allc={**grid,**{n:c for n,c in cs.items() if c['role']=='benchmark'}};candidates=[c for c in cs.values() if c['role']=='candidate'];bench={c['BTC_bank_units']:c for c in cs.values() if c['role']=='benchmark'}
def export(name,rows):
 assert rows;path=R/(name+'.csv');fields=list(rows[0]);assert all(list(x)==fields for x in rows)
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 return {'path':str(path.relative_to(ROOT)),'rows':len(rows),'sha256':sha(path)}
cols=['net_return_pct','max_drawdown_pct','sharpe_365','calmar']
cost=[];full=[];recent=[];daily=[];comparisons=[]
for c in allc.values():
 for k,s in c['scenes'].items():
  t=s['recent40'];cost.append({'name':c['name'],'role':c['role'],'read_only_old':bool(c.get('read_only_anchor')),'status':c['status'],'cost_multiplier':int(k),**{x:s[x] for x in cols},'recent_return_pct':t['net_return_pct'],'recent_DD_pct':t['max_drawdown_pct'],'recent_positive_folds':positive_recent(c,k),'monthly_positive_folds':sum(f['net_return_pct']>0 for f in s['folds'][:12]),'source_execution_actions':s['executions'],'source_round_trips':s['round_trips'],'cost_usdt':s['cost_usdt'],'cost_pct_initial':s['cost_pct_initial'],'funding_usdt':s['funding_usdt'],'funding_income_usdt':s['funding_income_usdt'],'funding_outflow_usdt':s['funding_outflow_usdt'],'gross_plus_funding_to_cost':s['gross_reference_PnL_to_execution_cost'],'NAV_sha256_f64le':s['NAV_sha256_f64le']})
  for dest,ff in [(full,s['folds']),(recent,t['folds'])]:
   for f in ff:dest.append({'name':c['name'],'cost_multiplier':int(k),'fold':f['fold'],'duration_days':f['duration_days'],'start_utc':f['start_utc'],'end_exclusive_utc':f['end_exclusive_utc'],**{x:f[x] for x in cols}})
  if c['name'] in cs:
   for i,v in enumerate(s['daily_equity_usdt']):daily.append({'name':c['name'],'cost_multiplier':int(k),'day_boundary_index':i,'NAV_usdt':v})
for c in candidates:
 anchor=next(x for x in grid.values() if x.get('read_only_anchor') and x['ETH_exit_buffer_fraction']==c['ETH_exit_buffer_fraction'] and x['ETH_trend_lookback_days']==c['ETH_trend_lookback_days'])
 for typ,ref in [('same_E_S_raw1_1',anchor),('same_raw_units_constant_long',bench[c['BTC_bank_units']])]:
  for k in ['1','2','3']:
   a,b=c['scenes'][k],ref['scenes'][k];comparisons.append({'name':c['name'],'reference_type':typ,'reference_name':ref['name'],'cost_multiplier':int(k),'candidate_return_pct':a['net_return_pct'],'reference_return_pct':b['net_return_pct'],'return_delta_pp':a['net_return_pct']-b['net_return_pct'],'candidate_DD_pct':a['max_drawdown_pct'],'reference_DD_pct':b['max_drawdown_pct'],'candidate_recent_return_pct':a['recent40']['net_return_pct'],'reference_recent_return_pct':b['recent40']['net_return_pct'],'recent_return_delta_pp':a['recent40']['net_return_pct']-b['recent40']['net_return_pct'],'candidate_positive_recent_folds':positive_recent(c,k),'reference_positive_recent_folds':positive_recent(ref,k),'candidate_source_actions':a['executions'],'reference_source_actions':b['executions']})
index={(c['BTC_bank_units'],c['ETH_exit_buffer_fraction'],c['ETH_trend_lookback_days']):c for c in grid.values()};edges=[]
for c in grid.values():
 point=[c['BTC_bank_units'],c['ETH_exit_buffer_fraction'],c['ETH_trend_lookback_days']]
 for j,(axis,vals) in enumerate(axes(c).items()):
  i=vals.index(point[j])
  if i+1==len(vals):continue
  q=point.copy();q[j]=vals[i+1];b=index[tuple(q)];aa,bb=c['scenes']['3'],b['scenes']['3'];edges.append({'axis':axis,'left':c['name'],'right':b['name'],'full_return_delta_pp':bb['net_return_pct']-aa['net_return_pct'],'DD_delta_pp':bb['max_drawdown_pct']-aa['max_drawdown_pct'],'Sharpe_delta':None if aa['sharpe_365'] is None or bb['sharpe_365'] is None else bb['sharpe_365']-aa['sharpe_365'],'Calmar_delta':None if aa['calmar'] is None or bb['calmar'] is None else bb['calmar']-aa['calmar'],'recent_return_delta_pp':bb['recent40']['net_return_pct']-aa['recent40']['net_return_pct'],'left_min_positive_recent_folds':min(positive_recent(c,k) for k in ['1','2','3']),'right_min_positive_recent_folds':min(positive_recent(b,k) for k in ['1','2','3'])})
assert len(grid)==63 and len(cost)==201 and len(full)==2613 and len(recent)==1608 and len(daily)==44520 and len(edges)==138 and len(comparisons)==216
exportinfo={name:export(name,rows) for name,rows in [('cost_results',cost),('walk_forward_folds',full),('recent40_folds',recent),('daily_NAV',daily),('sensitivity_edges',edges),('reference_comparisons',comparisons)]}
frag={'report_sha256':sha(R/'report.json'),'new_financial_evaluations':0,'new_gate':'Every1/2/3xcost musthave at least6of8positive5dayfolds andlocalneighborsmeetingthis>=60percent;predeclaredbeforePnl.','old27qualifications_unchanged':True,'rows':[]}
for c in candidates:
 frag['rows'].append({'name':c['name'],'fingerprint':c['fingerprint'],'status':c['status'],'positive_recent_folds_by_cost':{k:positive_recent(c,k) for k in ['1','2','3']},'minimum_positive_recent_fold_pct_by_cost':{k:min((f['net_return_pct'] for f in c['scenes'][k]['recent40']['folds'] if f['net_return_pct']>0),default=None) for k in ['1','2','3']},'local_recent6of8_allcost_fraction':c['sensitivity']['local_recent6of8_allcost_fraction'],'independent_future_qualified':False})
put(R/'qualification_fragility.json',frag)
figures=[]
for E in EXITS:
 fig,axs=plt.subplots(2,3,figsize=(17,9));items=[('3x full net %',lambda c:c['scenes']['3']['net_return_pct']),('3x continuous NAV max DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe',lambda c:c['scenes']['3']['sharpe_365']),('3x Calmar',lambda c:c['scenes']['3']['calmar']),('3x recent40 net %',lambda c:c['scenes']['3']['recent40']['net_return_pct']),('Minimum positive 5d folds over 1/2/3x',lambda c:min(positive_recent(c,k) for k in ['1','2','3']))]
 for ax,(title,fn) in zip(axs.flat,items):
  a=np.array([[fn(index[w,E,S]) for w in WEIGHTS] for S in SLOWS]);im=ax.imshow(a,aspect='auto',cmap='viridis');ax.set_xticks(range(len(WEIGHTS)),[str(x) for x in WEIGHTS]);ax.set_yticks(range(3),[str(x) for x in SLOWS]);ax.set_xlabel('Raw BTC bank units w; ETH=2-w (old w=.5,.75,1)');ax.set_ylabel('Slow center S');ax.set_title(title,fontsize=11)
  for i,j in itertools.product(range(3),range(len(WEIGHTS))):ax.text(j,i,f'{a[i,j]:.2f}',ha='center',va='center',color='white' if a[i,j]<(a.min()+a.max())/2 else 'black',fontsize=10)
  fig.colorbar(im,ax=ax,shrink=.8)
 fig.suptitle(f'Existing fixed-scale bank ownership | E={E:.3f} | L3 H2.5% | capital20000 | no normalization',fontsize=14);fig.tight_layout();path=R/f'sensitivity_E{round(E*10000)}.png';fig.savefig(path,dpi=125);plt.close(fig);figures.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),'panels':6})
failed=Counter(x for c in candidates for x in c['failed_criteria']);best=max(candidates,key=lambda c:c['scenes']['3']['net_return_pct']);sharpediffs=[x['Sharpe_delta'] for x in edges if x['Sharpe_delta'] is not None];std=float(np.std(sharpediffs,ddof=1));cliffs=[x for x in edges if x['Sharpe_delta'] is not None and abs(x['Sharpe_delta'])>2*std];allvalues=list(grid.values());highest=max(allvalues,key=lambda c:c['scenes']['3']['net_return_pct']);boundary={p:cvals.index(highest[p]) in [0,len(cvals)-1] for p,cvals in axes(highest).items()}
summary={'actual_configs':40,'actual_candidates':36,'actual_reference_only':4,'new_native_models':0,'cost_scenes':120,'passed':len(report['summary']['passed']),'rejected_candidates':len(report['summary']['rejected']),'failed_criteria_counts':dict(failed),'positive_candidate_configs_by_cost':report['summary']['positive_configs_by_cost'],'candidate_eachcost_recent6of8_count':sum(stress_fold_ok(c) for c in candidates),'complete_sensitivity_cells':63,'old_read_only_cells':27,'edges':138,'full3_positive_Sharpe_fraction':sum(c['scenes']['3']['sharpe_365']>0 for c in allvalues)/63,'full3_positive_net_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in allvalues)/63,'recent3_positive_net_fraction':sum(c['scenes']['3']['recent40']['net_return_pct']>0 for c in allvalues)/63,'descriptive_Sharpe_cliff_edges':len(cliffs),'descriptive_cliff_threshold_2sd':2*std,'highest_observed_cell':highest['name'],'highest_observed_boundary':boundary,'best_new':{'name':best['name'],'net_return3_pct':best['scenes']['3']['net_return_pct'],'whole_DD3_pct':best['scenes']['3']['max_drawdown_pct'],'recent_return3_pct':best['scenes']['3']['recent40']['net_return_pct'],'recent_positive_folds_by_cost':{k:positive_recent(best,k) for k in ['1','2','3']},'status':best['status'],'failed_criteria':best['failed_criteria']},'by_BTC_units':{str(w):{'candidates':sum(c['BTC_bank_units']==w for c in candidates),'passed':sum(c['BTC_bank_units']==w and c['status']=='passed' for c in candidates),'eachcost_recent6of8':sum(c['BTC_bank_units']==w and stress_fold_ok(c) for c in candidates)} for w in NEW_WEIGHTS},'exports':exportinfo,'figures':figures,'report_sha256':sha(R/'report.json'),'strict_gates_predeclared':True,'old_statuses_unchanged':True,'independent_future_qualification':False};put(R/'summary.json',summary)

put(R/'export_manifest.json',{'exports':exportinfo,'figures':figures,'financial_report_sha256':sha(R/'report.json')})
from run import module
module(R/'write_result.py','refined_ownership_result')
print(json.dumps({k:v for k,v in summary.items() if k not in ['exports','figures']},ensure_ascii=False),flush=True)
