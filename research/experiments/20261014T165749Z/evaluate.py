#!/usr/bin/env python3
"""Evaluate frozen daily channel-entry / Wilder-ATR trailing-stop variants."""
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];R=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));from kernel import fill
sp=importlib.util.spec_from_file_location('atr_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py');engine=importlib.util.module_from_spec(sp);sys.modules[sp.name]=engine;sp.loader.exec_module(engine)
MIN_NS=60_000_000_000;MIN_MS=60000;DAY_NS=1440*MIN_NS;DAY_MS=1440*MIN_MS
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ms):return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def put(path,obj):path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def write_csv(path,rows):
 fields=list(dict.fromkeys(k for x in rows for k in x))
 with path.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
def write_gz_csv(path,rows):
 import io
 fields=list(dict.fromkeys(k for x in rows for k in x));b=io.StringIO(newline='');w=csv.DictWriter(b,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
 with path.open('wb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as z:z.write(b.getvalue().encode())
def load_asset(asset,plan):
 frames=[];files=[]
 for item in plan['data']['assets'][asset]:
  path=ROOT/item['path'];assert path.is_file() and path.stat().st_size==item['bytes'] and sha(path)==item['sha256']
  f=pl.read_parquet(path,columns=['open_ts','available_ts','open','high','low','close','base_volume','quote_volume','is_closed'])
  assert f.height==525600 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN_NS).all() and (f['available_ts']-f['open_ts']==MIN_NS).all()
  assert (f['open']>0).all() and (f['low']>0).all() and (f['high']>=f['low']).all() and (f['close']>0).all() and (f['quote_volume']>=0).all()
  files.append({**item,'minute_bars':f.height,'first_open_ns':int(f['open_ts'][0]),'last_open_ns':int(f['open_ts'][-1])});frames.append(f)
 m=pl.concat(frames,how='vertical_relaxed').sort('open_ts');assert m.height==1051200 and (m['open_ts'].diff().drop_nulls()==MIN_NS).all()
 day=(m.with_columns((pl.col('open_ts')//DAY_NS).alias('day_ns')).group_by('day_ns',maintain_order=True).agg(pl.col('high').max().cast(pl.Float64).alias('high'),pl.col('low').min().cast(pl.Float64).alias('low'),pl.col('close').last().cast(pl.Float64).alias('close'),pl.col('quote_volume').sum().cast(pl.Float64).alias('quote_volume'),pl.len().alias('n')).sort('day_ns'))
 assert day.height==730 and (day['n']==1440).all()
 ts=day['day_ns'].to_numpy()*DAY_MS;hi=day['high'].to_numpy();lo=day['low'].to_numpy();cl=day['close'].to_numpy();qv=day['quote_volume'].to_numpy()
 assert np.all(np.diff(ts)==DAY_MS) and np.isfinite(hi).all() and np.isfinite(lo).all() and np.isfinite(cl).all() and np.isfinite(qv).all() and (lo>0).all() and (hi>=lo).all() and (cl>0).all() and (qv>=0).all()
 dr=[{'date':datetime.fromtimestamp(int(t)/1000,timezone.utc).date().isoformat(),'day_open_ms':int(t),'high':D(str(h)),'low':D(str(l)),'close':D(str(c)),'quote_volume':D(str(v))} for t,h,l,c,v in zip(ts,hi,lo,cl,qv)]
 return {'asset':asset,'files':files,'minute_ts':m['open_ts'].to_numpy()//1_000_000,'minute_open':m['open'].cast(pl.Float64).to_numpy(),'minute_close':m['close'].cast(pl.Float64).to_numpy(),'minute_base':m['base_volume'].cast(pl.Float64).to_numpy(),'minute_quote':m['quote_volume'].cast(pl.Float64).to_numpy(),'day_ts':ts,'daily_high':hi,'daily_low':lo,'daily_close':cl,'daily_rows':dr,'ohlc_sha256':hashlib.sha256(np.column_stack([hi,lo,cl]).astype('<f8').tobytes()).hexdigest()}
def wilder_atr(m,n):
 h=m['daily_high'];l=m['daily_low'];c=m['daily_close'];tr=np.empty(len(c),dtype=np.float64);tr[0]=h[0]-l[0]
 for j in range(1,len(c)):tr[j]=max(h[j]-l[j],abs(h[j]-c[j-1]),abs(l[j]-c[j-1]))
 out=np.full(len(c),np.nan,dtype=np.float64)
 if n<len(c):
  out[n]=float(np.mean(tr[1:n+1]))
  for j in range(n+1,len(c)):out[j]=((n-1)*out[j-1]+tr[j])/n
 assert np.isfinite(out[n:]).all() and (out[n:]>=0).all()
 return out,tr
def dd(v):
 a=np.asarray(v,dtype=np.float64);p=np.maximum.accumulate(a);return float(np.max(np.where(p>0,100*(1-a/p),0),initial=0))
def evaluate_one(row,mult,m,filters,plan):
 spec=json.loads((ROOT/row['spec']).read_text());p=spec['parameters'];a=row['asset'];E=p['entry_lookback_days'];N=p['wilder_atr_period'];M=p['trailing_stop_multiple'];cap=D('2000');cash=cap;units=D(0);peak_close=None;atr_entry=None;stop=None
 atr,tr=wilder_atr(m,N);start=int(datetime.fromisoformat(plan['time_boundaries']['oos_start_utc'].replace('Z','+00:00')).timestamp()*1000);end=int(datetime.fromisoformat(plan['time_boundaries']['oos_end_exclusive_utc'].replace('Z','+00:00')).timestamp()*1000);m0=int(m['minute_ts'][0]);start_i=(start-m0)//MIN_MS;end_i=(end-m0)//MIN_MS;day0=int(m['day_ts'][0])
 assert m['minute_ts'][start_i]==start and m['minute_ts'][end_i]==end and end_i-start_i==360*1440
 events=[];trades=[];decisions=[];filled=rejected=trips=0;parts={k:D(0) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
 for step in range(360):
  exec_ms=start+step*DAY_MS;signal_ms=exec_ms-DAY_MS-MIN_MS;idx=(signal_ms-day0)//DAY_MS;assert m['day_ts'][idx]==signal_ms and idx>=max(E,N)
  prev_high=float(np.max(m['daily_high'][idx-E:idx]));close=float(m['daily_close'][idx]);atrv=float(atr[idx]);prior_desired=units>0;decision_stop=stop;action='hold';reason='state_unchanged'
  if units==0:
   if close>prev_high:action='entry';reason='close_strictly_above_prior_high_channel'
  else:
   peak_close=max(float(peak_close),close);stop=max(float(stop),peak_close-M*float(atr_entry));decision_stop=stop
   if close<=stop:action='exit';reason='closed_close_at_or_below_ratchet_stop'
  target=action!='exit' and (action=='entry' or units>0)
  decisions.append({'configuration':row['name'],'asset':a,'cost_multiplier':mult,'signal_day_utc':stamp(signal_ms),'signal_available_at_utc':stamp(signal_ms+DAY_MS),'simulated_decision_at_utc':stamp(exec_ms),'execution_delay_seconds':60,'entry_lookback_days':E,'atr_period':N,'stop_multiple':M,'daily_close':close,'prior_E_day_high':prev_high,'true_range':float(tr[idx]),'wilder_atr':atrv,'prior_desired_long':prior_desired,'desired_long':bool(target),'action':action,'stop_before_decision':decision_stop,'peak_close':peak_close,'reason':reason})
  if action not in ('entry','exit'):continue
  mi=(exec_ms-m0)//MIN_MS;ref=D(str(m['minute_open'][mi]));day_i=(exec_ms-day0)//DAY_MS;adv,sigma=engine.lagged_cost_inputs(m['daily_rows'],int(day_i));avgmins=int(filters.get('PERCENT_PRICE_BY_SIDE',filters.get('PERCENT_PRICE',{})).get('avgPriceMins',5));base=m['minute_base'][mi-avgmins:mi];quote=m['minute_quote'][mi-avgmins:mi];bs=float(np.sum(base));qs=float(np.sum(quote));proxy=D(str(qs/bs if bs>0 else float(ref)))
  cb,ub=cash,units;c2,u2,t=fill(cash,units,action=='entry',ref,D(str(adv)),D(str(sigma)),mult,filters,proxy)
  t.update({'configuration':row['name'],'asset':a,'cost_multiplier':mult,'trade_id':f'{row["name"]}:{mult}:{exec_ms}:{action}','reason':reason,'signal_day_utc':stamp(signal_ms),'signal_available_utc':stamp(signal_ms+DAY_MS),'execution_utc':stamp(int(m['minute_ts'][mi])),'signal_to_execution_seconds':60,'minute_index':int(mi),'terminal':False,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(c2),'units_after':str(u2),'observed_signal':{'daily_close':close,'entry_prior_Eday_high':prev_high,'ATR':atrv,'entry_peak_close':peak_close,'entry_ATR':atr_entry,'stop':stop}});trades.append(t)
  if t['status']=='filled':
   filled+=1;cash,units=c2,u2;events.append({'minute_index':int(mi),'reference':ref,'cash_after':cash,'units_after':units,'trade_id':t['trade_id']})
   for k,v in t['cost_parts'].items():parts[k]+=D(v)
   if action=='entry':peak_close=close;atr_entry=atrv;stop=peak_close-M*atr_entry
   elif action=='exit' and units==0:trips+=1;peak_close=atr_entry=stop=None
  else:rejected+=1
 # Always liquidate a remaining terminal lot at the fixed OOS boundary.
 if units>0:
  ref=D(str(m['minute_open'][end_i]));adv,sigma=engine.lagged_cost_inputs(m['daily_rows'],int((end-day0)//DAY_MS));bs=float(np.sum(m['minute_base'][end_i-5:end_i]));qs=float(np.sum(m['minute_quote'][end_i-5:end_i]));proxy=D(str(qs/bs if bs>0 else float(ref)));cb,ub=cash,units;c2,u2,t=fill(cash,units,False,ref,D(str(adv)),D(str(sigma)),mult,filters,proxy)
  t.update({'configuration':row['name'],'asset':a,'cost_multiplier':mult,'trade_id':f'{row["name"]}:{mult}:{end}:terminal','reason':'predeclared_terminal_liquidation','signal_day_utc':stamp(end-DAY_MS-MIN_MS),'signal_available_utc':stamp(end-MIN_MS),'execution_utc':stamp(int(m['minute_ts'][end_i])),'signal_to_execution_seconds':60,'minute_index':int(end_i),'terminal':True,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(c2),'units_after':str(u2),'observed_signal':None});trades.append(t)
  if t['status']=='filled':
   filled+=1;cash,units=c2,u2;trips+=1;events.append({'minute_index':int(end_i),'reference':ref,'cash_after':cash,'units_after':units,'trade_id':t['trade_id']})
   for k,v in t['cost_parts'].items():parts[k]+=D(v)
  else:rejected+=1
 assert units==0,'Unable to terminally liquidate; keep explicit failure outcome.'
 # Continuous minute-close NAV plus post-fill references, then terminal mark.
 navclose=[];post={};cc,uu=cap,D(0);cursor=start_i
 for ev in sorted(events,key=lambda x:x['minute_index']):
  mi=ev['minute_index']
  if mi>=end_i:continue
  if mi>cursor:navclose.extend((float(cc)+float(uu)*m['minute_close'][cursor:mi]).tolist())
  cc,uu=ev['cash_after'],ev['units_after'];post[mi]=float(cc+uu*ev['reference']);cursor=mi
 if cursor<end_i:navclose.extend((float(cc)+float(uu)*m['minute_close'][cursor:end_i]).tolist())
 assert len(navclose)==end_i-start_i
 samples=[]
 for i,v in enumerate(navclose):
  if start_i+i in post:samples.append(post[start_i+i])
  samples.append(v)
 daily=[float(cap)]+[navclose[k*1440+1438] for k in range(360)];terminal=cash+units*D(str(m['minute_open'][end_i]));daily[-1]=float(terminal);samples.append(float(terminal))
 folds=[]
 for f in range(12):
  x,y=daily[f*30],daily[(f+1)*30];seg=daily[f*30:(f+1)*30+1];folds.append({'fold':f+1,'start_utc':stamp(start+f*30*DAY_MS),'end_exclusive_utc':stamp(start+(f+1)*30*DAY_MS),'start_nav_usdt':x,'end_nav_usdt':y,'net_return_pct':100*(y/x-1),'daily_sample_drawdown_pct':dd(seg),'observations':31})
 r=np.asarray(daily[1:])/np.asarray(daily[:-1])-1;sd=float(np.std(r,ddof=1));sh=float(np.mean(r)/sd*math.sqrt(365)) if sd else None
 cost=sum(parts.values(),D(0));gross=terminal-cap+cost;cagr=(float(terminal)/float(cap))**(365/360)-1;daydd=dd(daily)
 return {'configuration':row['name'],'asset':a,'entry_lookback_days':E,'atr_period':N,'stop_multiple':M,'cost_multiplier':mult,'terminal_nav_usdt':str(terminal),'net_pnl_usdt':str(terminal-cap),'net_return_pct':float(100*(terminal/cap-1)),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_flat':units==0,'cost_usdt':str(cost),'cost_parts_usdt':{k:str(v) for k,v in parts.items()},'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,'max_drawdown_1m_sampled_pct':dd(samples),'daily_sample_drawdown_pct':daydd,'drawdown_scope':'OOS 1-minute close marks plus immediate post-fill references and terminal close; intraminute extrema excluded.','daily_sharpe_annualized':sh,'cagr_pct':cagr*100,'calmar_daily_sampled':cagr/(daydd/100) if daydd else None,'filled_orders':filled,'rejected_orders':rejected,'round_trips':trips,'positive_folds':sum(x['net_return_pct']>0 for x in folds),'folds':folds,'minute_nav_samples':len(samples),'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(samples,dtype='<f8').tobytes()).hexdigest(),'daily_nav':daily,'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(daily,dtype='<f8').tobytes()).hexdigest(),'trades':trades,'decisions':decisions}
def main():
 plan=json.loads((R/'plan.json').read_text());batch=json.loads((R/'batch.json').read_text());filters=json.loads((R/'exchange_filters.json').read_text())['filters'];markets={a:load_asset(a,plan) for a in ('BTC','ETH')};configs={};trades=[];decisions=[];daily_rows=[];fold_rows=[];cost_rows=[]
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());assert registry.fingerprint(spec)==row['fingerprint'];scenes={}
  for mult in (1,2,3):
   z=evaluate_one(row,mult,markets[row['asset']],filters[row['asset']],plan);scenes[str(mult)]=z;trades+=z['trades'];decisions+=z['decisions']
   for j,v in enumerate(z['daily_nav']):daily_rows.append({'configuration':row['name'],'asset':row['asset'],'entry_lookback_days':row['entry_lookback_days'],'atr_period':row['atr_period'],'stop_multiple':row['stop_multiple'],'cost_multiplier':mult,'day_index':j,'nav_usdt':v})
   for f in z['folds']:fold_rows.append({'configuration':row['name'],'asset':row['asset'],'entry_lookback_days':row['entry_lookback_days'],'atr_period':row['atr_period'],'stop_multiple':row['stop_multiple'],'cost_multiplier':mult,**f})
   cost_rows.append({'configuration':row['name'],'asset':row['asset'],'entry_lookback_days':row['entry_lookback_days'],'atr_period':row['atr_period'],'stop_multiple':row['stop_multiple'],'cost_multiplier':mult,'net_return_pct':z['net_return_pct'],'cost_usdt':z['cost_usdt'],'gross_reference_pnl_to_cost':z['gross_reference_pnl_to_cost'],'positive_folds':z['positive_folds'],'round_trips':z['round_trips'],'rejected_orders':z['rejected_orders'],**{f'cost_{k}_usdt':v for k,v in z['cost_parts_usdt'].items()}})
   print(row['name'],mult,round(z['net_return_pct'],5),z['round_trips'],z['rejected_orders'],flush=True)
  configs[row['name']]={'name':row['name'],'asset':row['asset'],'entry_lookback_days':row['entry_lookback_days'],'atr_period':row['atr_period'],'stop_multiple':row['stop_multiple'],'fingerprint':row['fingerprint'],'spec_path':row['spec'],'initial_capital_usdt':2000,'raw_asset_weight':1.0,'scenarios':scenes}
 gridE=plan['grid']['entry_lookback_days'];gridN=plan['grid']['wilder_atr_periods'];gridM=plan['grid']['trailing_stop_multipliers'];by={(c['asset'],c['entry_lookback_days'],c['atr_period'],c['stop_multiple']):c for c in configs.values()}
 for c in configs.values():
  neighbors=[]
  for i in range(max(0,gridE.index(c['entry_lookback_days'])-1),min(len(gridE),gridE.index(c['entry_lookback_days'])+2)):
   for j in range(max(0,gridN.index(c['atr_period'])-1),min(len(gridN),gridN.index(c['atr_period'])+2)):
    for k in range(max(0,gridM.index(c['stop_multiple'])-1),min(len(gridM),gridM.index(c['stop_multiple'])+2)):
     neighbors.append(by[(c['asset'],gridE[i],gridN[j],gridM[k])])
  frac=sum(x['scenarios']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors);c['sensitivity']={'neighbor_count':len(neighbors),'local_3x_neighbor_positive_fraction':frac,'neighbor_names':[x['name'] for x in neighbors]}
  one=c['scenarios']['1'];three=c['scenarios']['3'];c['gates']={'all_cost_scenarios_positive':all(c['scenarios'][str(k)]['net_return_pct']>0 for k in (1,2,3)),'positive_1x_folds_at_least_8':one['positive_folds']>=8,'drawdown3_lte25':three['max_drawdown_1m_sampled_pct']<=25,'neighbor3_positive_fraction_gte60':frac>=.6,'round_trips1_gte8':one['round_trips']>=8,'gross_cost_ratio1_gte2_5':one['gross_reference_pnl_to_cost'] is not None and one['gross_reference_pnl_to_cost']>=2.5,'no_exchange_or_capacity_rejections':all(c['scenarios'][str(k)]['rejected_orders']==0 for k in (1,2,3)),'terminal_flat':all(c['scenarios'][str(k)]['terminal_flat'] for k in (1,2,3))};c['status']='passed' if all(c['gates'].values()) else 'rejected'
 prior=json.loads((ROOT/'research/experiments/20261014T084051Z/report.json').read_text());bench={a:prior['benchmark_read_only']['assets'][a] for a in ('BTC','ETH')}
 for c in configs.values():
  for z in c['scenarios'].values():
   for k in ('trades','decisions','daily_nav'):z.pop(k,None)
 inputs={'assets':{a:{'source_files':markets[a]['files'],'minute_bars':len(markets[a]['minute_ts']),'daily_bars':len(markets[a]['day_ts']),'daily_ohlc_sha256_f64le':markets[a]['ohlc_sha256']} for a in markets}}
 report={'round':R.name,'frozen_plan_sha256':sha(R/'plan.json'),'input_data':inputs,'exchange_info_raw_sha256':sha(R/'exchange_info_raw.json'),'benchmark_read_only':{'source_report':'research/experiments/20261014T084051Z/report.json','same_OOS_period_buy_hold':bench,'rerun':False},'summary':{'candidate_configs':len(configs),'passed':sum(c['status']=='passed' for c in configs.values()),'rejected':sum(c['status']=='rejected' for c in configs.values()),'cost_scenarios':len(configs)*3,'oos_days':360,'folds':12,'fold_days':30,'positive_configs_by_cost':{str(k):sum(c['scenarios'][str(k)]['net_return_pct']>0 for c in configs.values()) for k in (1,2,3)},'configs_with_8_positive_1x_folds':sum(c['scenarios']['1']['positive_folds']>=8 for c in configs.values()),'global_3x_positive_neighbor_fraction':sum(c['scenarios']['3']['net_return_pct']>0 for c in configs.values())/len(configs),'ranked_by_1x_net_return':sorted(configs,key=lambda n:configs[n]['scenarios']['1']['net_return_pct'],reverse=True)},'configs':configs,'artifacts':{'fold_results':'fold_results.csv','cost_scenarios':'cost_scenarios.csv','daily_equity':'daily_equity.csv.gz','trades':'trades.csv.gz','decisions':'decisions.csv.gz'}}
 write_csv(R/'fold_results.csv',fold_rows);write_csv(R/'cost_scenarios.csv',cost_rows);write_gz_csv(R/'daily_equity.csv.gz',daily_rows);write_gz_csv(R/'trades.csv.gz',trades);write_gz_csv(R/'decisions.csv.gz',decisions);put(R/'report.json',report)
 print('SUMMARY',json.dumps(report['summary'],sort_keys=True))
if __name__=='__main__':main()
