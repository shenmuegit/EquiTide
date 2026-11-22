"""Legacy H filename: compare saved M2/3/5 outcomes with preregistered old M4 controls."""
from common import *
import csv
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');r=rd(R/'report.json');before=sha(R/'report.json');rows=[]
for c in r['configs'].values():
 z=p['additional_predeclared_M4_report_controls'][str(c['W'])]
 for key in ['spec','report','archive']:assert sha(ROOT/z[key])==z[key+'_sha256']
 old=next(x for x in rd(ROOT/z['report'])['configs'].values() if x['fingerprint']==z['fingerprint']);q=rd(ROOT/c['spec'])['parameters'];assert q['ETH_trend_lookback_days']==16 and q['ETH_entry_funding_volatility_ratio']==.0075 and q['ETH_entry_funding_budget_volatility_window_days']==9 and q['ETH_trend_slope_lag_days']==3 and q['ETH_entry_funding_settlement_count']==c['K'] in [2,3,5] and q['ETH_entry_funding_max_age_hours']==36 and sorted(old['source_fingerprints'])==sorted(z['source_fingerprints'])
 for k,s in c['scenes'].items():
  o=old['scenes'][k];rows.append({'fingerprint':c['fingerprint'],'prior_fingerprint':old['fingerprint'],'BTC_N':c['W'],'ETH_S':16,'ETH_M':c['K'],'cost':int(k),'new_mature_settlement_count':c['K'],'old_mature_settlement_count':4,'new_return_pct':s['net_return_pct'],'old_return_pct':o['net_return_pct'],'return_difference_pp':s['net_return_pct']-o['net_return_pct'],'DD_difference_pp':s['max_drawdown_pct']-o['max_drawdown_pct'],'Sharpe_difference':s['sharpe_365']-o['sharpe_365'],'Calmar_difference':s['calmar']-o['calmar'],'same_full_NAV':s['NAV_sha256_f64le']==o['NAV_sha256_f64le']})
f=R/'exports/previous_M4_comparisons.csv'
with f.open('w',newline='') as out:w=csv.DictWriter(out,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
assert sha(R/'report.json')==before
put(R/'previous_H_comparison.json',{'passed':True,'recorded_utc':now(),'completed_report_sha256_unchanged':before,'predeclared_old_M4_controls':p['additional_predeclared_M4_report_controls'],'rows':rows,'CSV':rel(f),'CSV_sha256':sha(f),'saved_actual_results_only':True,'no_financial_or_account_reexecution':True});print('PASS18savedM4matchedcomparisons;0modeloraccountreexecution')
