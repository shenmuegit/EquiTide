"""Final ledger/spec/report/state linkage checks for this pre-reserved grid."""
import hashlib,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];T=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
batch=json.loads((T/'batch.json').read_text());grid=json.loads((T/'grid_batch.json').read_text());report=json.loads((T/'report.json').read_text());ledgerfile=ROOT/'research/automation/registry.jsonl';raw=[json.loads(x) for x in ledgerfile.read_text().splitlines()];records=registry.read_records(ledgerfile)
assert len(batch)==28 and len(grid)==42 and sum(x['is_new'] for x in grid)==28
assert report['summary']['new_configs']==28 and len(report['summary']['passed'])+len(report['summary']['rejected'])==28
assert report['summary']['new_cost_scenes']==84 and report['summary']['new_minute_NAV_points']==84*259382
assert report['summary']['allocation_profiles']=={'0.5':[1000,1000],'0.55':[1100,900],'0.6':[1200,800]}
for b in batch:
 fp=b['fingerprint'];sp=json.loads((ROOT/b['spec']).read_text());assert registry.fingerprint(sp)==fp
 events=[x for x in raw if x['fingerprint']==fp];res=[x for x in events if x['status']=='reserved'];fin=[x for x in events if x.get('report_sha256')]
 assert len(res)==len(fin)==1 and res[0]['recorded_at_utc']<report['evaluation_started_utc']
 c=report['configs'][b['name']];assert c['fingerprint']==fp and c['status']==records[fp]['status'] in ('passed','rejected')
 assert records[fp]['report_sha256']==sha(T/'report.json') and records[fp]['report']==str((T/'report.json').relative_to(ROOT))
 assert sha(ROOT/c['archive'])==c['archive_sha256']
 assert set(c['scenes'])=={'1','2','3'} and len(c['scenes']['1']['folds'])==6
 assert all(c['scenes'][k]['net_return_pct']>0 for k in ('1','2','3'))
 assert (c['status']=='passed')==all(c['criteria'].values())
 if sp['kind']=='strategy':
  cap=D(str(sp['parameters']['initial_capital_usdt']));budget=D(2000)*D(str(b['raw_weights'][0 if b['asset']=='BTC' else 1]));assert cap==budget==D(b['capital_usdt'])
 else:
  assert sum(D(str(x['weight'])) for x in sp['components'])==D(1)
  assert [x['weight'] for x in sp['components']]==b['raw_weights']
  assert [records[x['fingerprint']]['spec']['parameters']['initial_capital_usdt'] for x in sp['components']]==[int(D(2000)*D(str(w))) for w in b['raw_weights']]
for path,h in report['source_hashes'].items():assert sha(ROOT/path)==h,path
for path,h in report['data'][ '2025'].items() if False else []:pass
for period in report['data'].values():
 for rec in period.values():assert sha(ROOT/rec['path'])==rec['sha256']
assert sha(T/'legacy_shadow_gap.json') and json.loads((T/'legacy_shadow_gap.json').read_text())['missed_daily_orders_backfilled']==0
assert sha(ROOT/'research/experiments/20261011T235327Z/forward_state.json')==report['plan']['legacy_shadow_gap']['source_state_sha256']
paper=json.loads((ROOT/'research/paper10/state.json').read_text());assert paper['observations']==51 and paper['last_observation_id']=='20261012T002852636046Z'
print(json.dumps({'passed':True,'new_configs':28,'finished_events':28,'new_cost_scenes':84,'folds_per_scene':6,'folder_sha256_bound':sha(T/'report.json'),'paper10_observations_preserved':51,'blocked_shadow_no_backfill_preserved':True}))
