"""Read-only saved-scene attribution; no signal, strategy or account calculation."""
import json,math
from common import *
rep=json.loads((R/'report.json').read_text());guard=sha(R/'report.json');rows=[]
for c in rep['configs'].values():
 old=next(z for z in rep['all_current_grid'].values() if z['scope']==c['scope'] and z['E']==c['E'] and z['H']==.025);assert old['readonly'] and old['capital_usdt']==c['capital_usdt']
 for k,a in c['scenes'].items():
  b=old['scenes'][k];cap=c['capital_usdt'];net=cap*(a['net_return_pct']-b['net_return_pct'])/100;price=a['gross_reference_price_PnL_usdt']-b['gross_reference_price_PnL_usdt'];fund=a['funding_usdt']-b['funding_usdt'];save=b['cost_usdt']-a['cost_usdt'];assert math.isclose(net,price+fund+save,rel_tol=1e-10,abs_tol=1e-8)
  rows.append({'new_configuration':c['name'],'scope':c['scope'],'exit_E':c['E'],'new_H':c['H'],'readonly_comparator':old['fingerprint'],'readonly_H':.025,'cost_multiplier':int(k),'net_change_USDT':net,'reference_price_PnL_change_USDT':price,'funding_change_USDT':fund,'execution_cost_saved_USDT':save,'new_executions':a['executions'],'readonly_executions':b['executions'],'fewer_executions':b['executions']-a['executions'],'new_positive5d':sum(f['net_return_pct']>0 for f in a['recent40']['folds']),'readonly_positive5d':sum(f['net_return_pct']>0 for f in b['recent40']['folds']),'capital_USDT':cap})
assert len(rows)==12 and sha(R/'report.json')==guard
out={'passed':True,'scope':'Derived differences of already actual evaluated scenes only; zero new backtest, weight/parameter/account evaluation, registration or model calls.','financial_report_sha256':guard,'cost_scene_comparisons':len(rows),'all_new_net_changes_negative':all(x['net_change_USDT']<0 for x in rows),'all_execution_cost_changes_savings':all(x['execution_cost_saved_USDT']>0 for x in rows),'fewer_executions_range':[min(x['fewer_executions'] for x in rows),max(x['fewer_executions'] for x in rows)],'rows':rows};put(R/'boundary_attribution.json',out);print(json.dumps({k:v for k,v in out.items() if k!='rows'}),flush=True)
