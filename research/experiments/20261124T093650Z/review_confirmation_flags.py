"""Correct a missing optional diagnostic field by checking exact saved BTC policy inputs."""
import csv,gzip,hashlib,json
from fractions import Fraction
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
rd=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
binding=rd(R/'confirmation_checker_binding.json');assert sha(Path(__file__))==binding['source_sha256']
p=rd(R/'plan.json');rhash=sha(R/'report.json');review=rd(R/'joint_economic_review.json');basefp='41de4309229b892489a07574af07a73ae93229a35c118558ed60362285e90c89';arcs={}
for fp,z in p['read_only_references'].items():
 if z['scope']=='native' and z['role']=='component' and z['asset']=='BTC':
  assert sha(ROOT/z['archive'])==z['archive_sha256'];arcs[fp]=json.loads(gzip.decompress((ROOT/z['archive']).read_bytes()))
def flags(arc,cost):
 hurdle=Fraction(str(arc['spec']['parameters'].get('entry_directional_confirmation_hurdle',0)));rows=[]
 for d in arc['scenes'][cost]['decisions']:
  a=d['policy_audit'];before=a['raw_desired_before_confirmation_filter'];applied=a['confirmation_applied'];assert applied==bool(before and before!=d['actual_position_before']) if 'actual_position_before' in d else isinstance(applied,bool)
  blocked=applied and before*Fraction(a['recent_confirmation_ROC_exact'])<=hurdle
  assert d['desired_direction']==(0 if blocked else before)
  rows.append((d['execution_ts_ns'],blocked))
 assert len(rows)==391
 return rows
rows=[]
for fp,arc in arcs.items():
 for k in ['1','2','3']:
  actual,base=flags(arc,k),flags(arcs[basefp],k);assert [x[0] for x in actual]==[x[0] for x in base]
  rows.append({'asset':'BTC','fingerprint':fp,'confirmation_hurdle':arc['spec']['parameters'].get('entry_directional_confirmation_hurdle',0),'cost':int(k),'actual_blocked_decisions':sum(x[1] for x in actual),'old_Q0025_blocked_decisions':sum(x[1] for x in base),'confirmation_block_flag_changes':sum(x[1]!=y[1] for x,y in zip(actual,base)),'exact_saved_policy_decisions_checked':391})
assert sha(R/'report.json')==rhash
with (R/'exports/confirmation_block_flags_corrected.csv').open('w',newline='') as f:w=csv.DictWriter(f,list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
out={'passed':True,'recorded_utc':datetime.now(timezone.utc).isoformat(),'source_binding':'confirmation_checker_binding.json','correction':'joint_economic_review.native_mechanism_rows[*].confirmation_block_flag_changes was computed from absent optional confirmation_blocked fields,so its zero values are invalid diagnostics. Superseded only that column by exact Fraction ROC/hurdle and actual confirmation_applied;all desired directions and monetary comparisons unchanged.','superseded_review_sha256':sha(R/'joint_economic_review.json'),'corrected_native_mechanism_rows':rows,'financial_report_sha256_unchanged':rhash,'new_financial_or_account_calculations':0,'policy_checks_per_cost':391,'missing_diagnostic_not_filled_with_zero':True}
(R/'confirmation_diagnostic_correction.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'corrected_rows':rows,'new_financial_or_account_calculations':0}))
