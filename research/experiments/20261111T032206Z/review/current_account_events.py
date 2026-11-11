"""Fresh Nov11_00 fields,each own pre-settlementq/cash,daily ordering and full-chain uniqueness."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,rel,now
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));bind=rd(R/'code_binding_before_evaluation.json');win=rd(R/'account_windows.json');pre=rd(R/'funding00_nov11_preflight.json');rr=rd(R/'funding00_nov11_preflight_receipts.json');cap=rd(R/'review_public_nov11_00_reuse.py_receipt.json');original=ROOT/'research/experiments/20261111T012135Z/review_capture_nov11_00_public.py_receipt.json';assert rd(original)['actual_exit_code']==0;assert cap['actual_exit_code']==0 and cap['finished_utc']<bind['recorded_utc'] and pre['account_or_strategy_calculations']==0
for n in ['funding00_nov11_preflight.json','funding00_nov11_preflight_receipts.json','review/public_nov11_00_reuse.py','review_public_nov11_00_reuse.py_receipt.json']:assert sha(R/n)==bind['immutable_source_sha256'][rel(R/n)]
for z in rr:
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z['http_status']==200 and z['curl_exit_code']==0:assert gz(ROOT/z['raw'])==pre['public_fields_by_asset'][z['asset']]
expected={a:{int(z['fundingTime'])*1000000:z for z in es} for a,es in pre['public_fields_by_asset'].items()};newtimes={t for es in expected.values() for t in es};MID=1794355200000000000;DEC=MID+60000000000;assert newtimes=={1794355200002000000};OLD00=1794268800000000000;OLD08=1794297600000000000;OLD16=1794326400002000000;OLDDEC=OLD00+60000000000;older=[1794211200001000000,1794240000001000000,OLD00,OLD08,OLD16]
counts={};rows=[];chains={};latest={};dailycounts={};filledcounts={}
for stem in ['candidate','l4h02','fewm']:
 W=R/(stem+'_observation');v=rd(R/(stem+'_verification.json'));before=rd(ROOT/rd(W/'previous_pointer.json')['state']);state=rd(W/'state.json');im=rd(W/'input_manifest.json');packet=gz(ROOT/im['packet']);delta=gz(W/'delta.json.gz');fund=[z for z in delta['journal'] if z['kind']=='funding'];dec=[z for z in delta['journal'] if z['kind']=='decision'];trades=[z for z in delta['journal'] if z['kind']=='trade' and z['status']=='filled'];dailycounts[stem]=v['new_daily_events'];filledcounts[stem]=len(trades);counts[stem]=len(fund);cross=stem=='candidate'
 assert v['passed'] and len(fund)==v['new_funding_settlements']==win[stem]['expected_funding_records']==(6 if cross else 0) and len(dec)==v['new_exact_causal_decisions']==(6 if cross else 0) and v['new_daily_events']==(1 if cross else 0)
 assert all(z['timestamp_ns']==DEC for z in dec) and all(z['timestamp_ns']>=DEC for z in trades)
 for a in ['BTC','ETH']:
  for k in ['1','2','3']:
   b,s=before['books'][a][k],state['books'][a][k];fs=[z for z in fund if z['asset']==a and str(z['cost_multiplier'])==k];assert len(fs)==int(cross);amount=D(0)
   for z in fs:
    t=z['timestamp_ns'];f=expected[a][t];raw=next(f for f in packet['assets'][a]['funding'] if int(f['fundingTime'])*1000000==t);assert all(str(raw[n])==str(f[n]) for n in ['symbol','fundingTime','fundingRate','markPrice']);q=D(b['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);value=base*int(k) if base<0 else base
    assert D(z['signed_units'])==q and D(z['rate'])==D(f['fundingRate']) and D(z['mark_price'])==D(f['markPrice']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==value and D(z['cash_before'])==D(b['cash']) and D(z['cash_after'])==D(b['cash'])+value and t<DEC;amount+=value
    rows.append({'account':stem,'asset':a,'cost':k,'timestamp_ns':t,'fundingTime_ms':f['fundingTime'],'rate':f['fundingRate'],'mark':f['markPrice'],'own_pre_settlement_q':str(q),'base_usdt':str(base),'amount_usdt':str(value),'cash_before_settlement':b['cash'],'cash_after_settlement':z['cash_after'],'cash_after_own_daily':s['cash'],'q_after_own_daily':s['signed_units']})
   owntrades=[z for z in trades if z['asset']==a and str(z['cost_multiplier'])==k]
   if owntrades:assert s==owntrades[-1]['state_after']
   else:assert all(s[n]==b[n] for n in ['signed_units','entry_price','entry_reference']) and D(s['cash'])==D(b['cash'])+amount
 point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();sets={t:set() for t in [*older,OLDDEC,DEC,*newtimes]};last=0
 while point:
  assert point['delta'] not in seen;seen.add(point['delta']);assert sha(ROOT/point['delta'])==point['delta_sha256']
  for z in gz(ROOT/point['delta'])['journal']:
   t=z['timestamp_ns'];kind=z['kind']
   if kind=='funding':last=max(last,t)
   if t in sets and (kind=='funding' and t not in [OLDDEC,DEC] or kind=='decision' and t in [OLDDEC,DEC]):
    key=z['asset'],str(z['cost_multiplier']);assert key not in sets[t];sets[t].add(key)
  ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
 assert all(len(sets[t])==6 for t in [*older,OLDDEC]) and len(sets[DEC])==6 and sum(len(sets[t]) for t in newtimes)==6 and last==max(newtimes);latest[stem]=last;chains[stem]={str(t):len(keys) for t,keys in sets.items()}
assert counts=={'candidate':6,'l4h02':0,'fewm':0} and dailycounts=={'candidate':1,'l4h02':0,'fewm':0} and len(rows)==6
out={'passed':True,'verified_utc':now(),'actual_times_ns':sorted(newtimes),'public_preflight_sha256':sha(R/'funding00_nov11_preflight.json'),'native_actual_capture_receipt':rel(original),'native_actual_capture_receipt_sha256':sha(original),'current_native_reuse_receipt':rel(R/'review_public_nov11_00_reuse.py_receipt.json'),'fresh_public_GETs':0,'original_public_GETs':len(rr),'own_current_funding_records':counts,'own_cashflow_rows':rows,'full_own_chain_settlement_counts':chains,'latest_actual_funding_ns_by_account':latest,'own_current_daily_events':dailycounts,'own_current_filled_trades':filledcounts,'all_three_own_Nov11_00_and_daily_completed_once':True,'L4_FEWM_own_Nov11_00_and_daily_completed_once':True,'single_Nov11_00_and_daily_pending_own_next_window':False,'positive_income_not_boosted2x3x':True,'each_own_q_and_cash_used':True,'original_frozen_rules_and_principal_unchanged':True,'new_account_or_financial_valuations':0}
put(R/'current_actual_nov11_00_funding_verification.json',out);put(R/'current_actual00_funding_verification.json',out);put(R/'current_midnight_funding_verification.json',out)
zero={s:0 for s in counts}
for label,ts,source,original in [('nov10_16',OLD16,'funding16_nov10_preflight.json','20261110T171502Z/review_capture_nov10_16_public.py_receipt.json'),('nov10_08',OLD08,'funding08_nov10_preflight.json','20261110T091228Z/review_capture_nov10_08_public.py_receipt.json')]:
 assert rd(ROOT/'research/experiments'/original).get('exit_code',rd(ROOT/'research/experiments'/original).get('actual_exit_code'))==0
 old={'passed':True,'actual_times_ns':[ts],'public_preflight_sha256':sha(R/source),'native_actual_capture_receipt':'research/experiments/'+original,'fresh_public_GETs':0,'own_current_funding_records':zero,'full_own_chain_settlement_counts':chains,'latest_actual_funding_ns_by_account':latest,'historical_all_three_own_once':True,'all_three_own_Nov10_16_completed_once':True,'single_pending_own_window':False,'new_account_or_financial_valuations':0};put(R/('current_actual_'+label+'_funding_verification.json'),old);put(R/('current_actual'+('16' if label.endswith('16') else '08')+'_funding_verification.json'),old)
fv=rd(R/'forward_verification.json');assert fv['new_daily_decisions']==2 and fv['new_reference_points']==1
put(R/'current_midnight_daily_verification.json',{'passed':True,'current_new_daily_events':1,'current_new_causal_decisions':6,'current_new_midnight_funding_records':6,'current_SMA_new_daily_decisions':2,'current_Nov11_daily_decisions_by_account':dailycounts,'current_Nov10_daily_decisions_by_account':zero,'historical_original_Nov10_daily_once_all3_perps_and_SMA':True,'current_Nov10_08_records_by_account':zero,'current_Nov10_16_records_by_account':zero,'current_Nov11_00_records_by_account':counts,'next_daily_by_account':{'SMA':'2026-11-12T00:01:00Z','single':'2026-11-12T00:01:00Z','L4':'2026-11-12T00:01:00Z','FEWM':'2026-11-12T00:01:00Z'},'latest_actual_funding_ns_by_account':latest,'new_account_or_financial_valuations':0})
print(json.dumps({'passed':True,'actual_currentNov11_00_counts':counts,'daily_counts':dailycounts,'own_filled_records':filledcounts,'own_cashflows':rows,'latest_actual_funding':latest}),flush=True)
