#!/usr/bin/env python3
import csv,gzip,hashlib,json,math,sys
from decimal import Decimal as D
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]; ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation')); import registry

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 with gzip.open(p,'rt') as f:return json.load(f)
def writecsv(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());report=json.loads((ROUND/'report.json').read_text())
assert plan['grid']['rotation_configs']==9 and plan['grid']['comparators']==3 and plan['grid']['total_registry_definitions']==12
assert len(batch)==12 and len({r['fingerprint'] for r in batch})==12
assert report['summary']['candidate_configs']==9 and report['summary']['comparators']==3 and report['summary']['cost_scenes']==36
reserved=set(registry.read_records(ROOT/'research/automation/registry.jsonl'))
fdata=json.loads((ROUND/'exchange_filters.json').read_text());fs={a+'USDT':{x['filterType']:x for x in rows} for a,rows in fdata['symbols'].items()}
assert fdata['snapshot']['raw_sha256']==plan['costs']['filters_source']['raw_sha256'] and sha(ROOT/fdata['snapshot']['path'])==fdata['snapshot']['archive_sha256']
for ent in report['data_manifest']['assets'].values():
 for f in ent['source_files']:
  p=ROOT/f['path'];assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
folds=[];scenes=[];sens=[];data=ROOT/'data/runs'/ROUND.name
for row in batch:
 spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);assert fp==row['fingerprint'] and fp in reserved
 cfg=report['configs'][row['name']];assert cfg['fingerprint']==fp and cfg['role']==row['role']
 for mult in (1,2,3):
  arc=load(data/f"{row['name']}_cost{mult}.json.gz");s=arc['summary'];assert all(s[k]==cfg['scenarios'][str(mult)][k] for k in s) and arc['fingerprint']==fp
  nav=arc['daily_nav_usdt'];assert len(nav)==361 and all(math.isfinite(x) and x>0 for x in nav) and abs(nav[-1]-float(s['terminal_nav_usdt']))<1e-8
  assert len(s['folds'])==12 and all(f['observations']==30 for f in s['folds']) and s['cost_multiplier']==mult
  for t in arc['trades']:
   cb,ub,ca,ua,ref=(D(t[k]) for k in ('cash_before','units_before','cash_after','units_after','reference'))
   if t['status']=='filled':
    q,px=(D(t[k]) for k in ('quantity','execution'));cost=D(t['cost_usdt']);parts=sum((D(v) for v in t['cost_parts'].values()),D(0))
    assert abs(parts-cost)<D('1e-18') and abs((cb+ub*ref)-(ca+ua*ref)-cost)<D('1e-10')
    assert q%D(fs[t['asset']+'USDT']['LOT_SIZE']['stepSize'])==0 and px%D(fs[t['asset']+'USDT']['PRICE_FILTER']['tickSize'])==0 and D(t['participation'])<=D(plan['costs']['maximum_participation']) and ca>=0 and ua>=0
   else:
    assert cb==ca and ub==ua
    if t.get('reason')=='participation':assert D(t['participation'])>D(plan['costs']['maximum_participation'])
   if t.get('signal_available_utc') is not None and not t['terminal']:
    from datetime import datetime
    ns=lambda z:int(datetime.fromisoformat(z.replace('Z','+00:00')).timestamp()*1e9)
    assert ns(t['execution_utc'])-ns(t['signal_available_utc'])==60_000_000_000
  assert s['capacity_rejections']==sum(t.get('reason')=='participation' for t in arc['trades']) and s['rejected_orders']==sum(t['status']!='filled' for t in arc['trades'])
  if row['role']=='single_asset_hold':assert s['terminal_flat'] and s['executions']==2
  if row['role']=='static_equal_hold':assert s['terminal_flat'] and s['executions']==4
  scenes.append({'name':row['name'],'role':row['role'],'cost_multiplier':mult,'net_return_pct':s['net_return_pct'],'net_pnl_usdt':s['net_pnl_usdt'],'cost_usdt':s['cost_usdt'],'max_drawdown_pct':s['max_drawdown_pct'],'daily_mark_drawdown_pct':s['daily_mark_drawdown_pct'],'round_trips':s['round_trips'],'positive_1x_folds':s['positive_1x_folds'],'capacity_rejections':s['capacity_rejections'],'rejected_orders':s['rejected_orders'],'terminal_flat':s['terminal_flat']})
  for f in s['folds']:folds.append({'name':row['name'],'role':row['role'],'cost_multiplier':mult,**f})
