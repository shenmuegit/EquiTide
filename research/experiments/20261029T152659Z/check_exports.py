"""Read-only complete export binding,all folds,ownership comparisons and adjacency check."""
import csv,json,math
from run import ROOT,R,sha,put,grid_configs,axes,positive_recent,WEIGHTS
r=json.loads((R/'report.json').read_text());s=json.loads((R/'summary.json').read_text());m=json.loads((R/'export_manifest.json').read_text());grid=grid_configs(r['configs']);allc={**grid,**{n:c for n,c in r['configs'].items() if c['role']=='benchmark'}}
def read(name):return list(csv.DictReader((R/(name+'.csv')).open()))
def near(a,b):assert abs(float(a)-float(b))<=1e-10*max(1,abs(float(a)),abs(float(b))),(a,b)
def check(row,want):
 for k,v in want.items():
  if v is None:assert row[k]=='',(k,row[k])
  elif isinstance(v,(int,float)) and not isinstance(v,bool):near(row[k],v)
  else:assert row[k]==str(v),(k,row[k],v)
for x in m['exports'].values():assert sha(ROOT/x['path'])==x['sha256']
cost=read('cost_results');full=read('walk_forward_folds');recent=read('recent40_folds');daily=read('daily_NAV');edges=read('sensitivity_edges');comparisons=read('reference_comparisons');assert list(map(len,[cost,full,recent,daily,edges,comparisons]))==[147,1911,1176,44520,96,216]
assert len({(x['name'],x['cost_multiplier']) for x in cost})==147
for row in cost:
 c=allc[row['name']];z=c['scenes'][row['cost_multiplier']];t=z['recent40'];check(row,{'role':c['role'],'read_only_old':bool(c.get('read_only_anchor')),'status':c['status'],**{f:z[f] for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']},'recent_return_pct':t['net_return_pct'],'recent_DD_pct':t['max_drawdown_pct'],'recent_positive_folds':positive_recent(c,row['cost_multiplier']),'monthly_positive_folds':sum(f['net_return_pct']>0 for f in z['folds'][:12]),'source_execution_actions':z['executions'],'source_round_trips':z['round_trips'],'cost_usdt':z['cost_usdt'],'cost_pct_initial':z['cost_pct_initial'],'funding_usdt':z['funding_usdt'],'funding_income_usdt':z['funding_income_usdt'],'funding_outflow_usdt':z['funding_outflow_usdt'],'gross_plus_funding_to_cost':z['gross_reference_PnL_to_execution_cost'],'NAV_sha256_f64le':z['NAV_sha256_f64le']})
for rows,kind,nfold in [(full,'full',13),(recent,'recent',8)]:
 assert len({(x['name'],x['cost_multiplier'],x['fold']) for x in rows})==len(rows)
 for row in rows:
  z=allc[row['name']]['scenes'][row['cost_multiplier']];z=z if kind=='full' else z['recent40'];f=z['folds'][int(row['fold'])-1];check(row,{k:f[k] for k in ['fold','duration_days','start_utc','end_exclusive_utc','net_return_pct','max_drawdown_pct','sharpe_365','calmar']})
for row in daily:near(row['NAV_usdt'],r['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['day_boundary_index'])])
assert len({(x['name'],x['cost_multiplier'],x['day_boundary_index']) for x in daily})==44520
seen=set()
for row in edges:
 a,b=grid[row['left']],grid[row['right']];dim=axes(a);axis=row['axis'];assert dim[axis].index(b[axis])==dim[axis].index(a[axis])+1 and all(a[p]==b[p] for p in dim if p!=axis);seen.add((row['left'],row['right']));aa,bb=a['scenes']['3'],b['scenes']['3'];check(row,{'full_return_delta_pp':bb['net_return_pct']-aa['net_return_pct'],'DD_delta_pp':bb['max_drawdown_pct']-aa['max_drawdown_pct'],'Sharpe_delta':bb['sharpe_365']-aa['sharpe_365'],'Calmar_delta':bb['calmar']-aa['calmar'],'recent_return_delta_pp':bb['recent40']['net_return_pct']-aa['recent40']['net_return_pct'],'left_min_positive_recent_folds':min(positive_recent(a,k) for k in ['1','2','3']),'right_min_positive_recent_folds':min(positive_recent(b,k) for k in ['1','2','3'])})
assert len(seen)==96
for row in comparisons:
 c,ref=allc[row['name']],allc[row['reference_name']];k=row['cost_multiplier'];a,b=c['scenes'][k],ref['scenes'][k]
 if row['reference_type']=='same_E_S_raw1_1':assert ref.get('read_only_anchor') and ref['BTC_bank_units']==1 and c['ETH_exit_buffer_fraction']==ref['ETH_exit_buffer_fraction'] and c['ETH_trend_lookback_days']==ref['ETH_trend_lookback_days']
 else:assert row['reference_type']=='same_raw_units_constant_long' and ref['role']=='benchmark' and c['raw_component_multipliers']==ref['raw_component_multipliers']
 check(row,{'candidate_return_pct':a['net_return_pct'],'reference_return_pct':b['net_return_pct'],'return_delta_pp':a['net_return_pct']-b['net_return_pct'],'candidate_DD_pct':a['max_drawdown_pct'],'reference_DD_pct':b['max_drawdown_pct'],'candidate_recent_return_pct':a['recent40']['net_return_pct'],'reference_recent_return_pct':b['recent40']['net_return_pct'],'recent_return_delta_pp':a['recent40']['net_return_pct']-b['recent40']['net_return_pct'],'candidate_positive_recent_folds':positive_recent(c,k),'reference_positive_recent_folds':positive_recent(ref,k),'candidate_source_actions':a['executions'],'reference_source_actions':b['executions']})
assert len({(x['name'],x['reference_type'],x['cost_multiplier']) for x in comparisons})==216
for x in m['figures']:assert sha(ROOT/x['path'])==x['sha256'] and (ROOT/x['path']).read_bytes().startswith(b'\x89PNG')
assert s['report_sha256']==m['financial_report_sha256']==sha(R/'report.json') and s['complete_sensitivity_cells']==45 and s['edges']==96 and s['actual_configs']==40 and s['passed']==len(r['summary']['passed'])
out={'passed':True,'cost_rows':147,'full_fold_rows':1911,'recent_fold_rows':1176,'daily_NAV_rows':44520,'edges':96,'reference_comparisons':216,'figures':3,'panels':18,'old9statuses_preserved':True,'financial_report_sha256':sha(R/'report.json')};put(R/'export_verification.json',out);print(json.dumps(out),flush=True)
