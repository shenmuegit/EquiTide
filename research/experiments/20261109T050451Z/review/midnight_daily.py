"""Verify saved Nov9 own midnight events remain unique; current windows append only marks."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261109T030420Z';sys.path.insert(0,str(R));from common import sha,put
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));MID=1794182400000000000;DEC=MID+60000000000;pref=rd(R/'funding_midnight_preflight.json');receipts=rd(R/'funding_midnight_preflight_receipts.json');win=rd(R/'account_windows.json');counts={};deccounts={};fundrows=[];current={}
for z in receipts:assert z['http_status']==200 and z['curl_exit_code']==0 and sha(ROOT/z['raw'])==z['sha256']
for stem in ['candidate','l4h02','fewm']:
 w=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));before=rd(ROOT/rd(w/'previous_pointer.json')['state']);state=rd(w/'state.json');delta=gz(w/'delta.json.gz');assert v['passed'] and not win[stem]['expected_daily_events_utc'] and not win[stem]['expected_funding_utc']
 assert v['new_funding_settlements']==v['new_daily_events']==v['new_exact_causal_decisions']==v['new_fills']==0 and state['books']==before['books'] and state['context'][ 'BTC']['daily']==before['context']['BTC']['daily'] and state['context']['ETH']['daily']==before['context']['ETH']['daily']
 assert not any(z['kind'] in ['funding','decision','trade'] for z in delta['journal']);current[stem]=0;point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();fundseen=set();decseen=set()
 while point:
  assert point['delta'] not in seen;seen.add(point['delta'])
  for k in ['delta','report','state','complete']:assert sha(ROOT/point[k])==point[k+'_sha256']
  own=gz(ROOT/point['delta']);matches=[z for z in own['journal'] if z['kind']=='funding' and z['timestamp_ns']==MID];decs=[z for z in own['journal'] if z['kind']=='decision' and z['timestamp_ns']==DEC]
  if matches:
   prior=rd(ROOT/point['previous_pointer']['path']);ownbefore=rd(ROOT/prior['state']);assert len(matches)==6
   for z in matches:
    a,k=z['asset'],str(z['cost_multiplier']);key=(a,k);assert key not in fundseen;fundseen.add(key);f=pref['public_fields_by_asset'][a][0];q=D(ownbefore['books'][a][k]['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);amount=base*int(k) if base<0 else base
    assert int(f['fundingTime'])*1000000==MID and D(z['signed_units'])==q and D(z['rate'])==D(f['fundingRate']) and D(z['mark_price'])==D(f['markPrice']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(ownbefore['books'][a][k]['cash']) and D(z['cash_after'])==D(z['cash_before'])+amount
    fundrows.append({'account':stem,'asset':a,'cost':k,'actual_timestamp_ns':MID,'rate':f['fundingRate'],'mark':f['markPrice'],'own_pre_daily_units':str(q),'own_base_usdt':str(base),'own_amount_usdt':str(amount),'original_delta':point['delta']})
  for z in decs:
   key=(z['asset'],str(z['cost_multiplier']));assert key not in decseen;decseen.add(key)
  ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
 assert len(fundseen)==len(decseen)==6;counts[stem]=len(fundseen);deccounts[stem]=len(decseen)
assert len(fundrows)==18 and current=={'candidate':0,'l4h02':0,'fewm':0};oldproof=P/'current_midnight_daily_verification.json';assert rd(oldproof)['passed'];fr=rd(R/'forward_report.json');fv=rd(R/'forward_verification.json');priorfr=rd(P/'forward_report.json');full=gz(ROOT/priorfr['source_inputs_path'])
assert fv['passed'] and fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0 and rd(R/'forward_state.json')['next_daily_decision_utc']=='2026-11-10T00:01:00Z'
for a in ['BTC','ETH']:assert len(full[a]['1d'])==65 and full[a]['1d'][-1][6]+1==MID//1000000 and priorfr['daily_decisions_by_asset'][a][0]['executed_at_utc']=='2026-11-09T00:01:00Z'
put(R/'current_midnight_funding_verification.json',{'passed':True,'actual_timestamp_ns':MID,'own_current_funding_records':current,'full_own_chain_Nov9_midnight_counts':counts,'historical_own_cashflow_rows':fundrows,'all3_original_own_midnight_funding_once':True,'own_predecision_quantities_used':True,'positive_income_not_cost_boosted':True,'immutable_public_preflight_sha256':sha(R/'funding_midnight_preflight.json'),'current_cashflows_copied_or_rebooked':0,'new_backtests_or_account_advances':0})
put(R/'current_midnight_daily_verification.json',{'passed':True,'UTC_daily_decision':'2026-11-09T00:01:00Z','current_new_daily_events':0,'current_new_causal_decisions':0,'current_new_funding_records':0,'current_SMA_new_percost_decisions':0,'historical_perp_daily_decisions_once_by_account':deccounts,'historical_SMA_daily_decisions_by_asset':priorfr['daily_decisions_by_asset'],'historical_SMA_proof':str(oldproof.relative_to(ROOT)),'historical_SMA_proof_sha256':sha(oldproof),'authoritative_SMA65_source':priorfr['source_inputs_path'],'authoritative_SMA65_sha256':sha(ROOT/priorfr['source_inputs_path']),'all4_next_daily_decision_utc':'2026-11-10T00:01:00Z','current_windows_only_closed_marks':True,'all4_own_midnight_events_not_repeated':True,'scope':'Read-only original complete chains and real saved data; no account advance/financial valuation/new fills or old byte changes.'});print('PASS18historicalownNov9fundingformulas/18perpdecisions/2SMAdecisions eachonce;currentall4marksonly,0newmidnight/fills')
