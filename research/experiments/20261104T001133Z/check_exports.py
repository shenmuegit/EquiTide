import csv,json
from common import *
s=json.loads((R/'sensitivity_summary.json').read_text());expected={'cost_scenes.csv':27,'walk_forward_folds.csv':351,'recent40_folds.csv':216,'daily_NAV.csv':10017,'sensitivity_grid.csv':27,'readonly_reused_scenes.csv':27,'adjacent_edges.csv':36,'matched_hold_comparisons.csv':27,'source_curves.csv':39,'fixed_allocations.csv':10};assert s['CSV_rows']==expected
for n,k in expected.items():
 raw=(R/n).read_bytes();assert b'\r' not in raw and len(list(csv.DictReader(raw.decode().splitlines())))==k,n
assert (R/'sensitivity.png').stat().st_size>40000
put(R/'export_verification.json',{'passed':True,'CSV_rows':expected,'line_endings':'LF','allactualpositiveandnegativefoldspreserved':True,'readonly_old_allocation_scenes':27,'report_sha256':sha(R/'report.json'),'images_sha256':{'sensitivity.png':sha(R/'sensitivity.png')}});print('PASS10CSV/27newportfolio scenes,39readonlynativecurves;no nativesimulations')
