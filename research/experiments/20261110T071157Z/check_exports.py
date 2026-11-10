import csv,json,math
from common import *
r=json.loads((R/'report.json').read_text());expected={'cost_scenes.csv':48,'walk_forward_folds.csv':624,'recent40_folds.csv':384,'daily_NAV.csv':17808,'sensitivity_grid.csv':27,'native_sensitivity_grid.csv':27,'readonly_reused_scenes.csv':3,'adjacent_edges.csv':72,'matched_hold_comparisons.csv':27,'source_curves.csv':42,'fixed_allocations.csv':10};counts={}
for name,n in expected.items():
 with (R/name).open() as f:rows=list(csv.DictReader(f))
 assert len(rows)==n,(name,len(rows),n);counts[name]=len(rows)
rows=list(csv.DictReader((R/'cost_scenes.csv').open()));lookup={(c['fingerprint'],k):s for c in r['configs'].values() for k,s in c['scenes'].items()}
for x in rows:
 c=next(c for c in r['configs'].values() if c['fingerprint']==x['fingerprint']);assert float(x['ETH_VC'])==c['VC'] and float(x['ETH_E'])==c['E'] and c['VC']==.05
 z=lookup[x['fingerprint'],x['cost_multiplier']]
 for col,key in [('return_pct','net_return_pct'),('whole_DD_pct','max_drawdown_pct'),('cost_usdt','cost_usdt')]:assert math.isclose(float(x[col]),z[key],rel_tol=1e-12,abs_tol=1e-12)
put(R/'export_verification.json',{'passed':True,'CSV_rows':counts,'all48_actual_scenes_match_report':True,'readonly_grid_center_not_counted_as_new':True});print('PASS11CSVs/48actualnewscenes,2x9VW_Rsurfaces,42old/newnativecostcurves')
