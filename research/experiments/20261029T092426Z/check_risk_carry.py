"""Independently bind carried06hour books to actual08funding cash and08hour risk stacks."""
import copy,gzip,json
from datetime import datetime,timezone
from decimal import Decimal as D
from run import ROOT,R,sha,put
ns=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())*1000000000
beforepath=ROOT/'research/experiments/20261029T072425Z/candidate_observation/state.json';afterpath=R/'candidate_observation/state.json';before=json.loads(beforepath.read_text());after=json.loads(afterpath.read_text());v=json.loads((R/'candidate_verification.json').read_text());delta=json.loads(gzip.decompress((R/'candidate_observation/delta.json.gz').read_bytes()))
assert v['passed'] and v['window_start_utc']=='2026-10-29T06:30:00Z' and v['cutoff_utc']=='2026-10-29T08:30:00Z' and v['new_exact_causal_decisions']==v['new_fills']==0
assert v['new_funding_settlements']==6 and len(delta['journal'])==6 and v['new_closed_hour_risk_checks']==6 and v['new_risk_proxy_violations']==0
rows=[];flows=[]
for a in ['BTC','ETH']:
 for k in ['1','2','3']:
  old=before['risk'][a][k];new=after['risk'][a][k];book=copy.deepcopy(before['books'][a][k]);assert len(old)==1 and old[0]['t']==ns('2026-10-29T06:00:00Z') and old[0]['state']==book
  js=[x for x in delta['journal'] if x['asset']==a and str(x['cost_multiplier'])==k];assert len(js)==1;j=js[0];t=j['timestamp_ns'];assert ns('2026-10-29T08:00:00Z')<=t<=ns('2026-10-29T08:30:00Z')
  raw=-D(book['signed_units'])*D(j['mark_price'])*D(j['rate']);amount=raw*int(k) if raw<0 else raw;assert D(j['signed_units'])==D(book['signed_units']) and D(j['base_amount_usdt'])==raw and D(j['amount_usdt'])==amount and D(j['cash_before'])==D(book['cash'])
  expected=[{'t':ns('2026-10-29T08:00:00Z'),'state':copy.deepcopy(book)}]
  if amount:book['cash']=str(D(book['cash'])+amount);expected.append({'t':t,'state':copy.deepcopy(book)})
  assert D(j['cash_after'])==D(book['cash']) and after['books'][a][k]==book and new==expected
  for field in ['signed_units','entry_price','entry_reference']:assert after['books'][a][k][field]==before['books'][a][k][field]
  rows.append({'asset':a,'cost':k,'source06hour_state_count':1,'current08hour_state_count':len(new),'current08hour_state_times_ns':[x['t'] for x in new],'prefunding_positive_duration_ns':t-ns('2026-10-29T08:00:00Z') if amount else None,'next09close_policy':'Keep all states;count only positive-overlap duration,excluding any exact same-timestamp zero-duration prefix.'});flows.append(j)
put(R/'risk_carry_verification.json',{'passed':True,'source_state':str(beforepath.relative_to(ROOT)),'source_state_sha256':sha(beforepath),'new_state':str(afterpath.relative_to(ROOT)),'new_state_sha256':sha(afterpath),'states':rows,'actual08funding_cashflows':flows,'positive_overlap06hour_checked_at07close_and07hour_at08close':True,'actual_independently_checked_state_hours':v['new_closed_hour_risk_checks'],'new_funding_settlements':6,'only_this_window_exact_actual_settlements_credited_once':True,'income_not_cost_amplified_outflow_stressed':True,'actual_settlement_precision_not_assumed':True,'current08hour_pre_post_cash_states_preserved':True,'new_financial_evaluations':0})
print('PASS:6 actual08funding cashflows independently verified;06/07hour checks6;precise08hour pre/post states kept for next09close,quantity and entry unchanged')
