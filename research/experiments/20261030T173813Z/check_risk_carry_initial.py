"""Funding-crossing continuation: exact carried q/entry, cash and true risk-state times."""
import gzip,json
from decimal import Decimal as D
from run import ROOT,R,sha,put
P=ROOT/'research/experiments/20261030T153707Z';old=json.loads((P/'candidate_observation/state.json').read_text());new=json.loads((R/'candidate_observation/state.json').read_text());v=json.loads((R/'candidate_verification.json').read_text());flows=v['independent_funding_cashflows'];assert v['passed'] and v['new_exact_causal_decisions']==v['new_fills']==v['new_risk_proxy_violations']==0 and old['cutoff_ns']<new['cutoff_ns']
assert new['books']['BTC']['1']['signed_units']=='-0.012000000000000000' and all(D(x['signed_units'])==0 for x in new['books']['ETH'].values())
for asset,books in new['books'].items():
 for k,b in books.items():
  before=old['books'][asset][k]
  for key in ['signed_units','entry_price','entry_reference']:assert D(b[key])==D(before[key])
  amount=sum((D(x['amount_usdt']) for x in flows if x['asset']==asset and x['cost']==k),D(0));assert D(b['cash'])==D(before['cash'])+amount
  states=new['risk'][asset][k];assert states and all(old['cutoff_ns']<x['t']<=new['cutoff_ns'] for x in states) and all(x['t']<y['t'] for x,y in zip(states,states[1:]))
  assert {q:D(z) for q,z in states[-1]['state'].items()}=={q:D(z) for q,z in b.items()}
assert all(old['cutoff_ns']<x['timestamp_ns']<=new['cutoff_ns'] for x in flows)
assert len(flows)==v['expected_from_actual_settlement_actions']
put(R/'risk_carry_verification.json',{'passed':True,'old_state_sha256':sha(P/'candidate_observation/state.json'),'new_state_sha256':sha(R/'candidate_observation/state.json'),'new_closed_hour_risk_checks':v['new_closed_hour_risk_checks'],'new_risk_proxy_violations':0,'new_funding_cashflows':len(flows),'actual_funding_cashflows':flows,'funding08_not_recredited':True,'cash_units_entry_precisely_carried':True,'current16hour_risk_stack':new['risk'],'daily_context_bars':36,'daily_NAV_boundaries':4,'next_daily_decision_utc':'2026-10-31T00:01:00Z','next_window_policy':'16:30to18:30derivepacket,no assumed funding; preserve actual16UTCsubmillisecond funding and remaining positive-duration risk states, no reset.'});print('PASS actual16fundingcashflows/carry and strictly orderedrisk states; no zero-event/wholehour assumption')
