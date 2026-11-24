"""Verify real midnight source and original daily boundaries before any reservation."""
from common import *
rd=lambda p:json.loads(p.read_text());w=rd(R/'account_windows.json');assert not(R/'reserve_batches').exists()
assert {a:len(w[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']}=={'SMA':0,'candidate':0,'l4h02':1,'fewm':1}
assert {a:w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']}=={'SMA':0,'candidate':0,'l4h02':6,'fewm':6}
for n in ['actual08_nov23_prebinding_source.json','actual16_nov23_prebinding_source.json']:
 p=rd(R/n);assert p['passed'] and p['before_any_current_reservation'] and sha(ROOT/p['source'])==p['sha256'] and all(sum(xs.values())==6 for xs in p['prior_unique_counts'].values()) and all(sum(xs.values())==0 for xs in p['expected_current_increment_counts'].values())
p=rd(R/'actual00_nov24_prebinding_source.json');assert p['passed'] and p['before_any_current_reservation'] and p['sha256']=='8a476216d35fbacff319b02e10697418dc4604f5e89c9b9adaa4c07aa1d1647b' and p['first_capture_utc']=='2026-11-24T16:08:09.873310Z' and sha(ROOT/p['source'])==p['sha256'] and all(sum(xs.values())==0 for xs in p['prior_unique_counts'].values())
assert {a:sum(xs.values()) for a,xs in p['expected_current_increment_counts'].items()}=={'candidate':0,'l4h02':6,'fewm':6}
for a in ['l4h02','fewm']:
 assert w[a]['expected_daily_events_utc']==['2026-11-24T00:01:00Z'] and w[a]['next_daily_decision_utc']=='2026-11-25T00:01:00Z'
 assert all(int(z['fundingTime'])*1000000==1795478400001000000 for xs in w[a]['expected_funding_by_asset'].values() for z in xs)
for name in ['observe_l4h02.py','observe_fewm.py','audit_incremental.py']:assert sha(R/name)==sha(ROOT/'research/experiments/20261124T153824Z'/name)
assert rd(R/'SMA_markonly_kernel_identity.json')['passed'];put(R/'boundary_unit_verification.json',{'passed':True,'current_daily_event_counts':{a:len(w[a]['expected_daily_events_utc']) for a in ['SMA','candidate','l4h02','fewm']},'actual_funding_counts':{a:w[a]['expected_funding_records'] for a in ['SMA','candidate','l4h02','fewm']},'exact_actual00_timestamp_ns':'1795478400001000000','source_original_UTC_and_SHA_and_zero_prior_keys_checked':True,'funding_before_daily_by_59999000000_ns':True,'old08_and16_six_each_no_repeat':True,'before_any_current_reservation':True});print('PASSdaily0,0,1,1/funding0,0,6,6/exact00.001originalsourceand0prior/full75SMA')
