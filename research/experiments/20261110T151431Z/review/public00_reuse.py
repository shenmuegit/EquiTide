"""Immutable actual Nov10_00 public fields/provenance reuse; no account calculation."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];P=ROOT/'research/experiments/20261110T131400Z';sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());names=['funding00_current_preflight.json','funding00_current_preflight_receipts.json'];reuse=rd(R/'funding00_current_reuse.json');assert reuse['new_current_HTTP_requests']==0 and reuse['only_public_fields_reused_not_account_cashflows'] and reuse['original_retrieval_UTC_preserved']
for n in names:assert (R/n).read_bytes()==(P/n).read_bytes()
pre=rd(R/names[0]);receipts=rd(R/names[1]);assert pre['account_or_strategy_calculations']==0 and rd(P/'review_public00_reuse.py_receipt.json')['actual_exit_code']==0 and rd(ROOT/'research/experiments/20261110T011054Z/review_capture_current00_public.py_receipt.json')['actual_exit_code']==0
for z in receipts:assert z['http_status']==200 and z['curl_exit_code']==0 and sha(ROOT/z['raw'])==z['sha256'] and len(gzip.decompress((ROOT/z['raw']).read_bytes()))==z['bytes']
assert {int(z['fundingTime']) for rows in pre['public_fields_by_asset'].values() for z in rows}=={1794268800000}
put(R/'immutable_current00_public_reuse_verification.json',{'passed':True,'verified_utc':now(),'new_current_HTTP_requests':0,'account_or_strategy_calculations':0,'original_actual_capture_receipt':'research/experiments/20261110T011054Z/review_capture_current00_public.py_receipt.json','exact_prior_public_field_bytes':{rel(P/n):sha(P/n) for n in names},'original_receipts':receipts,'only_actual_public_fields_reused_not_cashflows':True,'original_wholemillisecond_timestamp_preserved':True});print('PASSimmutableactualNov10_00fields/raw/originalnativecapture0;0newGET/valuation;eachownqrequired')
