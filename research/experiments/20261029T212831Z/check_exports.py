"""Verify every exported numeric cell against immutable reports;no new evaluations."""
import csv,gzip,json,math
from datetime import datetime,timedelta,timezone
from run import ROOT,R,sha,put,grid_configs
from controls import load_controls
r=json.loads((R/'report.json').read_text());summary=json.loads((R/'sensitivity_summary.json').read_text());allc={**r['configs'],**{c['name']:c for c in load_controls().values()}}
rows={}
for name,x in summary['exports'].items():
 p=ROOT/x['path'];assert sha(p)==x['sha256'] and b'\r' not in p.read_bytes();rows[name]=list(csv.DictReader(p.open()));assert len(rows[name])==x['rows']
def eq(a,b):assert (a=='' and b is None) or (b is not None and float(a)==float(b)),(a,b)
for z in rows['cost_results']:
 s=allc[z['name']]['scenes'][z['cost_multiplier']];t=s.get('recent40',s.get('extension40'))
 for k in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar','executions','round_trips','cost_usdt','cost_pct_initial','funding_usdt']:eq(z[k],s[k])
 eq(z['gross_plus_funding_to_cost'],s['gross_reference_PnL_to_execution_cost']);assert int(z['positive_complete30d_folds'])==sum(f['net_return_pct']>0 for f in s['folds'][:12]);eq(z['recent_return_pct'],t['net_return_pct']);eq(z['recent_DD_pct'],t['max_drawdown_pct']);assert int(z['recent_positive_folds'])==sum(f['net_return_pct']>0 for f in t['folds']) and z['NAV_sha256_f64le']==s['NAV_sha256_f64le']
for typ in ['walk_forward_folds','recent40_folds']:
 for z in rows[typ]:
  s=allc[z['name']]['scenes'][z['cost_multiplier']]
  if typ=='recent40_folds':s=s.get('recent40',s.get('extension40'))
  f=s['folds'][int(z['fold'])-1];start=f.get('start_utc') or (datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*(f['fold']-1))).isoformat().replace('+00:00','Z');end=f.get('end_exclusive_utc') or (datetime(2026,9,14,0,1,tzinfo=timezone.utc)+timedelta(days=5*f['fold'])).isoformat().replace('+00:00','Z');assert z['start_utc']==start and z['end_exclusive_utc']==end and int(z['duration_days'])==f['duration_days']
  for k in ['net_return_pct','max_drawdown_pct','sharpe_365','calmar']:eq(z[k],f[k])
for z in rows['daily_NAV']:eq(z['NAV_usdt'],r['configs'][z['name']]['scenes'][z['cost_multiplier']]['daily_equity_usdt'][int(z['day_boundary_index'])])
for z in rows['reference_comparisons']:
 a=allc[z['name']]['scenes'][z['cost_multiplier']];b=allc[z['reference_name']]['scenes'][z['cost_multiplier']];ta,tb=a.get('recent40',a.get('extension40')),b.get('recent40',b.get('extension40'))
 for k,val in [('return_pct',a['net_return_pct']),('reference_return_pct',b['net_return_pct']),('delta_return_pp',a['net_return_pct']-b['net_return_pct']),('DD_pct',a['max_drawdown_pct']),('reference_DD_pct',b['max_drawdown_pct']),('recent_return_pct',ta['net_return_pct']),('reference_recent_return_pct',tb['net_return_pct']),('recent_delta_pp',ta['net_return_pct']-tb['net_return_pct'])]:eq(z[k],val)
for z in rows['sensitivity_edges']:
 a,b=[allc[z[k]]['scenes']['3'] for k in ['left','right']]
 for k,val in [('full_return_delta_pp',b['net_return_pct']-a['net_return_pct']),('DD_delta_pp',b['max_drawdown_pct']-a['max_drawdown_pct']),('Sharpe_delta',None if a['sharpe_365'] is None or b['sharpe_365'] is None else b['sharpe_365']-a['sharpe_365']),('Calmar_delta',None if a['calmar'] is None or b['calmar'] is None else b['calmar']-a['calmar']),('recent_return_delta_pp',b['recent40']['net_return_pct']-a['recent40']['net_return_pct'])]:eq(z[k],val)
out={'passed':True,'financial_report_sha256':sha(R/'report.json'),'all_LF':True,'rows_verified':{k:len(v) for k,v in rows.items()},'new_evaluations':0};put(R/'export_verification.json',out);print(json.dumps(out))
