"""Read-only reuse of the prior actual Nov11_08 public response bytes."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261111T092544Z';sys.path.insert(0,str(R));from common import sha,put,rel,now
rd=lambda p:json.loads(p.read_text())
pre=rd(P/'funding08_nov11_preflight.json');rr=rd(P/'funding08_nov11_preflight_receipts.json');cap=rd(P/'review_capture_nov11_08_public.py_receipt.json');assert cap['actual_exit_code']==0 and pre['nominal_UTC']=='2026-11-11T08:00:00Z' and pre['account_or_strategy_calculations']==0
for n in ['funding08_nov11_preflight.json','funding08_nov11_preflight_receipts.json']:assert (R/n).read_bytes()==(P/n).read_bytes()
for z in rr:
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes'] and z['curl_exit_code']==0 and z['http_status']==200
 assert json.loads(gzip.decompress((ROOT/z['raw']).read_bytes()))==pre['public_fields_by_asset'][z['asset']]
put(R/'immutable_nov11_08_public_reuse_verification.json',{'passed':True,'recorded_utc':now(),'source':rel(P/'funding08_nov11_preflight.json'),'source_sha256':sha(P/'funding08_nov11_preflight.json'),'original_native_capture_receipt':rel(P/'review_capture_nov11_08_public.py_receipt.json'),'original_native_capture_receipt_sha256':sha(P/'review_capture_nov11_08_public.py_receipt.json'),'fresh_GETs':0,'original_GETs':len(rr),'original_retrieval_UTC_preserved':True,'public_fields':pre['public_fields_by_asset'],'account_cashflows_reused':False,'new_strategy_or_account_valuations':0})
print('PASS original Nov11_08 2raw/native0/UTC unchanged,freshGET0;own single cashflow remains pending evaluation')
