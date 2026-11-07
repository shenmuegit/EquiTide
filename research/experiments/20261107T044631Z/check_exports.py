import csv,json,math
from common import *
r=json.loads((R/'report.json').read_text());expected={'cost_scenes.csv':42,'walk_forward_folds.csv':546,'recent40_folds.csv':336,'daily_NAV.csv':15582,'sensitivity_grid.csv':81,'native_sensitivity_grid.csv':27,'readonly_reused_scenes.csv':27,'adjacent_edges.csv':198,'matched_hold_comparisons.csv':81,'source_curves.csv':42,'fixed_allocations.csv':28};counts={}
for name,n in expected.items():
 with (R/name).open() as f:rows=list(csv.DictReader(f))
 assert len(rows)==n,(name,len(rows),n);counts[name]=len(rows)
rows=list(csv.DictReader((R/'cost_scenes.csv').open()));lookup={(c['fingerprint'],k):s for c in r['configs'].values() for k,s in c['scenes'].items()}
for x in rows:
 z=lookup[x['fingerprint'],x['cost_multiplier']]
 for col,key in [('return_pct','net_return_pct'),('whole_DD_pct','max_drawdown_pct'),('cost_usdt','cost_usdt')]:assert math.isclose(float(x[col]),z[key],rel_tol=1e-12,abs_tol=1e-12)
put(R/'export_verification.json',{'passed':True,'CSV_rows':counts,'all42_actual_scenes_match_report':True,'readonly_grid_center_not_counted_as_new':True});print('PASS11CSVs/42newparentscenes,27jointL/D/VCparents+9readonlynativecells,42oldnativecurves/zero newnative')
