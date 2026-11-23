"""Classify actual saved adjacency coordinates and warnings without changing any gate."""
from common import *
import csv
rd=lambda p:json.loads(p.read_text());r=rd(R/'report.json');before=sha(R/'report.json');ex=rd(R/'export_verification.json');grid={c['name']:c for c in r['all_current_grid'].values()};rows=[]
def identify(z):
 a,b=grid[z['from']],grid[z['to']];axis='BTC_ENTRY_TARGET_USDT' if a['W']!=b['W'] and a['K']==b['K'] else 'ETH_ENTRY_VOLATILITY_DAYS' if a['W']==b['W'] and a['K']!=b['K'] else None;assert axis;return {**z,'actual_axis':axis,'from_BTC_N':a['W'],'to_BTC_N':b['W'],'from_ETH_entry_V':a['K'],'to_ETH_entry_V':b['K']}
for z in csv.DictReader((R/'exports/adjacent_sensitivity_edges.csv').open()):rows.append(identify(z))
assert len(rows)==12;warnings=[identify(z) for z in ex['cliffs_over_two_std']];assert all(any(z['from']==v['from'] and z['to']==v['to'] for v in rows) for z in warnings)
assert sha(R/'report.json')==before;put(R/'sensitivity_axis_review.json',{'passed':True,'recorded_utc':now(),'report_sha256_unchanged':before,'rows':rows,'cliff_warning_rows':warnings,'warning_count':len(warnings),'warning_counts_by_axis':{a:sum(z['actual_axis']==a for z in warnings) for a in ['BTC_ENTRY_TARGET_USDT','ETH_ENTRY_VOLATILITY_DAYS']},'heuristic_two_std_not_statistical_significance':True,'preset_unchanged':rd(R/'plan.json')['representative_preset'],'saved_evidence_only_no_financial_or_account_execution':True});print(json.dumps({'passed':True,'edges':len(rows),'warnings':len(warnings),'warning_axes':[z['actual_axis'] for z in warnings]}))
