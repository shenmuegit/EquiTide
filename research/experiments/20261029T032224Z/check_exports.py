"""Read-only validation of every saved export and true within-scope parameter edge."""
import csv,gzip,io,json
from run import R,sha,put,grid_configs,axes
from summarize import all_configs
r=json.loads((R/'report.json').read_text());p=json.loads((R/'plan.json').read_text());allby=all_configs(r,p);grid=grid_configs(r['configs'])
def read(n):return list(csv.DictReader((R/n).open()))
cost,folds,recent,edges,comp=[read(n) for n in ['sensitivity.csv','fold_results.csv','recent40_fold_results.csv','joint_edges.csv','reference_comparisons.csv']];daily=list(csv.DictReader(io.StringIO(gzip.decompress((R/'daily_equity.csv.gz').read_bytes()).decode())));assert list(map(len,[cost,folds,recent,daily,edges,comp]))==[150,1950,1200,40068,92,216]
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
 a,b=grid[e['from']],grid[e['to']];dims=axes(a);assert a['scope']==b['scope']==e['scope'] and sum(a[k]!=b[k] for k in dims)==1 and dims[e['axis']].index(b[e['axis']])-dims[e['axis']].index(a[e['axis']])==1;za,zb=a['scenes']['3'],b['scenes']['3'];eq(e['return3_delta_pp'],zb['net_return_pct']-za['net_return_pct']);eq(e['DD3_delta_pp'],zb['max_drawdown_pct']-za['max_drawdown_pct']);eq(e['sharpe3_delta'],zb['sharpe_365']-za['sharpe_365'])
for row in comp:
 c,y=allby[row['name']],allby[row['reference_name']];a,b=c['scenes'][row['cost_multiplier']],y['scenes'][row['cost_multiplier']];assert y['fingerprint']==row['reference_fingerprint'] and y['status']==row['reference_original_status'] and c['scope']==y['scope'] and c['capital_usdt']==y['capital_usdt'];eq(row['return_delta_pp'],a['net_return_pct']-b['net_return_pct']);eq(row['DD_delta_pp'],a['max_drawdown_pct']-b['max_drawdown_pct']);eq(row['recent40_return_delta_pp'],a['recent40']['net_return_pct']-b['recent40']['net_return_pct']);eq(row['cost_delta_usdt'],a['cost_usdt']-b['cost_usdt'])
 if row['reference_kind']=='matched_old_G0':
  dims=list(axes(c));assert y[dims[0]]==0 and all(c[f]==y[f] for f in dims[1:]) and y['read_only_anchor'] is True
 else:assert y['role']=='benchmark'
assert sha(R/'report.json')==json.loads((R/'verification.json').read_text())['report_sha256'];put(R/'export_verification.json',{'passed':True,'cost_rows':150,'full_folds':1950,'recent_folds':1200,'daily_NAV_rows':40068,'true_3D_edges':92,'comparisons':216,'financial_report_sha256':sha(R/'report.json'),'new_financial_evaluations':0});print('PASS:150costs/1950folds/1200recentfolds/40068dailyNAV/92scope-specific3Dedges/216readonlycomparisons exact')
