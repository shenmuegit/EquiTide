"""Export every actual ETH H/E result and old center without new simulation."""
import csv,json,statistics,collections
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from common import *
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());rows={}
def write(name,cols,items):
 with (R/name).open('w',newline='') as f:w=csv.writer(f,lineterminator='\n');w.writerow(cols);w.writerows(items)
 rows[name]=len(items)
cost=[];wf=[];recent=[];daily=[]
for c in r['configs'].values():
 for k,s in c['scenes'].items():
  cost.append([c['name'],c['fingerprint'],c['scope'],c['role'],c['D'],c['K'],c['S'],c['L'],c['H'],c['E'],c['R'],c['M'],c['VW'],c['VC'],c['N'],c['capital_usdt'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['cost_usdt'],s['cost_pct_initial'],s['funding_usdt'],s['gross_reference_PnL_to_execution_cost'],s['executions'],s['round_trips'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),c['status']]);wf.extend([c['name'],c['D'],c['K'],c['S'],c['L'],c['H'],c['E'],c['R'],c['M'],c['VW'],c['VC'],k,f['fold'],f['start_utc'],f['end_exclusive_utc'],f['duration_days'],f['net_return_pct'],f['max_drawdown_pct'],f['sharpe_365'],f['calmar']] for f in s['folds']);recent.extend([c['name'],c['D'],c['K'],c['S'],c['L'],c['H'],c['E'],c['R'],c['M'],c['VW'],c['VC'],k,f['fold'],f['start_utc'],f['end_exclusive_utc'],f['net_return_pct'],f['max_drawdown_pct'],f['sharpe_365'],f['calmar']] for f in s['recent40']['folds']);daily.extend([c['name'],c['D'],c['K'],c['S'],c['L'],c['H'],c['E'],c['R'],c['M'],c['VW'],c['VC'],k,i,v] for i,v in enumerate(s['daily_equity_usdt']))
write('cost_scenes.csv',['configuration','fingerprint','scope','role','ETH_D','ETH_K','ETH_S','ETH_L','ETH_H','ETH_E','ETH_R','ETH_M','ETH_budget_VW','ETH_VC','native_N_or_fixed_BTC_N','capital','cost_multiplier','return_pct','whole_DD_pct','Sharpe365','Calmar','cost_usdt','cost_pct_initial','funding_usdt','gross_plus_funding_to_cost','executions','closes','recent40_return_pct','positive5d_folds','status'],cost);write('walk_forward_folds.csv',['configuration','ETH_D','ETH_K','ETH_S','ETH_L','ETH_H','ETH_E','ETH_R','ETH_M','ETH_budget_VW','ETH_VC','cost_multiplier','fold','start_utc','end_exclusive_utc','days','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],wf);write('recent40_folds.csv',['configuration','ETH_D','ETH_K','ETH_S','ETH_L','ETH_H','ETH_E','ETH_R','ETH_M','ETH_budget_VW','ETH_VC','cost_multiplier','fold','start_utc','end_exclusive_utc','return_pct','whole_fold_DD_pct','Sharpe365','Calmar'],recent);write('daily_NAV.csv',['configuration','ETH_D','ETH_K','ETH_S','ETH_L','ETH_H','ETH_E','ETH_R','ETH_M','ETH_budget_VW','ETH_VC','cost_multiplier','boundary','NAV_usdt'],daily)
edges=[];flags={};cols=['ETH_D','ETH_S','ETH_H','ETH_E','ETH_R','ETH_M','ETH_budget_VW','ETH_K','ETH_VC','native_N_or_fixed_BTC_N','fingerprint','readonly_old','canonical_status','cost_multiplier','return_pct','whole_DD_pct','Sharpe365','Calmar','recent40_return_pct','positive5d_folds','local_positive3_fraction','local_strict_recent_fraction']
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key];items=[]
 for g in grid:
  c=full[g['fingerprint']];d=c['current_grid_diagnostic_sensitivity']
  for k,s in c['scenes'].items():items.append([g['D'],g['S'],g['H'],g['E'],g['R'],g['M'],g['VW'],g['K'],g['VC'],g['N'],g['fingerprint'],g['readonly'],c['status'],k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],s['recent40']['net_return_pct'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']),d['local_positive3_fraction'],d['local_strict_recent_fraction']])
 for k in ['1','2','3']:
  for g in grid:
   i,j=p['entry_hurdles'].index(g['H']),p['exit_buffers'].index(g['E']);adj=[h for h in grid if i<2 and h['H']==p['entry_hurdles'][i+1] and h['E']==g['E'] or j<2 and h['E']==p['exit_buffers'][j+1] and h['H']==g['H']]
   for h in adj:
    a,b=full[g['fingerprint']]['scenes'][k],full[h['fingerprint']]['scenes'][k];edges.append([scope,k,g['H'],g['E'],h['H'],h['E'],g['fingerprint'],h['fingerprint'],(abs(a['sharpe_365']-b['sharpe_365']) if a['sharpe_365'] is not None and b['sharpe_365'] is not None else None),abs(a['net_return_pct']-b['net_return_pct']),abs(a['max_drawdown_pct']-b['max_drawdown_pct'])])
 flags[scope]={}
 for k in ['1','2','3']:
  allxs=[x[8] for x in edges if x[0]==scope and x[1]==k];xs=[x for x in allxs if x is not None];t=2*statistics.stdev(xs) if len(xs)>=2 else None;flags[scope][k]={'edge_count':len(allxs),'defined_Sharpe_edges':len(xs),'undefined_Sharpe_edges':len(allxs)-len(xs),'max_Sharpe_change':max(xs) if xs else None,'two_std_change_threshold':t,'descriptive_cliff_flag':max(xs)>t if t is not None else None,'scope':'Dependent adjacency diagnostic,not multiplicity-adjusted significance or qualification.'}
 write('sensitivity_grid.csv' if scope=='parent' else 'native_sensitivity_grid.csv',cols,items)
write('adjacent_edges.csv',['scope','cost_multiplier','from_H','from_E','to_H','to_E','from_fp','to_fp','absolute_Sharpe_change','absolute_return_change_pp','absolute_DD_change_pp'],edges);ext=[]
ref=p['read_only_references'][p['primary_control_fingerprint']];old=next(c for c in json.loads((ROOT/ref['report']).read_text())['configs'].values() if c['fingerprint']==p['primary_control_fingerprint'])
for k,s in old['scenes'].items():ext.append([old['name'],old['fingerprint'],29,.03,18750,k,s['net_return_pct'],s['max_drawdown_pct'],s['sharpe_365'],s['calmar'],old['status'],ref['report'],ref['report_sha256']])
write('readonly_reused_scenes.csv',['configuration','fingerprint','BTC_L','BTC_H','capital','cost_multiplier','return_pct','whole_DD_pct','Sharpe365','Calmar','unchanged_status','report','report_sha256'],ext);cs=r['matched_hold_comparisons'];write('matched_hold_comparisons.csv',list(cs[0]),[list(x.values()) for x in cs])
source=[]
for fp,c in {**{fp:next(c for c in json.loads((ROOT/z['report']).read_text())['configs'].values() if c['fingerprint']==fp) for fp,z in p['read_only_references'].items() if z['scope']=='native'},**{c['fingerprint']:c for c in r['configs'].values() if c['scope']=='native'}}.items():
 isnew=any(x['fingerprint']==fp for x in r['configs'].values());spec=json.loads((ROOT/c['spec']).read_text());q=spec['parameters']
 for k,s in c['scenes'].items():source.append([fp,spec['universe'][0],q['initial_capital_usdt'],q['fixed_entry_notional_usdt'],q.get('lookback_days'),q.get('return_hurdle'),q.get('exit_buffer_fraction'),q.get('trend_window_days'),q.get('trend_slope_lag_days'),q.get('trend_slope_hurdle_fraction'),q.get('entry_volatility_ceiling'),k,s['net_return_pct'],s['max_drawdown_pct'],s['cost_usdt'],s['funding_usdt'],s['executions'],s['NAV_sha256_f64le'],isnew])
write('source_curves.csv',['fingerprint','asset','actual_bank_capital','actual_entry_N','lookback','hurdle','exit_buffer','trend_S','slope_D','slope_K','entry_VC','cost_multiplier','return_pct','whole_DD_pct','cost_usdt','funding_usdt','executions','NAV_sha256','new_native_actual'],source);alloc=[[g['fingerprint'],g['role'],(29 if g['role']!='benchmark' else 0),(.03 if g['role']!='benchmark' else 0),(.01 if g['role']!='benchmark' else 0),g['L'],g['H'],g['E'],g['S'],g['D'],g['K'],g.get('VC'),3750,15000,18750,1000,4500,1,1,.2,.8,1000/18750,.24,g['readonly']] for g in p['grid']+p['benchmarks']];write('fixed_allocations.csv',['fingerprint','role','BTC_L','BTC_H','BTC_E','ETH_L','ETH_H','ETH_E','ETH_S','ETH_D','ETH_K','ETH_VC','BTC_bank','ETH_bank','total_initial_capital','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','BTC_capital_share','ETH_capital_share','BTC_initial_nominal_share','ETH_initial_nominal_share','readonly'],alloc);put(R/'edge_flags.json',flags)
fig,axs=plt.subplots(2,4,figsize=(17,9),layout='constrained')
for rr,(label,key) in enumerate([('ETH: bank15000/N4500','all_current_native_grid'),('BTC3750/N1000 + ETH15000/N4500','all_current_grid')]):
 for jj,(title,fn) in enumerate([('3x continuous370 return %',lambda c:c['scenes']['3']['net_return_pct']),('3x wholecurve DD %',lambda c:c['scenes']['3']['max_drawdown_pct']),('3x daily Sharpe365',lambda c:c['scenes']['3']['sharpe_365']),('3x recent positive5d /8',lambda c:sum(f['net_return_pct']>0 for f in c['scenes']['3']['recent40']['folds']))]):
  arr=np.empty((3,3))
  for c in r[key].values():arr[p['entry_hurdles'].index(c['H']),p['exit_buffers'].index(c['E'])]=fn(c)
  ax=axs[rr,jj];im=ax.imshow(arr,aspect='auto',cmap='RdYlGn_r' if jj==1 else 'RdYlGn',**({'vmin':0,'vmax':8} if jj==3 else {}));ax.set_xticks(range(3),['E=0.00625','E=0.0075','E=0.00875']);ax.set_yticks(range(3),['H=0.0175','H=0.02','H=0.0225']);ax.set_xlabel('ETH exit buffer E');ax.set_ylabel('ETH ROC entry hurdle H');ax.set_title(label+'\n'+title,fontsize=10)
  for c in r[key].values():ii,j=p['entry_hurdles'].index(c['H']),p['exit_buffers'].index(c['E']);ax.text(j,ii,(f'{arr[ii,j]:.3f}' if np.isfinite(arr[ii,j]) else 'N/A')+(' O' if c['readonly'] else ' N'),ha='center',va='center',fontsize=9)
  fig.colorbar(im,ax=ax,shrink=.7)
fig.suptitle('ETH H0.0175/0.02/0.0225 x E0.00625/0.0075/0.00875 | fixed funding M4/VW8/R0.00875 | K0.75% VC5% | fixedL5 S16 D3,V10 | H/E varied | BTC29/H3%/E1%\nraw[1,1],wholebanks3750/15000 | O=oldH.02/E.0075 center,N=new | priceV10,budgetVW8 fixed | reuseddevelopmenthistory');fig.savefig(R/'sensitivity.png',dpi=140);plt.close(fig)
summary={'report_sha256':sha(R/'report.json'),**p['expected_counts'],'passed':len(r['summary']['passed']),'rejected':len(r['summary']['candidate_rejected']),'native_passed':sum(c['scope']=='native' and c['status']=='passed' for c in r['configs'].values()),'failed_criteria':dict(collections.Counter(x for c in r['configs'].values() for x in c['failed_criteria'])),'CSV_rows':rows,'edge_flags':flags};put(R/'sensitivity_summary.json',summary)
comparisons=[]
for c in r['configs'].values():
 ref=p['read_only_references'][c['reference_fingerprint']];oc=next(x for x in json.loads((ROOT/ref['report']).read_text())['configs'].values() if x['fingerprint']==c['reference_fingerprint']);comparisons.append({'fingerprint':c['fingerprint'],'scope':c['scope'],'L':c['L'],'H':c['H'],'E':c['E'],'M':c['M'],'VW':c['VW'],'R':c['R'],'reference_fingerprint':oc['fingerprint'],'D':c['D'],'K':c['K'],'VC':c['VC'],'old_VC':.05,'old_D':oc['D'],'old_K':oc['K'],'old_E':oc['E'],'old_L':5,'old_H':oc['H'],'old_S':oc['S'],'fixed_BTC_L':29,'fixed_BTC_H':.03,'fixed_BTC_E':.01,'same_bank_capitals_and_entry_notionals':True,'same_BTC_component_if_parent':True,'all_cost_NAV_identical':all(c['scenes'][k]['NAV_sha256_f64le']==oc['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),'cost_comparisons':{k:{'return_pct':s['net_return_pct'],'whole_DD_pct':s['max_drawdown_pct'],'old_return_pct':oc['scenes'][k]['net_return_pct'],'old_DD_pct':oc['scenes'][k]['max_drawdown_pct']} for k,s in c['scenes'].items()}})
put(R/'equivalent_realized_NAV_paths.json',{'report_sha256':sha(R/'report.json'),'comparisons':comparisons,'scope':'ETH H/E changes against exactM4/VW8/R.00875 H.02/E.0075 center,actualETH4500quantity/cost recomputed;fixedBTC29H3readonly. No independentholdout claim.'});groups={}
for c in r['configs'].values():groups.setdefault(c['scope']+'|'+'|'.join(c['scenes'][k]['NAV_sha256_f64le'] for k in ['1','2','3']),[]).append(c['fingerprint'])
put(R/'prior_grid_NAV_aliases.json',{'new_definitions_matching_reference_NAV':sum(x['all_cost_NAV_identical'] for x in comparisons),'within_new_grid_alias_groups':[v for v in groups.values() if len(v)>1]})
rs=reg.read_records(ROOT/'research/automation/registry.jsonl');new={c['fingerprint'] for c in r['configs'].values()};hist={}
for fp,z in rs.items():
 sp=z.get('spec',{});obs=sp.get('family')=='paper-live-portfolio-observation' or sp.get('name','').startswith('forward_snapshot_') or 'observation_terminal_action' in sp.get('parameters',{})
 if fp not in new and sp and not obs:hist.setdefault(reg.fingerprint(sp),[]).append(z)
trials={'canonical_prior_research_definitions':len(hist),'registry_marked_actual':sum(any(z.get('result_available') is True for z in v) for v in hist.values()),'not_marked_actual':sum(not any(z.get('result_available') is True for z in v) for v in hist.values()),'initial16_actual_evidence':16,'new_financial_definitions':16,'new_native_models':8,'new_cost_scenes':48,'observations_excluded':True};put(R/'prior_actual_research_counts.json',trials);ctx=json.loads((R/'context.json').read_text());parents=[c for c in r['configs'].values() if c['scope']=='parent']



print(json.dumps(summary),flush=True)
