"""Check zero-duration08prefunding exclusion and carried postfund cash through10hour."""
import json
from run import ROOT,R,sha,put
beforepath=ROOT/'research/experiments/20261029T092426Z/candidate_observation/state.json';afterpath=R/'candidate_observation/state.json';before=json.loads(beforepath.read_text());after=json.loads(afterpath.read_text());v=json.loads((R/'candidate_verification.json').read_text());assert v['passed'] and v['window_start_utc']=='2026-10-29T08:30:00Z' and v['cutoff_utc']=='2026-10-29T10:30:00Z' and v['new_funding_settlements']==v['new_exact_causal_decisions']==v['new_fills']==0
rows=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  old=before['risk'][a][k];new=after['risk'][a][k];assert len(old)==(2 if a=='BTC' else 1) and all(x['t']==1793260800000000000 for x in old) and len(new)==1 and new[0]['t']==1793268000000000000 and new[0]['state']==old[-1]['state']==before['books'][a][k]==after['books'][a][k]
  rows.append({'asset':a,'cost':k,'source08hour_state_count':len(old),'source_state_times_ns':[x['t'] for x in old],'prefunding_duration_ns':0 if a=='BTC' else None,'nonzero_position_states_at09close':1 if a=='BTC' else 0,'current10hour_state_count':1})
assert v['new_closed_hour_risk_checks']==6 and v['new_risk_proxy_violations']==0
put(R/'risk_carry_verification.json',{'passed':True,'source_state':str(beforepath.relative_to(ROOT)),'source_state_sha256':sha(beforepath),'new_state':str(afterpath.relative_to(ROOT)),'new_state_sha256':sha(afterpath),'states':rows,'zero_duration08prefunding_state_correctly_excluded':True,'expected_BTC_state_hour_checks':6,'actual_independently_checked_state_hours':v['new_closed_hour_risk_checks'],'new_funding_settlements':0,'08funding_not_recredited':True,'current10hour_state_carried':True,'new_financial_evaluations':0});print('PASS:08zero-duration prefund excluded,postfund08at09close and09hourat10close=6BTC checks;no funding duplicate or reset')
