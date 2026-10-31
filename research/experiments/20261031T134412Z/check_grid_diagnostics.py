"""Readonly full-grid diagnostics, separate from immutable old qualifications."""
import json,statistics
from common import *
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());full=r['all_current_grid'];flags=json.loads((R/'edge_flags.json').read_text());out={};olds={}
recent=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values())
for scope,grid in [('native',p['native_grid']),('parent',p['grid'])]:
 out[scope]={}
 for g in grid:
  c=full[g['fingerprint']];ns=[full[h['fingerprint']] for h in grid if abs(h['L']-g['L'])<=1 and abs(p['hurdles'].index(h['H'])-p['hurdles'].index(g['H']))<=1];d=c['current_grid_diagnostic_sensitivity'];assert d['neighbor_names']==[x['name'] for x in ns] and d['neighbor_count']==len(ns) and d['local_positive3_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns) and d['local_strict_recent_fraction']==sum(recent(x) for x in ns)/len(ns)
  if g['readonly']:
   ref=p['read_only_references'][g['fingerprint']];doc=json.loads((ROOT/ref['report']).read_text());old=next(x for x in doc['configs'].values() if x['fingerprint']==g['fingerprint']);assert c['status']==ref['status']==old['status'] and c['criteria']==old['criteria'] and c['sensitivity']==old['sensitivity'];olds[g['fingerprint']]={'L':g['L'],'H':g['H'],'scope':scope,'canonical_status_unchanged':old['status'],'old_sensitivity_preserved':True,'new_grid_diagnostic_only':d}
 for k in ['1','2','3']:
  vals=[full[g['fingerprint']]['scenes'][k]['sharpe_365'] for g in grid];best=max(vals);bestcells=[{'L':g['L'],'H':g['H'],'readonly':g['readonly'],'fingerprint':g['fingerprint'],'at_grid_boundary':g['L'] in [3,5] or g['H'] in [.02,.03]} for g,x in zip(grid,vals) if x==best];out[scope][k]={'positive_Sharpe_cells':sum(x>0 for x in vals),'grid_cells':9,'positive_Sharpe_fraction':sum(x>0 for x in vals)/9,'strictly_over60pct':sum(x>0 for x in vals)/9>.6,'maximum_Sharpe':best,'maximum_cells':bestcells,'adjacent_edge_cliff':flags[scope+'_'+k]}
put(R/'sensitivity_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'scope':'Readonly current outward-grid diagnostics, no new backtest or oldcriteria/status rewrite; actual originals explicitly compared.','grid':out,'reused_grid_qualifications':olds,'independent_future_verified':False,'new_failed_gate_after_results':False});print(json.dumps({'passed':True,'reused_statuses_preserved':len(olds),'new_configs':len(r['configs']),'grid':out}),flush=True)
