"""Fixed asymmetric SMA grid with inherited Decimal fills and complete minute NAV."""
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
s=importlib.util.spec_from_file_location('ASYM_metrics',ROOT/'research/experiments/20261001T133655Z/evaluate.py');core=importlib.util.module_from_spec(s);sys.modules[s.name]=core;s.loader.exec_module(core)
signal=core.module('ASYM_signal',ROUND/'signals.py');rules=core.module('ASYM_gates',ROOT/'research/experiments/20261001T213902Z/evaluate.py')
sha=core.sha;CACHE=ROOT/'data/runs'/ROUND.name

def component(sp,rows,closes,k,folds):
 p=sp['parameters'];asset=sp['universe'][0].split('/')[0];capital=p['initial_capital_usdt']
 decisions=signal.asymmetric_sma_hysteresis([r['close'] for r in rows],p['lookback_days'],p['entry_band_fraction'],p['exit_band_fraction'])
 cash=D(capital);units=D(0);trades=[];states=[];v=np.empty(core.POINTS);v[0]=capital
 def execute(i,buy,terminal):
  nonlocal cash,units
  r=rows[i];adv,sigma=core.engine.lagged_cost_inputs(rows,i)
  cash,units,t=core.fill(cash,units,bool(buy),D(str(r['trade_open'])),D(str(adv)),D(str(sigma)),k,p['execution']['filters'][asset+'USDT'],D(r['proxy_vwap5']))
  t.update(decision_index=i,day_offset=i-183,trade_ts_ns=r['trade_ts'],terminal=terminal);trades.append(t)
 for d,i in enumerate(range(183,363)):
  assert rows[i-1]['close_available_ts']<rows[i]['trade_ts'];want=decisions[d]['long']
  if (want and not units) or (not want and units):execute(i,want,False)
  states.append({'day_offset':d,'cash':str(cash),'units':str(units)})
  v[d*core.SPAN+1]=float(cash+units*D(str(rows[i]['trade_open'])))
  v[d*core.SPAN+2:(d+1)*core.SPAN+1]=float(cash)+float(units)*closes[i*1440+1:(i+1)*1440+1]
 if units:execute(363,False,True)
 v[-1]=float(cash+units*D(str(rows[363]['trade_open'])));assert np.all(v>0)
 summary=core.summarize(v,trades,capital,folds,units);segments=[]
 for st in states:
  if not segments or (st['cash'],st['units'])!=(segments[-1]['cash'],segments[-1]['units']):segments.append({**st,'end_day_exclusive':st['day_offset']+1})
  else:segments[-1]['end_day_exclusive']+=1
 return v,{'decisions':decisions,'trades':trades,'position_segments':segments,'terminal_cash':str(cash),'terminal_units':str(units),'summary':summary}

