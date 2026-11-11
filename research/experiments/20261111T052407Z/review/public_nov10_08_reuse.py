"""Verify exact prior Nov10_08 public fields and original actual capture; no valuation."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261110T091228Z';sys.path.insert(0,str(R));from common import sha,put,rel,now
rd=lambda p:json.loads(p.read_text());pre=rd(R/'funding08_nov10_preflight.json');rr=rd(R/'funding08_nov10_preflight_receipts.json');assert rd(P/'review_capture_nov10_08_public.py_receipt.json')['actual_exit_code']==0 and pre['account_or_strategy_calculations']==0
for n in ['funding08_nov10_preflight.json','funding08_nov10_preflight_receipts.json']:assert (R/n).read_bytes()==(P/n).read_bytes()
for z in rr:assert z['http_status']==200 and z['curl_exit_code']==0 and sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
assert {int(f['fundingTime']) for fs in pre['public_fields_by_asset'].values() for f in fs}=={1794297600000}
put(R/'immutable_nov10_08_public_reuse_verification.json',{'passed':True,'verified_utc':now(),'new_current_HTTP_requests':0,'original_actual_capture_receipt':rel(P/'review_capture_nov10_08_public.py_receipt.json'),'original_actual_capture_receipt_sha256':sha(P/'review_capture_nov10_08_public.py_receipt.json'),'original_retrieval_UTC_preserved':True,'original_public_fields_sha256':sha(P/'funding08_nov10_preflight.json'),'own_account_cashflows_reused':False,'new_strategy_or_account_valuations':0});print('PASS immutable Nov10_08 official field reuse,original native0,0 new GET/valuation')
