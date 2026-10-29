"""Read-only verification that the prior02hour states survive through two closed hours."""
import json
from run import ROOT,R,sha,put
beforepath=ROOT/'research/experiments/20261029T032224Z/candidate_observation/state.json';afterpath=R/'candidate_observation/state.json';before=json.loads(beforepath.read_text());after=json.loads(afterpath.read_text());v=json.loads((R/'candidate_verification.json').read_text())
assert v['passed'] and v['window_start_utc']=='2026-10-29T02:30:00Z' and v['cutoff_utc']=='2026-10-29T04:30:00Z' and v['new_funding_settlements']==v['new_exact_causal_decisions']==v['new_fills']==0
rows=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  old=before['risk'][a][k];new=after['risk'][a][k];assert len(old)==len(new)==1 and old[0]['t']==1793239200000000000 and new[0]['t']==1793246400000000000 and new[0]['state']==old[0]['state']==before['books'][a][k]==after['books'][a][k]
  rows.append({'asset':a,'cost':k,'source02hour_state_count':1,'source02hour_timestamp_ns':old[0]['t'],'current04hour_state_count':1,'current04hour_timestamp_ns':new[0]['t'],'nonzero_position':a=='BTC'})
assert v['new_closed_hour_risk_checks']==6 and v['new_risk_proxy_violations']==0
put(R/'risk_carry_verification.json',{'passed':True,'source_state':str(beforepath.relative_to(ROOT)),'source_state_sha256':sha(beforepath),'new_state':str(afterpath.relative_to(ROOT)),'new_state_sha256':sha(afterpath),'states':rows,'positive_overlap02hour_checked_at03close_and03hour_at04close':True,'expected_BTC_state_hour_checks':6,'actual_independently_checked_state_hours':v['new_closed_hour_risk_checks'],'new_funding_settlements':0,'funding_not_recredited':True,'current04hour_state_carried':True,'new_financial_evaluations':0})
print('PASS:02hour at03close and03hour at04close=6BTC risk checks;current04hour stacks carried;no funding credited or account reset')
