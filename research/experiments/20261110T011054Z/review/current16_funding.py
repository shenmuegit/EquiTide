"""Read saved actual Nov9_16.001 public fields and each own ledger once; no valuation."""
import gzip,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());gz=lambda p:json.loads(gzip.decompress(p.read_bytes()));pre=rd(R/'funding16_current_preflight.json');receipts=rd(R/'funding16_current_preflight_receipts.json');win=rd(R/'account_windows.json');binding=rd(R/'code_binding_before_evaluation.json');expected=1794240000001000000;rows=[];counts={};chains={};fundtime={}
assert pre['account_or_strategy_calculations']==0 and pre['nominal_UTC']=='2026-11-09T16:00:00Z' and rd(R/'review_public16_reuse.py_receipt.json')['actual_exit_code']==0 and rd(R/'immutable_current16_public_reuse_verification.json')['passed']
for path in ['funding16_current_preflight.json','funding16_current_preflight_receipts.json','review/capture_current16_public.py']:assert binding['immutable_source_sha256'][rel(R/path)]==sha(R/path)
for z in receipts:assert z['http_status']==200 and z['curl_exit_code']==0 and sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
assert {int(z['fundingTime'])*1000000 for zz in pre['public_fields_by_asset'].values() for z in zz}=={expected}
for stem in ['candidate','l4h02','fewm']:
 W=R/(stem+'_observation');before=rd(ROOT/rd(W/'previous_pointer.json')['state']);state=rd(W/'state.json');delta=gz(W/'delta.json.gz');v=rd(R/(stem+'_verification.json'));im=rd(W/'input_manifest.json');assert sha(ROOT/im['packet'])==im['sha256'];packet=gz(ROOT/im['packet']);eligible=before['cutoff_ns']<expected<=state['cutoff_ns'];allfund=[z for z in delta['journal'] if z['kind']=='funding'];fund=[z for z in allfund if z['timestamp_ns']==expected];assert v['passed'] and len(allfund)==v['new_funding_settlements']==win[stem]['expected_funding_records'] and len(fund)==(6 if eligible else 0);counts[stem]=len(fund)
 for z in fund:
  a,k=z['asset'],str(z['cost_multiplier']);f=pre['public_fields_by_asset'][a][0];raw=next(t for t in packet['assets'][a]['funding'] if int(t['fundingTime'])*1000000==expected);assert all(str(raw[field])==str(f[field]) for field in ['symbol','fundingTime','fundingRate','markPrice']);b,s=before['books'][a][k],state['books'][a][k];q=D(b['signed_units']);base=-q*D(f['markPrice'])*D(f['fundingRate']);amount=base*int(k) if base<0 else base
  assert z['timestamp_ns']==expected and D(z['signed_units'])==q and D(z['rate'])==D(f['fundingRate']) and D(z['mark_price'])==D(f['markPrice']) and D(z['base_amount_usdt'])==base and D(z['amount_usdt'])==amount and D(z['cash_before'])==D(b['cash']) and D(z['cash_after'])==D(b['cash'])+amount and D(s['cash'])==D(z['cash_after']) and all(s[key]==b[key] for key in ['signed_units','entry_price','entry_reference'])
  rows.append({'account':stem,'asset':a,'cost':k,'actual_timestamp_ns':expected,'fundingTime_ms':f['fundingTime'],'rate':f['fundingRate'],'mark':f['markPrice'],'own_units':str(q),'own_base_usdt':str(base),'own_amount_usdt':str(amount),'cash_before':b['cash'],'cash_after':s['cash']})
 point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));seen=set();events=[];times=[]
 while point:
  for key in ['delta','report','state','complete']:assert sha(ROOT/point[key])==point[key+'_sha256']
  for z in gz(ROOT/point['delta'])['journal']:
   if z['kind']=='funding':
    times.append(z['timestamp_ns'])
    if z['timestamp_ns']==expected:
     key=(z['asset'],str(z['cost_multiplier']));assert key not in seen;seen.add(key);events.append(z)
  ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
 assert len(events)==6;chains[stem]=len(events);fundtime[stem]=max(times)
assert counts=={'candidate':0,'l4h02':0,'fewm':0} and chains=={'candidate':6,'l4h02':6,'fewm':6} and len(rows)==0 and fundtime=={'candidate':expected,'l4h02':1794268800000000000,'fewm':1794268800000000000}
put(R/'current_actual16_funding_verification.json',{'passed':True,'checked_utc':now(),'actual_timestamp_ns':expected,'actual_timestamp_utc':'2026-11-09T16:00:00.001Z','preflight_sha256':sha(R/'funding16_current_preflight.json'),'fresh_public_GETs':0,'original_actual_public_GETs':len(receipts),'immutable_prior_public_response_reused':True,'own_current_funding_records':counts,'full_own_chain_current16_counts':chains,'latest_funding_timestamp_ns_by_account':fundtime,'own_cashflow_rows':rows,'single_prior16_not_repeated':True,'L4_FEWM_prior16_not_repeated':True,'positive_income_not_cost_boosted':True,'next_single_window_marks_only_after16':False,'next_single_requires_NEW_Nov10_00_and_daily':True,'next_L4_FEWM_window_marks_only_after16':True,'new_financial_or_account_advances':0})
print('PASSnewactualNov9_16.001:single0,L4/FEWM0each;0newownq/rate/mark/cashflows;old16once;L4_FEWMlatestnew00,singlelatestold16;0replay')
