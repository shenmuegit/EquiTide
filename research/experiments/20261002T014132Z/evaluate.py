"""Derived hybrid portfolios use exact existing size/cost/timestamp vectors."""
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
 replay='--reproduce' in sys.argv;plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:assert ledger[b['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',)) and registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==b['fingerprint']
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
  sp=json.loads((ROOT/b['spec']).read_text());fps=[c['fingerprint'] for c in sp['components']];assert [refs[f]['capital_usdt'] for f in fps]==[1500,500];a={'spec':sp,'fingerprint':b['fingerprint'],'component_refs':b['component_refs'],'scenes':{}};scenes={}
  for k in ('1','2','3'):
   parts=[arcs[f]['scenes'][k] for f in fps];v=vectors[(fps[0],k)]+vectors[(fps[1],k)];trades=[t for p in parts for t in p['trades']];units=sum(D(p['terminal_units']) for p in parts)
   summary=core.summarize(v,trades,2000,sources[b['year']],units);a['scenes'][k]={'trades':trades,'terminal_units':str(units),'summary':summary};scenes[k]=summary
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
   coords={n:(plan['grid']['SMA_lookback_days'].index(r['SMA_lookback_days']),plan['grid']['EMA_span_days'].index(r['EMA_span_days'])) for n,r in rows.items()}
   for na,ra in rows.items():
    for nb,rb in rows.items():
     if na>=nb:continue
     ca,cb=coords[na],coords[nb]
     if abs(ca[0]-cb[0])+abs(ca[1]-cb[1])==1:edges.append({'a':na,'b':nb,'return_difference_3x_pct':abs(ra['scenes']['3']['net_return_pct']-rb['scenes']['3']['net_return_pct']),'sharpe_difference_3x':abs(ra['scenes']['3']['sharpe_365']-rb['scenes']['3']['sharpe_365'])})
   assert len(edges)==12;cutoff=2*statistics.stdev(e['sharpe_difference_3x'] for e in edges)
   for e in edges:e['cliff_flag_2sd']=e['sharpe_difference_3x']>cutoff
   report['sensitivity'][f'{year}_{direction}']={'axes':['SMA_lookback_days','EMA_span_days'],'cells':9,'metrics':stats,'adjacent_edges':edges,'cliff_cutoff':cutoff,'note':'Descriptive difference flags,not significance.'}
 for n,r in report['configs'].items():
  r['criteria']=gates(r['scenes'],report['sensitivity'][f'{r["year"]}_{r["direction"]}']['metrics']['3']['positive_return_fraction']);r['status']='passed' if all(r['criteria'].values()) else 'rejected';r['failed_criteria']=[k for k,v in r['criteria'].items() if not v]
 lookup={(r['year'],r['direction'],r['SMA_lookback_days'],r['EMA_span_days']):n for n,r in report['configs'].items()};pairs=[]
 for n,r in report['configs'].items():
  other=lookup[('2026' if r['year']=='2025' else '2025',r['direction'],r['SMA_lookback_days'],r['EMA_span_days'])];r['other_period_config']=other;r['both_periods_meet_full_gates']=r['status']==report['configs'][other]['status']=='passed'
  if r['year']=='2025' and r['both_periods_meet_full_gates']:pairs.append([n,other])
 for year in ('2025','2026'):
  for kind,rid in plan['component_report_rounds'][year].items():
   old=json.loads((ROOT/'research/experiments'/rid/'report.json').read_text())
   for n,r in old['configs'].items():
    if r['role']=='comparator_combination' and kind=='SMA':
     report['read_only_comparators'][n]={'year':year,'kind':'hold50/50','source_report':f'research/experiments/{rid}/report.json','fingerprint':r['fingerprint'],'scenes':r['scenes'],'status':r['status']};continue
    if r['role']!='combination':continue
    matched=(kind=='SMA' and r['lookback_days']==65 and r['raw_weights']==[.75,.25]) or (kind=='EMA' and r['year']==year and r['span_days']==50 and r['band']==.015)
    if matched:report['read_only_comparators'][n]={'year':year,'kind':kind,'source_report':f'research/experiments/{rid}/report.json','fingerprint':r['fingerprint'],'scenes':r['scenes'],'status':r['status']}
 report['summary']={'new_configs':36,'new_cost_scenes':108,'new_minute_NAV_points':36*3*core.POINTS,'reused_component_configs':24,'positive_1x':sum(r['scenes']['1']['net_return_pct']>0 for r in report['configs'].values()),'positive_3x':sum(r['scenes']['3']['net_return_pct']>0 for r in report['configs'].values()),'passed':[n for n,r in report['configs'].items() if r['status']=='passed'],'rejected':[n for n,r in report['configs'].items() if r['status']=='rejected'],'both_periods_passed_pairs':pairs,'new_component_backtests':0}
 report['source_hashes']={str(p.relative_to(ROOT)):core.sha(p) for p in [ROUND/'spec.json',ROUND/'batch.json',ROUND/'prepare.py',ROUND/'evaluate.py',ROUND/'audit.py',ROOT/'research/experiments/20261001T133655Z/evaluate.py',ROOT/'research/experiments/20261001T213902Z/audit.py']}
 if replay:
  old=json.loads((ROUND/'report.json').read_text());report['evaluation_started_utc']=old['evaluation_started_utc'];assert core.canonical(report)==old;print('PASS:all108 hybrid archives,minute NAV and full frozen report exactly reproduced;ledger unchanged');return
 (ROUND/'report.json').write_text(json.dumps(core.canonical(report),ensure_ascii=False,separators=(',',':'))+'\n')
 (ROUND/'data_manifest.json').write_text(json.dumps({'periods':plan['periods'],'component_sources':refs,'forward_observation':report['forward_observation']},indent=2)+'\n')
 with (ROUND/'sensitivity.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['config','year','direction','SMA_N','EMA_span','cost','return_pct','minute_DD_pct','daily_DD_pct','Sharpe365','Calmar','positive_folds1','round_trips','cost_pct','status'])
  for n,r in report['configs'].items():
   for k,s in r['scenes'].items():w.writerow([n,r['year'],r['direction'],r['SMA_lookback_days'],r['EMA_span_days'],k,*[s[x] for x in ('net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar')],r['positive_folds_1x'],s['round_trips'],s['cost_pct_initial'],r['status']])
 print(json.dumps(report['summary']),flush=True)
if __name__=='__main__':main()
