#!/usr/bin/env python3
"""Hash, timing, accounting and deterministic replay audit for this grid."""
import csv,gzip,hashlib,json,math,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROUND));import evaluate

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def readgz(p):
 with gzip.open(p,'rt') as f:return json.load(f)
def writecsv(path,rows):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def same_core(a,b):return all(a[k]==b[k] for k in b)
plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());report=json.loads((ROUND/'report.json').read_text())
assert len(batch)==18 and len({x['fingerprint'] for x in batch})==18 and report['summary']['cost_scenes']==54
assert report['summary']['candidate_configs']==18 and report['summary']['directions']==2
filters=json.loads((ROUND/'exchange_filters.json').read_text());assert filters['snapshot']['raw_sha256']==plan['costs']['exchange_filters_source']['raw_sha256']
assert sha(ROOT/filters['snapshot']['path'])==filters['snapshot']['archive_sha256']
records=registry.read_records(ROOT/'research/automation/registry.jsonl');events=registry.read_events(ROOT/'research/automation/registry.jsonl');reserved={x['fingerprint'] for x in events if x.get('status')=='reserved'}
for asset,rows in report['data_manifest']['assets'].items():
 for r in rows['source_files']:
  p=ROOT/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
markets={a:evaluate.load_asset(a) for a in ('BTC','ETH')};manifest=report['data_manifest'];assert {a:[f['sha256'] for f in markets[a]['files']] for a in markets}=={a:[f['sha256'] for f in manifest['assets'][a]['source_files']] for a in markets}
folds=[];scenes=[];sensitivity=[];n_replays=0;run_dir=ROOT/'data/runs'/ROUND.name
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);assert fp==row['fingerprint'] and fp in reserved
 cfg=report['configs'][row['name']];assert cfg['fingerprint']==fp and cfg['spec']==row['spec']
 reserve_event=next(x for x in reversed(events) if x['fingerprint']==fp and x['status']=='reserved');finish_times=[]
 assert reserve_event['recorded_at_utc']<report['evaluation_started_utc']
 for mult in (1,2,3):
  arc=readgz(run_dir/f"{row['name']}_cost{mult}.json.gz");actual=arc['summary'];s=cfg['scenarios'][str(mult)]
  assert arc['fingerprint']==fp and arc['name']==row['name'] and all(s[k]==actual[k] for k in actual)
  nav=arc['daily_nav_usdt'];assert len(nav)==361 and all(math.isfinite(x) and x>0 for x in nav) and abs(nav[-1]-float(actual['terminal_nav_usdt']))<1e-8
  assert len(actual['folds'])==12 and all(f['observations']==30 for f in actual['folds'])
  assert actual['cost_multiplier']==mult
  # Every accepted fill respects the exact Decimal cash/units and execution cost identity.
  position=D(0);cash=D('2000');last_time=None
  for t in arc['trades']:
   if last_time is not None:assert t['execution_utc']>=last_time
   last_time=t['execution_utc'];cb,ub,ca,ua,ref=(D(t[k]) for k in ('cash_before','units_before','cash_after','units_after','reference'))
   if t['status']!='filled':assert cb==ca and ub==ua;continue
   q,px=(D(t[k]) for k in ('quantity','execution'));cost=D(t['cost_usdt']);parts=sum((D(v) for v in t['cost_parts'].values()),D(0));assert abs(parts-cost)<D('1e-18')
   assert abs((cb+ub*ref)-(ca+ua*ref)-cost)<D('1e-10') and ca>=0 and ua>=0
   fs=filters['symbols'][t['asset']];fx={x['filterType']:x for x in fs};assert q%D(fx['LOT_SIZE']['stepSize'])==0 and px%D(fx['PRICE_FILTER']['tickSize'])==0
   assert D(t['participation'])<=D(plan['costs']['maximum_participation'])
   assert abs((evaluate.datetime.fromisoformat(t['execution_utc'].replace('Z','+00:00'))-evaluate.datetime.fromisoformat(t['signal_available_utc'].replace('Z','+00:00'))).total_seconds()-60)<1e-6
   assert t['signal_to_execution_seconds']==60
   if t['side']=='buy':assert ub==0 and ua==q
   else:assert ub==q and ua==0
  # Deterministic re-execution on source bars must reproduce every fill and fold summary.
  rerun=evaluate.run(spec,markets,{a+'USDT':{x['filterType']:x for x in fs} for a,fs in filters['symbols'].items()},mult)
  assert rerun['trades']==arc['trades'] and rerun['daily_nav_usdt']==nav and rerun['summary']['minute_nav_sha256_f64le']==actual['minute_nav_sha256_f64le'];n_replays+=1
  scenes.append({'name':row['name'],'role':'candidate','direction':row['leader']+'>'+row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'cost_multiplier':mult,'net_return_pct':actual['net_return_pct'],'net_pnl_usdt':actual['net_pnl_usdt'],'cost_usdt':actual['cost_usdt'],'cost_parts_usdt':json.dumps(actual['cost_parts_usdt'],sort_keys=True),'max_drawdown_pct':actual['max_drawdown_pct'],'daily_mark_drawdown_pct':actual['daily_mark_drawdown_pct'],'round_trips':actual['round_trips'],'positive_1x_folds':actual['positive_1x_folds'],'rejected_orders':actual['rejected_orders'],'capacity_rejections':actual['capacity_rejections'],'terminal_flat':actual['terminal_flat']})
  for fold in actual['folds']:folds.append({'name':row['name'],'direction':row['leader']+'>'+row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'cost_multiplier':mult,**fold})
