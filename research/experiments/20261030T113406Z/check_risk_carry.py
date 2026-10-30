"""Verify1msoldprefundingexposureactuallycheckedinclosed08hour,withoutrecreditingfunding/cash."""
import json
from decimal import Decimal as D
from run import ROOT,R,sha,put
W=R/'candidate_observation';read=lambda p:json.loads(p.read_text());point=read(W/'previous_pointer.json');old=read(ROOT/point['state']);state=read(W/'state.json');v=read(R/'candidate_verification.json');assert v['passed'] and v['cumulative_finished_candidate_observations']==126 and v['NAV_points_per_scene']==5064 and v['prior_NAV_prefix']==4942 and v['elapsed_minutes']==4949 and v['new_funding_settlements']==v['new_exact_causal_decisions']==v['new_fills']==0 and v['new_risk_proxy_violations']==0
assert state['books']==old['books'] and state['daily']==old['daily'];expected=0;details=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  prior=old['books'][a][k];stack=old['risk'][a][k];active=bool(D(prior['signed_units']));assert stack[0]['t']==1793347200000000000 and state['risk'][a][k]==[{'t':1793354400000000000,'state':prior}]
  if active:
   assert len(stack)==2 and stack[1]['t']==1793347200001000000 and stack[1]['state']==prior and stack[1]['t']-stack[0]['t']==1000000;assert D(stack[0]['state']['cash'])+D('.040380886617876192')==D(prior['cash']);hour08=len(stack);hour09=1;expected+=hour08+hour09
  else:assert len(stack)==1;hour08=hour09=0
  assert state['counters'][a][k]['funding_settlements']==old['counters'][a][k]['funding_settlements'] and state['counters'][a][k]['funding_usdt']==old['counters'][a][k]['funding_usdt'];details.append({'asset':a,'cost':k,'closed08hour_positive_duration_states':hour08,'closed09hour_states':hour09,'cash_units_entry_unchanged':True})
assert expected==9==v['new_closed_hour_risk_checks'];put(R/'risk_carry_verification.json',{'passed':True,'old_state_sha256':point['state_sha256'],'new_state_sha256':sha(W/'state.json'),'prefund_positive_duration_ns':1000000,'actual_positive_duration_pre_and_post_funding_states_checked_in08hour':True,'hour_state_details':details,'new_closed_hour_risk_checks':expected,'new_risk_proxy_violations':0,'new_funding_cashflows':0,'funding08_not_recredited':True,'cash_units_entry_precisely_carried':True,'current10hour_risk_stack':state['risk'],'daily_context_bars':36,'daily_NAV_boundaries':4,'next_funding_utc':'2026-10-30T16:00:00Z','next_daily_decision_utc':'2026-10-31T00:01:00Z','next_window_policy':'10:30to12:30deriveactualactionsfrompacket;current10houronepostfundstate,09closed08houralreadycheckedboth1msprefund/postfundstates;no reset/refunding.'});print('PASS08to10:9actualriskchecksinclude1msprefund,zero08fundingrecredit,cash/q/entryunchanged')
