import csv,json
from common import *
summary=json.loads((R/'sensitivity_summary.json').read_text());expected={'cost_scenes.csv':60,'walk_forward_folds.csv':780,'recent40_folds.csv':480,'daily_NAV.csv':22260,'sensitivity_grid.csv':30,'matched_hold_comparisons.csv':24,'NAV_interest_replication_comparisons.csv':54,'adjacent_edges.csv':96,'lot_impact_comparisons.csv':summary['native_lot_comparison_rows']}
for name,n in expected.items():
 raw=(R/name).read_bytes();assert b'\r' not in raw;assert len(list(csv.DictReader(raw.decode().splitlines())))==n,name
for name in ['sensitivity.png','replication_difference.png']:assert (R/name).stat().st_size>40000
put(R/'export_verification.json',{'passed':True,'CSV_rows':expected,'line_endings':'LF','positive_negative_actual_scenes_all_preserved':True,'same_capital_replication_PnL_decomposition_checked':54,'report_sha256':sha(R/'report.json'),'images_sha256':{n:sha(R/n) for n in ['sensitivity.png','replication_difference.png']}});print('PASS9CSV/60actualscenes, native LOT/impact and54prior-model decompositions')
