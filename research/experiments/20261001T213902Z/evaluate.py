"""Derive reserved portfolios from authenticated, already-sized net components."""
import csv
import gzip
import hashlib
import importlib.util
import json
import statistics
import sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
ss=importlib.util.spec_from_file_location('inherited_metrics',ROOT/'research/experiments/20261001T133655Z/evaluate.py')
core=importlib.util.module_from_spec(ss);sys.modules[ss.name]=core;ss.loader.exec_module(core)
sha=core.sha;canonical=core.canonical;CACHE=ROOT/'data/runs'/ROUND.name

def gates(s,positive_fraction):
 ratio=s['1']['gross_reference_PnL_to_execution_cost'];pf=sum(f['net_return_pct']>0 for f in s['1']['folds'])
 return {'positive_all_costs':all(x['net_return_pct']>0 for x in s.values()),'four_positive_1x_folds':pf>=4,'minute_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':positive_fraction>=.6,'two_round_trips1':s['1']['round_trips']>=2,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(x['cash_or_units_violations']==0 for x in s.values()),'terminal_flat':all(D(x['terminal_units'])==0 for x in s.values())}

def main():
 replay='--reproduce' in sys.argv
 plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:
  assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==b['fingerprint']
  assert ledger[b['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',))
 reports={};archives={};vectors={};refs={}
 for y,src in plan['periods'].items():
  assert sha(ROOT/src['report'])==src['sha256'];reports[y]=json.loads((ROOT/src['report']).read_text())
  for b in batch:
   if b['year']!=y:continue
   for name in b['component_names']:
    key=(y,name)
    if key in archives:continue
    r=reports[y]['configs'][name];path=ROOT/r['archive'];assert sha(path)==r['archive_sha256']
    a=json.loads(gzip.decompress(path.read_bytes()));assert a['fingerprint']==r['fingerprint']
    assert ledger[r['fingerprint']]['result_available'];assert a['scenes'].keys()==r['scenes'].keys()
    archives[key]=a
    refs[f'{y}/{name}']={'report':src['report'],'report_sha256':src['sha256'],'spec':r['spec_path'],'spec_sha256':sha(ROOT/r['spec_path']),'archive':r['archive'],'archive_sha256':r['archive_sha256'],'fingerprint':r['fingerprint'],'capital_usdt':r['parameters']['initial_capital_usdt'],'asset':r['asset'],'NAV_sha256_by_cost':{k:s['NAV_sha256_f64le'] for k,s in r['scenes'].items()}}
    for k in ('1','2','3'):
     v=np.load(ROOT/'data/runs'/src['source_round']/f'{name}_{k}.npy',allow_pickle=False)
     assert len(v)==core.POINTS and core.navhash(v)==r['scenes'][k]['NAV_sha256_f64le']
     assert a['scenes'][k]['summary']==r['scenes'][k]
     assert v[0]==r['parameters']['initial_capital_usdt'];vectors[(y,name,k)]=v
 CACHE.mkdir(parents=True,exist_ok=True)
 report={'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'component_sources':refs,'periods':{y:{'folds':r['folds'],'data':r['data'],'curve_formula':r['curve_formula']} for y,r in reports.items()},'configs':{},'read_only_diagonals':{},'read_only_comparators':{},'sensitivity':{},'environment':{'python':sys.version,'numpy':np.__version__}}
 for b in batch:
  y=b['year'];names=b['component_names'];sp=json.loads((ROOT/b['spec']).read_text())
  assert [archives[(y,n)]['fingerprint'] for n in names]==[c['fingerprint'] for c in sp['components']]
  assert [float(archives[(y,n)]['spec']['parameters']['initial_capital_usdt']) for n in names]==[2000*w for w in b['raw_weights']]
  scenes={};archive={'spec':sp,'fingerprint':b['fingerprint'],'component_refs':[refs[f'{y}/{n}'] for n in names],'scenes':{}}
  for k in ('1','2','3'):
   parts=[archives[(y,n)]['scenes'][k] for n in names]
   v=vectors[(y,names[0],k)]+vectors[(y,names[1],k)]
   trades=[t for p in parts for t in p['trades']];units=sum(D(p['terminal_units']) for p in parts)
   m=core.summarize(v,trades,2000,reports[y]['folds'],units)
   a={'component_names':names,'trades':trades,'terminal_units':str(units),'summary':m};archive['scenes'][k]=a;scenes[k]=m
   path=CACHE/f'{b["name"]}_{k}.npy'
   if replay:assert core.navhash(np.load(path,allow_pickle=False))==m['NAV_sha256_f64le']
   else:np.save(path,v,allow_pickle=False)
  path=ROUND/'results'/f'{b["name"]}.json.gz'
  if replay:assert canonical(archive)==json.loads(gzip.decompress(path.read_bytes())),b['name']
  else:core.gzwrite(path,archive)
  report['configs'][b['name']]={**b,'role':'combination','archive':str(path.relative_to(ROOT)),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])}
  print(json.dumps({'completed':b['name'],'return3_pct':scenes['3']['net_return_pct'],'DD3_pct':scenes['3']['max_drawdown_pct'],'positive_folds1':report['configs'][b['name']]['positive_folds_1x']}),flush=True)
 for y,old in reports.items():
  for name,r in old['configs'].items():
   if r['role']=='combination':
    assert ledger[r['fingerprint']]['result_available']
    report['read_only_diagonals'][name]={'year':y,'BTC_lookback_days':r['lookback_days'],'ETH_lookback_days':r['lookback_days'],'raw_weights':r['raw_weights'],'fingerprint':r['fingerprint'],'source_report':plan['periods'][y]['report'],'source_report_sha256':plan['periods'][y]['sha256'],'scenes':r['scenes'],'status':r['status'],'criteria':r['criteria'],'positive_folds_1x':r['positive_folds_1x']}
   elif r['role']=='comparator_combination':report['read_only_comparators'][name]={'year':y,'source_report':plan['periods'][y]['report'],'fingerprint':r['fingerprint'],'scenes':r['scenes'],'scope':'Previously registered equal50/50 hold; descriptive unmatched weight/exposure baseline, not equal-risk alpha.'}
 allrows={**report['configs'],**report['read_only_diagonals']}
 for y in reports:
  for wb,_ in plan['grid']['raw_weight_pairs']:
   rows={n:r for n,r in allrows.items() if r['year']==y and r['raw_weights'][0]==wb};assert len(rows)==9
   coords={n:(r['BTC_lookback_days'],r['ETH_lookback_days']) for n,r in rows.items()};assert len(set(coords.values()))==9
   stats={k:{'positive_return_fraction':sum(r['scenes'][k]['net_return_pct']>0 for r in rows.values())/9,'positive_sharpe_fraction':sum((r['scenes'][k]['sharpe_365'] or 0)>0 for r in rows.values())/9,'return_range_pct':[min(r['scenes'][k]['net_return_pct'] for r in rows.values()),max(r['scenes'][k]['net_return_pct'] for r in rows.values())]} for k in ('1','2','3')}
   edges=[]
   for na,ra in rows.items():
    for nb,rb in rows.items():
     if na>=nb:continue
     ca,cb=coords[na],coords[nb]
     if abs(ca[0]-cb[0])+abs(ca[1]-cb[1])==5:edges.append({'a':na,'b':nb,'return_difference_3x_pct':abs(ra['scenes']['3']['net_return_pct']-rb['scenes']['3']['net_return_pct']),'sharpe_difference_3x':abs(ra['scenes']['3']['sharpe_365']-rb['scenes']['3']['sharpe_365'])})
   assert len(edges)==12
   cutoff=2*statistics.stdev(e['sharpe_difference_3x'] for e in edges)
   for e in edges:e['cliff_flag_2sd']=e['sharpe_difference_3x']>cutoff
   group=f'{y}_w{wb}';report['sensitivity'][group]={'axes':['BTC_lookback_days','ETH_lookback_days'],'cells':9,'new_cells':6,'read_only_cells':3,'metrics':stats,'adjacent_edges':edges,'cliff_cutoff':cutoff,'note':'Descriptive2sd difference threshold, not significance; correlated histories/grid trials are development evidence.'}
 for n,r in report['configs'].items():
  fraction=report['sensitivity'][f'{r["year"]}_w{r["raw_weights"][0]}']['metrics']['3']['positive_return_fraction']
  r['criteria']=gates(r['scenes'],fraction);r['status']='passed' if all(r['criteria'].values()) else 'rejected';r['failed_criteria']=[k for k,v in r['criteria'].items() if not v]
 lookup={(r['year'],r['BTC_lookback_days'],r['ETH_lookback_days'],r['raw_weights'][0]):n for n,r in report['configs'].items()}
 paired=[]
 for n,r in report['configs'].items():
  other=lookup[('2026' if r['year']=='2025' else '2025',r['BTC_lookback_days'],r['ETH_lookback_days'],r['raw_weights'][0])]
  r['other_period_config']=other;r['both_periods_meet_full_gates']=r['status']==report['configs'][other]['status']=='passed'
  if r['year']=='2025' and r['both_periods_meet_full_gates']:paired.append({'BTC_lookback_days':r['BTC_lookback_days'],'ETH_lookback_days':r['ETH_lookback_days'],'raw_weights':r['raw_weights'],'configs':[n,other]})
 report['summary']={'new_configs':36,'new_cost_scenes':108,'new_minute_NAV_points':36*3*core.POINTS,'read_only_diagonal_configs':18,'displayed_grid_cells':54,'displayed_grid_cost_scenes':162,'passed':[n for n,r in report['configs'].items() if r['status']=='passed'],'rejected':[n for n,r in report['configs'].items() if r['status']=='rejected'],'positive_1x':sum(r['scenes']['1']['net_return_pct']>0 for r in report['configs'].values()),'positive_3x':sum(r['scenes']['3']['net_return_pct']>0 for r in report['configs'].values()),'both_periods_passed_pairs':paired,'new_component_backtests':0,'new_live_orders':0}
 report['source_hashes']={str(p.relative_to(ROOT)):sha(p) for p in [ROUND/'prepare.py',ROUND/'evaluate.py',ROUND/'audit.py',ROUND/'spec.json',ROUND/'batch.json',ROOT/'research/experiments/20261001T133655Z/evaluate.py',ROOT/'research/experiments/20261001T133655Z/kernel.py',ROOT/'research/experiments/20261001T113625Z/signals.py',ROOT/'research/experiments/20261001T013355Z/evaluate.py']}
 if replay:
  old=json.loads((ROUND/'report.json').read_text());report['evaluation_started_utc']=old['evaluation_started_utc'];assert canonical(report)==old,'frozen full report mismatch'
  print('PASS:all108 new scene archives, full minute vectors and report exactly reproduced;diagonals read only;ledger unchanged');return
 (ROUND/'report.json').write_text(json.dumps(canonical(report),ensure_ascii=False,separators=(',',':'))+'\n')
 (ROUND/'data_manifest.json').write_text(json.dumps({'periods':plan['periods'],'component_sources':refs,'no_new_market_data':True,'no_new_component_backtests':True},indent=2)+'\n')
 with (ROUND/'sensitivity.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['config','year','BTC_N','ETH_N','raw_BTC_weight','raw_ETH_weight','cost','return_pct','minute_DD_pct','daily_DD_pct','Sharpe365','Calmar','positive_folds1','component_round_trips','cost_pct_initial','status','read_only'])
  for n,r in allrows.items():
   for k,s in r['scenes'].items():w.writerow([n,r['year'],r['BTC_lookback_days'],r['ETH_lookback_days'],*r['raw_weights'],k,*[s[x] for x in ('net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar')],r['positive_folds_1x'],s['round_trips'],s['cost_pct_initial'],r['status'],n in report['read_only_diagonals']])
 print(json.dumps(report['summary']),flush=True)

if __name__=='__main__':main()
