"""Independent three-axis neighborhood checks; old canonical qualifications immutable."""
import json
from common import *
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());flags=json.loads((R/'edge_flags.json').read_text());recent=lambda c:all(s['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in s['recent40']['folds'])>=6 for s in c['scenes'].values());old={};out={}
for scope,grid,key in [('parent',p['grid'],'all_current_grid'),('native',p['native_grid'],'all_current_native_grid')]:
 full=r[key]
 for g in grid:
  c=full[g['fingerprint']];ns=[full[h['fingerprint']] for h in grid if abs(p['slope_lags'].index(h['D'])-p['slope_lags'].index(g['D']))<=1 and abs(p['volatility_ceilings'].index(h['VC'])-p['volatility_ceilings'].index(g['VC']))<=1 and (scope=='native' or abs(p['BTC_lookbacks'].index(h['BTC_L'])-p['BTC_lookbacks'].index(g['BTC_L']))<=1)];d=c['current_grid_diagnostic_sensitivity'];assert d['neighbor_names']==[x['name'] for x in ns] and d['neighbor_count']==len(ns) and d['local_positive3_fraction']==sum(x['scenes']['3']['net_return_pct']>0 for x in ns)/len(ns) and d['local_strict_recent_fraction']==sum(recent(x) for x in ns)/len(ns)
  if g['readonly']:
   ref=p['read_only_references'][g['fingerprint']];o=next(x for x in json.loads((ROOT/ref['report']).read_text())['configs'].values() if x['fingerprint']==g['fingerprint']);assert c['status']==o['status']==ref['status'] and c['criteria']==o['criteria'] and c['sensitivity']==o['sensitivity'];old[g['fingerprint']]={'canonical_status':o['status'],'old_sensitivity_preserved':True,'current_diagnostic_only':d}
 out[scope]={}
 for k in ['1','2','3']:
  vals=[full[g['fingerprint']]['scenes'][k]['sharpe_365'] for g in grid];best=max(vals);cells=[]
  for g,x in zip(grid,vals):
   if x==best:cells.append({**{key:g[key] for key in ['N','L','S','K','VC','D','E','H','readonly','fingerprint']},'BTC_L':g.get('BTC_L'),'at_grid_boundary':g['D'] in [6,8] or g['VC'] in [.04,.05] or scope=='parent' and g['BTC_L'] in [27,31]})
  out[scope][k]={'positive_Sharpe_cells':sum(x>0 for x in vals),'grid_cells':len(grid),'positive_Sharpe_fraction':sum(x>0 for x in vals)/len(grid),'strict_recent_cells':sum(recent(full[g['fingerprint']]) for g in grid),'maximum_Sharpe':best,'maximum_cells':cells,'adjacent_edge_cliff':flags[scope][k]}
assert len(old)==21
put(R/'sensitivity_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'grid':out,'reused_grid_qualifications':old,'scope':'Current joint BTC_L/ETH_D/VC parent and readonly ETH_D/VC diagnostics only; original canonical qualifications unchanged.','independent_future_verified':False});print(json.dumps({'passed':True,'old_qualifications_preserved':len(old),'grid':out}),flush=True)
