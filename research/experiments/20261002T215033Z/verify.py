"""Verify preserved research history and all new actual-result reservations before commit."""
import collections,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';before=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));raw=ledger.read_text().splitlines();records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert hashlib.sha256(('\n'.join(raw[:before['lines']])+'\n').encode()).hexdigest()==before['ledger_sha256']
assert before['lines']==1492 and before['canonical']==734 and len(before['records'])==736
assert all(records[fp]==v for fp,v in before['records'].items())
assert len(raw)==1570 and len(records)==775 and len(canonical)==773
assert all(v['status']!='reserved' and v.get('result_available') for v in records.values())
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());audits=[json.loads((ROUND/p).read_text()) for p in ['audit.log','audit_forward.log']];assert all(a['passed'] for a in audits)
assert len(r['configs'])==36 and len(f['configs'])==3 and len(r['component_sources'])==24
assert len(r['summary']['passed'])==25 and len(r['summary']['rejected'])==11 and len(r['summary']['both_periods_passed_pairs'])==7
for rp in [r,f]:
 for path,h in rp['source_hashes'].items():assert sha(ROOT/path)==h,path
for batchfile,rp,path,start in [('batch.json',r,ROUND/'report.json',r['evaluation_started_utc']),('forward_batch.json',f,ROUND/'forward_report.json',f['observation_started_utc'])]:
 for b in json.loads((ROUND/batchfile).read_text()):
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==fp;events=[json.loads(x) for x in raw[1492:] if json.loads(x)['fingerprint']==fp];assert len(events)==2 and events[0]['status']=='reserved' and events[1]['status']==rp['configs'][b['name']]['status'];assert events[0]['recorded_at_utc']<start<events[1]['recorded_at_utc'];assert records[fp]['report']==str(path.relative_to(ROOT)) and records[fp]['report_sha256']==sha(path)
for ref in r['component_sources'].values():
 assert records[ref['fingerprint']]==before['records'][ref['fingerprint']]
 for p,h in [('archive','archive_sha256'),('report','report_sha256'),('spec','spec_sha256')]:assert sha(ROOT/ref[p])==ref[h]
assert f['source_report_sha256']==sha(ROOT/f['source_report']) and f['source_state_sha256']==sha(ROOT/f['source_state'])
assert f['frozen_plan_sha256']==sha(ROOT/f['frozen_plan_path'])=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
assert f['resume_utc']=='2026-10-02T19:40:00Z' and f['cutoff_utc']=='2026-10-02T21:40:00Z'
assert all(len(z['equity_usdt'])==1301 and z['elapsed_minutes']==1299 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
replay=(ROUND/'reproduce.log').read_text();assert 'PASS:all108 channel/EMA archives' in replay and 'PASS:all9 cumulative forward scenes' in replay and 'PASS: new parameters/weights' in replay
assert len((ROUND/'finish.log').read_text().splitlines())==39 and len((ROUND/'reserve.log').read_text().splitlines())==40
assert len((ROUND/'sensitivity.csv').read_text().splitlines())==109
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert base=='6cb3e0f3e8fe6778a45407b5f3558003f289666c'
paths=sorted(p for p in ROUND.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='verification.json');paths += [ledger,ROOT/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'pre_commit_snapshot':True,'base_commit':base,'historical_report_sha256':sha(ROUND/'report.json'),'forward_report_sha256':sha(ROUND/'forward_report.json'),
'registry':{'rows':len(raw),'canonical':len(canonical),'preserved_ids':len(records),'statuses':dict(collections.Counter(v['status'] for v in records.values())),'unchanged_prior_records':len(before['records']),'unchanged_prior_rows':before['lines'],'new_configs_reserved_and_finished':39,'new_events':78,'pending':0,'all_results_available':True},
'scope':{'new_historical_combinations':36,'new_historical_cost_scenes':108,'read_only_component_configs':24,'read_only_component_cost_scenes':72,'read_only_component_simulated_fills':r['summary']['source_component_fills_read_only'],'new_component_backtests':0,'new_forward_snapshots':3,'new_forward_scenes':9,'positive_new_historical_all_costs':36,'passed_new_historical':25,'rejected_new_historical':11,'both_period_combo_pairs':7,'live_orders':0},
'independent_audits':audits,'exact_replay':{'new_historical_scenes':108,'new_cumulative_forward_scenes':9,'ledger_unchanged':True,'new_HTTP_requests':0},'frozen_forward_plan_sha256':f['frozen_plan_sha256'],
'limitations':['Both historical periods repeatedly used for development;not untouched final tests.','36distinct portfolio NAV still share components and history;not independent samples.','2026 gains remain concentrated in finalfold;fixed center reversedirection failedfoldgate.','Frozen cumulative observation remains negative,only1299minutes/0full days;delayed shadow reconstruction,not live execution.','Static exchange filters and assumed spread/slippage/impact lack historical L2/TCA/empirical capacity calibration.'],
'push_verification':'After committing,verify connected GitHub ref,parent/tree and all local file hashes;final brief states confirmed commit and push status.',
'files_sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}}
(ROUND/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v[k] for k in ['passed','registry','scope']},ensure_ascii=False))
