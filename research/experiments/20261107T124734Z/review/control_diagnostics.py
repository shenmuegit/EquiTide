"""Read-only matched-exit old H3% comparison, not a new qualification gate."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());p=rd(R/'plan.json');r=rd(R/'report.json');rows=[]
for c in r['configs'].values():
 key='all_current_native_grid' if c['scope']=='native' else 'all_current_grid';old=next(z for z in r[key].values() if z['H']==.03 and z['E']==c['E'] and z['L']==29);s={}
 for k,z in c['scenes'].items():
  q=old['scenes'][k];s[k]={'return_pct':z['net_return_pct'],'old_return_pct':q['net_return_pct'],'return_delta_pp':z['net_return_pct']-q['net_return_pct'],'whole_DD_pct':z['max_drawdown_pct'],'old_whole_DD_pct':q['max_drawdown_pct'],'execution_cost_usdt':z['cost_usdt'],'old_execution_cost_usdt':q['cost_usdt'],'executions':z['executions'],'old_executions':q['executions'],'old_dominates_return_and_DD':q['net_return_pct']>=z['net_return_pct'] and q['max_drawdown_pct']<=z['max_drawdown_pct']}
 rows.append({'name':c['name'],'fingerprint':c['fingerprint'],'scope':c['scope'],'BTC_L':c['L'],'BTC_H':c['H'],'BTC_E':c['E'],'oldH3_same_E_fingerprint':old['fingerprint'],'status':c['status'],'local_strict_recent_fraction':c['sensitivity']['local_recent_allcost_qualifying_fraction'],'cost_comparisons':s})
put(R/'relative_control_diagnostic.json',{'passed':True,'report_sha256':sha(R/'report.json'),'rows':rows,'summary':{'new_rows':len(rows),'new_parent_passes':len(r['summary']['passed']),'all_new_rejected':all(z['status']=='rejected' for z in rows),'rows_dominated_by_old_same_E_at_allcosts':sum(all(z['old_dominates_return_and_DD'] for z in x['cost_comparisons'].values()) for x in rows)},'scope':'Posthoc descriptive matched-E oldH3 controls only. Oldreport/statuses and frozen currentgates unchanged; not independentfuture or new strategy trial.'});print('PASS12currentresults vs exact same-E oldH3 controls;no gate/status change')
