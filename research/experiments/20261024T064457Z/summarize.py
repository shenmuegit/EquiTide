"""Complete three-axis portfolio surfaces and Chinese evidence before finish."""
import csv,gzip,io,itertools,json,statistics
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import ROOT,R,HURDLES,BUFFERS,sha,put,grid_configs
def table(path,rows,compressed=False):
 fields=list(dict.fromkeys(k for row in rows for k in row));buf=io.StringIO(newline='');w=csv.DictWriter(buf,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);raw=buf.getvalue().encode();path.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
def main():
 assert not (R/'finish.json').exists(),'Finished report bytes must stay immutable;use readonly audits.'
 report=json.loads((R/'report.json').read_text());plan=json.loads((R/'plan.json').read_text());grid=grid_configs(report['configs']);cs=list(report['configs'].values());anchors=json.loads((R/'anchors.json').read_text());by={(c['BTC_return_hurdle'],c['BTC_exit_buffer_fraction'],c['ETH_return_hurdle'],c['ETH_exit_buffer_fraction']):c for c in grid.values()};rows=[];folds=[];daily=[];cells={};edges=[];comparisons=[]
 for c in grid.values():
  readonly=c['name'] in anchors;meta={p:c[p] for p in ['name','BTC_return_hurdle','BTC_exit_buffer_fraction','ETH_return_hurdle','ETH_exit_buffer_fraction']};meta['read_only_anchor']=readonly
  cells[c['name']]={**meta,'fingerprint':c['fingerprint'],'qualification_status':c['status'],'qualification_scope':'originalsourcegrid unchanged' if readonly else 'current frozen144cellfouraxisgrid','original_report':anchors[c['name']]['report'] if readonly else str((R/'report.json').relative_to(ROOT)),'positive_folds_1x':c['positive_folds_1x'],'scenes':{k:{p:z[p] for p in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','NAV_sha256_f64le']} for k,z in c['scenes'].items()}}
  for k,z in c['scenes'].items():
   cost={'cost_multiplier':int(k)};rows.append({**meta,**cost,'status':c['status'],'positive_folds_1x':c['positive_folds_1x'],**{p:z[p] for p in ['net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar','cost_usdt','funding_usdt','gross_reference_PnL_to_execution_cost','executions','round_trips','NAV_sha256_f64le']},**{'cost_'+p:v for p,v in z['cost_parts_usdt'].items()},'funding_income_usdt':z['funding_income_usdt'],'funding_outflow_usdt':z['funding_outflow_usdt'],'funding_stress_increment_usdt':z['funding_stress_increment_usdt'],'margin_independent_sleeve_violations':z['margin']['independent_sleeve_violations'],'margin_minimum_sleeve_cushion_usdt':z['margin']['minimum_individual_sleeve_cushion_usdt']})
   for f in z['folds']:folds.append({**meta,**cost,**f})
   if not readonly:
    for j,equity in enumerate(z['daily_equity_usdt']):daily.append({**meta,**cost,'boundary_index':j,'equity_usdt':equity})
  if not readonly:
   old=by[c['BTC_return_hurdle'],c['BTC_exit_buffer_fraction'],c['ETH_return_hurdle'],0];comparisons.append({'name':c['name'],'readonly_zeroETHbuffer_name':old['name'],'old_status_unchanged':old['status'],'new_status':c['status'],'positive_folds1_delta':c['positive_folds_1x']-old['positive_folds_1x'],'return3_delta_pp':c['scenes']['3']['net_return_pct']-old['scenes']['3']['net_return_pct'],'DD3_delta_pp':c['scenes']['3']['max_drawdown_pct']-old['scenes']['3']['max_drawdown_pct']})
 axes=[HURDLES,BUFFERS,HURDLES,BUFFERS]
 for params,c in by.items():
  for index,axis in enumerate(axes):
   j=axis.index(params[index])
   if j+1==len(axis):continue
   other=list(params);other[index]=axis[j+1];d=by[tuple(other)];a,b=c['scenes']['3'],d['scenes']['3'];edges.append({'from':c['name'],'to':d['name'],'axis':['BTC_H','BTC_exit_buffer','ETH_H','ETH_exit_buffer'][index],'from_readonly':c['name'] in anchors,'to_readonly':d['name'] in anchors,'return3_delta_pp':b['net_return_pct']-a['net_return_pct'],'sharpe3_delta':b['sharpe_365']-a['sharpe_365'],'DD3_delta_pp':b['max_drawdown_pct']-a['max_drawdown_pct']})
 table(R/'sensitivity.csv',rows);table(R/'fold_results.csv',folds);table(R/'daily_equity.csv.gz',daily,True);table(R/'joint_edges.csv',edges);table(R/'zeroETHbuffer_comparison.csv',comparisons)
 holdref=plan['read_only_hold_reference'];assert sha(ROOT/holdref['report'])==holdref['report_sha256'];hold=json.loads((ROOT/holdref['report']).read_text())['configs'][holdref['name']];holdrows=[]
 for c in cs:
  for k,z in c['scenes'].items():holdrows.append({'name':c['name'],'cost_multiplier':int(k),'new_return_pct':z['net_return_pct'],'readonly_samebudget_hold_return_pct':hold['scenes'][k]['net_return_pct'],'net_return_advantage_pp':z['net_return_pct']-hold['scenes'][k]['net_return_pct'],'cash_analytic_return_pct':0})
 table(R/'hold_comparison.csv',holdrows);diffs=[abs(e['sharpe3_delta']) for e in edges];threshold=2*statistics.stdev(diffs);peak=max(grid.values(),key=lambda c:c['scenes']['3']['net_return_pct']);report['joint_grid_sensitivity']={'axes':plan['grid'],'cells':cells,'new_cells':108,'read_only_old_cells':36,'old_qualification_not_rerated':True,'positive3_fraction':sum(c['scenes']['3']['net_return_pct']>0 for c in grid.values())/144,'positive_sharpe3_fraction':sum(c['scenes']['3']['sharpe_365']>0 for c in grid.values())/144,'adjacent_edges':len(edges),'descriptive_Sharpe_cliff_threshold':threshold,'descriptive_cliff_edges':[e for e in edges if abs(e['sharpe3_delta'])>threshold],'cliff_rule':'abs adjacent Sharpe3 change >2*sample std of408 absolute changes;description,not a new gate','highest_grid_cell':peak['name'],'highest_at_grid_boundary':peak['BTC_return_hurdle'] in [HURDLES[0],HURDLES[-1]] or peak['ETH_return_hurdle'] in [HURDLES[0],HURDLES[-1]] or peak['BTC_exit_buffer_fraction'] in [BUFFERS[0],BUFFERS[-1]] or peak['ETH_exit_buffer_fraction'] in [BUFFERS[0],BUFFERS[-1]],'selection_limit':'Known components/330dayhistory;no untouchedholdout,DSR/PBO orliveTCA.'};report['failure_counts']=dict(Counter(k for c in cs for k in c['failed_criteria']));report['readonly_hold_returns_by_cost']={k:z['net_return_pct'] for k,z in hold['scenes'].items()};report['buffer_tradeoff']={'matched_old_comparisons':108,'higher_return3_than_zeroETHbuffer':sum(x['return3_delta_pp']>0 for x in comparisons),'lower_DD3_than_zeroETHbuffer':sum(x['DD3_delta_pp']<0 for x in comparisons),'positive_folds1_improved':sum(x['positive_folds1_delta']>0 for x in comparisons)};put(R/'report.json',report)
 fig,axs=plt.subplots(4,4,figsize=(17,13),constrained_layout=True);vals=[c['scenes']['3']['net_return_pct'] for c in grid.values()];vmin=min(0,min(vals));vmax=max(vals)
 for i,eb in enumerate(BUFFERS):
  for j,ee in enumerate(BUFFERS):
   ax=axs[i,j];mat=np.asarray([[by[hb,eb,he,ee]['scenes']['3']['net_return_pct'] for he in HURDLES] for hb in HURDLES]);im=ax.imshow(mat,cmap='RdYlGn',vmin=vmin,vmax=vmax);ax.set_title(f'BTC E{eb:.2%} / ETH E{ee:.2%}'+(' (old)' if ee==0 else ' (new)'));ax.set_xticks(range(3),['1%','2%','4%']);ax.set_yticks(range(3),['1%','2%','4%']);ax.set_xlabel('ETH entry H');ax.set_ylabel('BTC entry H')
   for x,y in itertools.product(range(3),repeat=2):ax.text(y,x,f'{mat[x,y]:.2f}%',ha='center',va='center',fontsize=9)
 fig.colorbar(im,ax=axs,label='3x net return (%)');fig.suptitle('L30/L30 fixed1/1 fundedbanks 20000USDT;108 new+36readonly;knownhistory');fig.savefig(R/'sensitivity_surface.png',dpi=120);plt.close(fig)
 ctx=json.loads((R/'context.json').read_text());audit=json.loads((R/'verification.json').read_text());fwd=json.loads((R/'forward_report.json').read_text());fv=json.loads((R/'forward_verification.json').read_text());best=max(cs,key=lambda c:c['scenes']['3']['net_return_pct']);passed=[c for c in cs if c['status']=='passed'];summary={'new_parents':108,'source_components_readonly':21,'new_component_backtests':0,'new_cost_scenes':324,'new_folds':3564,'readonly_old_parents':36,'full_grid_cost_rows':len(rows),'fold_rows_including_old':len(folds),'new_daily_NAV_rows':len(daily),'joint_edges':len(edges),'passed':len(passed),'rejected':108-len(passed),'positive_configs_by_cost':report['summary']['positive_configs_by_cost'],'failure_counts':report['failure_counts'],'tradeoff':report['buffer_tradeoff'],'highest_new':{'name':best['name'],'return3':best['scenes']['3']['net_return_pct'],'DD3':best['scenes']['3']['max_drawdown_pct'],'positive_folds1':best['positive_folds_1x'],'status':best['status']}};put(R/'summary.json',summary)
 from summary_prose import write_texts
 write_texts(report,summary,audit,fwd,fv,ctx);print(json.dumps(summary,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
