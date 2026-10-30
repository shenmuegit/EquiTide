import csv,json
from common import *
r=json.loads((R/'report.json').read_text());counts=json.loads((R/'export_counts.json').read_text());names=['cost_results','walk_forward_folds','recent40_folds','daily_NAV','reference_comparisons','sensitivity_edges'];tables={n:list(csv.DictReader((R/(n+'.csv')).open())) for n in names};assert all(len(tables[n])==counts[n] and b'\r' not in (R/(n+'.csv')).read_bytes() for n in names);near=lambda a,b:abs(float(a)-float(b))<=1e-11*max(1,abs(float(a)),abs(float(b)))
for x in tables['cost_results']:
 c=r['configs'][x['name']];z=c['scenes'][x['cost_multiplier']]
 for a,b in [('net_return_pct','net_return_pct'),('whole_curve_drawdown_pct','max_drawdown_pct'),('cost_usdt','cost_usdt'),('funding_usdt','funding_usdt'),('gross_reference_price_PnL_usdt','gross_reference_price_PnL_usdt'),('completed_pair_round_trips','round_trips')]:assert near(x[a],z[b])
 assert x['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and x['status']==c['status'] and x['failed_criteria']=='|'.join(c['failed_criteria'])
for tab in ['walk_forward_folds','recent40_folds']:
 for x in tables[tab]:
  z=r['configs'][x['name']]['scenes'][x['cost_multiplier']];f=(z['folds'] if tab=='walk_forward_folds' else z['recent40']['folds'])[int(x['fold'])-1]
  for k,v in f.items():assert (x[k]=='' if v is None else x[k]==v if isinstance(v,str) else near(x[k],v))
for x in tables['daily_NAV']:assert near(x['equity_usdt'],r['configs'][x['name']]['scenes'][x['cost_multiplier']]['daily_equity_usdt'][int(x['day'])])
for x in tables['reference_comparisons']:
 z=r['configs'][x['name']]['scenes'][x['cost_multiplier']];b=r['read_only_reference_results'][x['readonly_benchmark_fingerprint']]['original_config']['scenes'][x['cost_multiplier']];assert near(x['return_difference_percentage_points'],z['net_return_pct']-b['net_return_pct']) and near(x['wholeDD_difference_percentage_points'],z['max_drawdown_pct']-b['max_drawdown_pct'])
for x in tables['sensitivity_edges']:
 a=r['configs'][x['left']]['scenes'][x['cost_multiplier']];b=r['configs'][x['right']]['scenes'][x['cost_multiplier']];assert near(x['absolute_return_difference_percentage_points'],abs(a['net_return_pct']-b['net_return_pct'])) and near(x['absolute_sharpe_difference'],abs(a['sharpe_365']-b['sharpe_365'])) and near(x['absolute_wholeDD_difference_percentage_points'],abs(a['max_drawdown_pct']-b['max_drawdown_pct']))
assert (R/'sensitivity.png').stat().st_size>30000;put(R/'export_verification.json',{'passed':True,'CSV_files':6,'all_LF':True,'counts':{n:len(t) for n,t in tables.items()},'all_rows_checked':True,'image_sha256':sha(R/'sensitivity.png')});print('PASS6 CSV tables/allrows/LF/imageartifact')
