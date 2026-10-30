import csv,json
from common import *
r=json.loads((R/'report.json').read_text());cs=list(r['configs'].values());counts=json.loads((R/'export_counts.json').read_text());files=['cost_results','walk_forward_folds','recent40_folds','daily_NAV','matched_capital_comparisons'];tables={name:list(csv.DictReader((R/(name+'.csv')).open())) for name in files};assert all(len(tables[n])==counts[n] for n in files);near=lambda a,b:abs(float(a)-float(b))<=1e-11*max(1,abs(float(a)),abs(float(b)))
for x in tables['cost_results']:
 c=r['configs'][x['name']];z=c['scenes'][x['cost_multiplier']]
 for key,field in [('net_return_pct','net_return_pct'),('whole_curve_drawdown_pct','max_drawdown_pct'),('cost_usdt','cost_usdt'),('funding_usdt','funding_usdt'),('gross_reference_price_PnL_usdt','gross_reference_price_PnL_usdt'),('initial_capital_usdt','initial_capital_usdt')]:assert near(x[key],z[field])
 assert x['NAV_sha256_f64le']==z['NAV_sha256_f64le'] and x['status']==c['status'] and x['failed_criteria']=='|'.join(c['failed_criteria'])
for table,key in [('walk_forward_folds','folds'),('recent40_folds','recent40')]:
 for x in tables[table]:
  z=r['configs'][x['name']]['scenes'][x['cost_multiplier']];f=(z['folds'] if key=='folds' else z['recent40']['folds'])[int(x['fold'])-1]
  for field,v in f.items():assert (x[field]=='' if v is None else x[field]==v if isinstance(v,str) else near(x[field],v))
for x in tables['daily_NAV']:assert near(x['equity_usdt'],r['configs'][x['name']]['scenes'][x['cost_multiplier']]['daily_equity_usdt'][int(x['day'])])
for x in tables['matched_capital_comparisons']:
 a=r['configs'][x['name']];b=r['configs'][x['matchedcapital_comparator']];k=x['cost_multiplier'];assert a['capital_usdt']==b['capital_usdt']==float(x['same_initial_capital_usdt']);assert near(x['candidate_minus_cash_return_percentage_points'],a['scenes'][k]['net_return_pct']-b['scenes'][k]['net_return_pct']);assert near(x['candidate_minus_cash_wholeDD_percentage_points'],a['scenes'][k]['max_drawdown_pct']-b['scenes'][k]['max_drawdown_pct'])
assert (R/'sensitivity.png').stat().st_size>30000;put(R/'export_verification.json',{'passed':True,'counts':{k:len(v) for k,v in tables.items()},'every_export_numeric_row_checked':True,'sensitivity_plot_sha256':sha(R/'sensitivity.png')});print('PASS all5 CSV tables and image artifact')
