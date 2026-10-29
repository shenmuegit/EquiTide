"""Check carried22h exposure and the actual post-midnight funding/decision risk stack."""
import copy,json
from decimal import Decimal as D
from run import ROOT,R,sha,put
beforepath=ROOT/'research/experiments/20261028T232123Z/candidate_observation/state.json';afterpath=R/'candidate_observation/state.json';before=json.loads(beforepath.read_text());after=json.loads(afterpath.read_text());v=json.loads((R/'candidate_verification.json').read_text());assert v['passed'] and v['window_start_utc']=='2026-10-28T22:30:00Z' and v['cutoff_utc']=='2026-10-29T00:30:00Z' and v['new_funding_settlements']==v['expected_from_actual_settlement_actions'] and v['new_exact_causal_decisions']==6 and v['daily_boundaries_per_scene']==3
zero=1793232000000000000;entries=sorted([*v['independent_funding_cashflows'],*v['independent_trades']],key=lambda x:(x['timestamp_ns'],x['event_code'],x['asset'],int(x['cost_multiplier'])));out=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  old=before['risk'][a][k];assert len(old)==1 and old[0]['t']==1793224800000000000 and old[0]['state']==before['books'][a][k];book=copy.deepcopy(before['books'][a][k]);stack=[{'t':zero,'state':copy.deepcopy(book)}]
  for e in entries:
   if e['asset']!=a or str(e['cost_multiplier'])!=k:continue
   previous=copy.deepcopy(book)
   if e['kind']=='funding':
    raw=-D(book['signed_units'])*D(e['mark_price'])*D(e['rate']);amount=raw*int(k) if raw<0 else raw;assert D(e['amount_usdt'])==amount and D(e['cash_before'])==D(book['cash'])
    if amount:book['cash']=str(D(book['cash'])+amount)
   elif e['status']=='filled':assert e['state_before']==book;book=copy.deepcopy(e['state_after'])
   if book!=previous:stack.append({'t':e['timestamp_ns'],'state':copy.deepcopy(book)})
  assert stack==after['risk'][a][k] and book==after['books'][a][k];out.append({'asset':a,'cost':k,'old22hour_state_carried':True,'current00hour_state_count':len(stack),'current_stack_event_times_ns':[x['t'] for x in stack]})
assert v['new_closed_hour_risk_checks']>=6 and v['new_risk_proxy_violations']==0
put(R/'risk_carry_verification.json',{'passed':True,'source_state':str(beforepath.relative_to(ROOT)),'source_state_sha256':sha(beforepath),'new_state':str(afterpath.relative_to(ROOT)),'new_state_sha256':sha(afterpath),'source22hour_then23hour_checks':v['new_closed_hour_risk_checks'],'new_funding_cashflows':v['new_funding_settlements'],'new_daily_decisions':v['new_exact_causal_decisions'],'new_fills':v['new_fills'],'preserved_current00hour_funding_decision_stacks':out,'no_funding_duplicate_or_cash_reset':True,'new_financial_evaluations':0});print('PASS:22/23hour risk consumed,actual midnightfunding/daily fills independently carried in00hour stacks;do not discard before01hourclose')
