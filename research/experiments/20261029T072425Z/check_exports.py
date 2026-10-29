"""Check every exported number and actual within-group parameter edge,without re-evaluation."""
import csv,gzip,io,json
from run import R,sha,put,grid_configs,axes
from summarize import all_configs
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());allby=all_configs(r,p);grid=grid_configs(r['configs'])
def read(n):return list(csv.DictReader((R/n).open()))
cost,folds,recent,edges,comp=[read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']];daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert list(map(len,[cost,folds,recent,daily,edges,comp]))==[273,3549,2184,60102,135,486]
def eq(s,v):assert (s=='' if v is None else float(s)==v),(s,v)
for row in cost:
 z=allby[row['name']]['scenes'][row['cost_multiplier']];assert row['NAV_sha256_f64le']==z['NAV_sha256_f64le']
 for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','cost_usdt','cost_pct_initial','funding_usdt']:eq(row[f],z[f])
 for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row['recent40_'+f],z['recent40'][f])
for rows,short in [(folds,False),(recent,True)]:
 for row in rows:
  z=allby[row['name']]['scenes'][row['cost_multiplier']];z=(z['recent40'] if short else z)['folds'][int(row['fold'])-1]
  for f in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row[f],z[f])
for row in daily:assert float(row['equity_usdt'])==r['configs'][row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['boundary_index'])]
for e in edges:
 a,b=grid[e['from']],grid[e['to']];dims=axes(a);assert sum(a[k]!=b[k] for k in dims)==1 and dims[e['axis']].index(b[e['axis']])-dims[e['axis']].index(a[e['axis']])==1;za,zb=a['scenes']['3'],b['scenes']['3'];eq(e['return3_delta_pp'],zb['net_return_pct']-za['net_return_pct']);eq(e['DD3_delta_pp'],zb['max_drawdown_pct']-za['max_drawdown_pct']);eq(e['sharpe3_delta'],zb['sharpe_365']-za['sharpe_365'])
for row in comp:
 c,y=allby[row['name']],allby[row['reference_name']];a,b=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'];eq(row['return_delta_pp'],a['net_return_pct']-b['net_return_pct']);eq(row['DD_delta_pp'],a['max_drawdown_pct']-b['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],a['recent40']['net_return_pct']-b['recent40']['net_return_pct']);eq(row['cost_delta_usdt'],a['cost_usdt']-b['cost_usdt'])
 if row['reference_kind']=='matched_single_full_gate':assert y['trend_filter_lookback_days']==c['trend_filter_lookback_days'] and y['reversal_return_hurdle']==c['reversal_return_hurdle'] and y['reversal_lookback_days']==c['ETH_A_lookback_days'] and y['ETH_gate_application']=='entries_and_retention'
 elif row['reference_kind']=='matched_single_entry_only':assert y['trend_filter_lookback_days']==c['trend_filter_lookback_days'] and y['reversal_return_hurdle']==c['reversal_return_hurdle'] and y['reversal_lookback_days']==c['ETH_A_lookback_days'] and y['ETH_gate_application']=='entries_only'
 else:assert y['role']=='benchmark'
assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];put(R/'export_verification.json',{'passed':True,'cost_rows':273,'full_folds':3549,'recent_folds':2184,'daily_NAV_rows':60102,'true_4D_edges':135,'comparisons':486,'financial_report_sha256':sha(R/'report.json'),'new_financial_evaluations':0});print('PASS:all273costs/3549folds/2184recentfolds/60102dailyNAV/135four-dimensional edges/486readonlycomparisons exact')
