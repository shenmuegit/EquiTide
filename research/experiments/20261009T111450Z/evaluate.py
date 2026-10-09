"""New relative quote-turnover entry confirmation using existing Decimal fills and complete minute NAV."""
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
s=importlib.util.spec_from_file_location('CHANNEL_metrics',ROOT/'research/experiments/20261001T133655Z/evaluate.py');core=importlib.util.module_from_spec(s);sys.modules[s.name]=core;s.loader.exec_module(core)
signal=core.module('CHANNEL_signal',ROUND/'signals.py');rules=core.module('CHANNEL_gates',ROOT/'research/experiments/20261001T213902Z/evaluate.py')
sha=core.sha;CACHE=ROOT/'data/runs'/ROUND.name

def component(sp,rows,closes,k,folds):
 p=sp['parameters'];asset=sp['universe'][0].split('/')[0];capital=p['initial_capital_usdt']
 decisions=signal.volume_channel(rows,p['entry_lookback_days'],p['exit_lookback_days'],p['volume_lookback_days'],p['minimum_volume_ratio'])
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
 replay='--reproduce' in sys.argv;plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());grid=json.loads((ROUND/'grid_batch.json').read_text());ledger=registry.read_records(ROOT/'research/automation/registry.jsonl')
 for b in batch:assert ledger[b['fingerprint']]['status'] in (('passed','rejected') if replay else ('reserved',)) and registry.fingerprint(json.loads((ROOT/b['spec']).read_text()))==b['fingerprint']
 started=datetime.now(timezone.utc).isoformat();data={};prices={};manifest={};dailyrefs={};folds=None;oldreport=None
 wf=core.module('volume_WFV',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py');validator=wf.WalkForwardValidator(wf.WalkForwardConfig(train_size=180,test_size=30,step_size=30,window_type='rolling',purge_size=0,embargo_size=3))
 folds=[{'fold':f.fold_idx+1,'train_start_index':int(f.train_indices[0]),'train_end_exclusive_index':int(f.train_indices[-1])+1,'test_start_index':int(f.test_indices[0]),'test_end_exclusive_index':int(f.test_indices[-1])+1}for f in validator.split(365)]
 for year,p in plan['periods'].items():
  assert sha(ROOT/p['report'])==p['sha256'];oldreport=json.loads((ROOT/p['report']).read_text());assert folds==oldreport['folds'];file=ROOT/'research/experiments'/p['source_round']/'daily_inputs.json.gz';data[year]=json.loads(gzip.decompress(file.read_bytes()));dailyrefs[year]={'path':str(file.relative_to(ROOT)),'sha256':sha(file)};prices[year]={};manifest[year]={}
  for asset,d in p['normalized_data'].items():
   assert sha(ROOT/d['path'])==d['sha256'];frame=pl.read_parquet(ROOT/d['path']);assert frame.height==525600 and frame['is_closed'].all() and (frame['open_ts'].diff().drop_nulls()==60000000000).all() and (frame['available_ts']-frame['open_ts']==60000000000).all();prices[year][asset]=np.asarray(frame['close'].cast(pl.Float64));manifest[year][asset]=d
   for i,row in enumerate(data[year][asset]):assert row['trade_ts']==frame['open_ts'][i*1440+1] and D(str(row['trade_open']))==frame['open'][i*1440+1] and frame.slice(i*1440,1440)['quote_volume'].sum()==D(row['quote_volume'])
  assert [r['trade_ts']for r in data[year]['BTC']]==[r['trade_ts']for r in data[year]['ETH']]
 CACHE.mkdir(parents=True,exist_ok=True);archives={};cache_by_fp={};report={'evaluation_started_utc':started,'plan':plan,'data':manifest,'daily_inputs':dailyrefs,'folds':folds,'curve_formula':oldreport['curve_formula'],'volume_input_precision':'Existing daily quote-volume aggregates are exact serialized Decimal sums of1440 normalized UTC minute quote volumes;Decimal28 reference means/comparisons preserve source precision. Independent audit verifies every daily sum.','configs':{},'sensitivity':{},'read_only_comparators':{},'forward_observation':{'path':str((ROUND/'forward_report.json').relative_to(ROOT)),'sha256':sha(ROUND/'forward_report.json')}}
 for b in grid:
  sp=json.loads((ROOT/b['spec']).read_text());year=b['year']
  if not b['is_new']:
   ref=b['source_ref'];assert ledger[b['fingerprint']]['result_available'] and sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/b['spec'])==ref['spec_sha256'];old=json.loads((ROOT/ref['report']).read_text())['configs'][b['name']];a=json.loads(gzip.decompress((ROOT/ref['archive']).read_bytes()));assert a['spec']==sp and a['fingerprint']==b['fingerprint'] and {k:z['summary']for k,z in a['scenes'].items()}==old['scenes']
   for k in ('1','2','3'):assert core.navhash(np.load(ROOT/'data/runs'/ref['source_round']/f'{b["name"]}_{k}.npy',allow_pickle=False))==old['scenes'][k]['NAV_sha256_f64le']
   archives[b['fingerprint']]=a;cache_by_fp[b['fingerprint']]=(ref['source_round'],b['name']);report['configs'][b['name']]={**b,'archive':ref['archive'],'archive_sha256':ref['archive_sha256'],'scenes':old['scenes'],'positive_folds_1x':old['positive_folds_1x'],'status':old['status'],'criteria':old['criteria'],'source_record_status':old['status'],'source_record_criteria':old['criteria']};print('READ_ONLY_RESULT:'+b['name'],flush=True);continue
  a={'spec':sp,'fingerprint':b['fingerprint'],'scenes':{}};scenes={}
  for k in ('1','2','3'):
   if b['role']=='component':v,part=component(sp,data[year]['BTC'],prices[year]['BTC'],int(k),folds)
   else:
    fps=[q['fingerprint']for q in sp['components']];parts=[archives[fp]['scenes'][k]for fp in fps];assert [archives[fp]['spec']['parameters']['initial_capital_usdt']for fp in fps]==[1500,500] and [q['weight']for q in sp['components']]==[.75,.25]
    v=sum((np.load(ROOT/'data/runs'/cache_by_fp[fp][0]/f'{cache_by_fp[fp][1]}_{k}.npy',allow_pickle=False)for fp in fps));trades=[t for part in parts for t in part['trades']];units=sum(D(part['terminal_units'])for part in parts);part={'component_names':[cache_by_fp[fp][1]for fp in fps],'trades':trades,'terminal_units':str(units),'summary':core.summarize(v,trades,2000,folds,units)}
   z=part['summary'];z['first_five_fold_return_pct']=100*(math.prod(1+q['net_return_pct']/100 for q in z['folds'][:5])-1);z['last_fold_return_pct']=z['folds'][-1]['net_return_pct'];a['scenes'][k]=part;scenes[k]=z;file=CACHE/f'{b["name"]}_{k}.npy'
   if replay:assert core.navhash(np.load(file,allow_pickle=False))==core.navhash(v)
   else:np.save(file,v,allow_pickle=False)
  archive=ROUND/'results'/f'{b["name"]}.json.gz'
  if replay:assert json.loads(gzip.decompress(archive.read_bytes()))==core.canonical(a)
  else:core.gzwrite(archive,a)
  archives[b['fingerprint']]=a;cache_by_fp[b['fingerprint']]=(ROUND.name,b['name']);report['configs'][b['name']]={**b,'archive':str(archive.relative_to(ROOT)),'archive_sha256':sha(archive),'scenes':scenes,'positive_folds_1x':sum(q['net_return_pct']>0 for q in scenes['1']['folds'])};print(json.dumps({'completed':b['name'],'return1_pct':scenes['1']['net_return_pct'],'return3_pct':scenes['3']['net_return_pct'],'DD3_pct':scenes['3']['max_drawdown_pct']}),flush=True)
 for year in ('2025','2026'):
  for group in ('BTC','combination'):
   rows={n:c for n,c in report['configs'].items()if c['year']==year and (c.get('asset')==group or c['role']==group)};assert len(rows)==9
   stats={k:{'positive_return_fraction':sum(c['scenes'][k]['net_return_pct']>0 for c in rows.values())/9,'positive_sharpe_fraction':sum((c['scenes'][k]['sharpe_365']or 0)>0 for c in rows.values())/9,'return_range_pct':[min(c['scenes'][k]['net_return_pct']for c in rows.values()),max(c['scenes'][k]['net_return_pct']for c in rows.values())]}for k in ('1','2','3')};edges=[]
   coords={n:(plan['grid']['volume_lookback_days'].index(c['volume_lookback_days']),plan['grid']['minimum_volume_ratio'].index(c['minimum_volume_ratio']))for n,c in rows.items()}
   for na,ca in rows.items():
    for nb,cb in rows.items():
     if na>=nb:continue
     a,b=coords[na],coords[nb]
     if abs(a[0]-b[0])+abs(a[1]-b[1])==1:edges.append({'a':na,'b':nb,'return_difference_3x_pct':abs(ca['scenes']['3']['net_return_pct']-cb['scenes']['3']['net_return_pct']),'sharpe_difference_3x':abs((ca['scenes']['3']['sharpe_365']or 0)-(cb['scenes']['3']['sharpe_365']or 0))})
   assert len(edges)==12;cutoff=2*statistics.stdev(e['sharpe_difference_3x']for e in edges)
   for e in edges:e['cliff_flag_2sd']=e['sharpe_difference_3x']>cutoff
   report['sensitivity'][year+'_'+group]={'axes':['volume_lookback_days','minimum_volume_ratio'],'cells':9,'metrics':stats,'adjacent_edges':edges,'cliff_cutoff':cutoff,'scope':'Descriptive2sd flags only,not significance/PBO or independent final optimization.'}
 for c in report['configs'].values():
  if c['is_new']:
   group='BTC' if c['role']=='component'else 'combination';c['criteria']=rules.gates(c['scenes'],report['sensitivity'][c['year']+'_'+group]['metrics']['3']['positive_return_fraction']);c['status']='passed'if all(c['criteria'].values())else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items()if not v]
  other=next(o for o in report['configs'].values()if o['year']!=c['year'] and o['role']==c['role'] and o.get('asset')==c.get('asset') and o.get('volume_lookback_days')==c.get('volume_lookback_days') and o.get('minimum_volume_ratio')==c.get('minimum_volume_ratio'));c['other_period_config']=other['name']
 for c in report['configs'].values():c['both_periods_meet_full_gates']=c['status']==report['configs'][c['other_period_config']]['status']=='passed'
 for ref in plan['read_only_comparator_refs']:
  assert sha(ROOT/ref['report'])==ref['report_sha256'];row=json.loads((ROOT/ref['report']).read_text())['configs'][ref['name']];report['read_only_comparators'][ref['name']]={'year':ref['year'],'kind':ref['kind'],'source_report':ref['report'],'source_report_sha256':ref['report_sha256'],'fingerprint':row['fingerprint'],'scenes':row['scenes'],'status':row['status']}
 fresh=[c for c in report['configs'].values()if c['is_new']];pairs=[[c['name'],c['other_period_config']]for c in fresh if c['year']=='2025'and c['role']=='combination'and c['both_periods_meet_full_gates']];allpairs=[[c['name'],c['other_period_config']]for c in report['configs'].values()if c['year']=='2025'and c['role']=='combination'and c['both_periods_meet_full_gates']]
 report['summary']={'new_configs':32,'new_component_configs':16,'new_combination_configs':16,'new_cost_scenes':96,'new_minute_NAV_points':96*core.POINTS,'old_component_configs_read_only':4,'old_component_cost_scenes_read_only':12,'old_combination_configs_read_only':2,'old_combination_cost_scenes_read_only':6,'positive_1x':sum(c['scenes']['1']['net_return_pct']>0 for c in fresh),'positive_3x':sum(c['scenes']['3']['net_return_pct']>0 for c in fresh),'passed':[c['name']for c in fresh if c['status']=='passed'],'rejected':[c['name']for c in fresh if c['status']=='rejected'],'new_both_periods_passed_combination_pairs':pairs,'both_periods_passed_combination_pairs':allpairs,'new_component_fills':sum(c['scenes'][k]['executions']for c in fresh if c['role']=='component'for k in ('1','2','3')),'read_only_component_fills':sum(c['scenes'][k]['executions']for c in report['configs'].values()if not c['is_new']and c['role']=='component'for k in ('1','2','3')),'new_live_orders':0}
 report['source_hashes']={str(q.relative_to(ROOT)):sha(q)for q in [ROUND/n for n in ('spec.json','batch.json','grid_batch.json','prepare.py','design.py','signals.py','check_signals.py','evaluate.py','audit.py','forward.py','audit_forward.py')]+[ROOT/'research/experiments/20261002T174933Z/evaluate.py',ROOT/'research/experiments/20261001T133655Z/evaluate.py',ROOT/'research/experiments/20261001T133655Z/kernel.py',ROOT/'research/experiments/20261001T213902Z/evaluate.py',ROOT/'research/experiments/20261001T213902Z/audit.py',ROOT/'.agents/skills/walk-forward-validation/scripts/walk_forward.py',ROOT/'research/automation/registry.py']}
 if replay:
  expected=json.loads((ROUND/'report.json').read_text());report['evaluation_started_utc']=expected['evaluation_started_utc'];assert core.canonical(report)==expected;print('PASS:all96 NEW volume-boundary scenes and full report exactly reproduced;18oldsource/portfolio scenes read-only verified,noHTTP/ledger write');return
 (ROUND/'report.json').write_text(json.dumps(core.canonical(report),ensure_ascii=False,separators=(',',':'))+'\n');(ROUND/'data_manifest.json').write_text(json.dumps({'normalized':manifest,'daily_inputs':dailyrefs,'periods':plan['periods'],'metadata_sha256':plan['execution']['metadata_sha256'],'no_new_market_downloads':True},indent=2)+'\n')
 with (ROUND/'sensitivity.csv').open('w',newline='')as fh:
  w=csv.writer(fh,lineterminator='\n');w.writerow(['config','year','role','asset','is_new','volume_lookback_days','minimum_volume_ratio','cost','net_return_pct','minute_DD_pct','daily_DD_pct','Sharpe365','Calmar','positive_folds1','round_trips','cost_pct','status'])
  for name,c in report['configs'].items():
   for k,z in c['scenes'].items():w.writerow([name,c['year'],c['role'],c.get('asset','BTC/ETH'),c['is_new'],c.get('volume_lookback_days'),c.get('minimum_volume_ratio'),k,*[z[x]for x in ('net_return_pct','max_drawdown_pct','daily_mark_drawdown_pct','sharpe_365','calmar')],c['positive_folds_1x'],z['round_trips'],z['cost_pct_initial'],c['status']])
 print(json.dumps(report['summary']),flush=True)
if __name__=='__main__':main()
