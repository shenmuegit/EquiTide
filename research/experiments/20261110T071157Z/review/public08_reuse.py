"""Verify immutable prior official funding fields; no account calculation or capture."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261110T051156Z';sys.path.insert(0,str(R));from common import sha,put,now
rd=lambda p:json.loads(p.read_text());files=['funding08_current_preflight.json','funding08_current_preflight_receipts.json'];reuse=rd(R/'funding08_current_reuse.json');assert reuse['new_current_HTTP_requests']==0 and reuse['only_public_fields_reused_not_account_cashflows'] and reuse['original_retrieval_UTC_preserved']
for f in files:assert (R/f).read_bytes()==(P/f).read_bytes()
pref=rd(R/files[0]);receipts=rd(R/files[1]);assert pref['account_or_strategy_calculations']==0 and rd(P/'review_public08_reuse.py_receipt.json')['actual_exit_code']==0 and rd(ROOT/'research/experiments/20261109T090618Z/review_capture_current08_public.py_receipt.json')['actual_exit_code']==0
for z in receipts:assert z['http_status']==200 and z['curl_exit_code']==0 and sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
assert {int(z['fundingTime']) for a in pref['public_fields_by_asset'].values() for z in a}=={1794211200001}
put(R/'immutable_current08_public_reuse_verification.json',{'passed':True,'verified_utc':now(),'new_current_HTTP_requests':0,'account_or_strategy_calculations':0,'exact_public_field_bytes':{str((P/f).relative_to(ROOT)):sha(P/f) for f in files},'original_receipts':receipts,'current_old08_not_rebooked':True,'current16_separately_verified':True,'other_account_cashflows_copied':False,'actual_millisecond_timestamp_preserved':True})
print('PASS immutable prior Nov9_08 publicTime/rate/mark/raw response bytes;0newGET/valuation/accountadvance,ownqrequired')
