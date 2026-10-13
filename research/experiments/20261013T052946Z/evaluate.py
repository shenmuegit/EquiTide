#!/usr/bin/env python3
"""Evaluate the frozen hourly first-half continuation grid on Binance 1m bars."""
from __future__ import annotations
import gzip, hashlib, importlib.util, json, math, statistics, sys
from datetime import datetime, timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np
import polars as pl

ROOT=Path(__file__).resolve().parents[3]; ROUND=Path(__file__).resolve().parent
MIN_NS=60_000_000_000; DAY_MIN=1440; HOUR_MIN=60
sys.path.insert(0,str(ROOT/'research/automation')); import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
from kernel import fill
def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
cost_engine=loadmod('hhr_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp_ns(ns):return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def safe(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def write_gz(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as g:g.write(json.dumps(safe(obj),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())

def source_paths(asset):
 return [ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
def load_market(asset):
 parts=[];manifest=[]
 for p in source_paths(asset):
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN_NS).all()
  assert (f['available_ts']-f['open_ts']==MIN_NS).all()
  manifest.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p),'bars':f.height,'first_open_utc':stamp_ns(int(f['open_ts'][0])),'last_open_utc':stamp_ns(int(f['open_ts'][-1]))})
  parts.append(f)
 f=pl.concat(parts,how='vertical_relaxed').sort('open_ts')
 assert f.height==730*DAY_MIN and (f['open_ts'].diff().drop_nulls()==MIN_NS).all()
 opens=np.asarray(f['open'].cast(pl.Float64).to_numpy(),dtype=np.float64)
 closes=np.asarray(f['close'].cast(pl.Float64).to_numpy(),dtype=np.float64)
 qv=np.asarray(f['quote_volume'].cast(pl.Float64).to_numpy(),dtype=np.float64)
 bv=np.asarray(f['base_volume'].cast(pl.Float64).to_numpy(),dtype=np.float64)
 ts=f['open_ts'].to_numpy()
 # UTC daily cost inputs use only closed rows, independently aggregated from the same source.
 daily=[]
 for d in range(730):
  a=d*DAY_MIN;b=a+DAY_MIN
  daily.append({'close':D(str(closes[b-1])),'quote_volume':D(str(float(qv[a:b].sum())))})
 # First-half quote volume by day/hour; ratio references the preceding 20 whole days only.
 first_qv=np.empty((730,24),dtype=np.float64)
 hour_ret=np.empty((730,24),dtype=np.float64)
 for d in range(730):
  daybase=d*DAY_MIN
  for h in range(24):
   m=daybase+h*HOUR_MIN
   first_qv[d,h]=qv[m:m+30].sum()
   hour_ret[d,h]=closes[m+29]/opens[m]-1.0
 slot_ratio=np.full((730,24),np.nan,dtype=np.float64)
 for d in range(20,730):
  slot_ratio[d]=first_qv[d-20:d].mean(axis=0)
 # Five-minute VWAP proxy ending immediately before each possible execution minute.
 proxy=np.zeros(len(opens),dtype=np.float64)
 for mi in range(5,len(opens)):
  qb=float(qv[mi-5:mi].sum());bb=float(bv[mi-5:mi].sum());proxy[mi]=qb/bb if bb else 0.0
 assert stamp_ns(int(ts[0]))=='2024-09-16T00:00:00Z' and stamp_ns(int(ts[-1]))=='2026-09-15T23:59:00Z'
 return {'asset':asset,'opens':opens,'closes':closes,'qv':qv,'bv':bv,'ts':ts,'daily':daily,'first_qv':first_qv,'hour_ret':hour_ret,'slot_mean':slot_ratio,'proxy':proxy,'manifest':manifest}

