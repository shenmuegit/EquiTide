#!/usr/bin/env python3
"""Apply terminal-reference marks and normalize compact reporting after the run."""
import gzip,hashlib,json,math
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent;RUNS=ROOT/'data/runs'/R.name
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dd(x):
 a=np.asarray(x,dtype=np.float64);peak=np.maximum.accumulate(a);d=1-a/peak;j=int(np.argmax(d));return float(100*d[j]),int(np.argmax(a[:j+1])),j
def write_gz(path,obj):
 with path.open('wb') as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as g:g.write(json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
report=json.loads((R/'report.json').read_text())
specs={x['name']:json.loads((ROOT/x['spec']).read_text()) for x in json.loads((R/'batch.json').read_text())}
for name,cfg in report['configs'].items():
 p=specs[name]['parameters'];end_day=int(p.get('oos_end_day_index',728));end_ts=int(datetime(2026,9,14,tzinfo=timezone.utc).timestamp())*1_000_000_000
 for m,s in cfg['scenarios'].items():
  if not isinstance(s,dict) or 'terminal_units' not in s:continue
  navpath=ROOT/s['event_nav_archive']
  with np.load(navpath) as z:nav=z['event_nav'].astype('<f8');times=z['event_time_ns'].astype('<i8')
  # The OOS boundary is exclusive. A residual that cannot be liquidated at the
  # terminal open is marked there; minute-close prices after that instant are excluded.
  keep=times<=end_ts;nav=nav[keep];times=times[keep]
  if abs(float(s['terminal_units']))>1e-14 and (len(times)==0 or int(times[-1])<end_ts or float(nav[-1])!=float(s['terminal_NAV_usdt'])):
   nav=np.append(nav,np.float64(s['terminal_NAV_usdt']));times=np.append(times,np.int64(end_ts))
  np.savez_compressed(navpath,event_nav=nav.astype('<f8'),event_time_ns=times.astype('<i8'))
  draw,peak,trough=dd(nav)
  s['max_drawdown_pct']=draw;s['drawdown_peak_index']=peak;s['drawdown_trough_index']=trough
  s['event_nav_sha256_f64le']=hashlib.sha256(np.asarray(nav,dtype='<f8').tobytes()).hexdigest();s['event_nav_samples']=len(nav);s['event_nav_archive_sha256']=sha(navpath)
  # Large per-day rejection counters remain in the ignored compressed event ledger.
  s.pop('rejected_by_utc_day',None)
  lp=RUNS/f'{name}_x{m}_ledger.json.gz'
  with gzip.open(lp,'rt',encoding='utf-8') as f:ledger=json.load(f)
  ledger['summary']=s;write_gz(lp,ledger)
# Recompute gates and statuses from the final archived scene summaries.
for name,cfg in report['configs'].items():
 role=specs[name]['logic'].get('control_role','buy_hold_comparator')
 if role!='primary_event':cfg['scenarios']['status']='rejected';continue
 sc=cfg['scenarios'];p=specs[name]['parameters'];asset=cfg['asset'];neighbors=[]
 for n,z in report['configs'].items():
  if z['asset']!=asset or specs[n]['logic'].get('control_role','buy_hold_comparator')=='buy_hold_comparator':continue
  q=specs[n]['parameters']
  if abs(int(q['phase_offset_minutes'])-int(p['phase_offset_minutes']))<=1 and abs(int(q['hold_minutes'])-int(p['hold_minutes']))<=1:neighbors.append(n)
 fraction=sum(report['configs'][n]['scenarios']['3']['net_return_pct']>0 for n in neighbors)/len(neighbors)
 one=sc['1'];three=sc['3'];positive=sum(f['net_return_pct']>0 for f in one['folds'])
 gates={'all_costs_positive':all(sc[str(k)]['net_return_pct']>0 for k in (1,2,3)),
  'positive_1x_folds_at_least_8_of_12':positive>=8,'drawdown_3x_at_most_25pct':three['max_drawdown_pct']<=25,
  'adjacent_3x_positive_fraction_at_least_0_60':fraction>=.6,'round_trips_1x_at_least_100':one['round_trips']>=100,
  'gross_to_cost_1x_at_least_2_5':one['gross_reference_pnl_to_cost'] is not None and one['gross_reference_pnl_to_cost']>=2.5,
  'no_order_rejections_or_capacity_violations':all(sc[str(k)]['rejected_orders']==0 and sc[str(k)]['capacity_rejections']==0 for k in (1,2,3)),
  'terminal_flat_all_costs':all(sc[str(k)]['terminal_flat'] for k in (1,2,3))}
 phase=report['phase_means_1x_by_asset'][asset];gates['phase0_beats_both_placebos_for_asset']=phase['0']>phase['1'] and phase['0']>phase['2']
 sc['gates']=gates;sc['neighbor_3x_positive_fraction']=fraction;sc['neighbor_count']=len(neighbors);sc['positive_1x_fold_count']=positive;sc['status']='passed' if all(gates.values()) else 'rejected'
report['summary']['primary_passed']=sum(c['scenarios'].get('status')=='passed' for c in report['configs'].values() if specs[c['name']]['logic'].get('control_role')=='primary_event')
report['summary']['primary_rejected']=sum(c['scenarios'].get('status')=='rejected' for c in report['configs'].values() if specs[c['name']]['logic'].get('control_role')=='primary_event')
report.pop('all_cost_scenes',None)
report['summary']['scene_rows_external']=['cost_scenarios.csv','fold_results.csv']
report['finalization']={'terminal_reference_mark_added_for_residual_inventory':True,'large_rejection_by_day_detail':'Preserved in ignored data/runs scene ledgers; report retains exact overall reason totals.','reused_history_not_untouched_holdout':True,'execution_code_sha256':sha(R/'evaluate.py')}
(R/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps({'primary_passed':report['summary']['primary_passed'],'primary_rejected':report['summary']['primary_rejected'],'terminal_nonflat_scenes':sum(not s.get('terminal_flat',True) for c in report['configs'].values() for s in c['scenarios'].values() if isinstance(s,dict)),'report_bytes':(R/'report.json').stat().st_size}))
