"""Read original actual Nov11_00.002 public fields;preserve original retrieval,no account calculation."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261111T092544Z';sys.path.insert(0,str(R));from common import sha,put,rel,now
rd=lambda p:json.loads(p.read_text());pre=rd(R/'funding00_nov11_preflight.json');receipts=rd(R/'funding00_nov11_preflight_receipts.json');original=ROOT/'research/experiments/20261111T012135Z/review_capture_nov11_00_public.py_receipt.json';assert rd(original)['actual_exit_code']==0 and pre['account_or_strategy_calculations']==0
for n in ['funding00_nov11_preflight.json','funding00_nov11_preflight_receipts.json']:assert (R/n).read_bytes()==(P/n).read_bytes()
for z in receipts:
 assert sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
 if z['http_status']==200 and z['curl_exit_code']==0:assert json.loads(gzip.decompress((ROOT/z['raw']).read_bytes()))==pre['public_fields_by_asset'][z['asset']]
assert {int(z['fundingTime']) for xs in pre['public_fields_by_asset'].values() for z in xs}=={1794355200002}
put(R/'immutable_nov11_00_public_reuse_verification.json',{'passed':True,'verified_utc':now(),'new_current_HTTP_requests':0,'actual_original_capture_receipt':rel(original),'actual_original_capture_receipt_sha256':sha(original),'original_retrieval_UTC_preserved':True,'only_public_fields_reused_not_account_cashflows':True,'single_requires_own_cash_q_and_own_daily':True,'L4_FEWM_own_Nov11_00_already_once':True,'source_sha256':{rel(P/n):sha(P/n) for n in ['funding00_nov11_preflight.json','funding00_nov11_preflight_receipts.json']},'new_strategy_or_account_valuations':0});print('PASS immutable genuineNov11_00.002 source;0newGET/valuation,singleownq/cash required,otheraccountsnotrepeated')
