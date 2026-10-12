#!/usr/bin/env python3
"""Evaluate pre-reserved BTC/ETH 4h volume-confirmed momentum on Binance 1m history."""
from __future__ import annotations
import gzip, hashlib, importlib.util, json, math, statistics, sys
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np, polars as pl
ROOT=Path(__file__).resolve().parents[3]; ROUND=Path(__file__).resolve().parent
MIN=60_000_000_000; H4=240*MIN; DAY=1440*MIN
sys.path.insert(0,str(ROOT/'research/automation')); import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
from kernel import fill
# Existing frozen market filter and lagged daily-cost implementation.
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m
engine=load('r51_daily_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ns): return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def canon(x): return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def gzwrite(path,x):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as g:g.write(json.dumps(canon(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())

def load_asset(asset):
 paths=[ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
 parts=[]; manifest=[]
 for p in paths:
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all()
  assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all()
  manifest.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'bars':f.height,'first_open_ns':int(f['open_ts'][0]),'last_open_ns':int(f['open_ts'][-1])})
  parts.append(f)
 m=pl.concat(parts,how='vertical_relaxed').sort('open_ts'); assert m.height==730*1440 and (m['open_ts'].diff().drop_nulls()==MIN).all()
 # NumPy minute-close marks; Decimal bar values retained separately for signal/fill references.
 opens=m['open'].to_list(); closes=m['close'].to_list(); qv=m['quote_volume'].to_list(); bv=m['base_volume'].to_list(); ts=m['open_ts'].to_numpy(); closef=m['close'].cast(pl.Float64).to_numpy()
 assert int(ts[0])==1726444800000000000 and int(ts[-1])==int(ts[0])+(len(ts)-1)*MIN
 nbars=len(ts)//240; assert nbars==4380
 bars=[{'open_ts':int(ts[j*240]),'available_ts':int(ts[(j+1)*240-1])+MIN,'close':D(str(closes[(j+1)*240-1])),'quote_volume':sum((D(str(x)) for x in qv[j*240:(j+1)*240]),D(0))} for j in range(nbars)]
 daily=[]
 for d in range(730):
  ix=(d+1)*1440-1
  daily.append({'close':D(str(closes[ix])),'quote_volume':sum((D(str(x)) for x in qv[d*1440:(d+1)*1440]),D(0))})
 assert stamp(bars[0]['open_ts'])=='2024-09-16T00:00:00Z' and stamp(bars[-1]['available_ts'])=='2026-09-16T00:00:00Z'
 assert all(bars[j]['available_ts']<=bars[j+1]['open_ts'] for j in range(nbars-1))
 # The 5m execution-price estimate at trade i uses five closed minutes through block boundary.
 proxy=[]
 for i in range(nbars+1):
  mi=i*240+1
  if mi<5: proxy.append(D(0)); continue
  q=sum((D(str(x)) for x in qv[mi-5:mi]),D(0)); b=sum((D(str(x)) for x in bv[mi-5:mi]),D(0)); proxy.append(q/b if b else D(0))
 return {'asset':asset,'minute_open':opens,'minute_close':closef,'minute_ts':ts,'minute_quote':qv,'minute_base':bv,'bars':bars,'daily':daily,'proxy':proxy,'manifest':manifest,
  'daily_close_sha256_f64le':hashlib.sha256(np.asarray([float(x['close']) for x in daily],dtype='<f8').tobytes()).hexdigest(),
  'bar_close_sha256_f64le':hashlib.sha256(np.asarray([float(x['close']) for x in bars],dtype='<f8').tobytes()).hexdigest()}

def dd(values):
 a=np.asarray(values,dtype=np.float64); peaks=np.maximum.accumulate(a); ratios=1-a/peaks; j=int(np.argmax(ratios)); return float(ratios[j]*100),int(np.argmax(a[:j+1])),j

def metrics(nav, bars_per_year=365):
 x=np.asarray(nav,dtype=np.float64); assert len(x)>1 and np.all(np.isfinite(x)) and np.all(x>0)
 rets=x[1:]/x[:-1]-1; sd=float(np.std(rets,ddof=1)) if len(rets)>1 else 0.; d,pi,ti=dd(x)
 cagr=(float(x[-1])/float(x[0]))**(bars_per_year/(len(x)-1))-1 if len(x)>1 else 0
 return {'net_return_pct':float((x[-1]/x[0]-1)*100),'max_drawdown_pct':d,'sharpe_annualized':float(np.mean(rets)/sd*math.sqrt(bars_per_year)) if sd else None,'cagr_pct':cagr*100,'calmar':cagr/(d/100) if d else None,'drawdown_peak_index':pi,'drawdown_trough_index':ti,'observations':len(x)-1}

