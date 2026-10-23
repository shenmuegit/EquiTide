"""New same-funded portfolios from hash-verified archived component NAVs; no old signal or fill rerun."""
import argparse,copy,csv,gzip,hashlib,importlib.util,json,math,statistics,subprocess,sys
from datetime import datetime,timezone,timedelta
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
core=module(ROOT/'research/experiments/20261001T133655Z/evaluate.py','combo_source_metrics')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
ns=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*10**9)
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def readgz(p):return json.loads(gzip.decompress(p.read_bytes()))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True)
 out={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(out),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'],out;return out
CAPS,SPANS=[.4,.5,.6],[25,30,35]
def selected(records):
 out={}
 for fp,rec in records.items():
  s=rec['spec'];p=s.get('parameters',{});year=p.get('start_utc','')[:4]
  btc=s['family']=='daily-sma-volatility-ceiling' and s.get('universe')==['BTC/USDT'] and p.get('initial_capital_usdt')==1500 and p.get('lookback_days')==65 and p.get('entry_band_fraction')==.0125 and p.get('exit_band_fraction')==.005 and p.get('annual_volatility_ceiling') in CAPS
  eth=s['family']=='daily-channel-ema-confirmation' and s.get('universe')==['ETH/USDT'] and p.get('initial_capital_usdt')==500 and p.get('entry_lookback_days')==15 and p.get('exit_lookback_days')==30 and p.get('EMA_span_days') in SPANS and p.get('EMA_symmetric_band')==.0125
  if year not in ['2025','2026'] or not(btc or eth):continue
  assert rec['result_available'] and rec['status'] in ['passed','rejected'];path=ROOT/rec['report'];assert sha(path)==rec['report_sha256'];report=json.loads(path.read_text());cfg=next(c for c in report['configs'].values() if c.get('fingerprint')==fp);assert sha(ROOT/cfg['archive'])==cfg['archive_sha256'];arc=readgz(ROOT/cfg['archive']);assert reg.fingerprint(arc['spec'])==reg.fingerprint(s)==fp
  asset='BTC' if btc else 'ETH';axis=p['annual_volatility_ceiling'] if btc else p['EMA_span_days'];key=(year,asset,axis);assert key not in out
  out[key]={'fingerprint':fp,'name':cfg['name'],'spec':cfg.get('spec',cfg.get('spec_path')),'spec_sha256':sha(ROOT/cfg.get('spec',cfg.get('spec_path'))),'report':rec['report'],'report_sha256':sha(path),'archive':cfg['archive'],'archive_sha256':cfg['archive_sha256'],'asset':asset,'year':year,'axis':axis,'capital_usdt':p['initial_capital_usdt'],'original_status':rec['status'],'is_new_component':False}
 assert len(out)==12;return out

def freeze():
 assert not (R/'plan.json').exists();records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');refs=selected(records);first=[json.loads(x)['fingerprint'] for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()[:16]];initial={}
 for e in events:
  if e['fingerprint'] in first:initial.setdefault(e['fingerprint'],{}).update(e)
 assert len(initial)==16 and all(x.get('result_available') for x in initial.values())
 old=ROOT/'research/experiments/20261009T070950Z/spec.json';base=json.loads(old.read_text());monitor=module(ROOT/'research/monitor/snapshot.py','combo_monitor_context');canonical={reg.fingerprint(x['spec']) for x in records.values() if not monitor.is_observation(x['spec'])};previous=ROOT/'research/experiments/20261023T023857Z';protected=[ROOT/'research/paper10/plan.json',ROOT/'research/paper10/state.json',previous/'forward_state.json',previous/'forward_report.json']
 put(R/'context.json',{'registry_events':len(events),'registry_ids':len(records),'canonical_research_definitions_excluding_observations':len(canonical),'main_registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'initial_16_missing_actual_results':0,'prior_conclusions_read':[{'path':rel(p),'sha256':sha(p),'opening':p.read_text()[:220]} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))],'account_hashes_before':{rel(p):sha(p) for p in protected}})
 plan={'round':R.name,'frozen_at_utc':now(),'trigger_utc':'2026-10-23T04:38:54.474Z','direction':'Combine BTC volatility-guarded SMA65 with ETH close-channel/EMA confirmation using existing exact-funded component outcomes.','hypothesis':'BTC volatility exits and ETH channel/EMA confirmation can have complementary timing across fixed historical folds. Test the complete cap/span grid without retuning either leaf or scaling previously incurred costs.','grid':{'BTC_annual_volatility_ceiling':CAPS,'ETH_EMA_span_days':SPANS,'periods':['2025','2026'],'new_parent_configs':18,'new_component_configs':0,'cost_multipliers':[1,2,3]},'periods':base['periods'],'walk_forward':base['walk_forward'],'execution':base['execution'],'costs':base['costs'],'gates':{**base['gates'],'no_exchange_or_capacity_rejections':True},'allocation':'Raw initialBTC/ETH75/25 means actual archived1500/500USDT funds,total2000. Sum absolute already-costed component NAVs once at matched timestamps. Never normalize or weight the already-funded NAVs a second time. No transfers,rebalance,extra turnover,leverage,borrow or cash yield.','fixed_rules':{'BTC':records[refs['2026','BTC',.5]['fingerprint']]['spec'],'ETH':records[refs['2026','ETH',30]['fingerprint']]['spec']},'component_refs':list(refs.values()),'source_plan':{'path':rel(old),'sha256':sha(old)},'sensitivity':'Per period full3x3 cap×EMA-span. Local adjacent-index rectangle includes center;>=60%positive3x. Report all variants/folds/continuous minute risk and descriptive adjacent Sharpe cliffs.','qualification':'Eight original per-period gates plus zero source order rejections. A paired candidate requires both reused periods to pass;single-period passed is historical only,not independent final test or forward qualification.','history_note':'Both2025/2026periods extensively reused development history;no untouched holdout,no DSR/PBO claim. Parameter novelty does not imply a new economic NAV path.','recovery_policy':'Old .npy cache missing. Recover archived cash/units segments against same-SHA real minute prices in RAM,require original NAV SHA equality for all36source scenes. No original signal,trade,fee recomputation or result-status overwrite.','sources':[{'url':'https://github.com/binance/binance-public-data','accessed_utc':'2026-10-23','scope':'Primary public archive provenance;four existing normalized files and original source reports rehashed,not a fresh full archive download.'},{'url':'https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html','accessed_utc':'2026-10-23','scope':'Primary EMA adjust=False recurrence reference only;existing leaf rules and archived outcomes unchanged.'},{'url':'https://developers.binance.com/en/docs/products/spot/filters','accessed_utc':'2026-10-23','scope':'Official rules;frozenOct1metadata and historical5minuteVWAP acceptance remain proxies,not current/historical real exchange proof.'}],'limitations':['No historical L2,TCA,queues,latency or actual IOC fill proof;source cost/metadata assumptions unchanged.','No new component backtests;parent NAV exact sum on existing same-funded timestamps,source vector sampling includes daily postdecision opens and closed minutes.','Real paper10 and original ongoingSMA accounts stay separate and unchanged.']}
 plan['walk_forward']['fit']='Fixed causal leaf rules,no fitting or future labels;180daycontext/3daygap,purgeNA,six30dayfolds each period,continuous source positions. No source rule or state reset at fold boundaries.'
 put(R/'plan.json',plan);(R/'specs').mkdir();batch=[];pairs={tuple(sorted(c['fingerprint'] for c in x['spec'].get('components',[]))) for x in records.values() if x['spec']['kind']=='combination'}
 for year in ['2025','2026']:
  for cap in CAPS:
   for span in SPANS:
    rr=[refs[year,'BTC',cap],refs[year,'ETH',span]];assert tuple(sorted(x['fingerprint'] for x in rr)) not in pairs
    name=f'guard_ema_combo_{year}_V{cap}_E{span}';period=plan['periods'][year]
    spec={'kind':'combination','family':'volatility-guarded-sma-ema-channel-initial-capital','name':name,'logic':{'allocation':plan['allocation'],'execution':'Reuse source1500BTC/500ETH absolute costed NAVs on the identical259382point180dayaxis;sum at each point,derive portfolio metrics from total NAV,never average component metrics. No extra rebalance/trades.'},'parameters':{'initial_capital_usdt':2000,'raw_initial_weights':{'BTC':.75,'ETH':.25},'component_capitals_usdt':[1500,500],'start_utc':period['oos_start_utc'],'end_utc':period['terminal_exit_utc'],'BTC_SMA_days':65,'BTC_entry_band':.0125,'BTC_exit_band':.005,'BTC_volatility_lookback_days':20,'BTC_annual_volatility_ceiling':cap,'ETH_entry_lookback_days':15,'ETH_exit_lookback_days':30,'ETH_EMA_span_days':span,'ETH_EMA_symmetric_band':.0125,'cost_multipliers':[1,2,3],'costs':plan['costs'],'metadata_sha256':plan['execution']['metadata_sha256'],'walk_forward_folds':6,'walk_forward_test_days':30,'warmup_days':180,'embargo_days':3},'components':[{'fingerprint':ref['fingerprint'],'weight':w} for ref,w in zip(rr,[.75,.25])],'validation_plan':rel(R/'plan.json'),'sources':plan['sources']}
    path=R/'specs'/(name+'.json');put(path,spec);batch.append({'name':name,'year':year,'BTC_annual_volatility_ceiling':cap,'ETH_EMA_span_days':span,'role':'combination','is_new':True,'spec':rel(path),'fingerprint':reg.fingerprint(spec),'component_refs':rr})
 assert len(batch)==len({x['fingerprint'] for x in batch})==18;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/guard_ema_combo_2026_V0.5_E30.json').read_text()));done=[]
 for row in batch:done.append(call('reserve',row));put(R/'reserve.json',done)
 print('FROZEN_AND_RESERVED',len(done),sha(R/'plan.json'),flush=True)

def sources(plan):
 frames={};refs={};arcs={};vectors={};proof=[];folds={}
 for year,p in plan['periods'].items():
  assert sha(ROOT/p['report'])==p['sha256'];folds[year]=json.loads((ROOT/p['report']).read_text())['folds']
  for asset,md in p['normalized_data'].items():
   path=ROOT/md['path'];assert sha(path)==md['sha256'];f=pl.read_parquet(path,columns=['open_ts','available_ts','open','close','is_closed']);assert f.height==525600 and f['is_closed'].all() and (f['open_ts'].diff().drop_nulls()==core.MIN).all() and (f['available_ts']-f['open_ts']==core.MIN).all();assert int(f['open_ts'][183*1440+1])==ns(p['oos_start_utc']) and int(f['open_ts'][363*1440+1])==ns(p['terminal_exit_utc']);frames[year,asset]=f
  assert frames[year,'BTC']['open_ts'].equals(frames[year,'ETH']['open_ts'])
 for ref in plan['component_refs']:
  fp=ref['fingerprint'];assert sha(ROOT/ref['report'])==ref['report_sha256'] and sha(ROOT/ref['archive'])==ref['archive_sha256'] and sha(ROOT/ref['spec'])==ref['spec_sha256'];arc=readgz(ROOT/ref['archive']);assert arc['fingerprint']==fp and reg.fingerprint(arc['spec'])==fp and arc['spec']['parameters']['initial_capital_usdt']==ref['capital_usdt'];assert arc['spec']['parameters']['start_utc']==plan['periods'][ref['year']]['oos_start_utc'] and arc['spec']['parameters']['end_utc']==plan['periods'][ref['year']]['terminal_exit_utc'];refs[fp]=ref;arcs[fp]=arc
  f=frames[ref['year'],ref['asset']];cl=np.asarray(f['close'].cast(pl.Float64))
  for k,z in arc['scenes'].items():
   v=np.empty(core.POINTS);v[0]=ref['capital_usdt'];states={d:st for st in z['position_segments'] for d in range(st['day_offset'],st['end_day_exclusive'])};assert sorted(states)==list(range(180))
   for d in range(180):
    i=183+d;st=states[d];cash,qty=D(st['cash']),D(st['units']);assert cash>=0 and qty>=0;v[d*core.SPAN+1]=float(cash+qty*f['open'][i*1440+1]);v[d*core.SPAN+2:(d+1)*core.SPAN+1]=float(cash)+float(qty)*cl[i*1440+1:(i+1)*1440+1]
   v[-1]=float(D(z['terminal_cash'])+D(z['terminal_units'])*f['open'][363*1440+1]);assert D(z['terminal_units'])==0 and core.navhash(v)==z['summary']['NAV_sha256_f64le'];vectors[fp,k]=v;proof.append({'fingerprint':fp,'cost_multiplier':k,'NAV_sha256_f64le':core.navhash(v),'NAV_points':len(v)})
 assert len(refs)==12 and len(proof)==36;return frames,refs,arcs,vectors,folds,proof

def summarize_pair(row,plan,arcs,vectors,folds):
 fps=[x['fingerprint'] for x in row['component_refs']];out={};full={}
 for k in ['1','2','3']:
  parts=[arcs[f]['scenes'][k] for f in fps];v=vectors[fps[0],k]+vectors[fps[1],k];assert v[0]==2000
  trades=[{**t,'source_component_fingerprint':fp,'asset':ref['asset']} for fp,ref,p in zip(fps,row['component_refs'],parts) for t in p['trades']];units=sum(D(p['terminal_units']) for p in parts);z=core.summarize(v,trades,2000,folds[row['year']],units)
  start=datetime.fromisoformat(plan['periods'][row['year']]['oos_start_utc'].replace('Z','+00:00'))
  for i,f in enumerate(z['folds']):f.update(start_utc=(start+timedelta(days=30*i)).isoformat().replace('+00:00','Z'),end_exclusive_utc=(start+timedelta(days=30*(i+1))).isoformat().replace('+00:00','Z'))
  z['first_five_fold_return_pct']=100*(math.prod(1+f['net_return_pct']/100 for f in z['folds'][:5])-1);z['last_fold_return_pct']=z['folds'][-1]['net_return_pct'];out[k]=z;full[k]={'summary':z,'trades':trades,'terminal_units':str(units)}
 return out,full

def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[b['fingerprint']]['status']=='reserved' for b in batch);started=now();frames,refs,arcs,vectors,folds,proof=sources(plan);configs={};(R/'results').mkdir()
 for row in batch:
  scenes,full=summarize_pair(row,plan,arcs,vectors,folds);path=R/'results'/(row['name']+'.json.gz');core.gzwrite(path,{'spec':json.loads((ROOT/row['spec']).read_text()),'fingerprint':row['fingerprint'],'component_refs':row['component_refs'],'scenes':full});configs[row['name']]={**row,'spec_path':row['spec'],'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 for x in configs.values():
  i=CAPS.index(x['BTC_annual_volatility_ceiling']);j=SPANS.index(x['ETH_EMA_span_days']);neighbors=[c for c in configs.values() if c['year']==x['year'] and abs(CAPS.index(c['BTC_annual_volatility_ceiling'])-i)<=1 and abs(SPANS.index(c['ETH_EMA_span_days'])-j)<=1];frac=sum(c['scenes']['3']['net_return_pct']>0 for c in neighbors)/len(neighbors);x['sensitivity']={'neighbor_names':[c['name'] for c in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac};s=x['scenes'];ratio=s['1']['gross_reference_PnL_to_execution_cost'];x['criteria']={'positive_all_costs':all(z['net_return_pct']>0 for z in s.values()),'four_positive_1x_folds':x['positive_folds_1x']>=4,'minute_DD3_lte25pct':s['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'two_round_trips1':s['1']['round_trips']>=2,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(z['cash_or_units_violations']==0 for z in s.values()),'no_exchange_or_capacity_rejections':all(z['rejected_orders']==0 for z in s.values()),'terminal_flat':all(D(z['terminal_units'])==0 for z in s.values())};x['status']='passed' if all(x['criteria'].values()) else 'rejected';x['failed_criteria']=[k for k,v in x['criteria'].items() if not v]
 pairs=[]
 for x in configs.values():
  other=next(c for c in configs.values() if c['year']!=x['year'] and c['BTC_annual_volatility_ceiling']==x['BTC_annual_volatility_ceiling'] and c['ETH_EMA_span_days']==x['ETH_EMA_span_days']);x['other_period_config']=other['name'];x['both_periods_meet_full_gates']=x['status']==other['status']=='passed'
  if x['year']=='2025' and x['both_periods_meet_full_gates']:pairs.append([x['name'],other['name']])
 report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'component_sources':refs,'curve_formula':{'points':core.POINTS,'span_per_day':core.SPAN,'definition':'Initial2000;each day both component postdecision references at00:01 then1440closed minute marks through next00:01;final after costed terminal liquidation. Absolute same-funded NAV sum,not weighted twice.'},'configs':configs,'summary':{'new_configs':18,'candidate_configs':18,'new_component_configs':0,'source_components_read_only':12,'source_cost_scenes_hash_verified':36,'cost_scenarios':54,'new_minute_NAV_points':54*core.POINTS,'passed':[c['name'] for c in configs.values() if c['status']=='passed'],'rejected':[c['name'] for c in configs.values() if c['status']=='rejected'],'positive_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in configs.values()) for k in ['1','2','3']},'new_both_periods_passed_combination_pairs':pairs},'recovery':{'new_component_backtests':0,'source_scenes_verified':proof,'RAM_only_no_old_cache_or_result_files_written':True},'limitations':plan['limitations']}
 put(R/'report.json',report);put(R/'cache_recovery.json',report['recovery']);print('SUMMARY',json.dumps(report['summary']),flush=True)

def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
