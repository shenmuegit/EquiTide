#!/usr/bin/env python3
"""Evaluate a reserved BTC/ETH daily relative-strength rotation grid."""
from __future__ import annotations
import csv,gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3]; ROUND=Path(__file__).resolve().parent
MIN=60_000_000_000; DAY=1440*MIN
sys.path.insert(0,str(ROOT/'research/automation')); import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
from kernel import fill

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
engine=load('r52_lagged_daily_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ns): return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def canonical(x): return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def gzwrite(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as g:g.write(json.dumps(canonical(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())

def load_asset(asset):
 paths=[ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
 frames=[];file_rows=[]
 for p in paths:
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all()
  assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all()
  file_rows.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'bars':f.height,'first_open_ns':int(f['open_ts'][0]),'last_open_ns':int(f['open_ts'][-1])})
  frames.append(f)
 minute=pl.concat(frames,how='vertical_relaxed').sort('open_ts');assert minute.height==730*1440 and (minute['open_ts'].diff().drop_nulls()==MIN).all()
 opens=minute['open'].to_list();closes=minute['close'].to_list();qv=minute['quote_volume'].to_list();bv=minute['base_volume'].to_list();ts=minute['open_ts'].to_numpy();closef=minute['close'].cast(pl.Float64).to_numpy()
 daily=[];proxy=[]
 for d in range(730):
  lo=d*1440; end=(d+1)*1440; close_i=end-1;trade_i=lo+1
  q=sum((D(str(x)) for x in qv[lo:end]),D(0));base=sum((D(str(x)) for x in bv[lo:end]),D(0))
  px_q=sum((D(str(x)) for x in qv[trade_i-5:trade_i]),D(0));px_b=sum((D(str(x)) for x in bv[trade_i-5:trade_i]),D(0))
  day_open=int(ts[lo]);avail=int(ts[close_i])+MIN;trade=int(ts[trade_i])
  assert avail==day_open+DAY and trade==day_open+MIN and avail<trade+DAY
  daily.append({'date':stamp(day_open).split('T')[0],'day_open_ns':day_open,'close':D(str(closes[close_i])),'close_available_ts':avail,'quote_volume':q,'trade_ts':trade,'trade_open':D(str(opens[trade_i]))})
  proxy.append(px_q/px_b if px_b>0 else D(0))
 assert stamp(daily[0]['day_open_ns'])=='2024-09-16T00:00:00Z' and stamp(daily[-1]['close_available_ts'])=='2026-09-16T00:00:00Z'
 return {'asset':asset,'daily':daily,'proxy':proxy,'minute_open':opens,'minute_close':closef,'minute_quote':qv,'minute_base':bv,'minute_ts':ts,'files':file_rows,'daily_close_sha256_f64le':hashlib.sha256(np.asarray([float(r['close']) for r in daily],dtype='<f8').tobytes()).hexdigest()}

def drawdown(x):
 a=np.asarray(x,dtype=np.float64);pk=np.maximum.accumulate(a);v=1-a/pk;j=int(np.argmax(v));return float(v[j]*100),int(np.argmax(a[:j+1])),j

def metrics(x,periods_per_year):
 a=np.asarray(x,dtype=np.float64);assert len(a)>1 and np.all(np.isfinite(a)) and np.all(a>0)
 rets=a[1:]/a[:-1]-1;sd=float(np.std(rets,ddof=1)) if len(rets)>1 else 0.;dd,pi,ti=drawdown(a)
 cagr=(float(a[-1])/float(a[0]))**(periods_per_year/(len(a)-1))-1
 return {'net_return_pct':float((a[-1]/a[0]-1)*100),'max_drawdown_pct':dd,'sharpe_annualized':float(np.mean(rets)/sd*math.sqrt(periods_per_year)) if sd else None,'cagr_pct':cagr*100,'calmar':cagr/(dd/100) if dd else None,'drawdown_peak_index':pi,'drawdown_trough_index':ti,'observations':len(a)-1}

def boundaries(parameters):
 start=parameters.get('oos_first_test_index',parameters.get('oos_start_day_index',parameters.get('start_day_index')))
 end=parameters.get('oos_end_exclusive_index',parameters.get('oos_end_day_index',parameters.get('end_day_index')))
 if start is None or end is None: raise ValueError('OOS daily index boundaries missing from spec')
 return int(start),int(end)

