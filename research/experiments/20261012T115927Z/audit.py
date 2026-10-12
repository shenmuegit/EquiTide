#!/usr/bin/env python3
"""Independent ledger/time/cost/fold/hash audit for R52."""
import gzip,hashlib,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text())
regrows={}
for line in (ROOT/'research/automation/registry.jsonl').read_text().splitlines():
 x=json.loads(line);regrows.setdefault(x.get('fingerprint'),[]).append(x)
reserved={json.loads(x)['stdout'] for x in (R/'reserve.log').read_text().splitlines()}
assert len(batch)==11 and len(reserved)==11 and len(set(x['fingerprint'] for x in batch))==11
verified=0
for b in batch:
 fp=b['fingerprint'];assert fp in reserved and fp in regrows
 last=regrows[fp][-1];assert last.get('status') in ('reserved','rejected')
 if last.get('status')=='rejected':assert last['report_sha256']==hashlib.sha256((R/'report.json').read_bytes()).hexdigest()
 for mult in (1,2,3):
  path=ROOT/'data/runs'/R.name/f"{b['name']}_cost{mult}.json.gz"
  with gzip.open(path,'rt',encoding='utf-8') as f:arc=json.load(f)
  assert arc['fingerprint']==fp
  cash=D(2000);units=D(0);held=None;last_time=None
  for t in arc['trades']:
   assert 368<=t['bar_index']<=728
   if last_time is not None:assert t['execution_utc']>=last_time
   last_time=t['execution_utc']
   assert t['signal_to_execution_seconds'] is None or t['signal_to_execution_seconds']==60.0
   if t['signal_available_utc']:assert t['signal_available_utc']<t['execution_utc']
   assert D(t['cash_before'])==cash and D(t['units_before'])==units
   ca,ua=D(t['cash_after']),D(t['units_after']);ref=D(t['reference'])
   if t['status']=='filled':
    parts=sum((D(x) for x in t['cost_parts'].values()),D(0));assert abs(parts-D(t['cost_usdt']))<D('1e-18')
    assert abs((cash+units*ref)-(ca+ua*ref)-parts)<D('1e-16')
    if t['side']=='buy':assert held is None;held=t['asset']
    else:assert t['side']=='sell' and held==t['asset'];held=None
   else:assert ca==cash and ua==units
   assert ca>=0 and ua>=0;cash,units=ca,ua
  s=arc['summary'];assert cash==D(s['terminal_cash_usdt']) and units==D(s['terminal_units']) and held==s['terminal_asset']
  assert s['balance_violations']==0 and len(s['folds'])==12 and all(x['observations']==30 for x in s['folds'])
  assert s['minute_nav_samples']>500000 and s['minute_nav_sha256_f64le']
  verified+=1
for cfg in report['configs'].values():
 for mult in ('1','2','3'):
  folds=cfg['scenarios'][mult]['folds'];assert len(folds)==12
  for x,y in zip(folds,folds[1:]):assert x['end_exclusive_utc']==y['start_utc']
manifest=json.loads((R/'data_manifest.json').read_text())
for asset in manifest['assets'].values():
 for f in asset['source_files']:assert hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest()==f['sha256']
assert report['summary']['candidate_configs']==9 and report['summary']['comparators']==2 and report['summary']['cost_scenes']==33
assert report['summary']['candidate_passed']==0 and report['summary']['candidate_rejected']==9
out={'passed':True,'candidate_configs':9,'comparators':2,'cost_scenes':33,'registry_reservations_verified':11,'registry_finished_rows_verified':sum(regrows[b['fingerprint']][-1]['status']=='rejected' for b in batch),'scene_archives_verified':verified,'chronology_accounting_cost_identity_violations':0,'contiguous_wfv_folds_verified':12,'source_hashes_verified':True,'all_candidates_rejected':True,'scope':'Independent audit of completed ledgers and report; minute-drawdown hashes are checked structurally and can be reproduced by the evaluator.'}
(R/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
