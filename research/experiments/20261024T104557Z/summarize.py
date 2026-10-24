"""Complete new/readonly joint surface and Chinese evidence; before registry finish."""
import csv,gzip,io,json,itertools
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,BTC_LOOKS,ETH_LOOKS,HURDLES,sha,put,grid_configs
def table(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=b.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
def main():
 assert not (R/'finish.json').exists(),'Finished report muststayimmutable'
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());grid=grid_configs(report['configs']);cs=list(report['configs'].values());anchors=json.loads((R/'anchors.json').read_text());by={(c['BTC_lookback_days'],c['BTC_return_hurdle'],c['ETH_lookback_days'],c['ETH_return_hurdle']):c for c in grid.values()};rows=[];folds=[];daily=[];cells={};edges=[]
 for c in grid.values():
  readonly=c['name'] in anchors;meta={p:c[p] for p in ['name','BTC_lookback_days','BTC_return_hurdle','ETH_lookback_days','ETH_return_hurdle']};meta['read_only_anchor']=readonly
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'qualification_status':c['status'],'qualification_scope':'originalsourcegrid unchanged' if readonly else 'current frozen225cellgrid','original_report':anchors[c['name']]['report'] if readonly else str((R/'report.json').relative_to(ROOT)),'positive_folds_1x':c['positive_folds_1x'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   cost={'cost_multiplier':int(k)};rows.append({**meta,**cost,'status':c['status'],'positive_folds_1x':c['positive_folds_1x'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()},'funding_income_usdt':z['funding_income_usdt'],'funding_outflow_usdt':z['funding_outflow_usdt'],'funding_stress_increment_usdt':z['funding_stress_increment_usdt'],'margin_independent_sleeve_violations':z['margin']['independent_sleeve_violations'],'margin_minimum_sleeve_cushion_usdt':z['margin']['minimum_individual_sleeve_cushion_usdt']})
   for f in z['folds']:folds.append({**meta,**cost,**f})
   if not readonly:
    for day,equity in enumerate(z['daily_equity_usdt']):daily.append({**meta,**cost,'boundary_index':day,'equity_usdt':equity})
 axes=[BTC_LOOKS,HURDLES,ETH_LOOKS,HURDLES]
 for params,c in by.items():
  for index,axis in enumerate(axes):
   i=axis.index(params[index])
   if i+1==len(axis):continue
   other=list(params);other[index]=axis[i+1];d=by[tuple(other)];a,b=c['scenes']['3'],d['scenes']['3'];edges.append({'from':c['name'],'to':d['name'],'axis':['BTC_L','BTC_H','ETH_L','ETH_H'][index],'from_readonly':c['name'] in anchors,'to_readonly':d['name'] in anchors,'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct']})
 table(R/'sensitivity.csv',rows);table(R/'fold_results.csv',folds);table(R/'daily_equity.csv.gz',daily,True);table(R/'joint_edges.csv',edges)
 report['joint_grid_sensitivity']={'axes':plan['grid'],'cells':cells,'new_cells':198,'read_only_old_cells':27,'old_qualification_not_rerated':True,'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in grid.values())/225,'positive_sharpe3_fraction':sum(c['scenes']['3']['sharpe_365']>0 for c in grid.values())/225,'new_positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in cs)/198,'adjacent_edges':len(edges),'largest_abs_adjacent_return3_change_pp':max(abs(e['return3_delta_pp']) for e in edges),'highest3_at_lookback_boundary':(lambda c:c['BTC_lookback_days'] in (BTC_LOOKS[0],BTC_LOOKS[-1]) or c['ETH_lookback_days'] in (ETH_LOOKS[0],ETH_LOOKS[-1]))(max(grid.values(),key=lambda x:x['scenes']['3']['net_return_pct'])),'selection_limit':'Seen-history extension and reused oldcomponents;no independent final holdout,DSR/PBO or live TCA.'}
 report['failure_counts']=dict(Counter(k for c in cs for k in c['failed_criteria']))
 hold=plan['read_only_hold_reference'];assert sha(ROOT/hold['report'])==hold['report_sha256'];holdcfg=json.loads((ROOT/hold['report']).read_text())['configs'][hold['name']]
 report['read_only_same_budget_hold_reference']={**hold,'returns_by_cost':{k:z['net_return_pct'] for k,z in holdcfg['scenes'].items()},'rerun':False};put(R/'report.json',report)
 fig,axs=plt.subplots(3,3,figsize=(13.5,12.5),constrained_layout=True);vmax=max(c['scenes']['3']['net_return_pct'] for c in grid.values());vmin=min(0,min(c['scenes']['3']['net_return_pct'] for c in grid.values()))
 for i,hb in enumerate(HURDLES):
  for j,he in enumerate(HURDLES):
   ax=axs[i,j];mat=np.asarray([[by[lb,hb,le,he]['scenes']['3']['net_return_pct'] for le in ETH_LOOKS] for lb in BTC_LOOKS]);im=ax.imshow(mat,cmap='RdYlGn',vmin=vmin,vmax=vmax);ax.set_xticks(range(5),[str(x) for x in ETH_LOOKS]);ax.set_yticks(range(5),[str(x) for x in BTC_LOOKS]);ax.set_xlabel('ETH lookback days');ax.set_ylabel('BTC lookback days');ax.set_title(f'BTC entry{hb:.0%} / ETH entry{he:.0%}')
   for x,y in itertools.product(range(5),repeat=2):
    c=by[BTC_LOOKS[x],hb,ETH_LOOKS[y],he];ax.text(y,x,f'{mat[x,y]:.2f}'+('*' if c['name'] in anchors else ''),ha='center',va='center',fontsize=8)
 fig.colorbar(im,ax=axs,label='3x cost net return (%)');fig.suptitle('Fixed funded1/1 banks20000USDT;198new+27readonly(*);225cellknownhistory');fig.savefig(R/'sensitivity_surface.png',dpi=135);plt.close(fig)
 fwd=json.loads((R/'forward_report.json').read_text());audit=json.loads((R/'verification.json').read_text());ctx=json.loads((R/'context.json').read_text());best=max(cs,key=lambda c:c['scenes']['3']['net_return_pct']);qualified=[c for c in cs if c['status']=='passed'];summary={'new_parents':198,'read_only_anchors':27,'new_component_backtests':0,'new_scenes':594,'new_folds':6534,'full_grid_scenes_with_old':len(rows),'fold_rows_with_old':len(folds),'new_daily_NAV_rows':len(daily),'new_passed':len(qualified),'new_rejected':198-len(qualified),'positive_new_by_cost':report['summary']['positive_configs_by_cost'],'failure_counts':report['failure_counts'],'highest_new':{'name':best['name'],'return3':best['scenes']['3']['net_return_pct'],'DD3':best['scenes']['3']['max_drawdown_pct'],'status':best['status'],'folds1':best['positive_folds_1x']}}
 if qualified:
  q=max(qualified,key=lambda c:c['scenes']['3']['net_return_pct']);summary['highest_qualified']={'name':q['name'],'return3':q['scenes']['3']['net_return_pct'],'DD3':q['scenes']['3']['max_drawdown_pct'],'folds1':q['positive_folds_1x']}
 put(R/'summary.json',summary)
 from summary_prose import write_texts
 write_texts(report,plan,summary,audit,fwd,ctx)
 print(json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
