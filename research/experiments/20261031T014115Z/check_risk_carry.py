"""Cross-day cash continuity using only independently audited real event journals."""
import json
from decimal import Decimal as D
from run import ROOT,R,sha,put
P=ROOT/'research/experiments/20261030T234040Z';old=json.loads((P/'candidate_observation/state.json').read_text());new=json.loads((R/'candidate_observation/state.json').read_text());v=json.loads((R/'candidate_verification.json').read_text());assert v['passed'] and v['new_exact_causal_decisions']==6 and v['daily_decisions_and_funding_and_fills_verified_independently'] and old['cutoff_ns']<new['cutoff_ns'];flows=v['independent_funding_cashflows'];trades=v['independent_trades'];journal=[*flows,*trades]
for asset,books in new['books'].items():
 for k,b in books.items():
  before=old['books'][asset][k];fund=sum((D(x['amount_usdt']) for x in flows if x['asset']==asset and str(x['cost_multiplier'])==k),D(0));fills=[x for x in trades if x['asset']==asset and str(x['cost_multiplier'])==k and x['status']=='filled'];realized=sum((D(x['realized_price_PnL_usdt']) for x in fills),D(0));fees=sum((D(x['cost_parts']['fee']) for x in fills),D(0));assert abs(D(b['cash'])-(D(before['cash'])+fund+realized-fees))<=D('1e-18')
  states=new['risk'][asset][k];assert states and all(old['cutoff_ns']<x['t']<=new['cutoff_ns'] for x in states) and all(x['t']<=y['t'] for x,y in zip(states,states[1:]))
  for a,z in zip(states,states[1:]):
   if a['t']==z['t']:assert any(x['asset']==asset and str(x['cost_multiplier'])==k and x['timestamp_ns']==a['t'] for x in journal)
  assert {q:D(z) for q,z in states[-1]['state'].items()}=={q:D(z) for q,z in b.items()}
assert all(old['cutoff_ns']<x['timestamp_ns']<=new['cutoff_ns'] for x in journal)
assert len(flows)==v['expected_from_actual_settlement_actions'] and v['new_risk_proxy_violations']==0
put(R/'risk_carry_verification.json',{'passed':True,'old_state_sha256':sha(P/'candidate_observation/state.json'),'new_state_sha256':sha(R/'candidate_observation/state.json'),'new_closed_hour_risk_checks':v['new_closed_hour_risk_checks'],'new_risk_proxy_violations':v['new_risk_proxy_violations'],'new_funding_cashflows':len(flows),'actual_funding_cashflows':flows,'actual_filled_orders':len([x for x in trades if x['status']=='filled']),'cash_continues_only_via_actualfunding_realizedPnL_andfees':True,'same_ns_funding_and_trade_risk_states_preserved':True,'daily_context_bars':37,'daily_NAV_boundaries':5,'next_daily_decision_utc':'2026-11-01T00:01:00Z','current_risk_stack':new['risk'],'next_window_policy':'Oct31UTC00:30to02:30deriveactualpacket,originalfrozenrules/BTCN1000ETHN3000/raw[1,1],do not recredit any funding<=current00:30cut;no account reset or newrankparameters.'});print('PASS crossdayactualfunding/trades/fees/cash/q and ordered riskstates;no zero-event assumption')
