"""Current bank-capital/H surface independently checked, old qualifications immutable."""
import json
from common import *
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());full=r['all_current_grid'];flags=json.loads((R/'edge_flags.json').read_text());recent=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values());old={}
for g in p['grid']:
 c=full[g['fingerprint']];ns=[full[h['fingerprint']] for h in p['grid'] if abs(p['BTC_capitals'].index(h['BTC_capital_usdt'])-p['BTC_capitals'].index(g['BTC_capital_usdt']))<=1 and abs(p['fast_hurdles'].index(h['H'])-p['fast_hurdles'].index(g['H']))<=1];d=c['current_grid_diagnostic_sensitivity'];assert d['neighbor_names']==[x['name'] for x in ns] and d['neighbor_count']==len(ns) and d['local_positive3_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns) and d['local_strict_recent_fraction']==sum(recent(x) for x in ns)/len(ns)
 if g['readonly']:
  ref=p['read_only_references'][g['fingerprint']];o=next(x for x in json.loads((ROOT/ref['report']).read_text())['configs'].values() if x['fingerprint']==g['fingerprint']);assert c['status']==o['status']==ref['status'] and c['criteria']==o['criteria'] and c['sensitivity']==o['sensitivity'];old[g['fingerprint']]={'canonical_status':o['status'],'old_sensitivity_preserved':True,'current_diagnostic_only':d}
out={}
for k in ['1','2','3']:
 vals=[full[g['fingerprint']]['scenes'][k]['sharpe_365'] for g in p['grid']];best=max(vals);out[k]={'positive_Sharpe_cells':sum(x>0 for x in vals),'grid_cells':9,'positive_Sharpe_fraction':sum(x>0 for x in vals)/9,'maximum_Sharpe':best,'maximum_cells':[{'BTC_capital_usdt':g['BTC_capital_usdt'],'H':g['H'],'readonly':g['readonly'],'fingerprint':g['fingerprint'],'at_grid_boundary':g['BTC_capital_usdt'] in [2500,5000] or g['H'] in [.02,.03]} for g,x in zip(p['grid'],vals) if x==best],'adjacent_edge_cliff':flags[k]}
put(R/'sensitivity_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'grid':out,'reused_grid_qualifications':old,'scope':'Current3x3capitalmix/H diagnostics only; no oldstatus rewrite;newnativepaths independentlyverified separately.','independent_future_verified':False});print(json.dumps({'passed':True,'old_qualifications_preserved':len(old),'grid':out}),flush=True)
