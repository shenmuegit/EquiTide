#!/usr/bin/env python3
"""Evaluate the pre-reserved daily BTC/ETH ratio z-score rotation grid."""
from __future__ import annotations
import gzip,hashlib,importlib.util,json,math,statistics,sys
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import numpy as np,polars as pl
ROOT=Path(__file__).resolve().parents[3];ROUND=Path(__file__).resolve().parent
MIN=60_000_000_000;DAY=1440*MIN
sys.path.insert(0,str(ROOT/'research/automation'));import registry
sys.path.insert(0,str(ROOT/'research/experiments/20261001T133655Z'))
from kernel import fill

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
engine=load('r53_lagged_daily_cost_engine',ROOT/'research/experiments/20261001T013355Z/evaluate.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def stamp(ns):return datetime.fromtimestamp(ns/1e9,timezone.utc).isoformat().replace('+00:00','Z')
def canonical(x):return json.loads(json.dumps(x,default=str,ensure_ascii=False,allow_nan=False))
def gzwrite(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as g:g.write(json.dumps(canonical(x),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())

def load_asset(asset):
 paths=[ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20240916T000000Z_20250916T000000Z_transfer_20261001/spot_bars.parquet',ROOT/f'data/normalized/binance/{asset}/binance_{asset}_20250916T000000Z_20260916T000000Z_archive_20260929/spot_bars.parquet']
 frames=[];info=[]
 for p in paths:
  f=pl.read_parquet(p,columns=['open_ts','available_ts','open','close','base_volume','quote_volume','is_closed'])
  assert f.height==365*1440 and f['is_closed'].all() and f['open_ts'].is_sorted()
  assert (f['open_ts'].diff().drop_nulls()==MIN).all() and (f['available_ts']-f['open_ts']==MIN).all()
  assert (f['open']>0).all() and (f['close']>0).all() and (f['base_volume']>=0).all() and (f['quote_volume']>=0).all()
  info.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size,'bars':f.height,'first_open_ns':int(f['open_ts'][0]),'last_open_ns':int(f['open_ts'][-1])});frames.append(f)
 minute=pl.concat(frames,how='vertical_relaxed').sort('open_ts');assert minute.height==730*1440 and (minute['open_ts'].diff().drop_nulls()==MIN).all()
 op=minute['open'].to_list();cl=minute['close'].to_list();qv=minute['quote_volume'].to_list();bv=minute['base_volume'].to_list();ts=minute['open_ts'].to_numpy();cf=minute['close'].cast(pl.Float64).to_numpy();daily=[];proxy=[]
 for d in range(730):
  lo=d*1440;hi=(d+1)*1440;trade_i=lo+1;close_i=hi-1;start_ns=int(ts[lo]);avail=int(ts[close_i])+MIN;trade_ts=int(ts[trade_i])
  pq=sum((D(str(x)) for x in qv[trade_i-5:trade_i]),D(0));pb=sum((D(str(x)) for x in bv[trade_i-5:trade_i]),D(0))
  assert avail==start_ns+DAY and trade_ts==start_ns+MIN
  daily.append({'date':stamp(start_ns).split('T')[0],'day_open_ns':start_ns,'close':D(str(cl[close_i])),'close_available_ts':avail,'quote_volume':sum((D(str(x)) for x in qv[lo:hi]),D(0)),'trade_ts':trade_ts,'trade_open':D(str(op[trade_i]))})
  proxy.append(pq/pb if pb>0 else D(0))
 assert daily[0]['date']=='2024-09-16' and stamp(daily[-1]['close_available_ts'])=='2026-09-16T00:00:00Z'
 return {'asset':asset,'daily':daily,'proxy':proxy,'minute_open':op,'minute_close':cf,'minute_quote':qv,'minute_base':bv,'minute_ts':ts,'files':info,'daily_close_sha256_f64le':hashlib.sha256(np.asarray([float(x['close']) for x in daily],dtype='<f8').tobytes()).hexdigest()}

def drawdown(x):
 a=np.asarray(x,dtype=np.float64);p=np.maximum.accumulate(a);v=1-a/p;j=int(np.argmax(v));return float(v[j]*100),int(np.argmax(a[:j+1])),j
def metrics(x,ppy):
 a=np.asarray(x,dtype=np.float64);assert len(a)>1 and np.isfinite(a).all() and (a>0).all();ret=a[1:]/a[:-1]-1;sd=float(np.std(ret,ddof=1)) if len(ret)>1 else 0.;dd,pi,ti=drawdown(a);cagr=(float(a[-1])/float(a[0]))**(ppy/(len(a)-1))-1
 return {'net_return_pct':float((a[-1]/a[0]-1)*100),'max_drawdown_pct':dd,'sharpe_annualized':float(np.mean(ret)/sd*math.sqrt(ppy)) if sd else None,'cagr_pct':cagr*100,'calmar':cagr/(dd/100) if dd else None,'drawdown_peak_index':pi,'drawdown_trough_index':ti,'observations':len(a)-1}

def run(spec,markets,ratio,filters,mult,hold_asset=None):
 p=spec['parameters'];start=int(p['oos_first_test_index']);end=int(p['oos_end_exclusive_index']);cap=D('2000');cash=cap;units=D(0);held=None;trades=[];decisions=[];events=[]
 assert start==368 and end==728 and len(ratio)==730
 def execute(asset,buy,i,terminal=False,signal_i=None):
  nonlocal cash,units
  market=markets[asset];row=market['daily'][i];adv,sigma=engine.lagged_cost_inputs(market['daily'],i);ref=D(row['trade_open']);avg=market['proxy'][i];cb,ub=cash,units
  cash,units,t=fill(cash,units,buy,ref,D(str(adv)),D(str(sigma)),mult,filters[asset+'USDT'],avg)
  t.update({'asset':asset,'bar_index':i,'signal_index':signal_i,'signal_available_utc':stamp(market['daily'][signal_i]['close_available_ts']) if signal_i is not None else None,'execution_utc':stamp(row['trade_ts']),'signal_to_execution_seconds':(row['trade_ts']-market['daily'][signal_i]['close_available_ts'])/1e9 if signal_i is not None else None,'terminal':terminal,'cash_before':str(cb),'units_before':str(ub),'cash_after':str(cash),'units_after':str(units)})
  trades.append(t);return t
 for i in range(start,end):
  if hold_asset:
   target=hold_asset if i==start else held
   acts=[('buy',target)] if i==start else []
  else:
   j=i-1;lb=int(p['lookback_days']);z=(ratio[j]-statistics.mean(ratio[j-lb:j]))/statistics.stdev(ratio[j-lb:j]) if statistics.stdev(ratio[j-lb:j])>0 else 0.0;thr=float(p['entry_zscore_threshold']);ex=float(p['exit_abs_zscore'])
   if z>thr:target='ETH'
   elif z < -thr:target='BTC'
   elif held=='ETH' and z>ex:target='ETH'
   elif held=='BTC' and z < -ex:target='BTC'
   else:target=None
   before=held;acts=[]
   if target!=held:
    if held is not None:acts.append(('sell',held))
    if target is not None:acts.append(('buy',target))
   decisions.append({'decision_index':i,'signal_index':j,'signal_available_utc':stamp(markets['BTC']['daily'][j]['close_available_ts']),'execution_utc':stamp(markets['BTC']['daily'][i]['trade_ts']),'log_ratio':ratio[j],'reference_mean':statistics.mean(ratio[j-lb:j]),'reference_sample_std':statistics.stdev(ratio[j-lb:j]),'zscore':z,'entry_threshold':thr,'exit_abs_zscore':ex,'held_before':before,'target':target,'actions':acts})
  for side,asset in acts:
   if side=='buy' and held is not None:continue
   t=execute(asset,side=='buy',i,False,None if hold_asset and i==start else i-1);mi=i*1440+1
   if side=='sell' and t['status']=='filled':held=None
   elif side=='buy' and t['status']=='filled':held=asset
   events.append((mi,t,held,cash,units))
 # Costed terminal liquidation at the next UTC day 00:01 reference.
 if held is not None:
  asset=held;t=execute(asset,False,end,True,end-1);mi=end*1440+1
  if t['status']=='filled':held=None
  events.append((mi,t,held,cash,units))
 terminal_asset=held or (trades[-1]['asset'] if trades else 'BTC');terminal_ref=D(markets[terminal_asset]['daily'][end]['trade_open']);terminal_nav=cash+(units*terminal_ref if held else D(0))
 start_min=start*1440+1;term_min=end*1440+1;nav=[float(cap)];close_index={};ev=0;mark_cash=cap;mark_units=D(0);mark_asset=None
 for mi in range(start_min,term_min):
  while ev<len(events) and events[ev][0]==mi:
   _,t,mark_asset,mark_cash,mark_units=events[ev];ref=D(t['reference']);nav.append(float(mark_cash+(mark_units*ref if mark_asset else D(0))));ev+=1
  if mark_asset:nav.append(float(mark_cash+mark_units*D(str(markets[mark_asset]['minute_close'][mi]))))
  else:nav.append(float(mark_cash))
  close_index[mi]=len(nav)-1
 nav.append(float(terminal_nav));daynav=[float(cap)]
 for d in range(1,361):daynav.append(nav[close_index[start_min+d*1440-1]])
 daynav[-1]=float(terminal_nav);dm=metrics(daynav,365);md,pi,ti=drawdown(nav)
 folds=[]
 for f in range(12):
  a=f*30;b=a+30;fold=metrics(daynav[a:b+1],365)
  folds.append({'fold':f+1,'start_utc':markets['BTC']['daily'][start+a]['date'],'end_exclusive_utc':markets['BTC']['daily'][start+b]['date'],**fold})
 filled=[t for t in trades if t['status']=='filled'];parts={k:str(sum((D(t['cost_parts'][k]) for t in filled),D(0))) for k in ('fee','half_spread','slippage','impact','tick_rounding')};cost=sum((D(v) for v in parts.values()),D(0));gross=terminal_nav-cap+cost
 summary={'net_return_pct':dm['net_return_pct'],'net_pnl_usdt':str(terminal_nav-cap),'terminal_nav_usdt':str(terminal_nav),'terminal_cash_usdt':str(cash),'terminal_units':str(units),'terminal_asset':held,'cost_usdt':str(cost),'cost_parts_usdt':parts,'gross_reference_pnl_usdt':str(gross),'gross_reference_pnl_to_cost':float(gross/cost) if cost else None,'max_drawdown_pct':md,'daily_mark_drawdown_pct':dm['max_drawdown_pct'],'drawdown_scope':'All OOS one-minute close samples plus immediate post-fill reference marks; no within-minute extrema.','sharpe_annualized_daily':dm['sharpe_annualized'],'cagr_pct':dm['cagr_pct'],'calmar':dm['calmar'],'attempts':len(trades),'executions':len(filled),'round_trips':sum(t['side']=='sell' for t in filled),'positive_1x_folds':sum(x['net_return_pct']>0 for x in folds),'rejected_orders':sum(t['status']!='filled' for t in trades),'balance_violations':sum(D(t['cash_after'])<0 or D(t['units_after'])<0 for t in trades),'folds':folds,'minute_nav_sha256_f64le':hashlib.sha256(np.asarray(nav,dtype='<f8').tobytes()).hexdigest(),'minute_nav_samples':len(nav),'cost_multiplier':mult}
 return {'name':spec['name'],'fingerprint':registry.fingerprint(spec),'spec':spec,'decisions':decisions,'trades':trades,'daily_nav_usdt':daynav,'summary':summary}

def main():
 plan=json.loads((ROUND/'spec.json').read_text());batch=json.loads((ROUND/'batch.json').read_text());source=json.loads((ROOT/'research/experiments/20261012T035429Z/report.json').read_text());filters=source['plan']['execution']['filters'];markets={a:load_asset(a) for a in ('BTC','ETH')}
 assert len(markets['BTC']['daily'])==len(markets['ETH']['daily']) and all(markets['BTC']['daily'][i]['day_open_ns']==markets['ETH']['daily'][i]['day_open_ns'] for i in range(730))
 ratio=[math.log(float(markets['BTC']['daily'][i]['close']/markets['ETH']['daily'][i]['close'])) for i in range(730)]
 manifest={'assets':{a:{'source_files':markets[a]['files'],'daily_count':len(markets[a]['daily']),'daily_close_sha256_f64le':markets[a]['daily_close_sha256_f64le']} for a in markets},'derived_log_ratio_sha256_f64le':hashlib.sha256(np.asarray(ratio,dtype='<f8').tobytes()).hexdigest(),'filters_source_sha256':sha(ROOT/'research/experiments/20261012T035429Z/report.json')};(ROUND/'data_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 out=ROOT/'data/runs'/ROUND.name;out.mkdir(parents=True,exist_ok=True);cfg={};allrows=[]
 for row in batch:
  spec=json.loads((ROOT/row['spec']).read_text());cfg[row['name']]={'fingerprint':row['fingerprint'],'spec':row['spec'],'is_comparator':row['is_comparator'],'scenarios':{}}
  hold=spec['universe'][0].split('/')[0] if row['is_comparator'] else None
  for mult in (1,2,3):
   arc=run(spec,markets,ratio,filters,mult,hold);cfg[row['name']]['scenarios'][str(mult)]=arc['summary'];gzwrite(out/f"{row['name']}_cost{mult}.json.gz",arc);allrows.append({'name':row['name'],'multiplier':mult,'is_comparator':row['is_comparator'],**arc['summary']})
  print(row['name'],*[round(cfg[row['name']]['scenarios'][str(x)]['net_return_pct'],4) for x in (1,2,3)],flush=True)
 for row in batch:
  if row['is_comparator']:continue
  s=json.loads((ROOT/row['spec']).read_text());p=s['parameters'];neighbors=[]
  for qrow in batch:
   if qrow['is_comparator']:continue
   q=json.loads((ROOT/qrow['spec']).read_text())['parameters']
   if abs(q['lookback_days']-p['lookback_days'])<=20 and abs(q['entry_zscore_threshold']-p['entry_zscore_threshold'])<=0.5:neighbors.append(qrow['name'])
  c=cfg[row['name']]['scenarios'];frac=sum(cfg[n]['scenarios']['3']['net_return_pct']>0 for n in neighbors)/len(neighbors)
  for m in ('1','2','3'):c[m]['neighborhood_positive_fraction_3x']=frac;c[m]['neighborhood_size']=len(neighbors)
  g={'all_costs_positive':all(c[str(m)]['net_return_pct']>0 for m in (1,2,3)),'positive_1x_folds':c['1']['positive_1x_folds'],'drawdown_under_25pct':c['3']['max_drawdown_pct']<=25,'neighborhood_fraction_at_least_0_60':frac>=0.60,'round_trips_at_least_2':c['1']['round_trips']>=2,'gross_to_cost_at_least_2_5':c['1']['gross_reference_pnl_to_cost'] is not None and c['1']['gross_reference_pnl_to_cost']>=2.5,'no_balance_violations':all(c[str(m)]['balance_violations']==0 for m in (1,2,3)),'terminal_flat':all(D(c[str(m)]['terminal_units'])==0 for m in (1,2,3))}
  cfg[row['name']]['gates']=g;cfg[row['name']]['status']='passed' if all([g['all_costs_positive'],g['positive_1x_folds']>=7,g['drawdown_under_25pct'],g['neighborhood_fraction_at_least_0_60'],g['round_trips_at_least_2'],g['gross_to_cost_at_least_2_5'],g['no_balance_violations'],g['terminal_flat']]) else 'rejected'
 ranked=sorted([x['name'] for x in batch if not x['is_comparator']],key=lambda n:cfg[n]['scenarios']['1']['net_return_pct'],reverse=True)
 report={'round':ROUND.name,'evaluation_started_utc':datetime.now(timezone.utc).isoformat(),'plan':plan,'data_manifest':manifest,'summary':{'candidate_configs':9,'comparators':2,'candidate_passed':sum(cfg[n]['status']=='passed' for n in ranked),'candidate_rejected':sum(cfg[n]['status']=='rejected' for n in ranked),'oos_days':360,'folds':12,'ranking_1x':ranked,'cost_scenes':len(allrows)},'configs':cfg,'scene_summaries':allrows}
 (ROUND/'report.json').write_text(json.dumps(canonical(report),indent=2,ensure_ascii=False)+'\n');print(json.dumps(report['summary'],ensure_ascii=False))
if __name__=='__main__':main()
