#!/usr/bin/env python3
"""Run frozen daily EMA crossover variants on continuous archived Binance spot data."""
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));from kernel import fill
spc=importlib.util.spec_from_file_location('ema_cross_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py');engine=importlib.util.module_from_spec(spc);sys.modules[spc.name]=engine;spc.loader.exec_module(engine)
MIN_NS=60_000_000_000;DAY_NS=1440*MIN_NS;MIN_MS=60000;DAY_MS=86400000
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ms):return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def canonical(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def write_json(path,obj):path.write_text(json.dumps(canonical(obj),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def write_gzip_json(path,obj):
 with path.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as out:out.write(json.dumps(canonical(obj),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def load_asset(asset,plan):
 frames=[];files=[]
 for item in plan['data']['assets'][asset]:
  path=ROOT/item['path'];assert path.is_file() and path.stat().st_size==item['bytes'] and sha(path)==item['sha256']
  frame=pl.read_parquet(path,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert frame.height==525600 and frame['is_closed'].all() and frame['open_ts'].is_sorted()
  assert (frame['open_ts'].diff().drop_nulls()==MIN_NS).all() and (frame['available_ts']-frame['open_ts']==MIN_NS).all()
  assert (frame['open']>0).all() and (frame['close']>0).all() and (frame['base_volume']>=0).all() and (frame['quote_volume']>=0).all()
  files.append({**item,'bars':frame.height,'first_open_ns':int(frame['open_ts'][0]),'last_open_ns':int(frame['open_ts'][-1])});frames.append(frame)
 minute=pl.concat(frames,how='vertical_relaxed').sort('open_ts');assert minute.height==1051200 and (minute['open_ts'].diff().drop_nulls()==MIN_NS).all()
 daily=(minute.with_columns((pl.col('open_ts')//DAY_NS).alias('day_ns')).group_by('day_ns',maintain_order=True).agg(pl.col('close').last().cast(pl.Float64).alias('close'),pl.col('quote_volume').sum().cast(pl.Float64).alias('quote_volume'),pl.len().alias('minute_count')).sort('day_ns'))
 assert daily.height==730 and (daily['minute_count']==1440).all()
 day_ts=daily['day_ns'].to_numpy()*DAY_MS;close=daily['close'].to_numpy();qv=daily['quote_volume'].to_numpy()
 assert np.all(np.diff(day_ts)==DAY_MS) and np.isfinite(close).all() and np.isfinite(qv).all() and (close>0).all() and (qv>=0).all()
 rows=[{'date':stamp(int(t)).split('T')[0],'day_open_ms':int(t),'close':D(str(c)),'quote_volume':D(str(v))} for t,c,v in zip(day_ts,close,qv)]
 return {'asset':asset,'files':files,'minute_ts':minute['open_ts'].to_numpy()//1_000_000,'minute_open':minute['open'].cast(pl.Float64).to_numpy(),'minute_close':minute['close'].cast(pl.Float64).to_numpy(),'minute_base':minute['base_volume'].cast(pl.Float64).to_numpy(),'minute_quote':minute['quote_volume'].cast(pl.Float64).to_numpy(),'day_ts':day_ts,'daily_close':close,'daily_quote_volume':qv,'daily_rows':rows,'daily_close_sha256_f64le':hashlib.sha256(np.asarray(close,dtype='<f8').tobytes()).hexdigest()}
def ema(values,span):
 alpha=2.0/(span+1.0);result=np.empty(len(values),dtype=np.float64);result[0]=float(values[0])
 for i in range(1,len(values)):result[i]=alpha*float(values[i])+(1-alpha)*result[i-1]
 return result
def drawdown(values):
 a=np.asarray(values,dtype=np.float64);peak=np.maximum.accumulate(a);return float(np.max(np.where(peak>0,100*(1-a/peak),0),initial=0))
def evaluate_one(name,asset,p,mult,market,filters,plan):
 capital=D('2000');cash=capital;units=D(0);desired=False;fast=ema(market['daily_close'],p['fast_ema_span_days']);slow=ema(market['daily_close'],p['slow_ema_span_days'])
 parts={k:D(0) for k in ('fee','half_spread','slippage','impact','tick_rounding')};trades=[];decisions=[];daily_nav=[float(capital)];events=[];fills=rejects=round_trips=0
 start=int(datetime.fromisoformat(plan['data']['oos_start_utc'].replace('Z','+00:00')).timestamp()*1000);end=int(datetime.fromisoformat(plan['data']['oos_end_exclusive_utc'].replace('Z','+00:00')).timestamp()*1000);minute0=int(market['minute_ts'][0]);day0=int(market['day_ts'][0])
 assert end-start==360*DAY_MS and start%DAY_MS==MIN_MS and end%DAY_MS==MIN_MS
 mstart=(start-minute0)//MIN_MS;mend=(end-minute0)//MIN_MS;assert market['minute_ts'][mstart]==start and market['minute_ts'][mend]==end
 key=asset
 for step in range(360):
  exec_ms=start+step*DAY_MS;signal_ms=exec_ms-DAY_MS-MIN_MS;idx=(signal_ms-day0)//DAY_MS;assert market['day_ts'][idx]==signal_ms
  avail_ms=signal_ms+DAY_MS;assert avail_ms==exec_ms-MIN_MS
  old=desired;ef=float(fast[idx]);es=float(slow[idx]);condition='equal_hold'
  if ef>es:desired=True;condition='fast_gt_slow'
  elif ef<es:desired=False;condition='fast_lt_slow'
  action='entry' if desired and units==0 else 'exit' if (not desired and units>0) else 'hold'
  decisions.append({'configuration':name,'asset':asset,'cost_multiplier':mult,'signal_day_utc':stamp(signal_ms),'signal_available_at_utc':stamp(avail_ms),'simulated_decision_at_utc':stamp(exec_ms),'execution_delay_seconds':60,'close':float(market['daily_close'][idx]),'EMA_fast':ef,'EMA_slow':es,'fast_span_days':p['fast_ema_span_days'],'slow_span_days':p['slow_ema_span_days'],'prior_desired_long':old,'desired_long':desired,'crossover_state':condition,'action':action})
  if action in ('entry','exit'):
   mi=(exec_ms-minute0)//MIN_MS;ref=D(str(market['minute_open'][mi]));avgmins=int(filters[key]['PERCENT_PRICE_BY_SIDE']['avgPriceMins']);base=sum((D(str(x)) for x in market['minute_base'][mi-avgmins:mi]),D(0));quote=sum((D(str(x)) for x in market['minute_quote'][mi-avgmins:mi]),D(0));proxy=quote/base if base>0 else ref
   day_i=int((exec_ms-day0)//DAY_MS);adv,sigma=engine.lagged_cost_inputs(market['daily_rows'],day_i);cb,ub=cash,units
   cash2,units2,t=fill(cash,units,action=='entry',ref,D(str(adv)),D(str(sigma)),mult,filters[key],proxy)
   t.update({'configuration':name,'asset':asset,'cost_multiplier':mult,'trade_id':f'{name}:{mult}:{exec_ms}:{action}','reason':action,'signal_day_utc':stamp(signal_ms),'signal_available_utc':stamp(avail_ms),'execution_utc':stamp(int(market['minute_ts'][mi])),'signal_to_execution_seconds':60,'minute_index':int(mi),'terminal':False,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(cash2),'units_after':str(units2),'observed_signal':{'EMA_fast':ef,'EMA_slow':es,'daily_close':str(market['daily_close'][idx])}})
   trades.append(t);cash,units=cash2,units2
   if t['status']=='filled':
    fills+=1;events.append({'minute_index':int(mi),'reference':ref,'cash_after':cash,'units_after':units})
    for k,v in t['cost_parts'].items():parts[k]+=D(v)
    if action=='exit' and units==0:round_trips+=1
   else:rejects+=1
  eod=(mstart+step*1440+1439);assert eod<mend;daily_nav.append(float(cash)+float(units)*float(market['minute_close'][eod]))
 # At the frozen end boundary, liquidate any residual position; no new entry is allowed.
 terminal_ref=D(str(market['minute_open'][mend]));terminal_avail=end-MIN_MS
 if units>0:
  adv,sigma=engine.lagged_cost_inputs(market['daily_rows'],int((end-day0)//DAY_MS));cb,ub=cash,units
  bsum=sum((D(str(x)) for x in market['minute_base'][mend-5:mend]),D(0));qsum=sum((D(str(x)) for x in market['minute_quote'][mend-5:mend]),D(0));proxy=qsum/bsum if bsum>0 else terminal_ref
  c2,u2,t=fill(cash,units,False,terminal_ref,D(str(adv)),D(str(sigma)),mult,filters[key],proxy)
  t.update({'configuration':name,'asset':asset,'cost_multiplier':mult,'trade_id':f'{name}:{mult}:{end}:terminal','reason':'terminal_liquidation','signal_day_utc':stamp(terminal_avail-DAY_MS),'signal_available_utc':stamp(terminal_avail),'execution_utc':stamp(int(market['minute_ts'][mend])),'signal_to_execution_seconds':60,'minute_index':int(mend),'terminal':True,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(c2),'units_after':str(u2),'observed_signal':None})
  trades.append(t);cash,units=c2,u2
  if t['status']=='filled':
   fills+=1;round_trips+=1;events.append({'minute_index':int(mend),'reference':terminal_ref,'cash_after':cash,'units_after':units})
   for k,v in t['cost_parts'].items():parts[k]+=D(v)
  else:rejects+=1
 terminal_nav=cash+units*terminal_ref;daily_nav[-1]=float(terminal_nav)
 # Mark every closed OOS minute, with an immediate post-fill mark at each execution reference.
 nav=[float(capital)];cur_cash=capital;cur_units=D(0);cursor=mstart
 for e in sorted(events,key=lambda x:x['minute_index']):
  mi=e['minute_index']
  if mi<mstart or mi>=mend:continue
  if mi>cursor:nav.extend((float(cur_cash)+float(cur_units)*market['minute_close'][cursor:mi]).tolist())
  cur_cash,cur_units=e['cash_after'],e['units_after'];nav.append(float(cur_cash+cur_units*e['reference']));cursor=mi
 if cursor<mend:nav.extend((float(cur_cash)+float(cur_units)*market['minute_close'][cursor:mend]).tolist())
 nav.append(float(terminal_nav))
 cost=sum(parts.values(),D(0));gross=terminal_nav-capital+cost
 folds=[]
 for i in range(12):
  a,b=daily_nav[i*30],daily_nav[(i+1)*30];folds.append({'fold':i+1,'start_utc':stamp(start+i*30*DAY_MS),'end_exclusive_utc':stamp(start+(i+1)*30*DAY_MS),'start_nav_usdt':a,'end_nav_usdt':b,'net_return_pct':(b/a-1)*100})
 rets=np.asarray(daily_nav[1:],dtype=np.float64)/np.asarray(daily_nav[:-1],dtype=np.float64)-1;sd=float(np.std(rets,ddof=1));sharpe=float(np.mean(rets)/sd*math.sqrt(365)) if sd else None
 cagr=(float(terminal_nav)/float(capital))**(365/360)-1;dd_day=drawdown(daily_nav)
 return {'asset':asset,'configuration':name,'cost_multiplier':mult,'terminal_nav_usdt':str(terminal_nav),'net_pnl_usdt':str(terminal_nav-capital),'net_return_pct':float(100*(terminal_nav/capital-1)),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_flat':units==0,'cost_usdt':str(cost),'cost_parts_usdt':{k:str(v) for k,v in parts.items()},'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,'max_drawdown_1m_sampled_pct':drawdown(nav),'daily_sample_drawdown_pct':dd_day,'drawdown_scope':'OOS 1m bar-close NAV plus immediate post-fill references; excludes intraminute extrema.','daily_sharpe_annualized':sharpe,'cagr_pct':cagr*100,'calmar_daily_sampled':cagr/(dd_day/100) if dd_day else None,'fills':fills,'rejected_orders':rejects,'round_trips':round_trips,'positive_folds':sum(x['net_return_pct']>0 for x in folds),'folds':folds,'minute_nav_samples':len(nav),'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(nav,dtype='<f8').tobytes()).hexdigest(),'daily_nav':daily_nav,'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(daily_nav,dtype='<f8').tobytes()).hexdigest(),'trades':trades,'decisions':decisions}
def main():
 plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());ex=json.loads((R/'exchange_filters.json').read_text());filters=ex['filters']
 markets={a:load_asset(a,plan) for a in ('BTC','ETH')};configs={};all_trades=[];all_decisions=[];all_daily=[];run_dir=ROOT/'data/runs'/R.name;run_dir.mkdir(parents=True,exist_ok=True)
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert registry.fingerprint(spec)==row['fingerprint'];scenes={}
  for mult in (1,2,3):
   z=evaluate_one(row['name'],row['asset'],spec['parameters'],mult,markets[row['asset']],filters,plan);scenes[str(mult)]=z;all_trades.extend(z['trades']);all_decisions.extend(z['decisions']);write_gzip_json(run_dir/f"{row['name']}_cost{mult}.json.gz",z)
   for i,v in enumerate(z['daily_nav']):all_daily.append({'configuration':row['name'],'asset':row['asset'],'cost_multiplier':mult,'day_index':i,'nav_usdt':v})
   print(row['name'],mult,round(z['net_return_pct'],5),z['fills'],flush=True)
  configs[row['name']]={'asset':row['asset'],'fast_span_days':row['fast'],'slow_span_days':row['slow'],'fingerprint':row['fingerprint'],'spec_path':row['spec'],'initial_capital_usdt':2000,'raw_weight':1.0,'scenarios':scenes}
 fast=plan['grid']['fast_ema_spans_days'];slow=plan['grid']['slow_ema_spans_days']
 for cfg in configs.values():
  fi=fast.index(cfg['fast_span_days']);si=slow.index(cfg['slow_span_days']);neighbors=[]
  for other in configs.values():
   if other['asset']==cfg['asset'] and abs(fast.index(other['fast_span_days'])-fi)<=1 and abs(slow.index(other['slow_span_days'])-si)<=1:neighbors.append(other)
  frac=sum(x['scenarios']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);cfg['sensitivity']={'neighbor_count':len(neighbors),'neighbors':[x['spec_path'] for x in neighbors],'local_3x_neighbor_positive_fraction':frac}
  one,three=cfg['scenarios']['1'],cfg['scenarios']['3']
  gates={'all_cost_scenarios_positive':all(cfg['scenarios'][k]['net_return_pct']>0 for k in ('1','2','3')),'positive_1x_folds_at_least_8':one['positive_folds']>=8,'drawdown3_lte25':three['max_drawdown_1m_sampled_pct']<=25,'neighbor3_positive_fraction_gte60':frac>=.6,'round_trips1_gte4':one['round_trips']>=4,'gross_cost_ratio1_gte2_5':one['gross_reference_pnl_to_cost'] is not None and one['gross_reference_pnl_to_cost']>=2.5,'no_exchange_or_capacity_rejections':all(cfg['scenarios'][k]['rejected_orders']==0 for k in ('1','2','3')),'terminal_flat':all(cfg['scenarios'][k]['terminal_flat'] for k in ('1','2','3'))}
  cfg['gates']=gates;cfg['status']='passed' if all(gates.values()) else 'rejected'
 prior=json.loads((ROOT/'research/experiments/20261013T123949Z/report.json').read_text());bench={asset:prior['configs'][f'hold_360d_{asset.lower()}_relative_strength_study']['scenarios'] for asset in ('BTC','ETH')}
 # Detailed per-day decisions, fill ledgers and NAVs remain in auditable CSV artifacts.
 # Keep the compact headline report small and avoid serializing the same event rows 54 times.
 for cfg in configs.values():
  for scene in cfg['scenarios'].values():
   for key in ('trades','decisions','daily_nav'):scene.pop(key,None)
 ranked=sorted(configs,key=lambda name:configs[name]['scenarios']['1']['net_return_pct'],reverse=True)
 data={'assets':{a:{'source_files':markets[a]['files'],'minute_bars':len(markets[a]['minute_ts']),'daily_bars':len(markets[a]['day_ts']),'daily_close_sha256_f64le':markets[a]['daily_close_sha256_f64le']} for a in markets}}
 report={'round':R.name,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':sha(R/'plan.json'),'plan':plan,'data_manifest':data,'benchmark_read_only':{'source_report':'research/experiments/20261013T123949Z/report.json','assets':bench,'status':'same-window reference; no rerun'},'summary':{'candidate_configs':len(configs),'passed':sum(x['status']=='passed' for x in configs.values()),'rejected':sum(x['status']=='rejected' for x in configs.values()),'cost_scenes':len(configs)*3,'oos_days':360,'folds':12,'fold_days':30,'positive_configs_by_cost':{k:sum(x['scenarios'][k]['net_return_pct']>0 for x in configs.values()) for k in ('1','2','3')},'ranked_by_1x_net_return':ranked},'configs':configs,'artifacts':{'trades':'research/experiments/'+R.name+'/trades.csv.gz','decisions':'research/experiments/'+R.name+'/decisions.csv.gz','daily_equity':'research/experiments/'+R.name+'/daily_equity.csv.gz'}}
 write_json(R/'report.json',report)
 for filename,rows in (('trades.csv',all_trades),('decisions.csv',all_decisions),('daily_equity.csv',all_daily)):
  fields=sorted({k for row in rows for k in row})
  with (R/filename).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
if __name__=='__main__':main()
