"""Export every saved cost/fold/variant; no strategy or account execution."""
import csv,json,math
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());out=R/'exports';out.mkdir(exist_ok=True)
def save(name,rows):
 assert rows;keys=list(dict.fromkeys(k for row in rows for k in row));f=out/(name+'.csv')
 with f.open('w',newline='') as z:
  w=csv.DictWriter(z,keys,lineterminator="\n");w.writeheader();w.writerows(rows)
 return {'path':rel(f),'rows':len(rows),'sha256':sha(f)}
costs=[];folds=[];recent=[];ext=[];daily=[];sensitivity=[]
fields=['net_return_pct','max_drawdown_pct','sharpe_365','calmar','executions','round_trips','cost_usdt','funding_usdt','gross_reference_price_PnL_usdt','gross_reference_PnL_to_execution_cost']
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  base=dict(name=c['name'],fingerprint=c['fingerprint'],scope=c['scope'],W=c['W'],K=c['K'],cost=int(k),status=c['status'],role=c['role']);row={**base,**{f:s.get(f) for f in fields},'fee_usdt':s['cost_parts_usdt']['fee'],'half_spread_usdt':s['cost_parts_usdt']['half_spread'],'slippage_usdt':s['cost_parts_usdt']['slippage'],'impact_usdt':s['cost_parts_usdt']['impact'],'execution_cost_pct_initial':100*s['cost_usdt']/c['capital_usdt'],'funding_pct_initial':100*s['funding_usdt']/c['capital_usdt'],'execution_cost_share_of_gross_plus_funding':s['cost_usdt']/(s['gross_reference_price_PnL_usdt']+s['funding_usdt']) if s['gross_reference_price_PnL_usdt']+s['funding_usdt'] else None,'local_positive3':c['sensitivity']['local_3x_neighbor_positive_fraction'],'local_strict_recent':c['sensitivity']['local_recent_allcost_qualifying_fraction'],'recent_positive_folds':c['recent40_positive_5d_folds_by_cost'][k],'failed_criteria':';'.join(c['failed_criteria'])};costs.append(row);sensitivity.append(row)
  for name,ss,dest in [('WF389',s,folds),('recent40',s['recent40'],recent),('extension19',s['extension19'],ext)]:
   for f in ss['folds']:dest.append({**base,'window':name,**f})
  for j,v in enumerate(s['daily_equity_usdt']):daily.append({**base,'boundary_index':j,'equity_usdt':v})
files=[save(n,z) for n,z in [('costs',costs),('walk_forward_folds',folds),('recent40_folds',recent),('extension19_folds',ext),('daily_NAV',daily),('joint_sensitivity',sensitivity),('matched_hold_comparisons',r['matched_hold_comparisons'])]]
edges=[]
for scope in ['native','parent']:
 cs=list((r['all_current_grid'] if scope=='parent' else r['all_current_native_grid']).values())
 for i,a in enumerate(cs):
  for b in cs[i+1:]:
   if abs(p['axes']['BTC_L'].index(a['W'])-p['axes']['BTC_L'].index(b['W']))+abs(p['axes']['BTC_E'].index(a['K'])-p['axes']['BTC_E'].index(b['K']))!=1:continue
   sa,sb=a['scenes']['3'],b['scenes']['3'];edges.append({'scope':scope,'from':a['name'],'to':b['name'],'delta_net_pp':sb['net_return_pct']-sa['net_return_pct'],'delta_sharpe':None if sa['sharpe_365'] is None or sb['sharpe_365'] is None else sb['sharpe_365']-sa['sharpe_365'],'delta_DD_pp':sb['max_drawdown_pct']-sa['max_drawdown_pct'],'delta_Calmar':None if sa['calmar'] is None or sb['calmar'] is None else sb['calmar']-sa['calmar']})
