"""Frozen spec, per-config reserve/finish, allocation, report, and paper10 continuity checks."""
import hashlib,json,sys
from decimal import Decimal as D
from pathlib import Path
T=Path(__file__).resolve().parent;ROOT=T.parents[2]
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
batch=json.loads((T/'batch.json').read_text());grid=json.loads((T/'grid_batch.json').read_text());report=json.loads((T/'report.json').read_text());plan=report['plan'];ledgerfile=ROOT/'research/automation/registry.jsonl';raw=[json.loads(x)for x in ledgerfile.read_text().splitlines()];records=registry.read_records(ledgerfile)
assert len(batch)==68 and len(grid)==110 and sum(x['is_new']for x in grid)==68
assert report['summary']['new_configs']==68 and len(report['summary']['passed'])+len(report['summary']['rejected'])==68
assert report['summary']['new_component_configs']==36 and report['summary']['new_combination_configs']==32
assert report['summary']['new_cost_scenes']==204 and report['summary']['new_minute_NAV_points']==204*259382
assert report['summary']['allocation_profiles']=={'0.45':[900,1100],'0.5':[1000,1000],'0.55':[1100,900],'0.6':[1200,800],'0.65':[1300,700]}
for b in batch:
 fp=b['fingerprint'];sp=json.loads((ROOT/b['spec']).read_text());assert registry.fingerprint(sp)==fp
 events=[x for x in raw if x['fingerprint']==fp];res=[x for x in events if x['status']=='reserved'];fin=[x for x in events if x.get('report_sha256')]
 assert len(res)==len(fin)==1 and res[0]['recorded_at_utc']<report['evaluation_started_utc']
 c=report['configs'][b['name']];assert c['fingerprint']==fp and c['status']==records[fp]['status'] in ('passed','rejected')
 assert records[fp]['report_sha256']==sha(T/'report.json') and records[fp]['report']==str((T/'report.json').relative_to(ROOT))
 assert sha(ROOT/c['archive'])==c['archive_sha256'] and set(c['scenes'])=={'1','2','3'} and len(c['scenes']['1']['folds'])==6
 assert c['status']=='passed' if all(c['criteria'].values()) else c['status']=='rejected'
 if sp['kind']=='strategy':
  idx=0 if b['asset']=='BTC' else 1;cap=D(str(sp['parameters']['initial_capital_usdt']));budget=D(2000)*D(str(b['raw_weights'][idx]));assert cap==budget==D(b['capital_usdt'])
 else:
  assert sum(D(str(x['weight']))for x in sp['components'])==D(1) and [x['weight']for x in sp['components']]==b['raw_weights']
  assert [records[x['fingerprint']]['spec']['parameters']['initial_capital_usdt']for x in sp['components']]==[int(D(2000)*D(str(w)))for w in b['raw_weights']]
for path,h in report['source_hashes'].items():assert sha(ROOT/path)==h,path
for period in report['data'].values():
 for rec in period.values():assert sha(ROOT/rec['path'])==rec['sha256']
for key,sens in report['sensitivity'].items():
 y,group=key.split('_',1);expected=5 if group=='BTC' else 25;edges=4 if group=='BTC' else 40
 assert sens['cells']==expected and len(sens['adjacent_edges'])==edges
obs='research/paper10/state.json';state=json.loads((ROOT/obs).read_text());assert state['observations']==52 and state['last_observation_id']=='20261012T023803425448Z'
for nm in ('20261012T023522370176Z','20261012T023611651051Z'):
 q=ROOT/'research/paper10/observations'/nm;assert json.loads((q/'report.json').read_text())['mode']=='blocked' and (q/'result.md').is_file()
print(json.dumps({'passed':True,'reserved_and_finished':len(batch),'new_scenes':204,'grid':110,'folds_per_new_scene':6,'paper10_obs':52,'paper10_state_preserved':True,'blocked_windows_preserved':2,'report_sha256':sha(T/'report.json')}))
