"""Read-only originalaccount10:30to12:30continuity,postfundcashandnonewfunding."""
import json
from decimal import Decimal as D
from run import ROOT,R,sha,put
W=R/'candidate_observation';read=lambda p:json.loads(p.read_text());point=read(W/'previous_pointer.json');old=read(ROOT/point['state']);state=read(W/'state.json');v=read(R/'candidate_verification.json');assert v['passed'] and v['cumulative_finished_candidate_observations']==129 and v['NAV_points_per_scene']==5186 and v['prior_NAV_prefix']==5064 and v['elapsed_minutes']==5069 and v['new_funding_settlements']==v['new_exact_causal_decisions']==v['new_fills']==0 and v['new_risk_proxy_violations']==0
assert state['books']==old['books'] and state['daily']==old['daily'];expected=0;details=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  prior=old['books'][a][k];assert old['risk'][a][k]==[{'t':1793354400000000000,'state':prior}] and state['risk'][a][k]==[{'t':1793361600000000000,'state':prior}];checks=2*int(D(prior['signed_units'])!=0);expected+=checks
  assert state['counters'][a][k]['funding_settlements']==old['counters'][a][k]['funding_settlements'] and state['counters'][a][k]['funding_usdt']==old['counters'][a][k]['funding_usdt'];details.append({'asset':a,'cost':k,'two_closed_hour_risk_checks':checks,'cash_units_entry_unchanged':True})
assert expected==6==v['new_closed_hour_risk_checks'];put(R/'risk_carry_verification.json',{'passed':True,'old_state_sha256':point['state_sha256'],'new_state_sha256':sha(W/'state.json'),'new_closed_hour_risk_checks':expected,'new_risk_proxy_violations':0,'new_funding_cashflows':0,'funding08_not_recredited':True,'cash_units_entry_precisely_carried':True,'hour_state_details':details,'current12hour_risk_stack':state['risk'],'daily_context_bars':36,'daily_NAV_boundaries':4,'next_funding_utc':'2026-10-30T16:00:00Z','next_daily_decision_utc':'2026-10-31T00:01:00Z','next_window_policy':'12:30to14:30deriveactualactionsfrompacket;current12houronepostfundstate;never reset/recredit08funding orswitch tonewresearchparameters.'});print('PASS10to12:6riskchecks,cash/q/entry/postfundstate unchanged,zero08fundingrecredit')
