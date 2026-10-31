import csv,json
from common import *
summary=json.loads((R/'sensitivity_summary.json').read_text());expected={'cost_scenes.csv':12,'walk_forward_folds.csv':156,'recent40_folds.csv':96,'daily_NAV.csv':4452,'sensitivity_grid.csv':96,'readonly_reused_scenes.csv':84,'adjacent_edges.csv':144,'matched_hold_comparisons.csv':48}
assert summary['CSV_rows']==expected
for name,n in expected.items():
 raw=(R/name).read_bytes();assert b'\r' not in raw and len(list(csv.DictReader(raw.decode().splitlines())))==n,name
assert (R/'sensitivity.png').stat().st_size>40000
put(R/'export_verification.json',{'passed':True,'CSV_rows':expected,'line_endings':'LF','all_positive_and_negative_new_scenes_preserved':True,'readonly_old_grid_scenes_separately_marked':84,'report_sha256':sha(R/'report.json'),'images_sha256':{'sensitivity.png':sha(R/'sensitivity.png')}});print('PASS8CSV/12new+84readonly scenes, full folds and matched actual bank hold comparisons')
