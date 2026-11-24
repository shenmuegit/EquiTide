"""Verify completed prior actual16 counts and exact own coverage before any reservation."""
from common import *
rd=lambda p:json.loads(p.read_text());w=rd(R/'account_windows.json');assert not(R/'reserve_batches').exists()
assert all(not w[a]['expected_daily_events_utc'] and w[a]['next_daily_decision_utc']=='2026-11-24T00:01:00Z' for a in ['SMA','candidate','l4h02','fewm'])
assert {a:w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']}=={'SMA':0,'candidate':0,'l4h02':0,'fewm':0}
old=rd(R/'actual08_nov23_prebinding_source.json');pre=rd(R/'actual16_nov23_prebinding_source.json');assert old['passed'] and pre['passed'] and pre['before_any_current_reservation'] and sha(ROOT/pre['source'])==pre['sha256'] and pre['first_capture_utc']=='2026-11-24T08:05:12.897402Z'
assert {a:sum(xs.values()) for a,xs in pre['prior_unique_counts'].items()}=={'candidate':6,'l4h02':6,'fewm':6} and {a:sum(xs.values()) for a,xs in pre['expected_current_increment_counts'].items()}=={'candidate':0,'l4h02':0,'fewm':0}
assert all(sum(xs.values())==6 for xs in old['prior_unique_counts'].values()) and all(sum(xs.values())==0 for xs in old['expected_current_increment_counts'].values())
for name in ['observe_l4h02.py','observe_fewm.py','audit_incremental.py']:assert sha(R/name)==sha(ROOT/'research/experiments/20261124T113752Z'/name)
assert rd(R/'SMA_markonly_kernel_identity.json')['passed'];put(R/'boundary_unit_verification.json',{'passed':True,'new_daily_decisions_expected':0,'actual_funding_counts':{a:w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']},'exact_first_actual16_timestamp_ns':'1795449600000000000','original_first_capture_UTC_and_fields_retained':True,'old08_six_each_no_repeat':True,'before_any_current_reservation':True});print('PASSdaily0/ownfund0,0,0,0/exact16firstsource/all-six-priorcounts/full75')