def main():
 replay='--reproduce' in sys.argv;plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:
  assert ledger[b['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',))
  assert registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==b['fingerprint']
 started=datetime.now(timezone.utc).isoformat();data={};prices={};manifest={};oldreports={};dailyrefs={}
 wf=core.module('ASYM_wf',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py')
 validator=wf.WalkForwardValidator(wf.WalkForwardConfig(train_size=180,test_size=30,step_size=30,window_type='rolling',purge_size=0,embargo_size=3))
 folds=[{'fold':f.fold_idx+1,'train_start_index':int(f.train_indices[0]),'train_end_exclusive_index':int(f.train_indices[-1])+1,'test_start_index':int(f.test_indices[0]),'test_end_exclusive_index':int(f.test_indices[-1])+1} for f in validator.split(365)]
 for y,p in plan['periods'].items():
  assert sha(ROOT/p['report'])==p['sha256'];oldreports[y]=json.loads((ROOT/p['report']).read_text());assert folds==oldreports[y]['folds']
  dailyfile=ROOT/'research/experiments'/p['source_round']/'daily_inputs.json.gz';data[y]=json.loads(gzip.decompress(dailyfile.read_bytes()));dailyrefs[y]={'path':str(dailyfile.relative_to(ROOT)),'sha256':sha(dailyfile)}
  prices[y]={};manifest[y]={}
  for asset,d in p['normalized_data'].items():
   path=ROOT/d['path'];assert sha(path)==d['sha256'];frame=pl.read_parquet(path)
   assert frame.height==525600 and frame['is_closed'].all() and frame['open_ts'].is_sorted()
   assert (frame['open_ts'].diff().drop_nulls()==60000000000).all() and (frame['available_ts']-frame['open_ts']==60000000000).all()
   prices[y][asset]=np.asarray(frame['close'].cast(pl.Float64));manifest[y][asset]=d
   for i,r in enumerate(data[y][asset]):assert r['trade_ts']==frame['open_ts'][i*1440+1] and D(str(r['trade_open']))==frame['open'][i*1440+1]
  assert [r['trade_ts'] for r in data[y]['BTC']]==[r['trade_ts'] for r in data[y]['ETH']]
 CACHE.mkdir(parents=True,exist_ok=True);archives={};byfp={b['fingerprint']:b['name'] for b in batch}
 report={'evaluation_started_utc':started,'plan':plan,'data':manifest,'daily_inputs':dailyrefs,'folds':folds,'curve_formula':oldreports['2026']['curve_formula'],'configs':{},'sensitivity':{},'read_only_comparators':{},'forward_observation':{'path':str((ROUND/'forward_report.json').relative_to(ROOT)),'sha256':sha(ROUND/'forward_report.json')},'environment':{'python':sys.version,'numpy':np.__version__,'polars':pl.__version__}}
 for b in batch:
  sp=json.loads((ROOT/b['spec']).read_text());y=b['year'];a={'spec':sp,'fingerprint':b['fingerprint'],'scenes':{}};scenes={}
  for k in ('1','2','3'):
   if b['role']=='component':v,part=component(sp,data[y][b['asset']],prices[y][b['asset']],int(k),folds)
   else:
    names=[byfp[c['fingerprint']] for c in sp['components']];parts=[archives[n]['scenes'][k] for n in names]
    assert [archives[n]['spec']['parameters']['initial_capital_usdt'] for n in names]==[1500,500]
    v=np.load(CACHE/f'{names[0]}_{k}.npy',allow_pickle=False)+np.load(CACHE/f'{names[1]}_{k}.npy',allow_pickle=False)
    trades=[t for p in parts for t in p['trades']];units=sum(D(p['terminal_units']) for p in parts)
    part={'component_names':names,'trades':trades,'terminal_units':str(units),'summary':core.summarize(v,trades,2000,folds,units)}
   part['summary']['first_five_fold_return_pct']=100*(math.prod(1+f['net_return_pct']/100 for f in part['summary']['folds'][:5])-1)
   part['summary']['last_fold_return_pct']=part['summary']['folds'][-1]['net_return_pct']
   a['scenes'][k]=part;scenes[k]=part['summary'];npfile=CACHE/f'{b["name"]}_{k}.npy'
   if replay:assert core.navhash(np.load(npfile,allow_pickle=False))==core.navhash(v)
   else:np.save(npfile,v,allow_pickle=False)
  path=ROUND/'results'/f'{b["name"]}.json.gz'
  if replay:assert json.loads(gzip.decompress(path.read_bytes()))==core.canonical(a),b['name']
  else:core.gzwrite(path,a)
  archives[b['name']]=a;report['configs'][b['name']]={**b,'archive':str(path.relative_to(ROOT)),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])}
  print(json.dumps({'completed':b['name'],'return1':scenes['1']['net_return_pct'],'return3':scenes['3']['net_return_pct'],'minute_DD3':scenes['3']['max_drawdown_pct']}),flush=True)
 for y in plan['periods']:
  for group in ('BTC','ETH','combination'):
   rows={n:r for n,r in report['configs'].items() if r['year']==y and (r.get('asset')==group or r['role']==group)};assert len(rows)==9
   stats={k:{'positive_return_fraction':sum(r['scenes'][k]['net_return_pct']>0 for r in rows.values())/9,'positive_sharpe_fraction':sum((r['scenes'][k]['sharpe_365'] or 0)>0 for r in rows.values())/9,'return_range_pct':[min(r['scenes'][k]['net_return_pct'] for r in rows.values()),max(r['scenes'][k]['net_return_pct'] for r in rows.values())]} for k in ('1','2','3')}
   coords={n:(plan['grid']['entry_band_fraction'].index(r['entry_band']),plan['grid']['exit_band_fraction'].index(r['exit_band'])) for n,r in rows.items()};edges=[]
   for na,ra in rows.items():
    for nb,rb in rows.items():
     if na>=nb:continue
     ca,cb=coords[na],coords[nb]
     if abs(ca[0]-cb[0])+abs(ca[1]-cb[1])==1:edges.append({'a':na,'b':nb,'return_difference_3x_pct':abs(ra['scenes']['3']['net_return_pct']-rb['scenes']['3']['net_return_pct']),'sharpe_difference_3x':abs(ra['scenes']['3']['sharpe_365']-rb['scenes']['3']['sharpe_365'])})
   assert len(edges)==12;cutoff=2*statistics.stdev(e['sharpe_difference_3x'] for e in edges)
   for e in edges:e['cliff_flag_2sd']=e['sharpe_difference_3x']>cutoff
   report['sensitivity'][f'{y}_{group}']={'axes':['entry_band_fraction','exit_band_fraction'],'cells':9,'metrics':stats,'adjacent_edges':edges,'cliff_cutoff':cutoff,'note':'Descriptive2sd threshold only; neither causal selection proof nor significance.'}
 for n,r in report['configs'].items():
  group=r.get('asset','combination');r['criteria']=rules.gates(r['scenes'],report['sensitivity'][f'{r["year"]}_{group}']['metrics']['3']['positive_return_fraction'])
  r['status']='passed' if all(r['criteria'].values()) else 'rejected';r['failed_criteria']=[k for k,v in r['criteria'].items() if not v]
 lookup={(r['year'],r.get('asset','combination'),r['entry_band'],r['exit_band']):n for n,r in report['configs'].items()}
 pairs=[]
 for n,r in report['configs'].items():
  other=lookup[('2026' if r['year']=='2025' else '2025',r.get('asset','combination'),r['entry_band'],r['exit_band'])]
  r['other_period_config']=other;r['both_periods_meet_full_gates']=r['status']==report['configs'][other]['status']=='passed'
  if r['year']=='2025' and r['role']=='combination' and r['both_periods_meet_full_gates']:pairs.append([n,other])
 for y,old in oldreports.items():
  for n,r in old['configs'].items():
   if r['role']=='comparator_combination' or (r['role']=='combination' and r['lookback_days']==65 and r['raw_weights']==[.75,.25]):
    report['read_only_comparators'][n]={'year':y,'source_report':plan['periods'][y]['report'],'source_report_sha256':plan['periods'][y]['sha256'],'fingerprint':r['fingerprint'],'scenes':r['scenes'],'status':r['status'],'scope':'Existing SMA65/75:25 or equal50/50 hold;read-only,not recomputed;hold not equal-risk alpha baseline.'}
 report['summary']={'configs':54,'component_configs':36,'combination_configs':18,'cost_scenes':162,'minute_NAV_points':54*3*core.POINTS,'positive_1x':sum(r['scenes']['1']['net_return_pct']>0 for r in report['configs'].values()),'positive_3x':sum(r['scenes']['3']['net_return_pct']>0 for r in report['configs'].values()),'passed':[n for n,r in report['configs'].items() if r['status']=='passed'],'rejected':[n for n,r in report['configs'].items() if r['status']=='rejected'],'both_periods_passed_combination_pairs':pairs,'actual_component_fills':sum(r['scenes'][k]['executions'] for r in report['configs'].values() if r['role']=='component' for k in ('1','2','3')),'new_live_orders':0}
 report['source_hashes']={str(p.relative_to(ROOT)):sha(p) for p in [ROUND/'spec.json',ROUND/'batch.json',ROUND/'prepare.py',ROUND/'signals.py',ROUND/'evaluate.py',ROUND/'audit.py',ROUND/'forward.py',ROUND/'audit_forward.py',ROOT/'research/experiments/20261001T133655Z/evaluate.py',ROOT/'research/experiments/20261001T133655Z/kernel.py',ROOT/'research/experiments/20261001T213902Z/evaluate.py',ROOT/'research/experiments/20261001T213902Z/audit.py',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py']}
 if replay:
  old=json.loads((ROUND/'report.json').read_text());report['evaluation_started_utc']=old['evaluation_started_utc'];assert core.canonical(report)==old,'full report mismatch'
  print('PASS:all162 scene archives,full minute NAV and frozen report exactly reproduced;ledger unchanged');return
 (ROUND/'report.json').write_text(json.dumps(core.canonical(report),ensure_ascii=False,separators=(',',':'))+'\n')
 (ROUND/'data_manifest.json').write_text(json.dumps({'normalized':manifest,'daily_inputs':dailyrefs,'periods':plan['periods'],'metadata_sha256':plan['execution']['metadata_sha256'],'no_new_market_downloads':True},indent=2)+'\n')
 with (ROUND/'sensitivity.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['config','year','role','asset','entry_band','exit_band','cost','net_return_pct','minute_DD_pct','daily_DD_pct','Sharpe365','Calmar','positive_folds1','round_trips','cost_pct','first_five_folds_return_pct','last_fold_return_pct','status'])
  for n,r in report['configs'].items():
   for k,s in r['scenes'].items():w.writerow([n,r['year'],r['role'],r.get('asset','75:25'),r['entry_band'],r['exit_band'],k,*[s[x] for x in ('net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar')],r['positive_folds_1x'],s['round_trips'],s['cost_pct_initial'],s['first_five_fold_return_pct'],s['last_fold_return_pct'],r['status']])
 print(json.dumps(report['summary']),flush=True)

if __name__=='__main__':main()