def dd_metrics(vals,periods_per_year):
 a=np.asarray(vals,dtype=np.float64)
 if len(a)<2 or not np.isfinite(a).all() or (a<=0).any():raise ValueError('invalid NAV vector')
 peaks=np.maximum.accumulate(a);drops=1-a/peaks;tr=int(np.argmax(drops));pk=int(np.argmax(a[:tr+1]))
 r=a[1:]/a[:-1]-1;sd=float(r.std(ddof=1)) if len(r)>1 else 0.
 sharpe=float(r.mean()/sd*math.sqrt(periods_per_year)) if sd else None
 cagr=(a[-1]/a[0])**(periods_per_year/(len(a)-1))-1
 return {'net_return_pct':float((a[-1]/a[0]-1)*100),'max_drawdown_pct':float(drops[tr]*100),'sharpe_annualized':sharpe,'cagr_pct':float(cagr*100),'calmar':float(cagr/(drops[tr])) if drops[tr] else None,'drawdown_peak_index':pk,'drawdown_trough_index':tr,'observations':len(a)-1}

def signal_events(spec,market,start_day,end_day,filters):
 p=spec['parameters'];events=[]
 for d in range(start_day,end_day):
  daybase=d*DAY_MIN
  for h in range(24):
   mean=float(market['slot_mean'][d,h])
   if not math.isfinite(mean) or mean<=0:continue
   ret=float(market['hour_ret'][d,h]);ratio=float(market['first_qv'][d,h]/mean)
   if ret>float(p['first_half_return_threshold']) and ratio>=float(p['same_slot_quote_volume_ratio_min']):
    entry=daybase+h*HOUR_MIN+31;exit=daybase+h*HOUR_MIN+61
    # Exact causal schedule. Last scheduled window may end at the common terminal execution.
    if entry<start_day*DAY_MIN+1 or exit>end_day*DAY_MIN+1:continue
    events.append({'signal_minute':daybase+h*HOUR_MIN+29,'signal_available_minute':daybase+h*HOUR_MIN+30,'entry_minute':entry,'scheduled_exit_minute':exit,'return_fraction':ret,'same_slot_volume_ratio':ratio})
 return events

