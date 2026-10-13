#!/usr/bin/env python3
"""Audit persisted event/NAV evidence, flatten fold sensitivity and write final report."""
import csv,gzip,hashlib,json,math,subprocess,sys
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;RUNS=ROOT/'data/runs'/R.name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dumpj(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
report=json.loads((R/'report.json').read_text());batch=json.loads((R/'batch.json').read_text());fails=[];flat=[];foldrows=[];gridrows=[]
for row in batch:
 name=row['name'];cfg=report['configs'][name];scene=cfg['scenarios']
 for mult in (1,2,3):
  s=scene[str(mult)];navpath=ROOT/s['minute_nav_archive']
  assert sha(navpath)==s['minute_nav_archive_sha256'],(name,mult,'nav sha')
  with np.load(navpath) as x:
   nav=x['nav_usdt'];times=x['timestamp_utc_ns']
  if len(nav)!=s['minute_nav_samples'] or len(nav)!=len(times):fails.append(f'{name} x{mult}: NAV length mismatch')
  if not np.isfinite(nav).all() or (nav<=0).any():fails.append(f'{name} x{mult}: invalid NAV values')
  # Trade ledger time, balance, position and causal timing checks.
  with gzip.open(RUNS/f'{name}_cost{mult}.json.gz','rt') as f:archive=json.load(f)
  trades=archive['trades'];last_by_side={}
  for t in trades:
   if t['status']=='filled':
    cash=float(t['cash_after']);units=float(t['units_after'])
    if cash < -1e-10 or units < -1e-10:fails.append(f'{name} x{mult}: negative balance')
    if t['side']=='buy' and t.get('signal_available_utc') and t['execution_utc']<=t['signal_available_utc']:fails.append(f'{name} x{mult}: noncausal buy')
    if t['side']=='sell' and t.get('scheduled_exit_minute') is not None and t['execution_minute']<t['scheduled_exit_minute']:fails.append(f'{name} x{mult}: early exit')
  if abs(float(s['terminal_units']))>1e-12 and s['terminal_flat']:fails.append(f'{name} x{mult}: inconsistent terminal flat')
  if s['balance_violations']!=0:fails.append(f'{name} x{mult}: reported balance violation')
  reason_counts=Counter(t.get('reason','') for t in trades if t['status']=='rejected')
  if sum(reason_counts.values())!=s['rejected_orders']:fails.append(f'{name} x{mult}: rejection count mismatch')
  if abs(float(s['net_PnL_usdt'])+float(s['cost_usdt'])-float(s['gross_reference_pnl_usdt']))>1e-6:fails.append(f'{name} x{mult}: gross/cost identity')
  gate=scene.get('gates',{}) if not row['is_comparator'] else {}
  flat.append({'name':name,'asset':row['asset'],'comparator':row['is_comparator'],'cost_multiplier':mult,'net_return_pct':s['net_return_pct'],'max_drawdown_pct':s['max_drawdown_pct'],'daily_drawdown_pct':s['daily_mark_drawdown_pct'],'round_trips':s['round_trips'],'signals':s['signals'],'filled_executions':s['executions'],'rejected_orders':s['rejected_orders'],'rejection_reasons':';'.join(f'{k}:{v}' for k,v in reason_counts.items()),'terminal_flat':s['terminal_flat'],'cost_usdt':s['cost_usdt'],'fee_usdt':s['cost_parts_usdt']['fee'],'half_spread_usdt':s['cost_parts_usdt']['half_spread'],'slippage_usdt':s['cost_parts_usdt']['slippage'],'impact_usdt':s['cost_parts_usdt']['impact'],'tick_rounding_usdt':s['cost_parts_usdt']['tick_rounding'],'gross_reference_pnl_to_cost':s['gross_reference_pnl_to_cost'],'adjacent_3x_positive_fraction':scene.get('adjacent_3x_positive_fraction'),'status':scene.get('status'),'nav_samples':s['minute_nav_samples'],'nav_sha256':s['minute_nav_sha256_f64le']})
  for frow in s['folds']:
   foldrows.append({'name':name,'asset':row['asset'],'cost_multiplier':mult,**frow})
  if not row['is_comparator']:
   p=json.loads((ROOT/row['spec']).read_text())['parameters'];gridrows.append({'asset':row['asset'],'return_threshold':p['first_half_return_threshold'],'same_slot_volume_ratio_min':p['same_slot_quote_volume_ratio_min'],'cost_multiplier':mult,'net_return_pct':s['net_return_pct'],'max_drawdown_pct':s['max_drawdown_pct'],'sharpe_daily':s['sharpe_annualized_daily'],'calmar_daily':s['calmar_daily'],'round_trips':s['round_trips'],'positive_folds':sum(f['net_return_pct']>0 for f in s['folds']),'status':scene.get('status'),'adjacent_3x_positive_fraction':scene.get('adjacent_3x_positive_fraction')})
if fails:raise SystemExit('\n'.join(fails))
for filename,rows in [('sensitivity.csv',gridrows),('fold_results.csv',foldrows),('cost_scenarios.csv',flat)]:
 with (R/filename).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
# Standalone SVG heatmaps: rows are return thresholds, columns are volume gates.
colors=lambda v:'#9b2335' if v<=-75 else ('#d95053' if v<=-25 else ('#f4a261' if v<0 else '#2a9d8f'))
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="510" viewBox="0 0 1060 510">','<rect width="100%" height="100%" fill="#101822"/>','<style>text{font-family:Arial,sans-serif;fill:#e7edf3}.small{font-size:13px}.title{font-size:19px;font-weight:bold}</style>']
for ai,asset in enumerate(('BTC','ETH')):
 for mi,mult in enumerate((1,2,3)):
  x0=45+mi*340;y0=70+ai*215
  svg.append(f'<text class="title" x="{x0}" y="{y0}">{asset} — {mult}× 成本，净收益</text>')
  for ri,ret in enumerate((0,.0005,.001)):
   for ci,vol in enumerate((.75,1.,1.25)):
    row=next(x for x in gridrows if x['asset']==asset and float(x['return_threshold'])==ret and float(x['same_slot_volume_ratio_min'])==vol and x['cost_multiplier']==mult)
    x=x0+ri*90;y=y0+25+ci*48;v=row['net_return_pct']
    svg.append(f'<rect x="{x}" y="{y}" width="82" height="42" rx="4" fill="{colors(v)}"/>')
    svg.append(f'<text class="small" x="{x+41}" y="{y+17}" text-anchor="middle">r&gt;{ret*100:.2f}%</text>')
    svg.append(f'<text class="small" x="{x+41}" y="{y+34}" text-anchor="middle">vol≥{vol:.2f}: {v:.1f}%</text>')
svg.extend(['<text class="small" x="45" y="490">同一 UTC 小时首半小时收益阈值 × 同槽历史成交额比率；所有网格点固定预登记，红色为更深的亏损。</text>','</svg>'])
(R/'sensitivity.svg').write_text('\n'.join(svg)+'\n')
# Persist audit/reproduction metadata and observed conclusion.
report['audit']={'passed':True,'checks':['all 60 scene NAV archive SHA-256 and sample lengths','finite positive NAV samples','nonnegative cash/units and balance accounting','causal signal availability before buys','scheduled sell not before holding period','rejected-order totals reconciled against event ledgers','gross reference PnL equals net PnL plus modeled cost'],'reproduction_commands':['python3 research/experiments/20261013T052946Z/prepare.py','python3 research/experiments/20261013T052946Z/evaluate.py','python3 research/experiments/20261013T052946Z/audit.py','python3 research/experiments/20261013T052946Z/finish.py'],'output_files':['report.json','result.md','sensitivity.csv','fold_results.csv','cost_scenarios.csv','sensitivity.svg','data_manifest.json','stdout.txt'],'historical_holdout_warning':'The repeatedly used 2024-09-16 to 2026-09-16 repository development/validation sample is not an untouched holdout.'}
dumpj(R/'report.json',report)
print(json.dumps({'audited_scenes':len(flat),'fold_rows':len(foldrows),'sensitivity_rows':len(gridrows),'files':['sensitivity.csv','fold_results.csv','cost_scenarios.csv','sensitivity.svg']},ensure_ascii=False))
