"""Both L/H surfaces checked independently; canonical old qualifications immutable."""
import json
from common import *
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());flags=json.loads((R/'edge_flags.json').read_text());recent=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values());old={};out={}
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key]
 for g in grid:
  c=full[g['fingerprint']];ns=[full[h['fingerprint']] for h in grid if (scope=='native' or abs(p['lookbacks'].index(h['L'])-p['lookbacks'].index(g['L']))<=1) and abs(p['entry_notionals'].index(h['N'])-p['entry_notionals'].index(g['N']))<=1];d=c['current_grid_diagnostic_sensitivity'];assert d['neighbor_names']==[x['name'] for x in ns] and d['neighbor_count']==len(ns) and d['local_positive3_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns) and d['local_strict_recent_fraction']==sum(recent(x) for x in ns)/len(ns)
  if g['readonly']:
   ref=p['read_only_references'][g['fingerprint']];o=next(x for x in json.loads((ROOT/ref['report']).read_text())['configs'].values() if x['fingerprint']==g['fingerprint']);assert c['status']==o['status']==ref['status'] and c['criteria']==o['criteria'] and c['sensitivity']==o['sensitivity'];old[g['fingerprint']]={'canonical_status':o['status'],'old_sensitivity_preserved':True,'current_diagnostic_only':d}
 out[scope]={}
 for k in ['1','2','3']:
  vals=[full[g['fingerprint']]['scenes'][k]['sharpe_365'] for g in grid];best=max(vals);out[scope][k]={'positive_Sharpe_cells':sum(x>0 for x in vals),'grid_cells':len(grid),'positive_Sharpe_fraction':sum(x>0 for x in vals)/len(grid),'strict_recent_cells':sum(recent(full[g['fingerprint']]) for g in grid),'maximum_Sharpe':best,'maximum_cells':[{'L':g['L'],'N':g['N'],'H':g['H'],'readonly':g['readonly'],'fingerprint':g['fingerprint'],'at_grid_boundary':g['L'] in [3,5] or g['N'] in [500,750]} for g,x in zip(grid,vals) if x==best],'adjacent_edge_cliff':flags[scope][k]}
put(R/'sensitivity_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'grid':out,'reused_grid_qualifications':old,'scope':'CurrentL/Nnativeandparentdiagnosticsonly;oldcanonicalqualificationsunchanged.','independent_future_verified':False});print(json.dumps({'passed':True,'old_qualifications_preserved':len(old),'grid':out}),flush=True)
