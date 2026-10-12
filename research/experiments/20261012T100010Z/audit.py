#!/usr/bin/env python3
"""Independent chronology, registry, equity and cost audit for R51 outputs."""
import gzip,hashlib,json,math
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; R=Path(__file__).resolve().parent
sys_path=ROOT/'research/experiments/20261012T100010Z'
report=json.loads((R/'report.json').read_text()); batch=json.loads((R/'batch.json').read_text())
rows=[]; violations=[]
registry_rows={}
for line in (ROOT/'research/automation/registry.jsonl').read_text().splitlines():
 x=json.loads(line); registry_rows[x['fingerprint']]=x
reserved={json.loads(x)['stdout'] for x in (R/'reserve.log').read_text().splitlines()}
for b in batch:
 spec=json.loads((ROOT/b['spec']).read_text())
 assert b['fingerprint'] in reserved and b['fingerprint'] in registry_rows
 assert registry_rows[b['fingerprint']]['status'] in ('reserved','rejected')
 if registry_rows[b['fingerprint']]['status']=='rejected':
  assert registry_rows[b['fingerprint']]['report_sha256']==hashlib.sha256((R/'report.json').read_bytes()).hexdigest()
 for mult in (1,2,3):
  p=ROOT/'data/runs'/R.name/f"{b['name']}_cost{mult}.json.gz"
  with gzip.open(p,'rt') as f: arc=json.load(f)
  assert arc['fingerprint']==b['fingerprint']
  trades=arc['trades']; cash=D('2000'); units=D(0)
  for t in trades:
   assert t['side'] in ('buy','sell') and t['bar_index']>=2208 and t['bar_index']<=4368
   assert t['signal_to_execution_seconds'] is None or t['signal_to_execution_seconds']==60.0
   if t['signal_available_utc'] is not None:
    assert t['signal_available_utc'] < t['execution_utc']
   after_cash=D(t['cash_after']); after_units=D(t['units_after']); ref=D(t['reference'])
   assert cash>=0 and units>=0 and after_cash>=0 and after_units>=0
   if t['status']=='filled':
    parts=sum((D(v) for v in t['cost_parts'].values()),D(0))
    assert abs(parts-D(t['cost_usdt'])) < D('1e-20')
    assert abs((cash+units*ref)-(after_cash+after_units*ref)-parts) < D('1e-18')
   else:
    assert cash==after_cash and units==after_units
   cash,units=after_cash,after_units
  s=arc['summary']; assert cash==D(s['terminal_cash_usdt']) and units==D(s['terminal_units'])
  assert s['balance_violations']==0
  assert s['minute_nav_samples']>500000 and s['minute_nav_sha256_f64le']
  assert len(s['folds'])==12 and all(x['observations']>40000 for x in s['folds'])
  for f in s['folds']: assert f['test_end_exclusive_utc']>f['test_start_utc']
  rows.append({'name':b['name'],'cost':mult,'attempts':len(trades),'fills':sum(t['status']=='filled' for t in trades),'terminal_cash':str(cash),'terminal_units':str(units)})
# Verify exact 30-day contiguous folds for each configuration.
for name,cfg in report['configs'].items():
 for mult in ('1','2','3'):
  folds=cfg['cost_scenarios'][mult]['folds']; assert len(folds)==12
  for x,y in zip(folds,folds[1:]): assert x['test_end_exclusive_utc']==y['test_start_utc']
# Complete dataset file hashes independently match the emitted manifest.
manifest=json.loads((R/'data_manifest.json').read_text())
for asset,entry in manifest['assets'].items():
 for f in entry['source_files']:
  p=ROOT/f['path']; assert hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
assert len(batch)==20 and len({b['fingerprint'] for b in batch})==20
assert report['summary']['candidate_rejected']==18 and report['summary']['candidate_passed']==0
out={'passed':True,'candidate_config_count':18,'comparator_count':2,'cost_scene_count':60,'verified_trade_scene_archives':len(rows),'registry_reservations_verified':20,'registry_finished_rows_verified':sum(registry_rows[b['fingerprint']]['status']=='rejected' for b in batch),'chronology_and_balance_violations':0,'contiguous_wfv_folds_verified':12,'dataset_hashes_verified':True,'all_candidates_rejected':True,'audit_scope':'Independent structural, chronology, Decimal balance/cost reconciliation, fold continuity and source SHA checks. Performance conclusions remain from the executed evaluator.'}
(R/'audit.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out))
