#!/usr/bin/env python3
"""Evaluate the frozen UTC weekday scheduled-window grid using archived Binance 1m bars."""
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone,timedelta
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));from kernel import fill
sys.path.insert(0,str(ROOT/'research/experiments/20261014T084051Z'))
# Reuse the independently reviewed lagged 20-day volatility / quote-ADV estimator.
sp=importlib.util.spec_from_file_location('weekday_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py');engine=importlib.util.module_from_spec(sp);sys.modules[sp.name]=engine;sp.loader.exec_module(engine)
MIN_NS=60_000_000_000;MIN_MS=60000;DAY_NS=1440*MIN_NS;DAY_MS=1440*MIN_MS
WEEKDAYS=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ms):return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def put(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def write_csv(path,rows):
 if not rows:return
 fields=list(dict.fromkeys(k for row in rows for k in row))
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
def write_gz_csv(path,rows):
 if not rows:return
 fields=list(dict.fromkeys(k for row in rows for k in row))
 with path.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as gz:
   import io
   text=io.StringIO(newline='');w=csv.DictWriter(text,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows);gz.write(text.getvalue().encode())
def load_asset(asset,plan):
 frames=[];files=[]
 for item in plan['data']['assets'][asset]:
  p=ROOT/item['path'];assert p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['sha256']
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==525600 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN_NS).all() and (f['available_ts']-f['open_ts']==MIN_NS).all()
  assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all()
  files.append({**item,'bars':f.height,'first_open_ns':int(f['open_ts'][0]),'last_open_ns':int(f['open_ts'][-1])});frames.append(f)
 m=pl.concat(frames,how='vertical_relaxed').sort('open_ts');assert m.height==1051200 and (m['open_ts'].diff().drop_nulls()==MIN_NS).all()
 day=(m.with_columns((pl.col('open_ts')//DAY_NS).alias('day_ns')).group_by('day_ns',maintain_order=True).agg(pl.col('close').last().cast(pl.Float64).alias('close'),pl.col('quote_volume').sum().cast(pl.Float64).alias('quote_volume'),pl.len().alias('n')).sort('day_ns'))
 assert day.height==730 and (day['n']==1440).all()
 ts=day['day_ns'].to_numpy()*DAY_MS;cl=day['close'].to_numpy();qv=day['quote_volume'].to_numpy()
 assert np.all(np.diff(ts)==DAY_MS) and np.isfinite(cl).all() and (cl>0).all() and np.isfinite(qv).all() and (qv>=0).all()
 dr=[{'date':datetime.fromtimestamp(int(t)/1000,timezone.utc).date().isoformat(),'day_open_ms':int(t),'close':D(str(c)),'quote_volume':D(str(v))} for t,c,v in zip(ts,cl,qv)]
 return {'asset':asset,'files':files,'ts':m['open_ts'].to_numpy()//1_000_000,'op':m['open'].cast(pl.Float64).to_numpy(),'cl':m['close'].cast(pl.Float64).to_numpy(),'base':m['base_volume'].cast(pl.Float64).to_numpy(),'quote':m['quote_volume'].cast(pl.Float64).to_numpy(),'day_ts':ts,'daily_close':cl,'daily_qv':qv,'daily_rows':dr,'close_sha':hashlib.sha256(np.asarray(cl,dtype='<f8').tobytes()).hexdigest()}
def dd(vals):
 a=np.asarray(vals,dtype=np.float64);peak=np.maximum.accumulate(a);return float(np.max(np.where(peak>0,100*(1-a/peak),0),initial=0))
def evaluate_one(row,mult,market,filters,plan):
 asset=row['asset'];dow=row['weekday_utc'];hold=row['holding_days'];capital=D('2000');cash=capital;units=D(0)
 start=int(datetime.fromisoformat(plan['time_boundaries']['oos_start_utc'].replace('Z','+00:00')).timestamp()*1000);end=int(datetime.fromisoformat(plan['time_boundaries']['oos_end_exclusive_utc'].replace('Z','+00:00')).timestamp()*1000)
 m0=int(market['ts'][0]);start_i=(start-m0)//MIN_MS;end_i=(end-m0)//MIN_MS;assert market['ts'][start_i]==start and market['ts'][end_i]==end and end_i-start_i==360*1440
 day0=int(market['day_ts'][0]);day_end=(end-start)//DAY_MS
 assert start%DAY_MS==MIN_MS and end%DAY_MS==MIN_MS
 events=[];attempts=[];trips=0;filled=0;rejected=0;cost_parts={k:D(0) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
 # Calendar-only signal schedule. Every eligible event and its exit are fixed before data is read.
 scheduled=[]
 for k in range(360):
  day_ms=start//DAY_MS*DAY_MS+k*DAY_MS
  if datetime.fromtimestamp(day_ms/1000,timezone.utc).weekday()==dow:
   entry=day_ms+MIN_MS;exit_ms=entry+hold*DAY_MS
   if entry>=start and exit_ms<=end:scheduled.append((entry,exit_ms))
 for entry_ms,exit_ms in scheduled:
  assert units==0
  entry_i=(entry_ms-m0)//MIN_MS;entry_ref=D(str(market['op'][entry_i]));day_i=(entry_ms-day0)//DAY_MS
  av,sig=engine.lagged_cost_inputs(market['daily_rows'],int(day_i))
  avgmins=int(filters['PERCENT_PRICE_BY_SIDE']['avgPriceMins']);base=market['base'][entry_i-avgmins:entry_i];quote=market['quote'][entry_i-avgmins:entry_i];bs=float(np.sum(base));qs=float(np.sum(quote));proxy=D(str(qs/bs if bs>0 else float(entry_ref)))
  b0,u0=cash,units;c2,u2,t=fill(cash,units,True,entry_ref,D(str(av)),D(str(sig)),mult,filters,proxy)
  t.update({'configuration':row['name'],'asset':asset,'weekday_utc':dow,'weekday_name':WEEKDAYS[dow],'holding_days':hold,'cost_multiplier':mult,'trade_id':f'{row["name"]}:{mult}:{entry_ms}:entry','attempt':1,'scheduled_event_utc':stamp(entry_ms),'signal_available_utc':stamp(entry_ms-MIN_MS),'execution_utc':stamp(entry_ms),'signal_to_execution_seconds':60,'minute_index':int(entry_i),'reason':'scheduled_weekly_entry','terminal':False,'cash_before':str(b0),'units_before':str(u0),'cash_after':str(c2),'units_after':str(u2)})
  attempts.append(t)
  if t['status']!='filled':rejected+=1;continue
  cash,units=c2,u2;filled+=1;events.append({'minute_index':int(entry_i),'ref':entry_ref,'cash':cash,'units':units,'trade_id':t['trade_id']})
  for k,v in t['cost_parts'].items():cost_parts[k]+=D(v)
  due_i=(exit_ms-m0)//MIN_MS;scheduled_due=due_i;success=False
  for attempt_i,mi in enumerate(range(due_i,end_i+1),1):
   ref=D(str(market['op'][mi]));day_i=(int(market['ts'][mi])-day0)//DAY_MS;av,sig=engine.lagged_cost_inputs(market['daily_rows'],int(day_i))
   b0,u0=cash,units;base=market['base'][mi-avgmins:mi];quote=market['quote'][mi-avgmins:mi];bs=float(np.sum(base));qs=float(np.sum(quote));proxy=D(str(qs/bs if bs>0 else float(ref)))
   c2,u2,t=fill(cash,units,False,ref,D(str(av)),D(str(sig)),mult,filters,proxy)
   t.update({'configuration':row['name'],'asset':asset,'weekday_utc':dow,'weekday_name':WEEKDAYS[dow],'holding_days':hold,'cost_multiplier':mult,'trade_id':f'{row["name"]}:{mult}:{entry_ms}:exit:{mi}','attempt':attempt_i,'scheduled_event_utc':stamp(exit_ms),'signal_available_utc':stamp(exit_ms-MIN_MS),'execution_utc':stamp(int(market['ts'][mi])),'signal_to_execution_seconds':int((int(market['ts'][mi])-exit_ms+MIN_MS)/1000),'minute_index':int(mi),'reason':'scheduled_weekly_exit_retry' if mi!=scheduled_due else 'scheduled_weekly_exit','terminal':mi==end_i,'cash_before':str(b0),'units_before':str(u0),'cash_after':str(c2),'units_after':str(u2)})
   attempts.append(t)
   if t['status']=='filled':
    cash,units=c2,u2;filled+=1;trips+=1;success=True;events.append({'minute_index':int(mi),'ref':ref,'cash':cash,'units':units,'trade_id':t['trade_id']})
    for k,v in t['cost_parts'].items():cost_parts[k]+=D(v)
    break
   rejected+=1
  if not success: raise AssertionError(f'no terminal fill before cutoff for {row["name"]} x{mult}; position must remain explicit')
  assert units==0
 # Continuous one-minute close NAV plus an immediately post-fill reference sample for full OOS sampled drawdown.
 minute_close_nav=[];postfills=[];curcash=capital;curunits=D(0);cursor=start_i
 for event in sorted(events,key=lambda x:x['minute_index']):
  mi=event['minute_index']
  if mi>=end_i: continue
  if mi>cursor:minute_close_nav.extend((float(curcash)+float(curunits)*market['cl'][cursor:mi]).tolist())
  curcash,curunits=event['cash'],event['units'];postfills.append({'minute_index':mi,'nav':float(curcash+curunits*event['ref'])});cursor=mi
 if cursor<end_i:minute_close_nav.extend((float(curcash)+float(curunits)*market['cl'][cursor:end_i]).tolist())
 assert len(minute_close_nav)==end_i-start_i
 # Minute chronology with after-fill samples inserted immediately before the same bar's close.
 mf={x['minute_index']:x['nav'] for x in postfills};sampled=[]
 for rel,v in enumerate(minute_close_nav):
  mi=start_i+rel
  if mi in mf:sampled.append(mf[mi])
  sampled.append(v)
 # Daily close marks are the 23:59 UTC close of each day; include capital as the initial value.
 dnav=[float(capital)]
 for k in range(360):
  mi=start_i+k*1440+1438;dnav.append(minute_close_nav[mi-start_i])
 terminal_ref=D(str(market['op'][end_i]));terminal_nav=cash+units*terminal_ref
 if units!=0: raise AssertionError('nonflat terminal account')
 total_cost=sum(cost_parts.values(),D(0));gross_ref=terminal_nav-capital+total_cost
 folds=[]
 for f in range(12):
  a=dnav[f*30];b=dnav[(f+1)*30];seg=dnav[f*30:(f+1)*30+1]
  folds.append({'fold':f+1,'start_utc':stamp(start+f*30*DAY_MS),'end_exclusive_utc':stamp(start+(f+1)*30*DAY_MS),'start_nav_usdt':a,'end_nav_usdt':b,'net_return_pct':(b/a-1)*100,'daily_sample_drawdown_pct':dd(seg),'scheduled_trips':sum(start+f*30*DAY_MS<=x[0]<start+(f+1)*30*DAY_MS for x in scheduled)})
 r=np.asarray(dnav[1:])/np.asarray(dnav[:-1])-1;sd=float(np.std(r,ddof=1));sh=float(np.mean(r)/sd*math.sqrt(365)) if sd else None
 # Daily open-to-open returns grouped by UTC weekday, fixed-clock matching the entry/exit references.
 wret=[]
 for k in range(360):
  t=start+k*DAY_MS;idx=(t-m0)//MIN_MS;endidx=idx+1440
  if endidx>end_i:continue
  value=100*(float(market['op'][endidx])/float(market['op'][idx])-1)
  dt=datetime.fromtimestamp(t/1000,timezone.utc)
  wret.append({'date_utc':dt.date().isoformat(),'weekday_utc':dt.weekday(),'weekday_name':WEEKDAYS[dt.weekday()],'open_to_open_24h_gross_return_pct':value})
 costs={k:str(v) for k,v in cost_parts.items()}
 return {'configuration':row['name'],'asset':asset,'weekday_utc':dow,'weekday_name':WEEKDAYS[dow],'holding_days':hold,'cost_multiplier':mult,'terminal_nav_usdt':str(terminal_nav),'net_pnl_usdt':str(terminal_nav-capital),'net_return_pct':float((terminal_nav/capital-1)*100),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_flat':units==0,'cost_usdt':str(total_cost),'cost_parts_usdt':costs,'gross_reference_pnl_usdt':str(gross_ref),'gross_reference_pnl_to_cost':float(gross_ref/total_cost) if total_cost else None,'max_drawdown_1m_sampled_pct':dd(sampled),'daily_sample_drawdown_pct':dd(dnav),'drawdown_scope':'All OOS 1-minute close marks plus immediate post-fill reference marks; excludes intraminute extrema.','daily_sharpe_annualized':sh,'cagr_pct':(float(terminal_nav)/float(capital))**(365/360)*100-100,'calmar_daily_sampled':(((float(terminal_nav)/float(capital))**(365/360)-1)/(dd(dnav)/100)) if dd(dnav) else None,'filled_orders':filled,'rejected_attempts':rejected,'round_trips':trips,'scheduled_entries':len(scheduled),'positive_folds':sum(x['net_return_pct']>0 for x in folds),'folds':folds,'minute_nav_samples':len(sampled),'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(sampled,dtype='<f8').tobytes()).hexdigest(),'daily_nav':dnav,'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(dnav,dtype='<f8').tobytes()).hexdigest(),'trade_attempts':attempts,'daily_gross_returns':wret,'end_boundary_mark_usdt':str(terminal_ref),'terminal_liquidation_in_oos':bool(events and events[-1]['minute_index']<end_i)}
def main():
 plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());filters=json.loads((R/'exchange_filters.json').read_text())['filters'];markets={a:load_asset(a,plan) for a in ('BTC','ETH')}
 allrows={};attempt_rows=[];dailyrows=[];foldrows=[];costrows=[];grossrows=[]
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert registry.fingerprint(spec)==row['fingerprint'];scenes={}
  for mult in (1,2,3):
   z=evaluate_one(row,mult,markets[row['asset']],filters[row['asset']],plan);scenes[str(mult)]=z;attempt_rows+=z['trade_attempts'];
   for k,v in enumerate(z['daily_nav']):dailyrows.append({'configuration':row['name'],'asset':row['asset'],'weekday_utc':row['weekday_utc'],'holding_days':row['holding_days'],'cost_multiplier':mult,'day_index':k,'nav_usdt':v})
   for f in z['folds']:foldrows.append({'configuration':row['name'],'asset':row['asset'],'weekday_utc':row['weekday_utc'],'holding_days':row['holding_days'],'cost_multiplier':mult,**f})
   costrows.append({'configuration':row['name'],'asset':row['asset'],'weekday_utc':row['weekday_utc'],'weekday_name':WEEKDAYS[row['weekday_utc']],'holding_days':row['holding_days'],'cost_multiplier':mult,**{f'cost_{k}_usdt':v for k,v in z['cost_parts_usdt'].items()},'total_cost_usdt':z['cost_usdt'],'gross_reference_pnl_to_cost':z['gross_reference_pnl_to_cost'],'net_return_pct':z['net_return_pct'],'round_trips':z['round_trips'],'rejected_attempts':z['rejected_attempts']})
   for x in z['daily_gross_returns']:grossrows.append({'configuration':row['name'],'asset':row['asset'],'weekday_utc':row['weekday_utc'],'holding_days':row['holding_days'],'cost_multiplier':mult,**x})
   print(row['name'],mult,round(z['net_return_pct'],6),z['round_trips'],z['rejected_attempts'],flush=True)
  allrows[row['name']]={'name':row['name'],'asset':row['asset'],'weekday_utc':row['weekday_utc'],'weekday_name':WEEKDAYS[row['weekday_utc']],'holding_days':row['holding_days'],'fingerprint':row['fingerprint'],'spec_path':row['spec'],'initial_capital_usdt':2000,'raw_asset_weight':1.0,'scenarios':scenes}
 # Prespecified local sensitivity is categorical/cyclic weekday ±1 and both horizons.
 by={(x['asset'],x['weekday_utc'],x['holding_days']):x for x in allrows.values()}
 for x in allrows.values():
  ns=[]
  for wd in {(x['weekday_utc']-1)%7,x['weekday_utc'],(x['weekday_utc']+1)%7}:
   for h in (1,3):ns.append(by[(x['asset'],wd,h)])
  frac=sum(y['scenarios']['3']['net_return_pct']>0 for y in ns)/len(ns);x['sensitivity']={'local_neighbor_count':len(ns),'local_3x_neighbor_positive_fraction':frac,'neighbor_names':[y['name'] for y in ns]}
  one=x['scenarios']['1'];three=x['scenarios']['3']
  x['gates']={'all_1x_2x_3x_positive':all(x['scenarios'][str(k)]['net_return_pct']>0 for k in (1,2,3)),'positive_1x_folds_at_least_8':one['positive_folds']>=8,'drawdown3_lte25pct':three['max_drawdown_1m_sampled_pct']<=25,'neighbor3_positive_fraction_gte60':frac>=.6,'round_trips1_gte40':one['round_trips']>=40,'gross_cost_ratio1_gte2_5':one['gross_reference_pnl_to_cost'] is not None and one['gross_reference_pnl_to_cost']>=2.5,'no_exchange_or_capacity_rejections':all(x['scenarios'][str(k)]['rejected_attempts']==0 for k in (1,2,3)),'terminal_flat':all(x['scenarios'][str(k)]['terminal_flat'] for k in (1,2,3))}
  x['status']='passed' if all(x['gates'].values()) else 'rejected'
 prior=json.loads((ROOT/'research/experiments/20261014T084051Z/report.json').read_text())
 benchmarks={a:prior['benchmark_read_only']['assets'][a] for a in ('BTC','ETH')}
 for x in allrows.values():
  for s in x['scenarios'].values():
   for k in ('trade_attempts','daily_nav','daily_gross_returns'):s.pop(k,None)
 src={'assets':{a:{'source_files':markets[a]['files'],'minute_bars':len(markets[a]['ts']),'daily_bars':len(markets[a]['day_ts']),'daily_close_sha256_f64le':markets[a]['close_sha']} for a in markets}}
 report={'round':R.name,'frozen_plan_sha256':sha(R/'plan.json'),'input_data':src,'fresh_exchange_info_sha256':sha(R/'exchange_info_raw.json'),'benchmark_read_only':{'source_report':'research/experiments/20261014T084051Z/report.json','same_OOS_period_cost_adjusted_buy_hold':benchmarks,'rerun':False},'summary':{'candidate_configurations':len(allrows),'passed':sum(x['status']=='passed' for x in allrows.values()),'rejected':sum(x['status']=='rejected' for x in allrows.values()),'cost_scenarios':len(allrows)*3,'oos_days':360,'folds':12,'fold_days':30,'positive_configurations_by_cost':{str(k):sum(x['scenarios'][str(k)]['net_return_pct']>0 for x in allrows.values()) for k in (1,2,3)},'configurations_with_8_positive_folds':sum(x['scenarios']['1']['positive_folds']>=8 for x in allrows.values()),'global_3x_neighbor_robustness_fraction':sum(x['scenarios']['3']['net_return_pct']>0 for x in allrows.values())/len(allrows),'ranked_by_1x_net_return':sorted(allrows,key=lambda n:allrows[n]['scenarios']['1']['net_return_pct'],reverse=True)},'configs':allrows,'artifacts':{'trades':'trades.csv.gz','daily_equity':'daily_equity.csv.gz','fold_results':'fold_results.csv','cost_scenarios':'cost_scenarios.csv','weekday_daily_returns':'weekday_daily_returns.csv'}}
 write_csv(R/'fold_results.csv',foldrows);write_csv(R/'cost_scenarios.csv',costrows);write_csv(R/'weekday_daily_returns.csv',grossrows)
 write_gz_csv(R/'daily_equity.csv.gz',dailyrows);write_gz_csv(R/'trades.csv.gz',attempt_rows)
 put(R/'report.json',report)
 print('SUMMARY',json.dumps(report['summary'],sort_keys=True))
if __name__=='__main__':main()
