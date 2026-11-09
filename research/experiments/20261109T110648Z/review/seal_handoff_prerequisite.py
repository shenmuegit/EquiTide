"""Read current actual pointer chains and verify latest funding for corrected handoff."""
import gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));from common import sha,put,now
rd=lambda p:json.loads(p.read_text());pref=rd(R/'funding08_current_preflight.json');expected={int(z['fundingTime'])*1000000 for rows in pref['public_fields_by_asset'].values() for z in rows};assert expected=={1794211200001000000};out={}
for stem in ['candidate','l4h02','fewm']:
 point=rd(ROOT/('research/automation/'+stem+'_forward_latest.json'));latest={}
 while point and len(latest)<6:
  assert sha(ROOT/point['delta'])==point['delta_sha256'];journal=json.loads(gzip.decompress((ROOT/point['delta']).read_bytes()))['journal']
  for z in sorted([z for z in journal if z['kind']=='funding'],key=lambda z:z['timestamp_ns'],reverse=True):latest.setdefault((z['asset'],str(z['cost_multiplier'])),z)
  ref=point.get('previous_pointer');point=rd(ROOT/ref['path']) if ref else None
 assert len(latest)==6 and {z['timestamp_ns'] for z in latest.values()}==expected;out[stem]=list(latest.values())
assert sha(R/'report.json')==rd(R/'verification.json')['report_sha256']
for path,h in rd(R/'code_binding_before_evaluation.json')['source_sha256'].items():assert sha(ROOT/path)==h
put(R/'seal_handoff_prerequisite_verification.json',{'passed':True,'verified_utc':now(),'latest_own_actual_funding_records':out,'all3_latest_actual08_not_old_midnight':True,'same_corrected_expectation_for_all3':True,'financial_report_and36_bound_sources_preserved':True,'new_financial_or_account_evaluations':0,'original_failed_seal_receipt':'failed_seal_attempt1/native_receipt.json','correction_limited_to_unbound_sealer_handoff_metadata':True})
print('PASS3ownlatestfunding6recordseachactual08.001;report/36executorsunchanged;0financial/accountreplays')
