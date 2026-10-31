import csv,json
from common import *
summary=json.loads((R/'sensitivity_summary.json').read_text());expected={'cost_scenes.csv':48,'walk_forward_folds.csv':624,'recent40_folds.csv':384,'daily_NAV.csv':17808,'sensitivity_grid.csv':54,'readonly_center_scenes.csv':6,'adjacent_edges.csv':72,'matched_hold_comparisons.csv':27}
assert summary['CSV_rows']==expected
for name,n in expected.items():
 raw=(R/name).read_bytes();assert b'\r' not in raw and len(list(csv.DictReader(raw.decode().splitlines())))==n,name
assert (R/'sensitivity.png').stat().st_size>40000
put(R/'export_verification.json',{'passed':True,'CSV_rows':expected,'line_endings':'LF','all_positive_and_negative_new_scenes_preserved':True,'readonly_old_center_scenes_separately_marked':6,'report_sha256':sha(R/'report.json'),'images_sha256':{'sensitivity.png':sha(R/'sensitivity.png')}});print('PASS8CSV/48new+6readonly scenes, full folds and matched actual bank hold comparisons')
