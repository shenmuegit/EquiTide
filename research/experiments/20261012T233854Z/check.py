#!/usr/bin/env python3
"""Audit candle-turn results, data hashes, and ledger event status."""
import gzip,hashlib,json,math,pathlib,struct,sys
ROOT=pathlib.Path(__file__).resolve().parents[3];R=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
report=json.loads((R/'report.json').read_text());res=json.loads((R/'reserve.json').read_text());records=registry.read_records(ROOT/'research/automation/registry.jsonl');finished='--pre-finish' not in sys.argv
assert len(res)==40 and all(x['exit_code']==0 for x in res)
assert len(report['configs'])==36 and len(report['benchmarks'])==4 and report['summary']['cost_scenes']==120
assert report['summary']['candidate_configs']==12 and report['summary']['placebo_controls']==24
assert report['summary']['oos_days']==360 and report['summary']['folds']==12
assert report['summary']['candidate_passed']+report['summary']['candidate_rejected']==12
for e in res:
 fp=e['output'];assert fp in records
 spec=json.loads((ROOT/e['spec']).read_text());name=spec['name']
 expected='passed' if name.startswith('buy_hold_') else (report['configs'][name]['status'])
 if finished:
  assert records[fp].get('status')==expected and records[fp].get('result_available') is True,(name,records[fp].get('status'),expected)
 else:assert records[fp].get('status')=='reserved'
for asset,files in report['data_manifest']['source_files'].items():
 for item in files:assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256']
scenes=0
for name,cfg in report['configs'].items():
 assert cfg['fingerprint'] in records and len(cfg['scenarios'])==3
 for m in ('1','2','3'):
  p=ROOT/'data/runs'/R.name/f'{name}_cost{m}.json.gz';assert p.exists()
  with gzip.open(p,'rt',encoding='utf-8') as f:x=json.load(f)
  assert x['summary']==cfg['scenarios'][m]
  assert len(x['daily_nav'])==361 and math.isclose(x['daily_nav'][0],cfg['capital'],rel_tol=0,abs_tol=1e-8)
  assert hashlib.sha256(struct.pack('<'+'d'*len(x['daily_nav']),*x['daily_nav'])).hexdigest()==x['summary']['daily_nav_sha256_f64le']
  s=x['summary'];assert s['cost_multiplier']==int(m) and s['terminal_flat']==(float(s['terminal_units'])==0.0)
  assert s['rejected_orders']>=s['capacity_rejections'] and s['capacity_rejections']==0
  if s['rejected_orders']:assert cfg.get('gates',{}).get('no_rejections_or_capacity_violations') is False
  if not s['terminal_flat']:assert cfg.get('gates',{}).get('terminal_flat') is False
  parts=sum((float(v) for v in s['cost_parts_usdt'].values()),0.0)
  assert math.isclose(parts,float(s['cost_usdt']),rel_tol=0,abs_tol=1e-8)
  assert len(s['folds'])==12 and math.isclose(s['net_return_pct'],100*(float(s['terminal_nav_usdt'])/cfg['capital']-1),abs_tol=1e-8)
  scenes+=1
for name,cfg in report['benchmarks'].items():
 assert cfg['fingerprint'] in records
 for m in ('1','2','3'):
  p=ROOT/'data/runs'/R.name/f'{name}_cost{m}.json.gz';assert p.exists()
  with gzip.open(p,'rt',encoding='utf-8') as f:x=json.load(f)
  assert x['summary']==cfg['scenarios'][m] and x['summary']['terminal_flat']
  scenes+=1
assert scenes==120 and report['summary']['candidate_passed']==0
conflict=json.loads((R/'conflicting_reservations.json').read_text());assert len(conflict['attempts'])==20 and all(x['exit_code']==3 for x in conflict['attempts'])
print(json.dumps({'passed':True,'candidate_configs':12,'placebo_controls':24,'benchmarks':4,'cost_scenes_verified':120,'reservations':40,'conflicting_reserved_trials_preserved':20,'finished_check':finished,'input_hashes':'PASS','cost_ledger_summaries':'PASS','folds':12},indent=2))