files.append(save('adjacent_sensitivity_edges',edges));valid=[abs(e['delta_sharpe']) for e in edges if e['delta_sharpe'] is not None];sd=float(np.std(valid,ddof=1));cliffs=[e for e in edges if e['delta_sharpe'] is not None and abs(e['delta_sharpe'])>2*sd]
by={};old={}
for c in r['configs'].values():by.setdefault(tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),[]).append(c['name'])
for fp,z in p['read_only_references'].items():
 doc=json.loads((ROOT/z['report']).read_text());c=next(c for c in doc['configs'].values() if c['fingerprint']==fp);old[fp]=tuple(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3'])
aliases=[{'new_names':names,'old_fingerprints':[fp for fp,v in old.items() if v==sig]} for sig,names in by.items()]
put(R/'NAV_alias_inventory.json',{'passed':True,'new_configs':12,'distinct_allcost_NAV_paths':len(by),'groups':aliases,'new_allcost_signatures_seen_before':sum(bool(x['old_fingerprints']) for x in aliases),'candidate_parent_old_path_aliases':sum(any(n.startswith('btclexitmid389_parent') for n in x['new_names']) and bool(x['old_fingerprints']) for x in aliases),'definition_count_not_independent_trial_count':True})
for g,c in r['all_current_grid'].items():
 if c.get('readonly'):
  ns=[z for z in r['all_current_grid'].values() if abs(p['axes']['BTC_L'].index(z['W'])-p['axes']['BTC_L'].index(c['W']))<=1 and abs(p['axes']['BTC_E'].index(z['K'])-p['axes']['BTC_E'].index(c['K']))<=1];c['sensitivity']=dict(c['sensitivity'],local_recent_allcost_qualifying_fraction=sum(all(z['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in z['recent40']['folds'])>=6 for z in a['scenes'].values()) for a in ns)/len(ns))
fig,axs=plt.subplots(2,3,figsize=(15,8),layout='constrained');cs=list(r['all_current_grid'].values());panels=[('389d net return, 3x (%)',lambda c:c['scenes']['3']['net_return_pct'],None),('Whole-path max drawdown, 3x (%)',lambda c:c['scenes']['3']['max_drawdown_pct'],None),('Recent40 positive 5d folds, 3x',lambda c:c['recent40_positive_5d_folds_by_cost']['3'],(0,8)),('389d Sharpe, 3x',lambda c:c['scenes']['3']['sharpe_365'],None),('389d Calmar, 3x',lambda c:c['scenes']['3']['calmar'],None),('Local strict recent fraction',lambda c:c['sensitivity']['local_recent_allcost_qualifying_fraction'],(0,1))]
for ax,(title,get,bounds) in zip(axs.flat,panels):
 arr=np.array([[get(next(c for c in cs if c['W']==W and c['K']==K)) for K in p['axes']['BTC_E']] for W in p['axes']['BTC_L']],dtype=float);im=ax.imshow(arr,aspect='auto',cmap='viridis',**({'vmin':bounds[0],'vmax':bounds[1]} if bounds else {}));ax.set(title=title,xlabel='BTC persistence exit buffer',ylabel='BTC completed-day ROC lookback');ax.set_xticks(range(3),['0.5%','1.0%','1.5%']);ax.set_yticks(range(3),['28','29','30']);fig.colorbar(im,ax=ax,shrink=.8)
 for i in range(3):
  for j in range(3):ax.text(j,i,f'{arr[i,j]:.3f}',ha='center',va='center',color='white' if (im.norm(arr[i,j]) if math.isfinite(arr[i,j]) else 0)<.55 else 'black')
fig.suptitle('Predeclared BTC immediate lookback/exit boundary + fixed ETH long-only bank | 389 historical days | 3x costs',fontsize=14);fig.savefig(out/'sensitivity.png',dpi=150);plt.close(fig)
put(R/'export_verification.json',{'passed':True,'saved_results_only':True,'files':files,'plot':rel(out/'sensitivity.png'),'plot_sha256':sha(out/'sensitivity.png'),'adjacent_edges':len(edges),'absolute_sharpe_change_sample_std':sd,'cliffs_over_two_std':cliffs,'boundary_optima_diagnostic_only':True,'no_grid_extension_or_representative_reselection':True});print(json.dumps({'passed':True,'exports':files,'distinct_paths':len(by),'cliff_edges':len(cliffs)}))
