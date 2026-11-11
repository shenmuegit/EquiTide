"""Verify immutable genuine Nov10_16 public fields and original native capture; no valuation."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261110T171502Z';sys.path.insert(0,str(R));from common import sha,put,rel,now
rd=lambda p:json.loads(p.read_text());names=['funding16_nov10_preflight.json','funding16_nov10_preflight_receipts.json'];pre=rd(R/names[0]);rr=rd(R/names[1]);cap=rd(P/'review_capture_nov10_16_public.py_receipt.json');assert cap['exit_code']==0 and pre['account_or_strategy_calculations']==0 and rd(R/'funding16_nov10_reuse.json')['new_current_HTTP_requests']==0
for n in names:assert (R/n).read_bytes()==(P/n).read_bytes()
for z in rr:
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z['http_status']==200 and z['curl_exit_code']==0:assert json.loads(gzip.decompress((ROOT/z['raw']).read_bytes()))==pre['public_fields_by_asset'][z['asset']]
assert {int(z['fundingTime']) for es in pre['public_fields_by_asset'].values() for z in es}=={1794326400002}
put(R/'immutable_nov10_16_public_reuse_verification.json',{'passed':True,'verified_utc':now(),'new_current_HTTP_requests':0,'original_actual_capture_receipt':rel(P/'review_capture_nov10_16_public.py_receipt.json'),'original_actual_capture_receipt_sha256':sha(P/'review_capture_nov10_16_public.py_receipt.json'),'original_retrieval_UTC_preserved':True,'source_bytes_sha256':{rel(P/n):sha(P/n) for n in names},'only_public_fields_reused_not_account_cashflows':True,'single_requires_own_q_cash_and_original_plan':True,'L4_FEWM_already_own16_once':True,'new_strategy_or_account_valuations':0});print('PASS immutable actualNov10_16.002 public source/native0/raw fields;0newHTTP/valuation,ownq/cash required')