for row in batch:
 c=report['configs'][row['name']]['scenarios'];lookvals=plan['parameter_grid']['leader_lookback_minutes'];holdvals=plan['parameter_grid']['fixed_hold_minutes'];li=lookvals.index(row['lookback_minutes']);hi=holdvals.index(row['hold_minutes']);neighbors=[]
 for q in batch:
  if q['leader']==row['leader'] and abs(lookvals.index(q['lookback_minutes'])-li)<=1 and abs(holdvals.index(q['hold_minutes'])-hi)<=1:neighbors.append(q['name'])
 frac=sum(report['configs'][n]['scenarios']['3']['net_return_pct']>0 for n in neighbors)/len(neighbors)
 sensitivity.append({'name':row['name'],'direction':row['leader']+'>'+row['follower'],'lookback_minutes':row['lookback_minutes'],'hold_minutes':row['hold_minutes'],'neighbor_configs':';'.join(neighbors),'neighbor_count':len(neighbors),'neighbor_3x_positive_fraction':frac,'1x_net_return_pct':c['1']['net_return_pct'],'2x_net_return_pct':c['2']['net_return_pct'],'3x_net_return_pct':c['3']['net_return_pct'],'1x_sharpe':c['1']['sharpe_annualized_daily'],'1x_calmar':c['1']['calmar'],'3x_sample_drawdown_pct':c['3']['max_drawdown_pct']})
writecsv(ROUND/'fold_results.csv',folds);writecsv(ROUND/'cost_scenarios.csv',scenes);writecsv(ROUND/'sensitivity.csv',sensitivity)
curves=[]
for row in batch:
 for mult in (1,2,3):
  arc=readgz(run_dir/f"{row['name']}_cost{mult}.json.gz")
  for i,v in enumerate(arc['daily_nav_usdt']):curves.append({'name':row['name'],'direction':row['leader']+'>'+row['follower'],'cost_multiplier':mult,'day_index':i,'date':plan['time_boundaries']['start_utc'][:10] if i==0 else (plan['time_boundaries']['end_exclusive_utc'][:10] if i==360 else markets[row['leader']]['daily'][368+i]['date']),'nav_usdt':v})
writecsv(ROUND/'equity_curves_daily.csv',curves)
# Dependency-free 2-direction sensitivity heatmap of 1x net returns.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="360" viewBox="0 0 960 360"><rect width="100%" height="100%" fill="white"/><text x="20" y="28" font-family="sans-serif" font-size="18" font-weight="bold">1× 成本：回看分钟 × 固定持有分钟</text>']
for panel,leader in enumerate(('BTC','ETH')):
 base_x=80+panel*450;svg.append(f'<text x="{base_x+190}" y="55" text-anchor="middle" font-family="sans-serif" font-size="15">{leader} 领先方向</text>')
 for j,h in enumerate((60,240,720)):svg.append(f'<text x="{base_x+120+j*110}" y="78" text-anchor="middle" font-family="sans-serif" font-size="12">持有 {h}m</text>')
 for i,L in enumerate((15,60,240)):
  y=90+i*78;svg.append(f'<text x="{base_x+85}" y="{y+38}" text-anchor="end" font-family="sans-serif" font-size="12">回看 {L}m</text>')
  for j,H in enumerate((60,240,720)):
   v=next(x['1x_net_return_pct'] for x in sensitivity if x['direction'].startswith(leader+'>') and x['lookback_minutes']==L and x['hold_minutes']==H);x=base_x+100+j*110;color='#b42318' if v<0 else '#16803c';svg.extend([f'<rect x="{x}" y="{y}" width="106" height="74" rx="4" fill="{color}"/>',f'<text x="{x+53}" y="{y+42}" text-anchor="middle" font-family="sans-serif" fill="white">{v:.2f}%</text>'])
svg.append('</svg>');(ROUND/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')
report['integrity_audit']={'status':'passed','unique_reserved_fingerprints':18,'scenarios_audited':54,'exact_deterministic_replays':n_replays,'input_hashes_verified':True,'exchange_filter_snapshot_verified':True,'walk_forward_folds':12,'daily_curve_samples_per_scenario':361,'fill_cash_units_cost_lot_tick_and_delay_checks':'passed','historical_OOS_backtest_not_live':'confirmed'}
report['reproduction']={'evaluate':'.venv/bin/python research/experiments/20261013T164415Z/evaluate.py','audit':'.venv/bin/python research/experiments/20261013T164415Z/audit.py','reserve':'18 configurations reserved separately before first return calculation.'}
report['artifacts']={'fold_results':'research/experiments/20261013T164415Z/fold_results.csv','cost_scenarios':'research/experiments/20261013T164415Z/cost_scenarios.csv','equity_curves_daily':'research/experiments/20261013T164415Z/equity_curves_daily.csv','sensitivity':'research/experiments/20261013T164415Z/sensitivity.csv','sensitivity_surface':'research/experiments/20261013T164415Z/sensitivity_surface.svg'}
report['code_hashes']={'prepare.py':sha(ROUND/'prepare.py'),'evaluate.py':sha(ROUND/'evaluate.py'),'audit.py':sha(ROUND/'audit.py')}
(ROUND/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps({'audit':'passed','scenario_rows':len(scenes),'fold_rows':len(folds),'curve_rows':len(curves),'replays':n_replays,'report_sha256':sha(ROUND/'report.json')}))
