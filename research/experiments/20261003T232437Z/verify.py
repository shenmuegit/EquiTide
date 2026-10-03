"""Verify reservations preceded calculations, all outcomes finished, old evidence retained, and artifact hashes."""
import json,gzip,hashlib,sys,subprocess,collections
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal as D
T=Path(__file__).resolve().parent;ROOT=T.parents[2]
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=ROOT/'research/automation/registry.jsonl';raw=L.read_bytes().splitlines(keepends=True);records=registry.read_records(L)
assert p['lines']==2305 and p['canonical']==1103 and len(p['records'])==1105
assert hashlib.sha256(b''.join(raw[:p['lines']])).hexdigest()==p['ledger_sha256'] and all(records[k]==v for k,v in p['records'].items())
assert len(raw)==2383 and len(records)==1144 and len({registry.fingerprint(v['spec']) for v in records.values()})==1142
assert all(v['status']!='reserved' and v.get('result_available') for v in records.values())
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());s=r['summary'];notes=json.loads((T/'artifact_notes.json').read_text());audits=[json.loads((T/n).read_text()) for n in ('audit.log','audit_forward.log')];assert all(a['passed'] for a in audits)
assert (s['new_configs'],s['new_cost_scenes'],s['reused_grid_configs'],s['reused_cost_scenes'])==(36,108,18,54)
assert len(s['passed'])==24 and len(s['rejected'])==12 and s['positive_3x']==36 and len(s['new_both_periods_passed_combination_pairs'])==6
assert all(r['configs'][n]['failed_criteria']==['four_positive_1x_folds'] for n in s['rejected'])
for bfile,rfile,rp,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bfile).read_text()):
  fp=b['fingerprint'];sp=json.loads((ROOT/b['spec']).read_text());assert registry.fingerprint(sp)==fp
  ev=[json.loads(z) for z in raw[p['lines']:] if json.loads(z)['fingerprint']==fp]
  assert len(ev)==2 and ev[0]['status']=='reserved' and ev[1]['status']==rp['configs'][b['name']]['status']
  assert ev[0]['recorded_at_utc']<start<ev[1]['recorded_at_utc'] and ev[1]['result_available']
  assert records[fp]['report_sha256']==ev[1]['report_sha256']==sha(T/rfile) and records[fp]['report']==str((T/rfile).relative_to(ROOT))
for rp in (r,f):
 for path,h in rp['source_hashes'].items():assert sha(ROOT/path)==h,path
assert r['forward_observation']['sha256']==sha(T/'forward_report.json')
for b in json.loads((T/'grid_batch.json').read_text()):
 sp=json.loads((ROOT/b['spec']).read_text());w=b['raw_weights'];assert w in ([.655,.345],[.675,.325],[.695,.305])
 if b['role']=='component':assert sp['parameters']['initial_capital_usdt']==b['capital_usdt']==int(D(2000)*D(str(w[0 if b['asset']=='BTC' else 1])))
 else:
  assert [c['weight'] for c in sp['components']]==w
  for c,x in zip(sp['components'],w):assert records[c['fingerprint']]['spec']['parameters']['initial_capital_usdt']==int(D(2000)*D(str(x)))
 if not b['is_new']:
  assert b['BTC_weight']==.675 and records[b['fingerprint']]==p['records'][b['fingerprint']]
  ref=b['source_ref'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/b['spec'])==ref['spec_sha256']
  old=json.loads((ROOT/ref['report']).read_text())['configs'][b['name']];assert old['scenes']==r['configs'][b['name']]['scenes']
assert f['frozen_plan_sha256']==sha(ROOT/f['frozen_plan_path'])=='2798390f02bd43059097cf16f9b8b1f30db4b96776431c18684b540130f86d81'
assert f['resume_utc']=='2026-10-03T21:10:00Z' and f['cutoff_utc']=='2026-10-03T23:10:00Z'
assert all(len(z['equity_usdt'])==2832 and z['elapsed_minutes']==2829 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
old=json.loads((ROOT/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-04T00:01:00Z'
replay=(T/'reproduce.log').read_text();assert all(x in replay for x in ('PASS:all108 NEW scenes','and54 EXISTING scenes read-only verified','PASS:all9 cumulative forward scenes','PASS: new parameters/weights'))
assert len((T/'finish.log').read_text().splitlines())==39 and len((T/'reserve.log').read_text().splitlines())==58 and len(p['prior_conclusions'])==27
base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert base=='e85f82c685337f759544f96c6d0095778481c7cf'
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name!='verification.json');paths+=[L,ROOT/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':len(raw),'canonical':1142,'preserved_ids':1144,'unchanged_prior_rows':2305,'unchanged_prior_records':1105,'new_reserved_and_finished':39,'new_events':78,'statuses':dict(collections.Counter(x['status'] for x in records.values())),'pending':0},'historical_summary':s,'audits':audits,'replay':'108new+54readonly+9partial exact;noHTTP/ledgerwrites','artifact_notes':notes,'limitations':['Repeated development histories, not final untouched holdout','Six new combinations but only two 2026 realized NAV paths','2026 profits concentrated last fold','Original observer47h9m partial, no stable live profit','Assumed costs/filters/IOC execution lack TCA calibration'],'files_sha256':{str(q.relative_to(ROOT)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':True,'registry':v['registry']},ensure_ascii=False))
