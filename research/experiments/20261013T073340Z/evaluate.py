#!/usr/bin/env python3
"""Execute the exact pre-reserved BTC/ETH quarter-hour turn falsification grid."""
from __future__ import annotations
import gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np, polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent;MIN_NS=60_000_000_000;DAY=1440
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'));from kernel import fill
def loadmod(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
cost_engine=loadmod('turn15_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ns):return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def safe(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def gzwrite(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('wb') as f:
  with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as g:g.write(json.dumps(safe(obj),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def dd(values):
 a=np.asarray(values,dtype=np.float64);peaks=np.maximum.accumulate(a);drops=1-a/peaks;j=int(np.argmax(drops));return float(100*drops[j]),int(np.argmax(a[:j+1])),j
def metrics(a,annual=365):
 x=np.asarray(a,dtype=np.float64)
 if len(x)<2 or not np.isfinite(x).all() or (x<=0).any():raise ValueError('invalid/non-positive NAV')
 rets=x[1:]/x[:-1]-1;sd=float(rets.std(ddof=1)) if len(rets)>1 else 0;d,pi,ti=dd(x)
 cagr=(x[-1]/x[0])**(annual/(len(x)-1))-1
 return {'net_return_pct':float(100*(x[-1]/x[0]-1)),'max_drawdown_pct':d,'sharpe_annualized':float(rets.mean()/sd*math.sqrt(annual)) if sd else None,'cagr_pct':float(100*cagr),'calmar':float(cagr/(d/100)) if d else None,'drawdown_peak_index':pi,'drawdown_trough_index':ti,'observations':len(x)-1}

def load_asset(asset,source_files):
 parts=[];manifest=[]
 for item in source_files[asset]:
  p=ROOT/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256']
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*DAY and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN_NS).all() and (f['available_ts']-f['open_ts']==MIN_NS).all()
  assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all()
  manifest.append({'path':item['path'],'bytes':p.stat().st_size,'sha256':sha(p),'bars':f.height,'first_open_utc':stamp(int(f['open_ts'][0])),'last_open_utc':stamp(int(f['open_ts'][-1]))});parts.append(f)
 f=pl.concat(parts,how='vertical_relaxed').sort('open_ts');assert f.height==730*DAY and (f['open_ts'].diff().drop_nulls()==MIN_NS).all()
 op=np.asarray(f['open'].cast(pl.Float64).to_numpy(),dtype=np.float64);cl=np.asarray(f['close'].cast(pl.Float64).to_numpy(),dtype=np.float64)
 qv=np.asarray(f['quote_volume'].cast(pl.Float64).to_numpy(),dtype=np.float64);bv=np.asarray(f['base_volume'].cast(pl.Float64).to_numpy(),dtype=np.float64);ts=f['open_ts'].to_numpy()
 daily=[]
 for d in range(730):
  a=d*DAY;b=a+DAY;daily.append({'close':D(str(cl[b-1])),'quote_volume':D(str(float(qv[a:b].sum())))})
 proxy=np.zeros(len(op),dtype=np.float64);pq=np.concatenate(([0.],np.cumsum(qv)));pb=np.concatenate(([0.],np.cumsum(bv)))
 for i in range(5,len(op)):
  qb=pq[i]-pq[i-5];bb=pb[i]-pb[i-5];proxy[i]=qb/bb if bb>0 else 0
 assert stamp(int(ts[0]))=='2024-09-16T00:00:00Z' and stamp(int(ts[-1]))=='2026-09-15T23:59:00Z'
 return {'asset':asset,'open':op,'close':cl,'quote':qv,'base':bv,'ts':ts,'daily':daily,'proxy':proxy,'manifest':manifest,
  'daily_close_sha256_f64le':hashlib.sha256(np.asarray([float(x['close']) for x in daily],dtype='<f8').tobytes()).hexdigest()}

def one_scene(spec,market,filters,mult,comparator=False):
 start_day=368;end_day=728;start=start_day*DAY;end=end_day*DAY;capital=D('2000');cash=capital;units=D(0)
 params=spec['parameters'];phase=int(params.get('phase_offset_minutes',0));hold=int(params.get('hold_minutes',1))
 events=[] if comparator else [i for i in range(start,end) if (i%60)%15==phase and i+hold<end]
 if comparator:events=[start]
 if comparator:hold=end-start
 evset=set(events);event_i=0;next_exit=None;nav=[float(capital)];times=[int(market['ts'][start])];changes=[(start,cash,units)]
 trades=[];attempts=0;fills=0;rejected=0;rejects={};rejects_by_day={};rejection_examples={};skipped=0;capacity_rejections=0;balance_bad=0
 entry_count=len(events);terminal_idx=end
 # Work only on scheduled event opens, exits/retries and held-minute closes. Flat cash
 # between these points is constant, so these samples capture every NAV change.
 mi=start;last_entry=events[-1] if events else start
 while mi<=terminal_idx:
  is_event=(event_i<len(events) and mi==events[event_i])
  if units>0 and next_exit is not None and mi>=next_exit:
   trade_day=mi//DAY;adv,sigma=cost_engine.lagged_cost_inputs(market['daily'],trade_day)
   ref=D(str(market['open'][mi]));avg=D(str(market['proxy'][mi]))
   cash2,units2,tr=fill(cash,units,False,ref,D(str(adv)),D(str(sigma)),mult,filters,avg);attempts+=1
   tr.update({'execution_minute':mi,'execution_utc':stamp(int(market['ts'][mi])),'signal_utc':stamp(int(market['ts'][int(tr.get('entry_minute',mi))-1])) if tr.get('entry_minute') is not None else None,'scheduled_event_utc':None,'terminal':mi==terminal_idx})
   if tr['status']=='filled':
    cash,units=cash2,units2;fills+=1;trades.append(tr);changes.append((mi,cash,units));nav.append(float(cash+units*ref));times.append(int(market['ts'][mi]));next_exit=None
   else:
    rejected+=1;why=tr.get('reason','unknown');rejects[why]=rejects.get(why,0)+1
    rejects_by_day[str(mi//DAY)]=rejects_by_day.get(str(mi//DAY),0)+1
    if why=='participation':capacity_rejections+=1
    if len(rejection_examples.get(why,[]))<8:rejection_examples.setdefault(why,[]).append(tr)
    if mi<end:
     nav.append(float(cash+units*D(str(market['close'][mi]))));times.append(int(market['ts'][mi])+MIN_NS)
    next_exit=mi+1
   if cash<0 or units<0:balance_bad+=1
  if is_event:
   if units==0:
    event_count=event_i;trade_day=mi//DAY;adv,sigma=cost_engine.lagged_cost_inputs(market['daily'],trade_day)
    ref=D(str(market['open'][mi]));avg=D(str(market['proxy'][mi]));min_notional=D(filters['NOTIONAL']['minNotional'])
    attempts+=1
    if cash<min_notional:
     rejected+=1;rejects['notional']=rejects.get('notional',0)+1;rejects_by_day[str(mi//DAY)]=rejects_by_day.get(str(mi//DAY),0)+1
    else:
     cash2,units2,tr=fill(cash,units,True,ref,D(str(adv)),D(str(sigma)),mult,filters,avg)
     tr.update({'execution_minute':mi,'execution_utc':stamp(int(market['ts'][mi])),'signal_available_utc':stamp(int(market['ts'][mi])-MIN_NS),'signal_to_execution_seconds':60,'event_phase_minutes':phase,'hold_minutes':hold,'terminal':False})
     if tr['status']=='filled':
      cash,units=cash2,units2;fills+=1;trades.append(tr);changes.append((mi,cash,units));nav.append(float(cash+units*ref));times.append(int(market['ts'][mi]));next_exit=mi+hold
     else:
      rejected+=1;why=tr.get('reason','unknown');rejects[why]=rejects.get(why,0)+1;rejects_by_day[str(mi//DAY)]=rejects_by_day.get(str(mi//DAY),0)+1
      if why=='participation':capacity_rejections+=1
      if len(rejection_examples.get(why,[]))<8:rejection_examples.setdefault(why,[]).append(tr)
   else:skipped+=1
   event_i+=1
  # minute close marks while a position is open; end-index is an exclusive boundary.
  if units>0 and start<=mi<end:
   nav.append(float(cash+units*D(str(market['close'][mi]))));times.append(int(market['ts'][mi])+MIN_NS)
  mi+=1
 # Any terminal holding is costed at the first terminal executable minute open.
 terminal_nav=float(cash+units*D(str(market['open'][end])))
 # Preserve the terminal reference mark in sampled drawdown when a frozen filter
 # leaves a residual below the exchange minimum notional.
 if units>0 and (not times or times[-1]<int(market['ts'][end])):
  nav.append(terminal_nav);times.append(int(market['ts'][end]))
 # Daily NAV is marked from the latest fill state at each daily close. Most windows
 # exit in <=3 minutes; if a filter retry spans midnight, the still-open units are marked.
 daily_nav=[float(capital)];daily_times=[stamp(int(market['ts'][start]))]
 change_i=0
 for day in range(start_day,end_day):
  close_i=(day+1)*DAY-1
  while change_i+1<len(changes) and changes[change_i+1][0]<=close_i:change_i+=1
  _,dc,du=changes[change_i];value=float(dc)+float(du)*float(market['close'][close_i]);daily_nav.append(value);daily_times.append(stamp(int(market['ts'][close_i])+MIN_NS))
 if len(daily_nav)!=361:raise AssertionError('daily OOS NAV length')
 daily_nav[-1]=terminal_nav;daily_times[-1]=stamp(int(market['ts'][end]))
 nav_stats=metrics(nav,365*1440);daily_stats=metrics(daily_nav,365)
 allcost={k:str(sum((D(t['cost_parts'][k]) for t in trades),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')};cost=sum((D(v) for v in allcost.values()),D(0));net=D(str(terminal_nav))-capital;gross=net+cost
 folds=[]
 for f in range(12):
  x=f*30;y=(f+1)*30;folds.append({'fold':f+1,'start_utc':daily_times[x],'end_utc':daily_times[y],**metrics(daily_nav[x:y+1],365)})
 sells=sum(t['side']=='sell' for t in trades);flat=units==0
 summary={'net_PnL_usdt':str(net),'terminal_NAV_usdt':str(terminal_nav),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_flat':flat,
  'net_return_pct':nav_stats['net_return_pct'],'max_drawdown_pct':nav_stats['max_drawdown_pct'],'drawdown_scope':'OOS one-minute closes during held windows plus immediate post-fill reference marks; no within-minute extrema; flat-cash periods have constant NAV.',
  'daily_mark_drawdown_pct':daily_stats['max_drawdown_pct'],'sharpe_annualized_daily':daily_stats['sharpe_annualized'],'cagr_pct_daily':daily_stats['cagr_pct'],'calmar_daily':daily_stats['calmar'],
  'cost_usdt':str(cost),'cost_parts_usdt':allcost,'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,
  'scheduled_events':entry_count,'entry_attempts':sum(1 for x in events if x<end),'skipped_entries_while_holding':skipped,'attempts':attempts,'filled_orders':fills,'round_trips':sells,'rejected_orders':rejected,'rejected_by_reason':rejects,'rejected_by_utc_day':rejects_by_day,'rejection_examples':rejection_examples,'capacity_rejections':capacity_rejections,'balance_violations':balance_bad,
  'folds':folds,'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(daily_nav,dtype='<f8').tobytes()).hexdigest(),'daily_nav_samples':len(daily_nav),
  'event_nav_sha256_f64le':hashlib.sha256(np.asarray(nav,dtype='<f8').tobytes()).hexdigest(),'event_nav_samples':len(nav),'cost_multiplier':mult}
 return {'summary':summary,'fills':trades,'daily_nav_usdt':daily_nav,'daily_nav_utc':daily_times,'event_nav_usdt':nav,'event_nav_utc_ns':times}

def main():
 plan=json.loads((ROUND/'plan.json').read_text());batch=json.loads((ROUND/'batch.json').read_text())
 prior=json.loads((ROOT/'research/experiments/20261012T035429Z/report.json').read_text());filters=prior['plan']['execution']['filters']
 markets={a:load_asset(a,plan['data_files']) for a in ('BTC','ETH')};out=ROOT/'data/runs'/ROUND.name;out.mkdir(parents=True,exist_ok=True)
 manifest={'built_at_utc':datetime.now(timezone.utc).isoformat(),'assets':{a:{'sources':markets[a]['manifest'],'minute_bars':len(markets[a]['ts']),'first_open_utc':stamp(int(markets[a]['ts'][0])),'last_open_utc':stamp(int(markets[a]['ts'][-1])),'daily_close_sha256_f64le':markets[a]['daily_close_sha256_f64le']} for a in markets},'filter_source_sha256':sha(ROOT/'research/experiments/20261012T035429Z/report.json'),'kernel_sha256':sha(ROOT/'research/experiments/20261001T133655Z/kernel.py'),'lagged_cost_engine_sha256':sha(ROOT/'research/experiments/20261001T013355Z/evaluate.py')}
 (ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 scenes={};scene_rows=[]
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());asset=row['asset'];sc={};archives={}
  for mult in (1,2,3):
   z=one_scene(spec,markets[asset],filters[asset+'USDT'],mult,row['role']=='buy_hold_comparator');sc[str(mult)]=z['summary'];archives[str(mult)]=z
   # Historical NAV/event ledgers are stored outside Git. Keep their hashes and
   # compact fill-only ledgers in the report archive; notional failures are counted by day.
   navpath=out/f"{row['name']}_x{mult}_nav.npz";np.savez_compressed(navpath,event_nav=np.asarray(z['event_nav_usdt'],dtype='<f8'),event_time_ns=np.asarray(z['event_nav_utc_ns'],dtype='<i8'))
   z['summary']['event_nav_archive']=str(navpath.relative_to(ROOT));z['summary']['event_nav_archive_sha256']=sha(navpath)
   gzwrite(out/f"{row['name']}_x{mult}_ledger.json.gz",{'name':row['name'],'cost_multiplier':mult,'fills':z['fills'],'rejected_orders':z['summary']['rejected_orders'],'rejected_by_reason':z['summary']['rejected_by_reason'],'rejected_by_utc_day':z['summary']['rejected_by_utc_day'],'rejection_examples':z['summary']['rejection_examples'],'daily_nav_usdt':z['daily_nav_usdt'],'daily_nav_utc':z['daily_nav_utc'],'summary':z['summary']})
   scene_rows.append({'name':row['name'],'asset':asset,'role':row['role'],'cost_multiplier':mult,**z['summary']})
   npz=navpath;z['summary']['event_nav_archive_sha256']=sha(npz);archives[str(mult)]=z
   print(f"scene {row['name']} x{mult}: {z['summary']['net_return_pct']:.5f}% trips={z['summary']['round_trips']} rejects={z['summary']['rejected_orders']}",flush=True)
  scenes[row['name']]={'name':row['name'],'asset':asset,'role':row['role'],'fingerprint':row['fingerprint'],'spec':row['spec'],'scenarios':sc,'archives':archives,'spec_object':spec}
 # 3x neighbor share includes cells within one predeclared step on both axes.
 for name,x in scenes.items():
  if x['role']!='primary_event':continue
  p=x['spec_object']['parameters'];asset=x['asset'];neighbors=[]
  for n,y in scenes.items():
   if y['asset']!=asset or y['role']=='buy_hold_comparator':continue
   q=y['spec_object']['parameters']
   if abs(p['phase_offset_minutes']-q['phase_offset_minutes'])<=1 and abs(p['hold_minutes']-q['hold_minutes'])<=1:neighbors.append(n)
  fraction=sum(scenes[n]['scenarios']['3']['net_return_pct']>0 for n in neighbors)/len(neighbors)
  sc=x['scenarios'];one=sc['1'];three=sc['3'];positive=sum(f['net_return_pct']>0 for f in one['folds'])
  gates={'all_costs_positive':all(sc[str(m)]['net_return_pct']>0 for m in (1,2,3)),'positive_1x_folds_at_least_8_of_12':positive>=8,'drawdown_3x_at_most_25pct':three['max_drawdown_pct']<=25,
   'adjacent_3x_positive_fraction_at_least_0_60':fraction>=.60,'round_trips_1x_at_least_100':one['round_trips']>=100,'gross_to_cost_1x_at_least_2_5':one['gross_reference_pnl_to_cost'] is not None and one['gross_reference_pnl_to_cost']>=2.5,
   'no_order_rejections_or_capacity_violations':all(sc[str(m)]['rejected_orders']==0 and sc[str(m)]['capacity_rejections']==0 for m in (1,2,3)),'terminal_flat_all_costs':all(sc[str(m)]['terminal_flat'] for m in (1,2,3))}
  sc['gates']=gates;sc['neighbor_3x_positive_fraction']=fraction;sc['neighbor_count']=len(neighbors);sc['positive_1x_fold_count']=positive
 # Exact phase specificity across matched hold lengths for each asset.
 phase_means={}
 for a in ('BTC','ETH'):
  phase_means[a]={}
  for p in (0,1,2):
   xs=[v['scenarios']['1']['net_return_pct'] for v in scenes.values() if v['asset']==a and v['role']!='buy_hold_comparator' and v['spec_object']['parameters']['phase_offset_minutes']==p]
   phase_means[a][str(p)]=float(np.mean(xs))
 for name,x in scenes.items():
  if x['role']!='primary_event':continue
  a=x['asset'];g=x['scenarios']['gates'];g['phase0_beats_both_placebos_for_asset']=phase_means[a]['0']>phase_means[a]['1'] and phase_means[a]['0']>phase_means[a]['2'];x['scenarios']['phase_means_1x_by_asset']=phase_means[a];x['scenarios']['status']='passed' if all(g.values()) else 'rejected'
 for name,x in scenes.items():
  if x['role']!='primary_event':x['scenarios']['status']='rejected'
 # Report full per-scene fold tables and summary rows; verbose event arrays remain ignored under data/runs.
 configs={n:{k:v for k,v in x.items() if k!='archives' and k!='spec_object'} for n,x in scenes.items()}
 for cfg in configs.values():
  for sv in cfg['scenarios'].values():
   if isinstance(sv,dict):sv.pop('rejected_by_utc_day',None)
 report={'round':ROUND.name,'evaluation_finished_at_utc':manifest['built_at_utc'],'plan':plan,'data_manifest':manifest,'phase_means_1x_by_asset':phase_means,
  'summary':{'candidate_configs':6,'phase_controls':12,'comparators':2,'primary_passed':sum(x['scenarios']['status']=='passed' for x in configs.values() if next(y for y in batch if y['name']==x['name'])['role']=='primary_event'),'primary_rejected':sum(x['scenarios']['status']=='rejected' for x in configs.values() if next(y for y in batch if y['name']==x['name'])['role']=='primary_event'),'oos_days':360,'folds':12,'primary_ranked_by_1x_return':sorted([x['name'] for x in configs.values() if next(y for y in batch if y['name']==x['name'])['role']=='primary_event'],key=lambda n:configs[n]['scenarios']['1']['net_return_pct'],reverse=True)},'configs':configs,'scene_rows_external':['cost_scenarios.csv','fold_results.csv']}
 (ROUND/'report.json').write_text(json.dumps(safe(report),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 print(json.dumps(report['summary'],ensure_ascii=False),flush=True)
if __name__=='__main__':main()