def run_scene(spec,market,filters,mult,is_comparator=False):
 p=spec['parameters'];start_day=368;end_day=728;start_min=start_day*DAY_MIN;end_min=end_day*DAY_MIN+2
 capital=D('2000');cash=capital;units=D(0);trades=[];events=[] if is_comparator else signal_events(spec,market,start_day,end_day,filters)
 if is_comparator: events=[{'signal_minute':None,'signal_available_minute':None,'entry_minute':start_min+1,'scheduled_exit_minute':end_min,'return_fraction':None,'same_slot_volume_ratio':None}]
 evix=0;held_exit=None;attempts=0;rejected=0;capacity_rejections=0;balance_violations=0
 minute_nav=[float(capital)];minute_times=[int(market['ts'][start_min])];daily_nav=[float(capital)];daily_times=[int(market['ts'][start_min])]
 # At each minute open, first process scheduled/continuing exits, then signals that were available earlier.
 for mi in range(start_min+1,end_min):
  filled_at_open=False
  if units>0 and held_exit is not None and mi>=held_exit:
   adv,sigma=cost_engine.lagged_cost_inputs(market['daily'],mi//DAY_MIN)
   ref=D(str(market['opens'][mi]));avg=D(str(market['proxy'][mi]))
   cash,units,tr=fill(cash,units,False,ref,D(str(adv)),D(str(sigma)),mult,filters,avg);attempts+=1
   tr.update({'execution_minute':mi,'execution_utc':stamp_ns(int(market['ts'][mi])),'reference_utc':stamp_ns(int(market['ts'][mi])),'scheduled_exit_minute':held_exit,'terminal':mi>=end_min-1,'cost_multiplier':mult})
   trades.append(tr)
   if tr['status']=='filled':held_exit=None;filled_at_open=True
   else:
    rejected+=1
    if tr.get('reason')=='participation':capacity_rejections+=1
    held_exit=mi+1
   if cash<0 or units<0:balance_violations+=1
  while evix<len(events) and events[evix]['entry_minute']==mi:
   e=events[evix]
   if units==0 and held_exit is None:
    adv,sigma=cost_engine.lagged_cost_inputs(market['daily'],mi//DAY_MIN)
    ref=D(str(market['opens'][mi]));avg=D(str(market['proxy'][mi]))
    cash,units,tr=fill(cash,units,True,ref,D(str(adv)),D(str(sigma)),mult,filters,avg);attempts+=1
    signal_available_utc=stamp_ns(int(market['ts'][e['signal_available_minute']])) if e['signal_available_minute'] is not None else None
    signal_utc=stamp_ns(int(market['ts'][e['signal_minute']])) if e['signal_minute'] is not None else None
    tr.update({'signal_minute':e['signal_minute'],'signal_available_utc':signal_available_utc,'signal_utc':signal_utc,'execution_minute':mi,'execution_utc':stamp_ns(int(market['ts'][mi])),'signal_to_execution_seconds':60 if signal_available_utc else None,'reference_utc':stamp_ns(int(market['ts'][mi])),'signal_first_half_return':e['return_fraction'],'same_slot_volume_ratio':e['same_slot_volume_ratio'],'scheduled_exit_minute':e['scheduled_exit_minute'],'terminal':False})
    trades.append(tr)
    if tr['status']=='filled':held_exit=e['scheduled_exit_minute'];filled_at_open=True
    else:
     rejected+=1
     if tr.get('reason')=='participation':capacity_rejections+=1
    if cash<0 or units<0:balance_violations+=1
   evix+=1
  # immediate reference mark after any fills at this open, then the closed one-minute bar mark.
  if filled_at_open:
   v=float(cash+units*D(str(market['opens'][mi])));minute_nav.append(v);minute_times.append(int(market['ts'][mi]))
  mark=float(cash)+float(units)*float(market['closes'][mi]);minute_nav.append(mark);minute_times.append(int(market['ts'][mi])+MIN_NS)
  if (mi+1-start_min)%DAY_MIN==0:
   daily_nav.append(mark);daily_times.append(int(market['ts'][mi])+MIN_NS)
 # force terminal close at the frozen 00:01 open; all prior scheduled exit retries have had their minute.
 terminal_min=end_min-1
 already_attempted_terminal=any(t.get('execution_minute')==terminal_min and t.get('side')=='sell' for t in trades)
 if units>0 and not already_attempted_terminal:
  adv,sigma=cost_engine.lagged_cost_inputs(market['daily'],terminal_min//DAY_MIN)
  ref=D(str(market['opens'][terminal_min]));avg=D(str(market['proxy'][terminal_min]))
  cash,units,tr=fill(cash,units,False,ref,D(str(adv)),D(str(sigma)),mult,filters,avg);attempts+=1
  tr.update({'execution_minute':terminal_min,'execution_utc':stamp_ns(int(market['ts'][terminal_min])),'reference_utc':stamp_ns(int(market['ts'][terminal_min])),'terminal':True,'cost_multiplier':mult})
  trades.append(tr)
  if tr['status']!='filled':rejected+=1
  if cash<0 or units<0:balance_violations+=1
 terminal_nav=float(cash+units*D(str(market['opens'][terminal_min])))
 if units!=0: # a filter rejection at terminal is retained as a failed liquidation, never hidden.
  terminal_flat=False
 else:terminal_flat=True
 if not daily_nav or daily_times[-1]<int(market['ts'][end_min-2])+MIN_NS:
  daily_nav.append(terminal_nav);daily_times.append(int(market['ts'][end_min-1]))
 else:
  daily_nav[-1]=terminal_nav;daily_times[-1]=int(market['ts'][end_min-1])
 nav_stats=dd_metrics(minute_nav,365*1440) if minute_nav else dd_metrics([float(capital),terminal_nav],365)
 day_stats=dd_metrics(daily_nav,365)
 fills=[t for t in trades if t['status']=='filled']
 parts={k:str(sum((D(t['cost_parts'][k]) for t in fills),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')}
 total_cost=sum((D(v) for v in parts.values()),D(0));net=D(str(terminal_nav))-capital
 gross=net+total_cost
 folds=[]
 # Start boundary then 12 contiguous 30-day boundary marks.
 for f in range(12):
  i=f*30; j=(f+1)*30
  vals=daily_nav[i:j+1]
  folds.append({'fold':f+1,'test_start_utc':stamp_ns(daily_times[i]),'test_end_exclusive_utc':stamp_ns(daily_times[j]),**dd_metrics(vals,365)})
 round_trips=sum(t['side']=='sell' and t['status']=='filled' for t in trades)
 summary={'net_PnL_usdt':str(net),'terminal_NAV_usdt':str(terminal_nav),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_flat':terminal_flat,
  'net_return_pct':nav_stats['net_return_pct'],'max_drawdown_pct':nav_stats['max_drawdown_pct'],'drawdown_scope':'OOS one-minute closes plus immediate post-fill reference marks; does not include within-minute extrema.',
  'daily_mark_drawdown_pct':day_stats['max_drawdown_pct'],'sharpe_annualized_daily':day_stats['sharpe_annualized'],'cagr_pct_daily':day_stats['cagr_pct'],'calmar_daily':day_stats['calmar'],
  'cost_usdt':str(total_cost),'cost_parts_usdt':parts,'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/total_cost) if total_cost else None,
  'signals':len(events),'attempts':attempts,'executions':len(fills),'round_trips':round_trips,'rejected_orders':rejected,'capacity_rejections':capacity_rejections,'balance_violations':balance_violations,
  'folds':folds,'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(daily_nav,dtype='<f8').tobytes()).hexdigest(),'daily_nav_samples':len(daily_nav),
  'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(minute_nav,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(minute_nav),'cost_multiplier':mult}
 return {'summary':summary,'trades':trades,'daily_nav_usdt':daily_nav,'daily_nav_utc':list(map(stamp_ns,daily_times)),'minute_nav_usdt':minute_nav,'minute_nav_utc_ns':minute_times,'minute_nav_hash':summary['minute_nav_sha256_f64le']}

def main():
 plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text())
 src=json.loads((ROOT/'research/experiments/20261012T035429Z/report.json').read_text());filters=src['plan']['execution']['filters']
 markets={a:load_market(a) for a in ('BTC','ETH')};start=368*DAY_MIN;end=728*DAY_MIN
 mfest={'built_utc':datetime.now(timezone.utc).isoformat(),'assets':{a:{'source_files':markets[a]['manifest'],'bars_1m':len(markets[a]['ts']),'first_open_utc':stamp_ns(int(markets[a]['ts'][0])),'last_open_utc':stamp_ns(int(markets[a]['ts'][-1])),'hourly_first_half_returns_sha256_f64le':hashlib.sha256(np.asarray(markets[a]['hour_ret'],dtype='<f8').tobytes()).hexdigest(),'first_half_quote_volume_sha256_f64le':hashlib.sha256(np.asarray(markets[a]['first_qv'],dtype='<f8').tobytes()).hexdigest()} for a in markets},'filter_source_sha256':sha(ROOT/'research/experiments/20261012T035429Z/report.json')}
 (ROUND/'data_manifest.json').write_text(json.dumps(mfest,indent=2)+'\n')
 out=ROOT/'data/runs'/ROUND.name;out.mkdir(parents=True,exist_ok=True)
 all_results=[]; summaries={}
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());asset=row['asset'];market=markets[asset];sc={};archives={}
  for mult in (1,2,3):
   archive=run_scene(spec,market,filters[asset+'USDT'],mult,row['is_comparator']);sc[str(mult)]=archive['summary'];archives[str(mult)]=archive
   nav_path=out/f"{row['name']}_cost{mult}_nav.npz"
   np.savez_compressed(nav_path,nav_usdt=np.asarray(archive.pop('minute_nav_usdt'),dtype='<f8'),timestamp_utc_ns=np.asarray(archive.pop('minute_nav_utc_ns'),dtype='<i8'))
   sc[str(mult)]['minute_nav_archive']=str(nav_path.relative_to(ROOT));sc[str(mult)]['minute_nav_archive_sha256']=sha(nav_path)
   all_results.append({'name':row['name'],'asset':asset,'cost_multiplier':mult,'is_comparator':row['is_comparator'],**archive['summary']})
   print(f"scene {row['name']} x{mult}: {archive['summary']['net_return_pct']:.5f}% trips={archive['summary']['round_trips']} reject={archive['summary']['rejected_orders']}",flush=True)
  summaries[row['name']]={'scenarios':sc,'archives':archives,'row':row,'spec':spec}
 # Predetermined adjacent 3x grid robustness on parameter-neighbor cells (Manhattan distance one grid step).
 for name,info in summaries.items():
  if info['row']['is_comparator']:continue
  p=info['spec']['parameters'];asset=info['row']['asset'];neighbors=[]
  for n,j in summaries.items():
   if j['row']['is_comparator'] or j['row']['asset']!=asset:continue
   q=j['spec']['parameters'];di=abs(float(p['first_half_return_threshold'])-float(q['first_half_return_threshold']))<=0.0005+1e-12;dv=abs(float(p['same_slot_quote_volume_ratio_min'])-float(q['same_slot_quote_volume_ratio_min']))<=0.25+1e-12
   if di and dv:neighbors.append(n)
  frac=sum(summaries[n]['scenarios']['3']['net_return_pct']>0 for n in neighbors)/len(neighbors)
  sc=info['scenarios'];one=sc['1'];three=sc['3'];positive_folds=sum(f['net_return_pct']>0 for f in one['folds'])
  gates={'all_costs_positive':all(sc[str(m)]['net_return_pct']>0 for m in (1,2,3)),'positive_1x_folds_at_least_8_of_12':positive_folds>=8,
   '3x_drawdown_at_most_25pct':three['max_drawdown_pct']<=25,'adjacent_3x_positive_fraction_at_least_0_60':frac>=.60,
   '1x_round_trips_at_least_250':one['round_trips']>=250,'1x_gross_to_cost_at_least_2_5':one['gross_reference_pnl_to_cost'] is not None and one['gross_reference_pnl_to_cost']>=2.5,
   'no_order_rejections':all(sc[str(m)]['rejected_orders']==0 for m in (1,2,3)),'no_balance_violations':all(sc[str(m)]['balance_violations']==0 for m in (1,2,3)),
   'terminal_flat':all(sc[str(m)]['terminal_flat'] for m in (1,2,3))}
  sc['gates']=gates;sc['adjacent_3x_positive_fraction']=frac;sc['adjacent_3x_neighbor_count']=len(neighbors);sc['positive_1x_folds']=positive_folds
  sc['status']='passed' if all(gates.values()) else 'rejected'
 # Output compact light report; full event ledgers are gzip data-run archives (ignored by git).
 configs={}
 for name,info in summaries.items():
  configs[name]={'asset':info['row']['asset'],'spec':info['row']['spec'],'fingerprint':info['row']['fingerprint'],'is_comparator':info['row']['is_comparator'],'scenarios':info['scenarios']}
  for mult,archive in info['archives'].items():write_gz(out/f'{name}_cost{mult}.json.gz',{'name':name,'asset':info['row']['asset'],'cost_multiplier':int(mult),'spec':info['spec'],'summary':archive['summary'],'trades':archive['trades'],'daily_nav_usdt':archive['daily_nav_usdt'],'daily_nav_utc':archive['daily_nav_utc']})
 report={'round':ROUND.name,'evaluation_started_utc':mfest['built_utc'],'plan':plan,'data_manifest':mfest,
  'summary':{'candidate_configs':18,'comparators':2,'candidate_passed':sum(configs[x['name']]['scenarios']['status']=='passed' for x in batch if not x['is_comparator']),'candidate_rejected':sum(configs[x['name']]['scenarios']['status']=='rejected' for x in batch if not x['is_comparator']),'oos_days':360,'folds':12,
   'candidates_ranked_by_1x_return':sorted([x['name'] for x in batch if not x['is_comparator']],key=lambda n:configs[n]['scenarios']['1']['net_return_pct'],reverse=True)},'configs':configs,'all_cost_scene_rows':all_results}
 (ROUND/'report.json').write_text(json.dumps(safe(report),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 print(json.dumps(report['summary'],ensure_ascii=False),flush=True)
if __name__=='__main__':main()
