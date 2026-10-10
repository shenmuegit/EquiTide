"""Derived channel/asymmetric-SMA portfolios use exact existing size/cost/timestamp vectors."""
import csv,gzip,importlib.util,json,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
s=importlib.util.spec_from_file_location('hybrid_core',ROOT/'research/experiments/20261001T133655Z/evaluate.py');core=importlib.util.module_from_spec(s);sys.modules[s.name]=core;s.loader.exec_module(core)
gates=core.module('hybrid_gates',ROOT/'research/experiments/20261001T213902Z/evaluate.py').gates
CACHE=ROOT/'data/runs'/ROUND.name
def main():
 replay='--reproduce' in sys.argv;plan=json.loads((ROUND/'spec.json').read_text());newbatch=json.loads((ROUND/'batch.json').read_text());batch=json.loads((ROUND/'grid_batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in newbatch:assert ledger[b['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',)) and registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==b['fingerprint']
 started=datetime.now(timezone.utc).isoformat();arcs={};vectors={};refs={};sources={}
 for b in batch:
  for ref in b['component_refs']:
   fp=ref['fingerprint']
   if fp in refs:continue
   assert core.sha(ROOT/ref['report'])==ref['report_sha256'] and core.sha(ROOT/ref['archive'])==ref['archive_sha256'];old=json.loads((ROOT/ref['report']).read_text());a=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));assert a['fingerprint']==fp and registry.fingerprint(a['spec'])==fp
   assert ledger[fp]['result_available'];assert a['spec']['parameters']['initial_capital_usdt']==ref['capital_usdt']
   assert a['spec']['parameters']['start_utc']==plan['periods'][b['year']]['oos_start_utc'] and a['spec']['parameters']['end_utc']==plan['periods'][b['year']]['terminal_exit_utc']
   refs[fp]={**ref,'year':b['year'],'spec_sha256':core.sha(ROOT/ref['spec'])};arcs[fp]=a;sources[b['year']]=old['folds']
   for k in ('1','2','3'):
    v=np.load(ROOT/'data/runs'/ref['source_round']/f'{ref["name"]}_{k}.npy',allow_pickle=False);assert core.navhash(v)==a['scenes'][k]['summary']['NAV_sha256_f64le'] and len(v)==core.POINTS;vectors[(fp,k)]=v
 CACHE.mkdir(parents=True,exist_ok=True)
 report={'evaluation_started_utc':started,'plan':plan,'component_sources':refs,'folds_by_year':sources,'curve_formula':json.loads((ROOT/plan['periods']['2026']['report']).read_text())['curve_formula'],'configs':{},'sensitivity':{},'forward_observation':{'path':str((ROUND/'forward_report.json').relative_to(ROOT)),'sha256':core.sha(ROUND/'forward_report.json')},'read_only_comparators':{}}
 for b in batch:
  if not b['is_new']:
   ref=b['source_ref'];assert core.sha(ROOT/ref['archive'])==ref['archive_sha256'] and core.sha(ROOT/ref['report'])==ref['report_sha256'] and core.sha(ROOT/b['spec'])==ref['spec_sha256']
   prev=json.loads((ROOT/ref['report']).read_text())['configs'][b['name']];a=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));assert a['fingerprint']==b['fingerprint']
   for k,z in a['scenes'].items():
    v=np.load(ROOT/'data/runs'/ref['source_round']/f'{b["name"]}_{k}.npy',allow_pickle=False);assert core.navhash(v)==z['summary']['NAV_sha256_f64le']
   report['configs'][b['name']]={**b,'archive':ref['archive'],'archive_sha256':ref['archive_sha256'],'scenes':prev['scenes'],'positive_folds_1x':prev['positive_folds_1x'],'source_record_status':prev['status'],'source_record_criteria':prev['criteria']}
   print('READ_ONLY_RESULT:'+b['name'],flush=True);continue
  sp=json.loads((ROOT/b['spec']).read_text());fps=[c['fingerprint'] for c in sp['components']];assert [refs[f]['capital_usdt'] for f in fps]==[1500,500];a={'spec':sp,'fingerprint':b['fingerprint'],'component_refs':b['component_refs'],'scenes':{}};scenes={}
  for k in ('1','2','3'):
   parts=[arcs[f]['scenes'][k] for f in fps];v=vectors[(fps[0],k)]+vectors[(fps[1],k)];trades=[t for p in parts for t in p['trades']];units=sum(D(p['terminal_units']) for p in parts)
   summary=core.summarize(v,trades,2000,sources[b['year']],units);summary.update(first_five_fold_return_pct=100*(__import__('math').prod(1+f['net_return_pct']/100 for f in summary['folds'][:5])-1),last_fold_return_pct=summary['folds'][-1]['net_return_pct']);a['scenes'][k]={'trades':trades,'terminal_units':str(units),'summary':summary};scenes[k]=summary
   path=CACHE/f'{b["name"]}_{k}.npy'
   if replay:assert core.navhash(np.load(path,allow_pickle=False))==core.navhash(v)
   else:np.save(path,v,allow_pickle=False)
  path=ROUND/'results'/f'{b["name"]}.json.gz'
  if replay:assert json.loads(gzip.decompress(path.read_bytes()))==core.canonical(a)
  else:core.gzwrite(path,a)
  report['configs'][b['name']]={**b,'archive':str(path.relative_to(ROOT)),'archive_sha256':core.sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])}
  print(json.dumps({'completed':b['name'],'return3_pct':scenes['3']['net_return_pct'],'minute_DD3_pct':scenes['3']['max_drawdown_pct']}),flush=True)
 for year in ('2025','2026'):
  for direction in plan['grid']['directions']:
   rows={n:r for n,r in report['configs'].items() if r['year']==year and r['direction']==direction};assert len(rows)==9
   stats={k:{'positive_return_fraction':sum(r['scenes'][k]['net_return_pct']>0 for r in rows.values())/9,'positive_sharpe_fraction':sum((r['scenes'][k]['sharpe_365'] or 0)>0 for r in rows.values())/9,'return_range_pct':[min(r['scenes'][k]['net_return_pct'] for r in rows.values()),max(r['scenes'][k]['net_return_pct'] for r in rows.values())]} for k in ('1','2','3')};edges=[]
   coords={n:(plan['grid']['BTC_minimum_volume_ratio'].index(r['BTC_minimum_volume_ratio']),plan['grid']['ETH_EMA_span_days'].index(r['ETH_EMA_span_days'])) for n,r in rows.items()}
   for na,ra in rows.items():
    for nb,rb in rows.items():
     if na>=nb:continue
     ca,cb=coords[na],coords[nb]
     if abs(ca[0]-cb[0])+abs(ca[1]-cb[1])==1:edges.append({'a':na,'b':nb,'return_difference_3x_pct':abs(ra['scenes']['3']['net_return_pct']-rb['scenes']['3']['net_return_pct']),'sharpe_difference_3x':abs(ra['scenes']['3']['sharpe_365']-rb['scenes']['3']['sharpe_365'])})
   assert len(edges)==12;cutoff=2*statistics.stdev(e['sharpe_difference_3x'] for e in edges)
   for e in edges:e['cliff_flag_2sd']=e['sharpe_difference_3x']>cutoff
   report['sensitivity'][f'{year}_{direction}']={'axes':['BTC_minimum_volume_ratio','ETH_EMA_span_days'],'cells':9,'metrics':stats,'adjacent_edges':edges,'cliff_cutoff':cutoff,'note':'Descriptive difference flags,not significance.'}
 for n,r in report['configs'].items():
  if not r['is_new']:
   r.update(criteria=r['source_record_criteria'],status=r['source_record_status'],failed_criteria=[k for k,v in r['source_record_criteria'].items() if not v]);continue
  r['criteria']=gates(r['scenes'],report['sensitivity'][f'{r["year"]}_{r["direction"]}']['metrics']['3']['positive_return_fraction']);r['status']='passed' if all(r['criteria'].values()) else 'rejected';r['failed_criteria']=[k for k,v in r['criteria'].items() if not v]
 lookup={(r['year'],r['direction'],r['BTC_minimum_volume_ratio'],r['ETH_EMA_span_days']):n for n,r in report['configs'].items()};pairs=[]
 for n,r in report['configs'].items():
  other=lookup[('2026' if r['year']=='2025' else '2025',r['direction'],r['BTC_minimum_volume_ratio'],r['ETH_EMA_span_days'])];r['other_period_config']=other;r['both_periods_meet_full_gates']=r['status']==report['configs'][other]['status']=='passed'
  if r['year']=='2025' and r['both_periods_meet_full_gates']:pairs.append([n,other])
 for ref in plan['read_only_comparator_refs']:
  assert core.sha(ROOT/ref['report'])==ref['report_sha256'];old=json.loads((ROOT/ref['report']).read_text());row=old['configs'][ref['name']]
  report['read_only_comparators'][ref['name']]={'year':ref['year'],'kind':ref['kind'],'source_report':ref['report'],'source_report_sha256':ref['report_sha256'],'fingerprint':row['fingerprint'],'ETH_EMA_span_days':ref.get('ETH_EMA_span_days'),'BTC_minimum_volume_ratio':ref.get('BTC_minimum_volume_ratio'),'scenes':row['scenes'],'status':row['status']}
 fresh={n:c for n,c in report['configs'].items() if c['is_new']}
 report['summary']={'new_configs':18,'new_cost_scenes':54,'new_minute_NAV_points':54*core.POINTS,'reused_grid_configs':0,'reused_cost_scenes':0,'grid_configs':18,'grid_cost_scenes':54,'reused_component_configs':12,'positive_1x':sum(c['scenes']['1']['net_return_pct']>0 for c in fresh.values()),'positive_3x':sum(c['scenes']['3']['net_return_pct']>0 for c in fresh.values()),'passed':[n for n,c in fresh.items() if c['status']=='passed'],'rejected':[n for n,c in fresh.items() if c['status']=='rejected'],'both_periods_passed_combination_pairs':pairs,'new_both_periods_passed_combination_pairs':[pair for pair in pairs if report['configs'][pair[0]]['is_new']],'new_component_backtests':0,'new_live_orders':0,'source_component_fills_read_only':sum(s['summary']['executions'] for a in arcs.values() for s in a['scenes'].values())}
 report['source_hashes']={str(p.relative_to(ROOT)):core.sha(p) for p in [ROUND/'spec.json',ROUND/'batch.json',ROUND/'grid_batch.json',ROUND/'restore_cache.py',ROUND/'prepare.py',ROUND/'evaluate.py',ROUND/'audit.py',ROOT/'research/experiments/20261001T133655Z/evaluate.py',ROOT/'research/experiments/20261001T213902Z/audit.py',ROOT/'research/experiments/20261001T213902Z/evaluate.py',ROOT/'research/experiments/20261001T013355Z/evaluate.py',ROOT/'research/experiments/20261001T133655Z/kernel.py',ROOT/'research/experiments/20261001T113625Z/signals.py',ROOT/'research/automation/registry.py']}
 if replay:
  old=json.loads((ROUND/'report.json').read_text());report['evaluation_started_utc']=old['evaluation_started_utc'];assert core.canonical(report)==old;print('PASS:all54 NEW mixed-volume-EMA cost scenes exactly reproduced;matched controls read-only verified;full report reproduced;ledger unchanged');return
 (ROUND/'report.json').write_text(json.dumps(core.canonical(report),ensure_ascii=False,separators=(',',':'))+'\n')
 (ROUND/'data_manifest.json').write_text(json.dumps({'periods':plan['periods'],'component_sources':refs,'forward_observation':report['forward_observation']},indent=2)+'\n')
 with (ROUND/'sensitivity.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['config','year','direction','BTC_minimum_volume_ratio','ETH_EMA_span_days','cost','return_pct','minute_DD_pct','daily_DD_pct','Sharpe365','Calmar','positive_folds1','round_trips','cost_pct','status'])
  for n,r in report['configs'].items():
   for k,s in r['scenes'].items():w.writerow([n,r['year'],r['direction'],r['BTC_minimum_volume_ratio'],r['ETH_EMA_span_days'],k,*[s[x] for x in ('net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar')],r['positive_folds_1x'],s['round_trips'],s['cost_pct_initial'],r['status']])
 print(json.dumps(report['summary']),flush=True)
if __name__=='__main__':main()
