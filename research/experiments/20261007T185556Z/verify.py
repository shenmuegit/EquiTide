"""Verify preserved history, actual results, chronological ledger and reproducibility."""
import csv,gzip,hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
T=Path(__file__).resolve().parent;R=T.parents[2];sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);rr=registry.read_records(L)
assert (p['lines'],p['canonical'],len(p['records']),len(p['prior_conclusions']))==(4451,2176,2178,54)
assert hashlib.sha256(b''.join(lines[:p['lines']])).hexdigest()==p['ledger_sha256'] and all(rr[k]==v for k,v in p['records'].items())
assert (len(lines),len(rr),len({registry.fingerprint(v['spec']) for v in rr.values()}))==(4529,2217,2215)
assert all(v['status']!='reserved' and (v.get('result_available') or v['spec'].get('parameters',{}).get('owner_automation_id')=='btc-eth-2') for v in rr.values())
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());audits=[json.loads((T/q).read_text()) for q in ('audit.log','audit_forward.log')];assert all(a['passed'] for a in audits)
assert len(r['summary']['passed'])+len(r['summary']['rejected'])==36
for batch,report,rp,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/batch).read_text()):
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==fp
  ev=[json.loads(z) for z in lines[p['lines']:] if json.loads(z)['fingerprint']==fp];assert len(ev)==2 and ev[0]['status']=='reserved' and ev[0]['recorded_at_utc']<start<ev[1]['recorded_at_utc'] and ev[1]['status']==rp['configs'][b['name']]['status'] and ev[1]['report_sha256']==sha(T/report)
for rp in (r,f):
 for path,h in rp['source_hashes'].items():assert sha(R/path)==h,path
for path,h in r['plan']['reused_code_sha256'].items():assert sha(R/path)==h,path
for b in json.loads((T/'grid_batch.json').read_text()):
 assert b['exit_days']==30 and b['raw_weights'] in [[.575,.425],[.60,.40],[.625,.375]]
 if not b['is_new']:assert b['BTC_weight']==.60 and rr[b['fingerprint']]==p['records'][b['fingerprint']]
 if b['role']=='component':
  sp=json.loads((R/b['spec']).read_text());assert 'EMA_span_days' not in sp['parameters'] and sp['parameters']['initial_capital_usdt']==b['capital_usdt']
with (T/'sensitivity.csv').open() as fh:
 rows=list(csv.DictReader(fh));assert len(rows)==162 and all(None not in x and None not in x.values() for x in rows)
 for x in rows:assert float(x['BTC_initial_weight'])==r['configs'][x['config']]['BTC_weight']
assert r['plan']['grid']['predeclared_center']==[15,.60]
assert all(len(z['equity_usdt'])==8326 and z['elapsed_minutes']==8319 and z['elapsed_complete_days']==5 and z['new_reference_points']==0 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-08T00:01:00Z'
replay=(T/'reproduce.log').read_text();assert all(x in replay for x in ('PASS:all108 NEW scenes','and54 EXISTING scenes read-only verified','PASS:all9 cumulative forward scenes','PASS: new parameters/weights'))
assert len((T/'finish.log').read_text().splitlines())==39
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json') and h['new_scenes_already_in_any_prior_report']+h['new_scenes_not_in_any_prior_report']==108
for path,hv in h['all_prior_report_sha256'].items():assert sha(R/path)==hv
assert sha(R/'research/paper10/state.json')==p['paper10_live_state_sha256'] and sha(R/'research/paper10/plan.json')==p['paper10_plan_sha256']
base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert base==p['base_commit']
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name!='verification.json')+[L,R/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':4529,'canonical':2215,'preserved_ids':2217,'unchanged_prior_rows':4451,'new_reserved_and_finished':39,'pending':0},'historical_summary':r['summary'],'audits':audits,'files_sha256':{str(q.relative_to(R)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v['registry']))
