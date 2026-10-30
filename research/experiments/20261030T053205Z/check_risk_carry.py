import json
from run import ROOT,R,sha,put
W=R/'candidate_observation';read=lambda p:json.loads(p.read_text());point=read(W/'previous_pointer.json');old=read(ROOT/point['state']);state=read(W/'state.json');v=read(R/'candidate_verification.json');assert v['passed'] and v['cumulative_finished_candidate_observations']==117 and v['NAV_points_per_scene']==4696 and v['prior_NAV_prefix']==4574 and v['elapsed_minutes']==4589 and v['new_closed_hour_risk_checks']==6 and v['new_risk_proxy_violations']==0 and v['new_funding_settlements']==v['new_exact_causal_decisions']==v['new_fills']==0
assert state['books']==old['books'] and state['daily']==old['daily']
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  assert len(old['risk'][a][k])==len(state['risk'][a][k])==1 and old['risk'][a][k][0]['t']==1793325600000000000 and state['risk'][a][k][0]['t']==1793332800000000000 and old['risk'][a][k][0]['state']==state['risk'][a][k][0]['state']==state['books'][a][k]
put(R/'risk_carry_verification.json',{'passed':True,'old_state_sha256':point['state_sha256'],'new_state_sha256':sha(W/'state.json'),'only_postfund_positive_duration_exposure_checked':True,'new_closed_hour_risk_checks':6,'new_funding_day_decision_or_fill_events':0,'cash_units_entry_precisely_carried':True,'current04hour_risk_stack':state['risk'],'daily_context_bars':36,'daily_NAV_boundaries':4,'next_funding_utc':'2026-10-30T08:00:00Z','next_daily_decision_utc':'2026-10-31T00:01:00Z'});print('PASS02to04riskcarry,no old funding recredit')
