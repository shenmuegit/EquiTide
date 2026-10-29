"""Read-only carried12/13hour verification;no new funding or account reset."""
import json
from run import ROOT,R,sha,put
beforepath=ROOT/'research/experiments/20261029T132528Z/candidate_observation/state.json';afterpath=R/'candidate_observation/state.json';before=json.loads(beforepath.read_text());after=json.loads(afterpath.read_text());v=json.loads((R/'candidate_verification.json').read_text());assert v['passed'] and v['window_start_utc']=='2026-10-29T12:30:00Z' and v['cutoff_utc']=='2026-10-29T14:30:00Z' and v['new_funding_settlements']==v['new_exact_causal_decisions']==v['new_fills']==0
rows=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  old=before['risk'][a][k];new=after['risk'][a][k];assert len(old)==len(new)==1 and old[0]['t']==1793275200000000000 and new[0]['t']==1793282400000000000 and new[0]['state']==old[0]['state']==before['books'][a][k]==after['books'][a][k]
  rows.append({'asset':a,'cost':k,'source12hour_state_count':1,'current14hour_state_count':1,'source_time_ns':old[0]['t'],'current_time_ns':new[0]['t'],'nonzero_position':a=='BTC'})
assert v['new_closed_hour_risk_checks']==6 and v['new_risk_proxy_violations']==0
put(R/'risk_carry_verification.json',{'passed':True,'source_state':str(beforepath.relative_to(ROOT)),'source_state_sha256':sha(beforepath),'new_state':str(afterpath.relative_to(ROOT)),'new_state_sha256':sha(afterpath),'states':rows,'12hour_checked_at13close_and13hour_at14close':True,'expected_BTC_state_hour_checks':6,'actual_independently_checked_state_hours':v['new_closed_hour_risk_checks'],'new_funding_settlements':0,'08funding_not_recredited':True,'current14hour_state_carried':True,'new_financial_evaluations':0});print('PASS:12hourat13close and13hourat14close=6BTC checks;current14hour state carried;no funding duplicate or reset')