for row in batch:
 if row['role']!='candidate':continue
 cfg=report['configs'][row['name']];p=json.loads((ROOT/row['spec']).read_text())['parameters'];near=[]
 for other in batch:
  if other['role']!='candidate':continue
  q=json.loads((ROOT/other['spec']).read_text())['parameters']
  if abs(q['lookback_days']-p['lookback_days'])<=63 and abs(q['absolute_return_hurdle']-p['absolute_return_hurdle'])<=.0500000001:near.append(other['name'])
 frac=sum(report['configs'][n]['scenarios']['3']['net_return_pct']>0 for n in near)/len(near);c=cfg['scenarios']
 sens.append({'name':row['name'],'lookback_days':p['lookback_days'],'hurdle':p['absolute_return_hurdle'],'neighbors':';'.join(near),'neighbor_count':len(near),'neighbor_3x_positive_fraction':frac,'1x_return_pct':c['1']['net_return_pct'],'2x_return_pct':c['2']['net_return_pct'],'3x_return_pct':c['3']['net_return_pct'],'3x_sample_drawdown_pct':c['3']['max_drawdown_pct']})
writecsv(ROUND/'fold_results.csv',folds);writecsv(ROUND/'cost_scenarios.csv',scenes);writecsv(ROUND/'sensitivity.csv',sens)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="620" height="270" viewBox="0 0 620 270"><rect width="100%" height="100%" fill="white"/><text x="20" y="25" font-family="sans-serif" font-size="18" font-weight="bold">3× 成本 OOS 净收益</text>']
for j,h in enumerate((0,.05,.1)):svg.append(f'<text x="{230+j*130}" y="48" text-anchor="middle" font-family="sans-serif">门槛 {h:.0%}</text>')
for i,L in enumerate((63,126,252)):
 y=60+i*65;svg.append(f'<text x="145" y="{y+33}" text-anchor="end" font-family="sans-serif">{L} 天</text>')
 for j,h in enumerate((0,.05,.1)):
  v=next(z['3x_return_pct'] for z in sens if z['lookback_days']==L and z['hurdle']==h);x=165+j*130;svg.extend([f'<rect x="{x}" y="{y}" width="126" height="60" rx="4" fill="{("#b42318" if v<0 else "#16803c")}"/>',f'<text x="{x+63}" y="{y+35}" text-anchor="middle" font-family="sans-serif" fill="white">{v:.2f}%</text>'])
svg.append('</svg>');(ROUND/'sensitivity_surface.svg').write_text('\n'.join(svg)+'\n')
report['integrity_audit']={'status':'passed','reserved_unique_fingerprints':12,'cost_scenes_audited':36,'input_hashes_verified':True,'exchange_filter_archive_hash_verified':True,'daily_nav_observations_per_scene':361,'walk_forward_folds_per_scene':12,'fill_cost_balance_tick_lot_participation_checks':'passed','decision_execution_delay_seconds':60,'evaluation_type':'historical OHLCV backtest; not live execution'}
report['reproduction']={'evaluation':'.venv/bin/python research/experiments/20261013T123949Z/evaluate.py','audit':'.venv/bin/python research/experiments/20261013T123949Z/audit.py','reservations':'All 12 unique fingerprints were reserved successfully before evaluation.'}
report['artifacts']={'fold_results':'research/experiments/20261013T123949Z/fold_results.csv','cost_scenarios':'research/experiments/20261013T123949Z/cost_scenarios.csv','sensitivity':'research/experiments/20261013T123949Z/sensitivity.csv','sensitivity_surface':'research/experiments/20261013T123949Z/sensitivity_surface.svg'}
(ROUND/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps({'audit':'passed','fold_rows':len(folds),'cost_scenes':len(scenes),'sensitivity_variants':len(sens),'report_sha256':sha(ROUND/'report.json')}))
