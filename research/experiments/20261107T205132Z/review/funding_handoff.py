"""Read saved own-account chains to prove no repeated Nov7 16UTC funding."""
import gzip,json,sys
from decimal import Decimal as D
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());win=rd(R/'account_windows.json');ns16=1794067200000000000;rows=[]
for stem in ['candidate','l4h02','fewm']:
 w=R/(stem+'_observation');previous=rd(w/'previous_pointer.json');before=rd(ROOT/previous['state']);state=rd(w/'state.json');v=rd(R/(stem+'_verification.json'));delta=json.loads(gzip.decompress((w/'delta.json.gz').read_bytes()))
 assert v['passed'] and v['new_daily_events']==v['new_exact_causal_decisions']==v['new_funding_settlements']==v['new_fills']==0
 assert not win[stem]['expected_funding_utc'] and not any(x['kind'] in ['funding','trade'] for x in delta['journal'])
 assert state['books']==before['books'] and before['cutoff_ns']>ns16 and state['cutoff_ns']>before['cutoff_ns']
 point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();past={}
 while point:
  assert point['delta'] not in seen;seen.add(point['delta']);assert sha(ROOT/point['delta'])==point['delta_sha256'];d=json.loads(gzip.decompress((ROOT/point['delta']).read_bytes()))
  for x in d['journal']:
   if x['kind']=='funding' and x['timestamp_ns']==ns16:
    key=(x['asset'],str(x['cost_multiplier']));assert key not in past;past[key]=(x,point['delta'])
  ref=point.get('previous_pointer')
  if ref:assert sha(ROOT/ref['path'])==ref['sha256'];point=rd(ROOT/ref['path'])
  else:point=None
 assert set(past)=={(a,k) for a in ['BTC','ETH'] for k in ['1','2','3']}
 for asset in ['BTC','ETH']:
  for k in ['1','2','3']:
   b,s=before['books'][asset][k],state['books'][asset][k];x,path=past[asset,k];q=D(x['signed_units']);base=-q*D(x['mark_price'])*D(x['rate']);amount=base*int(k) if base<0 else base
   assert D(x['base_amount_usdt'])==base and D(x['amount_usdt'])==amount and D(x['cash_after'])==D(x['cash_before'])+amount
   assert D(s['signed_units'])==q and s==b
   if asset=='BTC':assert q=={'candidate':D('-.012'),'l4h02':D('-.006'),'fewm':D('-.009')}[stem] and D(x['rate'])==D('.00001302') and D(x['mark_price'])==D('75728')
   else:assert q==amount==0 and D(x['rate'])==D('.00007427') and D(x['mark_price'])==D('2236.19')
   rows.append({'account':stem,'asset':asset,'cost':k,'own_q':s['signed_units'],'own_cash_before':b['cash'],'own_cash_after':s['cash'],'new_funding_records':0,'new_funding_usdt':'0','funding_fields':[],'prior16_settlement_found_exactly_once':True,'prior16_delta':path,'prior16_timestamp_ns':ns16,'prior16_rate':x['rate'],'prior16_mark':x['mark_price'],'prior16_own_amount_usdt':x['amount_usdt']})
assert len(rows)==18
put(R/'actual16_funding_handoff_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'all18_own_book_checks':rows,'all_three_perp_accounts16_already_accounted_independently_once':True,'current_three_perp_new_funding_records':0,'current_original_books_unchanged':True,'positive_income_not_boosted2x3x':True,'zero_ETH_funding_derived_from_actual_q_zero':True,'current_single_window_utc':[win['candidate']['start_utc'],win['candidate']['cutoff_utc']],'L4_FEWM_current_window_utc':[win['l4h02']['start_utc'],win['l4h02']['cutoff_utc']],'next_single_window_utc':['2026-11-07T18:30:00Z','2026-11-07T20:30:00Z'],'next_L4_FEWM_window_utc':['2026-11-07T20:10:00Z','2026-11-07T22:10:00Z'],'no_future_window_should_repeat16':True,'next_scheduled_funding00_only_when_own_window_reaches_it':True,'all_next_daily_decision_utc':'2026-11-08T00:01:00Z','no_new_daily_decisions_or_trades':True,'only_saved_actual_own_chains_read_no_account_or_financial_rerun':True})
print('PASS18ownbooksunchanged;prioractual16fundingexactlyonceeach;currentfunding/trades/dailyzero')
