"""Resolve saved formatting/seal blockers only after actual successful scoped checks."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[2];sys.path.insert(0,str(R));from common import sha,put,now,rel
rd=lambda p:json.loads(p.read_text());v=rd(R/'staged_whitespace_verification.json');receipt=rd(R/'review/native_staged_whitespace_retry.py_receipt.json');bound=rd(R/'bound_source_whitespace_verification.json');assert v['passed'] and all(x['exit_code']==0 for x in v['commands']) and receipt['exit_code']==0 and bound['passed'] and sha(R/'run.py')==bound['before_evaluation_bound_sha256'] and sha(R/'report.json')==bound['financial_report_sha256']
f=R/'read_failures.json';d=rd(f)
for z in d['facts']:
 if z['kind'] in ['staged_whitespace','prepublication_seal']:
  assert not z['resolved'];z.update(resolved=True,resolved_utc=now(),resolution='Native scoped style retry passed; report EOF normalized; single immutable executed-source pureblank exception guarded by original bound SHA and exact line content; all financial/registry/full local-remote byte checks retained.',successful_style_retry_receipt=rel(R/'review/native_staged_whitespace_retry.py_receipt.json'),successful_style_retry_sha256=sha(R/'review/native_staged_whitespace_retry.py_receipt.json'),financial_or_account_reruns=0)
assert all(z['resolved'] for z in d['facts']);put(f,d);print('PASS originalstyleandsealblockersresolvedbyactualnativeformatretry;allboundfinancialsourcebytesunchanged')
