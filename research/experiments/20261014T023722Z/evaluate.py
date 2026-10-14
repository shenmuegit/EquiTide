#!/usr/bin/env python3
"""Evaluate the frozen CMF-confirmed daily channel grid on archived Binance spot bars."""
import csv,gzip,hashlib,json,math,os,statistics,sys,time
from datetime import datetime,timezone,timedelta
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));import kernel
DAY=86_400_000;MINUTE=60_000

def stamp(ms):return datetime.fromtimestamp(ms/1000,timezone.utc).isoformat().replace('+00:00','Z')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def dec(v):return D(str(v))
def write_json(p,x):p.write_text(json.dumps(clean(x),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def load_market(plan):
 assets={}
 for asset in ('BTC','ETH'):
  files=plan['data']['assets'][asset]
  frames=[]
  for meta in files:
   path=ROOT/meta['path'];assert sha(path)==meta['sha256'] and path.stat().st_size==meta['bytes']
   f=pl.read_parquet(path,columns=['open_ts','available_ts','open','high','low','close','quote_volume','is_closed'])
   assert f.height==525600 and f['is_closed'].all() and f['open_ts'].is_sorted()
   assert (f['available_ts'].to_numpy()-f['open_ts'].to_numpy()==MINUTE*1_000_000).all()
   assert (f['open_ts'].diff().drop_nulls()==MINUTE*1_000_000).all()
   frames.append(f)
  f=pl.concat(frames).sort('open_ts')
  ts_ns=f['open_ts'].to_numpy();ts=ts_ns//1_000_000
  assert len(ts)==1_051_200 and ts[0]==int(datetime(2024,9,16,tzinfo=timezone.utc).timestamp()*1000) and ts[-1]+MINUTE==int(datetime(2026,9,16,tzinfo=timezone.utc).timestamp()*1000)
  assert (np.diff(ts)==MINUTE).all(),f'{asset} source gap or overlap'
  daily=(f.with_columns((pl.col('open_ts')//(DAY*1_000_000)*DAY).alias('day_ts'))
      .group_by('day_ts',maintain_order=True)
      .agg(pl.col('open').first().cast(pl.Float64).alias('open'),pl.col('high').max().cast(pl.Float64).alias('high'),pl.col('low').min().cast(pl.Float64).alias('low'),pl.col('close').last().cast(pl.Float64).alias('close'),pl.col('quote_volume').sum().cast(pl.Float64).alias('quote_volume'),pl.len().alias('minute_count')))
  assert daily.height==730 and (daily['minute_count']==1440).all()
  assert daily['day_ts'].is_sorted() and (np.diff(daily['day_ts'].to_numpy())==DAY).all()
  arrays={'minute_ts':ts,'minute_open':f['open'].cast(pl.Float64).to_numpy(),'minute_close':f['close'].cast(pl.Float64).to_numpy(),
    'day_ts':daily['day_ts'].to_numpy(),'open':daily['open'].to_numpy(),'high':daily['high'].to_numpy(),'low':daily['low'].to_numpy(),'close':daily['close'].to_numpy(),'quote_volume':daily['quote_volume'].to_numpy(),'minute_count':daily['minute_count'].to_numpy()}
  assert all(np.isfinite(arrays[k]).all() for k in ('minute_open','minute_close','open','high','low','close','quote_volume'))
  assert (arrays['minute_open']>0).all() and (arrays['minute_close']>0).all() and (arrays['quote_volume']>=0).all()
  assert ((arrays['low']<=arrays['close'])&(arrays['close']<=arrays['high'])).all()
  arrays['cmfv']=np.where(arrays['high']>arrays['low'],((2*arrays['close']-arrays['high']-arrays['low'])/(arrays['high']-arrays['low']))*arrays['quote_volume'],0.0)
  assets[asset]=arrays
 filters={}
 ex=json.loads((ROUND/'exchange_info_raw.json').read_text())
 for asset in ('BTC','ETH'):
  s=next(x for x in ex['symbols'] if x['symbol']==asset+'USDT')
  assert s['status']=='TRADING' and s.get('isSpotTradingAllowed',True)
  filters[asset]={x['filterType']:x for x in s['filters']}
  for typ in ('PRICE_FILTER','LOT_SIZE','NOTIONAL','PERCENT_PRICE_BY_SIDE'):assert typ in filters[asset]
 return assets,filters

def cmf_at(m,i,n):
 a=i-n+1; assert a>=0
 v=m['quote_volume'][a:i+1];den=float(v.sum())
 return float(m['cmfv'][a:i+1].sum()/den) if den>0 else 0.0

def drawdown(path):
 ar=np.asarray(path,dtype=np.float64);peaks=np.maximum.accumulate(ar);dd=np.where(peaks>0,100*(1-ar/peaks),0)
 return float(dd.max(initial=0))

def evaluate_sleeve(name,asset,params,mult,m,filters,plan):
 capital=D('1000');cash=capital;units=D(0);cost_parts={x:D(0) for x in ('fee','half_spread','slippage','impact','tick_rounding')};trades=[];decisions=[]
 desired=False;last_fill=None;fills=rejects=round_trips=0
 start_ms=int(datetime.fromisoformat(plan['data']['start_utc'].replace('Z','+00:00')).timestamp()*1000)
 end_ms=int(datetime.fromisoformat(plan['data']['end_exclusive_utc'].replace('Z','+00:00')).timestamp()*1000)
 first=int(m['day_ts'][0]);daily_start_ms=first
 assert (end_ms-start_ms)==360*DAY and start_ms%DAY==MINUTE and end_ms%DAY==MINUTE
 start_i=(start_ms-int(m['minute_ts'][0]))//MINUTE;end_i=(end_ms-int(m['minute_ts'][0]))//MINUTE
 assert m['minute_ts'][start_i]==start_ms and m['minute_ts'][end_i]==end_ms
 nav_path=[float(capital)];daily_equity=[];daily_nav=[];fold_nav=[float(capital)];event_marks=[]
 prev_entry=params['channel_entry_lookback_days'];cmfn=params['cmf_lookback_days'];exitn=params['channel_exit_lookback_days'];threshold=params['cmf_entry_threshold']
 for k in range(360):
  exec_ms=start_ms+k*DAY;signal_ms=(exec_ms-MINUTE)-DAY;di=(signal_ms-daily_start_ms)//DAY
  assert m['day_ts'][di]==signal_ms
  cmfv=cmf_at(m,di,cmfn)
  upper=float(np.max(m['high'][di-prev_entry:di]));lower=float(np.min(m['low'][di-exitn:di]))
  close=float(m['close'][di]);entry=close>upper and cmfv>threshold;exit_signal=close<lower
  previous=desired
  if not desired and entry:desired=True
  elif desired and exit_signal:desired=False
  decision={'configuration':name,'asset':asset,'cost_multiplier':mult,'signal_day_utc':stamp(signal_ms),'signal_available_at_utc':stamp(signal_ms+DAY),'simulated_decision_at_utc':stamp(exec_ms),'execution_delay_seconds':60,'close':close,'prior_channel_entry_high':upper,'prior_channel_exit_low':lower,'entry_lookback_days':prev_entry,'exit_lookback_days':exitn,'cmf_lookback_days':cmfn,'cmf':cmfv,'cmf_threshold':threshold,'entry_channel_breakout':close>upper,'entry_flow_confirmation':cmfv>threshold,'exit_channel_breakdown':exit_signal,'previous_desired_long':previous,'desired_long':desired,'action':'entry' if desired and not previous else 'exit' if previous and not desired else 'hold'}
  decisions.append(decision)
  mi=(exec_ms-int(m['minute_ts'][0]))//MINUTE;ref=dec(m['minute_open'][mi]);avgmins=int(filters['PERCENT_PRICE_BY_SIDE']['avgPriceMins'])
  avg_price=dec(np.mean(m['minute_close'][mi-avgmins:mi])) if avgmins else ref
  terminal=False
  if (desired and units==0) or ((not desired) and units>0):
   vv=np.diff(np.log(m['close'][di-20:di+1]));sigma=dec(np.std(vv,ddof=1));adv=dec(np.mean(m['quote_volume'][di-19:di+1]))
   if adv<=0:raise ValueError('nonpositive lagged ADV')
   cash2,units2,tr=kernel.fill(cash,units,desired,ref,adv,sigma,mult,filters,avg_price)
   tr.update({'configuration':name,'asset':asset,'cost_multiplier':mult,'trade_id':f'{name}:{mult}:{asset}:{exec_ms}','signal_day_utc':stamp(signal_ms),'signal_available_at_utc':stamp(signal_ms+DAY),'simulated_at_utc':stamp(exec_ms),'quote_reference':'archived Binance 1m open; virtual price, not actual book quote','minute_index':int(mi),'terminal':False,'cmf':cmfv,'entry_high':upper,'exit_low':lower})
   trades.append(tr)
   if tr['status']=='filled':
    fills+=1;round_trips+=int(not desired and units>0 and units2==0);cash,units=cash2,units2;last_fill=tr
    for key in cost_parts:cost_parts[key]+=D(tr['cost_parts'][key])
   else:rejects+=1
   event_marks.append({'minute_index':int(mi),'reference':str(ref),'cash_after':str(cash),'units_after':str(units),'status':tr['status']})
  post_nav=float(cash+units*ref);nav_path.append(post_nav)
  if k>0 and k%30==0:fold_nav.append(post_nav)
  # Segment from this day's 00:01 execution through the next 00:00 bar close.
  close_end=mi+1440;assert close_end<=end_i
  nav_path.extend((float(cash)+float(units)*m['minute_close'][mi:close_end]).tolist())
  eod_i=mi+1438;eod_ms=int(m['minute_ts'][eod_i])+MINUTE;assert eod_ms==exec_ms+DAY-MINUTE
  eod_nav=float(cash)+float(units)*float(m['minute_close'][eod_i]);daily_equity.append({'configuration':name,'cost_multiplier':mult,'asset':asset,'timestamp_utc':stamp(eod_ms),'nav_usdt':eod_nav})
  daily_nav.append(eod_nav)
 # Force liquidation at predeclared terminal timestamp. No position carries beyond OOS.
 mi=end_i;ref=dec(m['minute_open'][mi]);avgmins=int(filters['PERCENT_PRICE_BY_SIDE']['avgPriceMins']);avg_price=dec(np.mean(m['minute_close'][mi-avgmins:mi])) if avgmins else ref
 if units>0:
  terminal_signal_ms=end_ms-MINUTE-DAY;terminal_di=(terminal_signal_ms-daily_start_ms)//DAY;assert m['day_ts'][terminal_di]==terminal_signal_ms
  terminal_adv=dec(np.mean(m['quote_volume'][terminal_di-19:terminal_di+1]));terminal_sigma=dec(np.std(np.diff(np.log(m['close'][terminal_di-20:terminal_di+1])),ddof=1))
  cash2,units2,tr=kernel.fill(cash,units,False,ref,terminal_adv,terminal_sigma,mult,filters,avg_price)
  tr.update({'configuration':name,'asset':asset,'cost_multiplier':mult,'trade_id':f'{name}:{mult}:{asset}:{end_ms}:terminal','signal_day_utc':stamp(end_ms-MINUTE-DAY),'signal_available_at_utc':stamp(end_ms-MINUTE),'simulated_at_utc':stamp(end_ms),'quote_reference':'archived Binance 1m open; terminal virtual liquidation','minute_index':int(mi),'terminal':True,'cmf':None,'entry_high':None,'exit_low':None})
  trades.append(tr)
  if tr['status']=='filled':
   fills+=1;round_trips+=1;cash,units=cash2,units2;last_fill=tr
   for key in cost_parts:cost_parts[key]+=D(tr['cost_parts'][key])
  else:rejects+=1
  event_marks.append({'minute_index':int(mi),'reference':str(ref),'cash_after':str(cash),'units_after':str(units),'status':tr['status']})
 terminal_nav=float(cash+units*ref);nav_path.append(terminal_nav);fold_nav.append(terminal_nav)
 assert units==0,'terminal liquidation did not flatten sleeve'
 assert len(fold_nav)==13
 folds=[]
 for i in range(12):
  a=fold_nav[i];b=fold_nav[i+1]
  folds.append({'fold':i+1,'start_utc':stamp(start_ms+i*30*DAY),'end_exclusive_utc':stamp(start_ms+(i+1)*30*DAY),'start_nav_usdt':a,'end_nav_usdt':b,'net_return_pct':(b/a-1)*100})
 fee=sum(cost_parts.values(),D(0));gross=terminal_nav-float(capital)+float(fee)
 return {'terminal_nav_usdt':str(D(str(terminal_nav))),'net_pnl_usdt':str(D(str(terminal_nav))-capital),'net_return_pct':(terminal_nav/float(capital)-1)*100,'cost_usdt':str(fee),'cost_parts_usdt':{k:str(v) for k,v in cost_parts.items()},'gross_reference_pnl_usdt':str(D(str(gross))),'gross_to_cost':gross/float(fee) if fee>0 else None,'fills':fills,'rejected_orders':rejects,'round_trips':round_trips,'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_reference_price':str(ref),'max_drawdown_1m_sampled_pct':drawdown(nav_path),'daily_sample_drawdown_pct':drawdown([float(capital)]+daily_nav+[terminal_nav]),'drawdown_scope':'OOS 1-minute archived closes plus immediate post-fill reference marks; no intra-minute extrema.','folds':folds,'fold_nav':[str(x) for x in fold_nav],'minute_nav_samples':len(nav_path),'sampled_nav_sha256':hashlib.sha256(np.asarray(nav_path,dtype='<f8').tobytes()).hexdigest(),'daily_nav':daily_nav,'daily_equity':daily_equity,'trades':trades,'decisions':decisions,'event_marks':event_marks,'asset':asset,'configuration':name}

def main():
 plan=json.loads((ROUND/'plan.json').read_text());plan_sha=sha(ROUND/'plan.json');plan['_sha256']=plan_sha
 batch=json.loads((ROUND/'batch.json').read_text())
 ledger=Path(os.environ.get('CMF_REGISTRY_LEDGER',ROOT/'research/automation/registry.jsonl'));rec=registry.read_records(ledger)
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());fp=registry.fingerprint(spec);r=rec.get(fp);assert r and r['status']=='reserved' and r['result_available'] is False,(row['name'],r)
 markets,filters=load_market(plan);assets={};all_trades=[];all_decisions=[];all_daily=[];configs={}
 start_ms=int(datetime.fromisoformat(plan['data']['start_utc'].replace('Z','+00:00')).timestamp()*1000);end_ms=int(datetime.fromisoformat(plan['data']['end_exclusive_utc'].replace('Z','+00:00')).timestamp()*1000)
 assert (end_ms-start_ms)==360*DAY and start_ms%DAY==MINUTE and end_ms%DAY==MINUTE
 prior=json.loads((ROOT/'research/experiments/20261013T224056Z/report.json').read_text())
 baseline=prior['configs']['hold_360d_BTC_ETH_50_50_monthly_volmanaged']
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());p=spec['parameters'];scenes={}
  for mult in (1,2,3):
   sleeves={a:evaluate_sleeve(row['name'],a,p,mult,markets[a],filters[a],plan) for a in ('BTC','ETH')}
   for a in ('BTC','ETH'):
    all_trades.extend(sleeves[a]['trades']);all_decisions.extend(sleeves[a]['decisions']);all_daily.extend(sleeves[a]['daily_equity'])
   daily_nav=np.asarray(sleeves['BTC']['daily_nav'])+np.asarray(sleeves['ETH']['daily_nav'])
   terminal=sum((dec(sleeves[a]['terminal_nav_usdt']) for a in ('BTC','ETH')),D(0))
   cost=sum((dec(sleeves[a]['cost_usdt']) for a in ('BTC','ETH')),D(0));costparts={k:str(sum((dec(sleeves[a]['cost_parts_usdt'][k]) for a in ('BTC','ETH')),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
   # Synchronized minute close portfolio NAV plus all immediate post-fill reference marks.
   minute_start=(start_ms-int(markets['BTC']['minute_ts'][0]))//MINUTE;minute_end=(end_ms-int(markets['BTC']['minute_ts'][0]))//MINUTE
   # Compute portfolio drawdown on synchronized OOS minute closes directly from post-fill sleeve states.
   base_minute=(np.asarray([float(dec('1000'))]* (minute_end-minute_start),dtype=np.float64))
   for a in ('BTC','ETH'):
    st=sleeves[a]
    # Build the true marked NAV series from fills and minute closes; reconstruct from event states.
    times=np.array(markets[a]['minute_ts'][minute_start:minute_end],dtype=np.int64)
    mclose=markets[a]['minute_close'][minute_start:minute_end]
    changes=sorted(st['event_marks'],key=lambda x:x['minute_index'])
    casharr=np.full(len(mclose),1000.0);unitsarr=np.zeros(len(mclose));cash=1000.0;units=0.0;cursor=0
    for e in changes:
     pos=e['minute_index']-minute_start
     if pos<0 or pos>=len(mclose):continue
     if pos>cursor:casharr[cursor:pos]=cash;unitsarr[cursor:pos]=units
     cash=float(dec(e['cash_after']));units=float(dec(e['units_after']));cursor=pos
     casharr[pos]=cash;unitsarr[pos]=units
     cursor=pos+1
    if cursor<len(mclose):casharr[cursor:]=cash;unitsarr[cursor:]=units
    st['_minute_navclose']=casharr+unitsarr*mclose
   portfolio_close=sleeves['BTC']['_minute_navclose']+sleeves['ETH']['_minute_navclose']
   # Event marks are drawn from each asset's actual fill reference and the other sleeve's as-of holdings.
   event_rows=[]
   for a in ('BTC','ETH'):
    for e in sleeves[a]['event_marks']:
     if e['minute_index']<minute_start or e['minute_index']>minute_end:continue
     pos=e['minute_index']-minute_start;wealth=0.0
     for b in ('BTC','ETH'):
      entries=[z for z in sleeves[b]['event_marks'] if z['minute_index']<=e['minute_index']]
      if entries:
       z=entries[-1];ca=float(dec(z['cash_after']));ua=float(dec(z['units_after']))
      else:ca,ua=1000.0,0.0
      px=float(dec(e['reference'])) if b==a else float(markets[b]['minute_open'][e['minute_index']])
      wealth+=ca+ua*px
     event_rows.append((pos,wealth))
   path=[2000.0];cursor=0
   for pos,wealth in sorted(set(event_rows)):
    if pos>cursor:path.extend(portfolio_close[cursor:pos].tolist())
    if pos==len(portfolio_close):
     path.append(wealth);cursor=pos
    else:
     path.extend([wealth,float(portfolio_close[pos])]);cursor=pos+1
   path.extend(portfolio_close[cursor:].tolist())
   folds=[]
   for i in range(12):
    start_nav=sum((dec(sleeves[a]['fold_nav'][i] if 'fold_nav' in sleeves[a] else '1000') for a in ('BTC','ETH')),D(0))
    end_nav=sum((dec(sleeves[a]['fold_nav'][i+1] if 'fold_nav' in sleeves[a] else '1000') for a in ('BTC','ETH')),D(0))
    folds.append({'fold':i+1,'start_utc':stamp(start_ms+i*30*DAY),'end_exclusive_utc':stamp(start_ms+(i+1)*30*DAY),'start_nav_usdt':str(start_nav),'end_nav_usdt':str(end_nav),'net_return_pct':float(100*(end_nav/start_nav-1))})
   positive=sum(f['net_return_pct']>0 for f in folds)
   net=float(100*(terminal/D(2000)-1));gross=sum((dec(sleeves[a]['gross_reference_pnl_usdt']) for a in ('BTC','ETH')),D(0))
   daily_path=np.concatenate((np.asarray([2000.0]),daily_nav,np.asarray([float(terminal)])))
   daily_returns=daily_path[1:]/daily_path[:-1]-1;daily_std=float(np.std(daily_returns,ddof=1)) if len(daily_returns)>1 else 0.0
   daily_sharpe=float(np.mean(daily_returns)/daily_std*math.sqrt(365)) if daily_std else None
   cagr_pct=((float(terminal)/2000)**(365/360)-1)*100
   sampled_daily_dd=drawdown(daily_path);calmar=cagr_pct/(sampled_daily_dd) if sampled_daily_dd>0 else None
   scene={'terminal_nav_usdt':str(terminal),'net_pnl_usdt':str(terminal-D(2000)),'net_return_pct':net,'cost_usdt':str(cost),'cost_parts_usdt':costparts,'gross_reference_pnl_usdt':str(gross),'gross_to_cost':float(gross/cost) if cost else None,'fills':sum(sleeves[a]['fills'] for a in ('BTC','ETH')),'rejected_orders':sum(sleeves[a]['rejected_orders'] for a in ('BTC','ETH')),'round_trips':sum(sleeves[a]['round_trips'] for a in ('BTC','ETH')),'positive_folds':positive,'daily_sharpe_annualized':daily_sharpe,'cagr_pct':cagr_pct,'daily_sample_drawdown_pct':sampled_daily_dd,'calmar_daily_sampled':calmar,'terminal_units_by_asset':{a:sleeves[a]['terminal_units'] for a in ('BTC','ETH')},'max_drawdown_1m_sampled_pct':drawdown(path),'drawdown_scope':'Synchronized OOS 1-minute archived close marks plus immediate post-fill marks; no intra-minute extrema.','folds':folds,'minute_nav_samples':len(path),'minute_nav_sha256':hashlib.sha256(np.asarray(path,dtype='<f8').tobytes()).hexdigest(),'asset_sleeves':{a:{k:v for k,v in sleeves[a].items() if k not in ('daily_nav','daily_equity','trades','decisions','event_marks','_minute_navclose')} for a in ('BTC','ETH')},'daily_nav_sha256':hashlib.sha256(np.asarray(daily_nav,dtype='<f8').tobytes()).hexdigest()}
   scenes[str(mult)]=scene
  cfg= {'name':row['name'],'spec_path':row['spec'],'fingerprint':registry.fingerprint(spec),'parameters':p,'cost_scenarios':scenes,'role':'candidate'}
  configs[row['name']]=cfg
  print(f"{row['name']} {scenes['1']['net_return_pct']:.4f}%/{scenes['2']['net_return_pct']:.4f}%/{scenes['3']['net_return_pct']:.4f}%",flush=True)
 # 3x3 local sensitivity neighborhood and preregistered gates.
 grid=[x for x in batch]
 for row in batch:
  c=configs[row['name']];p=c['parameters'];neighbors=[]
  for other in batch:
   q=json.loads((ROOT/other['spec']).read_text())['parameters']
   if abs([10,20,40].index(q['channel_entry_lookback_days'])-[10,20,40].index(p['channel_entry_lookback_days']))<=1 and abs([10,20,40].index(q['cmf_lookback_days'])-[10,20,40].index(p['cmf_lookback_days']))<=1:neighbors.append(other['name'])
  frac=sum(configs[x]['cost_scenarios']['3']['net_return_pct']>0 for x in neighbors)/len(neighbors)
  s1,s2,s3=(c['cost_scenarios'][str(k)] for k in (1,2,3));gates={'all_cost_scenes_positive':all(c['cost_scenarios'][str(k)]['net_return_pct']>0 for k in (1,2,3)),'positive_1x_folds':s1['positive_folds'],'positive_1x_folds_at_least_8':s1['positive_folds']>=8,'3x_sampled_drawdown_at_most_25pct':s3['max_drawdown_1m_sampled_pct']<=25,'local_3x_neighbor_positive_fraction':frac,'local_3x_neighbors_at_least_60pct':frac>=.60,'1x_gross_to_cost':s1['gross_to_cost'],'gross_to_cost_at_least_2_5':s1['gross_to_cost'] is not None and s1['gross_to_cost']>=2.5,'zero_rejected_orders':all(c['cost_scenarios'][str(k)]['rejected_orders']==0 for k in (1,2,3)),'terminal_flat':all(D(v)==0 for k in ('1','2','3') for v in c['cost_scenarios'][k]['terminal_units_by_asset'].values())}
  gates['pass']=all(gates[k] for k in ('all_cost_scenes_positive','positive_1x_folds_at_least_8','3x_sampled_drawdown_at_most_25pct','local_3x_neighbors_at_least_60pct','gross_to_cost_at_least_2_5','zero_rejected_orders','terminal_flat'))
  c['sensitivity']={'local_3x_neighbor_positive_fraction':frac,'neighbor_count':len(neighbors),'neighbors':neighbors};c['gates']=gates;c['status']='passed' if gates['pass'] else 'rejected'
 manifest={'plan_sha256':plan_sha,'exchange_info_raw_sha256':sha(ROUND/'exchange_info_raw.json'),'assets':{a:{'source_files':plan['data']['assets'][a],'one_minute_rows':len(markets[a]['minute_ts']),'daily_rows':len(markets[a]['day_ts']),'daily_ohlcv_sha256_f64le':hashlib.sha256(np.column_stack([markets[a][k] for k in ('open','high','low','close','quote_volume')]).astype('<f8').tobytes()).hexdigest()} for a in ('BTC','ETH')}}
 benchmark={'source_report':'research/experiments/20261013T224056Z/report.json','configuration':'hold_360d_BTC_ETH_50_50_monthly_volmanaged','status':'read_only_same_window_reference','scenes':baseline['cost_scenarios']}
 report={'round':ROUND.name,'plan_sha256':plan_sha,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':manifest,'benchmark_read_only':benchmark,'summary':{'candidate_configs':len(configs),'passed':sum(x['status']=='passed' for x in configs.values()),'rejected':sum(x['status']=='rejected' for x in configs.values()),'oos_days':360,'folds':12,'fold_days':30,'cost_scenes':len(configs)*3,'positive_configs_by_cost_multiplier':{str(k):sum(x['cost_scenarios'][str(k)]['net_return_pct']>0 for x in configs.values()) for k in (1,2,3)},'ranked_by_1x_net_return':sorted(configs,key=lambda n:configs[n]['cost_scenarios']['1']['net_return_pct'],reverse=True)},'configs':configs}
 write_json(ROUND/'report.json',report)
 for filename,rows in [('trades.csv',all_trades),('decisions.csv',all_decisions),('daily_equity.csv',all_daily)]:
  keys=sorted({k for x in rows for k in x})
  with (ROUND/filename).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');w.writeheader();w.writerows(rows)
 print(json.dumps(report['summary'],ensure_ascii=False),flush=True)
if __name__=='__main__':main()
