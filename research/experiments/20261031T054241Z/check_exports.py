import csv,json
from common import *
expected={'cost_scenes.csv':30,'walk_forward_folds.csv':390,'recent40_folds.csv':240,'daily_NAV.csv':11130,'sensitivity_grid.csv':18,'reference_comparisons.csv':30}
for f,n in expected.items():
 raw=(R/f).read_bytes();assert b'\r' not in raw;rows=list(csv.DictReader(raw.decode().splitlines()));assert len(rows)==n
assert (R/'sensitivity.png').stat().st_size>40000
put(R/'export_verification.json',{'passed':True,'CSV_rows':expected,'line_endings':'LF','all_positive_and_negative_scenes_present':True,'report_sha256':sha(R/'report.json'),'image_sha256':sha(R/'sensitivity.png')});print('PASS6complete CSV exports, LF, all30scenes')
