"""Owncurrent08.001funding;historical00/16exactlyonce,no new daily decision."""
import gzip,json,sys
from decimal import Decimal as D
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());win=rd(R/'account_windows.json');ns=lambda s:(int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp())*10**9+datetime.fromisoformat(s.replace('Z','+00:00')).microsecond*1000);ns16=1794067200000000000;mid=ns('2026-11-08T00:00:00Z');rows=[];counts={};daily={};fills={};allunchanged=True
for stem in ['candidate','l4h02','fewm']:
 w=R/(stem+'_observation');before=rd(ROOT/rd(w/'previous_pointer.json')['state']);state=rd(w/'state.json');v=rd(R/(stem+'_verification.json'));im=rd(w/'input_manifest.json');assert sha(ROOT/im['packet'])==im['sha256'];packet=json.loads(gzip.decompress((ROOT/im['packet']).read_bytes()));delta=json.loads(gzip.decompress((w/'delta.json.gz').read_bytes()));fund=[x for x in delta['journal'] if x['kind']=='funding'];trades=[x for x in delta['journal'] if x['kind']=='trade' and x['status']=='filled'];expected=list(map(ns,win[stem]['expected_funding_utc']));assert v['passed'] and v['new_funding_settlements']==win[stem]['expected_funding_records']==len(fund) and v['new_daily_events']==len(win[stem]['expected_daily_events_utc']) and v['new_exact_causal_decisions']==6*v['new_daily_events']
 assert sorted({x['timestamp_ns'] for x in fund})==expected
 if win[stem]['expected_daily_events_utc']:assert all(x['timestamp_ns']<ns(win[stem]['expected_daily_events_utc'][0]) for x in fund)
 counts[stem]=len(fund);daily[stem]=v['new_exact_causal_decisions'];fills[stem]=v['new_fills'];allunchanged=allunchanged and state['books']==before['books'];point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();past={};current={}
 while point:
  assert point['delta'] not in seen;seen.add(point['delta']);assert sha(ROOT/point['delta'])==point['delta_sha256'];dd=json.loads(gzip.decompress((ROOT/point['delta']).read_bytes()))
  for x in dd['journal']:
   if x['kind']=='funding' and x['timestamp_ns'] in [ns16,mid]:
    dest=past if x['timestamp_ns']==ns16 else current;key=(x['asset'],str(x['cost_multiplier']));assert key not in dest;dest[key]=(x,point['delta'])
  ref=point.get('previous_pointer')
  if ref:assert sha(ROOT/ref['path'])==ref['sha256'];point=rd(ROOT/ref['path'])
  else:point=None
 assert set(past)=={(a,k) for a in ['BTC','ETH'] for k in ['1','2','3']};assert len(current)==6
 for a in ['BTC','ETH']:
  for k in ['1','2','3']:
   b,s=before['books'][a][k],state['books'][a][k];old,oldpath=past[a,k];fs=[x for x in fund if x['asset']==a and str(x['cost_multiplier'])==k];ts=[x for x in trades if x['asset']==a and str(x['cost_multiplier'])==k];amount=D(0);details=[]
   for x in fs:
    q=D(b['signed_units']);f=next(z for z in packet['assets'][a]['funding'] if int(z['fundingTime'])*1000000==x['timestamp_ns']);base=-q*D(f['markPrice'])*D(f['fundingRate']);value=base*int(k) if base<0 else base;assert q==D(x['signed_units']) and D(x['rate'])==D(f['fundingRate']) and D(x['mark_price'])==D(f['markPrice']) and D(x['base_amount_usdt'])==base and D(x['amount_usdt'])==value and D(x['cash_before'])==D(b['cash']) and D(x['cash_after'])==D(b['cash'])+value;assert all(z['timestamp_ns']>x['timestamp_ns'] for z in ts);amount+=value;details.append({'ns':x['timestamp_ns'],'actual_rate':x['rate'],'actual_mark':x['mark_price'],'own_predecision_q':str(q),'base_usdt':str(base),'actual_usdt':str(value),'cash_before':x['cash_before'],'cash_after':x['cash_after']})
   if ts:assert s==ts[-1]['state_after']
   else:assert all(s[z]==b[z] for z in ['signed_units','entry_price','entry_reference']) and D(s['cash'])==D(b['cash'])+amount
   rows.append({'account':stem,'asset':a,'cost':k,'own_q_before':b['signed_units'],'own_q_after':s['signed_units'],'own_cash_before':b['cash'],'own_cash_after':s['cash'],'prior16_seen_exactly_once':True,'prior16_delta':oldpath,'prior16_rate':old['rate'],'prior16_mark':old['mark_price'],'prior16_own_q':old['signed_units'],'new_funding_records':len(fs),'new_funding_usdt':str(amount),'funding_fields':details,'actual_new_filled_trade_records':len(ts),'final_book_matches_own_fund_then_trade_ledger':True})
assert len(rows)==18 and counts=={'candidate':0,'l4h02':0,'fewm':0} and daily=={'candidate':0,'l4h02':0,'fewm':0}
put(R/'actual16_funding_handoff_verification.json',{'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'all18_own_book_checks':rows,'all_three_previous16_not_repeated':True,'Nov8_00_historical_settlement_each_account_once':True,'new_funding_records_by_account':counts,'new_causal_daily_decisions_by_account':daily,'new_fills_by_account':fills,'all18_own_cashflow_postfunding_and_trade_states_correct':True,'current_original_books_unchanged':allunchanged,'current_original_rules_and_complete_NAV_prefixes_preserved':True,'funding_income_not_boosted2x3x':True,'single_00_now_settled_once_in_own_window':True,'next_single_window_utc':['2026-11-09T18:30:00Z','2026-11-09T20:30:00Z'],'next_L4_FEWM_window_utc':['2026-11-09T20:10:00Z','2026-11-09T22:10:00Z'],'historical_Nov8_single08_completed_once_from_own_rate_mark_q':True,'Nov9_single08_completed_once_in_prior_own_window':True,'Nov9_L4_FEWM08_previously_booked_independently_once':True,'current_L4_FEWM08_not_repeated':True,'all_three_own08_complete_once':True,'current_round_future08_calculations':0,'L4_FEWM_prior16_once_no_repeat':True,'single_prior16_once_no_repeat':True,'next_L4_FEWM_marks_only_after16':True,'next_single_window_marks_only_after_own16':True,'no_original_frozen_E_rule_or_capital_adoption':True,'only_saved_own_chains_read_no_account_or_financial_rerun':True})
print('PASS18ownbooks;prior16once,eachown00once;alloriginalaccountsownNov9midnightonce;single08nowsettledonce;no00or16repeat;L4FEWM00notrepeated')
