"""Verify exact reservations/outcomes, unchanged historical evidence and local artifact binding."""
import collections,csv,gzip,hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
T=Path(__file__).resolve().parent;ROOT=T.parents[2];sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=ROOT/'research/automation/registry.jsonl';raw=L.read_bytes().splitlines(keepends=True);records=registry.read_records(L)
assert (p['lines'],p['canonical'],len(p['records']),len(p['prior_conclusions']))==(2773,1337,1339,33)
assert hashlib.sha256(b''.join(raw[:p['lines']])).hexdigest()==p['ledger_sha256'] and all(records[k]==v for k,v in p['records'].items())
assert (len(raw),len(records),len({registry.fingerprint(v['spec']) for v in records.values()}))==(2851,1378,1376)
assert all(v['status']!='reserved' and v.get('result_available') for v in records.values())
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());diag=json.loads((T/'diagnostic.json').read_text());s=r['summary'];notes=json.loads((T/'artifact_notes.json').read_text());audits=[json.loads((T/q).read_text()) for q in ('audit.log','audit_forward.log')]
assert all(a['passed'] for a in audits) and (s['new_configs'],s['new_cost_scenes'],s['reused_grid_configs'],s['reused_cost_scenes'])==(36,108,18,54)
assert len(s['passed'])==15 and len(s['rejected'])==21 and s['positive_3x']==36 and len(s['new_both_periods_passed_combination_pairs'])==3
assert collections.Counter(k for c in r['configs'].values() if c['is_new'] for k in c['failed_criteria'])=={'four_positive_1x_folds':18,'minute_DD3_lte25pct':3}
for bfile,rfile,rp,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bfile).read_text()):
  fp=b['fingerprint'];sp=json.loads((ROOT/b['spec']).read_text());assert registry.fingerprint(sp)==fp
  events=[json.loads(z) for z in raw[p['lines']:] if json.loads(z)['fingerprint']==fp]
  assert len(events)==2 and events[0]['status']=='reserved' and events[1]['status']==rp['configs'][b['name']]['status']
  assert events[0]['recorded_at_utc']<start<events[1]['recorded_at_utc'] and events[1]['result_available']
  assert records[fp]['report_sha256']==events[1]['report_sha256']==sha(T/rfile)
for rp in (r,f):
 for path,h in rp['source_hashes'].items():assert sha(ROOT/path)==h,path
assert r['forward_observation']['sha256']==sha(T/'forward_report.json') and diag['source_report_sha256']==sha(T/'report.json')
assert diag['identical_new_scenes_to_matching_old_exit30']==63 and diag['all_new_cross_period_qualified_NAVs_identical_to_old_exit30'] and diag['new_cross_period_qualified_distinct_NAV_pairs']==0
assert len(diag['comparisons'])==108 and diag['combo_2026_unique_3x_NAVs']==2 and len(diag['all_2026_combo_first5_3x_return_pct'])==1
assert r['plan']['grid']['predeclared_center']==[15,30] and r['plan']['grid']['center_is_read_only_existing_anchor'] is True
for b in json.loads((T/'grid_batch.json').read_text()):
 sp=json.loads((ROOT/b['spec']).read_text());assert b['raw_weights']==[.675,.325] and b['exit_days'] in (20,30,40) and b['entry_days'] in (10,15,20)
 if b['role']=='component':assert sp['parameters']['initial_capital_usdt']==b['capital_usdt']==(1350 if b['asset']=='BTC' else 650) and sp['parameters']['exit_lookback_days']==b['exit_days'] and sp['parameters']['entry_lookback_days']==b['entry_days']
 else:
  assert [c['weight'] for c in sp['components']]==b['raw_weights']
  for c,w in zip(sp['components'],b['raw_weights']):assert records[c['fingerprint']]['spec']['parameters']['initial_capital_usdt']==int(D(2000)*D(str(w))) and records[c['fingerprint']]['spec']['parameters']['exit_lookback_days']==b['exit_days']
 if b['is_new']:assert b['exit_days'] in (20,40)
 else:
  assert b['exit_days']==30 and records[b['fingerprint']]==p['records'][b['fingerprint']];ref=b['source_ref']
  assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/b['spec'])==ref['spec_sha256']
  old=json.loads((ROOT/ref['report']).read_text())['configs'][b['name']];assert old['scenes']==r['configs'][b['name']]['scenes']
with (T/'sensitivity.csv').open() as z:
 table=list(csv.DictReader(z));assert len(table)==162 and all(None not in c and None not in c.values() for c in table)
 for c in table:assert int(c['exit_days'])==r['configs'][c['config']]['exit_days'] and float(c['BTC_initial_weight'])==.675
assert f['frozen_plan_sha256']==sha(ROOT/f['frozen_plan_path'])=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
assert f['resume_utc']=='2026-10-04T23:10:00Z' and f['cutoff_utc']=='2026-10-05T01:10:00Z'
assert all(len(z['equity_usdt'])==4394 and z['elapsed_minutes']==4389 and z['elapsed_complete_days']==3 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
old=json.loads((ROOT/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-06T00:01:00Z'
assert {a:d['action'] for a,d in f['daily_decisions_by_asset'].items()}=={'BTC':'hold_long','ETH':'hold_long'} and all(d['executed_at_utc']=='2026-10-05T00:01:00Z' for d in f['daily_decisions_by_asset'].values())
replay=(T/'reproduce.log').read_text();assert all(x in replay for x in ('PASS:all108 NEW scenes','and54 EXISTING scenes read-only verified','PASS:all9 cumulative forward scenes','PASS: new parameters/weights'))
assert len((T/'finish.log').read_text().splitlines())==39 and len((T/'reserve.log').read_text().splitlines())==58
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert base=='ee38a411cdbeb9f10f0bbdd77be1f392e3624547'
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name!='verification.json');paths+=[L,ROOT/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':len(raw),'canonical':1376,'preserved_ids':1378,'unchanged_prior_rows':2773,'unchanged_prior_records':1339,'new_reserved_and_finished':39,'new_events':78,'statuses':dict(collections.Counter(x['status'] for x in records.values())),'pending':0},'historical_summary':s,'audits':audits,'replay':'108new+54readonly+9partial exact,noHTTP or ledgerwrites','artifact_notes':notes,'limitations':['Repeated development histories;no untouchedholdout','Three qualified new exit40parameterpairs share all oldexit30NAVs','2026firstfivefold loss unchanged;profit concentrated lastfold','Original observer73h9m partial delayedshadow,no stable liveprofit','Estimated costs/IOCfilters not TCA calibrated'],'files_sha256':{str(q.relative_to(ROOT)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'registry':v['registry']},ensure_ascii=False))
