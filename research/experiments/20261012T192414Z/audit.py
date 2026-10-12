#!/usr/bin/env python3
"""Independent chronology, accounting, cost, WFV and input SHA audit."""
import gzip,hashlib,json,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());reg={}
hash_reconciliation=json.loads((R/'report_hash_reconciliation.json').read_text())
current_report_sha=hashlib.sha256((R/'report.json').read_bytes()).hexdigest()
for line in (ROOT/'research/automation/registry.jsonl').read_text().splitlines():
 x=json.loads(line);reg.setdefault(x.get('fingerprint'),[]).append(x)
reserved={json.loads(x)['stdout'] for x in (R/'reserve.log').read_text().splitlines()};assert len(reserved)==20 and len(batch)==20
verified=0
for b in batch:
 fp=b['fingerprint'];assert fp in reserved and fp in reg and reg[fp][-1]['status'] in ('reserved','rejected')
 if reg[fp][-1]['status']=='rejected':assert reg[fp][-1]['report_sha256']==hash_reconciliation['registry_finish_report_sha256']
 for m in (1,2,3):
  with gzip.open(ROOT/'data/runs'/R.name/f"{b['name']}_cost{m}.json.gz",'rt',encoding='utf-8') as f:arc=json.load(f)
  assert arc['fingerprint']==fp;cash=D(2000);units=D(0);held=False;last=None
  for t in arc['trades']:
   assert 35328<=t['bar_index']<=69888
   if last is not None:assert t['execution_utc']>=last
   last=t['execution_utc'];assert t['signal_to_execution_seconds'] is None or t['signal_to_execution_seconds']==60.0
   if t['signal_available_utc'] is not None:assert t['signal_available_utc']<t['execution_utc']
   assert D(t['cash_before'])==cash and D(t['units_before'])==units
   ca,ua,ref=D(t['cash_after']),D(t['units_after']),D(t['reference'])
   if t['status']=='filled':
    parts=sum((D(x) for x in t['cost_parts'].values()),D(0));assert abs(parts-D(t['cost_usdt']))<D('1e-18') and abs((cash+units*ref)-(ca+ua*ref)-parts)<D('1e-16')
    if t['side']=='buy':assert not held;held=True
    else:assert t['side']=='sell' and held;held=False
   else:assert ca==cash and ua==units
   assert ca>=0 and ua>=0;cash,units=ca,ua
  s=arc['summary'];assert cash==D(s['terminal_cash_usdt']) and units==D(s['terminal_units']) and held==s['terminal_held'] and s['balance_violations']==0
  assert len(s['folds'])==12 and all(x['observations']==30 for x in s['folds']) and s['minute_nav_samples']>500000
  verified+=1
for cfg in report['configs'].values():
 for m in ('1','2','3'):
  fs=cfg['scenarios'][m]['folds'];assert len(fs)==12
  for a,b in zip(fs,fs[1:]):assert a['end_exclusive_utc']==b['start_utc']
manifest=json.loads((R/'data_manifest.json').read_text())
for asset in manifest['assets'].values():
 for x in asset['source_files']:assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256']
assert report['summary']['candidate_configs']==18 and report['summary']['comparators']==2 and report['summary']['cost_scenes']==60 and report['summary']['candidate_passed']==0 and report['summary']['candidate_rejected']==18
hash_match=hash_reconciliation['hash_match'] and current_report_sha==hash_reconciliation['current_report_json_sha256']
out={'accounting_and_causality_passed':True,'report_hash_match':hash_match,'report_hash_reconciliation':'report_hash_reconciliation.json','candidate_configs':18,'benchmarks':2,'scenes':60,'reservations_verified':20,'finished_rejections_verified':sum(reg[b['fingerprint']][-1]['status']=='rejected' for b in batch),'trade_archives_verified':verified,'chronology_cash_units_cost_identity_violations':0,'contiguous_12fold_wfv_verified':True,'data_hashes_verified':True,'all_candidates_rejected':True,'overall_passed':hash_match}
(R/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
