"""Immutable actual Nov9_16 public fields/provenance reuse; no cashflow calculation."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261110T091228Z';sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());names=['funding16_current_preflight.json','funding16_current_preflight_receipts.json'];reuse=rd(R/'funding16_current_reuse.json');assert reuse['new_current_HTTP_requests']==0 and reuse['only_public_fields_reused_not_account_cashflows'] and reuse['original_retrieval_UTC_preserved']
for n in names:assert (R/n).read_bytes()==(P/n).read_bytes()
pref,receipts=rd(R/names[0]),rd(R/names[1]);assert pref['account_or_strategy_calculations']==0 and rd(P/'review_public16_reuse.py_receipt.json')['actual_exit_code']==0 and rd(ROOT/'research/experiments/20261109T170751Z/review_capture_current16_public.py_receipt.json')['actual_exit_code']==0
for z in receipts:assert z['http_status']==200 and z['curl_exit_code']==0 and sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
assert {int(z['fundingTime']) for rows in pref['public_fields_by_asset'].values() for z in rows}=={1794240000001}
put(R/'immutable_current16_public_reuse_verification.json',{'passed':True,'verified_utc':now(),'new_current_HTTP_requests':0,'account_or_strategy_calculations':0,'exact_prior_public_bytes':{rel(P/n):sha(P/n) for n in names},'original_receipts':receipts,'original_capture_native_receipt':'research/experiments/20261109T170751Z/review_capture_current16_public.py_receipt.json','original_retrieval_UTC_preserved':True,'own_single16_cashflow_requires_own_q_and_cash':True,'L4_FEWM16_already_once_no_repeat':True,'actual_millisecond_timestamp_preserved':True})
print('PASS immutableactualNov9_16.001fields/rawreceipts;0newGET/valuation,cashflowsnotcopied,singleownqrequired')
