"""Classify saved adjacency pairs from actual grid coordinates; CSV has no axis column."""
from common import *
import csv
rd=lambda p:json.loads(p.read_text());r=rd(R/'report.json');before=sha(R/'report.json');ex=rd(R/'export_verification.json');grid={c['name']:c for c in r['all_current_grid'].values()};rows=[]
for z in csv.DictReader((R/'exports/adjacent_sensitivity_edges.csv').open()):
 a,b=grid[z['from']],grid[z['to']];axis='BTC_ENTRY_TARGET_USDT' if a['W']!=b['W'] and a['K']==b['K'] else 'ETH_EXIT_BUFFER_FRACTION' if a['W']==b['W'] and a['K']!=b['K'] else None;assert axis;rows.append({**z,'actual_axis':axis,'from_BTC_N':a['W'],'to_BTC_N':b['W'],'from_ETH_E':a['K'],'to_ETH_E':b['K']})
assert len(rows)==12;warnings=[]
for z in ex['cliffs_over_two_std']:
 a,b=grid[z['from']],grid[z['to']];assert a['W']!=b['W'] and a['K']==b['K'];warnings.append({**z,'actual_axis':'BTC_ENTRY_TARGET_USDT','warning_repeats_same_two_amounts_at_three_E_levels':True})
assert len(warnings)==3
for z in rows:
 if z['actual_axis']=='ETH_EXIT_BUFFER_FRACTION':assert all(float(z[k])==0 for k in ['delta_net_pp','delta_sharpe','delta_DD_pp','delta_Calmar'])
assert sha(R/'report.json')==before;put(R/'sensitivity_axis_review.json',{'passed':True,'report_sha256_unchanged':before,'rows':rows,'cliff_warning_rows':warnings,'ETH_exit_buffer_all_neighbor_metric_differences_zero':True,'three_warnings_share_one_BTC_amount_step_not_independent_findings':True,'saved_evidence_only_no_financial_or_account_execution':True})
f=rd(R/'read_failures.json');f['facts'].append({'native_chunk':'6905bf','actual_exit_code':1,'operation':'Read-only CSV inspection assumed nonexistent axis column','actual_stderr':"KeyError: 'axis'",'resolved':True,'resolution':'Actual stored columns are scope/from/to/deltas. Corrected read-only classification uses saved grid W/K and verifies all12edges, all3BTCwarningrows and zeroEedge differences.','effective_evidence':rel(R/'sensitivity_axis_review.json'),'financial_report_unchanged_sha256':before});put(R/'read_failures.json',f);print('PASS12savededges classified by W/K;three warnings are sameBTCstep, allEneighbor deltas0;0reruns')
