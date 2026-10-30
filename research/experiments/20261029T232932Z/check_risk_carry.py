"""Independent20hour riskcarry,actualfunding-only cashchanges and22hour state continuation."""
import gzip,json
from decimal import Decimal as D
from run import ROOT,R,put
W=R/'candidate_observation';read=lambda p:json.loads(p.read_text());before=read(ROOT/read(W/'previous_pointer.json')['state']);state=read(W/'state.json');delta=json.loads(gzip.decompress((W/'delta.json.gz').read_bytes()));cv=read(R/'candidate_verification.json');assert cv['new_exact_causal_decisions']==cv['new_fills']==0 and cv['new_closed_hour_risk_checks']==6 and cv['new_risk_proxy_violations']==0
start,end=1793304000000000000,1793311200000000000;rows=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  b,n=before['books'][a][k],state['books'][a][k];stack=before['risk'][a][k];assert stack==[{'t':start,'state':b}];funds=[x for x in delta['journal'] if x['kind']=='funding' and x['asset']==a and str(x['cost_multiplier'])==k];amount=sum((D(x['amount_usdt']) for x in funds),D(0));assert D(n['cash'])==D(b['cash'])+amount
  for key in ['signed_units','entry_price','entry_reference']:assert b[key]==n[key]
  assert state['risk'][a][k][0]['t']==end and state['risk'][a][k][-1]['state']==n and all(x['t']>=end for x in state['risk'][a][k]);old,new=before['counters'][a][k],state['counters'][a][k];assert new['funding_settlements']-old['funding_settlements']==len(funds)
  if a=='BTC':assert new['margin_checks']-old['margin_checks']==2
  else:assert new['margin_checks']==old['margin_checks']
  rows.append({'asset':a,'cost':k,'source20_states':stack,'current22_states':state['risk'][a][k],'closed_hour_checks':new['margin_checks']-old['margin_checks'],'actual_new_funding_entries':len(funds),'actual_funding_cashdelta':str(amount),'cash_after':n['cash']})
assert cv['cumulative_finished_candidate_observations']==108 and cv['prior_NAV_prefix']==4203 and cv['NAV_points_per_scene']==before['nav_points']+cv['new_NAV_points_per_scene'] and cv['elapsed_minutes']==4229
out={'passed':True,'new_funding_entries':cv['new_funding_settlements'],'prior16funding_not_recredited':True,'closed20_21hours_BTC_cost_checks':6,'risk_violations':0,'current22hour_ns':end,'states':rows,'next_funding_utc':'2026-10-30T00:00:00Z','next_daily_decision_utc':'2026-10-30T00:01:00Z'};put(R/'risk_carry_verification.json',out);print(json.dumps(out),flush=True)