def summarize(assetdata, trades, daynav, terminal_nav, multiplier, start, end):
 # Caller supplies one-minute closes plus immediate post-fill reference marks.
 minutevals=trades[-1].pop('_minute_nav')
 daynav[-1]=float(terminal_nav)
 mm=metrics(minutevals,365*1440); dm=metrics(daynav,365)
 fills=[t for t in trades if t.get('status')=='filled' and t.get('side') in ('buy','sell')]
 parts={k:str(sum((D(t['cost_parts'][k]) for t in fills),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
 cost=sum((D(v) for v in parts.values()),D(0)); gross=D(str(terminal_nav))-D('2000')+cost
 folds=[]
 close_indices=trades[-1].pop('_close_indices')
 for j in range(12):
  fold_start=start+j*180; fold_end=start+(j+1)*180
  a=0 if j==0 else close_indices[fold_start*240-1]
  b=len(minutevals)-1 if j==11 else close_indices[fold_end*240-1]
  f=metrics(minutevals[a:b+1],365*1440)
  folds.append({'fold':j+1,'test_start_utc':stamp(assetdata['bars'][start+j*180]['open_ts']),'test_end_exclusive_utc':stamp(assetdata['bars'][start+(j+1)*180]['open_ts']),**f})
 return {'net_PnL_usdt':str(D(str(terminal_nav))-D('2000')),'terminal_NAV_usdt':str(terminal_nav),'terminal_cash_usdt':str(trades[-1]['terminal_cash']),'terminal_units':str(trades[-1]['terminal_units']),'net_return_pct':mm['net_return_pct'],'daily_mark_drawdown_pct':dm['max_drawdown_pct'],'max_drawdown_pct':mm['max_drawdown_pct'],'drawdown_scope':'OOS one-minute bar-close samples plus immediate post-fill reference marks; no within-minute extrema.','sharpe_annualized_minute_sample':mm['sharpe_annualized'],'cagr_pct_daily':dm['cagr_pct'],'calmar_daily':dm['calmar'],'cost_usdt':str(cost),'cost_parts_usdt':parts,'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,'attempts':len(trades)-1,'executions':len(fills),'round_trips':sum(t['side']=='sell' for t in fills),'rejected_orders':sum(t.get('status')!='filled' for t in trades[:-1]),'balance_violations':sum(D(t.get('cash_after','0'))<0 or D(t.get('units_after','0'))<0 for t in trades[:-1]),'folds':folds,'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(minutevals,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(minutevals),'cost_multiplier':multiplier}

def run_one(spec, market, filters, multiplier, comparator=False):
 p=spec['parameters']; start=int(p['oos_start_bar_index']); end=int(p['oos_end_exclusive_bar_index']); bars=market['bars']; daily=market['daily']
 assert start==2208 and end==4368 and end<len(bars)
 closes=[b['close'] for b in bars]; capital=D('2000'); cash=capital; units=D(0); desired=False; trades=[]; decisions=[]
 # Continuous OOS daily and minute sampled NAV, starting flat. Use only completed candles for signals.
 start_min=start*240+1; end_min=end*240+1
 navstream=[float(capital)]; daynav=[float(capital)]; close_indices={}
 decision_at={}
 for i in range(start,end):
  if comparator:
   action='buy' if i==start else None
  else:
   lb=int(p['lookback_4h_bars']); j=i-1
   mom=closes[j]/closes[j-lb]-1
   slot=j%6; hist=[bars[j-6*k]['quote_volume'] for k in range(1,21)]
   mean=sum(hist,D(0))/D(len(hist)); ratio=bars[j]['quote_volume']/mean if mean>0 else D(0)
   before=desired
   if desired and mom<=0: desired=False
   elif not desired and mom>0 and ratio>=D(str(p['same_slot_quote_volume_ratio_min'])): desired=True
   action='buy' if desired and units==0 else ('sell' if not desired and units>0 else None)
   decisions.append({'bar_index':i,'signal_bar_index':j,'signal_close_available_utc':stamp(bars[j]['available_ts']),'execution_utc':stamp(bars[i]['open_ts']+MIN),'momentum_fraction':str(mom),'same_slot_quote_volume_ratio':str(ratio),'desired_before':before,'desired_after':desired,'action':action})
  if action:
   trade_day=i//6; trade_ts=bars[i]['open_ts']+MIN; trade_min=i*240+1
   # Cost inputs use only completed UTC daily bars before trade day.
   adv,sigma=engine.lagged_cost_inputs(daily,trade_day)
   ref=D(str(market['minute_open'][trade_min])); avg=market['proxy'][i]
   cash,units,tr=fill(cash,units,action=='buy',ref,D(str(adv)),D(str(sigma)),multiplier,filters,avg)
   tr.update({'bar_index':i,'signal_bar_index':i-1,'signal_available_utc':stamp(bars[i-1]['available_ts']),'execution_utc':stamp(trade_ts),'signal_to_execution_seconds':(trade_ts-bars[i-1]['available_ts'])/1e9,'reference_utc':stamp(trade_ts),'terminal':False,'cash_after':str(cash),'units_after':str(units)})
   trades.append(tr)
   decision_at[trade_min]=(cash,units)
 # Terminal sell at the next executable bar after end, all costed.
 i=end; trade_day=i//6; trade_ts=bars[i]['open_ts']+MIN; trade_min=i*240+1
 adv,sigma=engine.lagged_cost_inputs(daily,trade_day); ref=D(str(market['minute_open'][trade_min])); avg=market['proxy'][i]
 if comparator and units==0:
  cash,units,tr=fill(cash,units,True,ref,D(str(adv)),D(str(sigma)),multiplier,filters,avg); tr.update({'bar_index':start,'signal_bar_index':None,'signal_available_utc':None,'execution_utc':stamp(bars[start]['open_ts']+MIN),'signal_to_execution_seconds':None,'terminal':False,'cash_after':str(cash),'units_after':str(units)}); trades.insert(0,tr); decision_at[start*240+1]=(cash,units)
 terminal_ref=ref
 if units>0:
  cash,units,tr=fill(cash,units,False,terminal_ref,D(str(adv)),D(str(sigma)),multiplier,filters,avg)
  tr.update({'bar_index':end,'signal_bar_index':end-1,'signal_available_utc':stamp(bars[end-1]['available_ts']),'execution_utc':stamp(trade_ts),'signal_to_execution_seconds':(trade_ts-bars[end-1]['available_ts'])/1e9,'terminal':True,'cash_after':str(cash),'units_after':str(units)})
  trades.append(tr)
 # Add terminal event for deterministic accounting/reporting, even when flat.
 trades.append({'side':'terminal_state','status':'filled','terminal_cash':str(cash),'terminal_units':str(units),'cash_after':str(cash),'units_after':str(units),'_minute_nav':None})
 terminal_nav=cash+units*terminal_ref
 # Build minute NAV marks applying each attempt before its execution-minute close.
 events=sorted((int(t['bar_index'])*240+1,t,D(t['cash_after']),D(t['units_after'])) for t in trades[:-1] if t.get('side') in ('buy','sell'))
 event_i=0; cash_at=capital; units_at=D(0)
 for mi in range(start_min,end_min):
  while event_i<len(events) and events[event_i][0]==mi:
   _,t,cash_at,units_at=events[event_i]
   navstream.append(float(cash_at+units_at*D(str(t['reference']))))
   event_i+=1
  navstream.append(float(cash_at+units_at*D(str(market['minute_close'][mi]))))
  close_indices[mi]=len(navstream)-1
 while event_i<len(events) and events[event_i][0]==end_min:
  _,t,cash_at,units_at=events[event_i]
  navstream.append(float(cash_at+units_at*D(str(t['reference']))))
  event_i+=1
 if len(navstream)==1 or close_indices.get(end_min-1)!=len(navstream)-1:
  navstream.append(float(cash_at+units_at*terminal_ref))
 terminal_nav=cash_at+units_at*terminal_ref
 # Daily marks use the last closed minute before each successive UTC 00:01 mark.
 for d in range(1,361):
  mi=start_min+d*1440-1
  daynav.append(navstream[close_indices[mi]])
 # make the internal marker available only to summarize; preserve a clean ledger below.
 trades[-1]['_minute_nav']=navstream; trades[-1]['_close_indices']=close_indices
 result=summarize(market,trades,daynav,terminal_nav,multiplier,start,end)
 clean_trades=[{k:v for k,v in t.items() if k!='_minute_nav'} for t in trades[:-1]]
 archive={'name':spec['name'],'fingerprint':registry.fingerprint(spec),'spec':spec,'decisions':decisions,'trades':clean_trades,'daily_nav_usdt':daynav,'summary':result}
 return archive

def main():
 plan=json.loads((ROUND/'spec.json').read_text()); batch=json.loads((ROUND/'batch.json').read_text())
 source=json.loads((ROOT/'research/experiments/20261012T035429Z/report.json').read_text()); filters=source['plan']['execution']['filters']
 markets={a:load_asset(a) for a in ('BTC','ETH')}
 manifest={'built_utc':'2026-10-12T10:00:10Z','assets':{a:{'source_files':markets[a]['manifest'],'bars_4h':len(markets[a]['bars']),'first_4h_open_utc':stamp(markets[a]['bars'][0]['open_ts']),'last_4h_available_utc':stamp(markets[a]['bars'][-1]['available_ts']),'bar_close_sha256_f64le':markets[a]['bar_close_sha256_f64le'],'daily_close_sha256_f64le':markets[a]['daily_close_sha256_f64le']} for a in markets},'filters_source_sha256':sha(ROOT/'research/experiments/20261012T035429Z/report.json')}
 (ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 summaries={}; results=[]
 out=ROOT/'data/runs'/ROUND.name; out.mkdir(parents=True,exist_ok=True)
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text()); a=row['asset']; summaries[row['name']]={}
  for mult in (1,2,3):
   archive=run_one(spec,markets[a],filters[a+'USDT'],mult,row['is_comparator'])
   summaries[row['name']][str(mult)]=archive['summary']
   gzwrite(out/f"{row['name']}_cost{mult}.json.gz",archive)
   results.append({'name':row['name'],'asset':a,'cost_multiplier':mult,'is_comparator':row['is_comparator'],**archive['summary']})
  print(f"finished {row['name']}: {summaries[row['name']]['1']['net_return_pct']:.4f}% / {summaries[row['name']]['3']['net_return_pct']:.4f}%",flush=True)
 # Neighborhood fractions are evaluated over the fixed 3x grid within each asset.
 for row in batch:
  if row['is_comparator']: continue
  a=row['asset']; spec=json.loads((ROOT/row['spec']).read_text()); p=spec['parameters']
  neighbors=[x for x in batch if not x['is_comparator'] and x['asset']==a and abs(json.loads((ROOT/x['spec']).read_text())['parameters']['lookback_4h_bars']-p['lookback_4h_bars'])<=12 and abs(json.loads((ROOT/x['spec']).read_text())['parameters']['same_slot_quote_volume_ratio_min']-p['same_slot_quote_volume_ratio_min'])<=0.25]
  frac=sum(summaries[x['name']]['3']['net_return_pct']>0 for x in neighbors)/len(neighbors)
  summaries[row['name']]['3']['neighborhood_positive_fraction']=frac
  summaries[row['name']]['3']['neighborhood_size']=len(neighbors)
  g=summaries[row['name']]['1']['gross_reference_pnl_to_cost']
  positive=sum(f['net_return_pct']>0 for f in summaries[row['name']]['1']['folds'])
  gates={'all_costs_positive':all(summaries[row['name']][str(m)]['net_return_pct']>0 for m in (1,2,3)),'positive_1x_folds':positive,'drawdown_under_25pct':summaries[row['name']]['3']['max_drawdown_pct']<=25,'neighborhood_fraction_at_least_0_60':frac>=.6,'round_trips_at_least_2':summaries[row['name']]['1']['round_trips']>=2,'gross_to_cost_at_least_2_5':g is not None and g>=2.5,'no_balance_violations':all(summaries[row['name']][str(m)]['balance_violations']==0 for m in (1,2,3)),'terminal_flat':all(D(summaries[row['name']][str(m)]['terminal_units'])==0 for m in (1,2,3))}
  summaries[row['name']]['gates']=gates; summaries[row['name']]['status']='passed' if all([gates['all_costs_positive'],positive>=7,gates['drawdown_under_25pct'],gates['neighborhood_fraction_at_least_0_60'],gates['round_trips_at_least_2'],gates['gross_to_cost_at_least_2_5'],gates['no_balance_violations'],gates['terminal_flat']]) else 'rejected'
 # Consolidated report: candidate configs sorted by 1x net return; all variants and comparators retained.
 cfgs={}
 for row in batch:
  cfgs[row['name']]={'asset':row['asset'],'spec':row['spec'],'fingerprint':row['fingerprint'],'is_comparator':row['is_comparator'],'cost_scenarios':summaries[row['name']]}
 report={'round':ROUND.name,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':manifest,'summary':{'candidate_configs':18,'comparators':2,'candidate_rejected':sum(cfgs[x['name']]['cost_scenarios']['status']=='rejected' for x in batch if not x['is_comparator']),'candidate_passed':sum(cfgs[x['name']]['cost_scenarios']['status']=='passed' for x in batch if not x['is_comparator']),'oos_days':360,'folds':12,'candidates_ranked_by_1x_net_return':sorted([x['name'] for x in batch if not x['is_comparator']],key=lambda n:cfgs[n]['cost_scenarios']['1']['net_return_pct'],reverse=True)},'configs':cfgs,'all_cost_scene_rows':results}
 (ROUND/'report.json').write_text(json.dumps(canon(report),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 print(json.dumps(report['summary'],ensure_ascii=False),flush=True)
if __name__=='__main__': main()
