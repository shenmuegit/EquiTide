"""Verify preserved ledger, independent actual-result reservations, reuse and original daily continuation before commit."""
import collections,gzip,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ledger=ROOT/'research/automation/registry.jsonl';before=json.loads(gzip.decompress((ROUND/'prior_summary.json.gz').read_bytes()));raw=ledger.read_text().splitlines();records=registry.read_records(ledger);canonical={registry.fingerprint(v['spec']) for v in records.values()}
assert before['lines']==1684 and before['canonical']==830 and len(before['records'])==832
assert hashlib.sha256(('\n'.join(raw[:1684])+'\n').encode()).hexdigest()==before['ledger_sha256'] and all(records[fp]==v for fp,v in before['records'].items())
assert len(raw)==1762 and len(records)==871 and len(canonical)==869 and all(v['status']!='reserved' and v.get('result_available') for v in records.values())
r=json.loads((ROUND/'report.json').read_text());f=json.loads((ROUND/'forward_report.json').read_text());audits=[json.loads((ROUND/p).read_text()) for p in ('audit.log','audit_forward.log')];assert all(a['passed'] for a in audits)
s=r['summary'];assert s['new_configs']==36 and s['new_component_configs']==24 and s['new_combination_configs']==12 and s['new_cost_scenes']==108
assert len(s['passed'])==6 and len(s['rejected'])==30 and s['positive_1x']==36 and s['positive_3x']==35 and not s['new_both_periods_passed_combination_pairs']
assert len(s['both_periods_passed_combination_pairs'])==3 and s['reused_grid_configs']==18 and s['reused_cost_scenes']==54 and s['actual_component_fills']==570 and s['audited_component_fills']==750
for rp in (r,f):
 for path,h in rp['source_hashes'].items():assert sha(ROOT/path)==h,path
for bf,rp,path,start in [('batch.json',r,ROUND/'report.json',r['evaluation_started_utc']),('forward_batch.json',f,ROUND/'forward_report.json',f['observation_started_utc'])]:
 for b in json.loads((ROUND/bf).read_text()):
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==fp;events=[json.loads(x) for x in raw[1684:] if json.loads(x)['fingerprint']==fp]
  assert len(events)==2 and events[0]['status']=='reserved' and events[1]['status']==rp['configs'][b['name']]['status'] and events[1]['result_available'];assert events[0]['recorded_at_utc']<start<events[1]['recorded_at_utc']
  assert records[fp]['report']==str(path.relative_to(ROOT)) and records[fp]['report_sha256']==sha(path)
gb=json.loads((ROUND/'grid_batch.json').read_text());old=[b for b in gb if not b['is_new']];assert len(gb)==54 and len(old)==18
for b in old:
 ref=b['source_ref'];assert records[b['fingerprint']]==before['records'][b['fingerprint']]
 assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/b['spec'])==ref['spec_sha256']
 source=json.loads((ROOT/ref['report']).read_text())['configs'][b['name']];current=r['configs'][b['name']];assert source['scenes']==current['scenes'] and source['status']==current['source_record_status'] and source['criteria']==current['source_record_criteria']
assert f['frozen_plan_sha256']==sha(ROOT/f['frozen_plan_path'])=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
assert f['resume_utc']=='2026-10-02T23:40:00Z' and f['cutoff_utc']=='2026-10-03T01:40:00Z'
assert all(len(z['equity_usdt'])==1542 and z['elapsed_minutes']==1539 and z['elapsed_complete_days']==1 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
assert all(d['action']=='hold_long' for d in f['daily_decisions_by_asset'].values());state=json.loads((ROUND/'forward_state.json').read_text());oldstate=json.loads((ROOT/f['source_state']).read_text());assert state['positions_by_asset_and_cost']==oldstate['positions_by_asset_and_cost']
assert state['next_daily_decision_utc']=='2026-10-04T00:01:00Z';assert audits[0]['current_or_future_close_perturbations']==72 and audits[1]['original_daily_decisions_independently_checked']==6
replay=(ROUND/'reproduce.log').read_text();assert 'PASS:all108 NEW scenes' in replay and 'and54 EXISTING scenes read-only verified' in replay and 'PASS:all9 cumulative forward scenes' in replay and 'PASS: new parameters/weights' in replay
assert len((ROUND/'finish.log').read_text().splitlines())==39 and len((ROUND/'reserve.log').read_text().splitlines())==58 and len((ROUND/'sensitivity.csv').read_text().splitlines())==163
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert base=='016e09c113920aa40b7a73e4d9c7510fff6c20cb'
paths=sorted(p for p in ROUND.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='verification.json');paths += [ledger,ROOT/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'pre_commit_snapshot':True,'base_commit':base,'historical_report_sha256':sha(ROUND/'report.json'),'forward_report_sha256':sha(ROUND/'forward_report.json'),
 'registry':{'rows':len(raw),'canonical':len(canonical),'preserved_ids':len(records),'statuses':dict(collections.Counter(v['status'] for v in records.values())),'unchanged_prior_records':832,'unchanged_prior_rows':1684,'new_configs_reserved_and_finished':39,'new_events':78,'pending':0,'all_results_available':True},
 'scope':{'new_historical_configs':36,'new_historical_components':24,'new_historical_combinations':12,'new_historical_cost_scenes':108,'reused_historical_configs':18,'reused_historical_cost_scenes':54,'new_simulated_component_fills':570,'audited_including_old_fills':750,'new_forward_snapshots':3,'new_forward_scenes':9,'positive_new_historical_1x':36,'positive_new_historical_3x':35,'cost3_loss_new_historical':1,'passed_new_historical':6,'rejected_new_historical':30,'new_both_period_combo_pairs':0,'old_both_period_combo_pairs':3,'live_orders':0},
 'independent_audits':audits,'exact_replay':{'new_historical_scenes':108,'existing_historical_scenes_read_only':54,'new_cumulative_forward_scenes':9,'ledger_unchanged':True,'new_HTTP_requests':0},'frozen_forward_plan_sha256':f['frozen_plan_sha256'],
 'limitations':['Both histories repeatedly used for development;not untouched final tests.','Six newly passed2026 combinations all fail corresponding2025 fold criterion;no new cross-period passing parameters.','Faster exits have mixed risk/concentration/return tradeoffs;prior shared-NAV cross-period candidates retained as historical evidence only.','Frozen original observer only1539minutes/1complete day and negative;delayed shadow reconstruction,no real-time execution.','Static historical exchange filters and assumed spread/slippage/impact lack empirical L2/TCA/capacity calibration.'],
 'push_verification':'Final brief confirms remote ref,parent/tree and exact local/staged bytes after force=false update.',
 'files_sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths}}
(ROUND/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v[k] for k in ('passed','registry','scope')},ensure_ascii=False))
