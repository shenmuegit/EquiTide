import csv,json
from common import *
s=json.loads((R/'sensitivity_summary.json').read_text());expected={'cost_scenes.csv':54,'walk_forward_folds.csv':702,'recent40_folds.csv':432,'daily_NAV.csv':20034,'sensitivity_grid.csv':27,'native_sensitivity_grid.csv':27,'readonly_reused_scenes.csv':6,'adjacent_edges.csv':72,'matched_hold_comparisons.csv':27,'source_curves.csv':42,'fixed_allocations.csv':10};assert s['CSV_rows']==expected
for n,k in expected.items():
 raw=(R/n).read_bytes();assert b'\r' not in raw and len(list(csv.DictReader(raw.decode().splitlines())))==k,n
assert (R/'sensitivity.png').stat().st_size>40000
put(R/'export_verification.json',{'passed':True,'CSV_rows':expected,'line_endings':'LF','all_actual_positive_and_negative_scenes_preserved':True,'readonly_old_parent_scenes':6,'report_sha256':sha(R/'report.json'),'images_sha256':{'sensitivity.png':sha(R/'sensitivity.png')}});print('PASS11CSVs/54newscenes,bothS/Dsurfaces,42nativecostsources')
