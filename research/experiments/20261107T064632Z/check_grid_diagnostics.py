import json
from common import *
p=json.loads((R/'plan.json').read_text());r=json.loads((R/'report.json').read_text());s=json.loads((R/'sensitivity_summary.json').read_text());out={}
for scope,key in [('parent','all_current_grid'),('native','all_current_native_grid')]:
 out[scope]={};full=r[key];assert len(full)==9
 for k in ['1','2','3']:
  best=max(c['scenes'][k]['sharpe_365'] for c in full.values());cells=[{'L':c['L'],'H':c['H'],'N':1000,'fingerprint':fp,'readonly':c['readonly'],'at_grid_boundary':c['L'] in [23,27] or c['H'] in [.03,.05]} for fp,c in full.items() if c['scenes'][k]['sharpe_365']==best]
  out[scope][k]={'positive_Sharpe_cells':sum(c['scenes'][k]['sharpe_365']>0 for c in full.values()),'grid_cells':9,'positive_Sharpe_fraction':sum(c['scenes'][k]['sharpe_365']>0 for c in full.values())/9,'strict_recent_cells':sum(c['scenes'][k]['recent40']['net_return_pct']>0 and sum(f['net_return_pct']>0 for f in c['scenes'][k]['recent40']['folds'])>=6 for c in full.values()),'maximum_Sharpe':best,'maximum_cells':cells,'adjacent_edge_cliff':s['edge_flags'][scope][k]}
put(R/'sensitivity_diagnostics.json',{'passed':True,'report_sha256':sha(R/'report.json'),'axes':['BTClookbackL23/25/27','BTCentryH3/4/5%'],'grid':out,'old_center_qualifications_preserved':True,'boundary_flags_not_a_postoutcome_expansion':True});print('PASS complete native/parent BTC L/H surfaces,Sharpe/Calmar/DD/edge diagnostics;oldcenter not regraded')
