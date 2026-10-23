"""Continuous360-day counter-test of the prior guarded-BTC/channel-EMA family."""
import argparse,copy,gzip,hashlib,importlib.util,json,math,subprocess,sys
from datetime import datetime,timezone,timedelta
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry as reg
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
def module(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
core=module(ROOT/'research/experiments/20261001T133655Z/evaluate.py','annual_cost_metrics');btc_signal=module(ROOT/'research/experiments/20261002T134733Z/signals.py','annual_BTC_signal');eth_signal=module(ROOT/'research/experiments/20261010T114325Z/signals.py','annual_ETH_signal')
START,END,DAYS,SPAN=368,728,360,1441;POINTS=DAYS*SPAN+2;DAY_NS=86400000000000;MIN_NS=60000000000
CAPS,EMAS=[.4,.5,.6],[25,30,35]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rel=lambda p:str(p.relative_to(ROOT))
now=lambda:datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
ns=lambda s:int(datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()*10**9)
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def readgz(p):return json.loads(gzip.decompress(p.read_bytes()))
def call(command,row,*args):
 p=subprocess.run([sys.executable,'research/automation/registry.py',command,row['spec'],*args],cwd=ROOT,capture_output=True,text=True);out={'name':row['name'],'fingerprint':row['fingerprint'],'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};print(json.dumps(out),flush=True);assert p.returncode==0 and p.stdout.strip()==row['fingerprint'];return out

def freeze():
 assert not (R/'plan.json').exists();previous=ROOT/'research/experiments/20261023T043854Z';prior=json.loads((previous/'plan.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');events=reg.read_events(ROOT/'research/automation/registry.jsonl');first=[json.loads(x)['fingerprint'] for x in (ROOT/'research/automation/registry.jsonl').read_text().splitlines()[:16]];initial={}
 for x in events:
  if x['fingerprint'] in first:initial.setdefault(x['fingerprint'],{}).update(x)
 assert len(initial)==16 and all(x.get('result_available') for x in initial.values())
 monitor=module(ROOT/'research/monitor/snapshot.py','annual_monitor_context');canonical={reg.fingerprint(x['spec']) for x in records.values() if not monitor.is_observation(x['spec'])};protected=[ROOT/'research/paper10/plan.json',ROOT/'research/paper10/state.json',previous/'forward_state.json',previous/'forward_report.json']
 put(R/'context.json',{'registry_events':len(events),'registry_ids':len(records),'canonical_research_definitions_excluding_observations':len(canonical),'main_registry_sha256_before_reserve':sha(ROOT/'research/automation/registry.jsonl'),'initial_16_missing_actual_results':0,'prior_conclusions_read':[{'path':rel(p),'sha256':sha(p),'opening':p.read_text()[:220]} for p in sorted((ROOT/'research/experiments').glob('*/result.md'))],'account_hashes_before':{rel(p):sha(p) for p in protected}})
 data=json.loads((ROOT/'research/experiments/20261023T023857Z/plan.json').read_text())['data'];time={'input_start_utc':'2024-09-16T00:00:00Z','input_end_exclusive_utc':'2026-09-16T00:00:00Z','oos_start_utc':'2025-09-19T00:01:00Z','oos_end_exclusive_utc':'2026-09-14T00:01:00Z','oos_days':360,'warmup_days':365,'initial_gap_days':3,'folds':12,'fold_days':30,'state':'One cold cash start per configuration at OOS start,no imported spring-summer positions,no interfold resets;carry actual cash,units and desired through the missing winter period.'}
 plan={'round':R.name,'frozen_at_utc':now(),'trigger_utc':'2026-10-23T06:38:24.789Z','direction':'Continuous360-day counter-test of guardedBTC+channelEMAETH including the previously omitted winter.','hypothesis':'Determine whether the prior positive paired spring-summer family survives the intervening decline with one continuous account. Negative results must remain;do not infer annual profit by multiplying old segment returns.','grid':{'BTC_annual_volatility_ceiling':CAPS,'ETH_EMA_span_days':EMAS,'new_components':6,'new_combinations':9,'new_benchmarks':3,'total_financial_configs':18,'cost_multipliers':[1,2,3]},'time_boundaries':time,'data':data,'execution':prior['execution'],'costs':prior['costs'],'fixed_leaf_rules':prior['fixed_rules'],'allocation':'Parent raw initialBTC/ETH75/25 means actual1500/500USDT of2000. Independent same-sized leaf NAVs summed once;never weight already-funded curves again,normalize,transfer,rebalance,borrow,short or add cash yield.','precision':'Native Decimal day CLOSE/quote-volume sums and OPEN execution references. BTC SMA/log-volatility Decimal28;ETH original recursive PythonFloatEMA from datasetday0. CLOSED-minute NAV keeps original PolarsFloat64 price encoding;postdecision OPEN stays nativeDecimal until finalfloat conversion.','gates':{'all_cost_returns_positive':True,'positive_1x_folds_min':8,'max_3x_minute_drawdown_pct':25,'local_3x_positive_fraction_min':.6,'round_trips_1x_min':4,'gross_reference_pnl_to_cost_min':2.5,'negative_cash_or_units':0,'order_rejections':0,'terminal_flat':True},'sensitivity':'Parent cap×EMAspan3x3 inclusive adjacent-index neighborhood;leaves same-asset adjacent-axis subset,benchmark reference-only. Full returns/DD/Sharpe/Calmar and all folds reported;no OOS selection.','prior_read_only':{'report':rel(previous/'report.json'),'sha256':sha(previous/'report.json'),'status':'Prior12single-period passed/6rejected,4paired parameters passed;both windows onlyMarch-September. Read-only context,not annual or independent holdout evidence.'},'validation':'365daywarmup+3dayinitialgap;12continuous30dayfolds. Fixed causal rules,no fitting/future labels,purgeNA. Same broadly reused development history,not untouched final test;no DSR/PBO claim.','benchmark_scope':'New exact-funded BTC1500/ETH500 buy-hold leaves and75/25portfolio on same360dayaxis,all1/2/3costs. No preexisting same-funded full-window hold found. Benchmarks are reference-only,not alpha qualification. Cash0yield analytic0.','sources':prior['sources'],'limits':['FrozenOct1filters,historical5minuteVWAP acceptance andIOC liquidity remain proxies;no historical L2,TCA/queue/latency proof.','360continuousdays is a near-year counter-test,not365days,independent holdout or stableliveprofit proof.','Original ongoingSMA andpaper10accounts are read-only and never replaced.']}
 put(R/'plan.json',plan);(R/'specs').mkdir();batch=[];fps={}
 def save(spec,row):
  path=R/'specs'/(spec['name']+'.json');put(path,spec);x={**row,'name':spec['name'],'spec':rel(path),'fingerprint':reg.fingerprint(spec)};batch.append(x);return x
 for asset,axes,capital in [('BTC',CAPS,1500),('ETH',EMAS,500)]:
  for axis in axes:
   ref=next(x for x in prior['component_refs'] if x['year']=='2026' and x['asset']==asset and x['axis']==axis);spec=copy.deepcopy(readgz(ROOT/ref['archive'])['spec']);spec.update(name=f'annual_{asset}_{axis}_c{capital}',validation_plan=rel(R/'plan.json'),sources=plan['sources']);p=spec['parameters'];p.update(start_utc=time['oos_start_utc'],end_utc=time['oos_end_exclusive_utc'],warmup_days=365,embargo_days=3,walk_forward_folds=12,walk_forward_test_days=30,walk_forward_step_days=30,input_history_start_utc=time['input_start_utc'],signal_initialization='Desired cash at full-history index368,OOS2025-09-19;no warmup fills or fold resets. BTC thresholds fixed;ETH EMA recursively seeded from first2024-09-16close.')
   if 'state' in spec['logic']:spec['logic']['state']='One cash/desired-cash start at declaredOOS;365daily context;carry all cash/units/desired across12folds,no imports from old seasonal portfolios.'
   fps[asset,axis]=save(spec,{'role':'component','asset':asset,'axis':axis,'capital_usdt':capital})['fingerprint']
 bench={}
 for asset,capital in [('BTC',1500),('ETH',500)]:
  spec={'kind':'strategy','family':'spot-hold-comparator','name':f'annual_hold_{asset}_c{capital}','market':'spot','timeframe':'1d','universe':[asset+'/USDT'],'logic':{'entry':'Constant desired-long from declaredOOS start;buy maximum affordable lot at first next00:01OPEN;retain residue,no add-ons. If rejected,retry only on later daily decision.','exit':'Fixed costed terminal liquidation at declaredOOS end. No signal or future-price selection.','sizing':'Independent actual declared capital,unlevered spot,no transfer/rebalance/borrowing/cashyield.'},'parameters':{'initial_capital_usdt':capital,'start_utc':time['oos_start_utc'],'end_utc':time['oos_end_exclusive_utc'],'execution':plan['execution'],'costs':plan['costs'],'cost_multipliers':[1,2,3],'warmup_days':365,'embargo_days':3,'walk_forward_folds':12,'walk_forward_test_days':30},'validation_plan':rel(R/'plan.json')};bench[asset]=save(spec,{'role':'benchmark_component','asset':asset,'axis':None,'capital_usdt':capital})['fingerprint']
 def parent(name,bfp,efp,role,cap=None,span=None):
  spec={'kind':'combination','family':'volatility-guarded-sma-ema-channel-initial-capital' if role=='combination' else 'buy-hold-initial-capital-reference','name':name,'logic':{'allocation':plan['allocation'],'execution':'Sum aligned continuous360day exact-funded componentNAVs;derive totalportfolio risk/returns from full summed vector,never average component metrics.'},'parameters':{'initial_capital_usdt':2000,'raw_initial_weights':{'BTC':.75,'ETH':.25},'component_capitals_usdt':[1500,500],'start_utc':time['oos_start_utc'],'end_utc':time['oos_end_exclusive_utc'],'BTC_annual_volatility_ceiling':cap,'ETH_EMA_span_days':span,'costs':plan['costs'],'metadata_sha256':plan['execution']['metadata_sha256'],'cost_multipliers':[1,2,3],'warmup_days':365,'embargo_days':3,'walk_forward_folds':12,'walk_forward_test_days':30},'components':[{'fingerprint':bfp,'weight':.75},{'fingerprint':efp,'weight':.25}],'validation_plan':rel(R/'plan.json')};save(spec,{'role':role,'BTC_annual_volatility_ceiling':cap,'ETH_EMA_span_days':span,'capital_usdt':2000})
 for cap in CAPS:
  for span in EMAS:parent(f'annual_combo_V{cap}_E{span}',fps['BTC',cap],fps['ETH',span],'combination',cap,span)
 parent('annual_hold_75_25',bench['BTC'],bench['ETH'],'benchmark');assert len(batch)==len({x['fingerprint'] for x in batch})==18;put(R/'batch.json',batch);put(R/'spec.json',json.loads((R/'specs/annual_combo_V0.5_E30.json').read_text()));done=[]
 for x in batch:done.append(call('reserve',x));put(R/'reserve.json',done)
 print('FROZEN_AND_RESERVED',len(done),sha(R/'plan.json'),flush=True)

def markets(plan):
 out={}
 for asset,files in plan['data']['assets'].items():
  fs=[]
  for md in files:
   p=ROOT/md['path'];assert sha(p)==md['sha256'] and p.stat().st_size==md['bytes'];f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed']);assert f.height==525600 and f['is_closed'].all() and (f['available_ts']-f['open_ts']==MIN_NS).all();fs.append(f)
  f=pl.concat(fs,how='vertical_relaxed').sort('open_ts');assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all();assert f.height==1051200 and (f['open_ts'].diff().drop_nulls()==MIN_NS).all();daily=f.with_columns((pl.col('open_ts')//DAY_NS).alias('day')).group_by('day',maintain_order=True).agg(pl.col('close').last().alias('close'),pl.col('quote_volume').sum().alias('quote_volume'),pl.len().alias('bars')).sort('day');assert daily.height==730 and (daily['bars']==1440).all();rows=[]
  for i,z in enumerate(daily.to_dicts()):rows.append({'date':datetime.fromtimestamp(z['day']*86400,timezone.utc).date().isoformat(),'close':z['close'],'quote_volume':z['quote_volume'],'close_available_ts':(z['day']+1)*DAY_NS,'trade_ts':int(f['open_ts'][i*1440+1]),'trade_open':f['open'][i*1440+1]})
  assert rows[START]['trade_ts']==ns(plan['time_boundaries']['oos_start_utc']) and rows[END]['trade_ts']==ns(plan['time_boundaries']['oos_end_exclusive_utc']);out[asset]={'frame':f,'rows':rows,'closes':np.asarray(f['close'].cast(pl.Float64))}
 return out

def summary(v,trades,capital,units):
 m,daily=core.metric(v,DAYS,True);m['folds']=[];start=datetime(2025,9,19,0,1,tzinfo=timezone.utc)
 for j in range(12):
  a=j*30*SPAN;b=(j+1)*30*SPAN+1+(j==11);s,_=core.metric(v[a:b],30,j==11);m['folds'].append({'fold':j+1,'start_utc':(start+timedelta(days=30*j)).isoformat().replace('+00:00','Z'),'end_exclusive_utc':(start+timedelta(days=30*(j+1))).isoformat().replace('+00:00','Z'),**s})
 assert abs(math.prod(1+f['net_return_pct']/100 for f in m['folds'])-v[-1]/v[0])<1e-12
 filled=[t for t in trades if t['status']=='filled'];parts={k:float(sum(D(t['cost_parts'][k]) for t in filled)) for k in ['fee','half_spread','slippage','impact','tick_rounding']};cost=sum(parts.values());gross=sum(float(D(t['quantity'])*D(t['reference']))*(1 if t['side']!='buy' else -1) for t in filled);assert abs(gross-cost-(v[-1]-v[0]))<1e-8
 m.update(initial_capital_usdt=capital,final_NAV_usdt=float(v[-1]),cost_usdt=cost,cost_pct_initial=cost/capital*100,cost_parts_usdt=parts,gross_reference_PnL_usdt=gross,gross_reference_PnL_to_execution_cost=gross/cost if cost else None,executions=len(filled),round_trips=sum(t['side']=='sell' for t in filled),rejected_orders=len(trades)-len(filled),cash_or_units_violations=sum(D(t['cash_after'])<0 or D(t['units_after'])<0 for t in trades),terminal_units=str(units),daily_equity_usdt=daily,NAV_points=len(v),NAV_sha256_f64le=core.navhash(v));return m

def component(spec,market,mult,hold=False):
 p=spec['parameters'];asset=spec['universe'][0].split('/')[0];rows=market['rows'];f=market['frame'];closes=market['closes'];capital=p['initial_capital_usdt'];values=[r['close'] for r in rows]
 if hold:decisions=[{'decision_index':i,'long':True,'action':'constant_long'} for i in range(START,END)]
 elif asset=='BTC':decisions=btc_signal.volatility_guarded_asymmetric_sma(values,65,.0125,.005,20,p['annual_volatility_ceiling'],start=START,end=END)
 else:decisions=eth_signal.filtered_channel(values,15,30,p['EMA_span_days'],.0125,start=START,end=END)
 cash,qty=D(capital),D(0);v=np.empty(POINTS);v[0]=capital;trades=[];states=[]
 def execute(i,buy,terminal):
  nonlocal cash,qty
  mi=i*1440+1;ref=f['open'][mi];h=f.slice(mi-5,5);assert int(h['available_ts'].max())<=rows[i]['trade_ts'] and h['base_volume'].sum()>0;proxy=h['quote_volume'].sum()/h['base_volume'].sum();adv,sigma=core.engine.lagged_cost_inputs(rows,i);cb,qb=cash,qty;cash,qty,t=core.fill(cash,qty,bool(buy),ref,D(str(adv)),D(str(sigma)),mult,p['execution']['filters'][asset+'USDT'],proxy);t.update(asset=asset,decision_index=i,day_offset=i-START,trade_ts_ns=rows[i]['trade_ts'],terminal=terminal,cash_before=str(cb),units_before=str(qb));trades.append(t)
 for d,i in enumerate(range(START,END)):
  assert rows[i-1]['close_available_ts']<rows[i]['trade_ts'];want=decisions[d]['long']
  if (want and not qty) or (not want and qty):execute(i,want,False)
  states.append({'day_offset':d,'cash':str(cash),'units':str(qty)});v[d*SPAN+1]=float(cash+qty*rows[i]['trade_open']);v[d*SPAN+2:(d+1)*SPAN+1]=float(cash)+float(qty)*closes[i*1440+1:(i+1)*1440+1]
 if qty:execute(END,False,True)
 v[-1]=float(cash+qty*rows[END]['trade_open']);assert qty==0 and np.isfinite(v).all() and (v>0).all();segments=[]
 for st in states:
  if not segments or (st['cash'],st['units'])!=(segments[-1]['cash'],segments[-1]['units']):segments.append({**st,'end_day_exclusive':st['day_offset']+1})
  else:segments[-1]['end_day_exclusive']+=1
 return v,{'decisions':decisions,'trades':trades,'position_segments':segments,'terminal_cash':str(cash),'terminal_units':str(qty),'summary':summary(v,trades,capital,qty)}

def evaluate():
 assert not (R/'report.json').exists();plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());records=reg.read_records(ROOT/'research/automation/registry.jsonl');assert all(records[x['fingerprint']]['status']=='reserved' for x in batch);started=now();market=markets(plan);arcs={};vectors={};configs={};(R/'results').mkdir()
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());scenes={};arc={'spec':spec,'fingerprint':row['fingerprint'],'scenes':{}}
  for k in ['1','2','3']:
   if spec['kind']=='strategy':v,z=component(spec,market[row['asset']],int(k),row['role']=='benchmark_component')
   else:
    fps=[x['fingerprint'] for x in spec['components']];parts=[arcs[fp]['scenes'][k] for fp in fps];v=vectors[fps[0],k]+vectors[fps[1],k];trades=[t for z0 in parts for t in z0['trades']];units=sum(D(z0['terminal_units']) for z0 in parts);z={'trades':trades,'terminal_units':str(units),'summary':summary(v,trades,2000,units)}
   arc['scenes'][k]=z;scenes[k]=z['summary']
   if spec['kind']=='strategy':vectors[row['fingerprint'],k]=v
  path=R/'results'/(row['name']+'.json.gz');core.gzwrite(path,arc);arcs[row['fingerprint']]=arc;configs[row['name']]={**row,'spec_path':row['spec'],'archive':rel(path),'archive_sha256':sha(path),'scenes':scenes,'positive_folds_1x':sum(f['net_return_pct']>0 for f in scenes['1']['folds'])};print(row['name'],scenes['1']['net_return_pct'],scenes['3']['net_return_pct'],flush=True)
 for c in configs.values():
  if c['role'].startswith('benchmark'):c.update(status='rejected',criteria={'reference_only_no_strategy_qualification':False},sensitivity={'reference_only':True});continue
  if c['role']=='component':axis=CAPS if c['asset']=='BTC' else EMAS;i=axis.index(c['axis']);neighbors=[x for x in configs.values() if x['role']=='component' and x['asset']==c['asset'] and abs(axis.index(x['axis'])-i)<=1]
  else:i=CAPS.index(c['BTC_annual_volatility_ceiling']);j=EMAS.index(c['ETH_EMA_span_days']);neighbors=[x for x in configs.values() if x['role']=='combination' and abs(CAPS.index(x['BTC_annual_volatility_ceiling'])-i)<=1 and abs(EMAS.index(x['ETH_EMA_span_days'])-j)<=1]
  frac=sum(x['scenes']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);c['sensitivity']={'neighbor_names':[x['name'] for x in neighbors],'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac};ss=c['scenes'];ratio=ss['1']['gross_reference_PnL_to_execution_cost'];c['criteria']={'positive_all_costs':all(s['net_return_pct']>0 for s in ss.values()),'eight_positive_1x_folds':c['positive_folds_1x']>=8,'minute_DD3_lte25pct':ss['3']['max_drawdown_pct']<=25,'neighbourhood_positive3_gte60pct':frac>=.6,'four_round_trips1':ss['1']['round_trips']>=4,'gross_to_cost1_gte2_5':ratio is not None and ratio>=2.5,'no_balance_violations':all(s['cash_or_units_violations']==0 for s in ss.values()),'no_order_rejections':all(s['rejected_orders']==0 for s in ss.values()),'terminal_flat':all(D(s['terminal_units'])==0 for s in ss.values())};c['status']='passed' if all(c['criteria'].values()) else 'rejected';c['failed_criteria']=[k for k,v in c['criteria'].items() if not v]
 parents=[c for c in configs.values() if c['role']=='combination'];candidates=[c for c in configs.values() if not c['role'].startswith('benchmark')];report={'round':R.name,'evaluation_started_utc':started,'frozen_plan_sha256':sha(R/'plan.json'),'time_boundaries':plan['time_boundaries'],'configs':configs,'input_data':plan['data'],'curve_formula':{'points':POINTS,'span_per_day':SPAN,'days':DAYS,'definition':'Initial capital;each day nativeDecimalpostdecisionOPEN mark then1440PolarsFloat64close marks;final costed liquidation. Sum actual1500/500funded leafvectors once for parents.'},'summary':{'actual_financial_configs':18,'candidate_configs':15,'new_component_configs':6,'new_parent_configs':9,'benchmark_configs':3,'cost_scenarios':54,'passed':[c['name'] for c in candidates if c['status']=='passed'],'rejected':[c['name'] for c in candidates if c['status']=='rejected'],'parent_passed':[c['name'] for c in parents if c['status']=='passed'],'parent_rejected':[c['name'] for c in parents if c['status']=='rejected'],'positive_parent_configs_by_cost':{k:sum(c['scenes'][k]['net_return_pct']>0 for c in parents) for k in ['1','2','3']}},'scope':plan['limits']};put(R/'report.json',report);print('SUMMARY',json.dumps(report['summary']),flush=True)

def finish():
 report=json.loads((R/'report.json').read_text());done=[]
 for row in json.loads((R/'batch.json').read_text()):done.append(call('finish',row,report['configs'][row['name']]['status'],rel(R/'report.json')));put(R/'finish.json',done)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('command',choices=['freeze','evaluate','finish']);globals()[p.parse_args().command]()
