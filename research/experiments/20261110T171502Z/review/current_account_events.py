"""Read-only actual Nov10_16 official fields, own funding cashflows and full-chain uniqueness."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel,now
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));pre=rd(R/'funding16_nov10_preflight.json');rr=rd(R/'funding16_nov10_preflight_receipts.json');bind=rd(R/'code_binding_before_evaluation.json');win=rd(R/'account_windows.json');receipt=rd(R/'review_capture_nov10_16_public.py_receipt.json');assert receipt['exit_code']==0 and pre['account_or_strategy_calculations']==0
for name in ['funding16_nov10_preflight.json','funding16_nov10_preflight_receipts.json','review/capture_nov10_16_public.py','review_capture_nov10_16_public.py_receipt.json']:assert sha(R/name)==bind['immutable_source_sha256'][rel(R/name)]
assert receipt['finished_utc']<bind['recorded_utc']
for z in rr:
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z['http_status']==200 and z['curl_exit_code']==0:assert gz(ROOT/z['raw'])==pre['public_fields_by_asset'][z['asset']]
expected={a:{int(z['fundingTime'])*1000000:z for z in es} for a,es in pre['public_fields_by_asset'].items()};newtimes={t for es in expected.values() for t in es};MID=1794268800000000000;OLD08=1794211200001000000;OLD16=1794240000001000000;NOV10_08=1794297600000000000;DEC=MID+60000000000;assert newtimes and all(MID+15*3600*10**9<t<MID+17*3600*10**9 for t in newtimes)
rows=[];counts={};latest={};chains={}
for stem in ['candidate','l4h02','fewm']:
 W=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));before=rd(ROOT/rd(W/'previous_pointer.json')['state']);state=rd(W/'state.json');im=rd(W/'input_manifest.json');packet=gz(ROOT/im['packet']);delta=gz(W/'delta.json.gz');fund=[z for z in delta['journal'] if z['kind']=='funding'];assert v['passed'] and v['new_daily_events']==v['new_exact_causal_decisions']==v['new_fills']==0 and not [z for z in delta['journal'] if z['kind'] in ['decision','trade']];counts[stem]=len(fund);assert len(fund)==v['new_funding_settlements']==win[stem]['expected_funding_records']==(0 if stem=='candidate' else 6)
 for a in ['BTC','ETH']:
  for k in ['1','2','3']:
   b,s=before['books'][a][k],state['books'][a][k];fs=[z for z in fund if z['asset']==a and str(z['cost_multiplier'])==k];amount=D(0)
   for z in fs:
    t=z['timestamp_ns'];f=expected[a][t];raw=next(f for f in packet['assets'][a]['funding'] if int(f['fundingTime'])*1000000==t);assert all(str(raw[n])==str(f[n]) for n in ['symbol','fundingTime','fundingRate','markPrice']);q=D(b['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);value=base*int(k) if base<0 else base;assert D(z['signed_units'])==q and D(z['rate'])==D(f['fundingRate']) and D(z['mark_price'])==D(f['markPrice']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==value and D(z['cash_before'])==D(b['cash']) and D(z['cash_after'])==D(b['cash'])+value;amount+=value;rows.append({'account':stem,'asset':a,'cost':k,'timestamp_ns':t,'fundingTime_ms':f['fundingTime'],'rate':f['fundingRate'],'mark':f['markPrice'],'own_pre_settlement_q':str(q),'base_usdt':str(base),'amount_usdt':str(value),'cash_before':b['cash'],'cash_after':s['cash']})
   assert all(s[n]==b[n] for n in ['signed_units','entry_price','entry_reference']) and D(s['cash'])==D(b['cash'])+amount
 point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();sets={t:set() for t in [MID,OLD08,OLD16,NOV10_08,DEC,*newtimes]};last=0
 while point:
  assert point['delta'] not in seen;seen.add(point['delta']);assert sha(ROOT/point['delta'])==point['delta_sha256']
  for z in gz(ROOT/point['delta'])['journal']:
   t=z['timestamp_ns'];kind=z['kind']
   if kind=='funding':last=max(last,t)
   if t in sets and (kind=='funding' and t!=DEC or kind=='decision' and t==DEC):
    key=z['asset'],str(z['cost_multiplier']);assert key not in sets[t];sets[t].add(key)
  ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
 assert all(len(sets[t])==6 for t in [MID,OLD08,OLD16,NOV10_08,DEC]);assert sum(len(sets[t]) for t in newtimes)==(0 if stem=='candidate' else 6);assert last==(NOV10_08 if stem=='candidate' else max(newtimes));latest[stem]=last;chains[stem]={str(t):len(keys) for t,keys in sets.items()}
assert counts=={'candidate':0,'l4h02':6,'fewm':6} and len(rows)==12
out={'passed':True,'verified_utc':now(),'actual_times_ns':sorted(newtimes),'public_preflight_sha256':sha(R/'funding16_nov10_preflight.json'),'native_actual_capture_receipt':rel(R/'review_capture_nov10_16_public.py_receipt.json'),'native_actual_capture_receipt_sha256':sha(R/'review_capture_nov10_16_public.py_receipt.json'),'fresh_public_GETs':len(rr),'own_current_funding_records':counts,'own_cashflow_rows':rows,'full_own_chain_settlement_counts':chains,'latest_actual_funding_ns_by_account':latest,'single_pending_own14_30to16_30_window':True,'positive_income_not_boosted2x3x':True,'each_own_q_and_cash_used':True,'no_original_rules_principal_positions_or_daily_changes':True,'new_account_or_financial_valuations':0}
put(R/'current_actual_nov10_16_funding_verification.json',out);put(R/'current_actual16_funding_verification.json',out)
# All three own Nov10_08 records remain exactly once; this round does not repeat them.
old08={'passed':True,'actual_times_ns':[NOV10_08],'public_preflight_sha256':sha(R/'funding08_nov10_preflight.json'),'native_actual_capture_receipt':'research/experiments/20261110T091228Z/review_capture_nov10_08_public.py_receipt.json','fresh_public_GETs':0,'own_current_funding_records':{a:0 for a in counts},'full_own_chain_settlement_counts':chains,'latest_actual_funding_ns_by_account':latest,'historical_all_three_own08_once':True,'new_account_or_financial_valuations':0}
put(R/'current_actual_nov10_08_funding_verification.json',old08);put(R/'current_actual08_funding_verification.json',old08)
for name in ['current_actual00_funding_verification.json','current_midnight_funding_verification.json']:put(R/name,{'passed':True,'actual_timestamp_ns':MID,'own_current_funding_records':{a:0 for a in counts},'latest_actual_funding_ns_by_account':latest,'historical_each_own00_once':True,'current_nov10_16_verification':rel(R/'current_actual_nov10_16_funding_verification.json'),'new_account_or_financial_valuations':0})
fv=rd(R/'forward_verification.json');assert fv['new_daily_decisions']==fv['new_reference_points']==fv['new_executions']==0
put(R/'current_midnight_daily_verification.json',{'passed':True,'current_new_daily_events':0,'current_new_causal_decisions':0,'current_new_midnight_funding_records':0,'current_SMA_new_daily_decisions':0,'current_Nov10_daily_decisions_by_account':{a:0 for a in counts},'historical_original_Nov10_daily_once_all3_perps_and_SMA':True,'current_Nov10_08_records_by_account':{a:0 for a in counts},'current_Nov10_16_records_by_account':counts,'all_next_daily_utc':'2026-11-11T00:01:00Z','latest_actual_funding_ns_by_account':latest,'new_account_or_financial_valuations':0})
print(json.dumps({'passed':True,'actual_current16_counts':counts,'own_cashflows':rows,'latest_actual_funding':latest}),flush=True)