def run(spec,markets,filters,mult,hold_asset=None):
 p=spec['parameters'];start,end=boundaries(p);cap=D('2000')
 assert start==368 and end==728
 daily={a:markets[a]['daily'] for a in ('BTC','ETH')};cash=cap;units=D(0);held=None;trades=[];decisions=[]
 def execute(asset,buy,i,terminal=False,signal_i=None):
  nonlocal cash,units
  m=markets[asset];row=m['daily'][i];day_index=i;ref=D(row['trade_open']);avg=m['proxy'][i]
  adv,sigma=engine.lagged_cost_inputs(m['daily'],day_index)
  priorcash,priorunits=cash,units
  cash,units,t=fill(cash,units,buy,ref,D(str(adv)),D(str(sigma)),mult,filters[asset+'USDT'],avg)
  t.update({'asset':asset,'bar_index':i,'signal_bar_index':signal_i,'signal_available_utc':stamp(m['daily'][signal_i]['close_available_ts']) if signal_i is not None else None,'execution_utc':stamp(row['trade_ts']),'signal_to_execution_seconds':(row['trade_ts']-m['daily'][signal_i]['close_available_ts'])/1e9 if signal_i is not None else None,'terminal':terminal,'cash_before':str(priorcash),'units_before':str(priorunits),'cash_after':str(cash),'units_after':str(units)})
  trades.append(t);return t
 start_min=start*1440+1;terminal_min=end*1440+1;mark_end=end*1440;close_indices={};nav=[float(cap)]
 events=[]
 for i in range(start,end):
  if hold_asset:
   target=hold_asset if i==start else held
   if i==start: action=[('buy',hold_asset)]
   else: action=[]
   prev_btc=prev_eth=None;roc_btc=roc_eth=None
  else:
   j=i-1;look=int(p['lookback_days']);rbtc=daily['BTC'][j]['close']/daily['BTC'][j-look]['close']-D(1);reth=daily['ETH'][j]['close']/daily['ETH'][j-look]['close']-D(1);hurdle=D(str(p['absolute_return_hurdle']))
   winner='BTC' if rbtc>=reth else 'ETH';target=winner if max(rbtc,reth)>hurdle else None
   before=held;action=[]
   if target!=held:
    if held is not None:action.append(('sell',held))
    if target is not None:action.append(('buy',target))
   prev_btc,prev_eth,roc_btc,roc_eth=rbtc,reth,rbtc,reth
   decisions.append({'decision_index':i,'signal_index':j,'signal_close_available_utc':stamp(daily['BTC'][j]['close_available_ts']),'execution_utc':stamp(daily['BTC'][i]['trade_ts']),'btc_return':str(rbtc),'eth_return':str(reth),'hurdle':str(hurdle),'desired_target':target,'held_before':before,'actions':action})
  for side,asset in action:
   if side=='buy' and held is not None: continue
   was=held
   t=execute(asset,side=='buy',i,False,None if hold_asset and i==start else i-1)
   mi=i*1440+1
   if side=='sell' and t['status']=='filled':held=None
   elif side=='buy' and t['status']=='filled':held=asset
   events.append((mi,t,held,cash,units))
 # Terminal liquidation at common next-day 00:01 reference.
 if held is not None:
  t=execute(held,False,end,True,end-1);mi=end*1440+1
  if t['status']=='filled':held=None
  events.append((mi,t,held,cash,units))
 terminal_ref_asset=held or (trades[-1]['asset'] if trades else 'BTC')
 terminal_ref=D(markets[terminal_ref_asset]['daily'][end]['trade_open']);terminal_nav=cash+(units*terminal_ref if held else D(0))
 navstream=[float(cap)];event_i=0;current_cash=cap;current_units=D(0);current_asset=None
 for mi in range(start_min,mark_end):
  while event_i<len(events) and events[event_i][0]==mi:
   _,t,asset_after,c,u=events[event_i]
   current_asset=asset_after;current_cash=c;current_units=u
   ref=D(t['reference']);navstream.append(float(current_cash+(current_units*ref if current_asset else D(0))));event_i+=1
  if current_asset:
   navstream.append(float(current_cash+current_units*D(str(markets[current_asset]['minute_close'][mi]))))
  else: navstream.append(float(current_cash))
  close_indices[mi]=len(navstream)-1
 # Terminal event is already applied above only if its execution minute was in the interval; it is excluded, so append terminal reference value.
 navstream.append(float(terminal_nav))
 daynav=[float(cap)]
 for d in range(1,361):
  mi=(start+d)*1440-1; daynav.append(navstream[close_indices[mi]])
 daynav[-1]=float(terminal_nav)
 minute_dd,mpi,mti=drawdown(navstream);daymet=metrics(daynav,365)
 folds=[]
 for f in range(12):
  a=f*30;b=a+30;fold=metrics(daynav[a:b+1],365)
  folds.append({'fold':f+1,'start_utc':daily['BTC'][start+a]['date'],'end_exclusive_utc':daily['BTC'][start+b]['date'] if start+b<len(daily['BTC']) else '2026-09-14',**fold})
 filled=[t for t in trades if t['status']=='filled'];parts={k:str(sum((D(t['cost_parts'][k]) for t in filled),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')};cost=sum((D(v) for v in parts.values()),D(0))
 gross=terminal_nav-cap+cost; npos=sum(f['net_return_pct']>0 for f in folds)
 rejected=[t for t in trades if t['status']!='filled']
 summary={'net_return_pct':daymet['net_return_pct'],'net_pnl_usdt':str(terminal_nav-cap),'terminal_nav_usdt':str(terminal_nav),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_asset':held,'terminal_flat':held is None and units==0,'cost_usdt':str(cost),'cost_parts_usdt':parts,'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,'max_drawdown_pct':minute_dd,'daily_mark_drawdown_pct':daymet['max_drawdown_pct'],'drawdown_scope':'All OOS one-minute bar-close samples plus immediate post-fill reference marks; no within-minute extrema.','sharpe_annualized_daily':daymet['sharpe_annualized'],'cagr_pct':daymet['cagr_pct'],'calmar':daymet['calmar'],'attempts':len(trades),'executions':len(filled),'round_trips':sum(t['side']=='sell' for t in filled),'positive_1x_folds':npos,'rejected_orders':len(rejected),'rejection_reasons':{r:sum(t.get('reason')==r for t in rejected) for r in sorted({t.get('reason') for t in rejected})},'capacity_rejections':sum(t.get('reason')=='participation' for t in rejected),'balance_violations':sum(D(t['cash_after'])<0 or D(t['units_after'])<0 for t in trades),'folds':folds,'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(navstream,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(navstream),'cost_multiplier':mult}
 archive={'name':spec['name'],'fingerprint':registry.fingerprint(spec),'spec':spec,'decisions':decisions,'trades':trades,'daily_nav_usdt':daynav,'summary':summary}
 return archive

def run_static_equal(spec,markets,filters,mult):
 """One-time 50/50 BTC/ETH sleeves; no rebalance after the initial allocation."""
 p=spec['parameters'];start,end=boundaries(p);capital=D('2000');weights={'BTC':D('.5'),'ETH':D('.5')}
 cash={a:capital*weights[a] for a in weights};units={a:D(0) for a in weights};trades=[]
 daily={'BTC':markets['BTC']['daily'],'ETH':markets['ETH']['daily']}
 def execute(a,buy,i,terminal=False):
  nonlocal cash,units
  m=markets[a];row=m['daily'][i];adv,sigma=engine.lagged_cost_inputs(m['daily'],i);ref=D(row['trade_open']);avg=m['proxy'][i]
  cb,ub=cash[a],units[a];cash[a],units[a],t=fill(cb,ub,buy,ref,D(str(adv)),D(str(sigma)),mult,filters[a+'USDT'],avg)
  t.update({'asset':a,'bar_index':i,'signal_bar_index':None if i==start else i-1,'signal_available_utc':stamp(row['day_open_ns']) if i==start else stamp(m['daily'][i-1]['close_available_ts']),'execution_utc':stamp(row['trade_ts']),'signal_to_execution_seconds':60,'terminal':terminal,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(cash[a]),'units_after':str(units[a])})
  trades.append(t);return t
 # First execution is one minute after OOS start. Each sleeve uses its frozen 50% raw allocation.
 for a in ('BTC','ETH'):execute(a,True,start)
 start_min=start*1440+1;end_min=end*1440;terminal_min=end*1440+1
 nav=[float(capital)];times=[int(markets['BTC']['minute_ts'][start*1440])]
 for a in ('BTC','ETH'):
  row=markets[a]['daily'][start];nav.append(float(cash['BTC']+cash['ETH']+sum(units[b]*D(row['trade_open'] if b==a else markets[b]['daily'][start]['trade_open']) for b in units)));times.append(int(row['trade_ts']))
 for mi in range(start_min,end_min):
  value=sum((float(cash[a])+float(units[a])*float(markets[a]['minute_close'][mi]) for a in units),0.0);nav.append(value);times.append(int(markets['BTC']['minute_ts'][mi])+MIN)
 # Daily OOS marks sample each prior calendar day's final close; all OOS positions are already active.
 daynav=[float(capital)]
 for d in range(1,361):
  mi=(start+d)*1440-1;daynav.append(sum((float(cash[a])+float(units[a])*float(markets[a]['minute_close'][mi]) for a in units),0.0))
 # Terminal liquidation at the frozen next-day 00:01 open.
 for a in ('BTC','ETH'):
  if units[a]>0:execute(a,False,end,True)
 terminal_nav=float(cash['BTC']+cash['ETH']);daynav[-1]=terminal_nav
 for t in trades[-2:]:
  if t['status']=='filled':nav.append(float(cash['BTC']+cash['ETH']));times.append(int(markets[t['asset']]['daily'][end]['trade_ts']))
 evmet=metrics(nav,365*1440);daymet=metrics(daynav,365);fills=[t for t in trades if t['status']=='filled']
 parts={k:str(sum((D(t['cost_parts'][k]) for t in fills),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')};cost=sum((D(v) for v in parts.values()),D(0));net=D(str(terminal_nav))-capital;gross=net+cost
 folds=[]
 for f in range(12):
  a=f*30;b=a+30;folds.append({'fold':f+1,'start_utc':daily['BTC'][start+a]['date'],'end_exclusive_utc':daily['BTC'][start+b]['date'] if start+b<len(daily['BTC']) else '2026-09-14',**metrics(daynav[a:b+1],365)})
 rejected=[t for t in trades if t['status']!='filled']
 summary={'net_return_pct':evmet['net_return_pct'],'net_pnl_usdt':str(net),'terminal_nav_usdt':str(terminal_nav),'terminal_cash_usdt':str(terminal_nav),'terminal_units':'0','terminal_asset':None,'terminal_flat':all(units[a]==0 for a in units),'cost_usdt':str(cost),'cost_parts_usdt':parts,'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,'max_drawdown_pct':evmet['max_drawdown_pct'],'daily_mark_drawdown_pct':daymet['max_drawdown_pct'],'drawdown_scope':'All OOS one-minute closes plus immediate post-fill reference marks; no within-minute extrema.','sharpe_annualized_daily':daymet['sharpe_annualized'],'cagr_pct_daily':daymet['cagr_pct'],'calmar_daily':daymet['calmar'],'attempts':len(trades),'executions':len(fills),'round_trips':sum(t['side']=='sell' for t in fills),'positive_1x_folds':sum(x['net_return_pct']>0 for x in folds),'rejected_orders':len(rejected),'rejection_reasons':{r:sum(t.get('reason')==r for t in rejected) for r in sorted({t.get('reason') for t in rejected})},'capacity_rejections':sum(t.get('reason')=='participation' for t in rejected),'balance_violations':sum(D(t['cash_after'])<0 or D(t['units_after'])<0 for t in trades),'folds':folds,'daily_nav_sha256_f64le':hashlib.sha256(np.asarray(daynav,dtype='<f8').tobytes()).hexdigest(),'daily_nav_samples':len(daynav),'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(nav,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(nav),'cost_multiplier':mult}
 return {'name':spec['name'],'fingerprint':registry.fingerprint(spec),'spec':spec,'decisions':[],'trades':trades,'daily_nav_usdt':daynav,'summary':summary,'event_nav_usdt':nav,'event_nav_utc_ns':times}

def main():
 plan=json.loads((ROUND/'plan.json').read_text()); batch=json.loads((ROUND/'batch.json').read_text())
 filterfile=json.loads((ROUND/'exchange_filters.json').read_text())
 filters={a+'USDT':{f['filterType']:f for f in filterfile['symbols'][a]} for a in ('BTC','ETH')}
 markets={a:load_asset(a) for a in ('BTC','ETH')}
 manifest={'assets':{a:{'source_files':markets[a]['files'],'daily_bars':len(markets[a]['daily']),'first_daily_date':markets[a]['daily'][0]['date'],'last_daily_date':markets[a]['daily'][-1]['date'],'daily_close_sha256_f64le':markets[a]['daily_close_sha256_f64le']} for a in markets},'exchange_filter_snapshot':filterfile['snapshot'],'kernel_sha256':sha(ROOT/'research/experiments/20261001T133655Z/kernel.py'),'lagged_cost_engine_sha256':sha(ROOT/'research/experiments/20261001T013355Z/evaluate.py')}
 (ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 out=ROOT/'data/runs'/ROUND.name;out.mkdir(parents=True,exist_ok=True);cfg={};results=[]
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());cfg[row['name']]={'asset_universe':spec['universe'],'fingerprint':row['fingerprint'],'spec':row['spec'],'role':row['role'],'scenarios':{}}
  for mult in (1,2,3):
   if row['role']=='static_equal_hold':arc=run_static_equal(spec,markets,filters,mult)
   else:
    hold_asset=row.get('asset') if row['role']=='single_asset_hold' else None
    arc=run(spec,markets,filters,mult,hold_asset)
   cfg[row['name']]['scenarios'][str(mult)]=arc['summary'];gzwrite(out/f"{row['name']}_cost{mult}.json.gz",arc);results.append({'name':row['name'],'cost':mult,'role':row['role'],**arc['summary']})
  print(row['name'],*[round(cfg[row['name']]['scenarios'][str(m)]['net_return_pct'],4) for m in (1,2,3)],flush=True)
 # Fixed 3x neighborhood across one adjacent value on each axis.
 for row in batch:
  if row['role']!='candidate':continue
  spec=json.loads((ROOT/row['spec']).read_text());p=spec['parameters'];neigh=[]
  for other in batch:
   if other['role']!='candidate':continue
   q=json.loads((ROOT/other['spec']).read_text())['parameters']
   if abs(q['lookback_days']-p['lookback_days'])<=63 and abs(q['absolute_return_hurdle']-p['absolute_return_hurdle'])<=0.05:neigh.append(other['name'])
  c=cfg[row['name']]['scenarios'];frac=sum(cfg[n]['scenarios']['3']['net_return_pct']>0 for n in neigh)/len(neigh)
  for m in ('1','2','3'):c[m]['neighborhood_positive_fraction_3x']=frac;c[m]['neighborhood_size']=len(neigh)
  gates={'all_cost_scenarios_positive':all(c[str(m)]['net_return_pct']>0 for m in (1,2,3)),'positive_1x_folds_at_least_8':c['1']['positive_1x_folds']>=8,'drawdown_3x_under_25pct':c['3']['max_drawdown_pct']<=25,'neighbor_fraction_at_least_0_60':frac>=0.6,'round_trips_at_least_4':c['1']['round_trips']>=4,'gross_to_cost_at_least_2_5':c['1']['gross_reference_pnl_to_cost'] is not None and c['1']['gross_reference_pnl_to_cost']>=2.5,'no_capacity_filter_or_balance_violations':all(c[str(m)]['capacity_rejections']==0 and c[str(m)]['balance_violations']==0 for m in (1,2,3)),'terminal_flat':all(c[str(m)]['terminal_flat'] for m in (1,2,3))}
  cfg[row['name']]['gates']=gates;cfg[row['name']]['status']='passed' if all(gates.values()) else 'rejected'
 ranked=sorted([x['name'] for x in batch if x['role']=='candidate'],key=lambda n:cfg[n]['scenarios']['1']['net_return_pct'],reverse=True)
 report={'round':ROUND.name,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':manifest,'summary':{'candidate_configs':9,'comparators':3,'candidate_passed':sum(cfg[n]['status']=='passed' for n in ranked),'candidate_rejected':sum(cfg[n]['status']=='rejected' for n in ranked),'oos_days':360,'folds':12,'ranking_1x':ranked,'cost_scenes':len(results)},'configs':cfg,'scene_summaries':results}
 (ROUND/'report.json').write_text(json.dumps(canonical(report),indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(report['summary'],ensure_ascii=False))
if __name__=='__main__':main()
