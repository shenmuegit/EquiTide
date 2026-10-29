"""Exact16UTCzero-duration prefunding carry,closed16/17hours and no duplicate funding."""
import gzip,json
from decimal import Decimal as D
from run import ROOT,R,sha,put
W=R/'candidate_observation';read=lambda p:json.loads(p.read_text());before=read(ROOT/read(W/'previous_pointer.json')['state']);state=read(W/'state.json');delta=json.loads(gzip.decompress((W/'delta.json.gz').read_bytes()));cv=read(R/'candidate_verification.json');packet=json.loads(gzip.decompress((ROOT/read(W/'input_manifest.json')['packet']).read_bytes()));assert not delta['journal'] and cv['new_funding_settlements']==cv['new_exact_causal_decisions']==cv['new_fills']==0 and cv['new_closed_hour_risk_checks']==6 and cv['new_risk_proxy_violations']==0
start,end=1793289600000000000,1793296800000000000;rows=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  b,n=before['books'][a][k],state['books'][a][k];assert b==n;stack=before['risk'][a][k];assert all(x['t']==start for x in stack);assert state['risk'][a][k]==[{'t':end,'state':n}]
  old,new=before['counters'][a][k],state['counters'][a][k]
  for field in ['funding_settlements','funding_usdt','executions','round_trips','cost_usdt']:
   if field in old:assert old[field]==new[field],field
  if a=='BTC':
   assert len(stack)==2 and stack[0]['t']==stack[1]['t'] and D(stack[1]['state']['cash'])-D(stack[0]['state']['cash'])==D('0.09807957839130000000000000000') and stack[1]['state']==b and new['margin_checks']-old['margin_checks']==2
  else:assert len(stack)==1 and new['margin_checks']==old['margin_checks']
  rows.append({'asset':a,'cost':k,'source16_states':stack,'current18_states':state['risk'][a][k],'zero_duration_prefunding_excluded':a=='BTC','closed_hour_checks':new['margin_checks']-old['margin_checks'],'cash_preserved':n['cash']})
assert cv['cumulative_finished_candidate_observations']==102 and cv['prior_NAV_prefix']==3959 and cv['NAV_points_per_scene']==4081 and cv['new_NAV_points_per_scene']==122 and cv['elapsed_minutes']==3989
out={'passed':True,'actual_settlement_ns_and_cash_exact':True,'source16_settlement_already_credited_once':True,'new_funding_entries':0,'zero_duration16prefund_state_excluded':True,'closed16_17hours_BTC_cost_checks':6,'risk_violations':0,'current18hour_ns':end,'states':rows,'next_funding_utc':'2026-10-30T00:00:00Z','next_daily_decision_utc':'2026-10-30T00:01:00Z'};put(R/'risk_carry_verification.json',out);print(json.dumps(out),flush=True)
