import csv,json,math
from common import *
from controls import reference
r=json.loads((R/'report.json').read_text());cs={**r['configs']};b=reference();cs[b['name']]=b
read=lambda n:list(csv.DictReader((R/(n+'.csv')).open()))
def eq(text,value):
 if value is None:assert text==''
 elif isinstance(value,bool):assert text==str(value)
 elif isinstance(value,(int,float)):assert abs(float(text)-value)<=1e-12*max(1,abs(value)),(text,value)
 else:assert text==str(value)
expected={'cost_results':30,'walk_forward_folds':390,'recent40_folds':240,'daily_NAV':10017,'sensitivity_edges':12,'reference_comparisons':27}
for n,count in expected.items():assert len(read(n))==count and b'\r' not in (R/(n+'.csv')).read_bytes()
for row in read('cost_results'):
 c=cs[row['name']];k=row['cost_multiplier'];s=c['scenes'][k]
 for key in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','round_trips','executions','cost_usdt','cost_pct_initial','funding_usdt','NAV_points','NAV_sha256_f64le']:eq(row[key],s[key])
 eq(row['gross_plus_funding_to_cost'],s['gross_reference_PnL_to_execution_cost']);eq(row['entry_z'],c['entry_z']);eq(row['exit_z'],c['exit_z']);eq(row['capital_usdt'],20000);eq(row['status'],c['status']);eq(row['recent40_return_pct'],s['recent40']['net_return_pct']);eq(row['recent40_DD_pct'],s['recent40']['max_drawdown_pct']);eq(row['positive_complete30d_folds'],sum(f['net_return_pct']>0 for f in s['folds'][:12]));eq(row['positive_recent5d_folds'],sum(f['net_return_pct']>0 for f in s['recent40']['folds']))
for n,part in [('walk_forward_folds',False),('recent40_folds',True)]:
 for row in read(n):
  s=cs[row['name']]['scenes'][row['cost_multiplier']];z=s['recent40'] if part else s;f=z['folds'][int(row['fold'])-1]
  for key in ['fold','duration_days','start_utc','end_exclusive_utc','net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(row[key],f[key])
for row in read('daily_NAV'):eq(row['NAV_usdt'],cs[row['name']]['scenes'][row['cost_multiplier']]['daily_equity_usdt'][int(row['day_boundary_index'])])
for row in read('sensitivity_edges'):
 a,c=cs[row['from_name']],cs[row['to_name']];axis=row['axis'];values=ENTRIES if axis=='entry_z' else EXITS;assert values.index(c[axis])-values.index(a[axis])==1;eq(row['return_change3_pct'],c['scenes']['3']['net_return_pct']-a['scenes']['3']['net_return_pct']);eq(row['DD_change3_pct'],c['scenes']['3']['max_drawdown_pct']-a['scenes']['3']['max_drawdown_pct']);eq(row['Sharpe_change3'],c['scenes']['3']['sharpe_365']-a['scenes']['3']['sharpe_365'])
for row in read('reference_comparisons'):
 s=cs[row['name']]['scenes'][row['cost_multiplier']];z=b['scenes'][row['cost_multiplier']];assert row['equal_risk_or_notional_match']=='False'
 for key,value in {'new_return_pct':s['net_return_pct'],'reference_return_pct':z['net_return_pct'],'return_difference_pct':s['net_return_pct']-z['net_return_pct'],'new_DD_pct':s['max_drawdown_pct'],'reference_DD_pct':z['max_drawdown_pct'],'new_NAV_points':s['NAV_points'],'reference_original_NAV_points':z['NAV_points']}.items():eq(row[key],value)
put(R/'export_verification.json',{'passed':True,'rows_verified':expected,'all_LF':True,'financial_report_sha256':sha(R/'report.json'),'new_financial_evaluations':0});print('PASS all6CSV numeric cells,dates/counts/NAVhashes and benchmark mismatch labels')
