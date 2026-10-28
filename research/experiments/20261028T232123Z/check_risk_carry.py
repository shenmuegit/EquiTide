"""Independent 18h to 20h mark-only carried risk-state verification."""
import json
from run import ROOT,R,sha,put
beforepath=ROOT/'research/experiments/20261028T212151Z/candidate_observation/state.json';afterpath=R/'candidate_observation/state.json';before=json.loads(beforepath.read_text());after=json.loads(afterpath.read_text());v=json.loads((R/'candidate_verification.json').read_text());assert v['passed'] and v['window_start_utc']=='2026-10-28T20:30:00Z' and v['cutoff_utc']=='2026-10-28T22:30:00Z' and v['new_funding_settlements']==v['expected_from_actual_settlement_actions']==0
rows=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  old=before['risk'][a][k];new=after['risk'][a][k];assert len(old)==len(new)==1 and old[0]['t']==1793217600000000000 and new[0]['t']==1793224800000000000
  assert old[0]['state']==before['books'][a][k]==after['books'][a][k]==new[0]['state'];rows.append({'asset':a,'cost':k,'source_state_start_ns':old[0]['t'],'current_state_start_ns':new[0]['t'],'signed_units':old[0]['state']['signed_units']})
assert v['new_closed_hour_risk_checks']==6 and v['new_risk_proxy_violations']==0 and v['new_exact_causal_decisions']==v['new_fills']==0
put(R/'risk_carry_verification.json',{'passed':True,'source_state':str(beforepath.relative_to(ROOT)),'source_state_sha256':sha(beforepath),'new_state':str(afterpath.relative_to(ROOT)),'new_state_sha256':sha(afterpath),'carried_states':rows,'expected_BTC_state_hour_checks':6,'actual_independently_checked_state_hours':v['new_closed_hour_risk_checks'],'new_funding_settlements':0,'funding_not_recredited':True,'current22hour_risk_state_carried':True,'new_financial_evaluations':0});print('PASS:all3costs carry20hour at21close and21hour at22close=6BTC checks;ETH flat,no new funding/daydecision/fill;22hourstate carried')
