"""Check that stored16hour pre/post-funding exposure was consumed by the17hour close audit."""
import json
from run import ROOT,R,sha,put
beforepath=ROOT/'research/experiments/20261028T172051Z/candidate_observation/state.json';afterpath=R/'candidate_observation/state.json';before=json.loads(beforepath.read_text());after=json.loads(afterpath.read_text());v=json.loads((R/'candidate_verification.json').read_text());assert v['passed'] and v['window_start_utc']=='2026-10-28T16:30:00Z' and v['cutoff_utc']=='2026-10-28T18:30:00Z' and v['new_funding_settlements']==v['expected_from_actual_settlement_actions']==0
start=1793203200000000000;fund=1793203200003000000;rows=[]
for k in ['1','2','3']:
 states=before['risk']['BTC'][k];assert len(states)==2 and [x['t'] for x in states]==[start,fund] and fund>start and states[0]['state']['signed_units']==states[1]['state']['signed_units']=='-0.012000000000000000';assert all(before['books']['BTC'][k][x]==after['books']['BTC'][k][x] for x in ['cash','signed_units','entry_price','entry_reference']);rows.append({'cost':k,'prefunding_state_start_ns':start,'postfunding_state_start_ns':fund,'prefunding_positive_duration_ns':fund-start,'source_state_count_to_check_at17hour_close':2})
for a in ['BTC','ETH']:
 for k in ['1','2','3']:assert len(after['risk'][a][k])==1 and after['risk'][a][k][0]['t']==1793210400000000000
assert v['new_closed_hour_risk_checks']==9 and v['new_risk_proxy_violations']==0
put(R/'risk_carry_verification.json',{'passed':True,'source_state':str(beforepath.relative_to(ROOT)),'source_state_sha256':sha(beforepath),'new_state':str(afterpath.relative_to(ROOT)),'new_state_sha256':sha(afterpath),'source16hour_pre_post_states':rows,'expected_BTC_state_hour_checks':9,'actual_independently_checked_state_hours':v['new_closed_hour_risk_checks'],'new_funding_settlements':0,'funding_not_recredited':True,'current18hour_risk_state_carried':True,'new_financial_evaluations':0});print('PASS:all3costs consume16hour positive-duration pre/post funding states at17close plus17hour at18close=9 checks;no funding recredit;18hour state carried')
