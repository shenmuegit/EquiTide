#!/usr/bin/env python3
"""Independent audit of reserved ratio-rotation run chronology and accounting."""
import gzip,hashlib,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text())
records={}
for line in (ROOT/'research/automation/registry.jsonl').read_text().splitlines():
 x=json.loads(line);records.setdefault(x.get('fingerprint'),[]).append(x)
reserved={json.loads(x)['stdout'] for x in (R/'reserve.log').read_text().splitlines()};assert len(batch)==11 and len(reserved)==11
verified=0
for b in batch:
 fp=b['fingerprint'];assert fp in reserved and fp in records;last=records[fp][-1];assert last['status'] in ('reserved','rejected')
 if last['status']=='rejected':assert last['report_sha256']==hashlib.sha256((R/'report.json').read_bytes()).hexdigest()
 for mult in (1,2,3):
  with gzip.open(ROOT/'data/runs'/R.name/f"{b['name']}_cost{mult}.json.gz",'rt',encoding='utf-8') as f:arc=json.load(f)
  assert arc['fingerprint']==fp;cash=D(2000);units=D(0);held=None;last_time=None
  for t in arc['trades']:
   assert 368<=t['bar_index']<=728 and (last_time is None or t['execution_utc']>=last_time);last_time=t['execution_utc']
   assert t['signal_to_execution_seconds'] is None or t['signal_to_execution_seconds']==60.0
   if t['signal_available_utc'] is not None:assert t['signal_available_utc']<t['execution_utc']
   assert D(t['cash_before'])==cash and D(t['units_before'])==units
   ca,ua,ref=D(t['cash_after']),D(t['units_after']),D(t['reference'])
   if t['status']=='filled':
    parts=sum((D(v) for v in t['cost_parts'].values()),D(0));assert abs(parts-D(t['cost_usdt']))<D('1e-18') and abs((cash+units*ref)-(ca+ua*ref)-parts)<D('1e-16')
    if t['side']=='buy':assert held is None;held=t['asset']
    else:assert t['side']=='sell' and held==t['asset'];held=None
   else:assert ca==cash and ua==units
   assert ca>=0 and ua>=0;cash,units=ca,ua
  s=arc['summary'];assert cash==D(s['terminal_cash_usdt']) and units==D(s['terminal_units']) and held==s['terminal_asset'] and s['balance_violations']==0
  assert len(s['folds'])==12 and all(f['observations']==30 for f in s['folds']) and s['minute_nav_samples']>500000
  verified+=1
for cfg in report['configs'].values():
 for m in ('1','2','3'):
  fs=cfg['scenarios'][m]['folds'];assert len(fs)==12
  for a,b in zip(fs,fs[1:]):assert a['end_exclusive_utc']==b['start_utc']
manifest=json.loads((R/'data_manifest.json').read_text())
for data in manifest['assets'].values():
 for file in data['source_files']:assert hashlib.sha256((ROOT/file['path']).read_bytes()).hexdigest()==file['sha256']
assert report['summary']['candidate_configs']==9 and report['summary']['comparators']==2 and report['summary']['cost_scenes']==33
assert report['summary']['candidate_passed']==0 and report['summary']['candidate_rejected']==9
out={'passed':True,'candidate_configs':9,'benchmarks':2,'cost_scenes':33,'registry_reservations_verified':11,'registry_rejections_verified':sum(records[b['fingerprint']][-1]['status']=='rejected' for b in batch),'scene_ledgers_verified':verified,'causality_balance_cost_identity_violations':0,'continuous_12fold_wfv_verified':True,'source_data_hashes_verified':True,'all_candidates_rejected':True}
(R/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
