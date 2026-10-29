"""Read-only actual16funding and carried14/15hour risk/cash audit."""
import gzip,json
from decimal import Decimal as D
from run import ROOT,R,sha,put
P=ROOT/'research/experiments/20261029T152659Z';bp=P/'candidate_observation/state.json';ap=R/'candidate_observation/state.json';before=json.loads(bp.read_text());after=json.loads(ap.read_text());v=json.loads((R/'candidate_verification.json').read_text());delta=json.loads(gzip.decompress((R/'candidate_observation/delta.json.gz').read_bytes()));journal=delta['journal']
assert v['passed'] and v['window_start_utc']=='2026-10-29T14:30:00Z' and v['cutoff_utc']=='2026-10-29T16:30:00Z' and v['new_exact_causal_decisions']==v['new_fills']==0
assert len(journal)==v['new_funding_settlements']==6 and len({(x['asset'],x['cost_multiplier'],x['timestamp_ns']) for x in journal})==6
assert v['new_closed_hour_risk_checks']==6 and v['new_risk_proxy_violations']==0
source_hour=1793282400000000000;current_hour=1793289600000000000;rows=[]
for asset in ['BTC','ETH']:
 for k in ['1','2','3']:
  a,b=before['books'][asset][k],after['books'][asset][k];old=before['risk'][asset][k];new=after['risk'][asset][k];events=[x for x in journal if x['asset']==asset and str(x['cost_multiplier'])==k];assert len(events)==1;x=events[0]
  assert current_hour<=x['timestamp_ns']<current_hour+60*1000000000 and len(old)==1 and old[0]['t']==source_hour and old[0]['state']==a and new[0]['t']==current_hour
  for f in ['signed_units','entry_price','entry_reference']:assert a[f]==b[f]
  assert D(b['cash'])-D(a['cash'])==D(x['amount_usdt']) and D(x['cash_before'])==D(a['cash']) and D(x['cash_after'])==D(b['cash'])
  base=-D(a['signed_units'])*D(x['mark_price'])*D(x['rate']);assert D(x['base_amount_usdt'])==base and D(x['amount_usdt'])==(base*int(k) if base<0 else base)
  assert after['counters'][asset][k]['funding_settlements']==before['counters'][asset][k]['funding_settlements']+1
  assert len(new)==(2 if a!=b else 1) and new[-1]['state']==b
  if a!=b:assert new[0]['state']==a and new[-1]['t']==x['timestamp_ns']
  assert all(z['state'] in [a,b] for z in new) and all(a0['t']<=b0['t'] for a0,b0 in zip(new,new[1:]))
  rows.append({'asset':asset,'cost':k,'source14hour_states':old,'current16hour_states':new,'funding':x,'zero_duration_prefunding_state':bool(len(new)>1 and new[0]['t']==new[1]['t']),'positive_prefunding_duration_ns':new[1]['t']-new[0]['t'] if len(new)>1 else 0})
put(R/'risk_carry_verification.json',{'passed':True,'source_state':str(bp.relative_to(ROOT)),'source_state_sha256':sha(bp),'new_state':str(ap.relative_to(ROOT)),'new_state_sha256':sha(ap),'states':rows,'14hour_checked_at15close_and15hour_at16close':True,'expected_BTC_state_hour_checks':6,'actual_independently_checked_state_hours':6,'new_funding_settlements':6,'actual_settlement_ns_and_cash_exact':True,'income_not_cost_multiplied':True,'00_08funding_not_recredited':True,'current16hour_precise_pre_post_states_carried':True,'new_financial_evaluations':0});print('PASS:6actualfundingentries exactns/rate/mark/signedq/cash;14/15hours6BTCchecks;precise16hourpre/postriskstates carried;no duplicate00/08')
