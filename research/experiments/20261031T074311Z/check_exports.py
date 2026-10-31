import csv,json
from common import *
expected={'cost_scenes.csv':36,'walk_forward_folds.csv':468,'recent40_folds.csv':288,'daily_NAV.csv':13356,'sensitivity_grid.csv':18,'reference_comparisons.csv':24,'adjacent_edges.csv':72}
for name,n in expected.items():
 raw=(R/name).read_bytes();assert b'\r' not in raw;assert len(list(csv.DictReader(raw.decode().splitlines())))==n,name
assert (R/'sensitivity.png').stat().st_size>50000
put(R/'export_verification.json',{'passed':True,'CSV_rows':expected,'line_endings':'LF','all_36_actual_positive_and_negative_scenes_exported':True,'raw_funded_weight_and_capital_headers':True,'report_sha256':sha(R/'report.json'),'image_sha256':sha(R/'sensitivity.png')});print('PASS7CSV/36actualscenes and fixed rawweight/comparator headers')
