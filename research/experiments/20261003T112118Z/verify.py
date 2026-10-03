"""Check all independently reserved and finished outcomes and exact preservation of prior evidence."""
import json,gzip,hashlib,collections,sys,subprocess
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
ROOT=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=ROOT/'research/automation/registry.jsonl';raw=L.read_text().splitlines();records=registry.read_records(L)
assert p['lines']==1993 and p['canonical']==947 and len(p['records'])==949
assert hashlib.sha256(('\n'.join(raw[:1993])+'\n').encode()).hexdigest()==p['ledger_sha256'] and all(records[k]==v for k,v in p['records'].items())
assert len(raw)==2071 and len(records)==988 and len({registry.fingerprint(v['spec']) for v in records.values()})==986
assert all(v['status']!='reserved' and v.get('result_available') for v in records.values())
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());s=r['summary'];notes=json.loads((T/'artifact_notes.json').read_text());audits=[json.loads((T/n).read_text()) for n in ('audit.log','audit_forward.log')];assert all(a['passed'] for a in audits)
assert s['new_configs']==36 and s['new_cost_scenes']==108 and s['reused_grid_configs']==18 and s['reused_cost_scenes']==54
assert len(s['passed'])==18 and len(s['rejected'])==18 and s['positive_3x']==36 and not s['new_both_periods_passed_combination_pairs'] and len(s['both_periods_passed_combination_pairs'])==3
assert all(r['configs'][n]['failed_criteria']==['four_positive_1x_folds'] for n in s['rejected'])
for batch,n,rp,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/batch).read_text()):
  fp=b['fingerprint'];sp=json.loads((ROOT/b['spec']).read_text());assert registry.fingerprint(sp)==fp
  events=[json.loads(z) for z in raw[1993:] if json.loads(z)['fingerprint']==fp];assert len(events)==2 and events[0]['status']=='reserved' and events[1]['status']==rp['configs'][b['name']]['status'];assert events[0]['recorded_at_utc']<start<events[1]['recorded_at_utc']
  assert events[1]['result_available'] and events[1]['report_sha256']==sha(T/n)==records[fp]['report_sha256'] and records[fp]['report']==str((T/n).relative_to(ROOT))
for rp in (r,f):
 for path,h in rp['source_hashes'].items():assert sha(ROOT/path)==h,path
assert r['forward_observation']['sha256']==sha(T/'forward_report.json')
for b in json.loads((T/'grid_batch.json').read_text()):
 sp=json.loads((ROOT/b['spec']).read_text());w=b['raw_weights'];assert w in ([.5,.5],[.55,.45],[.6,.4])
 if b['role']=='component':assert sp['parameters']['initial_capital_usdt']==b['capital_usdt']==int(D(2000)*D(str(w[0 if b['asset']=='BTC' else 1])))
 else:
  assert [c['weight'] for c in sp['components']]==w and b['capital_usdt']==2000
  for c,x in zip(sp['components'],w):assert records[c['fingerprint']]['spec']['parameters']['initial_capital_usdt']==int(D(2000)*D(str(x)))
 if not b['is_new']:
  assert b['BTC_weight']==.6 and records[b['fingerprint']]==p['records'][b['fingerprint']]
  ref=b['source_ref'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/b['spec'])==ref['spec_sha256']
  old=json.loads((ROOT/ref['report']).read_text())['configs'][b['name']];c=r['configs'][b['name']];assert old['scenes']==c['scenes'] and old['status']==c['source_record_status'] and old['criteria']==c['source_record_criteria']
assert f['frozen_plan_sha256']==sha(ROOT/f['frozen_plan_path'])=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
assert f['resume_utc']=='2026-10-03T09:10:00Z' and f['cutoff_utc']=='2026-10-03T11:10:00Z'
assert all(len(z['equity_usdt'])==2112 and z['elapsed_minutes']==2109 and z['new_executions']==0 and z['new_reference_points']==0 for c in f['configs'].values() for z in c['scenes'].values())
state=json.loads((T/'forward_state.json').read_text());old=json.loads((ROOT/f['source_state']).read_text());assert state['positions_by_asset_and_cost']==old['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-04T00:01:00Z'
replay=(T/'reproduce.log').read_text();assert 'PASS:all108 NEW scenes' in replay and 'and54 EXISTING scenes read-only verified' in replay and 'PASS:all9 cumulative forward scenes' in replay and 'PASS: new parameters/weights' in replay
assert len((T/'finish.log').read_text().splitlines())==39 and len((T/'reserve.log').read_text().splitlines())==58 and len(p['legacy_results'])==7 and len(p['legacy_configuration_redaction']['fields'])==2 and len(p['prior_conclusions'])==23
assert notes['audit_failures']==0 and notes['backtest_compute_failures']==0 and notes['ledger_amendment_events']==0
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert base=='c1520be4377142cb008c56339c89a9f08bcba9c1'
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name!='verification.json');paths+=[L,ROOT/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':len(raw),'canonical':986,'preserved_ids':988,'unchanged_prior_rows':1993,'unchanged_prior_records':949,'new_reserved_and_finished':39,'new_events':78,'statuses':dict(collections.Counter(x['status'] for x in records.values())),'pending':0},'historical_summary':s,'audits':audits,'replay':'108new+54read-only+9partial scenes exact; no newHTTP/ledger writes','limitations':['Repeated development histories,not untouched final test.','50/50and55/45 positive2026total but fail3of6positivefolds; no newcrossperiod candidate.','Only2newrealized2026combinationNAVs,not6independent samples.','Original frozen observer only2109minutes,no live profit evidence.','Static filters and assumed costs lack empirical L2/TCA calibration.'],'artifact_notes':notes,'files_sha256':{str(q.relative_to(ROOT)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'registry':v['registry']},ensure_ascii=False))
