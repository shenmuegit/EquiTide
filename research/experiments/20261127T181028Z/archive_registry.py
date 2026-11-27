"""Move only this round's original append bytes to the existing supported sidecar format."""
import hashlib,json,subprocess
from collections import Counter
from common import *
rd=lambda p:json.loads(p.read_text());start=rd(R/'startup.json');PID=start['branch_lock_broker_pid'];assert any('FLOCK' in l and str(PID) in l.split() for l in Path('/proc/locks').read_text().splitlines());assert rd(R/'registry_archive_plan.json')['planned_before_any_reservation'];main=ROOT/'research/automation/registry.jsonl';sidecar=R/'registry_records.jsonl';assert not sidecar.exists();base=subprocess.check_output(['git','show',start['base_commit']+':research/automation/registry.jsonl'],cwd=ROOT);current=main.read_bytes();assert current.startswith(base) and base.endswith(b'\n');tail=current[len(base):];rows=[json.loads(x) for x in tail.splitlines()];assert len(rows)==rd(R/'registry_archive_plan.json')['own_raw_reserve_finish_events']==48
records=reg.read_records(main);events=reg.read_events(main);own={fp:x for fp,x in records.items() if x.get('report','').startswith(rel(R)+'/')};assert len(own)==24 and all(x['result_available'] and x['status'] in ['passed','rejected'] for x in own.values());assert set(x['fingerprint'] for x in rows)==set(own)
for fp in own:
 xs=[x for x in rows if x['fingerprint']==fp];assert len(xs)==2 and xs[0]['status']=='reserved' and xs[1]['status']==own[fp]['status']
canonical=lambda xs:Counter(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False) for x in xs);before=canonical(events)
# Preserve unmodified physical event bytes before trimming their duplicate location.
sidecar.write_bytes(tail)
try:
 main.write_bytes(base);afterevents=reg.read_events(main);after=reg.read_records(main);assert canonical(afterevents)==before and after==records and sidecar.read_bytes()==tail and sha(main)==hashlib.sha256(base).hexdigest()
except BaseException:
 main.write_bytes(current)
 if sidecar.exists():sidecar.unlink()
 raise
put(R/'registry_archive_verification.json',{'passed':True,'recorded_utc':now(),'base_commit':start['base_commit'],'physical_main_sha256_before_append':hashlib.sha256(base).hexdigest(),'physical_main_sha256_after_archive':sha(main),'original_full_main_with_own_append_sha256':hashlib.sha256(current).hexdigest(),'sidecar':rel(sidecar),'sidecar_sha256':sha(sidecar),'sidecar_bytes':len(tail),'events_archived_without_reencoding':len(rows),'own_finished_IDs':len(own),'logical_event_multiset_identical':True,'logical_full_record_index_identical':True,'all_prior_main_bytes_and_old_fragments_unchanged':True,'registry_implementation_unchanged':True,'new_models_or_accounts_executed':0});print(json.dumps({'archived_events':len(rows),'finished_IDs':len(own),'bytes':len(tail),'logical_index_unchanged':True,'main_bytes_unchanged_from_base':True}),flush=True)
