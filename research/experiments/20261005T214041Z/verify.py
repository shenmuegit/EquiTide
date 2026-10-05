import json,gzip,hashlib,sys,subprocess,collections
from pathlib import Path
from datetime import datetime,timezone
T=Path(__file__).resolve().parent;R=T.parents[2];sys.path.insert(0,str(R/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=json.loads(gzip.decompress((T/'prior_summary.json.gz').read_bytes()));L=R/'research/automation/registry.jsonl';lines=L.read_bytes().splitlines(keepends=True);rr=registry.read_records(L)
assert (p['lines'],p['canonical'],len(p['records']),len(p['prior_conclusions']))==(3553,1727,1729,43)
assert hashlib.sha256(b''.join(lines[:3553])).hexdigest()==p['ledger_sha256'] and all(rr[k]==v for k,v in p['records'].items())
assert (len(lines),len(rr),len({registry.fingerprint(v['spec']) for v in rr.values()}))==(3631,1768,1766)
assert all(v.get('result_available') and v['status']!='reserved' for v in rr.values())
audits=[json.loads((T/q).read_text()) for q in ('audit.log','audit_forward.log')];assert all(a['passed'] for a in audits)
r=json.loads((T/'report.json').read_text());f=json.loads((T/'forward_report.json').read_text());assert len(r['summary']['passed'])+len(r['summary']['rejected'])==36 and r['summary']['new_configs']==36
for bf,rf,rp,start in [('batch.json','report.json',r,r['evaluation_started_utc']),('forward_batch.json','forward_report.json',f,f['observation_started_utc'])]:
 for b in json.loads((T/bf).read_text()):
  fp=b['fingerprint'];assert registry.fingerprint(json.loads((R/b['spec']).read_text()))==fp
  ev=[json.loads(z) for z in lines[3553:] if json.loads(z)['fingerprint']==fp];assert len(ev)==2 and ev[0]['status']=='reserved' and ev[0]['recorded_at_utc']<start<ev[1]['recorded_at_utc'] and ev[1]['status']==rp['configs'][b['name']]['status'] and ev[1]['report_sha256']==sha(T/rf)
for rp in [r,f]:
 for path,h in rp['source_hashes'].items():assert sha(R/path)==h,path
for b in json.loads((T/'grid_batch.json').read_text()):
 assert b['exit_days']==30 and b['EMA_band']==.03 and b['span_days'] in (25,50,75) and b['raw_weights']==[.675,.325]
 if not b['is_new']:assert b['exit_days']==30 and b['EMA_band']==.03 and b['span_days']==50 and rr[b['fingerprint']]==p['records'][b['fingerprint']]
import csv
with (T/'sensitivity.csv').open() as fh:
 rows=list(csv.DictReader(fh));assert len(rows)==162 and all(None not in x and None not in x.values() for x in rows)
 for row in rows:assert float(row['EMA_symmetric_band'])==r['configs'][row['config']]['EMA_band'] and int(row['EMA_span_days'])==r['configs'][row['config']]['span_days']
for c in r['configs'].values():
 if c['role']=='component':
  sp=json.loads((R/c['spec']).read_text());assert sp['parameters']['EMA_symmetric_band']==c['EMA_band'] and sp['parameters']['EMA_span_days']==c['span_days']
assert r['plan']['grid']['predeclared_center']==[15,50] and r['plan']['grid']['exit_lookback_days']==[30]
assert all(len(z['equity_usdt'])==5594 and z['elapsed_minutes']==5589 and z['elapsed_complete_days']==3 and z['new_executions']==0 for c in f['configs'].values() for z in c['scenes'].values())
old=json.loads((R/f['source_state']).read_text());state=json.loads((T/'forward_state.json').read_text());assert old['positions_by_asset_and_cost']==state['positions_by_asset_and_cost'] and state['next_daily_decision_utc']=='2026-10-06T00:01:00Z'
replay=(T/'reproduce.log').read_text();assert all(x in replay for x in ('PASS:all108 NEW scenes','and54 EXISTING scenes read-only verified','PASS:all9 cumulative forward scenes','PASS: new parameters/weights'))
assert len((T/'finish.log').read_text().splitlines())==39
h=json.loads((T/'history_paths.json').read_text());assert h['report_sha256']==sha(T/'report.json') and h['new_scenes_already_in_any_prior_report']+h['new_scenes_not_in_any_prior_report']==108
for path,hv in h['all_prior_report_sha256'].items():assert sha(R/path)==hv
base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert base=='695681559c1d73c634d8bf1cf35ce4249bcac4d0'
paths=sorted(q for q in T.rglob('*') if q.is_file() and '__pycache__' not in q.parts and q.name!='verification.json')+[L,R/'research/automation/README.md']
v={'passed':True,'verified_at_utc':datetime.now(timezone.utc).isoformat(),'base_commit':base,'registry':{'rows':3631,'canonical':1766,'preserved_ids':1768,'unchanged_prior_rows':3553,'new_reserved_and_finished':39,'pending':0},'historical_summary':r['summary'],'audits':audits,'files_sha256':{str(q.relative_to(R)):sha(q) for q in paths}}
(T/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v['registry']))
