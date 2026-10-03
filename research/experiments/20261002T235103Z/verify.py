"""Verify preserved research history and all new actual-result reservations before commit."""
import collections,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';before=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));raw=ledger.read_text().splitlines();records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert hashlib.sha256(('\n'.join(raw[:before['lines']])+'\n').encode()).hexdigest()==before['ledger_sha256']
assert before['lines']==1570 and before['canonical']==773 and len(before['records'])==775
assert all(records[fp]==v for fp,v in before['records'].items())
assert len(raw)==1684 and len(records)==832 and len(canonical)==830
assert all(v['status']!='reserved' and v.get('result_available') for v in records.values())
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());audits=[json.loads((ROUND/p).read_text()) for p in ['audit.log','audit_forward.log']];assert all(a['passed'] for a in audits)
assert len(r['configs'])==54 and len(f['configs'])==3
assert len(r['summary']['passed'])==30 and len(r['summary']['rejected'])==24 and len(r['summary']['both_periods_passed_combination_pairs'])==3
for rp in [r,f]:
 for path,h in rp['source_hashes'].items():assert sha(ROOT/path)==h,path
for batchfile,rp,path,start in [('batch.json',r,ROUND/'report.json',r['evaluation_started_utc']),('forward_batch.json',f,ROUND/'forward_report.json',f['observation_started_utc'])]:
 for b in json.loads((ROUND/batchfile).read_text()):
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==fp;events=[json.loads(x) for x in raw[1570:] if json.loads(x)['fingerprint']==fp];assert len(events)==2 and events[0]['status']=='reserved' and events[1]['status']==rp['configs'][b['name']]['status'];assert events[0]['recorded_at_utc']<start<events[1]['recorded_at_utc'];assert records[fp]['report']==str(path.relative_to(ROOT)) and records[fp]['report_sha256']==sha(path)
assert f['source_report_sha256']==sha(ROOT/f['source_report']) and f['source_state_sha256']==sha(ROOT/f['source_state'])
assert f['frozen_plan_sha256']==sha(ROOT/f['frozen_plan_path'])=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
assert f['resume_utc']=='2026-10-02T21:40:00Z' and f['cutoff_utc']=='2026-10-02T23:40:00Z'
assert r['plan']['count_correction']['corrected_at_utc']<f['observation_started_utc']
for ref in r['plan']['count_correction']['failed_attempts']:assert sha(ROOT/ref['path'])==ref['sha256']
assert sum(all(z['net_return_pct']<0 for z in c['scenes'].values()) for c in r['configs'].values())==3
assert r['summary']['actual_component_fills']==570 and audits[0]['current_or_future_close_perturbations']==108
assert all(len(z['equity_usdt'])==1421 and z['elapsed_minutes']==1419 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
replay=(ROUND/'reproduce.log').read_text();assert 'PASS:all162 NEW scenes' in replay and 'PASS:all9 cumulative forward scenes' in replay and 'PASS: new parameters/weights' in replay
assert len((ROUND/'finish.log').read_text().splitlines())==57 and len((ROUND/'reserve.log').read_text().splitlines())==58
assert len((ROUND/'sensitivity.csv').read_text().splitlines())==163
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert base=='dc692309d21a1844d72828111065c98cc88e57dd'
paths=sorted(p for p in ROUND.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='verification.json');paths += [ledger,ROOT/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'pre_commit_snapshot':True,'base_commit':base,'historical_report_sha256':sha(ROUND/'report.json'),'forward_report_sha256':sha(ROUND/'forward_report.json'),
'registry':{'rows':len(raw),'canonical':len(canonical),'preserved_ids':len(records),'statuses':dict(collections.Counter(v['status'] for v in records.values())),'unchanged_prior_records':len(before['records']),'unchanged_prior_rows':before['lines'],'new_configs_reserved_and_finished':57,'new_events':114,'pending':0,'all_results_available':True},
'scope':{'new_historical_configs':54,'new_historical_components':36,'new_historical_combinations':18,'new_historical_cost_scenes':162,'new_simulated_component_fills':570,'new_forward_snapshots':3,'new_forward_scenes':9,'positive_new_historical_all_costs':51,'negative_new_historical_all_costs':3,'passed_new_historical':30,'rejected_new_historical':24,'both_period_combo_pairs':3,'live_orders':0},
'independent_audits':audits,'exact_replay':{'new_historical_scenes':162,'new_cumulative_forward_scenes':9,'ledger_unchanged':True,'new_HTTP_requests':0},'frozen_forward_plan_sha256':f['frozen_plan_sha256'],
'limitations':['Both histories repeatedly used for development;not untouched final tests.','Three cross-period passed parameter combinations share identical2026NAV;not independent samples.','Predeclared EMA65 center rejected in2026;profit remains concentrated in finalfold.','Frozen cumulative observation negative,only1419minutes/0full days;delayed shadow reconstruction,not live execution.','Static exchange filters and assumed spread/slippage/impact lack historical L2/TCA/empirical capacity calibration.'],
'first_engineering_failure':json.loads((ROUND/'failed_attempts/manifest.json').read_text()),
'push_verification':'After committing,verify connected GitHub ref,parent/tree and all local file hashes;final brief states confirmed commit and push status.',
'files_sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}}
(ROUND/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v[k] for k in ['passed','registry','scope']},ensure_ascii=False))
